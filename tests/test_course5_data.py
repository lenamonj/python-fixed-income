"""Checks on the Course 5 data: the UCI Taiwanese bankruptcy file, and the three Course 4 splits Course 5 rebuilds.

Run with: python -m pytest

The byte-for-byte comparison with the UCI zip needs the copy of the zip that tools/get_taiwan_bankruptcy.py keeps
outside the repo, and skips, saying why, when it is missing.

Course 5 never scores a row Course 4 used as a test row. The split checks below rebuild each Course 4 split with
Course 4's own code (same calls, seed 42) and check the counts Course 5 relies on: the rows Course 5 may use and the
rows that stay closed.
"""
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import train_test_split

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import get_taiwan_bankruptcy as taiwan  # noqa: E402

DATA = REPO / "data"
TAIWAN = DATA / "taiwan_bankruptcy.csv"
TARGET = "Bankrupt?"
SEED = 42
CARD_FEATURES = ["LIMIT_BAL", "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"] + \
    [f"BILL_AMT{i}" for i in range(1, 7)] + [f"PAY_AMT{i}" for i in range(1, 7)]


@pytest.fixture(scope="module")
def companies() -> pd.DataFrame:
    return pd.read_csv(TAIWAN)


# ---- Taiwanese bankruptcy
def test_taiwan_sha256_and_line_endings() -> None:
    raw = TAIWAN.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == taiwan.MEMBER_SHA256
    # CRLF line endings, as the zip holds them (.gitattributes keeps Git from converting them): a header and 6,819 rows
    assert raw.count(b"\r\n") == raw.count(b"\n") == 6_820
    # the only non-ASCII bytes: the yen sign (UTF-8 C2 A5) in three column names
    assert sum(byte > 127 for byte in raw) == 6
    assert raw.count("\u00a5".encode("utf-8")) == 3


def test_taiwan_shape_and_columns(companies: pd.DataFrame) -> None:
    assert companies.shape == (6_819, 96)
    # the target first, then 95 features whose names start with a space, in the file's order
    assert companies.columns[0] == TARGET
    assert all(name.startswith(" ") for name in companies.columns[1:])
    assert companies.columns[1] == " ROA(C) before interest and depreciation before interest"
    assert companies.columns[-1] == " Equity to Liability"
    assert [name for name in companies.columns if "\u00a5" in name] == [
        " Revenue Per Share (Yuan \u00a5)", " Operating Profit Per Share (Yuan \u00a5)",
        " Per Share Net profit before tax (Yuan \u00a5)"]


def test_taiwan_target_and_no_missing(companies: pd.DataFrame) -> None:
    assert set(companies[TARGET].unique()) == {0, 1}
    assert int(companies[TARGET].sum()) == 220
    assert int(companies.isna().sum().sum()) == 0
    assert int(companies.duplicated().sum()) == 0


def test_taiwan_constant_and_equal_columns(companies: pd.DataFrame) -> None:
    features = companies.drop(columns=TARGET)
    assert [name for name in features if features[name].nunique() == 1] == [" Net Income Flag"]
    assert (features[" Net Income Flag"] == 1).all()
    names = list(features.columns)
    equal = [(a, b) for i, a in enumerate(names) for b in names[i + 1:] if features[a].equals(features[b])]
    assert equal == [(" Current Liabilities/Liability", " Current Liability to Liability"),
                     (" Current Liabilities/Equity", " Current Liability to Equity")]


def test_taiwan_two_scales(companies: pd.DataFrame) -> None:
    features = companies.drop(columns=TARGET)
    assert int((features < 0).sum().sum()) == 0
    inside = [name for name in features if features[name].between(0, 1).all()]
    assert len(inside) == 71
    two_scale = [name for name in features if name not in inside]
    assert len(two_scale) == 24
    large = features[two_scale].where(features[two_scale] > 1)
    # values above 1 run from 583,000 to 1e10, with nothing strictly between 1 and 583,000
    assert int(large.notna().sum().sum()) == 24_940
    assert float(large.min().min()) == 583_000.0
    assert float(large.max().max()) == 1e10
    assert int(((features[two_scale] > 1) & (features[two_scale] < 583_000)).sum().sum()) == 0


def test_taiwan_equals_zip_member() -> None:
    if not taiwan.CACHE.exists():
        pytest.skip("the UCI zip is not in the cache folder outside the repo; run tools/get_taiwan_bankruptcy.py")
    assert TAIWAN.read_bytes() == taiwan.read_member(taiwan.CACHE.read_bytes())


# ---- the three Course 4 splits, rebuilt with Course 4's code
def test_course4_card_split() -> None:
    card = pd.read_csv(DATA / "credit_card_default.csv")
    X, y = card[CARD_FEATURES], card["default payment next month"]
    X_rest, X_test, y_rest, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
    X_train, X_valid, y_train, y_valid = train_test_split(X_rest, y_rest, test_size=0.25, stratify=y_rest,
                                                          random_state=SEED)
    assert (len(X_train), len(X_valid), len(X_test)) == (18_000, 6_000, 6_000)
    assert not set(X_test.index) & (set(X_train.index) | set(X_valid.index))
    assert int(y.sum()) == int(y_train.sum()) + int(y_valid.sum()) + int(y_test.sum())


def test_course4_bench_split() -> None:
    bench = pd.read_csv(DATA / "benchmark.csv")
    bench_train, bench_test = train_test_split(bench, test_size=0.25, random_state=SEED)
    assert (len(bench_train), len(bench_test)) == (615, 206)
    assert not set(bench_train["cusip"]) & set(bench_test["cusip"])


def test_course4_polish_split() -> None:
    frame = pd.read_csv(DATA / "polish_bankruptcy_5year.csv", float_precision="round_trip")
    unique = frame.drop_duplicates()
    X, y = unique.drop(columns="class"), unique["class"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
    assert (len(unique), len(X_train), len(X_test)) == (5_850, 4_680, 1_170)
    assert (int(y_train.sum()), int(y_test.sum())) == (326, 82)
    assert np.isclose(y_train.mean(), 326 / 4_680)
    assert not set(X_train.index) & set(X_test.index)


def test_taiwan_capstone_split(companies: pd.DataFrame) -> None:
    y = companies[TARGET]
    train, test = train_test_split(companies, test_size=0.2, stratify=y, random_state=SEED)
    assert (len(train), len(test)) == (5_455, 1_364)
    assert (int(train[TARGET].sum()), int(test[TARGET].sum())) == (176, 44)
