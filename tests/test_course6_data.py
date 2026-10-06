"""Checks on the Course 6 data. Course 6 adds no data file and changes none; these tests pin the rows it uses.

Run with: python -m pytest

- The Treasury cut (COURSE6_SPEC.md, "The test-row rule"): the development years, 2015-01-02 to 2022-12-30, and the
  held-out years, 2023-01-03 to 2026-10-02, opened once on day 14. Inputs are the 11 full tenors.
- The Taiwan training rows the capstone uses: Course 5's capstone preparation rebuilt here (names cleaned, the
  constant column and the second column of each equal pair dropped, an 80/20 stratified split with seed 42), so its
  1,364 test rows stay closed. Course 5's data test already checks the card and Polish counts.
"""
from pathlib import Path

import pandas as pd
import pytest
from sklearn.model_selection import train_test_split

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
SEED = 42
FULL_TENORS = ["1 Mo", "3 Mo", "6 Mo", "1 Yr", "2 Yr", "3 Yr", "5 Yr", "7 Yr", "10 Yr", "20 Yr", "30 Yr"]
PARTIAL_TENORS = ["1.5 Month", "2 Mo", "4 Mo"]
DEVELOPMENT_END = pd.Timestamp("2022-12-30")
HELD_OUT_START, LAST_DATE = pd.Timestamp("2023-01-03"), pd.Timestamp("2026-10-02")
TAIWAN_TARGET = "Bankrupt?"
TAIWAN_CONSTANT = "Net Income Flag"
TAIWAN_EQUAL_SECONDS = ["Current Liability to Liability", "Current Liability to Equity"]


@pytest.fixture(scope="module")
def treasury() -> pd.DataFrame:
    return pd.read_csv(DATA / "treasury_par_yields.csv", parse_dates=["date"])


def test_treasury_development_and_held_out_years(treasury: pd.DataFrame) -> None:
    dates = treasury["date"]
    assert dates.is_unique and dates.is_monotonic_increasing
    assert (len(treasury), dates.min(), dates.max()) == (2_940, pd.Timestamp("2015-01-02"), LAST_DATE)
    development = treasury[dates <= DEVELOPMENT_END]
    held_out = treasury[(dates >= HELD_OUT_START) & (dates <= LAST_DATE)]
    assert (len(development), len(held_out)) == (2_001, 939)
    # the two parts cover the file with nothing between them
    assert len(development) + len(held_out) == len(treasury)
    assert development["date"].max() == DEVELOPMENT_END and held_out["date"].min() == HELD_OUT_START


def test_treasury_full_tenors_have_no_empty_cell(treasury: pd.DataFrame) -> None:
    assert list(treasury.columns) == ["date", "1 Mo", "1.5 Month", "2 Mo", "3 Mo", "4 Mo", "6 Mo", "1 Yr", "2 Yr",
                                      "3 Yr", "5 Yr", "7 Yr", "10 Yr", "20 Yr", "30 Yr"]
    development = treasury[treasury["date"] <= DEVELOPMENT_END]
    held_out = treasury[treasury["date"] >= HELD_OUT_START]
    assert int(development[FULL_TENORS].isna().sum().sum()) == 0
    assert int(held_out[FULL_TENORS].isna().sum().sum()) == 0
    # the three partial tenors are not used: each has empty cells
    assert all(treasury[name].isna().any() for name in PARTIAL_TENORS)


def test_taiwan_training_rows() -> None:
    frame = pd.read_csv(DATA / "taiwan_bankruptcy.csv")
    # Course 5's cleaning: strip the leading space and remove " " plus the yen sign
    frame.columns = [name.strip().replace(" \u00a5", "") for name in frame.columns]
    X = frame.drop(columns=[TAIWAN_TARGET, TAIWAN_CONSTANT] + TAIWAN_EQUAL_SECONDS)
    y = frame[TAIWAN_TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
    assert (len(X_train), int(y_train.sum()), X_train.shape[1]) == (5_455, 176, 92)
    assert (len(X_test), int(y_test.sum())) == (1_364, 44)
    assert all(name.isascii() for name in X_train.columns)
    # the two-scale columns (some value above 1) in the training rows
    assert int((X_train > 1).any().sum()) == 23
