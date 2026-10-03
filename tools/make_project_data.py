"""Generate the data for the Course 1 project (week 4, days 4 and 5).

Everything here is invented: issuers, CUSIPs, prices, and positions. The script reads
holdings.csv, benchmark.csv, issuers.csv, and ratings.csv and writes three new files:

- project_holdings.csv    the desk's holdings one month later, as a raw extract with problems planted in it
- project_answer_key.md   every planted problem, row by row, and the control totals of the clean book
- project_cover_note.txt  the operations team's cover note, with the control totals

It writes nothing else and changes no existing file. The same seed always produces the same files.

Conventions:
- As-of date 2026-10-30, one month after holdings.csv. The benchmark file stays the September file.
- The book is the September book with some bonds sold out, some resized, and some bought. Every bond
  bought is a bond of benchmark.csv that the desk did not hold in September, so every CUSIP still joins
  to the benchmark, the issuer table, and the rating scale.
- Each bond's OAS is its September OAS times a small random factor, rounded to a whole basis point.
  Yield = the same invented Treasury curve as make_holdings.py, read at the bond's new time to
  maturity, plus the new OAS. Price, accrued interest, and modified duration are then calculated from
  that yield for settlement on the new as-of date, with the same semiannual 30/360 formulas as
  make_holdings.py (copied below, so that this script does not import or change that file).
- In every clean row: spread_duration = duration, dts = spread_duration x oas, and
  market_value = par_held x (price + accrued) / 100.

Usage (from the repo root):  python tools/make_project_data.py
"""
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261030
AS_OF = date(2026, 10, 30)
DATA = Path(__file__).resolve().parent.parent / "data"

SOLD, RESIZED, BOUGHT = 17, 40, 23
# planted problems: how many rows get each one
N_DUPLICATES, N_SECTOR, N_MISSING_OAS, N_PRICE, N_NEGATIVE_FACE, N_MATURITY = 3, 9, 4, 3, 2, 1

COLUMNS = ["as_of_date", "cusip", "ticker", "issuer", "sector", "rating", "coupon", "maturity", "price",
           "price_date", "accrued", "yield_pct", "oas", "duration", "spread_duration", "dts",
           "amount_outstanding", "par_held", "market_value"]


# ---- bond arithmetic, copied from tools/make_holdings.py so that both files follow one convention
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


# ---- the clean October book
def build_clean(rng: np.random.Generator) -> pd.DataFrame:
    september = pd.read_csv(DATA / "holdings.csv")
    benchmark = pd.read_csv(DATA / "benchmark.csv")
    issuers = pd.read_csv(DATA / "issuers.csv")
    ratings = pd.read_csv(DATA / "ratings.csv")

    # the five widest bonds stay in the book: they are the real outliers the student has to recognise
    widest = september.nlargest(5, "oas").index
    sold = rng.choice(september.index.difference(widest), size=SOLD, replace=False)
    kept = september.drop(index=sold)

    # resized positions: face moves by one to four lots of 250,000, and never to zero
    kept = kept.copy()
    for i in rng.choice(kept.index, size=RESIZED, replace=False):
        change = int(rng.integers(1, 5)) * 250_000 * (1 if rng.random() < 0.5 else -1)
        if kept.loc[i, "par_held"] + change <= 0:
            change = -change
        kept.loc[i, "par_held"] += change

    # bonds bought: benchmark bonds the desk did not hold in September
    not_held = benchmark[~benchmark["cusip"].isin(september["cusip"])]
    bought = not_held.sample(n=BOUGHT, random_state=int(rng.integers(1_000_000)))[
        [c for c in COLUMNS if c not in ("par_held", "market_value")]].copy()
    bought["par_held"] = rng.integers(1, 21, size=BOUGHT) * 250_000

    book = pd.concat([kept, bought], ignore_index=True).sort_values(["ticker", "maturity"]).reset_index(drop=True)

    # one month of spread moves, then every price-dependent column from the new yield
    book["oas"] = np.maximum(5, (book["oas"] * rng.lognormal(0, 0.05, size=len(book))).round()).astype(int)
    maturities = [date.fromisoformat(m) for m in book["maturity"]]
    years = [days_360(AS_OF, m) / 360 for m in maturities]
    book["yield_pct"] = [round(round(float(treasury_yield(t)), 3) + oas / 100, 3) for t, oas in zip(years, book["oas"])]
    results = [analytics(c, y, AS_OF, m) for c, y, m in zip(book["coupon"], book["yield_pct"], maturities)]
    book["price"] = [round(clean, 3) for clean, _, _ in results]
    book["accrued"] = [round(accrued, 3) for _, accrued, _ in results]
    book["duration"] = [round(duration, 3) for _, _, duration in results]
    book["spread_duration"] = book["duration"]
    book["dts"] = (book["spread_duration"] * book["oas"]).round(1)
    book["market_value"] = (book["par_held"] * (book["price"] + book["accrued"]) / 100).round(2)
    book["as_of_date"] = AS_OF.isoformat()
    book["price_date"] = AS_OF.isoformat()

    if book["cusip"].duplicated().any():
        raise ValueError("a CUSIP appears twice in the clean book")
    if not set(book["cusip"]) <= set(benchmark["cusip"]):
        raise ValueError("a bond of the book is not in benchmark.csv")
    if not set(book["ticker"]) <= set(issuers["ticker"]) or not set(book["rating"]) <= set(ratings["rating"]):
        raise ValueError("a ticker or a rating of the book does not join to its reference table")
    return book[COLUMNS]


def control_totals(clean: pd.DataFrame) -> dict:
    return dict(bonds=len(clean), face=int(clean["par_held"].sum()), market_value=round(float(clean["market_value"].sum()), 2))


# ---- the raw extract
def build_messy(clean: pd.DataFrame, rng: np.random.Generator) -> tuple[pd.DataFrame, dict]:
    """Plant the problems. Returns the extract and a record of what was changed, keyed by problem."""
    messy = clean.copy()
    messy["oas"] = messy["oas"].astype("Int64")  # whole numbers that can also be blank
    messy["order"] = np.arange(len(messy), dtype=float)

    # the planted rows never overlap, and never touch the five widest bonds
    eligible = clean.index.difference(clean.nlargest(5, "oas").index)
    # the wrong maturity is ten years early, so pick a bond for which that lands before the as-of date
    short = [i for i in eligible if clean.loc[i, "maturity"] < "2036-10-30"]
    maturity_rows = rng.choice(short, size=N_MATURITY, replace=False)
    rows = rng.choice(eligible.difference(maturity_rows),
                      size=N_DUPLICATES + N_SECTOR + N_MISSING_OAS + N_PRICE + N_NEGATIVE_FACE, replace=False)
    cuts = np.cumsum([N_DUPLICATES, N_SECTOR, N_MISSING_OAS, N_PRICE])
    duplicate_rows, sector_rows, oas_rows, price_rows, face_rows = np.split(rows, cuts)

    planted: dict = {name: [] for name in ["duplicates", "sector", "missing_oas", "price", "negative_face", "maturity"]}

    def bond(i) -> dict:
        return dict(cusip=clean.loc[i, "cusip"], ticker=clean.loc[i, "ticker"])

    for n, i in enumerate(sorted(sector_rows)):
        name = clean.loc[i, "sector"]
        written = [name.lower(), name.upper(), name + " ", " " + name.lower()][n % 4]
        messy.loc[i, "sector"] = written
        planted["sector"].append(bond(i) | dict(written=written, clean=name))

    for i in sorted(oas_rows):
        messy.loc[i, "oas"] = pd.NA
        planted["missing_oas"].append(bond(i) | dict(written="blank", clean=int(clean.loc[i, "oas"])))

    for n, i in enumerate(sorted(price_rows)):
        # the first two are a hundredth of the price and the third is a hundred times it
        price = clean.loc[i, "price"]
        written = round(price * 100, 1) if n == N_PRICE - 1 else round(price / 100, 5)
        messy.loc[i, "price"] = written
        planted["price"].append(bond(i) | dict(written=written, clean=price))

    for i in sorted(face_rows):
        messy.loc[i, "par_held"] = -clean.loc[i, "par_held"]
        planted["negative_face"].append(bond(i) | dict(written=int(-clean.loc[i, "par_held"]), clean=int(clean.loc[i, "par_held"])))

    for i in sorted(maturity_rows):
        maturity = clean.loc[i, "maturity"]
        written = f"{int(maturity[:4]) - 10}{maturity[4:]}"
        messy.loc[i, "maturity"] = written
        planted["maturity"].append(bond(i) | dict(written=written, clean=maturity))

    # each copy sits directly below the row it repeats
    copies = messy.loc[sorted(duplicate_rows)]
    planted["duplicates"] = [bond(i) for i in sorted(duplicate_rows)]
    messy = pd.concat([messy, copies]).sort_values("order", kind="stable").drop(columns="order").reset_index(drop=True)
    return messy, planted


def answer_key(clean: pd.DataFrame, messy: pd.DataFrame, planted: dict) -> str:
    totals = control_totals(clean)

    def listing(name: str, with_values: bool = True) -> str:
        lines = []
        for item in planted[name]:
            line = f"- `{item['cusip']}` ({item['ticker']})"
            if with_values:
                line += f": in the file `{item['written']}`, clean value `{item['clean']}`"
            lines.append(line)
        return "\n".join(lines)

    widest = clean.nlargest(5, "oas")
    mismatched = len(planted["price"]) + len(planted["negative_face"])
    return f"""# Answer key: project_holdings.csv

`project_holdings.csv` is the desk's book as of {AS_OF}, with these problems planted on purpose. Generated by `tools/make_project_data.py` with seed {SEED}. The clean book has {totals['bonds']} bonds and the file has {len(messy)} rows.

## Duplicate rows ({len(planted['duplicates'])} rows)
Each of these CUSIPs appears twice, the second row an exact copy directly below the first. Fix: remove the copies.
{listing('duplicates', with_values=False)}

## Sector names with the wrong case or a stray space ({len(planted['sector'])} rows)
The file has {messy['sector'].nunique()} different sector values where the clean book has {clean['sector'].nunique()}. Fix: strip the spaces and give each word a capital.
{listing('sector')}

## Missing OAS ({len(planted['missing_oas'])} rows)
The `oas` cell is blank. Fix: `dts` divided by `spread_duration`, rounded to a whole basis point, gives the clean value back.
{listing('missing_oas')}

## Prices in the wrong units ({len(planted['price'])} rows)
The price is a hundredth of the clean price, or a hundred times it. `market_value` was not changed. Fix: put the price back in units of per 100 of face.
{listing('price')}

## Face held with the wrong sign ({len(planted['negative_face'])} rows)
`par_held` is negative. `market_value` was not changed and is positive. Fix: the positive amount.
{listing('negative_face')}

## Maturity before the as-of date ({len(planted['maturity'])} row)
The year of the maturity is ten years early. Fix: the maturity of the same CUSIP in `benchmark.csv`.
{listing('maturity')}

## Market value that does not tie out ({mismatched} rows)
Not a separate problem. In the {len(planted['price'])} rows with a wrong price and the {len(planted['negative_face'])} rows with a negative face, `market_value` does not equal `par_held` x (`price` + `accrued`) / 100. It does in every other row, and in all rows once the two fixes are made.

## Wide spreads (not errors)
These are real features of the data: the five widest spreads in the clean book.
""" + "\n".join(f"- `{b.cusip}` ({b.ticker}), {b.rating}, OAS {b.oas} bp" for b in widest.itertuples()) + f"""

## Checks that find nothing
Tickers, ratings, CUSIP lengths, coupons, durations, and price dates are clean. Every CUSIP is in `benchmark.csv`.

## Control totals of the clean book
- Bonds: {totals['bonds']:,}
- Total face: {totals['face']:,} dollars
- Total market value: {totals['market_value']:,.2f} dollars

## What changed from September
Of the 200 bonds in `holdings.csv`, {SOLD} were sold out, {RESIZED} changed size, and {BOUGHT} benchmark bonds not held in September were bought.
"""


def cover_note(clean: pd.DataFrame) -> str:
    totals = control_totals(clean)
    return f"""To: Credit desk
From: Operations
Subject: Month-end holdings extract, as of {AS_OF}

The month-end extract is attached as project_holdings.csv.

Control totals for the book:
  Number of bonds:      {totals['bonds']:,}
  Total face:           {totals['face']:,} dollars
  Total market value:   {totals['market_value']:,.2f} dollars

Market value is face times clean price plus accrued interest, divided by 100.
All positions are priced as of {AS_OF}.
Please tell us if the extract does not agree with these totals.
"""


def build() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    rng = np.random.default_rng(SEED)
    clean = build_clean(rng)
    messy, planted = build_messy(clean, rng)
    return clean, messy, planted


def write_files(folder: Path) -> None:
    clean, messy, planted = build()
    messy.to_csv(folder / "project_holdings.csv", index=False, lineterminator="\n")
    (folder / "project_answer_key.md").write_text(answer_key(clean, messy, planted), encoding="utf-8", newline="\n")
    (folder / "project_cover_note.txt").write_text(cover_note(clean), encoding="utf-8", newline="\n")
    print(f"project holdings {len(messy)} rows, clean book {len(clean)} bonds")


if __name__ == "__main__":
    write_files(DATA)
