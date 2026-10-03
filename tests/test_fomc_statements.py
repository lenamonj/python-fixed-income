"""Checks on data/fomc_statements.csv. Run with: python -m pytest"""
import re
from pathlib import Path

import pandas as pd
import pytest

DATA = Path(__file__).resolve().parent.parent / "data"


@pytest.fixture(scope="module")
def statements() -> pd.DataFrame:
    return pd.read_csv(DATA / "fomc_statements.csv")


def test_row_count_and_columns(statements: pd.DataFrame) -> None:
    assert len(statements) == 46
    assert list(statements.columns) == ["date", "url", "text"]


def test_dates_are_iso_unique_and_ascending(statements: pd.DataFrame) -> None:
    assert statements["date"].str.fullmatch(r"\d{4}-\d{2}-\d{2}").all()
    # raises if any value is not a real calendar date
    pd.to_datetime(statements["date"], format="%Y-%m-%d")
    assert statements["date"].is_unique
    assert statements["date"].is_monotonic_increasing
    assert statements["date"].iloc[0] == "2021-01-27"
    assert statements["date"].iloc[-1] == "2026-09-16"


def test_every_url_is_the_statement_page_for_its_date(statements: pd.DataFrame) -> None:
    for date, url in zip(statements["date"], statements["url"]):
        expected = f"https://www.federalreserve.gov/newsevents/pressreleases/monetary{date.replace('-', '')}a.htm"
        assert url == expected


def test_text_is_present_and_long_enough(statements: pd.DataFrame) -> None:
    assert statements["text"].notna().all()
    assert (statements["text"].str.strip() != "").all()
    assert (statements["text"].str.len() > 300).all()


def test_text_has_no_markup_or_page_furniture(statements: pd.DataFrame) -> None:
    for text in statements["text"]:
        assert "<" not in text and ">" not in text
        assert "&nbsp;" not in text and "&amp;" not in text and "\xa0" not in text
        assert "Implementation Note" not in text
        assert "For media inquiries" not in text
        # white space was normalized: single spaces, and one line break between paragraphs
        assert not re.search(r" {2}|\n\n|\t|\r", text)
        assert text == text.strip()


def test_no_paragraph_is_cut_off(statements: pd.DataFrame) -> None:
    for text in statements["text"]:
        for paragraph in text.split("\n"):
            # a paragraph ends a sentence, or introduces the statement with a colon
            assert paragraph[-1] in ".:"
