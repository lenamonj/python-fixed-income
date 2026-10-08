"""Checks on the Course 7 data (DATA.md, "Added 2026-10-07: Course 7 data").

Run with: python -m pytest

- FOMC statements 2000 to 2026 (tools/get_fomc_history.py): rows, columns, dates, addresses, no HTML, and every
  2021 to 2026 text equal to data/fomc_statements.csv (the two tools agree).
"""
import re
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"


@pytest.fixture(scope="module")
def fomc() -> pd.DataFrame:
    return pd.read_csv(DATA / "course7_fomc_statements.csv")


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
        assert all(re.search(r"[.:;][\"')”]?$", paragraph) for paragraph in text.split("\n"))


def test_fomc_agrees_with_course1_file(fomc: pd.DataFrame) -> None:
    course1 = pd.read_csv(DATA / "fomc_statements.csv")
    later = fomc[fomc["date"] >= "2021-01-01"].reset_index(drop=True)
    assert len(later) == len(course1) == 46
    assert (later["date"] == course1["date"]).all()
    assert (later["url"] == course1["url"]).all()
    assert (later["text"] == course1["text"]).all()
