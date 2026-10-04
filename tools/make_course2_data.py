"""Generate the data for Course 2 (Bond Math): the invented Treasury curve and the capstone files.

Everything here is invented: issuers, CUSIPs, prices, and positions. The script reads holdings.csv,
benchmark.csv, issuers.csv, and ratings.csv and writes four new files:

- course2_treasury_curve.csv        the invented curve the holdings were built on, at ten tenors
- course2_capstone_holdings.csv     the desk's book as of 2026-11-30, a raw extract with bond-math problems planted
- course2_capstone_answer_key.md    every planted problem, row by row, the fixes, and the clean control totals
- course2_capstone_cover_note.txt   the operations team's cover note, with the control totals

It writes nothing else and changes no existing file. The same seed always produces the same files.

Conventions are those of COURSE2_SPEC.md ("Conventions, fixed in writing"): semiannual, US 30/360 as Excel
counts it, coupon dates computed from maturity directly with the month-end rule, PRICE's DSC = E - A, and
simple interest in the final coupon period. The bond math below is copied from the course's reference
bondmath (30/360 only), so this script imports nothing private; tests/test_course2_data.py checks it
against Excel's values in bondmath_excel_reference.csv.

The November book: the September book with some bonds sold, some resized, and some bought from
benchmark.csv, plus two new invented bonds (one in its final coupon period, one maturing on a month end).
Each OAS is its September OAS times a lognormal factor, rounded to a whole basis point. Yield = the
invented curve read at the bond's new time to maturity, rounded to 3 decimals, plus the OAS. Price,
accrued, and modified duration are recomputed from that yield for settlement on 2026-11-30.

Usage (from the repo root):  python tools/make_course2_data.py
"""
import calendar
import math
import re
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261130
AS_OF = date(2026, 11, 30)
DATA = Path(__file__).resolve().parent.parent / "data"

CURVE_TENORS = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0]
SOLD, RESIZED, BOUGHT = 15, 30, 12
# the two benchmark bonds maturing on 28 February of a non-leap year: the data generator and Excel
# disagree on their coupon dates, so they are never bought
BENCHMARK_EXCEPTIONS = ["99018SAA8", "99128YAE4"]

# planted problems: how many rows get each one
N_DIRTY_PRICE, N_YIELD_DECIMAL, N_COUPON_DECIMAL = 3, 3, 2
N_BLANK_PRICE, N_BLANK_YIELD, N_MACAULAY, N_ACCRUED_ACT360 = 2, 2, 3, 3
N_MATURITY, N_DUPLICATES = 1, 2
PROBLEMS = ["dirty_price", "yield_decimal", "coupon_decimal", "blank_price", "blank_yield", "macaulay",
            "accrued_act360", "maturity", "duplicates"]

# the two new invented bonds: an existing issuer's 99xxxx number and an unused issue code (Y*)
NEW_BONDS = [
    dict(ticker="TRNW", issue_code="YA", coupon=4.25, maturity="2027-03-15", oas=60,
         amount_outstanding=600_000_000, par_held=3_000_000, note="in its final coupon period"),
    dict(ticker="OSMC", issue_code="YA", coupon=5.5, maturity="2033-08-31", oas=150,
         amount_outstanding=900_000_000, par_held=2_500_000, note="maturing on a month end"),
]

COLUMNS = ["as_of_date", "cusip", "ticker", "issuer", "sector", "rating", "coupon", "maturity", "price",
           "price_date", "accrued", "yield_pct", "oas", "duration", "spread_duration", "dts",
           "amount_outstanding", "par_held", "market_value"]


# ---- bond math, copied from the course's reference bondmath (30/360 only)
def add_months(d: date, months: int) -> date:
    """d moved by whole months, the day clamped to the length of the new month."""
    year, month_zero_based = divmod(d.year * 12 + d.month - 1 + months, 12)
    month = month_zero_based + 1
    return date(year, month, min(d.day, calendar.monthrange(year, month)[1]))


def coupon_dates(settlement: date, maturity: date, frequency: int = 2) -> list[date]:
    """The previous coupon date, then every coupon date left through maturity (month-end rule applied)."""
    if frequency not in (1, 2, 4):
        raise ValueError(f"frequency must be 1, 2, or 4, not {frequency}")
    if settlement >= maturity:
        raise ValueError(f"settlement {settlement} must be before maturity {maturity}")
    step_months = 12 // frequency
    month_end = maturity.day == calendar.monthrange(maturity.year, maturity.month)[1]
    dates = []
    k = 0
    while True:
        # each date from maturity directly, so a 31st never drifts to the 28th
        coupon_date = add_months(maturity, -k * step_months)
        if month_end:
            coupon_date = date(coupon_date.year, coupon_date.month,
                               calendar.monthrange(coupon_date.year, coupon_date.month)[1])
        dates.append(coupon_date)
        if coupon_date <= settlement:
            break
        k += 1
    dates.reverse()
    return dates


def days_30_360(start: date, end: date) -> int:
    """Days on the US 30/360 basis as Excel's COUPDAYBS and YEARFRAC(..., 0) count them."""
    d1, d2 = start.day, end.day
    start_is_feb_end = start.month == 2 and start.day == calendar.monthrange(start.year, 2)[1]
    end_is_feb_end = end.month == 2 and end.day == calendar.monthrange(end.year, 2)[1]
    if start_is_feb_end:
        d1 = 30
    if start_is_feb_end and end_is_feb_end:
        d2 = 30
    if start.day == 31:
        d1 = 30
    # Excel looks at the start date's own day here, not at D1 after the February rule
    if end.day == 31 and start.day >= 30:
        d2 = 30
    return 360 * (end.year - start.year) + 30 * (end.month - start.month) + (d2 - d1)


def coupon_period_days(settlement: date, maturity: date, frequency: int = 2) -> tuple[int, int, int]:
    """(A, E, DSC) under 30/360, with DSC = E - A as Excel's PRICE uses it."""
    previous_coupon = coupon_dates(settlement, maturity, frequency)[0]
    days_accrued = days_30_360(previous_coupon, settlement)
    days_in_period = 360 // frequency
    return days_accrued, days_in_period, days_in_period - days_accrued


def accrued_interest(settlement: date, maturity: date, coupon_pct: float, frequency: int = 2) -> float:
    """Accrued interest per 100 of face: coupon_pct / frequency x A / E."""
    days_accrued, days_in_period, _ = coupon_period_days(settlement, maturity, frequency)
    return coupon_pct / frequency * days_accrued / days_in_period


def _discounted_flows(settlement: date, maturity: date, coupon_pct: float, yield_pct: float,
                      frequency: int) -> list[tuple[float, float]]:
    """(time in periods, present value) of each remaining cash flow, compound discounting."""
    coupons_left = len(coupon_dates(settlement, maturity, frequency)) - 1
    _, days_in_period, days_to_next = coupon_period_days(settlement, maturity, frequency)
    w = days_to_next / days_in_period
    period_yield = yield_pct / 100 / frequency
    coupon = coupon_pct / frequency
    flows = []
    for k in range(coupons_left):
        cash_flow = coupon + 100 if k == coupons_left - 1 else coupon
        flows.append((w + k, cash_flow / (1 + period_yield) ** (w + k)))
    return flows


def price(settlement: date, maturity: date, coupon_pct: float, yield_pct: float, frequency: int = 2) -> float:
    """Clean price per 100, as Excel's PRICE (simple interest in the final coupon period)."""
    coupons_left = len(coupon_dates(settlement, maturity, frequency)) - 1
    if coupons_left == 1:
        _, days_in_period, days_to_next = coupon_period_days(settlement, maturity, frequency)
        w = days_to_next / days_in_period
        dirty = (100 + coupon_pct / frequency) / (1 + w * yield_pct / 100 / frequency)
    else:
        dirty = sum(pv for _, pv in _discounted_flows(settlement, maturity, coupon_pct, yield_pct, frequency))
    return dirty - accrued_interest(settlement, maturity, coupon_pct, frequency)


def yield_to_maturity(settlement: date, maturity: date, coupon_pct: float, clean_price: float,
                      frequency: int = 2) -> float:
    """Yield in percent from a clean price, as Excel's YIELD x 100."""
    if len(coupon_dates(settlement, maturity, frequency)) - 1 == 1:
        # final period: YIELD's closed form, with DSR the 30/360 days from settlement to maturity
        days_accrued, days_in_period, _ = coupon_period_days(settlement, maturity, frequency)
        coupon = coupon_pct / frequency
        paid = clean_price + coupon * days_accrued / days_in_period
        return (100 + coupon - paid) / paid * frequency * days_in_period / days_30_360(settlement, maturity) * 100
    low_pct, high_pct = -5.0, 100.0
    highest_price = price(settlement, maturity, coupon_pct, low_pct, frequency)
    lowest_price = price(settlement, maturity, coupon_pct, high_pct, frequency)
    if not lowest_price <= clean_price <= highest_price:
        raise ValueError(f"price {clean_price} is outside {lowest_price:.6f} to {highest_price:.6f}")
    while high_pct - low_pct > 1e-10:
        mid_pct = (low_pct + high_pct) / 2
        if price(settlement, maturity, coupon_pct, mid_pct, frequency) > clean_price:
            low_pct = mid_pct
        else:
            high_pct = mid_pct
    return (low_pct + high_pct) / 2


def macaulay_duration(settlement: date, maturity: date, coupon_pct: float, yield_pct: float,
                      frequency: int = 2) -> float:
    """Macaulay duration in years, as Excel's DURATION (DSC / E / f in the final period)."""
    flows = _discounted_flows(settlement, maturity, coupon_pct, yield_pct, frequency)
    return sum(t / frequency * pv for t, pv in flows) / sum(pv for _, pv in flows)


def modified_duration(settlement: date, maturity: date, coupon_pct: float, yield_pct: float,
                      frequency: int = 2) -> float:
    """Modified duration in years, as Excel's MDURATION."""
    return (macaulay_duration(settlement, maturity, coupon_pct, yield_pct, frequency)
            / (1 + yield_pct / 100 / frequency))


def treasury_yield(years: float) -> float:
    """The smooth invented Treasury curve tools/make_holdings.py built every yield on, in percent."""
    return 3.55 + 1.05 * (1 - math.exp(-years / 7))


def round3(x: float) -> float:
    """Round to 3 decimals with Python's round on a Python float. round() on a numpy float64 can settle
    a tie such as 1.0875 the other way, so every 3-decimal figure goes through here."""
    return round(float(x), 3)


def curve_yield_pct(years: float) -> float:
    return round3(treasury_yield(years))


def cusip_check_digit(base: str) -> str:
    """Check digit of an 8-character CUSIP base (digits and capital letters)."""
    total = 0
    for i, char in enumerate(base):
        value = int(char) if char.isdigit() else ord(char) - ord("A") + 10
        if i % 2 == 1:
            value *= 2
        total += value // 10 + value % 10
    return str((10 - total % 10) % 10)


def month_end(d: date) -> bool:
    return d.day == calendar.monthrange(d.year, d.month)[1]


# ---- the curve file
def build_curve() -> pd.DataFrame:
    return pd.DataFrame({"tenor_years": CURVE_TENORS, "yield_pct": [curve_yield_pct(t) for t in CURVE_TENORS]})


# ---- the clean November book
def new_bond_rows(benchmark: pd.DataFrame, issuers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    taken = all_data_cusips()
    for spec in NEW_BONDS:
        issuer = issuers.set_index("ticker").loc[spec["ticker"]]
        issuer_number = benchmark.loc[benchmark["ticker"] == spec["ticker"], "cusip"].str[:6].unique()
        if len(issuer_number) != 1:
            raise ValueError(f"{spec['ticker']} does not have exactly one issuer number in benchmark.csv")
        base = issuer_number[0] + spec["issue_code"]
        cusip = base + cusip_check_digit(base)
        if cusip in taken:
            raise ValueError(f"new CUSIP {cusip} already appears in a file in data/")
        rows.append(dict(cusip=cusip, ticker=spec["ticker"], issuer=issuer["issuer"], sector=issuer["sector"],
                         rating=issuer["rating"], coupon=spec["coupon"], maturity=spec["maturity"],
                         oas=spec["oas"], amount_outstanding=spec["amount_outstanding"], par_held=spec["par_held"]))
    return pd.DataFrame(rows)


def all_data_cusips() -> set[str]:
    """Every 9-character CUSIP-like token in the existing data files (this script's own files excluded)."""
    found: set[str] = set()
    for path in sorted(DATA.iterdir()):
        if path.name.startswith("course2_") or path.suffix not in (".csv", ".md", ".txt"):
            continue
        found.update(re.findall(r"\b99[0-9A-Z]{7}\b", path.read_text(encoding="utf-8-sig")))
    return found


def build_clean(rng: np.random.Generator) -> tuple[pd.DataFrame, list[str]]:
    september = pd.read_csv(DATA / "holdings.csv")
    benchmark = pd.read_csv(DATA / "benchmark.csv")
    issuers = pd.read_csv(DATA / "issuers.csv")
    ratings = pd.read_csv(DATA / "ratings.csv")

    # the five widest bonds stay in the book: real outliers, not errors
    widest = september.nlargest(5, "oas").index
    sold = rng.choice(september.index.difference(widest), size=SOLD, replace=False)
    kept = september.drop(index=sold).copy()

    # resized positions: one to four lots of 250,000 of face, never to zero
    for i in rng.choice(kept.index, size=RESIZED, replace=False):
        change = int(rng.integers(1, 5)) * 250_000 * (1 if rng.random() < 0.5 else -1)
        if kept.loc[i, "par_held"] + change <= 0:
            change = -change
        kept.loc[i, "par_held"] += change

    not_held = benchmark[~benchmark["cusip"].isin(september["cusip"]) & ~benchmark["cusip"].isin(BENCHMARK_EXCEPTIONS)]
    bought = not_held.sample(n=BOUGHT, random_state=int(rng.integers(1_000_000)))[
        [c for c in COLUMNS if c not in ("par_held", "market_value")]].copy()
    bought["par_held"] = rng.integers(1, 21, size=BOUGHT) * 250_000

    book = pd.concat([kept, bought], ignore_index=True)
    # two months of spread moves for the bonds carried over or bought
    book["oas"] = np.maximum(5, (book["oas"] * rng.lognormal(0, 0.07, size=len(book))).round()).astype(int)
    new = new_bond_rows(benchmark, issuers)
    book = pd.concat([book, new], ignore_index=True).sort_values(["ticker", "maturity"]).reset_index(drop=True)

    maturities = [date.fromisoformat(m) for m in book["maturity"]]
    years = [days_30_360(AS_OF, m) / 360 for m in maturities]
    book["yield_pct"] = [round3(curve_yield_pct(t) + oas / 100) for t, oas in zip(years, book["oas"])]
    book["price"] = [round3(price(AS_OF, m, c, y)) for m, c, y in zip(maturities, book["coupon"], book["yield_pct"])]
    book["accrued"] = [round3(accrued_interest(AS_OF, m, c)) for m, c in zip(maturities, book["coupon"])]
    book["duration"] = [round3(modified_duration(AS_OF, m, c, y))
                        for m, c, y in zip(maturities, book["coupon"], book["yield_pct"])]
    book["spread_duration"] = book["duration"]
    book["dts"] = (book["spread_duration"] * book["oas"]).round(1)
    book["market_value"] = (book["par_held"] * (book["price"] + book["accrued"]) / 100).round(2)
    book["as_of_date"] = AS_OF.isoformat()
    book["price_date"] = AS_OF.isoformat()
    book["oas"] = book["oas"].astype(int)
    book["amount_outstanding"] = book["amount_outstanding"].astype("int64")
    book["par_held"] = book["par_held"].astype("int64")

    if book["cusip"].duplicated().any():
        raise ValueError("a CUSIP appears twice in the clean book")
    if not set(book["ticker"]) <= set(issuers["ticker"]) or not set(book["rating"]) <= set(ratings["rating"]):
        raise ValueError("a ticker or a rating of the book does not join to its reference table")
    if (book["par_held"] > book["amount_outstanding"]).any():
        raise ValueError("a position is larger than the bond's amount outstanding")
    final_period = [len(coupon_dates(AS_OF, m)) == 2 for m in maturities]
    if sum(final_period) != 1 or sum(month_end(m) for m in maturities) != 1:
        raise ValueError("the book must hold exactly one final-period bond and one month-end maturity")
    return book[COLUMNS], list(new["cusip"])


def control_totals(clean: pd.DataFrame) -> dict:
    return dict(bonds=len(clean), face=int(clean["par_held"].sum()), market_value=round(float(clean["market_value"].sum()), 2))


# ---- the raw extract
def build_messy(clean: pd.DataFrame, new_cusips: list[str], rng: np.random.Generator) -> tuple[pd.DataFrame, dict]:
    """Plant the problems. Returns the extract and a record of what was changed, keyed by problem."""
    messy = clean.copy()
    messy["order"] = np.arange(len(messy), dtype=float)
    maturities = {i: date.fromisoformat(clean.loc[i, "maturity"]) for i in clean.index}

    # planted rows never overlap and never touch the five widest bonds or the two new bonds
    protected = clean.nlargest(5, "oas").index.union(clean.index[clean["cusip"].isin(new_cusips)])
    free = list(clean.index.difference(protected))

    def take(candidates: list, n: int) -> list:
        chosen = sorted(int(i) for i in rng.choice(np.array(candidates), size=n, replace=False))
        for i in chosen:
            free.remove(i)
        return chosen

    # the wrong maturity is ten years early, so pick a bond for which that lands before the as-of date
    maturity_rows = take([i for i in free if clean.loc[i, "maturity"] < "2036-11-30"], N_MATURITY)

    def act360(i) -> float:
        previous_coupon = coupon_dates(AS_OF, maturities[i])[0]
        return round3(clean.loc[i, "coupon"] * (AS_OF - previous_coupon).days / 360)

    # the actual/360 accrued must differ visibly from the 30/360 figure
    accrued_rows = take([i for i in free if abs(act360(i) - clean.loc[i, "accrued"]) >= 0.001], N_ACCRUED_ACT360)

    def recovered_yield(i) -> float:
        return round3(yield_to_maturity(AS_OF, maturities[i], clean.loc[i, "coupon"], clean.loc[i, "price"]))

    # a blank yield must come back exactly when solved from the 3-decimal price and rounded
    blank_yield_rows = take([i for i in free if recovered_yield(i) == clean.loc[i, "yield_pct"]], N_BLANK_YIELD)
    dirty_rows = take(free, N_DIRTY_PRICE)
    yield_rows = take(free, N_YIELD_DECIMAL)
    coupon_rows = take(free, N_COUPON_DECIMAL)
    blank_price_rows = take(free, N_BLANK_PRICE)
    macaulay_rows = take(free, N_MACAULAY)
    duplicate_rows = take(free, N_DUPLICATES)

    planted: dict = {name: [] for name in PROBLEMS}

    def plant(name: str, i: int, column: str, written) -> None:
        clean_value = clean.loc[i, column]
        messy.loc[i, column] = written
        planted[name].append(dict(cusip=clean.loc[i, "cusip"], ticker=clean.loc[i, "ticker"],
                                  written="blank" if pd.isna(written) else written, clean=clean_value))

    for i in dirty_rows:
        plant("dirty_price", i, "price", round3(clean.loc[i, "price"] + clean.loc[i, "accrued"]))
    for i in yield_rows:
        plant("yield_decimal", i, "yield_pct", round(clean.loc[i, "yield_pct"] / 100, 5))
    for i in coupon_rows:
        plant("coupon_decimal", i, "coupon", round(clean.loc[i, "coupon"] / 100, 5))
    for i in blank_price_rows:
        plant("blank_price", i, "price", np.nan)
    for i in blank_yield_rows:
        plant("blank_yield", i, "yield_pct", np.nan)
    for i in macaulay_rows:
        m = maturities[i]
        plant("macaulay", i, "duration", round3(macaulay_duration(AS_OF, m, clean.loc[i, "coupon"], clean.loc[i, "yield_pct"])))
    for i in accrued_rows:
        plant("accrued_act360", i, "accrued", act360(i))
    for i in maturity_rows:
        written = f"{int(clean.loc[i, 'maturity'][:4]) - 10}{clean.loc[i, 'maturity'][4:]}"
        plant("maturity", i, "maturity", written)

    # each copy sits directly below the row it repeats
    copies = messy.loc[duplicate_rows]
    planted["duplicates"] = [dict(cusip=clean.loc[i, "cusip"], ticker=clean.loc[i, "ticker"]) for i in duplicate_rows]
    messy = pd.concat([messy, copies]).sort_values("order", kind="stable").drop(columns="order").reset_index(drop=True)
    return messy, planted


def answer_key(clean: pd.DataFrame, messy: pd.DataFrame, planted: dict, new_cusips: list[str]) -> str:
    totals = control_totals(clean)

    def listing(name: str, with_values: bool = True) -> str:
        lines = []
        for item in planted[name]:
            line = f"- `{item['cusip']}` ({item['ticker']})"
            if with_values:
                line += f": in the file `{item['written']}`, clean value `{item['clean']}`"
            lines.append(line)
        return "\n".join(lines)

    def count(name: str) -> str:
        n = len(planted[name])
        return f"{n} row" if n == 1 else f"{n} rows"

    widest = clean.nlargest(5, "oas")
    new = clean[clean["cusip"].isin(new_cusips)].set_index("cusip")
    notes = {cusip: spec["note"] for cusip, spec in zip(new_cusips, NEW_BONDS)}
    new_lines = "\n".join(
        f"- `{cusip}` ({b.ticker}, {b.issuer}), {b.coupon} percent maturing {b.maturity}, {notes[cusip]}."
        for cusip, b in new.iterrows())
    final_cusip, month_end_cusip = new_cusips
    mismatched = len(planted["dirty_price"]) + len(planted["accrued_act360"])
    received_face = int(messy["par_held"].sum())
    received_value = round(float(messy["market_value"].sum()), 2)
    return f"""# Answer key: course2_capstone_holdings.csv

`course2_capstone_holdings.csv` is the desk's book as of {AS_OF}, with these bond-math problems planted on purpose. Generated by `tools/make_course2_data.py` with seed {SEED}. The clean book has {totals['bonds']} bonds and the file has {len(messy)} rows. No row carries two problems. Settlement is the as-of date for every bond; the conventions are semiannual US 30/360 as in `COURSE2_SPEC.md`. In every row with a planted problem, every other column holds its clean value, and `market_value` is the clean value in every row.

## Dirty price in the price column ({count('dirty_price')})
`price` holds the clean price plus `accrued`. Fix: subtract `accrued`, rounded to 3 decimals (the same as repricing from `yield_pct` with `price` and rounding).
{listing('dirty_price')}

## Yield entered as a decimal ({count('yield_decimal')})
`yield_pct` is a hundredth of the clean value (0.05 for 5 percent). Fix: multiply by 100, rounded to 3 decimals.
{listing('yield_decimal')}

## Coupon entered as a decimal ({count('coupon_decimal')})
`coupon` is a hundredth of the clean value. Price, accrued, and the analytics in these rows were computed from the correct coupon. Fix: multiply by 100, rounded to 3 decimals.
{listing('coupon_decimal')}

## Blank price, recoverable from the yield ({count('blank_price')})
The `price` cell is blank. Fix: `price(settlement, maturity, coupon, yield_pct)`, rounded to 3 decimals.
{listing('blank_price')}

## Blank yield, recoverable from the price ({count('blank_yield')})
The `yield_pct` cell is blank. Fix: `yield_to_maturity(settlement, maturity, coupon, price)` from the 3-decimal price, rounded to 3 decimals, gives the clean value back.
{listing('blank_yield')}

## Duration entered as Macaulay instead of modified ({count('macaulay')})
`duration` holds Macaulay duration, rounded to 3 decimals. `spread_duration` and `dts` in these rows are correct, so these are the only rows where `duration` differs from `spread_duration`. Fix: `modified_duration` from the yield, rounded to 3 decimals.
{listing('macaulay')}

## Accrued computed on actual days over 360 ({count('accrued_act360')})
`accrued` is coupon x actual days since the previous coupon / 360, not the 30/360 figure. Fix: `accrued_interest` on 30/360, rounded to 3 decimals.
{listing('accrued_act360')}

## Maturity before settlement ({count('maturity')})
The year of the maturity is ten years early, so the maturity falls before the as-of date and `coupon_dates` raises `ValueError`. Fix: the maturity of the same CUSIP in `benchmark.csv`.
{listing('maturity')}

## Exact duplicate rows ({count('duplicates')})
Each of these CUSIPs appears twice, the second row an exact copy directly below the first. Fix: remove the copies.
{listing('duplicates', with_values=False)}

## Market value that does not tie out ({mismatched} rows)
Not a separate problem. In the {len(planted['dirty_price'])} dirty-price rows and the {len(planted['accrued_act360'])} actual/360 accrued rows, `market_value` does not equal `par_held` x (`price` + `accrued`) / 100. In the {len(planted['blank_price'])} blank-price rows it cannot be checked until the price is filled. It ties out in every row once the fixes are made.

## Clean on purpose
These two bonds are new this month. They are correct, and a reprice that follows Excel's conventions reproduces them. Neither is in `holdings.csv` or `benchmark.csv`.
{new_lines}

`{final_cusip}` has one coupon left, so `PRICE` uses simple interest and `YIELD` its closed form. `{month_end_cusip}` matures on a month end, so every coupon falls on a month end (previous coupon {coupon_dates(AS_OF, date.fromisoformat(new.loc[month_end_cusip, 'maturity']))[0]}, next {coupon_dates(AS_OF, date.fromisoformat(new.loc[month_end_cusip, 'maturity']))[1]}). Coupon dates stepped from the previous date instead of from maturity drift to the 28th after February and give the wrong accrued.

The five widest spreads in the clean book are real features of the data, not errors:
""" + "\n".join(f"- `{b.cusip}` ({b.ticker}), {b.rating}, OAS {b.oas} bp" for b in widest.itertuples()) + f"""

## Checks that find nothing
Tickers, issuers, sectors, ratings, CUSIP lengths and check digits, `oas`, `spread_duration`, `dts`, `par_held`, `amount_outstanding`, and price dates are clean. Every ticker is in `issuers.csv` and every rating in `ratings.csv`.

## Control totals of the clean book
- Bonds: {totals['bonds']:,}
- Total face: {totals['face']:,} dollars
- Total market value: {totals['market_value']:,.2f} dollars

As received, the file shows {len(messy):,} rows, {received_face:,} dollars of face, and {received_value:,.2f} dollars of market value; the difference is the duplicate rows.

## What changed from September
Of the 200 bonds in `holdings.csv`, {SOLD} were sold out, {RESIZED} changed size, {BOUGHT} benchmark bonds not held in September were bought, and {len(NEW_BONDS)} new invented bonds were added.
"""


def cover_note(clean: pd.DataFrame) -> str:
    totals = control_totals(clean)
    return f"""To: Credit desk
From: Operations
Subject: Month-end holdings extract, as of {AS_OF}

The month-end extract is attached as course2_capstone_holdings.csv. It is the same layout as last month.

Control totals for the book:
  Number of bonds:      {totals['bonds']:,}
  Total face:           {totals['face']:,} dollars
  Total market value:   {totals['market_value']:,.2f} dollars

Market value is face times clean price plus accrued interest, divided by 100.
All positions settle and are priced as of {AS_OF}. Analytics are semiannual, 30/360.
Please tell us if the extract does not agree with these totals.
"""


def build() -> tuple[pd.DataFrame, pd.DataFrame, dict, list[str]]:
    rng = np.random.default_rng(SEED)
    clean, new_cusips = build_clean(rng)
    messy, planted = build_messy(clean, new_cusips, rng)
    return clean, messy, planted, new_cusips


def write_files(folder: Path) -> None:
    build_curve().to_csv(folder / "course2_treasury_curve.csv", index=False, lineterminator="\n")
    clean, messy, planted, new_cusips = build()
    messy.to_csv(folder / "course2_capstone_holdings.csv", index=False, lineterminator="\n")
    (folder / "course2_capstone_answer_key.md").write_text(answer_key(clean, messy, planted, new_cusips),
                                                           encoding="utf-8", newline="\n")
    (folder / "course2_capstone_cover_note.txt").write_text(cover_note(clean), encoding="utf-8", newline="\n")
    print(f"curve {len(CURVE_TENORS)} tenors; capstone holdings {len(messy)} rows, clean book {len(clean)} bonds")


if __name__ == "__main__":
    write_files(DATA)
