"""Generate the Excel reference values that the Course 2 tests read.

The script drives desktop Excel for Windows through COM, has Excel compute every value, and writes:

- data/bondmath_excel_reference.csv      one row per bond case: coupon dates, day counts, price, accrued,
                                          yield, durations, DV01, bumped prices, and a convexity estimate
- data/bondmath_excel_reference_tvm.csv  week 1 rows: FV, PV, RATE, EFFECT, NOMINAL, and a bond priced
                                          with PV, each with the exact formula text Excel evaluated

Nothing is typed by hand: every output value is read back from an Excel cell. Running it twice gives
byte-identical files. It also prints the Excel version and build, and re-checks the Excel behaviours
that the CSV columns do not carry (YEARFRAC and DAYS360 on February month ends, FORECAST.LINEAR with
an INDEX/MATCH bracket, and a What-If Data Table over PRICE).

Inputs are in course units (coupon and yield in percent). Every formula divides by 100 explicitly.
Basis is Excel's number: 0 is US 30/360, 1 is actual/actual.

Author tool: Windows with desktop Excel, and Python with pywin32. Not part of the course requirements.
Usage (from the repo root):  python tools/make_excel_reference.py
"""
import csv
import math
from datetime import date, timedelta
from pathlib import Path

import win32com.client

DATA = Path(__file__).resolve().parent.parent / "data"
EXCEL_EPOCH = date(1899, 12, 30)  # Excel serial 1 is 1900-01-01; this offset is right for every date after 1900-02-28

# group "edge": basis 0, semiannual. (case_id, settlement, maturity, coupon_pct, yield_pct)
EDGE = [
    ("edge_coupon_date_3y", "2026-09-30", "2029-09-30", 5.0, 5.5),
    ("edge_coupon_date_5y", "2026-09-30", "2031-09-30", 6.25, 6.0),
    ("edge_coupon_date_10y", "2026-09-30", "2036-09-30", 4.5, 5.25),
    ("edge_coupon_date_30y", "2026-09-30", "2056-09-30", 7.0, 6.5),
    ("edge_coupon_date_mid_month_par", "2026-09-15", "2033-03-15", 5.5, 5.5),
    ("edge_settle_day_after_coupon", "2026-09-16", "2031-03-15", 6.0, 6.4),
    ("edge_settle_day_before_coupon", "2027-03-14", "2031-03-15", 6.0, 6.4),
    ("edge_settle_31_oct_mat_15", "2026-10-31", "2032-04-15", 5.75, 6.1),
    ("edge_settle_31_oct_mat_30_jul", "2026-10-31", "2031-07-30", 4.875, 5.2),
    ("edge_settle_31_dec_mat_30_jun_eom", "2026-12-31", "2031-06-30", 6.5, 6.0),
    ("edge_settle_31_jan_mat_15", "2027-01-31", "2034-07-15", 7.25, 7.9),
    ("edge_settle_31_mar_after_feb_end", "2027-03-31", "2031-08-31", 5.125, 5.6),
    ("edge_settle_1_mar_after_feb_end", "2027-03-01", "2031-08-31", 5.125, 5.6),
    ("edge_settle_feb_27_nonleap", "2027-02-27", "2036-02-28", 8.125, 8.0),
    ("edge_settle_feb_28_nonleap_mat_15", "2027-02-28", "2032-05-15", 6.0, 5.5),
    ("edge_settle_feb_28_nonleap_coupon_date", "2027-02-28", "2031-08-31", 6.0, 5.5),
    ("edge_settle_feb_28_leap_not_month_end", "2028-02-28", "2033-08-31", 4.25, 4.9),
    ("edge_settle_feb_29_leap_mat_15", "2028-02-29", "2033-05-15", 4.25, 4.9),
    ("edge_settle_feb_29_leap_coupon_date", "2028-02-29", "2033-08-31", 4.25, 4.9),
    ("edge_settle_oct_30_mat_feb_28_leap", "2026-10-30", "2036-02-28", 8.125, 7.9),
    ("edge_mat_feb_28_nonleap_month_end", "2026-09-30", "2031-02-28", 5.0, 5.3),
    ("edge_mat_feb_29_leap_month_end", "2026-09-30", "2032-02-29", 5.0, 5.3),
    ("edge_mat_feb_28_leap_not_month_end", "2026-09-30", "2032-02-28", 5.0, 5.3),
    ("edge_mat_jan_31", "2026-09-30", "2031-01-31", 6.375, 6.0),
    ("edge_mat_mar_31", "2026-10-15", "2035-03-31", 4.0, 4.6),
    ("edge_mat_apr_30", "2026-09-30", "2031-04-30", 5.5, 5.1),
    ("edge_mat_may_31", "2026-09-30", "2031-05-31", 7.5, 8.2),
    ("edge_mat_jun_30", "2026-11-15", "2033-06-30", 3.875, 4.4),
    ("edge_mat_jul_31", "2026-09-30", "2036-07-31", 6.0, 6.75),
    ("edge_mat_aug_31", "2026-09-30", "2031-08-31", 5.125, 5.6),
    ("edge_mat_sep_30", "2026-12-15", "2030-09-30", 4.625, 4.3),
    ("edge_mat_oct_31", "2026-12-01", "2032-10-31", 5.875, 6.2),
    ("edge_mat_nov_30", "2026-09-30", "2034-11-30", 6.75, 7.3),
    ("edge_mat_dec_31", "2026-09-30", "2031-12-31", 4.5, 4.8),
    ("edge_mat_29_aug", "2026-09-30", "2031-08-29", 5.25, 5.8),
    ("edge_mat_30_aug", "2026-11-15", "2031-08-30", 5.25, 5.8),
    ("edge_mat_29_aug_leap_feb_coupon", "2027-10-15", "2032-08-29", 6.625, 6.1),
    ("edge_mat_30_mar", "2026-10-15", "2031-03-30", 3.5, 4.2),
    ("edge_mat_29_mar", "2026-09-30", "2033-03-29", 7.0, 6.6),
    ("edge_final_period", "2026-09-30", "2027-02-15", 5.0, 6.0),
    ("edge_final_period_month_end", "2026-12-15", "2027-02-28", 6.5, 5.0),
    ("edge_final_period_one_day_left", "2027-02-14", "2027-02-15", 4.0, 4.5),
    ("edge_final_period_one_day_in", "2026-08-16", "2027-02-15", 7.0, 7.5),
    ("edge_final_period_31_oct_mat_31_mar", "2026-10-31", "2027-03-31", 5.5, 5.0),
    ("edge_zero_coupon_10y", "2026-09-30", "2036-03-15", 0.0, 5.0),
    ("edge_zero_coupon_final_period", "2026-12-01", "2027-03-15", 0.0, 4.0),
    ("edge_low_yield", "2026-09-30", "2031-06-15", 1.0, 0.5),
    ("edge_high_yield", "2026-09-30", "2033-04-01", 8.0, 20.0),
    ("edge_high_coupon", "2026-09-30", "2034-12-01", 15.0, 12.0),
    ("edge_deep_discount_30y", "2026-09-30", "2056-05-15", 2.0, 9.0),
]

# group "frequency": basis 0, annual and quarterly. (case_id, settlement, maturity, coupon_pct, yield_pct, frequency)
FREQUENCY = [
    ("freq1_coupon_date", "2026-09-30", "2031-09-30", 5.0, 5.4, 1),
    ("freq1_mid_period", "2026-09-30", "2033-06-15", 6.25, 5.9, 1),
    ("freq1_mat_feb_29_month_end", "2026-09-30", "2032-02-29", 4.75, 5.1, 1),
    ("freq1_final_period", "2026-09-30", "2027-06-15", 5.5, 6.0, 1),
    ("freq1_30y", "2026-09-30", "2056-03-01", 6.0, 6.3, 1),
    ("freq1_settle_feb_28_nonleap", "2027-02-28", "2035-08-31", 7.0, 7.6, 1),
    ("freq1_settle_feb_29_leap", "2028-02-29", "2034-11-30", 3.25, 3.9, 1),
    ("freq4_coupon_date_month_end", "2026-09-30", "2031-12-31", 5.0, 5.4, 4),
    ("freq4_mat_30_aug", "2026-09-30", "2031-08-30", 6.0, 5.7, 4),
    ("freq4_settle_31_oct_mat_may_31", "2026-10-31", "2033-05-31", 4.5, 5.0, 4),
    ("freq4_final_period", "2026-09-30", "2026-12-15", 5.25, 5.5, 4),
    ("freq4_settle_feb_28_mat_29_nov", "2027-02-28", "2036-11-29", 6.875, 6.2, 4),
    ("freq4_settle_feb_29_mat_aug_31", "2028-02-29", "2030-08-31", 4.0, 4.4, 4),
    ("freq4_20y", "2026-11-15", "2046-02-15", 5.75, 6.1, 4),
    ("freq4_mat_feb_28_month_end", "2026-09-30", "2031-02-28", 5.0, 5.3, 4),
    ("freq4_zero_coupon", "2026-09-30", "2031-11-15", 0.0, 4.5, 4),
]

# group "basis1": actual/actual. (case_id, settlement, maturity, coupon_pct, yield_pct, frequency)
BASIS1 = [
    ("act_coupon_date_5y", "2026-09-30", "2031-09-30", 6.25, 6.0, 2),
    ("act_mid_period", "2026-09-30", "2033-03-15", 5.5, 5.8, 2),
    ("act_period_over_feb_29", "2027-09-30", "2032-03-15", 4.5, 4.9, 2),
    ("act_settle_in_leap_period", "2028-01-15", "2033-07-15", 6.0, 6.4, 2),
    ("act_settle_feb_28_nonleap", "2027-02-28", "2032-05-15", 6.0, 5.5, 2),
    ("act_settle_feb_29_leap", "2028-02-29", "2033-05-15", 4.25, 4.9, 2),
    ("act_settle_31_mar_after_feb_end", "2027-03-31", "2031-08-31", 5.125, 5.6, 2),
    ("act_mat_feb_28_nonleap_month_end", "2026-09-30", "2031-02-28", 5.0, 5.3, 2),
    ("act_mat_feb_28_leap_not_month_end", "2026-09-30", "2036-02-28", 8.125, 8.066, 2),
    ("act_mat_mar_31", "2026-10-15", "2031-03-31", 4.0, 4.6, 2),
    ("act_mat_apr_30", "2026-09-30", "2031-04-30", 5.5, 5.1, 2),
    ("act_mat_30_may_settle_coupon_date", "2026-05-30", "2031-05-30", 6.5, 6.9, 2),
    ("act_mat_30_may_mid_period", "2026-06-15", "2031-05-30", 6.5, 6.9, 2),
    ("act_mat_aug_31_late_in_period", "2027-08-29", "2031-08-31", 5.0, 5.2, 2),
    ("act_mat_29_aug", "2026-09-30", "2031-08-29", 5.25, 5.8, 2),
    ("act_mat_dec_31", "2026-09-30", "2031-12-31", 4.5, 4.8, 2),
    ("act_final_period", "2026-09-30", "2027-02-15", 5.0, 6.0, 2),
    ("act_final_period_month_end", "2026-12-15", "2027-02-28", 6.5, 5.0, 2),
    ("act_zero_coupon", "2026-09-30", "2036-03-15", 0.0, 5.0, 2),
    ("act_high_yield", "2026-09-30", "2033-04-01", 8.0, 20.0, 2),
    ("act_30y", "2026-09-30", "2056-05-15", 7.0, 6.5, 2),
    ("act_freq1_mid_period", "2026-09-30", "2033-06-15", 6.25, 5.9, 1),
    ("act_freq1_over_feb_29", "2027-06-30", "2031-03-15", 4.0, 4.3, 1),
    ("act_freq1_final_period", "2026-09-30", "2027-06-15", 5.5, 6.0, 1),
    ("act_freq4_mid_period", "2026-10-31", "2033-05-31", 4.5, 5.0, 4),
    ("act_freq4_mat_aug_31", "2026-10-15", "2031-08-31", 5.0, 5.2, 4),
    ("act_freq4_settle_feb_29", "2028-02-29", "2030-08-31", 4.0, 4.4, 4),
    ("act_freq4_final_period", "2026-09-30", "2026-12-15", 5.25, 5.5, 4),
]

# week 1 rows. FV and PV: (amount, rate_pct, years, frequency)
TVM_FV_PV = [(100, 5, 3, 2), (100, 5, 3, 1), (100, 5, 3, 4), (1000000, 4.25, 10, 2), (250000, 6.5, 2.5, 2),
             (100, 7.125, 30, 2), (100, 0.5, 1, 4), (5000000, 3.8, 0.5, 2)]
# the week 1 bonds (COURSE2_SPEC.md, "Week 1"), settling 2026-09-30 on a coupon date. (cusip, coupon_pct, yield_pct, years)
WEEK1_BONDS = [("99001BZA7", 5.25, 5.4, 5), ("99002CZA4", 6.125, 6.125, 7), ("99003DZA1", 4.75, 4.6, 3),
               ("99004EZA8", 7.5, 7.7, 10)]
WEEK1_EXERCISE_BONDS = [("99005FZA4", 5.625, 5.8, 4), ("99007HZA8", 4.375, 4.3, 2), ("99008IZA5", 5.0, 5.35, 6),
                        ("99009JZA2", 8.25, 8.6, 8)]
# day 1: 100 of redemption grown and discounted at each bond's yield, semiannually, and the first bond's
# at annual and quarterly compounding too. Appended after the original rows, so their case_id values do not move.
TVM_FV_PV += [(100, y, n, 2) for _, _, y, n in WEEK1_BONDS + WEEK1_EXERCISE_BONDS]
TVM_FV_PV += [(100, WEEK1_BONDS[0][2], WEEK1_BONDS[0][3], f) for f in (1, 4)]
# RATE: (coupon_pct, price, years, frequency)
TVM_RATE = [(5, 98.25, 3, 2), (6.25, 101.5, 5, 2), (4.5, 94.875, 10, 2), (7, 104, 30, 2), (5.5, 100, 7, 2),
            (8, 97, 4, 1), (3.75, 99.5, 2, 4), (0, 78.5, 5, 2), (9.25, 88, 6, 2), (2, 70, 20, 2)]
# EFFECT and NOMINAL: (rate_pct, frequency)
TVM_EFFECT = [(5, 2), (5, 4), (6.25, 2), (4.5, 1), (7.1, 2), (3, 4), (10, 2), (0.5, 2)]
TVM_NOMINAL = [(5.0625, 2), (5.0945, 4), (6.25, 2), (7.2, 4), (4, 1), (10.25, 2)]
# PV_BOND: (coupon_pct, yield_pct, years, frequency)
TVM_PV_BOND = [(5, 5.5, 3, 2), (6.25, 6, 5, 2), (4.5, 5.25, 10, 2), (7, 6.5, 30, 2), (5.5, 5.5, 7, 2),
               (8, 7.75, 4, 1), (3.75, 4, 2, 4), (0, 5, 5, 2), (9.25, 11, 6, 2), (2, 6, 20, 2),
               (5, 6, 1, 2), (6, 6, 10, 4)]
# day 2: each week 1 bond priced at its yield on its coupon date, the running set then the exercise set.
# Appended after the original rows, so their case_id values do not move.
TVM_PV_BOND += [(c, y, n, 2) for _, c, y, n in WEEK1_BONDS + WEEK1_EXERCISE_BONDS]
# day 3: each week 1 bond's semiannual yield restated as an annually compounded rate, running set then exercise
# set. Written at the end of the file, after every earlier row, so no earlier row moves (day 2's notebook shows
# row positions); their case_id values continue the EFFECT numbering.
TVM_EFFECT_DAY3 = [(y, 2) for _, _, y, _ in WEEK1_BONDS + WEEK1_EXERCISE_BONDS]
# day 3: PRICE with settlement on the coupon date 2026-09-30, at yields other than the bond's own:
# (coupon_pct, yield_pct, years). The first running bond from 2.4 to 8.4 percent in 1-point steps (the
# price-yield column), the other three running bonds and one exercise bond (99008IZA5) 1 point either side.
TVM_PRICE = ([(5.25, y, 5) for y in (2.4, 3.4, 4.4, 5.4, 6.4, 7.4, 8.4)]
             + [(6.125, 5.125, 7), (6.125, 7.125, 7), (4.75, 3.6, 3), (4.75, 5.6, 3), (7.5, 6.7, 10), (7.5, 8.7, 10),
                (5.0, 4.35, 6), (5.0, 6.35, 6)])

REFERENCE_COLUMNS = ["case_id", "group", "settlement", "maturity", "coupon_pct", "yield_pct", "frequency", "basis",
                     "couppcd", "coupncd", "coupnum", "coupdaybs", "coupdays", "coupdaysnc", "price", "accrued",
                     "accrint", "yield_pct_from_price", "duration", "mduration", "dv01", "price_down_1bp",
                     "price_up_1bp", "convexity_fd"]
TVM_COLUMNS = ["case_id", "function", "amount", "rate_pct", "coupon_pct", "price", "years", "frequency",
               "excel_formula", "excel_value"]
OUTPUT_COLUMNS = REFERENCE_COLUMNS[8:]
DATE_COLUMNS = {"couppcd", "coupncd"}
INTEGER_COLUMNS = {"coupnum", "coupdaybs", "coupdays", "coupdaysnc"}


def serial(d: date) -> int:
    return (d - EXCEL_EPOCH).days


def from_serial(value: float) -> date:
    return EXCEL_EPOCH + timedelta(days=int(value))


def num(x: float) -> str:
    """A number as it is written in a formula or CSV cell: 3 rather than 3.0, otherwise the shortest exact form."""
    return str(int(x)) if float(x).is_integer() else repr(float(x))


def is_error(value) -> bool:
    # Value2 returns Excel errors (#NUM! and the like) as negative integers and numbers as floats
    return not isinstance(value, float)


def build_cases() -> list[dict]:
    cases = []
    with open(DATA / "holdings.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cases.append(dict(case_id=row["cusip"], group="holdings", settlement=row["as_of_date"],
                              maturity=row["maturity"], coupon_pct=float(row["coupon"]),
                              yield_pct=float(row["yield_pct"]), frequency=2, basis=0))
    for case_id, settlement, maturity, coupon, yld in EDGE:
        cases.append(dict(case_id=case_id, group="edge", settlement=settlement, maturity=maturity,
                          coupon_pct=coupon, yield_pct=yld, frequency=2, basis=0))
    for group, rows, basis in (("frequency", FREQUENCY, 0), ("basis1", BASIS1, 1)):
        for case_id, settlement, maturity, coupon, yld, frequency in rows:
            cases.append(dict(case_id=case_id, group=group, settlement=settlement, maturity=maturity,
                              coupon_pct=coupon, yield_pct=yld, frequency=frequency, basis=basis))
    if len({c["case_id"] for c in cases}) != len(cases):
        raise ValueError("case_id values are not unique")
    return cases


def reference_formulas(r: int, basis: int) -> list[str]:
    """Formulas for sheet row r. Columns A to F hold settlement, maturity, coupon_pct, yield_pct, frequency, basis."""
    dates = f"A{r},B{r},E{r},F{r}"
    rate, yld = f"C{r}/100", f"D{r}/100"
    bond = f"A{r},B{r},{rate}"
    # the accrued formula: E is COUPDAYS under basis 0, and the actual length of the period under basis 1,
    # because COUPDAYS with basis 1 is not always the period length (see DATA.md)
    period = f"COUPDAYS({dates})" if basis == 0 else f"(COUPNCD({dates})-COUPPCD({dates}))"
    # output columns G to V, in OUTPUT_COLUMNS order: M is price, N accrued, R mduration, T and U the bumped prices
    return [
        f"=COUPPCD({dates})",
        f"=COUPNCD({dates})",
        f"=COUPNUM({dates})",
        f"=COUPDAYBS({dates})",
        f"=COUPDAYS({dates})",
        f"=COUPDAYSNC({dates})",
        f"=PRICE({bond},{yld},100,E{r},F{r})",
        f"=100*{rate}/E{r}*COUPDAYBS({dates})/{period}",
        f"=ACCRINT(COUPPCD({dates}),COUPNCD({dates}),A{r},{rate},100,E{r},F{r})",
        f"=YIELD({bond},M{r},100,E{r},F{r})*100",
        f"=DURATION({bond},{yld},E{r},F{r})",
        f"=MDURATION({bond},{yld},E{r},F{r})",
        f"=R{r}*(M{r}+N{r})/10000",
        f"=PRICE({bond},{yld}-0.0001,100,E{r},F{r})",
        f"=PRICE({bond},{yld}+0.0001,100,E{r},F{r})",
        f"=(T{r}+U{r}-2*M{r})/((M{r}+N{r})*0.0001^2)",
    ]


def compute_reference(ws, app, cases: list[dict]) -> list[dict]:
    n = len(cases)
    inputs = [[serial(date.fromisoformat(c["settlement"])), serial(date.fromisoformat(c["maturity"])),
               c["coupon_pct"], c["yield_pct"], c["frequency"], c["basis"]] for c in cases]
    ws.Range(ws.Cells(1, 1), ws.Cells(n, 6)).Value2 = inputs
    formulas = [reference_formulas(r, c["basis"]) for r, c in enumerate(cases, start=1)]
    out_range = ws.Range(ws.Cells(1, 7), ws.Cells(n, 6 + len(OUTPUT_COLUMNS)))
    out_range.Formula = formulas
    app.Calculate()
    values = out_range.Value2

    rows = []
    for case, row_values in zip(cases, values):
        row = dict(case_id=case["case_id"], group=case["group"], settlement=case["settlement"],
                   maturity=case["maturity"], coupon_pct=repr(float(case["coupon_pct"])),
                   yield_pct=repr(float(case["yield_pct"])), frequency=case["frequency"], basis=case["basis"])
        for column, value in zip(OUTPUT_COLUMNS, row_values):
            if is_error(value):
                # ACCRINT refuses an issue date equal to settlement and a zero rate; every other column must compute
                on_coupon_date = row["coupdaybs"] == 0
                if column == "accrint" and (on_coupon_date or case["coupon_pct"] == 0):
                    row[column] = ""
                    continue
                raise RuntimeError(f"Excel returned error {value} for {column} in case {case['case_id']}")
            if column in DATE_COLUMNS:
                row[column] = from_serial(value).isoformat()
            elif column in INTEGER_COLUMNS:
                if not value.is_integer():
                    raise RuntimeError(f"{column} is not a whole number in case {case['case_id']}: {value}")
                row[column] = int(value)
            else:
                row[column] = repr(value)
        rows.append(row)
    ws.Cells.Clear()
    return rows


def tvm_cases() -> list[dict]:
    cases = []

    def add(function: str, formula: str, **inputs) -> None:
        cases.append(dict(case_id=f"tvm_{function.lower()}_{sum(c['function'] == function for c in cases) + 1:02d}",
                          function=function, excel_formula=formula, **{k: num(v) for k, v in inputs.items()}))

    for amount, rate, years, f in TVM_FV_PV:
        add("FV", f"=FV({num(rate)}/100/{f},{f}*{num(years)},0,-{num(amount)})",
            amount=amount, rate_pct=rate, years=years, frequency=f)
    for amount, rate, years, f in TVM_FV_PV:
        add("PV", f"=PV({num(rate)}/100/{f},{f}*{num(years)},0,{num(amount)})",
            amount=amount, rate_pct=rate, years=years, frequency=f)
    for coupon, price, years, f in TVM_RATE:
        add("RATE", f"=RATE({f}*{num(years)},{num(coupon)}/{f},-{num(price)},100)*{f}",
            coupon_pct=coupon, price=price, years=years, frequency=f)
    for rate, f in TVM_EFFECT:
        add("EFFECT", f"=EFFECT({num(rate)}/100,{f})", rate_pct=rate, frequency=f)
    for rate, f in TVM_NOMINAL:
        add("NOMINAL", f"=NOMINAL({num(rate)}/100,{f})", rate_pct=rate, frequency=f)
    for coupon, yld, years, f in TVM_PV_BOND:
        add("PV_BOND", f"=-PV({num(yld)}/100/{f},{f}*{num(years)},{num(coupon)}/{f},100)",
            coupon_pct=coupon, rate_pct=yld, years=years, frequency=f)
    for rate, f in TVM_EFFECT_DAY3:
        add("EFFECT", f"=EFFECT({num(rate)}/100,{f})", rate_pct=rate, frequency=f)
    for coupon, yld, years in TVM_PRICE:
        add("PRICE", f"=PRICE(DATE(2026,9,30),DATE({2026 + years},9,30),{num(coupon)}/100,{num(yld)}/100,100,2,0)",
            coupon_pct=coupon, rate_pct=yld, years=years, frequency=2)
    return cases


def compute_tvm(ws, app, cases: list[dict]) -> list[dict]:
    rng = ws.Range(ws.Cells(1, 1), ws.Cells(len(cases), 1))
    rng.Formula = [[c["excel_formula"]] for c in cases]
    app.Calculate()
    # Value2, not Value: Excel formats FV and PV cells as currency, and Value would round them to 4 decimals
    values = [row[0] for row in rng.Value2]
    rows = []
    for case, value in zip(cases, values):
        if is_error(value):
            raise RuntimeError(f"Excel returned error {value} for {case['case_id']}")
        rows.append({column: case.get(column, "") for column in TVM_COLUMNS} | {"excel_value": repr(value)})
    ws.Cells.Clear()
    return rows


def evaluate(ws, app, formulas: list[str]) -> list:
    rng = ws.Range(ws.Cells(1, 1), ws.Cells(len(formulas), 1))
    rng.Formula = [[f] for f in formulas]
    app.Calculate()
    values = [row[0] for row in rng.Value2]
    ws.Cells.Clear()
    return values


def confirm_behaviour(ws, app) -> None:
    """Print checks of Excel behaviours that the CSV columns do not carry. Each line ends in ok or DIFFERS."""
    print("Behaviour checks:")
    # YEARFRAC basis 0 and DAYS360 on February month ends, against the course's 30/360 rules
    pairs = [("2027-02-28", "2028-02-29", 360, 359), ("2027-02-28", "2031-08-31", 1621, 1620),
             ("2026-02-28", "2026-10-31", 241, 240), ("2027-02-28", "2027-02-28", 0, -2),
             ("2026-09-30", "2036-09-30", 3600, 3600), ("2026-09-30", "2032-06-18", 2058, 2058)]
    formulas = []
    for start, end, _, _ in pairs:
        s, e = serial(date.fromisoformat(start)), serial(date.fromisoformat(end))
        formulas += [f"=YEARFRAC({s},{e},0)*360", f"=DAYS360({s},{e})"]
    values = evaluate(ws, app, formulas)
    for i, (start, end, rules, days360) in enumerate(pairs):
        yearfrac_days, days360_value = values[2 * i], values[2 * i + 1]
        ok = abs(yearfrac_days - rules) < 1e-9 and days360_value == days360
        print(f"  {start} to {end}: YEARFRAC(,,0)*360 = {yearfrac_days:.9f} (rules {rules}), "
              f"DAYS360 = {days360_value:.0f} (expected {days360}): {'ok' if ok else 'DIFFERS'}")

    # FORECAST.LINEAR with an INDEX/MATCH bracket, on the invented curve, against linear interpolation
    tenors = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
    yields = [round(3.55 + 1.05 * (1 - math.exp(-t / 7)), 3) for t in tenors]
    ws.Range("A1:B10").Value2 = [[t, y] for t, y in zip(tenors, yields)]
    points = [0.25, 0.92, 6.4, 10, 29.5]
    for i, x in enumerate(points, start=1):
        ws.Cells(i, 4).Value2 = x
        bracket = f"MATCH(D{i},$A$1:$A$10,1)"
        ws.Cells(i, 5).Formula = (f"=FORECAST.LINEAR(D{i},INDEX($B$1:$B$10,{bracket}):INDEX($B$1:$B$10,{bracket}+1),"
                                  f"INDEX($A$1:$A$10,{bracket}):INDEX($A$1:$A$10,{bracket}+1))")
    app.Calculate()
    for i, x in enumerate(points, start=1):
        k = max(j for j in range(len(tenors)) if tenors[j] <= x)
        k = min(k, len(tenors) - 2)
        expected = yields[k] + (yields[k + 1] - yields[k]) * (x - tenors[k]) / (tenors[k + 1] - tenors[k])
        got = ws.Cells(i, 5).Value2
        print(f"  FORECAST.LINEAR with INDEX/MATCH at {x} years: {got!r} against {expected!r}: "
              f"{'ok' if abs(got - expected) < 1e-12 else 'DIFFERS'}")
    print(f"  The formula, for the tenor in D1: {ws.Cells(1, 5).Formula}")
    ws.Cells.Clear()

    # What-If Data Table: a column of yield shifts over a PRICE formula, against PRICE at each shifted yield
    s, m = serial(date(2026, 9, 30)), serial(date(2036, 3, 15))
    ws.Range("H1").Value2 = 5.0  # yield_pct
    ws.Range("H2").Value2 = 0  # shift in basis points, the table's input cell
    ws.Range("J2").Formula = f"=PRICE({s},{m},6/100,(H1+H2/100)/100,100,2,0)"
    shifts = [-100, -25, 25, 100]
    for i, shift in enumerate(shifts, start=3):
        ws.Cells(i, 9).Value2 = shift
    ws.Range("I2:J6").Table(None, ws.Range("H2"))
    for yld in (5.0, 7.0):
        ws.Range("H1").Value2 = yld
        app.Calculate()
        table = [ws.Cells(i, 10).Value2 for i in range(3, 3 + len(shifts))]
        direct = evaluate_keep(ws, app, [f"=PRICE({s},{m},6/100,({yld}+{shift}/100)/100,100,2,0)" for shift in shifts])
        gap = max(abs(a - b) for a, b in zip(table, direct))
        print(f"  Data Table over PRICE at yield {yld}: largest gap to direct PRICE {gap!r}: "
              f"{'ok' if gap == 0 else 'DIFFERS'} (table cell formula {ws.Range('J3').Formula})")
    ws.Cells.Clear()

    # week 1: the discount and growth formulas written out by hand, against PV and FV, for each week 1 bond
    for cusip, _, yld, years in WEEK1_BONDS:
        y, n = num(yld), num(years)
        written_pv, minus_pv, written_fv, fv = evaluate(ws, app, [
            f"=100/(1+{y}/100/2)^(2*{n})", f"=-PV({y}/100/2,2*{n},0,100)",
            f"=100*(1+{y}/100/2)^(2*{n})", f"=FV({y}/100/2,2*{n},0,-100)"])
        gap = max(abs(written_pv - minus_pv), abs(written_fv - fv))
        print(f"  {cusip}: =100/(1+{y}/100/2)^(2*{n}) = {written_pv!r}, -PV {minus_pv!r}; "
              f"=100*(1+{y}/100/2)^(2*{n}) = {written_fv!r}, FV {fv!r}: {'ok' if gap < 1e-12 else 'DIFFERS'}")

    # week 1: a growth column filled down period by period ends on FV's value
    _, _, yld, years = WEEK1_BONDS[0]
    periods = 2 * years
    ws.Range("A1").Value2 = 100
    ws.Range(f"A2:A{periods + 1}").Formula = f"=A1*(1+{num(yld)}/100/2)"
    ws.Range("C1").Formula = f"=FV({num(yld)}/100/2,2*{num(years)},0,-100)"
    app.Calculate()
    last, fv = ws.Range(f"A{periods + 1}").Value2, ws.Range("C1").Value2
    print(f"  Growth column =A1*(1+{num(yld)}/100/2) filled down {periods} periods: {last!r}, FV {fv!r}: "
          f"{'ok' if abs(last - fv) < 1e-12 else 'DIFFERS'}")
    ws.Cells.Clear()

    # week 1 day 2: a bond priced on a coupon date three more ways, against -PV with the coupon, for each week 1
    # running bond: NPV over a column of the cash flows (NPV discounts its first value by one full period);
    # a column of each cash flow over (1+y/100/2)^period, summed; and PRICE with settlement on the coupon date
    for cusip, coupon, yld, years in WEEK1_BONDS:
        c, y, n = num(coupon), num(yld), num(years)
        periods = 2 * years
        for k in range(1, periods + 1):
            ws.Cells(k, 1).Value2 = k
            ws.Cells(k, 2).Formula = f"={c}/2+100" if k == periods else f"={c}/2"
            ws.Cells(k, 3).Formula = f"=B{k}/(1+{y}/100/2)^A{k}"
        ws.Range("E1").Formula = f"=NPV({y}/100/2,B1:B{periods})"
        ws.Range("E2").Formula = f"=SUM(C1:C{periods})"
        ws.Range("E3").Formula = f"=-PV({y}/100/2,2*{n},{c}/2,100)"
        ws.Range("E4").Formula = f"=PRICE(DATE(2026,9,30),DATE({2026 + years},9,30),{c}/100,{y}/100,100,2,0)"
        app.Calculate()
        npv, column_sum, minus_pv, price = (ws.Range(f"E{i}").Value2 for i in range(1, 5))
        gap = max(abs(npv - minus_pv), abs(column_sum - minus_pv), abs(price - minus_pv))
        print(f"  {cusip}: -PV {minus_pv!r}; =NPV({y}/100/2,B1:B{periods}) {npv!r}; column of B/(1+{y}/100/2)^A "
              f"summed {column_sum!r}; {ws.Range('E4').Formula} {price!r}: largest gap {gap!r}: "
              f"{'ok' if gap < 1e-9 else 'DIFFERS'}")
        ws.Cells.Clear()

    # week 1 day 3: a semiannual yield restated quarterly in two cells, EFFECT then NOMINAL, against the
    # course formula ((1 + y/100/2)^2)^(1/4) - 1, times 4; and NOMINAL back to frequency 2 returns the yield
    for cusip, _, yld, _ in WEEK1_BONDS:
        y = num(yld)
        ws.Range("A1").Formula = f"=EFFECT({y}/100,2)"
        ws.Range("A2").Formula = "=NOMINAL(A1,4)*100"
        ws.Range("A3").Formula = "=NOMINAL(A1,2)*100"
        app.Calculate()
        quarterly, back = ws.Range("A2").Value2, ws.Range("A3").Value2
        expected = (((1 + yld / 100 / 2) ** 2) ** (1 / 4) - 1) * 4 * 100
        ok = abs(quarterly - expected) < 1e-12 and abs(back - yld) < 1e-12
        print(f"  {cusip}: =EFFECT({y}/100,2) in A1, =NOMINAL(A1,4)*100 {quarterly!r} (formula {expected!r}), "
              f"=NOMINAL(A1,2)*100 {back!r}: {'ok' if ok else 'DIFFERS'}")
        ws.Cells.Clear()

    # week 1 day 3: the price-yield column for the first running bond, yields in A2:A8 under a header, PRICE
    # filled down in B2:B8 reading the yield from column A, then a Scatter with Straight Lines chart made from the
    # selected A1:B8, as a student would insert it. The column must equal the PRICE rows of the TVM file, and the
    # chart's one series must take its x values from column A and its y values from column B.
    _, coupon, _, years = WEEK1_BONDS[0]
    grid = [y for c, y, n in TVM_PRICE if c == coupon and n == years]
    ws.Range("A1").Value2 = "yield_pct"
    ws.Range("B1").Value2 = "price"
    for i, y in enumerate(grid, start=2):
        ws.Cells(i, 1).Value2 = y
    last = len(grid) + 1
    ws.Range(f"B2:B{last}").Formula = f"=PRICE(DATE(2026,9,30),DATE({2026 + years},9,30),{num(coupon)}/100,A2/100,100,2,0)"
    app.Calculate()
    column = [ws.Cells(i, 2).Value2 for i in range(2, last + 1)]
    direct = evaluate_keep(ws, app, [f"=PRICE(DATE(2026,9,30),DATE({2026 + years},9,30),{num(coupon)}/100,{num(y)}/100,100,2,0)"
                                     for y in grid])
    ws.Activate()
    ws.Range(f"A1:B{last}").Select()
    chart = ws.Shapes.AddChart2(-1, 74).Chart  # 74 is xlXYScatterLines, Scatter with Straight Lines
    series = chart.SeriesCollection(1)
    ok = (column == direct and chart.SeriesCollection().Count == 1 and list(series.XValues) == grid
          and list(series.Values) == column and series.Name == "price")
    print(f"  Price-yield column =PRICE(...,{num(coupon)}/100,A2/100,100,2,0) for {WEEK1_BONDS[0][0]} at {grid}: "
          f"{column!r}; equal to the PRICE rows {column == direct}; Scatter with Straight Lines from A1:B{last}: "
          f"{chart.SeriesCollection().Count} series named {series.Name!r}, x values {list(series.XValues)}: "
          f"{'ok' if ok else 'DIFFERS'}")
    chart.Parent.Delete()
    ws.Cells.Clear()

    # week 1 day 3: pull to par on coupon dates. Years left in column A (from the full term down to 0.5),
    # =-PV(y/100/2,2*A1,c/2,100) in column B, against PRICE settled on the coupon date that leaves that many
    # years (maturity 30 September is a month end, so coupons fall on 31 March and 30 September)
    for cusip, coupon, yld, years in (WEEK1_BONDS[3], WEEK1_BONDS[2]):
        c, y = num(coupon), num(yld)
        rows = []
        for k in range(2 * years, 0, -1):
            months_back = 6 * k
            year, month = 2026 + years - (months_back // 12), 9 - months_back % 12
            if month <= 0:
                year, month = year - 1, month + 12
            day = 31 if month == 3 else 30
            rows.append((k / 2, f"DATE({year},{month},{day})"))
        for i, (left, settle) in enumerate(rows, start=1):
            ws.Cells(i, 1).Value2 = left
            ws.Cells(i, 2).Formula = f"=-PV({y}/100/2,2*A{i},{c}/2,100)"
            ws.Cells(i, 3).Formula = f"=PRICE({settle},DATE({2026 + years},9,30),{c}/100,{y}/100,100,2,0)"
        app.Calculate()
        gap = max(abs(ws.Cells(i, 2).Value2 - ws.Cells(i, 3).Value2) for i in range(1, len(rows) + 1))
        first, last_value = ws.Cells(1, 2).Value2, ws.Cells(len(rows), 2).Value2
        print(f"  {cusip}: pull to par =-PV({y}/100/2,2*A1,{c}/2,100) over {len(rows)} coupon dates, {first!r} "
              f"down to {last_value!r} at 0.5 years; against PRICE settled on each coupon date (first {rows[0][1]}), "
              f"largest gap {gap!r}: {'ok' if gap < 1e-9 else 'DIFFERS'}")
        ws.Cells.Clear()


def evaluate_keep(ws, app, formulas: list[str]) -> list:
    """Evaluate formulas in column L without clearing the rest of the sheet."""
    rng = ws.Range(ws.Cells(1, 12), ws.Cells(len(formulas), 12))
    rng.Formula = [[f] for f in formulas]
    app.Calculate()
    values = [row[0] for row in rng.Value2]
    rng.ClearContents()
    return values


def write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    cases = build_cases()
    app = win32com.client.DispatchEx("Excel.Application")
    try:
        app.Visible = False
        app.DisplayAlerts = False
        print(f"Excel {app.Version}, build {app.Build:.0f}, {app.OperatingSystem}")
        workbook = app.Workbooks.Add()
        ws = workbook.Worksheets(1)
        reference = compute_reference(ws, app, cases)
        tvm = compute_tvm(ws, app, tvm_cases())
        confirm_behaviour(ws, app)
        workbook.Close(SaveChanges=False)
    finally:
        app.Quit()

    write_csv(DATA / "bondmath_excel_reference.csv", REFERENCE_COLUMNS, reference)
    write_csv(DATA / "bondmath_excel_reference_tvm.csv", TVM_COLUMNS, tvm)
    groups = {g: sum(r["group"] == g for r in reference) for g in ("holdings", "edge", "frequency", "basis1")}
    blank_accrint = sum(r["accrint"] == "" for r in reference)
    print(f"bondmath_excel_reference.csv: {len(reference)} rows {groups}, accrint blank in {blank_accrint}")
    print(f"bondmath_excel_reference_tvm.csv: {len(tvm)} rows")


if __name__ == "__main__":
    main()
