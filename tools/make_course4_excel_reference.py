"""Generate the Excel reference values that the Course 4 tests read, and check the Excel behaviours Course 4 states.

The script drives desktop Excel for Windows through COM, has Excel compute every value, and writes:

- data/course4_excel_reference.csv   long format, one row per Excel result: case_id (model:quantity), quantity,
                                      excel_formula (the exact formula text Excel evaluated, or for a Solver result
                                      a description of the Solver run), excel_value (Value2, written with repr)

Rows, by the day of COURSE4_SPEC.md that first needs them. Every regression uses all 821 bonds of benchmark.csv
joined to ratings.csv (not a train and test split), so the file does not depend on any library's split:

- d01  SLOPE, INTERCEPT, RSQ, CORREL of oas (bp) on rating score; MAE and RMSE in bp of that line
- d02  LINEST of oas on score and duration; LINEST of oas on 17 rating dummies (reference A), duration, and
       9 sector dummies (reference Consumer), the dummies made by =--(cell="level"); adjusted R-squared by formula
- d03  LINEST of LN(oas) on score, duration, and the 9 sector dummies: coefficients, standard errors, R-squared,
       F, degrees of freedom, sums of squares, T.DIST.2T p-values, T.INV.2T 95 percent intervals, and each
       column's VIF as 1/(1-R2) of LINEST of that column on the others
- d04  LINEST of LN(oas) on rating dummies, duration, and sector dummies; Breusch-Pagan by hand (LINEST of the
       squared TREND residuals on the same columns, LM = n x R2, CHISQ.DIST.RT) for the bp and the log model;
       Q-Q theoretical quantiles by NORM.S.INV((RANK.EQ(r,range,1)-0.5)/n)
- d05  STDEV.S against STDEV.P of duration; ridge (alpha 10) in closed form with MMULT, TRANSPOSE, MINVERSE,
       MUNIT on columns standardized with STDEV.P, the intercept the mean of the target
- d06  Solver (GRG Nonlinear, "Make Unconstrained Variables Non-Negative" off) maximising the summed
       log-likelihood of default on PAY_0, and on PAY_0 and LIMIT_BAL per 10,000 NT dollars, over the 30,000
       card rows; the log-likelihood at Solver's coefficients; EXP of each slope as an odds ratio
- d07  confusion counts by COUNTIFS at threshold 0.5 on the PAY_0 model's probabilities (flagged when the
       probability is at least the threshold), precision, recall, accuracy, F1 by formula
- d08  ROC points at every distinct probability of the PAY_0 model by COUNTIFS, AUC by the trapezoid rule
       with SUMPRODUCT

It also prints the Excel version and build and these behaviour checks, which the CSV does not carry:
Formula against Formula2 for =AVERAGE(ABS(a-b)); Solver with its default options; a depth-2 tree of the card
file written as nested IF against the tree's own flags on every validation row (day 9); a rolling
SLOPE(OFFSET(...)) over 252 rows against a fit on each trailing window (day 11); SQRT(SUMXMY2(...)) distances
and MATCH(MIN(...)) nearest centres against K-means labels (day 12); a pivot table's Count and Average and
MEDIAN(IF(...)) by cluster (day 13); COVARIANCE.S and MMULT component scores (day 14).

The tree and the K-means centres are fitted by scikit-learn in the course venv (a subprocess), because Excel has
neither; Excel then reproduces their output. The Analysis ToolPak is not driven: a probe left Excel on a Visual
Basic dialog (COURSE4_SPEC.md).

Nothing is typed by hand: every output value is read back from an Excel cell with Value2 and written with repr.
Running it twice gives byte-identical files. Author tool: Windows with desktop Excel, and Python with pywin32.
Not part of the course requirements.

Usage (from the repo root):  python tools/make_course4_excel_reference.py [--out FOLDER]
"""
import csv
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import win32com.client
import win32process

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
VENV_PYTHON = REPO / ".venv" / "Scripts" / "python.exe"
OUT_NAME = "course4_excel_reference.csv"
COLUMNS = ["case_id", "quantity", "excel_formula", "excel_value"]
ERRORS = {-2146826281: "#DIV/0!", -2146826246: "#N/A", -2146826259: "#NAME?", -2146826288: "#NULL!",
          -2146826252: "#NUM!", -2146826265: "#REF!", -2146826273: "#VALUE!"}
XL_MANUAL, XL_AUTOMATIC = -4135, -4105
RIDGE_ALPHA = 10
RATING_REFERENCE, SECTOR_REFERENCE = "A", "Consumer"
TARGET = "default payment next month"
TENORS = ["1 Yr", "2 Yr", "3 Yr", "5 Yr", "7 Yr", "10 Yr", "20 Yr", "30 Yr"]

# fitted by scikit-learn in the course venv; Excel then reproduces the output
SKLEARN_HELPER = r'''
import json, os, sys
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np, pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
data = sys.argv[1]
card = pd.read_csv(f"{data}/credit_card_default.csv")
features = ["LIMIT_BAL", "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"] + \
    [f"BILL_AMT{i}" for i in range(1, 7)] + [f"PAY_AMT{i}" for i in range(1, 7)]
X, y = card[features], card["default payment next month"]
X_rest, X_test, y_rest, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
X_train, X_valid, y_train, y_valid = train_test_split(X_rest, y_rest, test_size=0.25, stratify=y_rest, random_state=42)
tree = DecisionTreeClassifier(max_depth=2, random_state=42).fit(X_train, y_train)
t = tree.tree_
nodes = [{"feature": features[t.feature[i]] if t.children_left[i] != -1 else None,
          "threshold": float(t.threshold[i]), "left": int(t.children_left[i]), "right": int(t.children_right[i]),
          "leaf_class": int(np.argmax(t.value[i][0]))} for i in range(t.node_count)]
bench = pd.read_csv(f"{data}/benchmark.csv").merge(pd.read_csv(f"{data}/ratings.csv"), on="rating", validate="many_to_one")
bench["log_oas"] = np.log(bench["oas"])
scaled = StandardScaler().fit_transform(bench[["log_oas", "duration", "coupon", "score"]])
km = KMeans(n_clusters=4, n_init=10, random_state=42).fit(scaled)
print(json.dumps({"nodes": nodes, "valid_positions": [int(i) for i in X_valid.index],
                  "valid_flags": [int(v) for v in tree.predict(X_valid)],
                  "centres": km.cluster_centers_.tolist(), "labels": [int(v) for v in km.labels_]}))
'''


def col(n: int) -> str:
    """Excel column letters for a 1-based column number."""
    letters = ""
    while n:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def shown(value) -> str:
    if isinstance(value, int) and value in ERRORS:
        return ERRORS[value]
    return repr(value)


def read_csv(name: str) -> list[dict]:
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_block(ws, top: int, left: int, rows: list[list]) -> None:
    ws.Range(ws.Cells(top, left), ws.Cells(top + len(rows) - 1, left + len(rows[0]) - 1)).Value2 = rows


class Reference:
    """Collects (model, quantity, formula) rows, has Excel evaluate them on one sheet, and keeps the results."""

    def __init__(self) -> None:
        self.pending: list[tuple[str, str, str]] = []
        self.rows: list[dict] = []

    def add(self, model: str, quantity: str, formula: str) -> None:
        self.pending.append((model, quantity, formula))

    def evaluate(self, ws, app) -> None:
        for i, (_, _, formula) in enumerate(self.pending, start=1):
            ws.Cells(i, 1).Formula2 = formula
        app.Calculate()
        for i, (model, quantity, _) in enumerate(self.pending, start=1):
            value = ws.Cells(i, 1).Value2
            if not isinstance(value, float):
                raise RuntimeError(f"Excel returned {shown(value)} for {model}:{quantity}")
            self.keep(model, quantity, ws.Cells(i, 1).Formula2, value)
        ws.Cells.Clear()
        self.pending = []

    def keep(self, model: str, quantity: str, formula: str, value: float) -> None:
        self.rows.append({"case_id": f"{model}:{quantity}", "quantity": quantity, "excel_formula": formula,
                          "excel_value": repr(float(value))})


def bench_sheet(ws) -> dict:
    """Write the 821 bonds and the derived columns; return the ranges each model needs."""
    ratings = {row["rating"]: int(row["score"]) for row in read_csv("ratings.csv")}
    bonds = read_csv("benchmark.csv")
    n = len(bonds)
    last = n + 1
    levels = list(ratings)
    sectors = sorted({b["sector"] for b in bonds})
    rating_dummies = [lv for lv in levels if lv != RATING_REFERENCE]
    sector_dummies = [s for s in sectors if s != SECTOR_REFERENCE]
    # A oas, B score, C duration, D coupon, E rating, F sector, G LN(oas)
    ws.Range("A1:G1").Value2 = [["oas", "score", "duration", "coupon", "rating", "sector", "log_oas"]]
    write_block(ws, 2, 1, [[float(b["oas"]), float(ratings[b["rating"]]), float(b["duration"]), float(b["coupon"]),
                            b["rating"], b["sector"]] for b in bonds])
    ws.Range(f"G2:G{last}").Formula = "=LN(A2)"

    # block 1 from column J: rating dummies, duration, sector dummies (27 columns)
    start = 10
    names_big = [f"rating_{lv}" for lv in rating_dummies] + ["duration"] + [f"sector_{s}" for s in sector_dummies]
    for j, name in enumerate(names_big):
        c = col(start + j)
        ws.Cells(1, start + j).Value2 = name
        if name.startswith("rating_"):
            formula = f'=--($E2="{name[7:]}")'
        elif name.startswith("sector_"):
            formula = f'=--($F2="{name[7:]}")'
        else:
            formula = "=$C2"
        ws.Range(f"{c}2:{c}{last}").Formula = formula
    big = f"${col(start)}$2:${col(start + len(names_big) - 1)}${last}"

    # block 2: score, duration, sector dummies (11 columns)
    start2 = start + len(names_big) + 1
    names_m3 = ["score", "duration"] + [f"sector_{s}" for s in sector_dummies]
    for j, name in enumerate(names_m3):
        c = col(start2 + j)
        ws.Cells(1, start2 + j).Value2 = name
        formula = {"score": "=$B2", "duration": "=$C2"}.get(name, f'=--($F2="{name[7:]}")')
        ws.Range(f"{c}2:{c}{last}").Formula = formula
    m3 = f"${col(start2)}$2:${col(start2 + len(names_m3) - 1)}${last}"

    # block 3: score, duration, coupon standardized with STDEV.P (ridge)
    start3 = start2 + len(names_m3) + 1
    names_ridge = ["score", "duration", "coupon"]
    for j, source in enumerate("BCD"):
        c = col(start3 + j)
        ws.Cells(1, start3 + j).Value2 = f"z_{names_ridge[j]}"
        ws.Range(f"{c}2:{c}{last}").Formula = (f"=STANDARDIZE({source}2,AVERAGE({source}$2:{source}${last}),"
                                               f"STDEV.P({source}$2:{source}${last}))")
    ridge = f"${col(start3)}$2:${col(start3 + 2)}${last}"

    # spill columns for TREND fitted values and residuals
    spill = start3 + 4
    return {"n": n, "last": last, "levels": levels, "sectors": sectors, "bonds": bonds,
            "big": big, "names_big": names_big, "m3": m3, "names_m3": names_m3,
            "ridge": ridge, "names_ridge": names_ridge, "spill": spill,
            "oas": f"bench!$A$2:$A${last}", "score": f"bench!$B$2:$B${last}",
            "duration": f"bench!$C$2:$C${last}", "log_oas": f"bench!$G$2:$G${last}"}


def linest_rows(ref: Reference, model: str, y: str, x: str, names: list[str], extras: bool = False) -> str:
    """Rows for every LINEST statistic, named in statsmodels' order (const first). Returns the LINEST text."""
    k = len(names)
    linest = f"LINEST({y},{x},TRUE,TRUE)"
    order = ["const"] + names
    for i, name in enumerate(order):
        # LINEST returns the columns in reverse order with the intercept last
        c = k + 1 - i
        ref.add(model, f"coef_{name}", f"=INDEX({linest},1,{c})")
        ref.add(model, f"se_{name}", f"=INDEX({linest},2,{c})")
    ref.add(model, "r2", f"=INDEX({linest},3,1)")
    ref.add(model, "se_y", f"=INDEX({linest},3,2)")
    ref.add(model, "f", f"=INDEX({linest},4,1)")
    ref.add(model, "df_resid", f"=INDEX({linest},4,2)")
    ref.add(model, "ss_reg", f"=INDEX({linest},5,1)")
    ref.add(model, "ss_resid", f"=INDEX({linest},5,2)")
    if extras:
        for i, name in enumerate(order):
            c = k + 1 - i
            t = f"ABS(INDEX({linest},1,{c})/INDEX({linest},2,{c}))"
            ref.add(model, f"p_{name}", f"=T.DIST.2T({t},INDEX({linest},4,2))")
            half = f"T.INV.2T(0.05,INDEX({linest},4,2))*INDEX({linest},2,{c})"
            ref.add(model, f"ci_low_{name}", f"=INDEX({linest},1,{c})-{half}")
            ref.add(model, f"ci_high_{name}", f"=INDEX({linest},1,{c})+{half}")
    return linest


def bench_rows(ref: Reference, ws, b: dict) -> None:
    n, last = b["n"], b["last"]
    oas, score, log_oas = b["oas"], b["score"], b["log_oas"]
    # d01: the simple line and its errors in bp
    m = "d01_oas_on_score"
    ref.add(m, "slope", f"=SLOPE({oas},{score})")
    ref.add(m, "intercept", f"=INTERCEPT({oas},{score})")
    ref.add(m, "rsq", f"=RSQ({oas},{score})")
    ref.add(m, "correl", f"=CORREL({oas},{score})")
    fitted = f"(INTERCEPT({oas},{score})+SLOPE({oas},{score})*{score})"
    ref.add(m, "mae_bp", f"=AVERAGE(ABS({oas}-{fitted}))")
    ref.add(m, "rmse_bp", f"=SQRT(SUMXMY2({oas},{fitted})/COUNT({oas}))")

    # d02: two features, then rating and sector dummies with adjusted R-squared
    linest_rows(ref, "d02_oas_on_score_duration", oas, f"bench!$B$2:$C${last}", ["score", "duration"])
    big = f"bench!{b['big']}"
    linest = linest_rows(ref, "d02_oas_on_rating_duration_sector", oas, big, b["names_big"])
    k = len(b["names_big"])
    ref.add("d02_oas_on_rating_duration_sector", "adj_r2",
            f"=1-(1-INDEX({linest},3,1))*(ROWS({oas})-1)/(ROWS({oas})-{k}-1)")
    for name in b["names_big"]:
        if name != "duration":
            column = b["names_big"].index(name) + 10
            ref.add("d02_dummy_counts", f"count_{name}", f"=SUM(bench!{col(column)}2:{col(column)}{last})")

    # d03: inference on the log model, and VIF by 1/(1-R2)
    m3 = f"bench!{b['m3']}"
    names = b["names_m3"]
    linest_rows(ref, "d03_log_oas_on_score_duration_sector", log_oas, m3, names, extras=True)
    for j, name in enumerate(names, start=1):
        others = ",".join(str(i) for i in range(1, len(names) + 1) if i != j)
        aux = f"LINEST(CHOOSECOLS({m3},{j}),CHOOSECOLS({m3},{others}),TRUE,TRUE)"
        ref.add("d03_vif", f"vif_rsq_{name}", f"=INDEX({aux},3,1)")
        ref.add("d03_vif", f"vif_{name}", f"=1/(1-INDEX({aux},3,1))")

    # d04: the log model on rating, duration, sector; Breusch-Pagan by hand; Q-Q points
    linest_rows(ref, "d04_log_oas_on_rating_duration_sector", log_oas, big, b["names_big"])
    spill = b["spill"]
    for offset, (label, y) in enumerate((("oas", oas), ("log_oas", log_oas))):
        fit_col, u2_col = col(spill + 3 * offset), col(spill + 3 * offset + 1)
        res_col = col(spill + 3 * offset + 2)
        ws.Range(f"{fit_col}2").Formula2 = f"=TREND({y},{big})"
        ws.Range(f"{res_col}2:{res_col}{last}").Formula = f"={'A' if label == 'oas' else 'G'}2-{fit_col}2"
        ws.Range(f"{u2_col}2:{u2_col}{last}").Formula = f"={res_col}2^2"
        u2 = f"bench!${u2_col}$2:${u2_col}${last}"
        model = f"d04_breusch_pagan_{label}_model"
        lm = f"ROWS({u2})*INDEX(LINEST({u2},{big},TRUE,TRUE),3,1)"
        ref.add(model, "lm", f"={lm}")
        ref.add(model, "lm_pvalue", f"=CHISQ.DIST.RT({lm},COLUMNS({big}))")
        if label == "log_oas":
            r = f"bench!${res_col}$2:${res_col}${last}"
            qq = "d04_qq_log_oas_model"
            ref.add(qq, "theoretical_at_min_residual", f"=NORM.S.INV((RANK.EQ(MIN({r}),{r},1)-0.5)/COUNT({r}))")
            ref.add(qq, "theoretical_at_max_residual", f"=NORM.S.INV((RANK.EQ(MAX({r}),{r},1)-0.5)/COUNT({r}))")
            ref.add(qq, "theoretical_at_first_bond",
                    f"=NORM.S.INV((RANK.EQ(bench!${res_col}$2,{r},1)-0.5)/COUNT({r}))")
            ref.add(qq, "residual_first_bond", f"=bench!${res_col}$2")

    # d05: the sample against population standard deviation, and ridge in closed form
    d = b["duration"]
    ref.add("d05_standardize", "stdev_s_duration", f"=STDEV.S({d})")
    ref.add("d05_standardize", "stdev_p_duration", f"=STDEV.P({d})")
    ref.add("d05_standardize", "ratio_s_to_p", f"=STDEV.S({d})/STDEV.P({d})")
    z = f"bench!{b['ridge']}"
    beta = (f"MMULT(MINVERSE(MMULT(TRANSPOSE({z}),{z})+{RIDGE_ALPHA}*MUNIT(COLUMNS({z}))),"
            f"MMULT(TRANSPOSE({z}),{log_oas}-AVERAGE({log_oas})))")
    model = f"d05_ridge_alpha{RIDGE_ALPHA}_log_oas_on_score_duration_coupon"
    ref.add(model, "intercept", f"=AVERAGE({log_oas})")
    for i, name in enumerate(b["names_ridge"], start=1):
        ref.add(model, f"coef_{name}", f"=INDEX({beta},{i},1)")


def check_formula_vs_formula2(ws, app, b: dict) -> None:
    oas, score = b["oas"], b["score"]
    text = f"=AVERAGE(ABS({oas}-(INTERCEPT({oas},{score})+SLOPE({oas},{score})*{score})))"
    ws.Range("A1").Formula = text
    ws.Range("A2").Formula2 = text
    app.Calculate()
    print(f"  =AVERAGE(ABS(a-b)) set with Formula (as pre-dynamic-array Excel reads it): stored as "
          f"{ws.Range('A1').Formula2[:40]}..., value {shown(ws.Range('A1').Value2)}; with Formula2 (as typed in this "
          f"Excel): value {shown(ws.Range('A2').Value2)}")
    ws.Cells.Clear()


def card_sheet(ws) -> int:
    card = read_csv("credit_card_default.csv")
    n = len(card)
    # A default, B PAY_0, C LIMIT_BAL, D LIMIT_BAL per 10,000
    ws.Range("A1:D1").Value2 = [["default", "PAY_0", "LIMIT_BAL", "LIMIT_BAL_10k"]]
    write_block(ws, 2, 1, [[float(r[TARGET]), float(r["PAY_0"]), float(r["LIMIT_BAL"])] for r in card])
    last = n + 1
    ws.Range(f"D2:D{last}").Formula = "=C2/10000"
    # model 1 on PAY_0: coefficients in H1:H2, probability E, log-likelihood F, sum in H3
    ws.Range("H1:H2").Value2 = [[0.0], [0.0]]
    ws.Range(f"E2:E{last}").Formula = "=1/(1+EXP(-($H$1+$H$2*B2)))"
    ws.Range(f"F2:F{last}").Formula = "=A2*LN(E2)+(1-A2)*LN(1-E2)"
    ws.Range("H3").Formula = f"=SUM(F2:F{last})"
    # model 2 on PAY_0 and LIMIT_BAL per 10,000: coefficients in K1:K3, probability I, log-likelihood J, sum K4
    ws.Range("K1:K3").Value2 = [[0.0], [0.0], [0.0]]
    ws.Range(f"I2:I{last}").Formula = "=1/(1+EXP(-($K$1+$K$2*B2+$K$3*D2)))"
    ws.Range(f"J2:J{last}").Formula = "=A2*LN(I2)+(1-A2)*LN(1-I2)"
    ws.Range("K4").Formula = f"=SUM(J2:J{last})"
    return last


SOLVER_OPTIONS = dict(MaxTime=600, Iterations=10000, Precision=1e-6, AssumeLinear=False, StepThru=False,
                      Estimates=1, Derivatives=2, SearchOption=1, IntTolerance=1, Scaling=True, Convergence=1e-10,
                      AssumeNonNeg=False)


def solve(app, wb, target: str, changing: str, options: bool) -> int:
    run = lambda name, *args: app.Run(f"'{wb.Name}'!{name}", *args)  # noqa: E731
    run("SolverReset")
    if options:
        run("SolverOptions", *SOLVER_OPTIONS.values())
    # SetCell, MaxMinVal (1 is max), ValueOf, ByChange, Engine (1 is GRG Nonlinear), EngineDesc
    run("SolverOk", target, 1, 0, changing, 1, "GRG Nonlinear")
    return int(run("SolverSolve", True))


def card_rows(ref: Reference, ws, app, solver_wb, last: int) -> None:
    app.Calculation = XL_AUTOMATIC
    ws.Activate()
    # Solver with its default options first: the non-negative box is ticked by default
    result = solve(app, solver_wb, "$H$3", "$H$1:$H$2", options=False)
    print(f"  Solver, default options, default on PAY_0: returned {result}, intercept {ws.Range('H1').Value2!r}, "
          f"slope {ws.Range('H2').Value2!r}, log-likelihood {ws.Range('H3').Value2!r}")
    ws.Range("H1:H2").Value2 = [[0.0], [0.0]]
    described = ("Solver GRG Nonlinear from 0: maximise {target} by changing {changing}; options "
                 + ", ".join(f"{k} {v}" for k, v in SOLVER_OPTIONS.items()) + "; returned {result}")
    for target, changing, cells, model, names, prob in (
            ("$H$3", "$H$1:$H$2", ["H1", "H2"], "d06_logit_default_on_pay0", ["const", "PAY_0"], "E"),
            ("$K$4", "$K$1:$K$3", ["K1", "K2", "K3"], "d06_logit_default_on_pay0_limit10k",
             ["const", "PAY_0", "LIMIT_BAL_10k"], "I")):
        result = solve(app, solver_wb, target, changing, options=True)
        if result not in (0, 1, 2):
            raise RuntimeError(f"Solver returned {result} for {model}")
        note = described.format(target=target, changing=changing, result=result)
        for cell, name in zip(cells, names):
            ref.keep(model, f"coef_{name}", note, ws.Range(cell).Value2)
        sum_cell = target.replace("$", "")
        ref.keep(model, "loglik", f"{ws.Range(sum_cell).Formula} at Solver's coefficients",
                 ws.Range(sum_cell).Value2)
        for cell, name in zip(cells[1:], names[1:]):
            ref.add(model, f"odds_ratio_{name}", f"=EXP(card!{cell})")
        print(f"  Solver, non-negative off, {model}: returned {result}, coefficients "
              f"{[ws.Range(c).Value2 for c in cells]}, log-likelihood {ws.Range(sum_cell).Value2!r}")
    app.Calculation = XL_MANUAL

    # d07: the confusion matrix at 0.5 on the PAY_0 model's probabilities, flagged when at least the threshold
    a, p = f"card!$A$2:$A${last}", f"card!$E$2:$E${last}"
    m = "d07_confusion_pay0_at_0.5"
    counts = {"tn": f'COUNTIFS({a},0,{p},"<0.5")', "fp": f'COUNTIFS({a},0,{p},">=0.5")',
              "fn": f'COUNTIFS({a},1,{p},"<0.5")', "tp": f'COUNTIFS({a},1,{p},">=0.5")'}
    for name, formula in counts.items():
        ref.add(m, name, f"={formula}")
    tp, fp, fn, tn = counts["tp"], counts["fp"], counts["fn"], counts["tn"]
    ref.add(m, "precision", f"={tp}/({tp}+{fp})")
    ref.add(m, "recall", f"={tp}/({tp}+{fn})")
    ref.add(m, "accuracy", f"=({tp}+{tn})/ROWS({a})")
    ref.add(m, "f1", f"=2*{tp}/(2*{tp}+{fp}+{fn})")

    # d08: ROC points at each distinct probability (high to low), AUC by the trapezoid rule
    # row 2 holds the starting point (0, 0); the thresholds spill from M3, highest first
    ws.Range("M1:O1").Value2 = [["threshold", "fpr", "tpr"]]
    ws.Range("N2:O2").Value2 = [[0.0, 0.0]]
    ws.Range("M3").Formula2 = f"=SORT(UNIQUE({p}),,-1)"
    app.Calculate()
    top = 3
    bottom = top + ws.Range("M3").SpillingToRange.Rows.Count - 1
    ws.Range(f"N{top}:N{bottom}").Formula = f'=COUNTIFS({a},0,{p},">="&M{top})/COUNTIF({a},0)'
    ws.Range(f"O{top}:O{bottom}").Formula = f'=COUNTIFS({a},1,{p},">="&M{top})/COUNTIF({a},1)'
    auc = (f"=SUMPRODUCT((card!$N$3:$N${bottom}-card!$N$2:$N${bottom - 1}),"
           f"(card!$O$3:$O${bottom}+card!$O$2:$O${bottom - 1})/2)")
    ref.add("d08_roc_pay0", "n_thresholds", f"=ROWS(card!$M$3#)")
    ref.add("d08_roc_pay0", "auc_trapezoid", auc)
    ref.add("d08_roc_pay0", "last_fpr", f"=card!$N${bottom}")
    ref.add("d08_roc_pay0", "last_tpr", f"=card!$O${bottom}")


def sklearn_fits() -> dict:
    result = subprocess.run([str(VENV_PYTHON), "-c", SKLEARN_HELPER, str(DATA)], capture_output=True, text=True,
                            check=True)
    return json.loads(result.stdout)


def nested_if(nodes: list[dict], i: int, row: int, columns: dict) -> str:
    node = nodes[i]
    if node["left"] == -1:
        return str(node["leaf_class"])
    cell = f"{columns[node['feature']]}{row}"
    return (f"IF({cell}<={node['threshold']!r},{nested_if(nodes, node['left'], row, columns)},"
            f"{nested_if(nodes, node['right'], row, columns)})")


def check_tree(ws, app, fits: dict) -> None:
    card = read_csv("credit_card_default.csv")
    used = sorted({n["feature"] for n in fits["nodes"] if n["feature"]})
    columns = {name: col(i + 1) for i, name in enumerate(used)}
    positions = fits["valid_positions"]
    write_block(ws, 1, 1, [used])
    write_block(ws, 2, 1, [[float(card[p][name]) for name in used] for p in positions])
    flag_col = col(len(used) + 2)
    last = len(positions) + 1
    formula = "=" + nested_if(fits["nodes"], 0, 2, columns)
    ws.Range(f"{flag_col}2:{flag_col}{last}").Formula = formula
    app.Calculate()
    excel = [int(v[0]) for v in ws.Range(f"{flag_col}2:{flag_col}{last}").Value2]
    agree = sum(e == s for e, s in zip(excel, fits["valid_flags"]))
    print(f"  depth-2 tree as nested IF, first row {ws.Range(f'{flag_col}2').Formula}: agrees with the tree's flags "
          f"on {agree} of {len(positions)} validation rows: {'ok' if agree == len(positions) else 'DIFFERS'}")
    ws.Cells.Clear()


def check_rolling_slope(ws, app) -> None:
    rows = read_csv("treasury_par_yields.csv")
    dates = [r["date"] for r in rows]
    write_block(ws, 2, 1, [[float(r["10 Yr"]), float(r["30 Yr"])] for r in rows])
    last = len(rows) + 1
    ws.Range(f"C3:C{last}").Formula = "=(A3-A2)*100"
    ws.Range(f"D3:D{last}").Formula = "=(B3-B2)*100"
    first = 3 + 251
    ws.Range(f"E{first}:E{last}").Formula = f"=SLOPE(OFFSET(D{first},-251,0,252,1),OFFSET(C{first},-251,0,252,1))"
    app.Calculate()
    excel = np.array([v[0] for v in ws.Range(f"E{first}:E{last}").Value2])
    ten = np.array([float(r["10 Yr"]) for r in rows])
    thirty = np.array([float(r["30 Yr"]) for r in rows])
    dx, dy = np.diff(ten) * 100, np.diff(thirty) * 100
    fits = np.array([np.polyfit(dx[i - 251:i + 1], dy[i - 251:i + 1], 1)[0] for i in range(251, len(dx))])
    gap = float(np.abs(excel - fits).max())
    lo, hi = int(np.argmin(excel)), int(np.argmax(excel))
    print(f"  rolling 252-row beta of 30 Yr on 10 Yr changes, {ws.Range(f'E{first}').Formula}: {len(excel)} windows, "
          f"largest gap to np.polyfit on each trailing window {gap:.1e}; lowest {excel[lo]:.3f} on "
          f"{dates[first - 2 + lo]}, highest {excel[hi]:.3f} on {dates[first - 2 + hi]}: "
          f"{'ok' if gap < 1e-9 else 'DIFFERS'}")
    ws.Cells.Clear()


def check_kmeans_and_profile(workbook, ws, app, fits: dict) -> None:
    ratings = {row["rating"]: float(row["score"]) for row in read_csv("ratings.csv")}
    bonds = read_csv("benchmark.csv")
    n, last = len(bonds), len(bonds) + 1
    ws.Range("A1:E1").Value2 = [["log_oas", "duration", "coupon", "score", "oas"]]
    write_block(ws, 2, 1, [[math.log(float(b["oas"])), float(b["duration"]), float(b["coupon"]),
                            ratings[b["rating"]], float(b["oas"])] for b in bonds])
    # scaled with the population standard deviation, as StandardScaler
    for j, source in enumerate("ABCD"):
        c = col(7 + j)
        ws.Range(f"{c}2:{c}{last}").Formula = (f"=STANDARDIZE({source}2,AVERAGE({source}$2:{source}${last}),"
                                               f"STDEV.P({source}$2:{source}${last}))")
    write_block(ws, 1, 20, fits["centres"])  # centres in T1:W4
    for k in range(4):
        c = col(12 + k)
        ws.Range(f"{c}2:{c}{last}").Formula = f"=SQRT(SUMXMY2($G2:$J2,$T${k + 1}:$W${k + 1}))"
    ws.Range(f"P2:P{last}").Formula = "=MATCH(MIN(L2:O2),L2:O2,0)-1"
    app.Calculate()
    excel = [int(v[0]) for v in ws.Range(f"P2:P{last}").Value2]
    agree = sum(e == s for e, s in zip(excel, fits["labels"]))
    print(f"  K-means k=4 on scaled log_oas, duration, coupon, score: {ws.Range('L2').Formula} and "
          f"{ws.Range('P2').Formula} give the label of {agree} of {n} bonds: {'ok' if agree == n else 'DIFFERS'}")

    # a pivot table of the profile: count and average work; a pivot has no median, MEDIAN(IF(...)) does
    # the pivot's source: a table with a header on every column, in Y to AA
    write_block(ws, 1, 25, [["cluster", "oas", "duration"]])
    write_block(ws, 2, 25, [[float(lab), float(bonds[i]["oas"]), float(bonds[i]["duration"])]
                            for i, lab in enumerate(fits["labels"])])
    source = ws.Range(f"Y1:AA{last}")
    target = workbook.Worksheets.Add()
    cache = workbook.PivotCaches().Create(1, source)
    pivot = cache.CreatePivotTable(target.Range("A3"), "profile")
    pivot.PivotFields("cluster").Orientation = 1
    pivot.AddDataField(pivot.PivotFields("oas"), "Count of oas", -4112)  # xlCount
    pivot.AddDataField(pivot.PivotFields("duration"), "Average of duration", -4106)  # xlAverage
    pivot.DataPivotField.Orientation = 2
    app.Calculate()
    body = pivot.DataBodyRange.Value2
    labels = fits["labels"]
    worst_avg, counts_ok = 0.0, True
    for k in range(4):
        members = [i for i, lab in enumerate(labels) if lab == k]
        counts_ok &= body[k][0] == len(members)
        mean = sum(float(bonds[i]["duration"]) for i in members) / len(members)
        worst_avg = max(worst_avg, abs(body[k][1] - mean))
    for k in range(4):
        target.Cells(k + 1, 10).Formula2 = f"=MEDIAN(IF({ws.Name}!$Y$2:$Y${last}={k},{ws.Name}!$Z$2:$Z${last}))"
    app.Calculate()
    medians_ok = all(target.Cells(k + 1, 10).Value2 == float(np.median(
        [float(bonds[i]["oas"]) for i, lab in enumerate(labels) if lab == k])) for k in range(4))
    print(f"  pivot table by cluster: Count of oas equals the cluster sizes: {counts_ok}; Average of duration within "
          f"{worst_avg:.1e} of the mean; a pivot's Summarize Values By list has no median; "
          f"{target.Cells(1, 10).Formula2} equals the median oas in bp of each cluster: {medians_ok}")
    app.DisplayAlerts = False
    target.Delete()
    ws.Cells.Clear()


def check_pca(ws, app) -> None:
    rows = read_csv("treasury_par_yields.csv")
    levels = np.array([[float(r[t]) for t in TENORS] for r in rows])
    write_block(ws, 1, 1, [TENORS])
    write_block(ws, 2, 1, levels.tolist())
    last = len(rows) + 1
    m = len(TENORS)
    # daily changes in bp in columns J onward, rows 3 to last
    for j in range(m):
        c, source = col(10 + j), col(1 + j)
        ws.Range(f"{c}3:{c}{last}").Formula = f"=({source}3-{source}2)*100"
    changes = np.diff(levels, axis=0) * 100
    cov_python = np.cov(changes, rowvar=False, ddof=1)
    for i in range(m):
        for j in range(m):
            a, b = col(10 + i), col(10 + j)
            ws.Cells(1 + i, 30 + j).Formula = f"=COVARIANCE.S({a}$3:{a}${last},{b}$3:{b}${last})"
    app.Calculate()
    cov_excel = np.array(ws.Range(ws.Cells(1, 30), ws.Cells(m, 29 + m)).Value2)
    cov_gap = float(np.abs(cov_excel - cov_python).max())
    # loadings from the covariance matrix: largest variance first, each column's loadings summing to a positive number
    values, vectors = np.linalg.eigh(cov_python)
    order = np.argsort(values)[::-1][:3]
    loadings = vectors[:, order]
    loadings *= np.where(loadings.sum(axis=0) < 0, -1.0, 1.0)
    write_block(ws, 12, 30, loadings.tolist())  # AD12 down, 8 rows by 3 columns
    change_cols = f"{col(10)}3:{col(9 + m)}{last}"
    loads = f"$AD$12:${col(32)}${11 + m}"
    # raw scores spill from AM3, centred scores from AQ3
    ws.Range("AM3").Formula2 = f"=MMULT({change_cols},{loads})"
    means = f"BYCOL({change_cols},LAMBDA(c,AVERAGE(c)))"
    ws.Range("AQ3").Formula2 = f"=MMULT({change_cols}-{means},{loads})"
    app.Calculate()
    raw = np.array(ws.Range("AM3").SpillingToRange.Value2)
    centred = np.array(ws.Range("AQ3").SpillingToRange.Value2)
    python_scores = (changes - changes.mean(axis=0)) @ loadings
    gap_centred = float(np.abs(centred - python_scores).max())
    shift = float(np.abs(raw - python_scores).max())
    print(f"  COVARIANCE.S matrix of daily changes in bp, {m} tenors: largest gap to np.cov(ddof=1) {cov_gap:.1e}")
    print(f"  scores by {ws.Range('AQ3').Formula2[:60]}... (changes less each column's mean, times the loadings): "
          f"largest gap to the centred projection {gap_centred:.1e}; MMULT of the raw changes differs by up to "
          f"{shift:.3f} bp, the column means times the loadings: {'ok' if gap_centred < 1e-9 else 'DIFFERS'}")
    ws.Cells.Clear()


def write_csv(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else DATA
    fits = sklearn_fits()
    ref = Reference()
    app = win32com.client.DispatchEx("Excel.Application")
    try:
        app.Visible = False
        app.DisplayAlerts = False
        _, pid = win32process.GetWindowThreadProcessId(app.Hwnd)
        print(f"Excel {app.Version}, build {app.Build:.0f}, {app.OperatingSystem}, process id {pid}")
        workbook = app.Workbooks.Add()
        solver_wb = app.Workbooks.Open(str(Path(app.LibraryPath) / "SOLVER" / "SOLVER.XLAM"))
        workbook.Activate()
        app.Calculation = XL_MANUAL
        sheets = {}
        for name in ("calc", "bench", "card", "scratch"):
            sheets[name] = workbook.Worksheets.Add()
            sheets[name].Name = name
        b = bench_sheet(sheets["bench"])
        bench_rows(ref, sheets["bench"], b)
        app.Calculate()
        ref.evaluate(sheets["calc"], app)
        last = card_sheet(sheets["card"])
        app.Calculate()
        card_rows(ref, sheets["card"], app, solver_wb, last)
        ref.evaluate(sheets["calc"], app)
        print("Behaviour checks:")
        check_formula_vs_formula2(sheets["scratch"], app, b)
        check_tree(sheets["scratch"], app, fits)
        check_rolling_slope(sheets["scratch"], app)
        check_kmeans_and_profile(workbook, sheets["scratch"], app, fits)
        check_pca(sheets["scratch"], app)
        workbook.Close(SaveChanges=False)
        solver_wb.Close(SaveChanges=False)
    finally:
        app.Quit()

    ids = [row["case_id"] for row in ref.rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("case_id values are not unique")
    write_csv(out / OUT_NAME, ref.rows)
    print(f"{OUT_NAME}: {len(ref.rows)} rows")


if __name__ == "__main__":
    main()
