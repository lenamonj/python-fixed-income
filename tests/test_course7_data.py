"""Checks on the Course 7 data (DATA.md, "Added 2026-10-07: Course 7 data").

Run with: python -m pytest

- FOMC statements 2000 to 2026 (tools/get_fomc_history.py): rows, columns, dates, addresses, no HTML, and every
  2021 to 2026 text equal to data/fomc_statements.csv (the two tools agree).
- Indentures (tools/get_indentures.py): the SHA-256 of each .htm as filed; the article 4 sections found; each .txt
  equal to the reference textkit.html_to_text of its .htm (skipped, with the reason, without the private build
  folder that holds the reference textkit).
- The Boyd 10-K and the indenture PDF: SHA-256, and the PDF's page count and redemption table.
- Risk factors (tools/get_edgar_filings.py): rows per filing, no empty heading or text, order 1 to n.
- 8-K item sections (tools/get_8k_items.py): rows per item and per year, no text starting with "Item", at most 300
  words, item codes as text, accessions unique per item.
- The GloVe subset (tools/make_glove_subset.py): word count, shape, float32, unique words, course terms present.
- The model outputs (tools/make_8k_model_outputs.py): one unit-length embedding per section; one zero-shot row per
  validation and test section, rows summing to 1, the pinned revision.
- Saved LLM responses: every file parses and holds no key-like string or header.
"""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
INDENTURES = DATA / "course7_indentures"
GLOVE = DATA / "course7_glove_6b_100d.npz"
ASSEMBLE = REPO / "instructor" / "_build" / "course7" / "assemble.py"
SHA256 = {
    "course7_indentures/boyd_2021.htm": "b69736238edfc629458185645b39746ecc6b195d10a6d9fff7409cfcf91f3cbe",
    "course7_indentures/levi_2006.htm": "58c68c2527ecdb364a48f0a78d823b904e9b8838f3f96c6889efab55f8810fa6",
    "course7_indentures/lamar_2007.htm": "80ac6087db6d64a00a4735230553a50b8d1f3831be537e2a710ed74f9e7cbb63",
    "course7_boyd_10k_2025.htm": "e5ecbcd3c179182cf9d2985d1d7b6d3ece0dc95bef3e592ed75392fd1ab055ec",
    "course7_boyd_2021_indenture.pdf": "b77925aa3e56c43af3192cbfdae5a6ac26dce1189f208f37eeb2096cb86a09e6",
}
ARTICLE_4 = {
    "boyd_2021": [f"4.{n:02d}" for n in range(1, 21)],
    "levi_2006": [f"4.{n:02d}" for n in range(1, 14)],
    "lamar_2007": [f"4.{n:02d}" for n in range(1, 20)],
}
RISK_FACTOR_ROWS = {"Boyd Gaming Corporation": 18, "Levi Strauss & Co.": 48, "Lamar Media Corp.": 33}
ZERO_SHOT_REVISION = "c07f66d9cbf781191bee66edfe8ad7856f045781"
# rows per item and filing year, as tools/get_8k_items.py wrote them (DATA.md): item -> counts for 2019 to 2025
EIGHTK_BY_YEAR = {
    "1.01": [100, 100, 100, 100, 100, 100, 100],
    "1.03": [96, 100, 65, 35, 100, 100, 84],
    "2.02": [100, 100, 100, 100, 100, 100, 100],
    "2.03": [100, 100, 100, 100, 100, 100, 100],
    "2.04": [100, 100, 85, 98, 100, 100, 100],
    "2.06": [73, 67, 36, 42, 53, 41, 51],
    "3.01": [100, 100, 100, 100, 100, 100, 100],
    "5.02": [100, 100, 100, 100, 100, 100, 100],
}
EIGHTK_COUNTS = {f"{item} {2019 + k}": n for item, counts in EIGHTK_BY_YEAR.items() for k, n in enumerate(counts)}


@pytest.fixture(scope="module")
def fomc() -> pd.DataFrame:
    return pd.read_csv(DATA / "course7_fomc_statements.csv")


@pytest.fixture(scope="module")
def textkit():
    """The reference textkit, assembled from the private build folder; the tests that need it skip without it."""
    if not ASSEMBLE.is_file():
        pytest.skip("the reference textkit lives in the private build folder instructor/_build/course7")
    sys.path.insert(0, str(REPO / "tools"))
    import course7_reference
    return course7_reference.textkit()


@pytest.fixture(scope="module")
def eightk() -> pd.DataFrame:
    return pd.read_csv(DATA / "course7_8k_items.csv", dtype={"item": str})


def test_fomc_rows_and_dates(fomc: pd.DataFrame) -> None:
    assert list(fomc.columns) == ["date", "url", "scheduled", "text"]
    assert len(fomc) == 226
    dates = pd.to_datetime(fomc["date"], format="%Y-%m-%d")
    assert dates.is_unique and dates.is_monotonic_increasing
    assert (fomc["date"].iloc[0], fomc["date"].iloc[-1]) == ("2000-02-02", "2026-09-16")
    assert fomc["scheduled"].dtype == bool and int((~fomc["scheduled"]).sum()) == 13
    # the unscheduled releases the spec names
    unscheduled = set(fomc.loc[~fomc["scheduled"], "date"])
    assert {"2001-01-03", "2008-01-22", "2020-03-15"} <= unscheduled


def test_fomc_urls_and_text(fomc: pd.DataFrame) -> None:
    assert fomc["url"].str.startswith("https://www.federalreserve.gov/").all()
    # each address carries its statement's date
    assert all(date.replace("-", "") in url for date, url in zip(fomc["date"], fomc["url"]))
    assert not fomc["text"].str.contains(r"[<>]|&[a-z]+;|Release Date|Last update|For immediate release",
                                         regex=True).any()
    assert fomc["text"].str.len().min() > 300
    # white space normalized and every paragraph ends as a sentence does
    for text in fomc["text"]:
        assert "  " not in text and text == text.strip()
        assert all(re.search(r"[.:;][\"')\N{RIGHT DOUBLE QUOTATION MARK}]?$", paragraph)
                   for paragraph in text.split("\n"))


def test_fomc_agrees_with_course1_file(fomc: pd.DataFrame) -> None:
    course1 = pd.read_csv(DATA / "fomc_statements.csv")
    later = fomc[fomc["date"] >= "2021-01-01"].reset_index(drop=True)
    assert len(later) == len(course1) == 46
    assert (later["date"] == course1["date"]).all()
    assert (later["url"] == course1["url"]).all()
    assert (later["text"] == course1["text"]).all()


@pytest.mark.parametrize("name", sorted(SHA256))
def test_edgar_documents_as_filed(name: str) -> None:
    assert hashlib.sha256((DATA / name).read_bytes()).hexdigest() == SHA256[name]


def test_indenture_sections(textkit) -> None:
    for name, numbers in ARTICLE_4.items():
        text = (INDENTURES / f"{name}.txt").read_text(encoding="utf-8")
        sections = textkit.find_sections(text)
        assert [n for n in sections["number"] if n.startswith("4.")] == numbers
        assert sections["number"].iloc[0] == "1.01"


def test_indenture_text_is_html_to_text(textkit) -> None:
    for name in ARTICLE_4:
        html = (INDENTURES / f"{name}.htm").read_bytes()
        assert (INDENTURES / f"{name}.txt").read_text(encoding="utf-8") == textkit.html_to_text(html)


def test_indenture_pdf() -> None:
    from pypdf import PdfReader
    reader = PdfReader(DATA / "course7_boyd_2021_indenture.pdf")
    assert len(reader.pages) == 132
    page = reader.pages[51].extract_text()
    for line in ("2026", "102.375%", "2027", "101.583%", "2028", "100.792%", "2029 and thereafter", "100.000%"):
        assert line in page


def test_risk_factors() -> None:
    frame = pd.read_csv(DATA / "course7_risk_factors.csv")
    assert list(frame.columns) == ["cik", "company", "form", "filed", "accession", "url", "order", "category",
                                   "heading", "text"]
    assert frame.groupby("company").size().to_dict() == RISK_FACTOR_ROWS
    assert frame["heading"].str.len().min() > 10 and frame["text"].str.split().str.len().min() >= 20
    for _, part in frame.groupby("company"):
        assert list(part["order"]) == list(range(1, len(part) + 1))
    assert (frame["form"] == "10-K").all() and frame["url"].str.startswith("https://www.sec.gov/Archives/").all()


def test_8k_rows_per_item_and_year(eightk: pd.DataFrame) -> None:
    counts = eightk.groupby([eightk["item"], eightk["filed"].str[:4]]).size()
    assert {f"{item} {year}": int(n) for (item, year), n in counts.items()} == EIGHTK_COUNTS
    assert counts.max() <= 100 and len(eightk) == 5_126


def test_8k_text_rules(eightk: pd.DataFrame) -> None:
    assert list(eightk.columns) == ["accession", "cik", "company", "filed", "item", "item_title", "words", "text",
                                    "url"]
    assert not eightk["text"].str.match(r"(?i)\s*item\b").any()
    assert eightk["text"].str.split().str.len().max() <= 300
    assert eightk["item"].map(type).eq(str).all()
    assert set(eightk["item"]) == {"1.01", "1.03", "2.02", "2.03", "2.04", "2.06", "3.01", "5.02"}
    assert not eightk.duplicated(["accession", "item"]).any()
    assert eightk["filed"].between("2019-01-01", "2025-12-31").all()


def test_glove_subset() -> None:
    with zipfile.ZipFile(GLOVE) as archive:
        assert sorted(archive.namelist()) == ["vectors.npy", "words.npy"]
    with np.load(GLOVE, allow_pickle=False) as data:
        vectors, words = data["vectors"], [str(w) for w in data["words"]]
    assert vectors.dtype == np.float32 and vectors.shape == (len(words), 100)
    assert len(words) == len(set(words))
    assert words[:5] == ["the", ",", ".", "of", "to"]
    assert all(word == word.lower() for word in words)
    terms = ["bond", "bonds", "indenture", "covenant", "covenants", "trustee", "notes", "indebtedness", "liens",
             "collateral", "inflation", "unemployment", "committee", "federal", "funds", "rate", "default",
             "bankruptcy", "dividend", "maturity"]
    assert [term for term in terms if term not in set(words)] == []


def test_model_outputs(eightk: pd.DataFrame) -> None:
    vectors = np.load(DATA / "course7_8k_minilm.npy", allow_pickle=False)
    assert vectors.dtype == np.float32 and vectors.shape == (len(eightk), 384)
    assert np.allclose(np.linalg.norm(vectors, axis=1), 1.0, atol=1e-5)
    scores = pd.read_csv(DATA / "course7_8k_zero_shot.csv", dtype={"item": str})
    later = eightk[eightk["filed"].str[:4].isin(["2024", "2025"])]
    assert len(scores) == len(later) and (scores["accession"].to_numpy() == later["accession"].to_numpy()).all()
    columns = [c for c in scores.columns if c.startswith("score_")]
    assert len(columns) == 8 and np.allclose(scores[columns].sum(axis=1), 1.0, atol=1e-5)
    assert (scores["revision"] == ZERO_SHOT_REVISION).all()


def test_llm_responses() -> None:
    folder = DATA / "course7_llm_responses"
    for path in sorted(folder.rglob("*.json")) if folder.is_dir() else []:
        raw = path.read_text(encoding="utf-8")
        record = json.loads(raw)
        # no key-like string anywhere; the header and key words only in field names, since the request's messages
        # carry indenture text, which may say "authorizations" (Boyd's definition of Gaming License)
        assert not re.search(r"sk-or-|Bearer", raw), path.name

        def field_names(value):
            if isinstance(value, dict):
                for name, inner in value.items():
                    yield name
                    yield from field_names(inner)
            elif isinstance(value, list):
                for inner in value:
                    yield from field_names(inner)
        assert not any(re.search(r"authorization|api[_-]?key|header|bearer", name, re.I)
                       for name in field_names(record)), path.name
