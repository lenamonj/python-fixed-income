"""Download the Daily Treasury Par Yield Curve Rates and write data/treasury_par_yields.csv.

Source: U.S. Department of the Treasury, Daily Treasury Par Yield Curve Rates
    https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve

One CSV per calendar year is downloaded from Treasury's own site, with no account and no key:
    https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/<YEAR>/all?type=daily_treasury_yield_curve&field_tdr_date_value=<YEAR>&page&_format=csv

The file in the repo was retrieved on 2026-10-03 and covers 2015-01-02 to 2026-10-02.

The values are written exactly as Treasury published them, in percent. Nothing is filled, smoothed,
or dropped. A blank means Treasury published no rate for that tenor on that date. The column names
are Treasury's own labels. Dates are rewritten from MM/DD/YYYY to YYYY-MM-DD and sorted ascending.

Usage (from the repo root):

    python tools/get_treasury_yields.py
"""
import io
import urllib.request
from datetime import date
from pathlib import Path

import pandas as pd

URL = (
    "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
    "daily-treasury-rates.csv/{year}/all?type=daily_treasury_yield_curve"
    "&field_tdr_date_value={year}&page&_format=csv"
)
FIRST_YEAR = 2015
OUT = Path(__file__).resolve().parent.parent / "data" / "treasury_par_yields.csv"


def download_year(year: int) -> pd.DataFrame:
    """Return one year of rates as text, so that each value stays exactly as published."""
    request = urllib.request.Request(URL.format(year=year), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        text = response.read().decode("utf-8")
    table = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False)
    if table.empty or table.columns[0] != "Date":
        raise RuntimeError(f"unexpected response for {year}: {text[:200]!r}")
    return table


def main() -> None:
    years = range(FIRST_YEAR, date.today().year + 1)
    tables = []
    for year in years:
        table = download_year(year)
        print(year, len(table), "rows,", len(table.columns) - 1, "tenors")
        tables.append(table)

    # the newest year lists every tenor, shortest first. Earlier years must not hold any other.
    tenors = [column for column in tables[-1].columns if column != "Date"]
    for year, table in zip(years, tables):
        unknown = set(table.columns) - set(tenors) - {"Date"}
        if unknown:
            raise RuntimeError(f"{year} has tenors missing from the newest year: {sorted(unknown)}")

    # a tenor that a year does not have becomes a blank, the same as a blank inside a year
    combined = pd.concat(tables, ignore_index=True).fillna("")
    combined["date"] = pd.to_datetime(combined["Date"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
    combined = combined.sort_values("date")[["date"] + tenors]
    if combined["date"].duplicated().any():
        raise RuntimeError("a date appears more than once")

    combined.to_csv(OUT, index=False, lineterminator="\n")
    print("wrote", OUT, "-", len(combined), "rows,", combined["date"].iloc[0], "to", combined["date"].iloc[-1])


if __name__ == "__main__":
    main()
