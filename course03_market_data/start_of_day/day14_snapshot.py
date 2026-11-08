"""snapshot.py: write the daily market snapshot for one market date, as HTML and as Excel.

Usage, from any folder:
    python snapshot.py --as-of 2026-10-02
    python snapshot.py                      (the last date in the market data)

It reads the Treasury file, the synthetic spreads, and the synthetic book from the folder this file is in, and
writes snapshots/snapshot_YYYY-MM-DD.html and .xlsx there. It describes the data and forecasts nothing.
"""
import argparse
from pathlib import Path

import pandas as pd
from matplotlib.figure import Figure

import marketdata as md

# the folder this file is in, whichever folder the script is started from
HERE = Path(__file__).resolve().parent
# the market columns on the levels table, and their units
UNITS = {"2 Yr": "pct", "5 Yr": "pct", "10 Yr": "pct", "30 Yr": "pct", "ig_spread_bp": "bp", "hy_spread_bp": "bp"}


def load_market() -> pd.DataFrame:
    """The Treasury file (percent) joined to the synthetic spreads (bp), one row per market date."""
    options = {"parse_dates": ["date"], "index_col": "date", "float_precision": "round_trip"}
    treasury = pd.read_csv(HERE / "treasury_par_yields.csv", **options)
    spreads = pd.read_csv(HERE / "course3_synthetic_spreads.csv", **options)
    return treasury.join(spreads, validate="one_to_one")


def charts(tables: dict[str, pd.DataFrame], market: pd.DataFrame) -> dict[str, Figure]:
    """The two charts, drawn without a screen: the curve on both days, and the synthetic spreads."""
    as_of = pd.Timestamp(tables["levels"].attrs["as_of"])
    previous = market.index[market.index.get_loc(as_of) - 1]
    curve = tables["curve"]
    curve_figure = Figure(figsize=(7, 3.5))
    axes = curve_figure.subplots()
    axes.plot(curve["years"], curve["previous_pct"], marker="o", markersize=3, label=f"{previous:%Y-%m-%d}")
    axes.plot(curve["years"], curve["as_of_pct"], marker="o", markersize=3, label=f"{as_of:%Y-%m-%d}")
    axes.set_title(f"Treasury par curve, {as_of:%Y-%m-%d} and the previous market date")
    axes.set_xlabel("Tenor (years)")
    axes.set_ylabel("Yield (percent)")
    axes.legend()
    curve_figure.tight_layout()

    recent = market.loc[:as_of, ["ig_spread_bp", "hy_spread_bp"]].tail(252)
    spread_figure = Figure(figsize=(7, 3.5))
    axes = spread_figure.subplots()
    axes.plot(recent.index, recent["ig_spread_bp"], label="Investment grade (synthetic)")
    axes.plot(recent.index, recent["hy_spread_bp"], label="High yield (synthetic)")
    axes.set_title("Synthetic credit spreads, the last 252 market days (invented, not an index)")
    axes.set_ylabel("Spread (bp)")
    axes.legend()
    spread_figure.autofmt_xdate()
    spread_figure.tight_layout()
    return {"Treasury curve": curve_figure, "Synthetic credit spreads": spread_figure}


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the daily market snapshot as HTML and Excel.")
    parser.add_argument("--as-of", help="the market date, YYYY-MM-DD (default: the last date in the market data)")
    args = parser.parse_args()

    market = load_market()
    book = pd.read_csv(HERE / "holdings.csv")
    as_of = args.as_of or f"{market.index[-1]:%Y-%m-%d}"
    try:
        tables = md.snapshot_tables(market, book, as_of, UNITS)
    except ValueError as error:
        # a one-line message and exit code 2, with no traceback: a traceback would print this file's full path
        parser.error(str(error))

    # the date as the tables carry it, YYYY-MM-DD, names both files
    as_of = tables["levels"].attrs["as_of"]
    out = HERE / "snapshots"
    out.mkdir(exist_ok=True)
    md.write_snapshot_html(tables, charts(tables, market), out / f"snapshot_{as_of}.html", f"Daily market snapshot, {as_of}")
    md.write_snapshot_excel(tables, out / f"snapshot_{as_of}.xlsx")
    print(f"snapshot for {as_of}: wrote snapshots/snapshot_{as_of}.html and snapshots/snapshot_{as_of}.xlsx")


if __name__ == "__main__":
    main()
