"""Generate the data for Course 3 (Market Data and Time Series).

The script reads treasury_par_yields.csv, holdings.csv, and ratings.csv and writes six new files:

- course3_synthetic_spreads.csv        SYNTHETIC daily investment grade and high yield spreads in bp, one row
                                        per date of the Treasury file (invented, not ICE, Moody's, or any index)
- course3_fred_format_dgs10.json       Treasury 10 Yr values from the Treasury file, laid out in the FRED API's
- course3_fred_format_dgs2.json        series/observations response format (nothing is downloaded from FRED)
- course3_capstone_extract.csv         a vendor extract for 2026-07-01 to 2026-10-02 with problems planted
- course3_capstone_answer_key.md       every planted row, the value in the file, the clean value, and the fix
- course3_capstone_cover_note.txt      the vendor's cover note: the period, the market days, the last values

It writes nothing else and changes no existing file. The same seeds always produce the same files.

The synthetic spreads: each series' log spread follows a mean-reverting daily process whose volatility
switches between a calm and a stressed state with fixed probabilities. The high yield shock is a multiple
of the investment grade shock plus its own noise. The paths start on 2015-01-02 and are then shifted in log
terms so that on 2026-09-30 each equals the market-value weighted oas of that grade's bonds in holdings.csv.
They depend on the Treasury file only through its dates, and no date is chosen to resemble market history.

Usage (from the repo root):  python tools/make_course3_data.py
"""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
SPREAD_SEED = 20261002
CAPSTONE_SEED = 20261005
PIN_DATE = "2026-09-30"

# the synthetic spread model: daily steps in log spread
MODEL = {
    "ig": dict(long_run_bp=120.0, reversion=0.004, calm_vol=0.010, stressed_vol=0.030),
    "hy": dict(long_run_bp=400.0, reversion=0.004, calm_vol=0.008, stressed_vol=0.020),
}
HY_BETA = 1.3  # high yield shock = HY_BETA x investment grade shock + its own noise
CALM_TO_STRESSED, STRESSED_TO_CALM = 0.004, 0.03  # daily switching probabilities
STALE_LIMIT = 5  # the clean synthetic file has no run of this many identical values

# the FRED-format samples
FRED_START, FRED_END, FRED_REALTIME = "2026-08-03", "2026-09-30", "2026-10-02"
FRED_SAMPLES = {"DGS10": "10 Yr", "DGS2": "2 Yr"}

# the capstone extract
EXTRACT_START, EXTRACT_END = "2026-07-01", "2026-10-02"
YIELD_COLUMNS = ["2 Yr", "5 Yr", "10 Yr", "30 Yr"]
SPREAD_COLUMNS = ["ig_spread_bp", "hy_spread_bp"]
EXTRACT_COLUMNS = ["date"] + YIELD_COLUMNS + SPREAD_COLUMNS
HOLIDAY = "2026-09-07"
N_MMDDYYYY, N_SPREAD_PERCENT, N_YIELD_BP, N_DUPLICATES = 3, 2, 2, 2
N_WEEKEND, N_MISSING, STALE_RUN_LENGTH = 1, 1, 5
STALE_COLUMN = "hy_spread_bp"


# ---- inputs
def read_treasury_text() -> pd.DataFrame:
    """The Treasury file with every value kept as the text Treasury published (4.20 stays 4.20)."""
    return pd.read_csv(DATA / "treasury_par_yields.csv", dtype=str, keep_default_na=False)


def weighted_oas_by_grade() -> dict[str, float]:
    """Market-value weighted oas of each grade in holdings.csv, in bp, summed as bondmath.weighted_average does."""
    holdings = pd.read_csv(DATA / "holdings.csv")
    grades = pd.read_csv(DATA / "ratings.csv").set_index("rating")["grade"]
    holdings["grade"] = holdings["rating"].map(grades)
    if holdings["grade"].isna().any():
        raise ValueError("a rating in holdings.csv is not in ratings.csv")
    result = {}
    for grade, key in (("Investment Grade", "ig"), ("High Yield", "hy")):
        rows = holdings[holdings["grade"] == grade]
        total = 0.0
        for oas, value in zip(rows["oas"], rows["market_value"]):
            total += float(oas) * float(value)
        result[key] = total / float(rows["market_value"].sum())
    return result


def longest_run(values: list) -> int:
    """Length of the longest run of identical consecutive values."""
    longest = current = 1
    for previous, value in zip(values, values[1:]):
        current = current + 1 if value == previous else 1
        longest = max(longest, current)
    return longest


# ---- synthetic spreads
def build_spreads() -> pd.DataFrame:
    dates = read_treasury_text()["date"].tolist()
    rng = np.random.default_rng(SPREAD_SEED)
    n = len(dates)
    stressed = np.zeros(n, dtype=bool)
    for t in range(1, n):
        switch = rng.random()
        if stressed[t - 1]:
            stressed[t] = switch >= STRESSED_TO_CALM
        else:
            stressed[t] = switch < CALM_TO_STRESSED
    ig_noise, hy_noise = rng.standard_normal(n), rng.standard_normal(n)

    log_spread = {key: np.zeros(n) for key in MODEL}
    for key, spec in MODEL.items():
        log_spread[key][0] = math.log(spec["long_run_bp"])
    for t in range(1, n):
        vol = "stressed_vol" if stressed[t] else "calm_vol"
        ig_shock = MODEL["ig"][vol] * ig_noise[t]
        shocks = {"ig": ig_shock, "hy": HY_BETA * ig_shock + MODEL["hy"][vol] * hy_noise[t]}
        for key, spec in MODEL.items():
            previous = log_spread[key][t - 1]
            log_spread[key][t] = previous + spec["reversion"] * (math.log(spec["long_run_bp"]) - previous) + shocks[key]

    # shift each path in log terms so it equals the book's weighted oas on the pin date
    targets = weighted_oas_by_grade()
    pin = dates.index(PIN_DATE)
    frame = pd.DataFrame({"date": dates})
    for key in MODEL:
        level = targets[key] * np.exp(log_spread[key] - log_spread[key][pin])
        frame[f"{key}_spread_bp"] = [round(float(x), 1) for x in level]

    if not (frame["hy_spread_bp"] > frame["ig_spread_bp"]).all() or not (frame["ig_spread_bp"] > 0).all():
        raise ValueError("the synthetic spreads must be positive with high yield above investment grade")
    for column in SPREAD_COLUMNS:
        if longest_run(frame[column].tolist()) >= STALE_LIMIT:
            raise ValueError(f"{column} has a run of {STALE_LIMIT} or more identical values")
    for key in MODEL:
        if frame.loc[pin, f"{key}_spread_bp"] != round(targets[key], 1):
            raise ValueError(f"{key} spread on {PIN_DATE} does not equal the book's weighted oas")
    return frame


def spreads_csv(frame: pd.DataFrame) -> str:
    lines = ["date,ig_spread_bp,hy_spread_bp"]
    lines += [f"{d},{ig:.1f},{hy:.1f}" for d, ig, hy in zip(frame["date"], frame["ig_spread_bp"], frame["hy_spread_bp"])]
    return "\n".join(lines) + "\n"


# ---- FRED-format samples
def fred_sample(column: str) -> dict:
    """Treasury values in the layout of FRED's series/observations JSON: weekdays only, "." where Treasury has no row."""
    treasury = read_treasury_text().set_index("date")[column]
    weekdays = pd.bdate_range(FRED_START, FRED_END).strftime("%Y-%m-%d")
    observations = []
    for day in weekdays:
        value = treasury.get(day, ".")
        observations.append(dict(realtime_start=FRED_REALTIME, realtime_end=FRED_REALTIME, date=day, value=value))
    missing = [o["date"] for o in observations if o["value"] == "."]
    if missing != [HOLIDAY]:
        raise ValueError(f"expected one '.' row on {HOLIDAY}, found {missing}")
    return dict(realtime_start=FRED_REALTIME, realtime_end=FRED_REALTIME, observation_start=FRED_START,
                observation_end=FRED_END, units="lin", output_type=1, file_type="json", order_by="observation_date",
                sort_order="asc", count=len(observations), offset=0, limit=100000, observations=observations)


# ---- the capstone extract
def clean_extract_rows() -> list[dict]:
    """One row per market day of the extract period: Treasury text values and the synthetic spreads, as text."""
    treasury = read_treasury_text()
    spreads = build_spreads()
    merged = treasury.merge(spreads, on="date", validate="one_to_one")
    period = merged[(merged["date"] >= EXTRACT_START) & (merged["date"] <= EXTRACT_END)]
    rows = []
    for _, r in period.iterrows():
        row = {"date": r["date"]} | {c: r[c] for c in YIELD_COLUMNS}
        row |= {c: f"{r[c]:.1f}" for c in SPREAD_COLUMNS}
        rows.append(row)
    return rows


def mmddyyyy(iso: str) -> str:
    return f"{iso[5:7]}/{iso[8:10]}/{iso[:4]}"


def build_capstone() -> tuple[list[dict], list[dict], dict]:
    """Returns the clean rows, the extract rows, and a record of every planted problem."""
    clean = clean_extract_rows()
    rng = np.random.default_rng(CAPSTONE_SEED)
    n = len(clean)
    # the first two and last two market days are never planted, so the period's ends are clean
    free = list(range(2, n - 2))
    planted: dict = {name: [] for name in ("holiday", "weekend", "missing", "duplicates", "mmddyyyy",
                                           "spread_percent", "yield_bp", "stale_run")}

    def take(candidates: list[int]) -> int:
        chosen = int(rng.choice(np.array(candidates)))
        free.remove(chosen)
        return chosen

    # the stale run first: five consecutive free market days whose true values all differ from the first day's
    starts = [i for i in free if all(j in free for j in range(i, i + STALE_RUN_LENGTH))
              and all(clean[j][STALE_COLUMN] != clean[i][STALE_COLUMN] for j in range(i + 1, i + STALE_RUN_LENGTH))]
    stale_start = int(rng.choice(np.array(starts)))
    stale_rows = list(range(stale_start, stale_start + STALE_RUN_LENGTH))
    for i in stale_rows:
        free.remove(i)
    # the weekend row repeats a Friday's values on the Saturday after it; that Friday is not planted otherwise
    fridays = [i for i in free if pd.Timestamp(clean[i]["date"]).dayofweek == 4]
    weekend_friday = take(fridays)
    missing_row = take(free)
    mmdd_rows = sorted(take(free) for _ in range(N_MMDDYYYY))
    percent_rows = sorted(take(free) for _ in range(N_SPREAD_PERCENT))
    bp_rows = sorted(take(free) for _ in range(N_YIELD_BP))
    duplicate_rows = sorted(take(free) for _ in range(N_DUPLICATES))

    extract = [dict(row) for row in clean]
    for i in mmdd_rows:
        extract[i]["date"] = mmddyyyy(clean[i]["date"])
        planted["mmddyyyy"].append(dict(date=clean[i]["date"], column="date", written=extract[i]["date"],
                                        clean=clean[i]["date"]))
    for i in percent_rows:
        column = str(rng.choice(SPREAD_COLUMNS))
        extract[i][column] = f"{float(clean[i][column]) / 100:.3f}"
        planted["spread_percent"].append(dict(date=clean[i]["date"], column=column, written=extract[i][column],
                                              clean=clean[i][column]))
    for i in bp_rows:
        column = str(rng.choice(YIELD_COLUMNS))
        extract[i][column] = str(round(float(clean[i][column]) * 100))
        planted["yield_bp"].append(dict(date=clean[i]["date"], column=column, written=extract[i][column],
                                        clean=clean[i][column]))
    stale_value = clean[stale_start][STALE_COLUMN]
    for i in stale_rows[1:]:
        extract[i][STALE_COLUMN] = stale_value
        planted["stale_run"].append(dict(date=clean[i]["date"], column=STALE_COLUMN, written=stale_value,
                                         clean=clean[i][STALE_COLUMN]))
    planted["stale_run_first_date"] = clean[stale_start]["date"]
    planted["missing"].append(dict(date=clean[missing_row]["date"], column="all", written="no row",
                                   clean=", ".join(clean[missing_row][c] for c in EXTRACT_COLUMNS[1:])))
    for i in duplicate_rows:
        planted["duplicates"].append(dict(date=clean[i]["date"], column="all", written="the row twice",
                                          clean="one row"))

    # assemble in date order: each copy directly below its row, the weekend and holiday rows in their places
    friday = clean[weekend_friday]["date"]
    saturday = (pd.Timestamp(friday) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    planted["weekend"].append(dict(date=saturday, column="all", written=f"the values of {friday}", clean="no row"))
    planted["holiday"].append(dict(date=HOLIDAY, column="all", written=". in every value column", clean="no row"))
    weekend_row = dict(extract[weekend_friday]) | {"date": saturday}
    holiday_row = {"date": HOLIDAY} | {c: "." for c in EXTRACT_COLUMNS[1:]}
    # (true date, row) pairs, so the MM/DD/YYYY rows sort by the date they stand for
    dated = []
    for i, row in enumerate(extract):
        if i == missing_row:
            continue
        dated.append((clean[i]["date"], row))
        if i in duplicate_rows:
            dated.append((clean[i]["date"], dict(row)))
    dated += [(saturday, weekend_row), (HOLIDAY, holiday_row)]
    # a stable sort keeps each copy directly below its row
    dated.sort(key=lambda pair: pair[0])
    return clean, [row for _, row in dated], planted


def extract_csv(rows: list[dict]) -> str:
    lines = [",".join(EXTRACT_COLUMNS)] + [",".join(row[c] for c in EXTRACT_COLUMNS) for row in rows]
    return "\n".join(lines) + "\n"


def answer_key(clean: list[dict], extract: list[dict], planted: dict) -> str:
    def listing(name: str) -> str:
        lines = []
        for item in planted[name]:
            if item["column"] == "all":
                lines.append(f"- `{item['date']}`: in the file {item['written']}; clean: {item['clean']}")
            else:
                lines.append(f"- `{item['date']}`, `{item['column']}`: in the file `{item['written']}`, "
                             f"clean value `{item['clean']}`")
        return "\n".join(lines)

    def count(name: str) -> str:
        k = len(planted[name])
        return f"{k} row" if k == 1 else f"{k} rows"

    stale_first = planted["stale_run_first_date"]
    stale_value = planted["stale_run"][0]["written"]
    last = clean[-1]
    return f"""# Answer key: course3_capstone_extract.csv

`course3_capstone_extract.csv` is a vendor extract for {EXTRACT_START} to {EXTRACT_END} with these problems planted on purpose. Generated by `tools/make_course3_data.py` with seed {CAPSTONE_SEED}. The clean extract has {len(clean)} rows, one per market day (the dates of `treasury_par_yields.csv` in the period); the file has {len(extract)} rows. No row carries two problems, and the first two and last two market days are clean. In every row with a planted problem, every other value is clean.

Clean values: the four yield columns equal `treasury_par_yields.csv` (percent, as Treasury published them) and the two spread columns equal `course3_synthetic_spreads.csv` (bp, synthetic) on every market day. Yields are in percent and spreads in bp.

## A holiday row with `.` in every value ({count('holiday')})
{HOLIDAY} has no row in the Treasury file: the market had no curve that day. The vendor sent the date with `.` in every value column, as FRED marks a weekday with no value. Fix: read `.` as missing and drop the row. Never turn `.` into 0.
{listing('holiday')}

## A weekend-dated row ({count('weekend')})
A Saturday carrying the values of the Friday before it. Fix: drop the row; a weekend is never a market day.
{listing('weekend')}

## A missing market day ({count('missing')})
A date with a row in the Treasury file is absent from the extract. Fix: report it. The row is restored from the clean source (the Treasury file and the synthetic spreads file); it is never forward filled, which would invent a zero change.
{listing('missing')}

## Exact duplicate rows ({count('duplicates')})
Each of these dates appears twice, the second row an exact copy directly below the first. Fix: remove the copies.
{listing('duplicates')}

## Dates written MM/DD/YYYY ({count('mmddyyyy')})
Every other date is ISO `YYYY-MM-DD`. Fix: parse these with the format `%m/%d/%Y`. Parsing the whole column with one format fails on them, which is how they are found.
{listing('mmddyyyy')}

## A spread in percent instead of bp ({count('spread_percent')})
The value is a hundredth of the clean figure, so it sits far below every other spread. Fix: multiply by 100 and round to 1 decimal.
{listing('spread_percent')}

## A yield in bp instead of percent ({count('yield_bp')})
The value is 100 times the clean figure (a whole number of basis points). Fix: divide by 100 and round to 2 decimals.
{listing('yield_bp')}

## A stale run ({count('stale_run')}, a run of {STALE_RUN_LENGTH} market days)
`{STALE_COLUMN}` holds `{stale_value}` on {STALE_RUN_LENGTH} consecutive market days from `{stale_first}`. The first day's value is correct; the next {STALE_RUN_LENGTH - 1} repeat it. The clean synthetic file has no run of {STALE_LIMIT} or more identical values in either spread. Fix: report the run. The true values are recoverable here only because the clean source exists; with a real vendor the values would be requested again, not guessed.
{listing('stale_run')}

## Checks that find nothing
The other dates are market days in ascending order, the column names and their order are as the cover note says, and every other value is in its stated units.

## Control figures
- Market days in the period: {len(clean)}
- Rows in the file as received: {len(extract)} ({len(clean)} - {len(planted['missing'])} missing + {len(planted['holiday'])} holiday + {len(planted['weekend'])} weekend + {len(planted['duplicates'])} duplicates)
- Last values, {last['date']}: 2 Yr {last['2 Yr']}, 5 Yr {last['5 Yr']}, 10 Yr {last['10 Yr']}, 30 Yr {last['30 Yr']} percent; investment grade {last['ig_spread_bp']} bp, high yield {last['hy_spread_bp']} bp (synthetic)
"""


def cover_note(clean: list[dict]) -> str:
    last = clean[-1]
    return f"""To: Credit desk
From: Market data vendor, client operations
Subject: Daily extract, {EXTRACT_START} to {EXTRACT_END}

The extract is attached as course3_capstone_extract.csv, in the usual layout.

Period:        {EXTRACT_START} to {EXTRACT_END}
Market days:   {len(clean)}
Columns:       date, 2 Yr, 5 Yr, 10 Yr, 30 Yr (par yields, percent), ig_spread_bp, hy_spread_bp (basis points)

Last values sent, for {last['date']}:
  2 Yr     {last['2 Yr']} percent
  5 Yr     {last['5 Yr']} percent
  10 Yr    {last['10 Yr']} percent
  30 Yr    {last['30 Yr']} percent
  ig_spread_bp   {last['ig_spread_bp']}
  hy_spread_bp   {last['hy_spread_bp']}

The spread columns are synthetic course data, invented for this course. They are not ICE, Moody's, or any index.
Please tell us if the extract does not agree with these figures.
"""


def write_files(folder: Path) -> None:
    spreads = build_spreads()
    (folder / "course3_synthetic_spreads.csv").write_text(spreads_csv(spreads), encoding="utf-8", newline="\n")
    for series_id, column in FRED_SAMPLES.items():
        text = json.dumps(fred_sample(column), indent=2) + "\n"
        (folder / f"course3_fred_format_{series_id.lower()}.json").write_text(text, encoding="utf-8", newline="\n")
    clean, extract, planted = build_capstone()
    (folder / "course3_capstone_extract.csv").write_text(extract_csv(extract), encoding="utf-8", newline="\n")
    (folder / "course3_capstone_answer_key.md").write_text(answer_key(clean, extract, planted), encoding="utf-8",
                                                           newline="\n")
    (folder / "course3_capstone_cover_note.txt").write_text(cover_note(clean), encoding="utf-8", newline="\n")
    print(f"synthetic spreads {len(spreads)} rows; FRED samples {fred_sample('10 Yr')['count']} rows each; "
          f"capstone extract {len(extract)} rows for {len(clean)} market days")


if __name__ == "__main__":
    write_files(DATA)
