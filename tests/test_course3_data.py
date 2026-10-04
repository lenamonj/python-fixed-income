"""Checks on the Course 3 data: the synthetic spreads, the FRED-format samples, the Excel reference file, and the
capstone files.

Run with: python -m pytest
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import make_course3_data as c3  # noqa: E402

DATA = REPO / "data"
FILES = ["course3_synthetic_spreads.csv", "course3_fred_format_dgs10.json", "course3_fred_format_dgs2.json",
         "course3_capstone_extract.csv", "course3_capstone_answer_key.md", "course3_capstone_cover_note.txt"]
FRED_KEYS = ["realtime_start", "realtime_end", "observation_start", "observation_end", "units", "output_type",
             "file_type", "order_by", "sort_order", "count", "offset", "limit", "observations"]


@pytest.fixture(scope="module")
def treasury() -> pd.DataFrame:
    return pd.read_csv(DATA / "treasury_par_yields.csv", parse_dates=["date"], index_col="date")


@pytest.fixture(scope="module")
def spreads() -> pd.DataFrame:
    return pd.read_csv(DATA / "course3_synthetic_spreads.csv", parse_dates=["date"], index_col="date")


@pytest.fixture(scope="module")
def reference() -> pd.DataFrame:
    return pd.read_csv(DATA / "course3_excel_reference.csv", parse_dates=["date"], index_col="date")


@pytest.fixture(scope="module")
def built():
    return c3.build_capstone()


def longest_run(values: pd.Series) -> int:
    run_id = (values != values.shift()).cumsum()
    return int(values.groupby(run_id).size().max())


def test_generator_is_deterministic(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    for folder in (first, second):
        folder.mkdir()
        c3.write_files(folder)
    for name in FILES:
        assert (first / name).read_bytes() == (second / name).read_bytes()
        assert (first / name).read_bytes() == (DATA / name).read_bytes()
        assert b"\r\n" not in (DATA / name).read_bytes()


# ---- synthetic spreads
def test_synthetic_spreads(treasury: pd.DataFrame, spreads: pd.DataFrame) -> None:
    assert list(spreads.columns) == ["ig_spread_bp", "hy_spread_bp"]
    assert spreads.index.equals(treasury.index)
    assert spreads.notna().all().all()
    assert (spreads > 0).all().all()
    assert (spreads["hy_spread_bp"] > spreads["ig_spread_bp"]).all()
    for column in spreads.columns:
        assert longest_run(spreads[column]) < 5
    # pinned on 2026-09-30 to the book's market-value weighted oas, to one decimal
    holdings = pd.read_csv(DATA / "holdings.csv")
    holdings["grade"] = holdings["rating"].map(pd.read_csv(DATA / "ratings.csv").set_index("rating")["grade"])
    for grade, column in (("Investment Grade", "ig_spread_bp"), ("High Yield", "hy_spread_bp")):
        rows = holdings[holdings["grade"] == grade]
        weighted = (rows["oas"] * rows["market_value"]).sum() / rows["market_value"].sum()
        assert spreads.loc["2026-09-30", column] == round(weighted, 1)
    assert spreads.loc["2026-09-30"].tolist() == [98.8, 334.7]


# ---- FRED-format samples
@pytest.mark.parametrize("series_id, column", [("DGS10", "10 Yr"), ("DGS2", "2 Yr")])
def test_fred_format_sample(series_id: str, column: str) -> None:
    payload = json.loads((DATA / f"course3_fred_format_{series_id.lower()}.json").read_text(encoding="utf-8"))
    assert list(payload) == FRED_KEYS
    observations = payload["observations"]
    assert payload["count"] == len(observations) == 43
    assert all(list(o) == ["realtime_start", "realtime_end", "date", "value"] for o in observations)
    assert [o["date"] for o in observations] == list(pd.bdate_range("2026-08-03", "2026-09-30").strftime("%Y-%m-%d"))
    assert [o["date"] for o in observations if o["value"] == "."] == ["2026-09-07"]
    # every other value is the Treasury file's text, character for character
    text = pd.read_csv(DATA / "treasury_par_yields.csv", dtype=str).set_index("date")[column]
    for o in observations:
        if o["value"] != ".":
            assert o["value"] == text[o["date"]]
    assert {o["realtime_start"] for o in observations} == {"2026-10-02"}


# ---- Excel reference
def test_excel_reference_inputs_equal_treasury(treasury: pd.DataFrame, reference: pd.DataFrame) -> None:
    year = treasury[treasury.index.year == 2026]
    assert len(reference) == 190
    assert reference.index.equals(year.index)
    for column in ["2 Yr", "5 Yr", "10 Yr", "30 Yr"]:
        assert (reference[column] == year[column]).all()


def test_excel_reference_identities(treasury: pd.DataFrame, reference: pd.DataFrame) -> None:
    previous_10y = treasury["10 Yr"].shift(1).reindex(reference.index)
    assert ((reference["chg_10y_bp"] - (reference["10 Yr"] - previous_10y) * 100).abs() <= 1e-9).all()
    assert ((reference["slope_2s10s_bp"] - (reference["10 Yr"] - reference["2 Yr"]) * 100).abs() <= 1e-9).all()
    fly = (2 * reference["5 Yr"] - reference["2 Yr"] - reference["10 Yr"]) * 100
    assert ((reference["fly_2s5s10s_bp"] - fly).abs() <= 1e-9).all()
    annual = reference["vol21_10y_bp"] * math.sqrt(252)
    assert ((reference["vol21_10y_annual_bp"] - annual).abs() <= 1e-9).all()
    # each formula is the first row's, filled down
    assert reference["vol21_10y_bp_formula"].iloc[0] == "=STDEV.S(F242:F262)"
    assert reference["vol21_10y_bp_formula"].iloc[-1] == "=STDEV.S(F431:F451)"


# ---- capstone
def read_extract() -> pd.DataFrame:
    return pd.read_csv(DATA / "course3_capstone_extract.csv", dtype=str)


def clean_rows(treasury: pd.DataFrame, spreads: pd.DataFrame) -> pd.DataFrame:
    """The market days of the extract period from the two clean sources."""
    joined = treasury[c3.YIELD_COLUMNS].join(spreads, validate="one_to_one")
    return joined.loc[c3.EXTRACT_START:c3.EXTRACT_END]


def test_capstone_planted_problems_present(built) -> None:
    clean, _, planted = built
    extract = read_extract()
    key = (DATA / "course3_capstone_answer_key.md").read_text(encoding="utf-8")
    assert list(extract.columns) == c3.EXTRACT_COLUMNS
    assert len(clean) == 66 and len(extract) == 69

    dot_rows = extract[(extract[c3.EXTRACT_COLUMNS[1:]] == ".").all(axis=1)]
    assert dot_rows["date"].tolist() == ["2026-09-07"]
    assert (extract == ".").sum().sum() == 6
    mmdd = extract["date"].str.fullmatch(r"\d{2}/\d{2}/\d{4}")
    assert mmdd.sum() == c3.N_MMDDYYYY
    dates = pd.to_datetime(extract["date"].where(~mmdd, pd.to_datetime(extract["date"][mmdd], format="%m/%d/%Y")
                                                 .dt.strftime("%Y-%m-%d")), format="%Y-%m-%d")
    assert (dates.dt.dayofweek >= 5).sum() == c3.N_WEEKEND
    assert extract.duplicated().sum() == c3.N_DUPLICATES
    numbers = extract[extract["date"] != "2026-09-07"].set_index("date").astype(float)
    assert (numbers[c3.SPREAD_COLUMNS] < 20).sum().sum() == c3.N_SPREAD_PERCENT
    assert (numbers[c3.YIELD_COLUMNS] > 20).sum().sum() == c3.N_YIELD_BP
    market_days = {row["date"] for row in clean}
    assert len(market_days - set(dates.dt.strftime("%Y-%m-%d"))) == c3.N_MISSING
    distinct = extract.drop_duplicates()
    stale = distinct.loc[distinct["date"] != "2026-09-07", c3.STALE_COLUMN].astype(float).reset_index(drop=True)
    assert longest_run(stale) == c3.STALE_RUN_LENGTH

    counts = {"holiday": 1, "weekend": c3.N_WEEKEND, "missing": c3.N_MISSING, "duplicates": c3.N_DUPLICATES,
              "mmddyyyy": c3.N_MMDDYYYY, "spread_percent": c3.N_SPREAD_PERCENT, "yield_bp": c3.N_YIELD_BP,
              "stale_run": c3.STALE_RUN_LENGTH - 1}
    assert {name: len(planted[name]) for name in counts} == counts
    # no market day carries two problems, and every planted date is named in the answer key
    planted_dates = [item["date"] for name in counts for item in planted[name]] + [planted["stale_run_first_date"]]
    assert len(planted_dates) == len(set(planted_dates))
    assert all(f"`{d}`" in key for d in planted_dates)


def test_capstone_fixes_restore_clean_rows(treasury: pd.DataFrame, spreads: pd.DataFrame, built) -> None:
    _, _, planted = built
    clean = clean_rows(treasury, spreads)
    raw = read_extract()

    # the fixes in the order of the answer key
    fixed = raw[raw["date"] != "2026-09-07"].copy()
    mmdd = fixed["date"].str.fullmatch(r"\d{2}/\d{2}/\d{4}")
    fixed.loc[mmdd, "date"] = pd.to_datetime(fixed.loc[mmdd, "date"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
    fixed["date"] = pd.to_datetime(fixed["date"], format="%Y-%m-%d")
    fixed = fixed[fixed["date"].dt.dayofweek < 5].drop_duplicates()
    fixed = fixed.set_index("date").astype(float)
    for column in c3.SPREAD_COLUMNS:
        low = fixed[column] < 20
        fixed.loc[low, column] = (fixed.loc[low, column] * 100).round(1)
    for column in c3.YIELD_COLUMNS:
        high = fixed[column] > 20
        fixed.loc[high, column] = (fixed.loc[high, column] / 100).round(2)
    # the missing day and the stale run are restored from the clean source, named in the answer key
    missing = pd.Timestamp(planted["missing"][0]["date"])
    fixed.loc[missing] = clean.loc[missing]
    fixed = fixed.sort_index()
    for item in planted["stale_run"]:
        assert fixed.loc[item["date"], c3.STALE_COLUMN] == float(item["written"])
        fixed.loc[item["date"], c3.STALE_COLUMN] = float(item["clean"])

    fixed.index.name = clean.index.name
    pd.testing.assert_frame_equal(fixed, clean, check_exact=True, check_freq=False)


def test_capstone_cover_note_figures(treasury: pd.DataFrame, spreads: pd.DataFrame) -> None:
    clean = clean_rows(treasury, spreads)
    note = (DATA / "course3_capstone_cover_note.txt").read_text(encoding="utf-8")
    last = pd.read_csv(DATA / "treasury_par_yields.csv", dtype=str).set_index("date").loc["2026-10-02"]
    assert f"Market days:   {len(clean)}" in note
    assert "2026-07-01 to 2026-10-02" in note
    for column in c3.YIELD_COLUMNS:
        assert f"{column:<8} {last[column]} percent" in note
    assert f"ig_spread_bp   {spreads.loc['2026-10-02', 'ig_spread_bp']:.1f}" in note
    assert f"hy_spread_bp   {spreads.loc['2026-10-02', 'hy_spread_bp']:.1f}" in note
    assert "synthetic" in note
    # the note names no problem
    for word in ("duplicate", "missing", "stale", "weekend", "holiday", "error"):
        assert word not in note.lower()
