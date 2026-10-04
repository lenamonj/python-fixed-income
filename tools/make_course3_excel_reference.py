"""Generate the Excel reference values that the Course 3 tests read, and check the Excel behaviours Course 3 states.

The script drives desktop Excel for Windows through COM, has Excel compute every value, and writes:

- data/course3_excel_reference.csv   one row per market date of 2026 in treasury_par_yields.csv (190): the input
                                      yields and, computed by Excel, the 10 Yr daily change in bp, its 21-row
                                      STDEV.S and that times SQRT(252), the 63-row AVERAGE of the 10 Yr, 2s10s and
                                      2s5s10s in bp, the 252-row STANDARDIZE, COUNTIF/COUNT*100, and PERCENTRANK.INC
                                      of the 10 Yr and of 2s10s, and the one-month as-of change, each with the exact
                                      formula text Excel evaluated in that row

The windows reach back into 2025 and 2024 rows that are written to the sheet but not to the CSV. Each formula is
written once in the first 2026 row and filled down with Range.FillDown, so every window is a fixed-size relative
range, as a student would fill it. Nothing is typed by hand: every output value is read back from an Excel cell
with Value2 and written with repr. Running it twice gives byte-identical files.

It also prints the Excel version and build and re-checks the Excel behaviours that the CSV does not carry:
ENCODEURL, VALUE and IFERROR on FRED's ".", WEEKDAY, a pivot table grouped by month, SUMIFS, COUNTIFS, AVERAGEIFS
and SUMPRODUCT on holdings.csv, and Power Query From File on the FRED-format JSON sample, Append, and Merge. With
--web it also runs Power Query From Web on FRED's key-free fredgraph.csv download (network, no key; prints only
the row count, the header, and the first and last date, and stores nothing).

Yields are in percent and changes, slopes, and flies in basis points, as in COURSE3_SPEC.md.

Author tool: Windows with desktop Excel, and Python with pywin32. Not part of the course requirements.
Usage (from the repo root):  python tools/make_course3_excel_reference.py [--web]
"""
import csv
import shutil
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

import win32com.client

DATA = Path(__file__).resolve().parent.parent / "data"
EXCEL_EPOCH = date(1899, 12, 30)  # Excel serial 1 is 1900-01-01; right for every date after 1900-02-28
YEAR = "2026"
BACK_ROWS = 260  # rows written before the first 2026 row, enough for the 252-row windows and the one-month lookup
INPUTS = ["2 Yr", "5 Yr", "10 Yr", "30 Yr"]  # sheet columns B to E
FAKE_KEY = "fakefakefakefakefakefakefakefake"
ERRORS = {-2146826281: "#DIV/0!", -2146826246: "#N/A", -2146826259: "#NAME?", -2146826288: "#NULL!",
          -2146826252: "#NUM!", -2146826265: "#REF!", -2146826273: "#VALUE!"}

# output columns: (name, sheet column, formula for sheet row r with {r} and friends filled in, first data row offset)
# offsets: "all" fills from the second data row, "out" from the first 2026 row
OUTPUTS = [
    ("chg_10y_bp", "F", "=(D{r}-D{p})*100", "all"),
    ("vol21_10y_bp", "G", "=STDEV.S(F{r20}:F{r})", "out"),
    ("vol21_10y_annual_bp", "H", "=G{r}*SQRT(252)", "out"),
    ("mean63_10y_pct", "I", "=AVERAGE(D{r62}:D{r})", "out"),
    ("slope_2s10s_bp", "J", "=(D{r}-B{r})*100", "all"),
    ("fly_2s5s10s_bp", "K", "=(2*C{r}-B{r}-D{r})*100", "out"),
    ("zscore252_10y", "L", "=STANDARDIZE(D{r},AVERAGE(D{r251}:D{r}),STDEV.S(D{r251}:D{r}))", "out"),
    ("zscore252_2s10s", "M", "=STANDARDIZE(J{r},AVERAGE(J{r251}:J{r}),STDEV.S(J{r251}:J{r}))", "out"),
    ("pctrank252_10y", "N", '=COUNTIF(D{r251}:D{r},"<="&D{r})/COUNT(D{r251}:D{r})*100', "out"),
    ("pctrank252_2s10s", "O", '=COUNTIF(J{r251}:J{r},"<="&J{r})/COUNT(J{r251}:J{r})*100', "out"),
    ("percentrank_inc252_10y", "P", "=PERCENTRANK.INC(D{r251}:D{r},D{r})", "out"),
    ("percentrank_inc252_2s10s", "Q", "=PERCENTRANK.INC(J{r251}:J{r},J{r})", "out"),
    ("chg1m_10y_bp", "R", "=(D{r}-XLOOKUP(EDATE(A{r},-1),$A$2:$A${last},$D$2:$D${last},,-1))*100", "out"),
]
COLUMNS = ["date"] + INPUTS + [name for name, *_ in OUTPUTS] + [f"{name}_formula" for name, *_ in OUTPUTS]


def serial(d: date) -> int:
    return (d - EXCEL_EPOCH).days


def from_serial(value: float) -> date:
    return EXCEL_EPOCH + timedelta(days=int(value))


def shown(value) -> str:
    """A value read back with Value2: an Excel error by name, otherwise repr."""
    if isinstance(value, int) and value in ERRORS:
        return ERRORS[value]
    if value is None:
        return "an empty cell"
    return repr(value)


def read_treasury() -> list[dict]:
    with open(DATA / "treasury_par_yields.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_reference(ws, app) -> list[dict]:
    rows = read_treasury()
    first_out = next(i for i, row in enumerate(rows) if row["date"].startswith(YEAR))
    sheet_rows = rows[first_out - BACK_ROWS:]
    last = len(sheet_rows) + 1  # header in row 1, data in rows 2 to last
    r0 = BACK_ROWS + 2  # the sheet row of the first 2026 date
    ws.Range("A1:E1").Value2 = [["date"] + INPUTS]
    ws.Range(ws.Cells(2, 1), ws.Cells(last, 5)).Value2 = [
        [serial(date.fromisoformat(row["date"]))] + [float(row[c]) for c in INPUTS] for row in sheet_rows]
    for name, column, template, start in OUTPUTS:
        top = 3 if start == "all" else r0
        formula = template.format(r=top, p=top - 1, r20=top - 20, r62=top - 62, r251=top - 251, last=last)
        ws.Range(f"{column}{top}").Formula = formula
        ws.Range(f"{column}{top}:{column}{last}").FillDown()
    app.Calculate()

    out_range = ws.Range(ws.Cells(r0, 1), ws.Cells(last, 18))
    values, formulas = out_range.Value2, out_range.Formula
    result = []
    for value_row, formula_row in zip(values, formulas):
        row = {"date": from_serial(value_row[0]).isoformat()}
        row |= {c: repr(v) for c, v in zip(INPUTS, value_row[1:5])}
        for k, (name, *_rest) in enumerate(OUTPUTS):
            value = value_row[5 + k]
            if not isinstance(value, float):
                raise RuntimeError(f"Excel returned {shown(value)} for {name} on {row['date']}")
            row[name] = repr(value)
            row[f"{name}_formula"] = formula_row[5 + k]
        result.append(row)
    ws.Cells.Clear()
    if len(result) != sum(row["date"].startswith(YEAR) for row in rows):
        raise RuntimeError("the reference does not hold one row per 2026 market date")
    return result


def evaluate(ws, app, formulas: list[str]) -> list:
    rng = ws.Range(ws.Cells(1, 1), ws.Cells(len(formulas), 1))
    rng.Formula = [[f] for f in formulas]
    app.Calculate()
    values = [row[0] for row in rng.Value2]
    ws.Cells.Clear()
    return values


def report(label: str, got, expected) -> None:
    print(f"  {label}: {got!r}: {'ok' if got == expected else 'DIFFERS, expected ' + repr(expected)}")


def check_encodeurl(ws, app) -> None:
    ws.Range("A1").Value2 = "DGS10"
    ws.Range("B1").Value2 = FAKE_KEY
    ws.Range("C1").Value2 = "'2015-01-01"
    ws.Range("D1").Formula = ('="https://api.stlouisfed.org/fred/series/observations?series_id="&A1&"&api_key="&B1'
                              '&"&file_type=json&observation_start="&ENCODEURL(C1)')
    ws.Range("D2").Formula = '=ENCODEURL("a b&c=d/e?f")'
    ws.Range("D3").Formula = '=ENCODEURL(C1)'
    app.Calculate()
    report(f"a request URL built with & and ENCODEURL, formula {ws.Range('D1').Formula}", ws.Range("D1").Value2,
           f"https://api.stlouisfed.org/fred/series/observations?series_id=DGS10&api_key={FAKE_KEY}"
           "&file_type=json&observation_start=2015-01-01")
    report('=ENCODEURL("a b&c=d/e?f")', ws.Range("D2").Value2, "a%20b%26c%3Dd%2Fe%3Ff")
    report("=ENCODEURL(C1) with C1 the text 2015-01-01", ws.Range("D3").Value2, "2015-01-01")
    ws.Cells.Clear()


def check_value_dot(ws, app) -> None:
    ws.Range("B1").Value2 = "value"
    ws.Range("B2").Value2 = "."  # stored as text, as FRED's "." arrives
    ws.Range("B3").Value2 = 4.23
    ws.Range("B4").Value2 = "'4.25"  # a number that arrived as text (the apostrophe keeps it text, as a typed '4.25)
    formulas = {"D1": '=VALUE(".")', "D2": "=VALUE(B2)", "D3": "=IFERROR(VALUE(B2),NA())",
                "D4": "=IFERROR(VALUE(B4),NA())", "D5": "=ISNUMBER(B2)", "D6": "=B3-B2",
                "D7": "=AVERAGE(B2:B4)", "D8": "=COUNT(B2:B4)", "D9": "=SUM(B2:B4)", "D10": "=ISNA(D3)"}
    for cell, formula in formulas.items():
        ws.Range(cell).Formula = formula
    app.Calculate()
    expected = {"D1": "#VALUE!", "D2": "#VALUE!", "D3": "#N/A", "D4": repr(4.25), "D5": repr(False),
                "D6": "#VALUE!", "D7": repr(4.23), "D8": repr(1.0), "D9": repr(4.23), "D10": repr(True)}
    note = "B2 the text '.', B3 the number 4.23, B4 the text '4.25'"
    for cell, formula in formulas.items():
        got = shown(ws.Range(cell).Value2)
        print(f"  {formula} ({note}): {got}: {'ok' if got == expected[cell] else 'DIFFERS, expected ' + expected[cell]}")
    ws.Cells.Clear()


def check_weekday(ws, app) -> None:
    days = [("2026-09-04", 5, 6), ("2026-09-05", 6, 7), ("2026-09-06", 7, 1), ("2026-09-07", 1, 2), ("2026-10-02", 5, 6)]
    formulas = []
    for day, _, _ in days:
        d = date.fromisoformat(day)
        formulas += [f"=WEEKDAY(DATE({d.year},{d.month},{d.day}),2)", f"=WEEKDAY(DATE({d.year},{d.month},{d.day}))"]
    values = evaluate(ws, app, formulas)
    for i, (day, monday_one, sunday_one) in enumerate(days):
        got = (values[2 * i], values[2 * i + 1])
        ok = got == (float(monday_one), float(sunday_one))
        print(f"  {day}: WEEKDAY(date,2) {got[0]!r} (Monday 1 to Sunday 7), WEEKDAY(date) {got[1]!r} (Sunday 1): "
              f"{'ok' if ok else 'DIFFERS'}")
    flags = evaluate(ws, app, [f"=WEEKDAY(DATE(2026,9,{d}),2)>5" for d in (4, 5, 6, 7)])
    report("=WEEKDAY(date,2)>5 for 2026-09-04 to 2026-09-07 (TRUE on a weekend)", flags, [False, True, True, False])


def check_pivot_by_month(workbook, app) -> None:
    rows = [row for row in read_treasury() if row["date"].startswith(YEAR)]
    source = workbook.Worksheets.Add()
    source.Range("A1:B1").Value2 = [["date", "ten_yr_pct"]]
    source.Range(source.Cells(2, 1), source.Cells(len(rows) + 1, 2)).Value2 = [
        [serial(date.fromisoformat(row["date"])), float(row["10 Yr"])] for row in rows]
    source.Range(f"A2:A{len(rows) + 1}").NumberFormat = "yyyy-mm-dd"
    target = workbook.Worksheets.Add()
    cache = workbook.PivotCaches().Create(1, source.Range(f"A1:B{len(rows) + 1}"))  # 1 is xlDatabase
    pivot = cache.CreatePivotTable(target.Range("A3"), "by_month")
    pivot.PivotFields("date").Orientation = 1  # xlRowField
    # group the dates by month only: Periods is seconds, minutes, hours, days, months, quarters, years
    pivot.PivotFields("date").DataRange.Cells(1).Group(True, True, None, (False, False, False, False, True, False, False))
    pivot.AddDataField(pivot.PivotFields("date"), "Last date", -4136)  # xlMax
    pivot.AddDataField(pivot.PivotFields("ten_yr_pct"), "Max 10 Yr", -4136)
    pivot.DataPivotField.Orientation = 2  # the two value fields side by side, as columns
    app.Calculate()
    body = pivot.DataBodyRange.Value2
    labels = [row[0] for row in pivot.RowRange.Value2][1:]
    months = sorted({row["date"][:7] for row in rows})
    last_rows = {m: [row for row in rows if row["date"][:7] == m][-1] for m in months}
    highest = {m: max(float(row["10 Yr"]) for row in rows if row["date"][:7] == m) for m in months}
    got_last = [from_serial(r[0]).isoformat() for r in body[:len(months)]]
    got_max = [r[1] for r in body[:len(months)]]
    want_last = [last_rows[m]["date"] for m in months]
    month_end_value = [float(last_rows[m]["10 Yr"]) for m in months]
    print(f"  pivot table on the 2026 10 Yr, dates grouped by month (row labels {labels[:3]} ...): Max of date "
          f"{got_last}: {'ok' if got_last == want_last else 'DIFFERS'} against the last market date of each month")
    differs = sum(a != b for a, b in zip(got_max, month_end_value))
    print(f"  the same pivot's Max of 10 Yr equals each month's highest value: "
          f"{'ok' if got_max == [highest[m] for m in months] else 'DIFFERS'}; it differs from the month-end value "
          f"in {differs} of {len(months)} months, so the month-end value needs MAXIFS and XLOOKUP")
    app.DisplayAlerts = False
    target.Delete()
    source.Delete()


def check_holdings_formulas(ws, app) -> None:
    with open(DATA / "holdings.csv", newline="", encoding="utf-8") as f:
        holdings = list(csv.DictReader(f))
    with open(DATA / "ratings.csv", newline="", encoding="utf-8") as f:
        grades = {row["rating"]: row["grade"] for row in csv.DictReader(f)}
    n = len(holdings)
    ws.Range("A1:E1").Value2 = [["sector", "rating", "oas", "market_value", "grade"]]
    ws.Range(ws.Cells(2, 1), ws.Cells(n + 1, 4)).Value2 = [
        [h["sector"], h["rating"], float(h["oas"]), float(h["market_value"])] for h in holdings]
    ws.Range("H1:I1").Value2 = [["rating", "grade"]]
    ws.Range(ws.Cells(2, 8), ws.Cells(len(grades) + 1, 9)).Value2 = [[r, g] for r, g in grades.items()]
    ws.Range(f"E2:E{n + 1}").Formula = f"=XLOOKUP(B2,$H$2:$H${len(grades) + 1},$I$2:$I${len(grades) + 1})"
    sectors = sorted({h["sector"] for h in holdings})
    formulas = []
    for i, sector in enumerate(sectors, start=1):
        ws.Cells(i, 11).Value2 = sector
        formulas.append((i, f"=COUNTIFS($A$2:$A${n + 1},K{i})", f"=SUMIFS($D$2:$D${n + 1},$A$2:$A${n + 1},K{i})",
                         f"=AVERAGEIFS($C$2:$C${n + 1},$A$2:$A${n + 1},K{i})"))
    for i, count_f, sum_f, avg_f in formulas:
        ws.Cells(i, 12).Formula, ws.Cells(i, 13).Formula, ws.Cells(i, 14).Formula = count_f, sum_f, avg_f
    app.Calculate()
    worst = {"COUNTIFS": 0.0, "SUMIFS": 0.0, "AVERAGEIFS": 0.0}
    for i, sector in enumerate(sectors, start=1):
        rows = [h for h in holdings if h["sector"] == sector]
        count, total = len(rows), sum(float(h["market_value"]) for h in rows)
        average = sum(float(h["oas"]) for h in rows) / count
        worst["COUNTIFS"] = max(worst["COUNTIFS"], abs(ws.Cells(i, 12).Value2 - count))
        worst["SUMIFS"] = max(worst["SUMIFS"], abs(ws.Cells(i, 13).Value2 - total))
        worst["AVERAGEIFS"] = max(worst["AVERAGEIFS"], abs(ws.Cells(i, 14).Value2 - average))
    print(f"  {len(sectors)} sectors of holdings.csv, {formulas[0][1]}, {formulas[0][2]}, {formulas[0][3]} against "
          f"counts, sums of market_value, and means of oas in Python: largest gaps {worst}: "
          f"{'ok' if worst['COUNTIFS'] == 0 and worst['SUMIFS'] < 0.005 and worst['AVERAGEIFS'] < 1e-9 else 'DIFFERS'}")
    # market-value weighted oas by grade, and COUNTIFS with two criteria
    for row, grade in ((1, "Investment Grade"), (2, "High Yield")):
        ws.Cells(row, 16).Value2 = grade
        ws.Cells(row, 17).Formula = (f"=SUMPRODUCT(($E$2:$E${n + 1}=P{row})*$C$2:$C${n + 1}*$D$2:$D${n + 1})"
                                     f"/SUMIFS($D$2:$D${n + 1},$E$2:$E${n + 1},P{row})")
        ws.Cells(row, 18).Formula = f"=COUNTIFS($E$2:$E${n + 1},P{row})"
        ws.Cells(row, 19).Formula = f'=COUNTIFS($E$2:$E${n + 1},P{row},$C$2:$C${n + 1},">200")'
    app.Calculate()
    for row, grade in ((1, "Investment Grade"), (2, "High Yield")):
        rows = [h for h in holdings if grades[h["rating"]] == grade]
        total = 0.0
        for h in rows:
            total += float(h["oas"]) * float(h["market_value"])
        weighted = total / sum(float(h["market_value"]) for h in rows)
        wide = sum(float(h["oas"]) > 200 for h in rows)
        got = (ws.Cells(row, 17).Value2, ws.Cells(row, 18).Value2, ws.Cells(row, 19).Value2)
        ok = abs(got[0] - weighted) < 1e-9 and got[1] == len(rows) and got[2] == wide
        print(f"  {grade}: {ws.Cells(row, 17).Formula} {got[0]!r} bp (Python {weighted!r}), COUNTIFS {got[1]:.0f} bonds, "
              f'COUNTIFS with oas ">200" {got[2]:.0f}: {"ok" if ok else "DIFFERS"}')
    ws.Cells.Clear()


def load_query(workbook, ws, name: str, formula: str) -> list:
    """Add a Power Query query with an M formula, load it to a table on ws, refresh, and return the values."""
    workbook.Queries.Add(name, formula)
    connection = f'OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location={name};Extended Properties=""'
    table = ws.ListObjects.Add(0, connection, None, 1, ws.Range("A1"))  # 0 is xlSrcExternal, 1 is xlYes (headers)
    table.QueryTable.CommandType = 2  # xlCmdSql
    table.QueryTable.CommandText = f"SELECT * FROM [{name}]"
    table.QueryTable.Refresh(False)
    values = table.Range.Value2
    table.Delete()
    return [list(row) for row in values]


def check_power_query(workbook, app) -> None:
    ws = workbook.Worksheets.Add()
    folder = Path(tempfile.mkdtemp(prefix="pfi_course3_pq_"))
    try:
        json_path = (DATA / "course3_fred_format_dgs10.json").as_posix()
        raw = load_query(workbook, ws, "fred_json", f'let Source = Json.Document(File.Contents("{json_path}")), '
                         'Rows = Table.FromRecords(Source[observations]) in Rows')
        dots = [row[2] for row in raw[1:] if row[3] == "."]
        print(f"  Power Query From File (Json.Document) on course3_fred_format_dgs10.json: header {raw[0]}, "
              f"{len(raw) - 1} rows, value read as text, '.' on {dots}: {'ok' if len(raw) - 1 == 43 and dots == ['2026-09-07'] else 'DIFFERS'}")
        typed = load_query(workbook, ws, "fred_json_typed", f'let Source = Json.Document(File.Contents("{json_path}")), '
                           'Rows = Table.FromRecords(Source[observations]), '
                           'Typed = Table.TransformColumnTypes(Rows, {{"date", type date}, {"value", type number}}, "en-US") '
                           'in Typed')
        dot_cell = [row[3] for row in typed[1:] if from_serial(row[2]).isoformat() == "2026-09-07"]
        print(f"  the same query with value changed to type number (Table.TransformColumnTypes, en-US): {len(typed) - 1} "
              f"rows loaded; the '.' row's value (an Error in Power Query) loads to the sheet as "
              f"{[shown(v) for v in dot_cell]}; first value {typed[1][3]!r}")
        cleaned = load_query(workbook, ws, "fred_json_clean", f'let Source = Json.Document(File.Contents("{json_path}")), '
                             'Rows = Table.FromRecords(Source[observations]), '
                             'NoDots = Table.SelectRows(Rows, each [value] <> "."), '
                             'Typed = Table.TransformColumnTypes(NoDots, {{"date", type date}, {"value", type number}}, "en-US") '
                             'in Typed')
        print(f"  with Table.SelectRows(Rows, each [value] <> \".\") before the type change: {len(cleaned) - 1} rows, "
              f"every value a number: {all(isinstance(row[3], float) for row in cleaned[1:])}")

        # two CSV files: the Treasury file split by year, then appended; the Treasury file merged with the spreads
        with open(DATA / "treasury_par_yields.csv", encoding="utf-8") as f:
            lines = f.read().splitlines()
        header, body = lines[0], lines[1:]
        (folder / "first.csv").write_text("\n".join([header] + [x for x in body if x < "2026"]) + "\n", encoding="utf-8")
        (folder / "second.csv").write_text("\n".join([header] + [x for x in body if x >= "2026"]) + "\n", encoding="utf-8")
        csv_source = 'Table.PromoteHeaders(Csv.Document(File.Contents("{}"), [Delimiter=",", Encoding=65001]))'
        appended = load_query(workbook, ws, "appended",
                              f"let First = {csv_source.format((folder / 'first.csv').as_posix())}, "
                              f"Second = {csv_source.format((folder / 'second.csv').as_posix())}, "
                              "Both = Table.Combine({First, Second}) in Both")
        print(f"  Power Query Append (Table.Combine) of the Treasury file split into two CSV files: {len(appended) - 1} "
              f"rows, header {appended[0][:3]}...: {'ok' if len(appended) - 1 == len(body) else 'DIFFERS'}")
        merged = load_query(workbook, ws, "merged",
                            f"let Curve = {csv_source.format((DATA / 'treasury_par_yields.csv').as_posix())}, "
                            f"Spreads = {csv_source.format((DATA / 'course3_synthetic_spreads.csv').as_posix())}, "
                            'Joined = Table.NestedJoin(Curve, {"date"}, Spreads, {"date"}, "s", JoinKind.LeftOuter), '
                            'Expanded = Table.ExpandTableColumn(Joined, "s", {"ig_spread_bp", "hy_spread_bp"}) in Expanded')
        last = merged[-1]
        print(f"  Power Query Merge (Table.NestedJoin, left outer, on date) of the Treasury file and the synthetic "
              f"spreads: {len(merged) - 1} rows, {len(merged[0])} columns, last row {last[0]} with ig {last[-2]} and "
              f"hy {last[-1]} (text, as Csv.Document reads them): {'ok' if len(merged) - 1 == len(body) else 'DIFFERS'}")
    finally:
        app.DisplayAlerts = False
        ws.Delete()
        shutil.rmtree(folder)


def check_power_query_web(workbook, app) -> None:
    ws = workbook.Worksheets.Add()
    try:
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10"
        rows = load_query(workbook, ws, "fredgraph",
                          f'let Source = Csv.Document(Web.Contents("{url}"), [Delimiter=",", Encoding=65001]), '
                          'Promoted = Table.PromoteHeaders(Source) in Promoted')
        dates = [row[0] for row in rows[1:]]
        print(f"  Power Query From Web (Web.Contents) on the key-free fredgraph.csv URL for DGS10: header {rows[0]}, "
              f"{len(rows) - 1} rows, first date {shown(dates[0])}, last date {shown(dates[-1])}")
    finally:
        app.DisplayAlerts = False
        ws.Delete()


def write_csv(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    web = "--web" in sys.argv[1:]
    app = win32com.client.DispatchEx("Excel.Application")
    try:
        app.Visible = False
        app.DisplayAlerts = False
        print(f"Excel {app.Version}, build {app.Build:.0f}, {app.OperatingSystem}")
        workbook = app.Workbooks.Add()
        ws = workbook.Worksheets(1)
        reference = compute_reference(ws, app)
        print("Behaviour checks:")
        check_encodeurl(ws, app)
        check_value_dot(ws, app)
        check_weekday(ws, app)
        check_holdings_formulas(ws, app)
        check_pivot_by_month(workbook, app)
        check_power_query(workbook, app)
        if web:
            check_power_query_web(workbook, app)
        workbook.Close(SaveChanges=False)
    finally:
        app.Quit()

    write_csv(DATA / "course3_excel_reference.csv", reference)
    print(f"course3_excel_reference.csv: {len(reference)} rows, {reference[0]['date']} to {reference[-1]['date']}")


if __name__ == "__main__":
    main()
