"""Generate the synthetic bond data used from week 2 onward.

Everything here is invented: issuers, tickers, CUSIPs, prices, and positions.
The same seed always produces the same files, so every student gets identical data.

Conventions (fixed with Jeff on 2026-10-03):
- Fixed-rate bullet bonds, semiannual coupons, 30/360 day count.
- Yield = synthetic Treasury yield for the bond's maturity + OAS. Price is then
  calculated from that yield, so price and yield always agree.
- Duration is modified duration. Spread duration equals modified duration for
  these bonds. DTS = spread duration x OAS (in basis points).
- CUSIPs use issuer numbers in the 99xxxx range reserved for internal use, so
  they match no real security. Each has a valid check digit.

Usage (from the repo root):  python tools/make_holdings.py
"""
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261003
AS_OF = date(2026, 9, 30)
DATA = Path(__file__).resolve().parent.parent / "data"

RATINGS = ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-",
           "BB+", "BB", "BB-", "B+", "B", "B-", "CCC+", "CCC"]
SCORE = {rating: i + 1 for i, rating in enumerate(RATINGS)}
BUCKET = {r: r.rstrip("+-") for r in RATINGS}

# typical OAS in basis points for a 10-year bond, by rating score
BASE_OAS = {1: 30, 2: 40, 3: 48, 4: 56, 5: 68, 6: 80, 7: 95, 8: 115, 9: 135, 10: 165,
            11: 215, 12: 260, 13: 310, 14: 370, 15: 440, 16: 530, 17: 720, 18: 900}

SECTORS = {
    "Energy": ["Energy", "Pipeline", "Resources"],
    "Transportation": ["Rail", "Freight", "Logistics"],
    "Materials": ["Paper", "Chemicals", "Metals"],
    "Consumer": ["Foods", "Retail", "Brands"],
    "Telecom": ["Telecom", "Wireless", "Networks"],
    "Health Care": ["Health", "Pharma", "Medical"],
    "Utilities": ["Utilities", "Power", "Water"],
    "Technology": ["Systems", "Software", "Devices"],
    "Financials": ["Bancorp", "Finance", "Insurance"],
    "Industrials": ["Industrial", "Machinery", "Aerospace"],
}

# the issuers students already met in week 1, kept so the big file feels familiar
KNOWN = [
    ("QVNE", "Quorvane Energy", "Energy", "BBB"),
    ("DNMR", "Dunmarrow Rail", "Transportation", "BB+"),
    ("PLWK", "Pellwick Paper", "Materials", "A-"),
    ("HLVF", "Halvering Foods", "Consumer", "B+"),
    ("OSTV", "Ostrevale Telecom", "Telecom", "BBB-"),
    ("VYRH", "Veyrholt Health", "Health Care", "BB"),
    ("TRNW", "Tarnwick Utilities", "Utilities", "A"),
    ("OSMC", "Osmere Chemicals", "Materials", "BBB-"),
    ("CLDB", "Calderby Retail", "Consumer", "B"),
]

STARTS = ["Dral", "Plev", "Hesk", "Zar", "Vyr", "Trom", "Skel", "Clav", "Brux", "Morv", "Thal", "Wyx",
          "Kez", "Zeph", "Grov", "Lorv", "Fesk", "Jax", "Kril", "Mulv", "Nev", "Prax", "Rulv", "Sylv",
          "Tov", "Vrax", "Xan", "Yarv", "Bez", "Corv", "Delv", "Elv", "Farv", "Galv", "Hulv", "Quel"]
ENDS = ["ane", "orin", "ellix", "undra", "ovar", "imer", "azor", "ithe", "oquil", "ebran",
        "ulex", "ostrin", "amyth", "erone", "izal", "entor", "iskan", "olvey"]


def cusip_check_digit(first8: str) -> str:
    total = 0
    for position, char in enumerate(first8, start=1):
        value = int(char) if char.isdigit() else ord(char) - 55
        if position % 2 == 0:
            value *= 2
        total += value // 10 + value % 10
    return str((10 - total % 10) % 10)


def days_360(start: date, end: date) -> int:
    """Days between two dates on the US 30/360 basis."""
    d1, d2 = min(start.day, 30), end.day
    if d2 == 31 and d1 == 30:
        d2 = 30
    return (end.year - start.year) * 360 + (end.month - start.month) * 30 + (d2 - d1)


def add_months(d: date, months: int) -> date:
    index = d.year * 12 + d.month - 1 + months
    return date(index // 12, index % 12 + 1, d.day)


def analytics(coupon: float, yield_pct: float, settle: date, maturity: date) -> tuple[float, float, float]:
    """Clean price, accrued interest, and modified duration for a semiannual 30/360 bullet bond."""
    # walk back from maturity in six-month steps to find the coupon dates around settlement
    next_coupon, remaining = maturity, 1
    while add_months(next_coupon, -6) > settle:
        next_coupon = add_months(next_coupon, -6)
        remaining += 1
    previous_coupon = add_months(next_coupon, -6)

    accrued_days = days_360(previous_coupon, settle)
    fraction = (180 - accrued_days) / 180  # part of a period left until the next coupon
    y = yield_pct / 100 / 2
    cash = coupon / 2

    dirty, weighted_time = 0.0, 0.0
    for k in range(remaining):
        flow = cash + (100 if k == remaining - 1 else 0)
        present_value = flow / (1 + y) ** (fraction + k)
        dirty += present_value
        weighted_time += (fraction + k) / 2 * present_value

    accrued = cash * accrued_days / 180
    modified_duration = weighted_time / dirty / (1 + y)
    return dirty - accrued, accrued, modified_duration


def treasury_yield(years: float) -> float:
    """A smooth, invented Treasury curve: about 3.7 percent at 1 year and 4.6 percent at 30 years."""
    return 3.55 + 1.05 * (1 - np.exp(-years / 7))


def build_issuers(rng: np.random.Generator) -> pd.DataFrame:
    rows = [dict(ticker=t, issuer=n, sector=s, rating=r) for t, n, s, r in KNOWN]
    tickers = {row["ticker"] for row in rows}
    names = {row["issuer"].split()[0] for row in rows}
    weights = np.array([1, 1, 2, 3, 5, 7, 8, 9, 10, 9, 7, 6, 5, 4, 3, 2, 1, 1], dtype=float)
    weights /= weights.sum()
    sector_names = list(SECTORS)
    while len(rows) < 150:
        word = rng.choice(STARTS) + rng.choice(ENDS)
        if word in names:
            continue
        ticker = (word[:3] + word[-1]).upper()
        if ticker in tickers:
            continue
        sector = sector_names[rng.integers(len(sector_names))]
        rows.append(dict(ticker=ticker, issuer=f"{word} {rng.choice(SECTORS[sector])}", sector=sector,
                         rating=RATINGS[rng.choice(len(RATINGS), p=weights)]))
        names.add(word)
        tickers.add(ticker)
    issuers = pd.DataFrame(rows)
    issuers.insert(3, "country", "US")
    return issuers


def build_benchmark(issuers: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for number, issuer in enumerate(issuers.itertuples(index=False), start=1):
        issuer_number = f"99{number:03d}{chr(65 + number % 26)}"
        issuer_effect = rng.lognormal(0, 0.15)
        score = SCORE[issuer.rating]
        for issue in range(int(rng.integers(3, 9))):
            years = float(rng.uniform(1.0, 30.0)) if rng.random() < 0.25 else float(rng.uniform(1.0, 12.0))
            month_offset = int(round(years * 12))
            maturity = add_months(date(AS_OF.year, AS_OF.month, int(rng.integers(1, 29))), month_offset)
            years_to_maturity = days_360(AS_OF, maturity) / 360

            oas = BASE_OAS[score] * (0.70 + 0.30 * min(years_to_maturity, 10) / 10) * issuer_effect * rng.lognormal(0, 0.18)
            oas = int(round(oas))
            bond_yield = round(round(float(treasury_yield(years_to_maturity)), 3) + oas / 100, 3)
            coupon = float(np.clip(round((bond_yield + rng.normal(0, 0.9)) / 0.125) * 0.125, 1.5, 11.0))

            first8 = issuer_number + chr(65 + issue // 26) + chr(65 + issue % 26)
            rows.append(dict(
                cusip=first8 + cusip_check_digit(first8), ticker=issuer.ticker, issuer=issuer.issuer,
                sector=issuer.sector, rating=issuer.rating, coupon=coupon, maturity=maturity,
                yield_pct=bond_yield, oas=oas,
                amount_outstanding=int(rng.integers(6, 51)) * 50_000_000,
            ))
    bonds = pd.DataFrame(rows)

    # a handful of distressed bonds trading at very wide spreads
    weak = bonds.index[bonds["rating"].map(SCORE) >= 15].to_numpy()
    for i in rng.choice(weak, size=6, replace=False):
        bonds.loc[i, "oas"] = int(bonds.loc[i, "oas"] * rng.uniform(2.5, 4.0))
        years_to_maturity = days_360(AS_OF, bonds.loc[i, "maturity"]) / 360
        bonds.loc[i, "yield_pct"] = round(round(float(treasury_yield(years_to_maturity)), 3) + bonds.loc[i, "oas"] / 100, 3)

    results = [analytics(b.coupon, b.yield_pct, AS_OF, b.maturity) for b in bonds.itertuples(index=False)]
    bonds["price"] = [round(clean, 3) for clean, _, _ in results]
    bonds["accrued"] = [round(accrued, 3) for _, accrued, _ in results]
    bonds["duration"] = [round(duration, 3) for _, _, duration in results]
    bonds["spread_duration"] = bonds["duration"]
    bonds["dts"] = (bonds["spread_duration"] * bonds["oas"]).round(1)
    bonds["market_value"] = (bonds["amount_outstanding"] * (bonds["price"] + bonds["accrued"]) / 100).round(2)
    bonds["weight_pct"] = (bonds["market_value"] / bonds["market_value"].sum() * 100).round(4)
    bonds.insert(0, "as_of_date", AS_OF)
    bonds["price_date"] = AS_OF
    return bonds


COLUMNS = ["as_of_date", "cusip", "ticker", "issuer", "sector", "rating", "coupon", "maturity", "price",
           "price_date", "accrued", "yield_pct", "oas", "duration", "spread_duration", "dts", "amount_outstanding"]


def build_holdings(benchmark: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    # one bond from each week 1 issuer, then a random draw to reach 200
    known = benchmark[benchmark["ticker"].isin([t for t, *_ in KNOWN])].groupby("ticker").head(1)
    others = benchmark.drop(known.index)
    picked = others.sample(n=200 - len(known), random_state=int(rng.integers(1_000_000)))
    holdings = pd.concat([known, picked]).sort_values(["ticker", "maturity"])[COLUMNS].reset_index(drop=True)
    holdings["par_held"] = rng.integers(1, 21, size=len(holdings)) * 250_000
    holdings["market_value"] = (holdings["par_held"] * (holdings["price"] + holdings["accrued"]) / 100).round(2)
    return holdings


def build_messy(holdings: pd.DataFrame, rng: np.random.Generator) -> tuple[pd.DataFrame, str]:
    messy = holdings.copy()
    messy["rating"] = messy["rating"].astype(object)
    messy["ticker"] = messy["ticker"].astype(object)
    rows = rng.choice(len(messy), size=25, replace=False)
    missing, ticker_rows, stale, wrong_units, duplicated = rows[:5], rows[5:13], rows[13:19], rows[19:21], rows[21:25]

    messy.loc[missing, "rating"] = None
    for n, i in enumerate(ticker_rows):
        t = messy.loc[i, "ticker"]
        messy.loc[i, "ticker"] = [f" {t}", f"{t} ", t.lower(), f" {t.lower()} "][n % 4]
    messy.loc[stale, "price_date"] = [date(2026, 8, int(d)) for d in rng.integers(3, 29, size=len(stale))]
    messy.loc[wrong_units, "yield_pct"] = (messy.loc[wrong_units, "yield_pct"] / 100).round(5)
    messy = pd.concat([messy, messy.loc[duplicated]], ignore_index=True)

    distressed = holdings.sort_values("oas", ascending=False).head(5)

    def listing(index) -> str:
        return "\n".join(f"- `{holdings.loc[i, 'cusip']}` ({holdings.loc[i, 'ticker']})" for i in sorted(index))

    key = f"""# Answer key: holdings_messy.csv

`holdings_messy.csv` is `holdings.csv` with these problems planted on purpose. Generated by `tools/make_holdings.py` with seed {SEED}.

## Missing ratings ({len(missing)} bonds)
The rating is blank.
{listing(missing)}

## Tickers with stray spaces or lower case ({len(ticker_rows)} bonds)
{listing(ticker_rows)}

## Stale prices ({len(stale)} bonds)
`price_date` is in August 2026, not the as-of date of {AS_OF}.
{listing(stale)}

## Yields in the wrong units ({len(wrong_units)} bonds)
`yield_pct` was entered as a decimal, for example 0.0612 where it should be 6.12.
{listing(wrong_units)}

## Duplicate rows ({len(duplicated)} bonds)
Each of these CUSIPs appears twice. The file has {len(messy)} rows where the clean file has {len(holdings)}.
{listing(duplicated)}

## Distressed outliers (not errors)
These are real features of the data, present in the clean file too: the five widest spreads in the portfolio.
""" + "\n".join(f"- `{b.cusip}` ({b.ticker}), {b.rating}, OAS {b.oas} bp" for b in distressed.itertuples()) + "\n"
    return messy, key


def main() -> None:
    rng = np.random.default_rng(SEED)
    DATA.mkdir(exist_ok=True)

    issuers = build_issuers(rng)
    benchmark = build_benchmark(issuers, rng)
    holdings = build_holdings(benchmark, rng)
    messy, key = build_messy(holdings, rng)
    ratings = pd.DataFrame({"rating": RATINGS, "score": [SCORE[r] for r in RATINGS], "bucket": [BUCKET[r] for r in RATINGS],
                            "grade": ["Investment Grade" if SCORE[r] <= 10 else "High Yield" for r in RATINGS]})
    positions = holdings[["cusip", "ticker", "coupon", "maturity", "price", "par_held"]]

    issuers.to_csv(DATA / "issuers.csv", index=False)
    ratings.to_csv(DATA / "ratings.csv", index=False)
    benchmark[COLUMNS + ["market_value", "weight_pct"]].to_csv(DATA / "benchmark.csv", index=False)
    holdings.to_csv(DATA / "holdings.csv", index=False)
    positions.to_csv(DATA / "positions.csv", index=False)
    messy.to_csv(DATA / "holdings_messy.csv", index=False)
    (DATA / "holdings_messy_answer_key.md").write_text(key, encoding="utf-8")

    print(f"issuers {len(issuers)}, benchmark {len(benchmark)}, holdings {len(holdings)}, messy {len(messy)}")


if __name__ == "__main__":
    main()
