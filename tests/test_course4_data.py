"""Checks on the Course 4 data: the UCI Polish bankruptcy file.

Run with: python -m pytest

The cell-by-cell comparison with the ARFF needs the UCI zip that tools/get_polish_bankruptcy.py keeps outside the
repo, and skips, saying why, when it is missing.
"""
import math
import sys
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import get_polish_bankruptcy as polish  # noqa: E402

DATA = REPO / "data"
POLISH = DATA / "polish_bankruptcy_5year.csv"


@pytest.fixture(scope="module")
def bankruptcy() -> pd.DataFrame:
    return pd.read_csv(POLISH, float_precision="round_trip")


# ---- Polish bankruptcy, 5th year
def test_polish_shape_and_columns(bankruptcy: pd.DataFrame) -> None:
    assert bankruptcy.shape == (5_910, 65)
    assert list(bankruptcy.columns) == [f"Attr{k}" for k in range(1, 65)] + ["class"]
    assert b"\r\n" not in POLISH.read_bytes()


def test_polish_class(bankruptcy: pd.DataFrame) -> None:
    assert set(bankruptcy["class"].unique()) == {0, 1}
    assert int(bankruptcy["class"].sum()) == 410


def test_polish_missing_and_duplicates(bankruptcy: pd.DataFrame) -> None:
    features = bankruptcy.drop(columns="class")
    assert int(features.isna().sum().sum()) == 4_666
    assert int((features.isna().sum() > 0).sum()) == 49
    assert int(features["Attr37"].isna().sum()) == 2_548
    # the provider's filter removed rows with a missing Attr20
    assert int(features["Attr20"].isna().sum()) == 0
    assert int(bankruptcy.duplicated(keep="first").sum()) == 60
    # no duplicated pair carries two different labels
    assert int(features.duplicated(keep="first").sum()) == 60
    deduplicated = bankruptcy.drop_duplicates()
    assert (len(deduplicated), int(deduplicated["class"].sum())) == (5_850, 408)


def test_polish_equals_arff() -> None:
    if not polish.CACHE.exists():
        pytest.skip("the UCI zip is not in the cache folder outside the repo; run tools/get_polish_bankruptcy.py")
    rows = polish.read_arff(polish.CACHE.read_bytes())
    # the same cell-by-cell comparison the tool makes after writing: equal floats, empty for ?, class as text
    polish.compare_with_arff(rows, POLISH)
    assert sum(row[-1] == "1" for row in rows) == 410
    assert sum(math.isnan(value) for row in rows for value in row[:-1]) == 4_666
