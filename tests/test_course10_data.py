"""Checks on the Course 10 data (DATA.md, "Added 2026-10-12: Course 10 data").

Run with: python -m pytest

- The 10-K PDF (tools/make_course10_pdf.py): page count and SHA-256 as recorded; every page's text, reduced to letters
  and digits, found in the 10-K's HTML text the same way, except the two pages DATA.md lists (an image's file name
  that Edge printed where the image was missing).
- The 10-Q (tools/get_course10_filings.py): SHA-256 as filed; textkit.split_items finds Part I's items 1 to 4 and
  Part II's items 1, 1A, 2, 5, and 6.
- The question set (data/course10_questions.csv, written by hand): columns; ids unique; splits as DATA.md states; every
  quote found on its page of the 10-K PDF, in its item of the 10-Q, or in its section of an indenture, and every
  10-K row's item among the items of its page; every number of an answer key inside its quotes; not_in_corpus and
  adversarial rows with no page and no quote; no question outside the adversarial rows holding a word of the prompt
  scan.
- The committed embeddings (data/course10_embeddings/), when present: one unit-length float32 row per chunk, and the
  sidecar's chunk-text hash equal to the reference recursive_split's chunks today.
- The recorded runs (data/course10_rag_runs/dayNN/), when present: Course 8's checks (the four fields, no header or
  key field, no sk- or Bearer string).
- The human labels (data/course10_human_labels.csv), when present: every answer_key names a saved run file, labels
  in the stated set.

The checks that need the reference textkit or ragkit skip, with the reason, without the private build folder.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
PDF = DATA / "course10_boyd_10k_2025.pdf"
TENK = DATA / "course7_boyd_10k_2025.htm"
TENQ = DATA / "course10_boyd_10q_2026q2.htm"
QUESTIONS = DATA / "course10_questions.csv"
EMBEDDINGS = DATA / "course10_embeddings"
RUNS = DATA / "course10_rag_runs"
LABELS = DATA / "course10_human_labels.csv"
sys.path.insert(0, str(REPO / "tools"))
import course7_reference  # noqa: E402
import course10_reference  # noqa: E402

PDF_PAGES = 113
PDF_SHA256 = "20cab642aa721a0ffdd448476c8b81b170859b5b8f77f4f29a55252a824d3479"
# pages whose text holds an image's file name (Edge printed it where the image was missing): DATA.md
PDF_PAGES_NOT_FOUND = {1, 25}
TENQ_SHA256 = "994a88f1e1226c117d941bf19bc2512fa81df78fe9ab9970bc9a340b4e3c14be"
COLUMNS = ["id", "split", "doc", "question", "answer_key", "key_kind", "expected_doc", "expected_item",
           "expected_page", "key_quote", "written_from", "notes"]
SPLITS = {"arc": 5, "dev": 25, "test": 20, "capstone": 25}
KINDS = {"number", "text", "not_in_corpus", "adversarial"}
INDENTURES = {"boyd2021": "boyd_2021", "levi2006": "levi_2006", "lamar2007": "lamar_2007"}
PROMPT_WORDS = re.compile(r"\brecommend\w*|\bratings?\b|\brank\w*|\bshould\b|\bbuy\b|\bsell\b|\battractive\b"
                          r"|\bforecast\w*|\boutlook\w*|\bis this a good\b", re.I)
NUMBER = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")
KEY_LIKE = re.compile(r"sk-or-(?!FAKEFAKEFAKE)[A-Za-z0-9-]+|\bsk-[A-Za-z0-9_-]{16,}|\bBearer\b")
HEADER_FIELD = re.compile(r"authorization|api[_-]?key|header|bearer|cookie", re.I)


def squeeze(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def squash(text: str) -> str:
    return " ".join(text.split())


@pytest.fixture(scope="module")
def textkit():
    """The reference textkit, assembled from the private build folder; the tests that need it skip without it."""
    if not course7_reference.ASSEMBLE.is_file():
        pytest.skip("the reference textkit lives in the private build folder instructor/_build/course7")
    return course7_reference.textkit()


@pytest.fixture(scope="module")
def ragkit():
    if not course10_reference.available():
        pytest.skip("the reference ragkit lives in the private build folder instructor/_build/course10")
    return course10_reference.ragkit()


@pytest.fixture(scope="module")
def questions() -> pd.DataFrame:
    return pd.read_csv(QUESTIONS, dtype=str, keep_default_na=False)


def test_pdf_pages_and_hash():
    from pypdf import PdfReader
    assert hashlib.sha256(PDF.read_bytes()).hexdigest() == PDF_SHA256
    assert len(PdfReader(PDF).pages) == PDF_PAGES


def test_pdf_text_found_in_html(textkit):
    whole = squeeze(textkit.html_to_text(TENK.read_bytes()))
    missing = {n for n, text in enumerate(textkit.pdf_text(PDF), start=1) if squeeze(text) not in whole}
    assert missing == PDF_PAGES_NOT_FOUND


def test_10q_hash_and_items(textkit):
    raw = TENQ.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == TENQ_SHA256
    text = textkit.normalize_text(textkit.html_to_text(raw))
    cut = text.index("\nPART II. Other Information")
    assert list(textkit.split_items(text[:cut], ["1", "2", "3", "4"])["item"]) == ["1", "2", "3", "4"]
    assert list(textkit.split_items(text[cut:], ["1", "1A", "2", "5", "6"])["item"]) == ["1", "1A", "2", "5", "6"]


def test_questions_shape(questions: pd.DataFrame):
    assert list(questions.columns) == COLUMNS and questions["id"].is_unique
    assert questions["split"].value_counts().to_dict() == SPLITS
    assert set(questions["key_kind"]) == KINDS
    raw = QUESTIONS.read_bytes()
    assert raw.isascii() and b"\r\n" not in raw


def test_questions_empty_where_unanswerable(questions: pd.DataFrame):
    blank = questions[questions["key_kind"].isin(["not_in_corpus", "adversarial"])]
    assert (blank["expected_page"] == "").all() and (blank["key_quote"] == "").all()
    assert (blank.loc[blank["key_kind"] == "not_in_corpus", "answer_key"] == "NOT IN CORPUS").all()
    asked = questions.loc[questions["key_kind"] != "adversarial", "question"]
    assert not asked.str.contains(PROMPT_WORDS).any()


def test_question_keys_inside_their_quotes(questions: pd.DataFrame):
    for row in questions[questions["key_quote"] != ""].itertuples():
        quotes = " ".join(row.key_quote.split(" | "))
        assert all(n in quotes for n in NUMBER.findall(row.answer_key)), row.id


def test_question_quotes_where_stated(textkit, questions: pd.DataFrame):
    pages = [squash(textkit.normalize_text(p)) for p in textkit.pdf_text(PDF)]
    tenq = textkit.normalize_text(textkit.html_to_text(TENQ.read_bytes()))
    part_one = textkit.split_items(tenq[:tenq.index("\nPART II. Other Information")], ["1", "2", "3", "4"])
    indentures = {d: (DATA / "course7_indentures" / f"{f}.txt").read_text(encoding="utf-8")
                  for d, f in INDENTURES.items()}
    for row in questions[questions["key_quote"] != ""].itertuples():
        if row.expected_doc == "boyd10k":
            haystack = pages[int(row.expected_page) - 1]
        elif row.expected_doc == "boyd10q":
            assert row.expected_item.startswith("I."), row.id
            item = row.expected_item.split(".")[1]
            haystack = squash(part_one.loc[part_one["item"] == item, "text"].iloc[0])
        else:
            text = indentures[row.expected_doc]
            if row.expected_item:
                sections = textkit.find_sections(text)
                found = sections.loc[sections["number"] == row.expected_item].iloc[0]
                text = text[found["start"]:found["end"]]
            haystack = squash(textkit.normalize_text(text))
        for quote in row.key_quote.split(" | "):
            assert squash(textkit.normalize_text(quote)) in haystack, row.id


def test_question_items_on_their_pages(ragkit, textkit, questions: pd.DataFrame):
    items = textkit.split_items(textkit.html_to_text(TENK.read_bytes()), ragkit.TEN_K_ITEMS)
    table = ragkit.page_items(ragkit.pdf_pages(PDF), items)
    for row in questions[questions["expected_doc"] == "boyd10k"].itertuples():
        on_page = set(table.loc[table["page"] == int(row.expected_page), "item"])
        assert row.expected_item in on_page, row.id


def test_embeddings(ragkit):
    files = sorted(EMBEDDINGS.glob("*.npy")) if EMBEDDINGS.is_dir() else []
    if not files:
        pytest.skip("no committed embeddings yet")
    for path in files:
        sidecar = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
        matrix = np.load(path)
        assert matrix.dtype == np.float32 and len(matrix) == sidecar["chunks"], path.name
        assert np.allclose(np.linalg.norm(matrix, axis=1), 1.0, atol=1e-6), path.name
        assert sidecar["model"]["revision"] == ragkit.EMBEDDERS[sidecar["model"]["key"]]["revision"], path.name


def test_recorded_runs():
    files = sorted(RUNS.glob("day*/*.json")) if RUNS.is_dir() else []
    for path in files:
        raw = path.read_text(encoding="utf-8")
        record = json.loads(raw)
        assert set(record) == {"path", "recorded", "request", "response"}, path.name
        assert not KEY_LIKE.search(raw) and not re.search(r"\bsk-", raw), path.name

        def keys(value):
            if isinstance(value, dict):
                for k, v in value.items():
                    yield k
                    yield from keys(v)
            elif isinstance(value, list):
                for v in value:
                    yield from keys(v)
        assert not any(HEADER_FIELD.search(str(k)) for k in keys(record)), path.name


def test_human_labels():
    if not LABELS.is_file():
        pytest.skip("no human labels yet (Jeff labels day 12's answers)")
    labels = pd.read_csv(LABELS, dtype=str, keep_default_na=False)
    saved = {p.stem for p in RUNS.glob("day*/*.json")}
    assert set(labels["answer_key"]) <= saved
    assert set(labels["grounded"]) <= {"yes", "partly", "no"} and set(labels["relevant"]) <= {"yes", "partly", "no"}
