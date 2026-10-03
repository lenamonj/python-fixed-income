"""Generate the synthetic trade blotter used in notebook 15.

Everything here is invented: the trades, the counterparties, and the desks. Every trade is in
a bond from data/holdings.csv, so the blotter joins to the tables the student already knows.
The same seed always produces the same file. This script reads holdings.csv and ratings.csv
and writes trade_blotter.csv. It writes nothing else.

Conventions:
- Trades fall on business days from 2026-09-01 to the holdings as-of date, 2026-09-30.
  Monday 2026-09-07 is a market holiday and has no trades.
- Settlement is the next business day after the trade date (T+1).
- quantity is face amount in dollars, a multiple of 5,000. price is the clean price per 100
  of face. principal = quantity x price / 100, in dollars, exact to the cent.
- A bond's prices walk back day by day from its month-end price in holdings.csv, so prices
  for the same bond on nearby dates are close to each other.
- For every bond, buys less sells over the month is no more than the par held at month end,
  so the position implied for the start of the month is never negative.
- The file is clean. The only extreme values are a few block trades, which are real trades.

Usage (from the repo root):  python tools/make_blotter.py
"""
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from make_holdings import AS_OF

SEED = 20261004
DATA = Path(__file__).resolve().parent.parent / "data"
MONTH_START = date(2026, 9, 1)
HOLIDAYS = [date(2026, 9, 7)]

# invented dealer names, each checked by web search on 2026-10-04 to match no real firm
# share = share of the trade count. shift moves the trade size up or down the size ladder.
COUNTERPARTIES = {
    "Kestermoor Securities": dict(share=0.25, shift=-1),
    "Talvesham Partners": dict(share=0.15, shift=2),
    "Zembrook Securities": dict(share=0.15, shift=0),
    "Orlinthe Capital": dict(share=0.14, shift=0),
    "Wendlecroft Securities": dict(share=0.12, shift=0),
    "Pendraleth Capital": dict(share=0.11, shift=0),
    "Ulverthorne Markets": dict(share=0.08, shift=0),
}
BLOCK_COUNTERPARTIES = ["Talvesham Partners", "Talvesham Partners", "Talvesham Partners",
                        "Orlinthe Capital", "Talvesham Partners", "Zembrook Securities"]

# each desk covers a group of sectors
DESK = {
    "Financials": "Desk 1", "Utilities": "Desk 1",
    "Energy": "Desk 2", "Materials": "Desk 2", "Industrials": "Desk 2",
    "Consumer": "Desk 3", "Health Care": "Desk 3", "Transportation": "Desk 3",
    "Technology": "Desk 4", "Telecom": "Desk 4",
}

# chance that a trade in the sector is a buy
BUY_CHANCE = {
    "Energy": 0.74, "Utilities": 0.68, "Health Care": 0.66, "Technology": 0.60, "Industrials": 0.56,
    "Consumer": 0.52, "Materials": 0.50, "Telecom": 0.44, "Transportation": 0.40, "Financials": 0.34,
}

# average trades per day by weekday (Monday is 0), and the pick-up on the last two days of the month
TRADES_PER_DAY = {0: 12, 1: 19, 2: 21, 3: 18, 4: 11}
MONTH_END_LIFT = 1.4

# relative weight of each hour of the day, 08:00 to 16:59
HOUR_WEIGHT = {8: 6, 9: 16, 10: 18, 11: 12, 12: 5, 13: 8, 14: 14, 15: 13, 16: 8}

# trade sizes in dollars of face, smallest to largest, and how often each is drawn by grade
SIZES = [25_000, 50_000, 100_000, 150_000, 200_000, 250_000, 300_000, 400_000, 500_000, 750_000]
SIZE_WEIGHT = {
    "Investment Grade": [2, 5, 9, 9, 10, 14, 11, 13, 16, 11],
    "High Yield": [9, 16, 20, 14, 12, 11, 7, 5, 4, 2],
}
BLOCK_SIZES = [5_000_000, 4_000_000, 3_000_000, 3_000_000, 2_500_000, 2_000_000]

COLUMNS = ["trade_id", "trade_date", "trade_time", "settle_date", "cusip", "ticker", "side",
           "quantity", "price", "principal", "counterparty", "trader"]


def business_days() -> pd.DatetimeIndex:
    """Trading days of the month, plus the days after it that the last trades settle on."""
    return pd.bdate_range(MONTH_START, "2026-10-09", freq="C", holidays=HOLIDAYS)


def build_blotter() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    bonds = pd.read_csv(DATA / "holdings.csv").merge(pd.read_csv(DATA / "ratings.csv"), on="rating")
    bonds = bonds.sort_values("cusip").reset_index(drop=True)

    days = business_days()
    trade_days = days[days <= pd.Timestamp(AS_OF)]
    next_day = dict(zip(days[:-1], days[1:]))

    # how likely each bond is to trade: a long tail, so a few bonds trade often and many trade once
    appeal = np.clip(rng.pareto(1.6, size=len(bonds)), 0, 12) + 0.15
    appeal = appeal / appeal.sum()

    # a mid price for every bond on every trading day, walked back from the month-end price
    daily_move = np.clip(0.03 * bonds["duration"].to_numpy(), 0.05, 0.35)
    steps = rng.normal(0, 1, size=(len(trade_days), len(bonds))) * daily_move
    steps[-1] = 0
    mid = bonds["price"].to_numpy() - np.cumsum(steps[::-1], axis=0)[::-1]
    mid = pd.DataFrame(mid, index=trade_days, columns=bonds["cusip"])

    hours = list(HOUR_WEIGHT)
    hour_p = np.array(list(HOUR_WEIGHT.values()), dtype=float) / sum(HOUR_WEIGHT.values())
    names = list(COUNTERPARTIES)
    name_p = [COUNTERPARTIES[name]["share"] for name in names]

    rows = []
    for day in trade_days:
        lift = MONTH_END_LIFT if day >= trade_days[-2] else 1.0
        for _ in range(rng.poisson(TRADES_PER_DAY[day.dayofweek] * lift)):
            bond = bonds.iloc[rng.choice(len(bonds), p=appeal)]
            counterparty = names[rng.choice(len(names), p=name_p)]
            weights = np.array(SIZE_WEIGHT[bond["grade"]], dtype=float)
            step = rng.choice(len(SIZES), p=weights / weights.sum()) + COUNTERPARTIES[counterparty]["shift"]
            quantity = SIZES[int(np.clip(step, 0, len(SIZES) - 1))]
            # one trade in five is an odd amount near the round size
            if rng.random() < 0.2:
                quantity += int(rng.integers(-3, 4)) * 5_000
            rows.append(dict(
                trade_date=day, trade_time=f"{rng.choice(hours, p=hour_p):02d}:{rng.integers(60):02d}",
                cusip=bond["cusip"], side="BUY" if rng.random() < BUY_CHANCE[bond["sector"]] else "SELL",
                quantity=max(quantity, 5_000), counterparty=counterparty,
            ))

    # the block trades: large investment grade trades in the bonds with the most par held
    large = bonds[(bonds["grade"] == "Investment Grade") & (bonds["par_held"] >= 4_000_000)]
    block_bonds = large.iloc[rng.choice(len(large), size=len(BLOCK_SIZES), replace=False)]
    for n, (size, bond) in enumerate(zip(BLOCK_SIZES, block_bonds.itertuples(index=False))):
        rows.append(dict(
            trade_date=trade_days[rng.integers(len(trade_days))],
            trade_time=f"{rng.choice([9, 10, 11, 14])}:{rng.integers(60):02d}".zfill(5),
            cusip=bond.cusip, side="BUY" if n % 2 == 0 and size <= bond.par_held else "SELL",
            quantity=size, counterparty=BLOCK_COUNTERPARTIES[n],
        ))

    trades = pd.DataFrame(rows).sort_values(["trade_date", "trade_time"], kind="stable").reset_index(drop=True)
    trades = trades.merge(bonds[["cusip", "ticker", "sector", "par_held"]], on="cusip", how="left")

    # keep each bond's net buying within the par held at month end. A buy that would go past it
    # is cut to the room left, or becomes a sell when there is no room.
    net_bought: dict[str, int] = {}
    for i, trade in trades.iterrows():
        net = net_bought.get(trade["cusip"], 0)
        if trade["side"] == "BUY":
            room = trade["par_held"] - net
            if room <= 0:
                trades.loc[i, "side"] = "SELL"
            elif trade["quantity"] > room:
                trades.loc[i, "quantity"] = room
        signed = trades.loc[i, "quantity"] if trades.loc[i, "side"] == "BUY" else -trades.loc[i, "quantity"]
        net_bought[trade["cusip"]] = net + signed

    noise = rng.normal(0, 0.04, size=len(trades))
    trades["price"] = [round(mid.loc[t.trade_date, t.cusip] + e, 3) for t, e in zip(trades.itertuples(), noise)]
    trades["principal"] = (trades["quantity"] * trades["price"] / 100).round(2)
    trades["settle_date"] = trades["trade_date"].map(next_day)
    trades["trader"] = trades["sector"].map(DESK)
    trades["trade_id"] = [f"T{n:04d}" for n in range(1, len(trades) + 1)]
    for column in ["trade_date", "settle_date"]:
        trades[column] = trades[column].dt.strftime("%Y-%m-%d")
    return trades[COLUMNS]


def write_blotter(path: Path) -> pd.DataFrame:
    blotter = build_blotter()
    blotter.to_csv(path, index=False, lineterminator="\n")
    return blotter


if __name__ == "__main__":
    blotter = write_blotter(DATA / "trade_blotter.csv")
    print(f"trade blotter {len(blotter)} trades in {blotter['cusip'].nunique()} bonds")
