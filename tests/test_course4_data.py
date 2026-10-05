"""Checks on the Course 4 data: the UCI Polish bankruptcy file and the Excel reference file.

Run with: python -m pytest

Two checks need files that are not in the repo and skip, saying why, when they are missing:
- the cell-by-cell comparison with the ARFF needs the UCI zip that tools/get_polish_bankruptcy.py keeps outside
  the repo;
- the Excel generator's two-run check needs desktop Excel and a Python with pywin32, named by the environment
  variable PFI_EXCEL_PYTHON.
"""
import io
import math
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import get_polish_bankruptcy as polish  # noqa: E402

DATA = REPO / "data"
POLISH = DATA / "polish_bankruptcy_5year.csv"
REFERENCE = DATA / "course4_excel_reference.csv"


@pytest.fixture(scope="module")
def bankruptcy() -> pd.DataFrame:
    return pd.read_csv(POLISH, float_precision="round_trip")


@pytest.fixture(scope="module")
def reference() -> pd.DataFrame:
    return pd.read_csv(REFERENCE, float_precision="round_trip")


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


# ---- Excel reference
def test_excel_reference_layout(reference: pd.DataFrame) -> None:
    assert list(reference.columns) == ["case_id", "quantity", "excel_formula", "excel_value"]
    assert reference["case_id"].is_unique
    assert (reference["case_id"].str.split(":").str[1] == reference["quantity"]).all()
    assert reference["excel_value"].map(np.isfinite).all()
    assert b"\r\n" not in REFERENCE.read_bytes()


def bench_design() -> tuple[pd.DataFrame, dict[str, tuple[str, pd.DataFrame]]]:
    """The benchmark bonds and the (target, features) of each regression the reference file holds."""
    bench = pd.read_csv(DATA / "benchmark.csv")
    ratings = pd.read_csv(DATA / "ratings.csv")
    bench = bench.merge(ratings[["rating", "score"]], on="rating", how="left", validate="many_to_one")
    bench["log_oas"] = np.log(bench["oas"])
    rating = pd.DataFrame({f"rating_{r}": (bench["rating"] == r).astype(float) for r in ratings["rating"] if r != "A"})
    sector = pd.DataFrame({f"sector_{s}": (bench["sector"] == s).astype(float)
                           for s in sorted(bench["sector"].unique()) if s != "Consumer"})
    big = pd.concat([rating, bench[["duration"]], sector], axis=1)
    models = {
        "d02_oas_on_score_duration": ("oas", bench[["score", "duration"]]),
        "d02_oas_on_rating_duration_sector": ("oas", big),
        "d03_log_oas_on_score_duration_sector": ("log_oas", pd.concat([bench[["score", "duration"]], sector], axis=1)),
        "d04_log_oas_on_rating_duration_sector": ("log_oas", big),
    }
    return bench, models


def test_excel_reference_r2_identity(reference: pd.DataFrame) -> None:
    excel = reference.set_index("case_id")["excel_value"]
    bench, models = bench_design()
    for model, (target, X) in models.items():
        fit = sm.OLS(bench[target], sm.add_constant(X)).fit()
        assert fit.rsquared == pytest.approx(excel[f"{model}:r2"], abs=1e-9), model
    simple = sm.OLS(bench["oas"], sm.add_constant(bench[["score"]])).fit()
    assert simple.rsquared == pytest.approx(excel["d01_oas_on_score:rsq"], abs=1e-9)


def test_excel_reference_vif_identity(reference: pd.DataFrame) -> None:
    excel = reference.set_index("case_id")["excel_value"]
    names = [q[len("vif_rsq_"):] for q in reference["quantity"] if q.startswith("vif_rsq_")]
    assert len(names) == 11
    for name in names:
        assert excel[f"d03_vif:vif_{name}"] == pytest.approx(1 / (1 - excel[f"d03_vif:vif_rsq_{name}"]), abs=1e-9)


def test_excel_generator_is_deterministic(tmp_path: Path) -> None:
    excel_python = os.environ.get("PFI_EXCEL_PYTHON")
    if not excel_python:
        pytest.skip("needs desktop Excel: set PFI_EXCEL_PYTHON to a Python with pywin32 (author machine only)")
    tool = REPO / "tools" / "make_course4_excel_reference.py"
    for name in ("first", "second"):
        (tmp_path / name).mkdir()
        subprocess.run([excel_python, str(tool), "--out", str(tmp_path / name)], check=True, capture_output=True)
    first = (tmp_path / "first" / REFERENCE.name).read_bytes()
    assert first == (tmp_path / "second" / REFERENCE.name).read_bytes()
    assert first == REFERENCE.read_bytes()
