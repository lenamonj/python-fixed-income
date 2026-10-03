"""Checks on the Course 1 project data. Run with: python -m pytest"""
import sys
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import make_project_data as project  # noqa: E402

DATA = REPO / "data"
FILES = ["project_holdings.csv", "project_answer_key.md", "project_cover_note.txt"]


@pytest.fixture(scope="module")
def built() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    return project.build()


@pytest.fixture(scope="module")
def extract() -> pd.DataFrame:
    return pd.read_csv(DATA / "project_holdings.csv")


def test_generator_is_deterministic(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    for folder in (first, second):
        folder.mkdir()
        project.write_files(folder)
    for name in FILES:
        assert (first / name).read_bytes() == (second / name).read_bytes()
        assert (first / name).read_bytes() == (DATA / name).read_bytes()


def test_layout_matches_the_week_3_file(extract: pd.DataFrame) -> None:
    assert list(extract.columns) == list(pd.read_csv(DATA / "holdings_messy.csv", nrows=0).columns)
    assert set(extract["as_of_date"]) == {"2026-10-30"}


def test_every_bond_joins(extract: pd.DataFrame) -> None:
    benchmark = pd.read_csv(DATA / "benchmark.csv")
    september = pd.read_csv(DATA / "holdings.csv")
    assert set(extract["cusip"]) <= set(benchmark["cusip"]) | set(september["cusip"])
    assert set(extract["ticker"]) <= set(pd.read_csv(DATA / "issuers.csv")["ticker"])
    assert set(extract["rating"]) <= set(pd.read_csv(DATA / "ratings.csv")["rating"])


def test_clean_book_is_internally_consistent(built) -> None:
    clean, _, _ = built
    assert clean["cusip"].is_unique
    worked_out = clean["par_held"] * (clean["price"] + clean["accrued"]) / 100
    assert ((worked_out - clean["market_value"]).abs() < 0.005).all()
    assert (clean["spread_duration"] == clean["duration"]).all()
    assert ((clean["dts"] - clean["spread_duration"] * clean["oas"]).abs() <= 0.05 + 1e-9).all()
    assert (clean["par_held"] > 0).all()
    assert (clean["par_held"] <= clean["amount_outstanding"]).all()
    assert (clean["maturity"] > clean["as_of_date"]).all()


def test_month_differs_from_september(built) -> None:
    clean, _, _ = built
    september = pd.read_csv(DATA / "holdings.csv")
    assert len(set(september["cusip"]) - set(clean["cusip"])) == project.SOLD
    assert len(set(clean["cusip"]) - set(september["cusip"])) == project.BOUGHT


def test_planted_problems_are_present_as_stated(built, extract: pd.DataFrame) -> None:
    clean, _, planted = built
    key = (DATA / "project_answer_key.md").read_text(encoding="utf-8")

    assert len(extract) == len(clean) + project.N_DUPLICATES
    assert extract.duplicated().sum() == project.N_DUPLICATES
    assert set(extract.loc[extract.duplicated(), "cusip"]) == {item["cusip"] for item in planted["duplicates"]}

    untidy = extract["sector"] != extract["sector"].str.strip().str.title()
    assert untidy.sum() == project.N_SECTOR
    assert extract["oas"].isna().sum() == project.N_MISSING_OAS
    assert extract.isna().sum().sum() == project.N_MISSING_OAS
    assert ((extract["price"] < 10) | (extract["price"] > 1000)).sum() == project.N_PRICE
    assert (extract["par_held"] <= 0).sum() == project.N_NEGATIVE_FACE
    assert (extract["maturity"] <= extract["as_of_date"]).sum() == project.N_MATURITY

    # market value fails to tie out in the wrong-price and negative-face rows only
    gap = (extract["par_held"] * (extract["price"] + extract["accrued"]) / 100 - extract["market_value"]).abs()
    assert (gap > 1).sum() == project.N_PRICE + project.N_NEGATIVE_FACE

    # every planted row is named in the answer key, and no row carries two problems
    planted_cusips = [item["cusip"] for items in planted.values() for item in items]
    assert len(planted_cusips) == len(set(planted_cusips))
    assert all(f"`{cusip}`" in key for cusip in planted_cusips)

    # checks the answer key says are clean
    assert (extract["ticker"] == extract["ticker"].str.strip().str.upper()).all()
    assert (extract["price_date"] == extract["as_of_date"]).all()
    assert extract["cusip"].str.len().eq(9).all()


def test_fixes_in_the_answer_key_restore_the_control_totals(built, extract: pd.DataFrame) -> None:
    clean, _, _ = built
    totals = project.control_totals(clean)
    benchmark = pd.read_csv(DATA / "benchmark.csv")

    book = extract.drop_duplicates().reset_index(drop=True)
    book["sector"] = book["sector"].str.strip().str.title()
    book["oas"] = book["oas"].fillna((book["dts"] / book["spread_duration"]).round())
    book.loc[book["price"] < 10, "price"] = (book["price"] * 100).round(3)
    book.loc[book["price"] > 1000, "price"] = (book["price"] / 100).round(3)
    book["par_held"] = book["par_held"].abs()
    matured = book["maturity"] <= book["as_of_date"]
    book.loc[matured, "maturity"] = book.loc[matured, "cusip"].map(benchmark.set_index("cusip")["maturity"])

    assert len(book) == totals["bonds"]
    assert book["par_held"].sum() == totals["face"]
    assert round(book["market_value"].sum(), 2) == totals["market_value"]
    # the fixed extract is the clean book, cell for cell
    pd.testing.assert_frame_equal(book.astype({"oas": "int64"}), clean, check_exact=False, atol=1e-9)

    note = (DATA / "project_cover_note.txt").read_text(encoding="utf-8")
    for figure in (f"{totals['bonds']:,}", f"{totals['face']:,}", f"{totals['market_value']:,.2f}"):
        assert figure in note
