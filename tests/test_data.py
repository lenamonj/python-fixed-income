"""Checks on the synthetic data files in data/. Run with: python -m pytest"""
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from make_holdings import AS_OF, analytics, cusip_check_digit  # noqa: E402

DATA = REPO / "data"


@pytest.fixture(scope="module")
def holdings() -> pd.DataFrame:
    return pd.read_csv(DATA / "holdings.csv", parse_dates=["maturity"])


def test_check_digit_matches_a_published_example() -> None:
    # 037833100 is the standard worked example of the CUSIP check digit algorithm
    assert cusip_check_digit("03783310") == "0"


def test_price_on_a_coupon_date_matches_the_closed_form() -> None:
    # 5.25 percent coupon, 7 years, 5.51 percent yield, settling on a coupon date
    clean, accrued, _ = analytics(5.25, 5.51, date(2026, 9, 15), date(2033, 9, 15))
    y, n = 0.0551 / 2, 14
    expected = 2.625 * (1 - (1 + y) ** -n) / y + 100 * (1 + y) ** -n
    assert accrued == 0
    assert clean == pytest.approx(expected, abs=1e-9)


def test_holdings_shape_and_identifiers(holdings: pd.DataFrame) -> None:
    assert len(holdings) == 200
    assert holdings["cusip"].is_unique
    assert holdings["cusip"].str.len().eq(9).all()
    # every CUSIP sits in the range reserved for internal use and has a valid check digit
    assert holdings["cusip"].str.startswith("99").all()
    assert all(cusip_check_digit(c[:8]) == c[8] for c in holdings["cusip"])


def test_price_yield_and_duration_agree(holdings: pd.DataFrame) -> None:
    for bond in holdings.itertuples(index=False):
        clean, accrued, duration = analytics(bond.coupon, bond.yield_pct, AS_OF, bond.maturity.date())
        assert bond.price == pytest.approx(clean, abs=0.0006)
        assert bond.accrued == pytest.approx(accrued, abs=0.0006)
        assert bond.duration == pytest.approx(duration, abs=0.0006)


def test_tables_join_cleanly(holdings: pd.DataFrame) -> None:
    issuers = pd.read_csv(DATA / "issuers.csv")
    ratings = pd.read_csv(DATA / "ratings.csv")
    assert issuers["ticker"].is_unique
    assert set(holdings["ticker"]) <= set(issuers["ticker"])
    assert set(holdings["rating"]) <= set(ratings["rating"])


def test_messy_file_has_the_planted_problems(holdings: pd.DataFrame) -> None:
    messy = pd.read_csv(DATA / "holdings_messy.csv")
    assert len(messy) == len(holdings) + 4
    assert messy["cusip"].duplicated().sum() == 4
    assert messy["rating"].isna().sum() >= 5
    assert (messy["yield_pct"] < 1).sum() >= 2


@pytest.fixture(scope="module")
def treasury() -> pd.DataFrame:
    return pd.read_csv(DATA / "treasury_par_yields.csv", parse_dates=["date"])


def test_treasury_dates_are_unique_ascending_weekdays(treasury: pd.DataFrame) -> None:
    assert treasury["date"].is_unique
    assert treasury["date"].is_monotonic_increasing
    # Monday is 0, so 5 and 6 are Saturday and Sunday
    assert (treasury["date"].dt.dayofweek < 5).all()


def test_treasury_yields_are_in_a_plausible_range(treasury: pd.DataFrame) -> None:
    # percent. Blanks are tenors Treasury did not publish on that date and are left out by min and max.
    yields = treasury.drop(columns="date")
    assert yields.min().min() >= -1
    assert yields.max().max() <= 20


def test_treasury_rows_per_full_year(treasury: pd.DataFrame) -> None:
    rows = treasury.groupby(treasury["date"].dt.year).size()
    # the last year in the file is still in progress
    full_years = rows.iloc[:-1]
    assert full_years.between(245, 255).all()


@pytest.fixture(scope="module")
def blotter() -> pd.DataFrame:
    return pd.read_csv(DATA / "trade_blotter.csv", parse_dates=["trade_date", "settle_date"])


def test_blotter_ids_are_unique_and_bonds_are_held(blotter: pd.DataFrame, holdings: pd.DataFrame) -> None:
    assert blotter["trade_id"].is_unique
    assert blotter.notna().all().all()
    assert blotter["side"].isin(["BUY", "SELL"]).all()
    # every trade is in a bond of the portfolio, under the same ticker
    pairs = set(zip(holdings["cusip"], holdings["ticker"]))
    assert set(zip(blotter["cusip"], blotter["ticker"])) <= pairs


def test_blotter_dates(blotter: pd.DataFrame) -> None:
    holiday = pd.Timestamp("2026-09-07")
    for column in ["trade_date", "settle_date"]:
        # Monday is 0, so 5 and 6 are Saturday and Sunday
        assert (blotter[column].dt.dayofweek < 5).all()
        assert (blotter[column] != holiday).all()
    assert blotter["trade_date"].between("2026-09-01", pd.Timestamp(AS_OF)).all()
    assert (blotter["settle_date"] > blotter["trade_date"]).all()
    # T+1: no business day lies between the trade date and the settle date
    business_days = pd.bdate_range("2026-09-01", "2026-10-09", freq="C", holidays=[holiday])
    next_day = dict(zip(business_days[:-1], business_days[1:]))
    assert (blotter["settle_date"] == blotter["trade_date"].map(next_day)).all()
    # trade ids run in time order
    assert blotter[["trade_date", "trade_time"]].apply(tuple, axis=1).is_monotonic_increasing


def test_blotter_amounts(blotter: pd.DataFrame, holdings: pd.DataFrame) -> None:
    assert (blotter["quantity"] > 0).all()
    assert (blotter["quantity"] % 5_000 == 0).all()
    # principal = quantity x price / 100, to the cent
    assert ((blotter["principal"] - blotter["quantity"] * blotter["price"] / 100).abs() < 0.005).all()
    # net buying of a bond never exceeds the par held at month end
    signed = blotter["quantity"].where(blotter["side"] == "BUY", -blotter["quantity"])
    net = signed.groupby(blotter["cusip"]).sum()
    assert (net <= holdings.set_index("cusip")["par_held"].reindex(net.index)).all()


def test_blotter_generator_is_deterministic(tmp_path: Path) -> None:
    from make_blotter import write_blotter

    write_blotter(tmp_path / "first.csv")
    write_blotter(tmp_path / "second.csv")
    first = (tmp_path / "first.csv").read_bytes()
    assert first == (tmp_path / "second.csv").read_bytes()
    assert first == (DATA / "trade_blotter.csv").read_bytes()
