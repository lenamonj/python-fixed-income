"""Checks on the Course 2 data: the curve file, the capstone files, and the Excel reference file.

Run with: python -m pytest
"""
import math
import re
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import make_course2_data as c2  # noqa: E402

DATA = REPO / "data"
FILES = ["course2_treasury_curve.csv", "course2_capstone_holdings.csv", "course2_capstone_answer_key.md",
         "course2_capstone_cover_note.txt"]
AS_OF = c2.AS_OF
ROUNDED = 0.0005 + 1e-9  # a value the file rounds to 3 decimals, against the unrounded calculation


@pytest.fixture(scope="module")
def built():
    return c2.build()


@pytest.fixture(scope="module")
def extract() -> pd.DataFrame:
    return pd.read_csv(DATA / "course2_capstone_holdings.csv")


@pytest.fixture(scope="module")
def reference() -> pd.DataFrame:
    return pd.read_csv(DATA / "bondmath_excel_reference.csv")


def d(text: str) -> date:
    return date.fromisoformat(text)


# ---- the curve file
def test_curve_file_equals_the_formula() -> None:
    curve = pd.read_csv(DATA / "course2_treasury_curve.csv")
    assert list(curve.columns) == ["tenor_years", "yield_pct"]
    assert curve["tenor_years"].tolist() == [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
    for tenor, yield_pct in zip(curve["tenor_years"], curve["yield_pct"]):
        assert yield_pct == c2.round3(3.55 + 1.05 * (1 - math.exp(-tenor / 7)))


# ---- the capstone files
def test_generator_is_deterministic(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    for folder in (first, second):
        folder.mkdir()
        c2.write_files(folder)
    for name in FILES:
        assert (first / name).read_bytes() == (second / name).read_bytes()
        assert (first / name).read_bytes() == (DATA / name).read_bytes()
        assert b"\r\n" not in (DATA / name).read_bytes()


def test_layout_matches_the_course1_file(extract: pd.DataFrame) -> None:
    assert list(extract.columns) == list(pd.read_csv(DATA / "holdings_messy.csv", nrows=0).columns)
    assert set(extract["as_of_date"]) == {"2026-11-30"}


def test_every_bond_joins_and_every_cusip_is_valid(built, extract: pd.DataFrame) -> None:
    _, _, _, new_cusips = built
    benchmark = pd.read_csv(DATA / "benchmark.csv")
    assert set(extract["cusip"]) <= set(benchmark["cusip"]) | set(new_cusips)
    assert set(extract["ticker"]) <= set(pd.read_csv(DATA / "issuers.csv")["ticker"])
    assert set(extract["rating"]) <= set(pd.read_csv(DATA / "ratings.csv")["rating"])
    assert all(re.fullmatch(r"99[0-9A-Z]{7}", c) and c2.cusip_check_digit(c[:8]) == c[8] for c in extract["cusip"])
    # each new bond uses its issuer's number from benchmark.csv and collides with no CUSIP in data/
    for cusip, spec in zip(new_cusips, c2.NEW_BONDS):
        assert cusip[:6] in set(benchmark.loc[benchmark["ticker"] == spec["ticker"], "cusip"].str[:6])
        assert cusip not in c2.all_data_cusips()


def test_clean_book_follows_the_course_conventions(built) -> None:
    clean, _, _, _ = built
    assert clean["cusip"].is_unique
    assert (clean["par_held"] > 0).all() and (clean["par_held"] <= clean["amount_outstanding"]).all()
    for row in clean.itertuples():
        maturity = d(row.maturity)
        years = c2.days_30_360(AS_OF, maturity) / 360
        assert abs((row.yield_pct - c2.curve_yield_pct(years)) * 100 - row.oas) < 1e-9
        assert abs(c2.price(AS_OF, maturity, row.coupon, row.yield_pct) - row.price) <= ROUNDED
        assert abs(c2.accrued_interest(AS_OF, maturity, row.coupon) - row.accrued) <= ROUNDED
        assert abs(c2.modified_duration(AS_OF, maturity, row.coupon, row.yield_pct) - row.duration) <= ROUNDED
        assert abs(c2.yield_to_maturity(AS_OF, maturity, row.coupon, row.price) - row.yield_pct) <= 0.001
    assert (clean["spread_duration"] == clean["duration"]).all()
    assert ((clean["dts"] - clean["spread_duration"] * clean["oas"]).abs() <= 0.05 + 1e-9).all()
    worked_out = clean["par_held"] * (clean["price"] + clean["accrued"]) / 100
    assert ((worked_out - clean["market_value"]).abs() < 0.005).all()


def test_month_differs_from_september(built) -> None:
    clean, _, _, new_cusips = built
    september = set(pd.read_csv(DATA / "holdings.csv")["cusip"])
    assert len(september - set(clean["cusip"])) == c2.SOLD
    assert len(set(clean["cusip"]) - september - set(new_cusips)) == c2.BOUGHT


def test_the_two_special_bonds_are_present_and_clean(built) -> None:
    clean, _, planted, new_cusips = built
    maturities = [d(m) for m in clean["maturity"]]
    final_period = [m for m in maturities if len(c2.coupon_dates(AS_OF, m)) == 2]
    month_ends = [m for m in maturities if c2.month_end(m)]
    assert final_period == [d("2027-03-15")] and month_ends == [d("2033-08-31")]
    # the month-end rule puts the coupons around settlement on 31 August and 28 February
    assert c2.coupon_dates(AS_OF, d("2033-08-31"))[:2] == [d("2026-08-31"), d("2027-02-28")]
    planted_cusips = {item["cusip"] for items in planted.values() for item in items}
    assert not planted_cusips & set(new_cusips)
    assert not planted_cusips & set(clean.nlargest(5, "oas")["cusip"])


def test_planted_problems_are_present_as_stated(built, extract: pd.DataFrame) -> None:
    clean, _, planted, _ = built
    key = (DATA / "course2_capstone_answer_key.md").read_text(encoding="utf-8")

    assert len(extract) == len(clean) + c2.N_DUPLICATES
    assert extract.duplicated().sum() == c2.N_DUPLICATES
    assert set(extract.loc[extract.duplicated(), "cusip"]) == {item["cusip"] for item in planted["duplicates"]}
    assert (extract["coupon"] < 1).sum() == c2.N_COUPON_DECIMAL
    assert (extract["yield_pct"] < 1).sum() == c2.N_YIELD_DECIMAL
    assert extract["price"].isna().sum() == c2.N_BLANK_PRICE
    assert extract["yield_pct"].isna().sum() == c2.N_BLANK_YIELD
    assert extract.isna().sum().sum() == c2.N_BLANK_PRICE + c2.N_BLANK_YIELD
    assert (extract["maturity"] <= extract["as_of_date"]).sum() == c2.N_MATURITY

    # the problems that only a reprice finds, on rows whose inputs are sound
    sound = extract.drop_duplicates()
    sound = sound[(sound["coupon"] >= 1) & (sound["yield_pct"] >= 1) & (sound["maturity"] > sound["as_of_date"])]
    dirty = accrued = macaulay = 0
    for row in sound.itertuples():
        maturity = d(row.maturity)
        clean_price = c2.round3(c2.price(AS_OF, maturity, row.coupon, row.yield_pct))
        dirty += abs(row.price - c2.round3(clean_price + row.accrued)) < 1e-9
        accrued_360 = c2.round3(c2.accrued_interest(AS_OF, maturity, row.coupon))
        if abs(row.accrued - accrued_360) > 1e-9:
            previous_coupon = c2.coupon_dates(AS_OF, maturity)[0]
            assert row.accrued == c2.round3(row.coupon * (AS_OF - previous_coupon).days / 360)
            accrued += 1
        mac = c2.round3(c2.macaulay_duration(AS_OF, maturity, row.coupon, row.yield_pct))
        macaulay += row.duration == mac and row.duration != row.spread_duration
    assert (dirty, accrued, macaulay) == (c2.N_DIRTY_PRICE, c2.N_ACCRUED_ACT360, c2.N_MACAULAY)
    assert (extract["duration"] != extract["spread_duration"]).sum() == c2.N_MACAULAY

    # market value fails to tie out in the dirty-price and actual/360 rows only
    gap = (extract["par_held"] * (extract["price"] + extract["accrued"]) / 100 - extract["market_value"]).abs()
    assert (gap > 0.005).sum() == c2.N_DIRTY_PRICE + c2.N_ACCRUED_ACT360

    # every planted row is named in the answer key, no row carries two problems, and the counts match
    counts = {"dirty_price": c2.N_DIRTY_PRICE, "yield_decimal": c2.N_YIELD_DECIMAL,
              "coupon_decimal": c2.N_COUPON_DECIMAL, "blank_price": c2.N_BLANK_PRICE,
              "blank_yield": c2.N_BLANK_YIELD, "macaulay": c2.N_MACAULAY, "accrued_act360": c2.N_ACCRUED_ACT360,
              "maturity": c2.N_MATURITY, "duplicates": c2.N_DUPLICATES}
    assert {name: len(items) for name, items in planted.items()} == counts
    planted_cusips = [item["cusip"] for items in planted.values() for item in items]
    assert len(planted_cusips) == len(set(planted_cusips))
    assert all(f"`{cusip}`" in key for cusip in planted_cusips)


def test_fixes_in_the_answer_key_restore_the_clean_book(built, extract: pd.DataFrame) -> None:
    clean, _, _, _ = built
    totals = c2.control_totals(clean)
    benchmark = pd.read_csv(DATA / "benchmark.csv")

    book = extract.drop_duplicates().reset_index(drop=True)
    matured = book["maturity"] <= book["as_of_date"]
    book.loc[matured, "maturity"] = book.loc[matured, "cusip"].map(benchmark.set_index("cusip")["maturity"])
    book.loc[book["coupon"] < 1, "coupon"] = (book["coupon"] * 100).round(3)
    book.loc[book["yield_pct"] < 1, "yield_pct"] = (book["yield_pct"] * 100).round(3)
    for i, row in book.iterrows():
        maturity = d(row["maturity"])
        if pd.isna(row["price"]):
            book.loc[i, "price"] = c2.round3(c2.price(AS_OF, maturity, row["coupon"], row["yield_pct"]))
        if pd.isna(row["yield_pct"]):
            book.loc[i, "yield_pct"] = c2.round3(c2.yield_to_maturity(AS_OF, maturity, row["coupon"], row["price"]))
        row = book.loc[i]
        accrued = c2.round3(c2.accrued_interest(AS_OF, maturity, row["coupon"]))
        if abs(row["accrued"] - accrued) > 1e-9:
            book.loc[i, "accrued"] = accrued
        if abs(row["price"] - c2.price(AS_OF, maturity, row["coupon"], row["yield_pct"])) > ROUNDED:
            book.loc[i, "price"] = c2.round3(row["price"] - accrued)
        duration = c2.round3(c2.modified_duration(AS_OF, maturity, row["coupon"], row["yield_pct"]))
        if row["duration"] != duration:
            book.loc[i, "duration"] = duration

    assert len(book) == totals["bonds"]
    assert book["par_held"].sum() == totals["face"]
    assert round(book["market_value"].sum(), 2) == totals["market_value"]
    pd.testing.assert_frame_equal(book, clean.reset_index(drop=True), check_exact=False, atol=1e-9)
    worked_out = book["par_held"] * (book["price"] + book["accrued"]) / 100
    assert ((worked_out - book["market_value"]).abs() < 0.005).all()

    note = (DATA / "course2_capstone_cover_note.txt").read_text(encoding="utf-8")
    for figure in (f"{totals['bonds']:,}", f"{totals['face']:,}", f"{totals['market_value']:,.2f}"):
        assert figure in note
    # the cover note names no bond
    assert re.findall(r"99[0-9A-Z]{7}", note) == []


# ---- the Excel reference file
def test_excel_reference_identities(reference: pd.DataFrame) -> None:
    f = reference["frequency"]
    assert ((reference["mduration"] - reference["duration"] / (1 + reference["yield_pct"] / 100 / f)).abs() < 1e-12).all()
    dv01 = reference["mduration"] * (reference["price"] + reference["accrued"]) / 10000
    assert ((reference["dv01"] - dv01).abs() < 1e-15).all()
    # outside the final period YIELD inverts PRICE; inside it YIELD uses its closed form (see the spec)
    whole = reference[reference["coupnum"] > 1]
    assert ((whole["yield_pct_from_price"] - whole["yield_pct"]).abs() < 1e-6).all()


def test_excel_reference_holdings_rows_equal_holdings_csv(reference: pd.DataFrame) -> None:
    holdings = pd.read_csv(DATA / "holdings.csv")
    rows = reference[reference["group"] == "holdings"].set_index("case_id").loc[holdings["cusip"]]
    assert len(rows) == 200
    assert (rows["settlement"].to_numpy() == holdings["as_of_date"].to_numpy()).all()
    assert (rows["maturity"].to_numpy() == holdings["maturity"].to_numpy()).all()
    assert (rows["coupon_pct"].to_numpy() == holdings["coupon"].to_numpy()).all()
    assert (rows["yield_pct"].to_numpy() == holdings["yield_pct"].to_numpy()).all()
    assert (rows["frequency"] == 2).all() and (rows["basis"] == 0).all()


def test_copied_math_agrees_with_excel(reference: pd.DataFrame) -> None:
    # the generator's math is 30/360 only, so it is checked on every basis 0 row (all frequencies)
    rows = reference[reference["basis"] == 0]
    assert len(rows) == 266
    for row in rows.itertuples():
        s, m, c, y, f = d(row.settlement), d(row.maturity), row.coupon_pct, row.yield_pct, row.frequency
        dates = c2.coupon_dates(s, m, f)
        assert (dates[0], dates[1], len(dates) - 1) == (d(row.couppcd), d(row.coupncd), row.coupnum), row.case_id
        a, e, _ = c2.coupon_period_days(s, m, f)
        assert (a, e) == (row.coupdaybs, row.coupdays), row.case_id
        assert c2.price(s, m, c, y, f) == pytest.approx(row.price, abs=1e-6), row.case_id
        assert c2.accrued_interest(s, m, c, f) == pytest.approx(row.accrued, abs=1e-9), row.case_id
        assert c2.yield_to_maturity(s, m, c, row.price, f) == pytest.approx(row.yield_pct_from_price, abs=1e-6), row.case_id
        assert c2.macaulay_duration(s, m, c, y, f) == pytest.approx(row.duration, abs=1e-6), row.case_id
        assert c2.modified_duration(s, m, c, y, f) == pytest.approx(row.mduration, abs=1e-6), row.case_id
