"""Generate the synthetic firm cohort used in Course 5C (Risk Models).

Everything here is invented: the firms, their ratings, their balance sheets, and every default.
No row describes a real company, and no default rate here is an agency statistic. Firms carry
ids only (F0001 and up), never names. Years are study years 1 to 20, not calendar years, so no
reader maps a default wave onto real history. The same seed always produces the same file.
This script reads ratings.csv and writes course5c_cohort.csv. It writes nothing else.

The model (every constant is stated in DATA.md, so the course can show models recovering it):
- A firm enters in a study year from 1 to 16 and is followed to default, exit, or year 20.
- One row per firm and year it is at risk. Covariates are dated at the start of the year:
  rating and rating_score (ratings.csv's scale, 1 = AAA to 18 = CCC), leverage (debt to EBITDA,
  times), coverage (EBITDA to interest, times).
- The chance of default in a year is a logistic function of those covariates, plus a bump for
  years 2 to 4 since entry and a common factor drawn once per study year, shared by every firm.
  The common factor makes defaults cluster by year.
- A firm that does not default leaves with a fixed chance each year for a reason unrelated to
  default (refinanced or called): exit = 1 in that year. A firm alive in year 20 is censored.
- From study year 11 the entering population shifts: lower ratings and higher leverage.
- Leverage, coverage, and rating move a little from year to year.

Usage (from the repo root):  python tools/make_cohort.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261022
DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "course5c_cohort.csv"

N_FIRMS = 4_000
FIRST_ENTRY, LAST_ENTRY, LAST_YEAR = 1, 16, 20
SECTORS = ["Consumer", "Energy", "Financials", "Health Care", "Industrials", "Materials",
           "Technology", "Telecom", "Transportation", "Utilities"]  # the sector list of issuers.csv

# entry rating weights by rating_score 1 (AAA) to 18 (CCC), before the shift
ENTRY_WEIGHT = np.array([1, 1, 2, 3, 4, 5, 6, 8, 9, 9, 9, 9, 8, 7, 6, 5, 3, 2], dtype=float)
SHIFT_START = 11          # first entry year of the shifted population
SHIFT_TILT = 0.04         # per year after SHIFT_START - 1: weight multiplied by exp(tilt * years * (score - 9))
SHIFT_LEVERAGE = 0.10     # times of leverage added per year after SHIFT_START - 1, at entry

# leverage at entry: LEV_BASE + LEV_SLOPE * rating_score + normal noise, floored at LEV_FLOOR
LEV_BASE, LEV_SLOPE, LEV_NOISE, LEV_FLOOR = 1.0, 0.30, 0.8, 0.3
LEV_STEP = 0.35           # standard deviation of the yearly change in leverage
# coverage: exp(COV_BASE - COV_LEV * leverage + normal noise), floored at COV_FLOOR
COV_BASE, COV_LEV, COV_NOISE, COV_FLOOR = 3.0, 0.30, 0.50, 0.2
DOWNGRADE, UPGRADE = 0.08, 0.06   # yearly chance of a one-notch move

# the planted annual default model: logit(p) = INTERCEPT + B_SCORE * rating_score
#   + B_LEV * leverage + B_LOG_COV * ln(coverage) + AGE_BUMP (years 2 to 4) + year factor
INTERCEPT = -9.6
B_SCORE = 0.38
B_LEV = 0.25
B_LOG_COV = -0.40
AGE_BUMP = 0.30
YEAR_FACTOR_SD = 0.45
EXIT_CHANCE = 0.07

COLUMNS = ["firm_id", "study_year", "years_since_entry", "sector", "rating", "rating_score",
           "leverage", "coverage", "default", "exit"]


def default_chance(score: int, leverage: float, coverage: float, years_since_entry: int,
                   year_factor: float) -> float:
    """The planted chance of default within one year, from start-of-year covariates."""
    logit = (INTERCEPT + B_SCORE * score + B_LEV * leverage + B_LOG_COV * np.log(coverage)
             + (AGE_BUMP if 2 <= years_since_entry <= 4 else 0.0) + year_factor)
    return float(1.0 / (1.0 + np.exp(-logit)))


def entry_weights(entry_year: int) -> np.ndarray:
    years_shifted = max(0, entry_year - (SHIFT_START - 1))
    scores = np.arange(1, 19)
    weights = ENTRY_WEIGHT * np.exp(SHIFT_TILT * years_shifted * (scores - 9))
    return weights / weights.sum()


def coverage_from(leverage: float, rng: np.random.Generator) -> float:
    return max(COV_FLOOR, round(float(np.exp(COV_BASE - COV_LEV * leverage + rng.normal(0, COV_NOISE))), 2))


def make_cohort() -> pd.DataFrame:
    ratings = pd.read_csv(DATA / "ratings.csv")
    rating_of = dict(zip(ratings["score"], ratings["rating"]))
    rng = np.random.default_rng(SEED)
    year_factor = {year: float(rng.normal(0, YEAR_FACTOR_SD)) for year in range(FIRST_ENTRY, LAST_YEAR + 1)}
    entry_years = np.sort(rng.integers(FIRST_ENTRY, LAST_ENTRY + 1, N_FIRMS))

    rows = []
    for number, entry_year in enumerate(entry_years, start=1):
        entry_year = int(entry_year)
        sector = SECTORS[int(rng.integers(0, len(SECTORS)))]
        score = int(rng.choice(np.arange(1, 19), p=entry_weights(entry_year)))
        shift = SHIFT_LEVERAGE * max(0, entry_year - (SHIFT_START - 1))
        leverage = max(LEV_FLOOR, round(float(LEV_BASE + LEV_SLOPE * score + shift + rng.normal(0, LEV_NOISE)), 2))
        coverage = coverage_from(leverage, rng)
        for year in range(entry_year, LAST_YEAR + 1):
            age = year - entry_year + 1
            p_default = default_chance(score, leverage, coverage, age, year_factor[year])
            defaulted = rng.random() < p_default
            exited = (not defaulted) and rng.random() < EXIT_CHANCE
            rows.append((f"F{number:04d}", year, age, sector, rating_of[score], score, leverage, coverage,
                         int(defaulted), int(exited)))
            if defaulted or exited:
                break
            # next year's start-of-year covariates
            move = rng.random()
            if move < DOWNGRADE:
                score = min(18, score + 1)
            elif move < DOWNGRADE + UPGRADE:
                score = max(1, score - 1)
            leverage = max(LEV_FLOOR, round(leverage + float(rng.normal(0, LEV_STEP)), 2))
            coverage = coverage_from(leverage, rng)
    return pd.DataFrame(rows, columns=COLUMNS)


def write_cohort(path: Path = OUT) -> None:
    make_cohort().to_csv(path, index=False, lineterminator="\n")


if __name__ == "__main__":
    write_cohort()
    print(f"wrote {OUT}")
