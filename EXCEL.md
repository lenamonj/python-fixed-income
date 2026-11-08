# Excel to Python

Every Excel comparison in the series, course by course. Each notebook introduces a new idea beside the Excel formula or feature you would use today, with the formula written out. Back to the [series front page](README.md).

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

| In Excel you would | In Python you will | Course | Where |
|:---|:---|:---:|:---|
| A workbook, its formula cells and notes, F9, add-ins, and VBA modules | A notebook, its code and markdown cells, Run All, libraries, and `.py` files | 1 | Week 1, Day 0 |
| `=2+2`, `=5-3`, `=5*5`, `=10/5`, `=QUOTIENT(7,2)`, `=MOD(7,2)`, `=5^2` | `2 + 2`, `5 - 3`, `5 * 5`, `10 / 5`, `7 // 2`, `7 % 2`, `5 ** 2` | 1 | Week 1, Day 0 |
| `=2+3*4` and `=(2+3)*4`: multiply before add, brackets first | `2 + 3 * 4` and `(2 + 3) * 4`: the same order | 1 | Week 1, Day 0 |
| Fill a formula down a column | Write the formula once, in a loop or on a whole array | 1 | Week 1, Day 1 Part 2 and Week 2, Day 1 |
| Wrap a number in `TEXT` and join it to a sentence with `&` | Write an f-string with a format code | 1 | Week 1, Day 1 |
| Type `=1/(1+0.05/2)^10` for a power, and use `QUOTIENT`, `MOD`, and `ROUND` | Write `1 / (1 + 0.05 / 2) ** 10`, `//`, `%`, and `round()`, and see why `^` is not a power in Python and `round(2.5)` gives 2 | 1 | Week 1, Day 1 |
| Name a cell in the Name Box: no leading digit, no space, and case ignored | Name a variable: no leading digit, no space, and case matters | 1 | Week 1, Day 1 |
| A number stored as text, flagged with a green triangle and skipped by `=SUM(A1:A4)`, and `=TRUE+TRUE+FALSE`, which gives 2 | Quotes make text, `type()` names the type, and `True + True + False` gives 2 | 1 | Week 1, Day 1 |
| `=A1*A2/100` for a cost, and `COUNTA`, `MIN`, `MAX`, `SUM`, and `AVERAGE` on a column | `face * price / 100`, and `len`, `min`, `max`, and `sum` on a list | 1 | Week 1, Day 1 |
| `=XLOOKUP("Seniority",A1:A6,B1:B6,"not recorded")`, and `=VLOOKUP("Coupon",A1:B6,2,FALSE)` | `bond['Coupon']`, and `bond.get('Seniority', 'not recorded')` | 1 | Week 1, Day 1 |
| `LEN`, `LEFT`, `MID`, `RIGHT`, `TRIM`, `UPPER`, `LOWER`, `SUBSTITUTE`, `VALUE`, `FIND`, `SEARCH`, and `TEXTSPLIT` | `len`, slicing, `strip()`, `upper()`, `lower()`, `replace()`, `int()`, `in`, and `split()` | 1 | Week 1, Day 1 |
| Write a nested `IF` | Write `if`, `elif`, `else`, one test per line | 1 | Week 1, Day 1 Part 2 |
| Compare with `=`, `<>`, `<`, `<=`, `>`, and `>=`, join tests with `=AND(A1>10,B1>100)`, `=OR(A1<=10,B1>100)`, and `=NOT(A1<=10)`, and ask whether a range holds a value with `=COUNTIF(A1:A4,"DNMR")>0` | `==`, `!=`, `<`, `<=`, `>`, `>=`, `and`, `or`, `not`, `in`, and `not in` | 1 | Week 1, Day 1 Part 2 |
| Test an empty cell with `=ISBLANK(A1)`, where `=A1+1` counts the blank as 0 | Test for `None` with `is None`, where `None + 1` is a `TypeError` | 1 | Week 1, Day 1 Part 2 |
| Total the cost in one cell with `=SUMPRODUCT(B2:B5,C2:C5)/100` | Keep a running total in a loop with `+=` | 1 | Week 1, Day 1 Part 2 |
| Keep the rows that pass with `=FILTER(A2:A5,F2:F5<=10)` | Write a list comprehension with an `if` at the end | 1 | Week 1, Day 1 Part 2 |
| Name a reusable formula `=LAMBDA(face,coupon,face*coupon/100)` in the Name Manager | Write a function with `def` and `return` | 1 | Week 1, Day 1 Part 2 |
| Sort with `=SORT(A1:A4,1,-1)` and `=SORTBY(A1:A4,C1:C4,-1)`, or with the Sort buttons on the Data tab | `sorted(price_list, reverse=True)`, and `sorted(holdings, key=price_of)` | 1 | Week 1, Day 1 Part 2 |
| Show a saved workbook's full path with `=CELL("filename",A1)` | `os.getcwd()` and `os.path.basename()` | 1 | Week 1, Day 2 |
| Double-click a CSV file and see it split at the commas, where Windows' list separator is a comma | Write a CSV file with `open()`, `write()`, and a loop, and read it back | 1 | Week 1, Day 2 |
| Split a column with Text to Columns, the comma as the delimiter | `line.strip().split(',')` | 1 | Week 1, Day 2 |
| See a quoted name such as `"Quorvane Energy, Inc."` stay in one cell | `csv.reader` and `csv.DictReader` | 1 | Week 1, Day 2 |
| Count the names that end in .csv with `=COUNTIF(A1:A10,"*.csv")` | `Path.glob('*.csv')` | 1 | Week 1, Day 2 |
| Type `=1+` and see Excel refuse the formula | Read a `SyntaxError` | 1 | Week 1, Day 3 |
| Multiply text by a number with `=A1*5.25/100` and get 78750, because Excel converts the text | See a `TypeError`, because Python never converts | 1 | Week 1, Day 3 |
| Repeat text with `=REPT("1500000",2)` | Repeat a string with `'1500000' * 2` | 1 | Week 1, Day 3 |
| Round down with `=INT(98.5)` | Round down with `math.floor(98.5)` | 1 | Week 1, Day 3 |
| Count from 1 with `=INDEX(A1:A4,1)`, and see `#REF!` from `=INDEX(A1:A4,5)` | Count from 0, and see an `IndexError` | 1 | Week 1, Day 3 |
| Look up with `XLOOKUP`, which ignores case | Use exact dictionary keys, and see a `KeyError` | 1 | Week 1, Day 3 |
| Convert with `=VALUE("5.25%")`, which returns 0.0525 | See `float()` refuse `'5.25%'` | 1 | Week 1, Day 3 |
| See `#NAME?`, `#VALUE!`, `#REF!`, `#N/A`, or `#DIV/0!` in a cell while the sheet calculates on | Read the error's type on a traceback's last line, from a table of every error so far | 1 | Week 1, Day 3 |
| Step through a formula with Evaluate Formula on the Formulas tab | Put a `print()` inside a loop | 1 | Week 1, Day 3 |
| Paste a range, a separate copy from the moment it lands | Ask for a separate list with `.copy()`, since a second name is not a copy | 1 | Week 1, Day 3 |
| See `=0.1+0.2=0.3` return TRUE | See `0.1 + 0.2 == 0.3` return `False`, and compare with `math.isclose()` | 1 | Week 1, Day 3 |
| Catch errors with `=IFERROR(VALUE(A1),"bad price")` and `=IFNA(XLOOKUP(...),"not found")` | See a bare `except:` hide a typo, and name the error instead | 1 | Week 1, Day 3 |
| Put an `IF` beside a total that shows OK or CHECK, and refuse a typed value with Data Validation | Stop the run with an `assert` on your own totals, and with `raise` in a function handed a bad value | 1 | Week 1, Day 3 |
| Add a class in VBA with Insert, Class Module, and refer to the object with `Me` | Write a `class`, and refer to the object with `self` | 1 | Week 1, Day 4 |
| See `=ROUND(98.5)` refused for too few arguments | See a `TypeError` name the term `__init__` was not given | 1 | Week 1, Day 4 |
| Paste a value over a formula, and watch it go stale | Store a worked-out value as an attribute and watch it go stale; a method works it out on every call | 1 | Week 1, Day 4 |
| Build a label with `=A2&" "&B2&"% of "&C2` | Write `__str__` with an f-string, so `print` shows a Bond in words | 1 | Week 1, Day 4 |
| Add a row to an Excel Table, and it picks up the formula columns | Make a new object, and it comes with its methods | 1 | Week 1, Day 4 |
| Filter with `=FILTER(A2:A5,D2:D5<100)` | Write a list comprehension with `if` over a list of objects | 1 | Week 1, Day 4 |
| Find the top row with `=INDEX(A2:A5,MATCH(MAX(B2:B5),B2:B5,0))` | Use `max(..., key=...)`, which hands back the whole object | 1 | Week 1, Day 4 |
| Find a position with `=MATCH("DNMR",A2:A7,0)`, counted from 1, and read it with `=INDEX(F2:F7,2)` | Find a position with `index()`, counted from 0, and read every list at it | 1 | Week 1, Day 5 |
| Fill `=IF(E2>=11,G2-0.5,G2)` down a new column | Correct the prices where they sit, with an `if` inside an `enumerate()` loop | 1 | Week 1, Day 5 |
| Count with `=COUNTIF(E2:E7,"<=10")` and `=COUNTIF(I2:I7,">100")` | Count in a loop with a counter and `+=` | 1 | Week 1, Day 5 |
| Count the rows that pass two tests with `=COUNTIFS(E2:E7,">=11",I2:I7,">100")` | Join two tests with `and`, and see `or` let in one more bond | 1 | Week 1, Day 5 |
| Let `=IFS(E4<=10,"BBB",E4<=7,"A or better",TRUE,"High yield")` stop at the first true test | Order the tests in `if` and `elif`, the narrowest first | 1 | Week 1, Day 5 |
| A worksheet: named columns, one bond per row | A pandas DataFrame, built from a dictionary of lists | 1 | Week 1, Day 5 |
| Take `COUNT`, `AVERAGE`, `STDEV.S`, `MIN`, `QUARTILE.INC`, `MEDIAN`, and `MAX`, and read 7.33E+05 in Scientific format | Call `describe()` once for every number column, and read `7.333333e+05` | 1 | Week 1, Day 5 |
| Subtract par with `=I2-100`, fill it down, and insert a Column Chart | Points from par by a comprehension, one colour per bar with `color=` | 1 | Week 1, Day 5 |
| Total with `=SUM(H2:H7)` | `df['Face'].sum()`, with no loop | 1 | Week 1, Day 5 |
| Save the sheet with File, Save As, CSV (Comma delimited), and open it again | Write the table with `to_csv()`, and read it back with `read_csv()` | 1 | Week 1, Day 5 |
| Filter with AutoFilter, and sort with Data, Sort, which reorders the sheet, or with `=SORT(A2:S201,13,-1)` in Excel 2021 and Microsoft 365, which spills a sorted copy | `holdings[is_energy]`, and `sort_values('oas', ascending=False)`, which hands back a sorted copy | 1 | Week 2, Day 2 Part 2 |
| Use `SUMIF` and `COUNTIF` | Filter, then sum or count | 1 | Week 2, Day 2 Part 2 and Day 5 |
| Count blanks with `=COUNTBLANK(E2:E201)`, and use Data, Remove Duplicates, which deletes the copies and says how many | `isna().sum()` per column, and `duplicated().sum()`, which marks only the second copy and deletes nothing | 1 | Week 2, Day 4 |
| Bring a column across with `=VLOOKUP(B2,issuers!A:C,3,FALSE)` filled down, once per column wanted; `=XLOOKUP(B2,issuers!A:A,issuers!C:C)` in Excel 2021 or later and Microsoft 365; `INDEX` and `MATCH` in any version | `pd.merge(positions, issuer_details, on='ticker')`: every column wanted in one line | 1 | Week 2, Day 3 and Day 5 |
| Build a pivot table | Group by a column and summarize | 1 | Week 2, Day 3, Day 3 Part 2, and Day 5 |
| Save a workbook with File, Save As, Excel Workbook, put two tables on two sheets, and open one sheet by its tab | `to_excel(sheet_name=)`, `pd.ExcelWriter` for several sheets, and `read_excel(sheet_name=)`, or `sheet_name=None` for every sheet | 1 | Week 2, Day 3 Part 2 and Day 5 |
| Weight the book with `=SUMPRODUCT(M2:M201,S2:S201)/SUM(S2:S201)`, and one sector with `=SUMPRODUCT((E2:E201="Energy")*M2:M201*S2:S201)/SUMIFS(S2:S201,E2:E201,"Energy")` | OAS times market value, summed, over the summed market value; per sector with `groupby` | 1 | Week 2, Day 3 Part 2 and Day 5 |
| Spill `=B2:B5*C2:C5/100` from one cell (Microsoft 365, Excel 2021) | Multiply two arrays value by value: `faces * prices / 100` | 1 | Week 2, Day 1 |
| Build a run of numbers with `=SEQUENCE(11,1,95,1)` | `np.arange` | 1 | Week 2, Day 1 |
| Total with `=SUM(E2:E5)`, or in one cell with `=SUMPRODUCT(B2:B5,C2:C5)/100` | `costs.sum()`, or `(faces * prices / 100).sum()` | 1 | Week 2, Day 1 |
| Test two decimals with `=ABS(F2-G2)<0.000001` or `=ROUND(F2,6)=ROUND(G2,6)` | `np.isclose` and `np.allclose`, never `==` | 1 | Week 2, Day 1 |
| Multiply by an empty cell and get 0 | A `ValueError` when four values meet five | 1 | Week 2, Day 1 |
| See `#DIV/0!` in a yield and in its `SUM` | `inf`, a `RuntimeWarning`, and an `inf` that carries into the sum | 1 | Week 2, Day 1 |
| Take `SUM`, `AVERAGE`, `MIN`, `MAX`, and `ROUND`, and find the top bond with `INDEX` and `MATCH` | `np.sum`, `np.mean`, `np.min`, `np.max`, `np.round`, and `tickers[np.argmax(coupons)]` | 1 | Week 2, Day 1 |
| Sort with `=SORT(D2:D5)`, and sort one column by another with `=SORTBY(A2:A5,D2:D5)` | `np.sort`, and `tickers[np.argsort(coupons)]` | 1 | Week 2, Day 1 |
| Start a running total with `=B2`, then fill `=H2+B3` down | `np.cumsum` | 1 | Week 2, Day 1 |
| Weight the coupons with `=SUMPRODUCT(D2:D5,B2:B5)/SUM(B2:B5)` | `np.average(coupons, weights=faces)` | 1 | Week 2, Day 1 |
| Use `=STDEV.P` and `=STDEV.S` | `np.std`, and `np.std(prices, ddof=1)` | 1 | Week 2, Day 1 |
| Draw with `=RAND()`, `=RANDBETWEEN(1,10)`, and `=NORM.S.INV(RAND())*5`, with no seed | `rng.random`, `rng.integers`, and `rng.standard_normal(250) * 5` from a seeded generator | 1 | Week 2, Day 1 |
| Take a change with `=B3-B2` and a return with `=B3/B2-1` | `np.diff`, and a simple return on the whole array | 1 | Week 2, Day 1 |
| Take a log return with `=LN(B3/B2)`, and undo it with `=EXP()` | `np.log` and `np.exp` on whole arrays | 1 | Week 2, Day 1 |
| Test a cell with `=ISNUMBER(F2)` | `np.isfinite` | 1 | Week 2, Day 1 Part 2 |
| Label with `=IF(C2>100,"Premium","Discount")`, count with `=COUNTIF(C2:C5,"<100")`, total with `=SUMIF(C2:C5,"<100",B2:B5)`, and keep rows with `=FILTER(A2:A5,C2:C5<100)` | `np.where`, and a boolean mask: `(prices < 100).sum()`, `faces[prices < 100].sum()`, `tickers[prices < 100]` | 1 | Week 2, Day 1 Part 2 |
| Price from cash flows with `=SUMPRODUCT(B2:B15,C2:C15)`, or in one step with `=PV(5.51%/2,14,-2.625,-100)` | `(cash_flows * discount_factors).sum()` | 1 | Week 2, Day 1 Part 2 |
| Use the Scientific number format | Read `1.5e+06` in an output | 1 | Week 2, Day 1 Part 2 |
| Put `=SUM()` under each column, or at the end of each row | `sum(axis=0)` and `sum(axis=1)` | 1 | Week 2, Day 1 Part 2 |
| Reshape a row with `=WRAPROWS(A1:L1,4)` | `reshape` | 1 | Week 2, Day 1 Part 2 |
| Value a book with `=SUMPRODUCT(B2:B4,C2:C4)/100` for one day or `=MMULT(TRANSPOSE(B2:B4),C2:F4)/100` for every day, turn a grid with `=TRANSPOSE(C2:F4)`, and build an identity with `=MUNIT(3)` | `@`, `.T`, and `np.eye(3)` | 1 | Week 2, Day 1 Part 2 |
| Save As CSV | `np.savetxt` | 1 | Week 2, Day 1 Part 2 |
| Look up by label with `=VLOOKUP("PLWK",A2:B5,2,FALSE)`, and by position with `=INDEX(B2:B5,1)`, counted from 1 | `prices['PLWK']`, and `prices.iloc[0]`, counted from 0 | 1 | Week 2, Day 2 |
| Pair each coupon with its own face with `=B2*VLOOKUP(A2,D:E,2,FALSE)/100` filled down, and see `#N/A` for a missing ticker carry into `=SUM()` | `faces * coupons / 100`, matched by label, with `NaN` for the missing bond and `sum()` totalling the rest | 1 | Week 2, Day 2 |
| Press Ctrl+End to land on S201: the header in row 1, the bonds in rows 2 to 201 | `holdings.tail(3)`, the last label 199, counted from 0 | 1 | Week 2, Day 2 |
| Hide the other columns, or take them with `=CHOOSECOLS(A1:S201,3,7,8,9)` in Microsoft 365 | `holdings[['ticker', 'coupon', 'maturity', 'price']]` | 1 | Week 2, Day 2 |
| Find a price with `=VLOOKUP("99039NAC0",B:I,8,FALSE)` or `=INDEX(I:I,MATCH("99039NAC0",B:B,0))`, take a block with `=TAKE(A2:S201,3,4)` in Microsoft 365, and see `#N/A` for a CUSIP that is not there | `by_cusip.loc['99039NAC0', 'price']`, `holdings.iloc[0:3, 0:4]`, and a `KeyError` | 1 | Week 2, Day 2 |
| Set a pivot to Show Values As, % of Grand Total | `value_counts(normalize=True)` | 1 | Week 2, Day 2 Part 2 |
| Count distinct values with `=COUNTA(UNIQUE(C2:C201))` | `nunique()` | 1 | Week 2, Day 2 Part 2 |
| Count several labels with `=SUM(COUNTIF(F:F,{"A+","A","A-"}))` | `isin().sum()` | 1 | Week 2, Day 2 Part 2 |
| Take the largest or smallest with `LARGE` and `SMALL` | `nlargest` and `nsmallest` | 1 | Week 2, Day 2 Part 2 |
| Label the rows that pass a test with `=IF(I2<80,"Confirm","OK")` filled down | `marks.loc[marks['price'] < 80, 'price_check'] = 'Confirm'` | 1 | Week 2, Day 2 Part 2 |
| Change a price and watch `=R4*(I4+K4)/100` recalculate | Change a price, then rerun the line that computes market value: a column holds values, not formulas | 1 | Week 2, Day 2 Part 2 |
| Set Format Cells to 2 decimal places, or Custom `#,##0" bp"`, while the cell keeps every digit | `.style.format({'price': '{:.2f}', 'oas': '{:,.0f} bp'})`, display only | 1 | Week 2, Day 2 Part 2 |
| Shade with Conditional Formatting, Color Scales, mark the top price with Top 10 Items set to 1, and add Data Bars | `.background_gradient()`, `.highlight_max()`, and `.bar()` on a Styler | 1 | Week 2, Day 2 Part 2 |
| Choose Inner, Left Outer, Right Outer, or Full Outer as the Join Kind in Power Query's Merge Queries (Excel 2016 and later) | `how='inner'`, `'left'`, `'right'`, or `'outer'`, and `indicator=True` to mark where each row was found | 1 | Week 2, Day 3 |
| See `#N/A` where `VLOOKUP` finds no match, and find it with `=ISNA(...)` | `NaN` from a left merge, found with `isna()` | 1 | Week 2, Day 3 |
| Let `VLOOKUP` take the first of two matches, and find repeats with a helper `=COUNTIF(A:A,A2)` above 1 | A repeated key repeats rows; `validate='many_to_one'` refuses it | 1 | Week 2, Day 3 |
| Mark the benchmark bonds held with a helper `=COUNTIF(holdings!B:B,B2)`, and add their weight with `=SUMIFS(S:S,T:T,1)` | A left merge on the CUSIP, then `notna()` and `loc[held, 'weight_pct'].sum()` | 1 | Week 2, Day 3 |
| Paste one range under another, or `=VSTACK(range1,range2)` in Microsoft 365 and Excel 2024, matched by position | `pd.concat([ig_book, hy_book])`, columns matched by name, and `ignore_index=True` to number the rows again | 1 | Week 2, Day 3 |
| Put ranges side by side with `=HSTACK(range1,range2)` in Microsoft 365 and Excel 2024, matched by position | `pd.concat([price_part, oas_part], axis=1)`, matched by row label | 1 | Week 2, Day 3 |
| Total, average, and count one sector with `=SUMIFS(S:S,E:E,"Energy")`, `=AVERAGEIFS(M:M,E:E,"Energy")`, and `=COUNTIFS(E:E,"Energy")` | `groupby('sector')` with `sum()`, `mean()`, `count()`, or `agg()`: every sector at once | 1 | Week 2, Day 3 |
| Read day-first dates with Text to Columns and DMY | `dayfirst=True` | 1 | Week 2, Day 3 Part 2 |
| Format a date with `=TEXT(H2,"dd mmm yyyy")` | `strftime` | 1 | Week 2, Day 3 Part 2 |
| Build a PivotTable with sector in Rows, grade in Columns, and Sum of market_value in Values, Grand Totals on | `pd.pivot_table(book, index='sector', columns='grade', values='market_value', aggfunc='sum', margins=True)` | 1 | Week 2, Day 3 Part 2 |
| Label each row with `=IF(I2>100,"Premium",IF(I2<100,"Discount","Par"))` filled down | `apply` with a function, or a nested `np.where` | 1 | Week 2, Day 3 Part 2 |
| Turn date text into a date with `=DATEVALUE(H2)`, and read its parts with `=YEAR(H2)`, `=MONTH(H2)`, and `=TEXT(H2,"dddd")` | `pd.to_datetime()`, then `.dt.year`, `.dt.month`, and `.dt.day_name()` | 1 | Week 2, Day 3 Part 2 |
| Work out years left with `=(H2-A2)/365.25`, three years on with `=EDATE(A2,36)`, and count early maturities with `=COUNTIF(H:H,"<"&DATE(2028,1,1))` | `(book['maturity'] - as_of).dt.days / 365.25`, and a date column compared with `pd.Timestamp` | 1 | Week 2, Day 3 Part 2 |
| Bucket with a nested `IF`, or `VLOOKUP` approximate on a table of edges | `pd.cut(years, bins=edges, labels=names)` | 1 | Week 2, Day 3 Part 2 |
| Keep a digit-only CUSIP's zeros with Data, From Text/CSV (Excel 2016 and later), Data Type Detection set to Do not detect data types | `read_csv(..., dtype={'cusip': str})` | 1 | Week 2, Day 3 Part 2 |
| Test each key with `=COUNTIF(issuers!A:A,B2)>0` filled down, ask whether all passed with `=AND(G2:G201)`, flip one with `=NOT(G2)`, and count the misses with `=COUNTIF(G2:G201,FALSE)` | `positions['ticker'].isin(issuers['ticker'])`, then `.all()`, `~`, and `(~found).sum()` | 1 | Week 2, Day 4 |
| Test a key for repeats with `=COUNTA(UNIQUE(A2:A201))=COUNTA(A2:A201)` in Excel 2021 and Microsoft 365 | `positions['cusip'].is_unique` | 1 | Week 2, Day 4 |
| Flag rows with helper columns such as `=IF(E2<100,1,0)`, add across with `=SUM(G2:I2)` and down with `=SUM(G2:G201)` | A DataFrame of True and False flags, `flags.sum(axis=1)` across and `flags.sum()` down | 1 | Week 2, Day 4 |
| Count lookups that found nothing with `=SUMPRODUCT(--ISNA(G2:G201))` | `isna().sum()` on the columns a left merge brought in | 1 | Week 2, Day 5 |
| Fill helper columns down: `=F2*E2/100` for value, `=F2*C2/100` for coupon income, `=(D2-DATE(2026,9,30))/365.25` for years, and `=N2/SUM($N$2:$N$201)*100` for weight, the anchors keeping the total fixed | One line per new column on the whole book, with `weight_pct` checked to add to 100 by `np.isclose()` | 1 | Week 2, Day 5 |
| Build a PivotTable with sector in Rows and Sum of value twice in Values, the second set to Show Values As, % of Grand Total | `groupby('sector').agg(bonds=..., value=...)`, then each value over the total | 1 | Week 2, Day 5 |
| Count and total one grade with `=COUNTIF(M:M,"High Yield")` and `=SUMIF(M:M,"High Yield",N:N)` | `groupby('grade')`: shares by count and by value side by side | 1 | Week 2, Day 5 |
| Insert, Bar, Stacked Bar on a sector by grade grid | `plot.barh(stacked=True)` | 1 | Week 2, Day 5 |
| Weight one grade's coupon with `=SUMPRODUCT((M2:M201="High Yield")*C2:C201*N2:N201)/SUMIF(M2:M201,"High Yield",N2:N201)` | A product column and the value summed by `groupby('grade')`, one divided by the other | 1 | Week 2, Day 5 |
| Build a PivotTable with issuer in Rows, Count of cusip and Average of coupon in Values, then Value Filters, Greater Than Or Equal To; or Sum of value with Value Filters, Top 10 | Two one-row-per-issuer summaries with `reset_index()`, filtered and joined with `.merge()`; or `nlargest(10)` | 1 | Week 2, Day 5 |
| Put grade and bucket both in a PivotTable's Rows, then drag grade from Rows to Columns | `groupby(['grade', 'maturity_bucket'])`, then `unstack('grade')` | 1 | Week 2, Day 5 |
| Insert a chart: Histogram and Box and Whisker from Insert, Statistic Chart; Clustered Column or Clustered Bar; Line with Markers; Scatter, with the first column on x | `ax.hist`, `ax.boxplot`, `ax.bar` and `ax.barh`, `ax.plot`, `ax.scatter`, or seaborn's `histplot`, `barplot`, `countplot`, `lineplot`, and `scatterplot` | 1 | Week 3, Day 1 |
| Add a line with Chart Elements, Trendline, Linear, which draws no band, and measure it with `=SLOPE(L2:L201,G2:G201)`, `=INTERCEPT(L2:L201,G2:G201)`, and `=RSQ(L2:L201,G2:G201)`, y first | `np.polyfit(book['coupon'], book['yield_pct'], deg=1)`, x first, and `sns.regplot`, which adds a band | 1 | Week 3, Day 2 |
| Show every bond in a Box and Whisker chart with Format Data Series, Show inner points; Excel has no violin chart | `sns.violinplot`, `sns.stripplot`, and `sns.swarmplot` | 1 | Week 3, Day 2 |
| Take one group's lowest and highest with `=MINIFS(M:M,V:V,"Investment Grade")` and `MAXIFS`, in Excel 2019 and later | A violin cut at the data with `cut=0`, its ends checked against `min()` and `max()` | 1 | Week 3, Day 2 |
| Draw one chart per group, each from the filtered table, and count a group with `=COUNTIFS(E:E,"Utilities",V:V,"High Yield")` | `sns.catplot(kind='strip', col='grade')` | 1 | Week 3, Day 2 |
| Put a Scatter beside two Histograms, and count with `=COUNTIF(M:M,"<250")` | `sns.jointplot` | 1 | Week 3, Day 2 |
| Rest the pointer on a point for a tip with its series and value | `px.scatter(hover_name=, hover_data=)` and `fig.show()` | 1 | Week 3, Day 2 |
| Total one stacked piece with `=SUMIFS(S:S,E:E,"Consumer",V:V,"High Yield")/1000000` | `groupby(['sector', 'grade'])` and a stacked `px.bar` | 1 | Week 3, Day 2 |
| Price a bond on a coupon date with `=PRICE(DATE(2026,9,15),DATE(2056,9,15),0.05,0.1,100,2)`, which gives 52.68, and draw a 3-D Surface chart | `bond_price(10, 30)`, `np.meshgrid`, and `go.Surface` | 1 | Week 3, Day 2 |
| Set Format Axis, Bounds, Minimum and Maximum; for two bars of 148.51 and 151.16 Excel's automatic minimum is 147 | `ax.set_ylim()`, with a bar axis left to start at zero | 1 | Week 3, Day 2 |
| Write axis numbers with Format Axis, Number, Format Code `#,##0`, add Chart Elements, Data Labels, and save with a right-click on the chart, Save as Picture | `ax.yaxis.set_major_formatter('{x:,.0f}')`, `ax.bar_label`, and `fig.savefig` | 1 | Week 3, Day 2 |
| Check a sheet against its cover note with `=COUNTA(B2:B205)` and `=SUM(S2:S205)`, and test a cell's type with `=ISNUMBER(I2)` and `=ISTEXT(I2)` | `len(raw)` and `.sum()` less stored control totals, and `dtypes` | 1 | Week 3, Day 3 |
| Mark repeats with `=COUNTIF(B:B,B2)>1`, then Data, Remove Duplicates, which deletes in place | `duplicated(keep=False)`, then `drop_duplicates()` on a copy | 1 | Week 3, Day 3 |
| Tidy text with `=UPPER(TRIM(C2))`; `=` ignores case, so `="thaa"="THAA"` is TRUE; `EXACT` tells them apart | `.str.strip().str.upper()`, compared with `!=` | 1 | Week 3, Day 3 |
| Test a rating against the scale with `=COUNTIF(ratings!A:A,F2)>0`, or limit entries with Data Validation, List | `book['rating'].isin(ratings['rating'])` | 1 | Week 3, Day 3 |
| Turn a system's words for missing into blanks with Power Query, Replace Values with `null` | `read_csv(..., na_values=['missing', '--'])` | 1 | Week 3, Day 3 |
| Count stale prices with `=COUNTIF(J:J,"<"&DATE(2026,9,30))` | `book[book['price_date'] < book['as_of_date']]` | 1 | Week 3, Day 3 |
| Count blank ratings with `=COUNTBLANK(F2:F201)`, total their value with `=SUMIF(F2:F201,"",S2:S201)`, and average past errors with `=AGGREGATE(1,6,...)` | `isna().sum()`, `.sum()` on the rows, and `mean()`, which skips a gap | 1 | Week 3, Day 3 |
| Fill every blank at once with Go To Special, Blanks, a value, and Ctrl+Enter | `fillna()` | 1 | Week 3, Day 3 |
| Measure with `=SKEW(M2:M201)`, `=QUARTILE.INC(L2:L201,1)`, a z-score with `=STANDARDIZE(M2,AVERAGE(M$2:M$201),STDEV.S(M$2:M$201))`, and cap with `=MIN(M2,409.875)` | `skew()`, `quantile(0.25)`, `(x - mean) / std`, and `clip(upper=409.875)` | 1 | Week 3, Day 3 |
| Correlate within one grade with `=CORREL(FILTER(N2:N201,V2:V201="High Yield"),FILTER(L2:L201,V2:V201="High Yield"))` in Excel 2021 and Microsoft 365; `CORREL` on a filtered sheet still counts the hidden rows | A filter, then `corr()` | 1 | Week 3, Day 3 |
| Untick Show outlier points in a Box and Whisker chart's Format Data Series (Excel 2016 and later) | `ax.boxplot(..., showfliers=False)` | 1 | Week 3, Day 3 |
| Repeat the month's steps with Power Query's Applied Steps and Refresh, and show a check with `=IF(COUNTA(B2:B201)=200,"ok","CHECK")`, which stops nothing | `clean_holdings(raw, ratings)`, with `assert` lines that stop the run | 1 | Week 3, Day 3 |
| Open the CSV in Excel 365, which converts its dates on opening, so `=ISNUMBER(A2)` is TRUE | `pd.read_csv(..., parse_dates=['date'], index_col='date')`, a `DatetimeIndex` | 1 | Week 3, Day 4 |
| Look up one date with `=XLOOKUP(DATE(2020,3,9),A2:A2941,M2:M2941)` (Excel 2021 and Microsoft 365) | `yields.loc['2020-03-09', '10 Yr']` | 1 | Week 3, Day 4 |
| Count the weekdays in the span with `=NETWORKDAYS(A2,A2941)`, 3,066, and blanks with `=COUNTBLANK(D2:D2941)`, 949 | `pd.date_range(freq='B')` with `difference()`, and `isna().sum()` | 1 | Week 3, Day 4 |
| Average one year with `=AVERAGEIFS(M:M,P:P,2020)` beside a `=YEAR(A2)` helper column, and `MAXIFS`, `MINIFS` from Excel 2019 | `yields.groupby(yields.index.year)['10 Yr'].agg(['mean', 'min', 'max'])` | 1 | Week 3, Day 4 |
| Turn wide to long with Power Query's Unpivot Other Columns, which leaves out null cells, and shade a table with Conditional Formatting, Color Scales | `melt()`, which keeps the blanks as `NaN` rows, and `sns.heatmap()` | 1 | Week 3, Day 4 |
| Find the date of the high with `=XLOOKUP(MAX(M2:M2941),M2:M2941,A2:A2941)` | `idxmax()` | 1 | Week 3, Day 4 |
| Take a month-end value with `=XLOOKUP(EOMONTH(DATE(2015,1,1),0),A2:A2941,M2:M2941,,-1)`, 1.68 | `resample('ME').last()` | 1 | Week 3, Day 4 |
| Chart a curve as a Scatter with Straight Lines, which places each point by its x in years; a Line chart spaces text labels evenly | `ax.plot(years, yields, marker='o')` | 1 | Week 3, Day 4 |
| Count days below zero with `=COUNTIF(Q2:Q2941,"<0")`, 544, beside `=(M2-I2)*100`, and in one year with `=COUNTIFS(Q2:Q2941,"<0",P2:P2941,2023)`, 250 | `(yields['spread_bp'] < 0).sum()` and `groupby(...).sum()` | 1 | Week 3, Day 4 |
| Take daily changes with `=(M3-M2)*100` filled down, the largest with `LARGE` and `SMALL`, and a 20-row average with `=AVERAGE(M2:M21)` filled down or a Moving Average trendline, period 20 | `diff() * 100`, `nlargest()`, `nsmallest()`, and `rolling(20).mean()` | 1 | Week 3, Day 4 |
| Net one sector with `=SUMIFS(J:J,O:O,"Financials",G:G,"BUY")` less the same with `"SELL"`, -7,042,969.65 | `pd.pivot_table(columns='side', aggfunc='sum')`, then `BUY` less `SELL` | 1 | Week 3, Day 5 |
| Check a blotter with `=COUNTBLANK(A2:L375)`, and `=MOD(H2,5000)` and `=COUNTIF(holdings!B:B,E2)` filled down | `isna().sum().sum()`, `quantity % 5000`, and `isin()` | 1 | Week 3, Day 5 |
| Show a check with `=IF(COUNTBLANK(A2:L375)=0,"ok","STOP")`, which stops nothing | `assert test, 'message'`, which stops the run | 1 | Week 3, Day 5 |
| Test a settle date with `=D2=WORKDAY(B2,1,$T$1)`, the holiday in T1; without it, the 14 Friday trades before the holiday turn FALSE | date minus date, `.dt.days`, then `value_counts()` | 1 | Week 3, Day 5 |
| Take the hour with `=HOUR(C2)` (Microsoft 365 opens `08:04` as a time) and the weekday with `=TEXT(B2,"dddd")` | `pd.to_datetime(format='%H:%M').dt.hour`, and `.dt.day_name()` in an ordered `pd.Categorical` | 1 | Week 3, Day 5 |
| Count by weekday and hour with a PivotTable: weekday in Rows, hour in Columns, Count of trade_id in Values | `pd.crosstab()`, drawn with `sns.heatmap()` | 1 | Week 3, Day 5 |
| Look up a trade's sector with `=XLOOKUP(E2,holdings!B:B,holdings!E:E)` (Excel 2021 and Microsoft 365; `INDEX` and `MATCH` before), which takes the first match silently | `pd.merge(how='left', validate='many_to_one')` | 1 | Week 3, Day 5 |
| Take a median by group, which a PivotTable cannot, with `=MEDIAN(IF(K2:K375="Kestermoor Securities",H2:H375))` (Ctrl+Shift+Enter before Excel 2021), and draw Insert, Statistic Chart, Box and Whisker (Excel 2016 and later) | named aggregation with `'median'`, and `sns.boxplot(order=)` | 1 | Week 3, Day 5 |
| Take turnover with `=SUMIF(O2:O375,"Consumer",J2:J375)/SUMIF(holdings!E2:E201,"Consumer",holdings!S2:S201)*100`, 35.55 | traded by sector over held by sector, aligned by label | 1 | Week 3, Day 5 |
| Sum market value looked up onto the blotter with `XLOOKUP`: 1,022,781,137.50, a bond counted once per trade | `trades['market_value'].sum()`, the same trap | 1 | Week 3, Day 5 |
| Take a volume-weighted price with `=SUMPRODUCT((E2:E375="99075XAE9")*I2:I375*H2:H375)/SUMIF(E2:E375,"99075XAE9",H2:H375)`, 99.742 | `(price * quantity).sum() / quantity.sum()` | 1 | Week 3, Day 5 |
| Keep a running net with `=IF(G2="BUY",J2,-J2)` and `=SUM($Q$2:Q2)` filled down | `cumsum()` | 1 | Week 3, Day 5 |
| Put ratings in credit order with `=UNIQUE(SORTBY(C2:C19,B2:B19))` | `ratings.sort_values('score')['bucket'].unique()` | 1 | Week 3, Day 1 |
| Name a chart's parts: the Chart Area, sized by dragging a corner, the Plot Area, the Chart Title, the Axis Titles, and Format Axis | `fig, ax = plt.subplots(figsize=(8, 4.5))`, `ax.set_title`, `ax.set_xlabel`, and `ax.set_ylabel` | 1 | Week 3, Day 1 |
| Count one histogram bin with `=COUNTIFS(M:M,">=19",M:M,"<325.4")`; a value on a bin edge falls in the left bin, where matplotlib puts it in the right | `counts, edges, bars = ax.hist(book['oas'], bins=5)`, then `counts[0]` | 1 | Week 3, Day 1 |
| Take quartiles with `=QUARTILE.INC(M2:M201,1)`, and set a Box and Whisker chart's Quartile Calculation to Inclusive median, since its default is Exclusive | `book['oas'].quantile(0.25)` | 1 | Week 3, Day 1 |
| Average one bucket with `=AVERAGEIFS(M:M,U:U,"BBB")`, and drag PivotTable buckets out of text order into credit order | `sns.barplot(data=book, x='bucket', y='oas', order=bucket_order)` | 1 | Week 3, Day 1 |
| Take one group's median with `=MEDIAN(IF(T2:T201=10,M2:M201))`, entered with Ctrl+Shift+Enter before dynamic arrays | `book.groupby('score')['oas'].agg(['median', 'mean', 'count'])` | 1 | Week 3, Day 1 |
| Add a note with an arrow through Insert, Shapes | `ax.annotate` | 1 | Week 3, Day 1 |
| Tick Logarithmic scale in Format Axis | `ax.set_yscale('log')` | 1 | Week 3, Day 1 |
| Tilt labels with a Custom angle in Format Axis | `rotation=45` | 1 | Week 3, Day 1 |
| Measure a correlation with `=CORREL(M2:M201,L2:L201)`, build a table with the Analysis ToolPak's Correlation, and shade it with Conditional Formatting, Color Scales | `.corr()`, then `sns.heatmap(corr_table, annot=True)` | 1 | Week 3, Day 1 |
| Draw a Scatter chart for each pair of columns, six for four columns | `sns.pairplot` | 1 | Week 3, Day 1 |
| Count, total, and average one group with `=COUNTIF(C2:C30001,1)`, `=SUMIF(C2:C30001,1,Y2:Y30001)`, and `=AVERAGEIF(C2:C30001,1,Y2:Y30001)` on a column of 0s and 1s | `groupby(column)['default'].agg(accounts='count', defaults='sum', rate_pct='mean')`, with a rough margin of error beside each rate | 1 | Week 4, Day 1 |
| Take a rate with `=AVERAGE(Y2:Y30001)` on a column of 0s and 1s, formatted as a percentage: the same as `=SUM(Y2:Y30001)/COUNT(Y2:Y30001)` | `cards['default'].mean()` | 1 | Week 4, Day 1 |
| Count codes a page never lists with `=COUNTIF(D2:D30001,"<1")+COUNTIF(D2:D30001,">4")`, and label codes with `=IFERROR(VLOOKUP(D2,codes,2,FALSE),"not documented")`, where `#N/A` marks a code missing from the list | `~isin([1, 2, 3, 4])`, then `map()` with a dictionary, which leaves a gap with no error, and `fillna('not documented')` | 1 | Week 4, Day 1 |
| Take a share of one outcome group with `=COUNTIFS(Y2:Y30001,1,B2:B30001,"<100000")/COUNTIF(Y2:Y30001,1)` | `sns.histplot(..., hue=, stat='percent', common_norm=False)` | 1 | Week 4, Day 1 |
| Use `FIND`, `SUBSTITUTE`, `TRIM`, and Find and Replace on text | Search and clean text with patterns, across every row at once | 1 | Week 4, Day 2 and Day 2 Part 2 |
| Find a word with `=FIND("Inflation",A2)`, which counts from 1, test for it with `=ISNUMBER(FIND(...))`, or use `SEARCH` to ignore capitals | `text.find('Inflation')`, which counts from 0, and `'inflation' in text` | 1 | Week 4, Day 2 |
| Count a piece of text with `=(LEN(A2)-LEN(SUBSTITUTE(A2,"rate","")))/LEN("rate")`, and the words with `=COUNTA(TEXTSPLIT(A2," "))` in Microsoft 365 and Excel 2024 | `text.count('rate')` and `len(text.split())` | 1 | Week 4, Day 2 |
| Pull the first match with `=REGEXEXTRACT(A2,pattern)`, its groups with `=REGEXEXTRACT(A2,pattern,2)`, and test a CUSIP's shape with `=REGEXTEST(B2,"^[0-9A-Z]{9}$")`, in Microsoft 365 | `re.search(pattern, text).group(0)`, `.groups()`, and `re.fullmatch()` or `.str.fullmatch()` on a column | 1 | Week 4, Day 2 |
| Take the text between two markers with `=TEXTBEFORE(TEXTAFTER(A2," at ")," percent")` in Microsoft 365 and Excel 2024 | A lazy group: `re.search(r' at (.+?) percent', text).group(1)` | 1 | Week 4, Day 2 |
| Split a bond description with `=TEXTSPLIT(TRIM(A2)," ")` and `=VALUE(C2)`, or type one and let Flash Fill (Ctrl+E) copy it as values | A pattern with three groups, `float()`, and `pd.to_datetime(format='%m/%d/%Y')` | 1 | Week 4, Day 2 |
| Count statements holding a word with `=COUNTIF(C2:C47,"*restrictive*")`, and a whole word list with `=SUMPRODUCT((LEN(C2)-LEN(SUBSTITUTE(LOWER(C2),$F$2:$F$15,"")))/LEN($F$2:$F$15))`, which counts pieces of text, so `support` inside `supporting` counts too | `.str.contains('restrictive').sum()`, and hits on whole tokens with a list comprehension | 1 | Week 4, Day 3 |
| Look up a word's rating with `=XLOOKUP("strong",lexicon!A:A,lexicon!B:B,0)`, in Microsoft 365 and Excel 2021 on | `analyzer.lexicon.get('strong', 0)` | 1 | Week 4, Day 3 |
| Standardize with `=STANDARDIZE(D2,AVERAGE($D$2:$D$47),STDEV.S($D$2:$D$47))`, correlate with `=CORREL(D2:D47,E2:E47)`, and take each change with `=D3-D2` filled down | `(scores - scores.mean()) / scores.std()`, `scores.corr()`, and `scores.diff()` | 1 | Week 4, Day 3 |
| Bring each statement date's yield change across with `=XLOOKUP(A2,yields!$A$2:$A$2941,yields!$P$2:$P$2941)`, where a missing date gives `#N/A` | `changes.join(yield_changes, how='left')`, where a missing date gives `NaN` | 1 | Week 4, Day 3 |
| Re-point every range for next month's file: `=SUM(S2:S205)` on the 204-row extract, `=SUM(S2:S201)` on the 200-row file | Change the file name and run the module's same lines | 1 | Week 4, Day 4 |
| Point a Power Query at a new file: Data, Get Data, Data Source Settings, Change Source, then Refresh (Excel 2016 and later) | A loop over the file names, each through `load_holdings`, `clean_holdings`, and `check_totals` | 1 | Week 4, Day 4 |
| Check the control totals with `=COUNTA(B2:B201)`, `=SUM(R2:R201)`, and `=SUM(S2:S201)`, where an `IF` check cell only shows a mismatch | `check_totals()`, which raises `ValueError` and stops the run | 1 | Week 4, Day 4 |
| Total a workbook's second sheet with `=COUNTA(book!B2:B201)`, `=SUM(book!R2:R201)`, and `=SUM(book!S2:S201)` | `write_report()` with `pd.ExcelWriter`, then `check_totals()` on the sheet read back | 1 | Week 4, Day 4 |
| Try a formula on a sheet of made-up rows with known answers before it meets the real ones | `test_clean_holdings()` on a seven-row table worked by hand | 1 | Week 4, Day 4 |
| Band a column with `=VLOOKUP(F2,bands,2,TRUE)` on a table of lower edges, and find a quartile edge with `=PERCENTILE.INC(B2:B30001,0.25)` | `pd.cut()`, and `pd.qcut()` for bands of equal counts, which ties on an edge can unbalance | 1 | Week 4, Day 1 |
| Count and average one cell of a two-way table with `=COUNTIFS(G2:G30001,2,B2:B30001,"<=50000")` and `=AVERAGEIFS(Y2:Y30001,G2:G30001,2,B2:B30001,"<=50000")` | Two `pd.pivot_table()` calls, `aggfunc='mean'` and `aggfunc='count'`, drawn side by side | 1 | Week 4, Day 1 |
| Divide by a zero bill with `=S2/M2`, which shows `#DIV/0!`, and guard it with `=IF(M2>0,S2/M2,"")` | pandas returns `inf` with no error; `np.isinf()` finds it and `np.where()` guards it | 1 | Week 4, Day 1 |
| Fix the range of Data Bars under More Rules | `vmin` and `vmax` on `.bar()` | 1 | Week 4, Day 1 |
| Count the months with a delay across a row with `=COUNTIF(G2:L2,">=1")` | `(cards[pay_columns] >= 1).sum(axis=1)` | 1 | Week 4, Day 1 |
| Correlate a column with an outcome of 0s and 1s with `=CORREL(B2:B30001,Y2:Y30001)` | `.corr()`, read beside the rates it cannot show | 1 | Week 4, Day 1 |
| Compare two word lists with `UNIQUE` and `=SUMPRODUCT(COUNTIF(B2:B5,A2:A4))` | `set()` and a Jaccard score | 1 | Week 4, Day 2 Part 2 |
| Clean text one step to a column: `=LOWER(A2)`, `=REGEXREPLACE(B2,"[^a-z\s]"," ")` in Microsoft 365, `=TRIM(C2)`, and `=TEXTSPLIT(D2," ")` in Microsoft 365 and Excel 2024; `TRIM` leaves line breaks and `CHAR(160)`, so `=COUNTA(TEXTSPLIT(A2," "))` counts 340 words where `split()` counts 344 | `clean()`: `lower()`, `re.sub(r'[^a-z\s]', ' ', text)`, `re.sub(r'\s+', ' ', text).strip()`, then `split(' ')` | 1 | Week 4, Day 2 Part 2 |
| Count a token with `=COUNTIF(B2:B344,"the")`, mark stopwords with `=COUNTIF(stop!A:A,B2)>0`, and keep the rest with `=FILTER(B2:B344,COUNTIF(stop!A:A,B2:B344)=0)` in Excel 2021 and Microsoft 365 | `Counter(tokens).most_common(10)` and `[token for token in tokens if token not in stop_words]` | 1 | Week 4, Day 2 Part 2 |
| Count every form of a word with a wildcard, `=COUNTIF(B2:B344,"remain*")`; no Excel function stems | `PorterStemmer().stem(word)` | 1 | Week 4, Day 2 Part 2 |
| Read a character's code with `=UNICODE(MID(C2,715,1))` and swap it with `=SUBSTITUTE(C2,UNICHAR(8209),"-")`, in Excel 2013 and later; a CSV opened by double-click garbles it unless written with `encoding='utf-8-sig'` | `ascii(text)`, `‑` in a character class, and `.str.replace('‑', '-')` | 1 | Week 4, Day 2 Part 2 |
| Shade a table of word counts with Conditional Formatting, Color Scales, and build the full table with a PivotTable: statement in Rows, token in Columns | `sns.heatmap(term_table.T)` and `pd.DataFrame(list(counters)).fillna(0)` | 1 | Week 4, Day 2 Part 2 |
| Take one year's share of statements holding a word with `=COUNTIFS(D2:D47,2026,E2:E47,TRUE)/COUNTIF(D2:D47,2026)` | The mean of a True and False column by year: `holds.groupby(year).mean()` | 1 | Week 4, Day 2 Part 2 |
| Hold a cut-off in one cell with `=IF(E2>=$H$1,...)` | A `cutoff=0.05` default | 1 | Week 4, Day 3 |
| Count above and below a cut-off with `=COUNTIF($E$2:$E$47,">="&H2)` | Try five cut-offs in a loop | 1 | Week 4, Day 3 |
| Type `=SUM` in a cell, then Ctrl+A, for the Function Arguments box | `help()`, which prints the signature and the docstring | 1 | Week 4, Day 4 |
| Save `=LAMBDA(oas, oas / 100)` in Formulas, Name Manager, for that workbook only (Microsoft 365, Excel 2024) | Write a function into a module any notebook can import | 1 | Week 4, Day 4 |
| Keep macros in the Personal Macro Workbook, PERSONAL.XLSB, which Excel opens hidden at start-up | `import desk_tools` | 1 | Week 4, Day 4 |
| Test an extract rule by rule with `=COUNTIF($B$2:$B$210, B2) > 1`, `=LEN(B2) = 9`, `=COUNTIF(R2:R210, "<=0")`, `=ABS(R2 * (I2 + K2) / 100 - S2) > 1` filled down, and `=COUNTBLANK(M2:M210)` | Each rule as a mask and a count: `duplicated(keep=False)`, `.str.fullmatch()`, `<= 0`, `.abs() > 1`, `isna().sum()` | 1 | Week 4, Day 5 |
| Match sector names with `=COUNTIF(benchmark!$E$2:$E$822, E2) = 0`, which ignores capitals, so it flags only the names off by a space | `~isin()`, which flags a name off by a space or by its capitals | 1 | Week 4, Day 5 |
| Weight a sector with `=SUMIF(E2:E207, "Materials", S2:S207) / SUM(S2:S207) * 100`, or a PivotTable value shown as % of Grand Total, and weight OAS and DTS with `=SUMPRODUCT(M2:M207, S2:S207) / SUM(S2:S207)` | `weight_pct` summed by `groupby()`, and `(x * w).sum() / w.sum()` | 1 | Week 4, Day 5 |
| Use `FV` and `PV`, and read the minus sign `PV` returns | Write `future_value` and `present_value` and test them against Excel's values | 2 | Week 1, Day 1 |
| Price a bond on a coupon date four ways: a column `=B1/(1+5.4/100/2)^A1` totalled by `=SUM(C1:C10)`, `=NPV(5.4/100/2,B1:B10)`, `=-PV(5.4/100/2,2*5,5.25/2,100)`, or `PRICE` | `cash_flows` and `price_from_yield`, tested against 20 `-PV` rows and 17 coupon-date `PRICE` rows | 2 | Week 1, Day 2 |
| Fill a column of `PRICE` formulas down a range of yields and chart it as a Scatter with Straight Lines | Price a grid of yields and plot the price-yield curve | 2 | Week 1, Day 3 |
| Restate a yield with `EFFECT` and `NOMINAL`, chained through A1: `=EFFECT(5.4/100,2)`, then `=NOMINAL(A1,4)*100` | Write `convert_yield` between any two compounding frequencies, tested against 16 `EFFECT` and 6 `NOMINAL` rows | 2 | Week 1, Day 3 |
| Goal Seek a yield, halve a bracket with `IF` formulas filled down, or use `=RATE(2*5,5.25/2,-99.125,100)*2` and `YIELD` on a coupon date | Write `yield_from_price`, a `while` loop that halves the bracket, tested against 18 `RATE` and 17 coupon-date `YIELD` rows | 2 | Week 1, Day 4 |
| Round a coupon with `MROUND`, and open a workbook of live `PRICE` and `YIELD` formulas | Find the coupon on a 1/8 grid, and write a workbook of live formulas with `to_excel` | 2 | Week 1, Day 5 |
| Write a growth factor as `=(1+5.4/100/2)^(2*5)` | `(1 + period_rate) ** (2 * 5)` | 2 | Week 1, Day 1 |
| Write a discount factor as `=1/(1+5.4/100/2)^(2*5)` or `=-PV(5.4/100/2,2*5,0,1)` | `bondmath.present_value(1, 5.4, 5)` | 2 | Week 1, Day 1 |
| Fill `=D1+100*5.4/100/2` down for simple interest | `100 + 100 * period_rate * k` | 2 | Week 1, Day 1 |
| Fill `=A1*(1+5.4/100/2)` down ten rows from 100 | A loop that multiplies by `1 + period_rate` ten times | 2 | Week 1, Day 1 |
| Discount with `=100/(1+5.4/100/2)^(2*5)`, or turn `PV`'s sign with `=-PV(5.4/100/2,2*5,0,100)` | `bondmath.present_value(100, 5.4, 5)`, positive as its docstring says | 2 | Week 1, Day 1 |
| Change the compounding in `=FV(5.4/100/4,4*5,0,-100)`, where the frequency sits in the rate and in the periods | The `frequency` argument of `future_value` and `present_value` | 2 | Week 1, Day 1 |
| Compound daily with `=100*(1+5.4/100/365)^(365*5)` | The formula written out, since the module refuses 365 | 2 | Week 1, Day 1 |
| Add a check column with `=ABS(A2-B2)<0.000001` beside `=FV(5.4/100/2,2*5,0,-100)` | `pytest.approx(..., abs=1e-6)` in a test over all 18 `FV` rows | 2 | Week 1, Day 1 |
| Save As with a date in the name | `git commit` | 2 | Week 1, Day 1 |
| Total the cash with `=SUM(B1:B10)` | `.sum()` | 2 | Week 1, Day 2 |
| Price the coupons alone with `=-PV(5.4/100/2,2*5,5.25/2,0)` | `price - redemption_pv` | 2 | Week 1, Day 2 |
| See `=-PV(5.4/100/2,2*2.3,5.25/2,100)` accept part periods | See `cash_flows` refuse them | 2 | Week 1, Day 2 |
| Price at a yield of 0 with `=-PV(0/100/2,2*5,5.25/2,100)`, the total cash | `bondmath.price_from_yield(5.25, 0, 5)` | 2 | Week 1, Day 2 |
| Read `=PRICE(DATE(2026,9,30),DATE(2031,9,30),5.25/100,5.4/100,100,2,0)` as the clean price, its seven arguments in order | `price_from_yield`, both the clean and the dirty price on a coupon date | 2 | Week 1, Day 2 |
| Label a bond with a nested `IF` on `ROUND` | A nested `np.where` on the rounded price | 2 | Week 1, Day 3 |
| Price a premium as `=-PV(4.6/100/2,2*3,(4.75-4.6)/2,0)` | The present value of the extras | 2 | Week 1, Day 3 |
| Restate a yield with `=((1+5.4/100/2)^2-1)*100` | Growth less 100 | 2 | Week 1, Day 3 |
| Price a coupon equal to the yield with `=-PV(6.125/100/2,2*30,6.125/2,100)`, 100 at any term | `bondmath.price_from_yield(6.125, 6.125, 30)` | 2 | Week 1, Day 3 |
| Fill `=-PV(7.7/100/2,2*A1,7.5/2,100)` down from 10 years left to 0.5 | Pull to par: `price_from_yield` at each coupon date, the yield held | 2 | Week 1, Day 3 |
| Measure a price change with `=B2-B1` and `=(B2-B1)/B1*100` | `(new - old) / old * 100`, and `price_change` in Exercise 4 | 2 | Week 1, Day 3 |
| Test `YIELD` with `ISERROR` | `ValueError` from the bracket check | 2 | Week 1, Day 4 |
| Find a negative yield with `=RATE(...,-130,100)*2*100` | `bondmath.yield_from_price(5.25, 130, 5)` | 2 | Week 1, Day 4 |
| Close without saving | `git restore` | 2 | Week 1, Day 4 |
| Start Goal Seek from 5.25 instead of 5, and see it stop at another yield | A search that stops where the code says: the bracket narrower than 1e-10 percent | 2 | Week 1, Day 4 |
| See `=YIELD(DATE(2026,9,30),DATE(2031,9,30),5.25/100,1000,100,2,0)*100` return -39.3451 | A bracket from -5 to 100 percent that refuses a price of 1,000 | 2 | Week 1, Day 4 |
| Measure a yield change with `=(B1-A1)*100` | `yield_change_bp` in Exercise 3 | 2 | Week 1, Day 4 |
| Count the different CUSIPs with `=SUMPRODUCT(1/COUNTIF(A1:A8,A1:A8))` | `.nunique()`, and `.is_unique` in an `assert` | 2 | Week 1, Day 5 |
| Test a coupon grid with `=MOD(5.125*8,1)` | `% 1` | 2 | Week 1, Day 5 |
| Move to a grid with `=FLOOR(5.69,0.125)` and `CEILING` | `math.floor` and `math.ceil` | 2 | Week 1, Day 5 |
| Price an eighth of coupon with `=-PV(5.5/100/2,2*30,0.125/2,0)` | The price of an eighth of coupon | 2 | Week 1, Day 5 |
| Price an eighth of coupon as two `PRICE` cells subtracted, 6.125 against 6 percent | `price_stepped - price_now` | 2 | Week 1, Day 5 |
| Open a workbook whose `YIELD` and `PRICE` formulas calculate on opening (Microsoft 365) | `pd.read_excel` reads the same cells as `NaN`: the file stores no result | 2 | Week 1, Day 5 |
| Keep a saved copy, `calendar_week1.xlsx` | `git tag` | 2 | Week 1, Day 5 |
| Read date serial numbers, and use `EDATE`, `EOMONTH`, `COUPPCD`, `COUPNCD`, and `COUPNUM` | Work with `date` values, add months, and build a coupon schedule back from maturity | 2 | Week 2, Day 1 |
| Use `COUPDAYBS`, `COUPDAYS`, `COUPDAYSNC`, `ACCRINT`, and `YEARFRAC` beside `DAYS360` | Count days on US 30/360 and actual/actual, and compute accrued interest | 2 | Week 2, Day 2 |
| Use `PRICE` between coupon dates, add accrued for the dirty price, use `YIELD`, and write the price out cell by cell | Write `price`, `dirty_price`, and `yield_to_maturity`, and invoice a month of trades | 2 | Week 2, Day 3 |
| Use `DURATION` and `MDURATION`, build DV01 from cells with `=B4*(B1+B2)/10000` and a position with `=B5*5000000/100`, and bump the yield in two `PRICE` cells with `=(B8-B9)/2` | Write `macaulay_duration`, `modified_duration`, and `dv01`, and check DV01 by bumping the yield | 2 | Week 2, Day 4 |
| Estimate convexity from three `PRICE` cells 1 bp apart and an accrued cell, `=(A2+A3-2*A1)/((A1+A4)*0.0001^2)`, since Excel has no convexity function | Write `convexity`, and check it against a central difference | 2 | Week 2, Day 5 |
| Take apart a date with `YEAR`, `MONTH`, and `DAY` | `.year`, `.month`, and `.day` | 2 | Week 2, Day 1 |
| Read a date with `=DATEVALUE("2031-09-30")` | `date.fromisoformat` | 2 | Week 2, Day 1 |
| Add days with `=DATE(...)+182` | `date + timedelta(days=182)` | 2 | Week 2, Day 1 |
| Compare dates with `<`, and take the latest with `MAX` | `<` and `max` on dates | 2 | Week 2, Day 1 |
| Find a month's length with `=DAY(EOMONTH(DATE(2027,2,1),0))` | `calendar.monthrange(...)[1]` | 2 | Week 2, Day 1 |
| Split months into years with `QUOTIENT` and `MOD` | `divmod(n, 12)` | 2 | Week 2, Day 1 |
| Set a date cell to General to see its serial, 46356, and subtract two dates | `(settlement - date(1899, 12, 30)).days`, and `(settlement - issue).days` | 2 | Week 2, Day 1 |
| See `=DATE(1900,2,29)` return 60, a day that never was | `date(1900, 2, 29)` raises `ValueError` | 2 | Week 2, Day 1 |
| Move by months with `=EDATE(DATE(2031,8,31),-6)` | `bondmath.add_months(date(2031, 8, 31), -6)` | 2 | Week 2, Day 1 |
| Fill `=EDATE(A1,-6)` down from the cell above, against `=EDATE($A$1,-6*C2)` from maturity | `add_months(stepped[-1], -6)` against `add_months(maturity, -6 * k)` | 2 | Week 2, Day 1 |
| Move to a month end with `=EOMONTH(DATE(2031,9,30),-6)` | the month-end rule in `coupon_dates` | 2 | Week 2, Day 1 |
| Find the previous coupon, the next, and the coupons left with `COUPPCD`, `COUPNCD`, and `COUPNUM` | `coupon_dates(settlement, maturity)[0]`, `[1]`, and `len(...) - 1` | 2 | Week 2, Day 1 |
| Test for month end with `=DATE(2031,9,30)=EOMONTH(DATE(2031,9,30),0)` | `d.day == calendar.monthrange(d.year, d.month)[1]`, and `.dt.is_month_end` on a column | 2 | Week 2, Day 1 |
| Name the weekday with `=TEXT(DATE(2026,11,30),"dddd")` | `settlement.strftime('%A')` | 2 | Week 2, Day 1 |
| Write the 30/360 formula with `YEAR`, `MONTH`, and `DAY`, and rule 3 with `MIN(DAY(A1),30)` | The formula on each date's `.year`, `.month`, and `.day`, then `days_30_360` with all four rules | 2 | Week 2, Day 2 |
| Count 30/360 days with `=YEARFRAC(DATE(2026,9,30),DATE(2026,11,30),0)*360` | `days_30_360` | 2 | Week 2, Day 2 |
| Work accrued on basis 1 with `COUPNCD` less `COUPPCD` | `accrued_interest(..., "ACT/ACT")` | 2 | Week 2, Day 2 |
| Check a period with `COUPDAYBS` plus `COUPDAYSNC` | A plus DSC | 2 | Week 2, Day 2 |
| See `DAYS360` give 359, 240, and -2 where `=YEARFRAC(...,0)*360` gives 360, 241, and 0, each pair starting on the last day of February | `bondmath.days_30_360`, which counts as `COUPDAYBS` and `YEARFRAC` do | 2 | Week 2, Day 2 |
| Set `COUPDAYSNC` beside `COUPDAYS` less `COUPDAYBS`: 150 against 148 for `99031FAF8` | DSC = E - A in `coupon_period_days`, the count `PRICE` uses | 2 | Week 2, Day 2 |
| Compute accrued with `=100*5.25/100/2*COUPDAYBS(...)/COUPDAYS(...)`, then with `ACCRINT(COUPPCD(...),COUPNCD(...),...)`, which differs on 9 reference rows and returns `#NUM!` on a coupon date or a zero coupon | `bondmath.accrued_interest`, equal to the `COUPDAYBS` route on all 306 rows | 2 | Week 2, Day 2 |
| Price the invoice in one cell, `=-PV(5.4/100/2,COUPNUM(...),5.25/2,100)*(1+5.4/100/2)^(COUPDAYBS(...)/COUPDAYS(...))` | The issue-date price grown by A / E of a period | 2 | Week 2, Day 3 |
| Price the final coupon period with simple interest, `=(100+5/2)/(1+(COUPDAYS(...)-COUPDAYBS(...))/COUPDAYS(...)*6/100/2)` less accrued, equal to `PRICE` | `price` with one coupon left | 2 | Week 2, Day 3 |
| Count the days left two ways, `=YEARFRAC(DATE(2026,12,15),DATE(2027,2,28),0)*360` (73) against `COUPDAYS` less `COUPDAYBS` (75) | The DSR that `YIELD` uses against the E - A that `PRICE` uses | 2 | Week 2, Day 3 |
| Invoice a trade, `=500000*(103.053+100*6.625/100/2*COUPDAYBS(DATE(2026,9,2),DATE(2033,5,9),2,0)/COUPDAYS(DATE(2026,9,2),DATE(2033,5,9),2,0))/100` | `principal + accrued_dollars` on all 374 trades | 2 | Week 2, Day 3 |
| Weight the time with `=SUMPRODUCT(B2:B11,D2:D11)/SUM(D2:D11)` | Macaulay duration, as weighted time | 2 | Week 2, Day 4 |
| Sign a short position with `*-2000000/100` | A short position's DV01 | 2 | Week 2, Day 4 |
| Divide `DURATION` by one plus the period yield, `=DURATION(...)/(1+5.4/100/2)`, equal to `MDURATION` | Modified duration from Macaulay duration | 2 | Week 2, Day 4 |
| Give `DURATION` a zero coupon, `=DURATION(DATE(2026,11,30),DATE(2031,9,30),0,5.4/100,2,0)`, 4.833333, the time to the one payment | `macaulay_duration` with a coupon of 0 | 2 | Week 2, Day 4 |
| Estimate a 100 bp rise with `=(-MDURATION(...)*0.01+0.5*A5*0.01^2)*100` beside a full reprice, `=(PRICE(...,7.7/100+0.01,...)-A1)/(A1+A4)*100` | The duration-and-convexity estimate against a full reprice | 2 | Week 2, Day 5 |
| Total a book's DV01 with `=SUMPRODUCT(E2:E201,H2:H201)/100`, its market value with `=SUM(I2:I201)`, and its duration with `=SUMPRODUCT(I2:I201,J2:J201)/SUM(I2:I201)` | Book DV01 in dollars and the market-value weighted duration of 200 bonds | 2 | Week 2, Day 5 |
| Chart a curve with Insert, Scatter with Straight Lines and Markers, tenors in years; a Line chart over the same range draws the tenor column as a second series and spaces the 14 points evenly | `ax.plot(real_curve['tenor_years'], real_curve['yield_pct'], marker='o')` | 2 | Week 3, Day 1 |
| Use `=YEARFRAC(D2,E2,0)` for years to maturity on 30/360, where `=DAYS360` gives 1620 against `YEARFRAC`'s 1621 days from 28 February 2027 to 31 August 2031 | `bondmath.years_to_maturity(as_of, maturity)`, equal to `YEARFRAC` on all 200 bonds | 2 | Week 3, Day 2 |
| Divide two bumped `PRICE` cells for spread duration, multiply for DTS, and total buckets with `SUMIFS` | Write `spread_duration` and `dts`, and group each bond's share of the book's DTS | 2 | Week 3, Day 3 |
| Add a calculated field to a pivot table, and run a What-If Data Table over a whole-book reprice | Group by sector, and reprice the book under rate and spread scenarios | 2 | Week 3, Day 4 |
| Price the month-end bond with `=COUPNCD(DATE(2026,11,30),DATE(2033,8,31),2,0)` and `PRICE`, the final-period bond with `PRICE`'s simple interest, and check the risk report workbook with `=SUM(R2:R200)` and `=SUMPRODUCT(N2:N200,P2:P200)/SUM(N2:N200)` | `coupon_dates`, `price`, and `dirty_price` on the two special bonds, and the workbook read back with `pd.read_excel(sheet_name=None)` and summed | 2 | Week 3, Day 5 |
| Count accrued on basis 0, `COUPDAYBS(...,2,0)/COUPDAYS(...,2,0)`, 1.375, beside basis 1 over `COUPNCD` less `COUPPCD`, 1.3825966 | `accrued_interest(..., 2, '30/360')` against an assistant's `'ACT/ACT'`, caught by a test against Excel's accrued | 2 | Week 3, Day 5 |
| Read a straight line between two tenors with `=FORECAST.LINEAR(6.4,B2:B3,A2:A3)`, yields before tenors; swapped, it returns 31.2 and no error | `left_yield + weight * (right_yield - left_yield)`, 5.16 at 6.4 years | 2 | Week 3, Day 1 |
| Find the bracket with `=MATCH(D1,A2:A15,1)`, counted from 1, and its two tenors with `INDEX` | A `while` loop that steps right while the tenor is short: positions 9 and 10, counted from 0 | 2 | Week 3, Day 1 |
| Interpolate any tenor inside a curve with `FORECAST.LINEAR` fed two points by `INDEX` and `MATCH`; it gives `#N/A` below the first tenor and `#REF!` at or past the last | `bondmath.interpolate_yield(tenor, tenors, yields)`, flat beyond the ends, within 8.9e-16 percent of Excel at 13 tenors | 2 | Week 3, Day 1 |
| Read the file's curve at each bond's own years with `=ROUND(3.55+1.05*(1-EXP(-G2/7)),3)` | `round(3.55 + 1.05 * (1 - math.exp(-years / 7)), 3)` | 2 | Week 3, Day 2 |
| Take the spread to that curve with `=(F2-J2)*100`, the yield typed in percent, so no `/100` | `bondmath.spread_to_curve_bp(y, t, [t], [c])` on a one-point curve, which rebuilds the `oas` column to 2.3e-13 bp | 2 | Week 3, Day 2 |
| Take the spread to the ten-tenor table with `=(F2-H2)*100`, the straight line from `FORECAST.LINEAR` in H2 | `bondmath.spread_to_curve_bp(y, t, curve_tenors, curve_yields)`: 147.41 bp where the file says 147 | 2 | Week 3, Day 2 |
| Measure spread duration in cells with `=(B2-B3)/(2*0.0001)/(B1+B4)`, two `PRICE` cells 1 bp each side over the dirty price, and set it beside `=MDURATION(...)` | `bondmath.spread_duration(...)`, 2.78e-07 years above `modified_duration` for Bezane | 2 | Week 3, Day 3 |
| Move the spread inside `PRICE` as `(4.136+(147+1)/100)/100`, which gives the price of the yield moved 1 bp, `=B11-B3` returning 0 | `bondmath.price(..., curve_pct + (spread_bp + 1) / 100)` | 2 | Week 3, Day 3 |
| Total the book's DTS with `=SUMPRODUCT(G2:G201,M2:M201)/SUM(G2:G201)` and each bucket's with `=SUMIFS(O2:O201,B2:B201,"BBB")` | `(market_value * dts_bm).sum() / total_value`, and `groupby('bucket')` | 2 | Week 3, Day 3 |
| Weight the book with `=SUMPRODUCT(N2:N201,S2:S201)/SUM(S2:S201)`, 6.254777411342787, where `=AVERAGE(N2:N201)` gives 6.470405 | `bondmath.weighted_average(values, weights)`, equal to the last digit | 2 | Week 3, Day 4 |
| Value the book with `=SUMPRODUCT(R2:R201,I2:I201+K2:K201)/100`, and weight its spread and DTS by `market_value` with `SUMPRODUCT` over `SUM` | `holdings['market_value'].sum()`, and `weighted_average` on `oas` and `dts` | 2 | Week 3, Day 4 |
| Reprice the book in one column at the shift in Y1, `=PRICE(A2,H2,G2/100,(L2+$Y$1/100)/100,100,2,0)`, and run every shift with a What-If Data Table, `=TABLE(,Y1)` | `reprice(...)` at four parallel shifts: +100 bp is -29,134,835.97 dollars in both | 2 | Week 3, Day 4 |
| Weight each sector's duration with a PivotTable: a helper column `=S2*N2`, `sector` in Rows, and a calculated field `=mv_x_duration/market_value` | `groupby('sector')` sums divided after, equal in all ten sectors | 2 | Week 3, Day 4 |
| Build a request URL in cells with `&` and `ENCODEURL`, `=ENCODEURL("a b&c=d/e?f")` giving `a%20b%26c%3Dd%2Fe%3Ff`, and load FRED's key-free `fredgraph.csv` with Power Query From Web, where `=WEBSERVICE` shows `#VALUE!` | Build the request in code, `quote(..., safe='')` equal to `ENCODEURL`, and read the key from outside the code so it is never typed into a cell or a file | 3 | Week 1, Day 1 |
| Hide a key in column B and save as `.xlsx`: it stays in `xl/sharedStrings.xml` and is back in B1 on reopening | Never type the key: `get_secret` reads it from the environment, Colab's Secrets panel, or `.env` | 3 | Week 1, Day 1 |
| Load FRED's JSON with Power Query (`Json.Document`, `Table.FromRecords`): 43 rows, every value text, `.` on 2026-09-07; `=VALUE(".")` shows `#VALUE!`, `=IFERROR(VALUE(B2),NA())` `#N/A`, and `Table.SelectRows(..., each [value] <> ".")` before typing leaves 42 numbers | Parse the answer with `json.loads`, read `.` as `NaN` with `errors='coerce'`, and drop it with `dropna`, never as 0 | 3 | Week 1, Day 2 |
| Count weekdays with `=NETWORKDAYS(A2,A2941)` 3,066 against `=COUNT(A2:A2941)` 2,940, 126 apart; with the seven 2026 dates in H2:H8 as the holiday list, `NETWORKDAYS` gives the file's 190 rows of 2026 and 21 in September, and `=WORKDAY(DATE(2026,9,4),1)` gives Labor Day, 2026-09-07, where `=WORKDAY(DATE(2026,9,4),1,H2:H8)` gives 2026-09-08 | `missing_weekdays` takes the market calendar from the file's own dates: 126 weekdays with no row | 3 | Week 1, Day 3 |
| Number the day of the week with `=WEEKDAY(DATE(2026,9,7),2)` 1, Monday first, and `=WEEKDAY(DATE(2026,9,7))` 2, Sunday first | `.dayofweek` counts Monday as 0 | 3 | Week 1, Day 3 |
| See `=XLOOKUP(DATE(2026,9,7),A2:A2941,B2:B2941)` return `#N/A` on Labor Day, a date with no row, and 4.8 on 2026-09-08 | `align` joins series inner or outer on their dates and fills nothing: an outer join leaves `NaN` | 3 | Week 1, Day 3 |
| Flag a stale value with `=AND(C4=C3,C3=C2)` filled down D4:D2941, and count the flags with `=COUNTIF(D4:D2941,TRUE)`: 4 in the synthetic IG spread | `stale_runs` reports each run of three or more identical values: 4 IG runs, none of five or more | 3 | Week 1, Day 3 |
| Find a month's last market date with `EOMONTH` and `MAXIFS`, look up a value as of a date with `XLOOKUP` match mode -1, and group a pivot table by month | Take the last observation of each week or month, labelled by its own date, and the as-of value | 3 | Week 1, Day 4 |
| Append and merge files with Power Query, and check a sheet with `SUMPRODUCT`, `UNIQUE`, and `COUNTBLANK` | Build one checked daily dataset from two files, and cache a download | 3 | Week 1, Day 5 |
| Keep an old copy of a workbook, which still holds a deleted key | The commit history | 3 | Week 1, Day 1 |
| Separate rows from numbers with `=COUNTA(B2:B44)` 43, `=COUNT(B2:B44)` 42, and `=COUNTIF(B2:B44,".")` 1 | `len(obs)`, and the dots counted with `(obs['value'] == '.').sum()` | 3 | Week 1, Day 2 |
| Compare `=AVERAGE(B2:B44)` 4.8367, the text skipped, with `=SUM(B2:B44)/ROWS(B2:B44)` 4.7242 | `mean` with the dot dropped, and with `fillna(0.0)`: 11.2 bp apart | 3 | Week 1, Day 2 |
| Find the first run over FRED's 120 requests a minute with `=INT(120/11)+1`, 11 | Count 11 requests a run, and see run 11 pass the limit at 121 | 3 | Week 1, Day 2 |
| Type the column in Power Query with `Table.TransformColumnTypes`: the dot loads as an empty cell, `=(D28-D27)*100` reads it as 0 and gives 480, and `=(D28-D26)*100` from Friday gives 2 | `fillna(0.0)` then `.diff()` invents a 480 bp move; with the dot dropped first, Tuesday's change is 2 bp from Friday | 3 | Week 1, Day 2 |
| See a line chart plot the text `.` at 0 and leave an empty cell as a gap, by default | Two panels: the dot as `NaN`, a gap, and as 0, a fall to zero and back | 3 | Week 1, Day 2 |
| Count calendar days with `=A2941-A2+1`, 4,292 | `len(pd.date_range(first, last))` | 3 | Week 1, Day 3 |
| Carry a value forward with `=IF(T3="",U2,T3)`: Labor Day takes Friday's 4.78 and `=(U3-U2)*100` gives a 0 bp change on a day with no market | `.ffill()` on a displayed copy only: the filled Labor Day adds a zero change | 3 | Week 1, Day 3 |
| Find a month's first, mean, and high with `XLOOKUP`, `AVERAGEIFS`, and `MAXIFS` | First, mean, and high | 3 | Week 1, Day 4 |
| Test a month end with `COUNTIF(dates,EOMONTH(...))` | `isin` on month ends | 3 | Week 1, Day 4 |
| Open a CSV of full-digit thirds and see the values change | `float_precision="round_trip"` | 3 | Week 1, Day 5 |
| Write `=(B3-B2)*100` for a change in bp, `XLOOKUP` with `EDATE` for a one-month change, and `MAX` with `XLOOKUP` for the date of the largest move | Compute changes in bp over rows and over calendar periods, and price returns in percent | 3 | Week 2, Day 1 |
| Fill `STDEV.S` down a fixed-size range, with `STDEV.P`, `OFFSET`, and `*SQRT(252)` beside it | Compute rolling volatility over a trailing window of rows, and test that it uses no future data | 3 | Week 2, Day 2 |
| Use `STANDARDIZE` filled down, and `=COUNTIF(C3:C254,"<="&C254)/COUNT(C3:C254)*100` for a percentile rank, beside `PERCENTRANK.INC`, `RANK.EQ`, and `RANK.AVG` | Write `rolling_zscore` and `rolling_percentile_rank` and match Excel on every row of 2026 | 3 | Week 2, Day 3 |
| Fill slope and butterfly formulas down the Treasury sheet, and weight a butterfly with `PRICE` and `MDURATION` | Compute slopes and butterflies in bp, and DV01-neutral weights from your own `bondmath` | 3 | Week 2, Day 4 |
| Build a summary sheet for one date with `XMATCH`, `XLOOKUP`, `INDEX`, `OFFSET`, `STANDARDIZE`, and `COUNTIF` | Build every measure as of one date in one table that reads nothing after it | 3 | Week 2, Day 5 |
| See `=(B440-B439)*100` hold more digits than it shows | `ten.iloc[-1] - ten.iloc[-2]` | 3 | Week 2, Day 1 |
| Choose `=D440-D439` or `*100` by the column's units | `change_bp(ig, percent_units=False)` and the default | 3 | Week 2, Day 1 |
| Step back a month with `=EDATE(DATE(2026,3,31),-1)` | `pd.DateOffset(months=1)` | 3 | Week 2, Day 1 |
| Rank moves with `=TAKE(SORT(ROUND(ABS(C251:C440),6),,-1),6)` and `LARGE` | `nlargest` | 3 | Week 2, Day 1 |
| Count large moves with `=SUMPRODUCT(--(ABS(C251:C440)>=10))` or two `COUNTIF`s | A threshold count | 3 | Week 2, Day 1 |
| Fill a histogram bin with `=COUNTIFS(C251:C440,">=0.5",C251:C440,"<1.5")` | A histogram bin | 3 | Week 2, Day 1 |
| Conditional Formatting, Data Bars and the Top 1 rule | `.bar` and `highlight_max` | 3 | Week 2, Day 1 |
| Count a calendar window with `=COUNTIFS($A$3:$A$2941,">"&A3-30,$A$3:$A$2941,"<="&A3)` | `rolling("30D").count()` | 3 | Week 2, Day 2 |
| Fill `=AVERAGE(A$1:A1)` down | `min_periods=1` | 3 | Week 2, Day 2 |
| Size the sample correction and the annualising factor with `=SQRT(21/20)` and `=SQRT(252)` | The ratio and the factor | 3 | Week 2, Day 2 |
| Count rows by year with `COUNTIFS` | `groupby(index.year).size()` | 3 | Week 2, Day 2 |
| Find the peak and its date with `MAX` and `XLOOKUP` | `max` and `idxmax` | 3 | Week 2, Day 2 |
| Compare two windows with `=G254/K254` | `vol_ratio` | 3 | Week 2, Day 2 |
| Find a window's extremes and the high's date with `MIN`, `MAX`, and `=XLOOKUP(MAX(C3:C254),C3:C254,A3:A254)` | `min`, `max`, and `idxmax` | 3 | Week 2, Day 3 |
| Score a day three ways with `AVERAGE`, `STDEV.S`, and `COUNTIF` | The z-score and the rank, three ways | 3 | Week 2, Day 3 |
| Leave today out with `=STANDARDIZE(C254,AVERAGE(C2:C253),STDEV.S(C2:C253))` | The z-score against the 252 rows before today | 3 | Week 2, Day 3 |
| Count `=(4.12-3.80)*100` and `=(4.13-3.81)*100` as a tie with `COUNTIF` over `COUNT`, 100 | `float(f'{value:.15g}')`, 15 significant digits | 3 | Week 2, Day 3 |
| Rank ties with `=RANK.EQ(7,A1:A10,1)`, `=RANK.AVG(7,A1:A10,1)`, and `=COUNTIF(A1:A10,"<="&7)/COUNT(A1:A10)*100` | `rank(method='min')`, `'average'`, and `rank(pct=True, method='max')` | 3 | Week 2, Day 3 |
| See `STANDARDIZE` over a flat window show `#NUM!`, and `=IFERROR(STANDARDIZE(...),NA())` show `#N/A` | `NaN` on a flat window | 3 | Week 2, Day 3 |
| Find the low in 2s10s and its date with `MIN` and `XLOOKUP` | `min` and `idxmin` | 3 | Week 2, Day 4 |
| Write a fly the other way round with `=(B+D-2*C)*100` | The other sign | 3 | Week 2, Day 4 |
| Count inverted days with `COUNTIF` | Sign counts | 3 | Week 2, Day 4 |
| Count a run with `=IF(E2<0,IF(N(E1)<0,F1+1,1),0)`, then `MAX` | `cumsum` and `groupby` runs | 3 | Week 2, Day 4 |
| Correlate changes with `=CORREL(F3:F752,G3:G752)` | `.corr` | 3 | Week 2, Day 5 |
| Find the mean absolute move with `SUMPRODUCT(ABS())/COUNT`, and `MIN` | The mean absolute move and the largest fall | 3 | Week 2, Day 5 |
| Count negative days with `COUNTIF` | Negative days | 3 | Week 2, Day 5 |
| Find the same-direction share with `SUMPRODUCT`, and the gap with `MIN` and `MAX` | The share and the gap | 3 | Week 2, Day 5 |
| Use `COUNTIFS`, `SUMIFS`, `AVERAGEIFS`, `FILTER`, `TAKE` with `SORTBY`, and a pivot table | Write `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, and `LIMIT` in SQL, each checked against pandas | 3 | Week 3, Day 1 |
| Join with `XLOOKUP` or Power Query Merge, and find repeated keys with `COUNTIF` | Join tables in SQL, catch a join that duplicates rows, and use window functions for daily changes and month ends | 3 | Week 3, Day 2 |
| Check a suggested formula, `PERCENTRANK.INC`, against `COUNTIF` over `COUNT`, and a DV01 built from cells | Test code written in the style of an AI assistant against your own functions and Excel's values | 3 | Week 3, Day 3 |
| Open the snapshot workbook and check its numbers with `SUMIFS`, `STANDARDIZE`, and `COUNTIF` | Write a daily market snapshot to HTML and Excel from one function that runs on any date | 3 | Week 3, Day 4 |
| Test a pasted extract's dates and units with `DATE`, `WEEKDAY`, `COUNTIF`, and `IFERROR(VALUE(...),NA())` | Clean a vendor extract with checks that stop, reconcile it, and run the snapshot on two dates | 3 | Week 3, Day 5 |
| Unpivot with Power Query's `Table.UnpivotOtherColumns`, then filter the blanks | `melt` and `dropna` | 3 | Week 3, Day 1 |
| Test a date range with two tests in `COUNTIFS` | `BETWEEN` | 3 | Week 3, Day 2 |
| Summarize a month with `MINIFS`, `MAXIFS`, and `AVERAGEIFS` | `GROUP BY substr(date, 1, 7)` | 3 | Week 3, Day 2 |
| Take a month label with `=TEXT(DATE(2026,9,30),"yyyy-mm")` | `substr(date, 1, 7)` | 3 | Week 3, Day 2 |
| See text dates compare wrongly with `="09/30/2026"<"10/02/2025"` | SQL text comparison | 3 | Week 3, Day 2 |
| Build dummy columns with `=--(D2="AAA")`, fit them with `LINEST`, and score the test rows with `TREND` | Encode ratings with a named reference level and fit a multiple regression | 4 | Week 1, Day 2 |
| `=COUNTIF(D2:D616,"A")` | `value_counts` of the rating column | 4 | Week 1, Day 2 |
| `AVERAGEIF` for BBB minus `AVERAGEIF` for A | Difference of two group means | 4 | Week 1, Day 2 |
| `=SORT(UNIQUE(D2:D616))`, which puts A- before A+, the reverse of Python | `sorted` on the rating labels | 4 | Week 1, Day 2 |
| `=LINEST(A2:A616,F2:X616,FALSE,TRUE)` | `LinearRegression(fit_intercept=False)` | 4 | Week 1, Day 2 |
| `=SUBSTITUTE(SUBSTITUTE(D2,"+",""),"-","")` | `.str.rstrip("+-")`, the letter grade | 4 | Week 1, Day 2 |
| Read `LINEST`'s standard errors, and compute p-values with `T.DIST.2T`, intervals with `T.INV.2T`, a VIF with `1/(1-R2)`, and a joint F-test with `F.DIST.RT` | Read statsmodels' coefficient table, test sector jointly, and measure multicollinearity | 4 | Week 1, Day 3 |
| `=100*(EXP(Z2)-1)` | A log coefficient read as a percent | 4 | Week 1, Day 3 |
| `=INDEX(LINEST(B2:B308,C2:M308,TRUE,TRUE),2,10)` | `fit_half.bse`, a standard error on half the rows | 4 | Week 1, Day 3 |
| `=CORREL(D2:D616,N2:N616)` | `corr` between two features | 4 | Week 1, Day 3 |
| `=SUMPRODUCT(--(D2:D616=O2:O616))` | Count of rows where two columns are equal | 4 | Week 1, Day 3 |
| Take `LN` and `EXP` of spreads, run Breusch-Pagan by hand with `LINEST` and `CHISQ.DIST.RT`, and compute Q-Q points with `NORM.S.INV` | Check a regression's assumptions with residual plots and tests, and model log spreads | 4 | Week 1, Day 4 |
| `=SKEW.P(A2:A616)`, where `SKEW` gives a different 4.44 | `scipy.stats.skew` | 4 | Week 1, Day 4 |
| `=100*(EXP(INDEX(LINEST(...),1,10))-1)` | `percent_effect` of a log-model coefficient | 4 | Week 1, Day 4 |
| `=AVERAGE(EXP(AI2:AI616))` | Mean of `exp(residual)`, the retransformation factor | 4 | Week 1, Day 4 |
| Standardize with `STANDARDIZE` and `STDEV.P`, and solve ridge in closed form with `MMULT`, `MINVERSE`, and `MUNIT` | Fit ridge and lasso inside a pipeline that scales on the training rows only | 4 | Week 1, Day 5 |
| `=SUMSQ(S2:U2)` | Sum of squared coefficients, the ridge penalty | 4 | Week 1, Day 5 |
| `=10^SEQUENCE(13,1,-3,0.5)` | `np.logspace(-3, 3, 13)`, the alpha grid | 4 | Week 1, Day 5 |
| `=LN(900/80)` | The generator's rating effect on the log scale | 4 | Week 1, Day 5 |
| Fill a logistic probability formula, sum a log-likelihood column, and maximise it with Solver, the non-negative box turned off | Fit a logistic regression and read odds ratios with `exp` | 4 | Week 2, Day 1 |
| `=SLOPE` and `=INTERCEPT` on a 0 and 1 column | `LinearRegression` on the default flag | 4 | Week 2, Day 1 |
| `=1/(1+EXP(-2))` | The logistic curve at a score of 2 | 4 | Week 2, Day 1 |
| `=LN(0.8/(1-0.8))` | Log odds of a probability | 4 | Week 2, Day 1 |
| `=AVERAGEIFS(A:A,B:B,2)`, then the odds and `LN` | Default rate by repayment code | 4 | Week 2, Day 1 |
| `=EXP(L2-NORM.S.INV(0.975)*M2)` and `=EXP(L2+NORM.S.INV(0.975)*M2)` | `conf_int` on the odds scale | 4 | Week 2, Day 1 |
| One account's probability from its coefficients | `logistic_probability` | 4 | Week 2, Day 1 |
| `=STDEV.P` | `StandardScaler`'s `scale_` | 4 | Week 2, Day 1 |
| `=CORREL` | `corr` | 4 | Week 2, Day 1 |
| A fitted curve filled into a scatter chart | matplotlib curve over the points | 4 | Week 2, Day 1 |
| Count a confusion matrix with `COUNTIFS` against a threshold cell | Count the confusion matrix and compute precision, recall, and F1 for the default class | 4 | Week 2, Day 2 |
| `=COUNTIF(B:B,">="&F$1)` | Number of accounts flagged at a threshold | 4 | Week 2, Day 2 |
| F1 of the model that flags every account | `f1_score` | 4 | Week 2, Day 2 |
| `COUNTIFS` over `COUNTIF` at a threshold of 0.7 | Precision | 4 | Week 2, Day 2 |
| `=F2/(F2+F3)` | Recall of row 0 | 4 | Week 2, Day 2 |
| `=AVERAGE(F2/(F2+F3),F5/(F5+F4))` | Macro recall | 4 | Week 2, Day 2 |
| `=2*F4+F3` | Weighted cost total | 4 | Week 2, Day 2 |
| `=(G3-F3)/(G5-F5)` | False flags per extra default caught | 4 | Week 2, Day 2 |
| A histogram chart of the scores | matplotlib histogram | 4 | Week 2, Day 2 |
| List thresholds with `SORT(UNIQUE(...))`, trace the ROC with `COUNTIFS`, take the AUC with `SUMPRODUCT`, and pick a threshold with `MAXIFS` | Draw ROC and precision-recall curves, and choose a threshold for a target recall on validation rows | 4 | Week 2, Day 3 |
| `=COUNTIF(...)*COUNTIF(...)` | Number of default and non-default pairs behind the AUC | 4 | Week 2, Day 3 |
| `=AVERAGE(A:A)` | The precision floor, the default rate | 4 | Week 2, Day 3 |
| `=SUMPRODUCT((B2:B6001>=LARGE(B2:B6001,100))*A2:A6001)` | Defaults among the top 100 scores | 4 | Week 2, Day 3 |
| `=AVERAGE(FILTER(A:A,B:B<=PERCENTILE.INC(B:B,0.1)))`, and the same on the scores | One calibration group | 4 | Week 2, Day 3 |
| Compute Gini with `COUNTIFS`, a leaf's default share with `AVERAGEIFS`, and write a small tree as nested `IF` | Grow, prune, and read a decision tree | 4 | Week 2, Day 4 |
| `=COUNTIF(B:B,">1.5")` | Accounts a one-question tree flags | 4 | Week 2, Day 4 |
| `COUNTIFS` over `COUNTIF` | Recall of the one-question tree | 4 | Week 2, Day 4 |
| `=1-(0.9^2+0.1^2)` | Gini of a 90 and 10 group | 4 | Week 2, Day 4 |
| Open the results workbook, recompute precision and recall, and find the best model with `INDEX` and `MATCH` | Compare three models on validation rows, open the test rows once, and write the comparison to Excel | 4 | Week 2, Day 5 |
| `=MEDIAN` and `=SKEW` | pandas `median` and `skew` | 4 | Week 2, Day 5 |
| Fill `SLOPE(OFFSET(...))` down a trailing window, fit one fold with `TREND`, and compare a whole-history `STANDARDIZE` with a trailing one | Validate on dated rows with walk-forward splits, and show lookahead in a feature | 4 | Week 3, Day 1 |
| `=CORREL(E3:E2941,E2:E2940)` and `=CORREL(H4:H2941,H3:H2940)` | `autocorr(1)` on levels and changes | 4 | Week 3, Day 1 |
| `=MEDIAN(ABS(H3:H2941))` | `.abs().median()` | 4 | Week 3, Day 1 |
| `=INDEX(A2:A2941,MATCH(MIN(E2:E2941),E2:E2941,0))` | `idxmin()` | 4 | Week 3, Day 1 |
| `=COUNTIF(E884:E1009,">"&MAX(E2:E883))` | Test rows above the training maximum | 4 | Week 3, Day 1 |
| `=LINEST(E2:E505,B2:C505)`, which returns the columns in reverse order | `coef_` and `intercept_` | 4 | Week 3, Day 1 |
| `=SUMXMY2(N507:N631,N506:N630)/SUMSQ(N506:N631)` | `durbin_watson` | 4 | Week 3, Day 1 |
| Measure distance to each centre with `SQRT(SUMXMY2(...))`, assign with `MATCH(MIN(...))`, and update the centres with `AVERAGEIF` | Scale the bonds and run K-means, with the elbow and the silhouette | 4 | Week 3, Day 2 |
| `=STDEV.S(B2:B822)` | `.std()` | 4 | Week 3, Day 2 |
| `=LN(B2)` | `np.log` | 4 | Week 3, Day 2 |
| `=(MAX(B2:B822)-AVERAGE(B2:B822))/STDEV.P(B2:B822)` | The largest z-score, `z.max()` | 4 | Week 3, Day 2 |
| `=SQRT(SUMXMY2(B3:E3,$B$2:$E$2))` with `INDEX` and `MATCH(MIN(...))` | The nearest bond | 4 | Week 3, Day 2 |
| `=MIN(L2:O2)^2`, then `=SUM(Q2:Q822)` | `inertia_` | 4 | Week 3, Day 2 |
| `SUMIF` and `COUNTIF`, `AVERAGEIF`, `MINIFS`, and `(b-a)/MAX(a,b)` | `silhouette_samples` for one bond | 4 | Week 3, Day 2 |
| Count clusters with a pivot table, and take medians with `MEDIAN(IF(...))`, which a pivot table cannot give | Build a hierarchical clustering, cut it, and profile the clusters in their own units | 4 | Week 3, Day 3 |
| `COUNTIF`, `SUMIF`, and `MEDIAN(IF(...))` on the ticker column | `groupby().agg()` | 4 | Week 3, Day 3 |
| `=CORREL(A2:A11176,B2:B11176)` | `cophenet` | 4 | Week 3, Day 3 |
| `=AVERAGEIF($H$2:$H$151,1,$G$2:$G$151)` | `groupby().mean()` | 4 | Week 3, Day 3 |
| `=CORREL(B2:B151,F2:F151)` and `=CORREL(D2:D151,E2:E151)` | `.corr()` | 4 | Week 3, Day 3 |
| Build a `COVARIANCE.S` grid, and score each date with `MMULT` of the centred changes | Find level, slope, and curvature with PCA on the Treasury curve | 4 | Week 3, Day 4 |
| `=SUMPRODUCT(B2:B9,B2:B9)` and `=SUM(C2:C9)` | A loading's length and the sign rule | 4 | Week 3, Day 4 |
| Check the capstone's results workbook with `COUNTIFS` against its threshold | Compare three models on a new file, test once, and write the results to Excel | 4 | Week 3, Day 5 |
| Chart a comparison of models as a clustered column or line chart, and shade a table with a conditional formatting color scale | Draw every comparison as a chart and show it as a formatted table with the best value in each column marked | 4 | Week 1, Day 2 to Week 3, Day 4 |
| Compute the share a sample leaves out with `=(1-1/n)^n`, count pasted positions with `FREQUENCY` and `COUNTIF`, and see `RANDARRAY` redraw on every recalculation | Draw a seeded bootstrap, count its rows, and measure how ten trees on ten samples disagree | 5 | Week 1, Day 1 |
| `=1-AVERAGE(Q2:Q6001)` on the pasted validation outcomes | `1 - y_valid.mean()` | 5 | Week 1, Day 1 |
| `=COUNTIF(M2:M6001,">=0.5")` on the ten-tree average | `(average_full >= 0.5).sum()` | 5 | Week 1, Day 1 |
| `=COUNTIFS(Q2:Q6001,1,M2:M6001,">=0.5")`, then `=R3/R2` for precision | Precision from `mlkit.classification_metrics` | 5 | Week 1, Day 1 |
| `=STDEV.P(B2:K2)`, `=COUNTIF(B2:K2,">=0.5")`, and `=AVERAGE(B2:K2)` across ten trees | `ten.std(axis=1, ddof=0)`, `(ten >= 0.5).sum(axis=1)`, and `proba_ten.mean(axis=1)` | 5 | Week 1, Day 1 |
| Average pasted tree columns with `AVERAGE`, and score a vote with `SUMPRODUCT` | Bag trees by hand and with scikit-learn, and read the out-of-bag score as the accuracy it is | 5 | Week 1, Day 2 |
| Count columns per split with `INT(SQRT(19))`, the chance one is tried with `COMBIN`, and two trees' agreement with `CORREL` | Fit a random forest, measure tree correlation, and summarise a search's fold scores | 5 | Week 1, Day 3 |
| `=ROWS(A2:A18001)/(2*COUNTIF(A2:A18001,1))` for a class weight, and `AVERAGE` and `STDEV.P` of the fold scores | `compute_class_weight("balanced")` and `cv_results_` | 5 | Week 1, Day 3 |
| Rank two importance columns with `RANK.EQ`, and compute a ROC AUC from `RANK.AVG` and `SUMIF` | Compare impurity and permutation importance, and catch a column of noise that one of them ranks second | 5 | Week 1, Day 4 |
| `=AVERAGE(A2:A18001)` and `=STDEV.S(A2:A18001)` on the noise column | `X_train["noise"].mean()` and `.std()` | 5 | Week 1, Day 4 |
| `=CORREL(A2:A18001,B2:B18001)` for the noise column against the outcome | `np.corrcoef(X_train["noise"], y_train)` | 5 | Week 1, Day 4 |
| `=COUNTA(UNIQUE(A2:A18001))` for the distinct values in a column | `X_train.nunique()` | 5 | Week 1, Day 4 |
| `=RANK.AVG(B2,$B$2:$B$21,1)` filled down, then `=CORREL(E2:E21,F2:F21)` on the ranks | `.corr(method="spearman")` | 5 | Week 1, Day 4 |
| `=AVERAGE(A2:A6)` and `=STDEV.P(A2:A6)` of five group shuffles | `np.mean(group_drops)` and `np.std(group_drops)` | 5 | Week 1, Day 4 |
| `=SUM(B2:B7)` of the six bills' permutation drops | `table.loc[bills, "permutation"].sum()` | 5 | Week 1, Day 4 |
| `=1-((B2/A2)^2+(C2/A2)^2)` for a node's Gini impurity | `tiny_tree.tree_.impurity` | 5 | Week 1, Day 4 |
| `=(A2*D2-A3*D3-A6*D6)/$A$2` for one split's credit, then `=(F3+F6)/(F2+F3+F6)` for a column's share | `split_credits(tiny_tree, tiny_columns)` and `tiny_tree.feature_importances_` | 5 | Week 1, Day 4 |
| Turn a fitted log spread into bp with `EXP`, average the misses with `AVERAGE(ABS(...))`, and compute R-squared with `SUMXMY2` and `DEVSQ` | Score OLS, a tree, and a forest on the spread cross-section by cross-validation and by issuer | 5 | Week 1, Day 5 |
| `=COUNTIF(C2:C616,C2)` for the bonds in one leaf | `same_leaf.sum()` | 5 | Week 1, Day 5 |
| `=AVERAGEIF(C2:C616,C2,B2:B616)`, then `=EXP(E2)` for the leaf's fitted spread in bp | `y[same_leaf].mean()` and `np.exp(fitted_log[0])` | 5 | Week 1, Day 5 |
| `=COUNTIFS(A2:A18001,1,B2:B18001,">="&E1)/COUNTIF(A2:A18001,1)` for recall at a threshold | `(oof_log >= threshold_log)[y_train == 1].mean()` | 5 | Week 1, Day 5 |
| `=AVERAGEIF(A2:A616,"High Yield",B2:B616)` and the same for "Investment Grade" | `residuals.abs().groupby(grade).mean()` | 5 | Week 1, Day 5 |
| Run an AdaBoost round with `SUMPRODUCT`, `LN`, and `EXP`, and see `LOG` return base 10 | Run three AdaBoost rounds by hand and match scikit-learn's stump weights | 5 | Week 2, Day 1 |
| `=COUNTIF(A2:A18001,"<=1.5")` and `=AVERAGEIFS(B2:B18001,A2:A18001,"<=1.5")` on each side of a stump's split | `(X_train["PAY_0"] <= 1.5).sum()` and `y_train[yes_side].mean()` | 5 | Week 2, Day 1 |
| `=COUNTIFS(C2:C18001,1,A2:A18001,"<=1.5")` for the misses on one side | `((missed == 1) & yes_side).sum()` | 5 | Week 2, Day 1 |
| `=1/(1+EXP(2))` and `=1/(1+EXP(-2))` | `1 / (1 + np.exp(2))` | 5 | Week 2, Day 1 |
| `=1/(1+EXP(-2*I2))` filled down on the pasted votes | `ada.predict_proba(X_valid)[:, 1]`, equal within 1e-12 | 5 | Week 2, Day 1 |
| `=COUNTIF(L2:L18001,">=3")` and `=AVERAGEIFS(B2:B18001,L2:L18001,">=3")` on the rows most reweighted | `(relative >= 3).sum()` and `y_train[relative >= 3].mean()` | 5 | Week 2, Day 1 |
| Fit one boosting round from residuals with two `AVERAGEIFS` and an `IF` | Build gradient boosting from residuals and match the library to 1e-12 | 5 | Week 2, Day 2 |
| `=DEVSQ(B2:B616)` | `((y - y.mean()) ** 2).sum()` | 5 | Week 2, Day 2 |
| `=COUNTIF(A2:A616,"<="&M2)` for the rows left of a split | `(train["score"] <= 9.5).sum()` | 5 | Week 2, Day 2 |
| Add gradients with `SUMIFS` for an XGBoost leaf and its gain, and fill a log loss column with `LN` | Regularise XGBoost, stop it early on rows carved from the training rows, and compute log loss by hand | 5 | Week 2, Day 3 |
| Blend two pasted probability columns with `AVERAGE`, and apply a stack's logistic layer with `EXP` | Stack models on out-of-fold outputs and check whether the stack beats its best member | 5 | Week 2, Day 4 |
| `=COUNTIFS(A2:A6001,1,C2:C6001,">=0.5")/COUNTIF(A2:A6001,1)` for recall | `(proba_light[y_valid == 1] >= 0.5).mean()` | 5 | Week 2, Day 4 |
| `=CORREL(A2:A18001,B2:B18001)` on two out-of-fold columns | `inputs.corr()` | 5 | Week 2, Day 4 |
| Read a bootstrap interval with `PERCENTILE.INC`, and find the chosen model with `INDEX` and `MATCH` | Compare six models with bootstrap intervals and paired differences, and write the results to Excel | 5 | Week 2, Day 5 |
| Summarise five fold scores with `AVERAGE` and `STDEV.P`, not `STDEV.S` | Read a randomized search's results and report a nested score beside its best score | 5 | Week 3, Day 1 |
| `=2^3*5` and `=5^3*5` for a grid's model count | `len(ParameterGrid(...)) * 5` | 5 | Week 3, Day 1 |
| `=RANDBETWEEN(4,31)`, upper bound included | `randint(4, 32)`, upper bound excluded | 5 | Week 3, Day 1 |
| `=EXP(LN(0.05)+RAND()*(LN(0.2)-LN(0.05)))` | `loguniform(0.05, 0.2)` | 5 | Week 3, Day 1 |
| `=COUNTIF(B2:B4681,">="&F1)` and `=COUNTIFS(A2:A4681,1,B2:B4681,">="&F1)` for flagged and caught | The flagged count and the bankrupt companies caught at a threshold | 5 | Week 3, Day 1 |
| Cap a column with `MIN`, guard a ratio with `IF(OR(...),NA(),...)`, clip with `PERCENTILE.INC`, and count gaps with `COUNTBLANK` | Engineer features from financial ratios, each statistic learned inside the fold | 5 | Week 3, Day 2 |
| `=COUNTIF(...,"<0")` on a guarded ratio, which skips `#N/A` | `(debt_to_equity < 0).sum()` | 5 | Week 3, Day 2 |
| `=100*AVERAGEIFS(...)` of the class by count of gaps | `y.groupby(gaps).mean()` | 5 | Week 3, Day 2 |
| `MEDIAN`, `AVERAGE`, and `COUNTBLANK` on a column with gaps | `median()`, `mean()`, and `isna().sum()` | 5 | Week 3, Day 2 |
| Rebuild one SMOTE row with `=x+u*(nb-x)`, correct a resampled score by formula, and compute a Brier score with `SUMXMY2` | Compare class weights, resampling, and a threshold on a rare outcome, and recalibrate the score | 5 | Week 3, Day 3 |
| `=COUNTIF(A2:A4681,0)/COUNTIF(A2:A4681,1)` and `=1-AVERAGE(A2:A4681)` | The class ratio and the all-zero baseline | 5 | Week 3, Day 3 |
| `=ROWS(A2:A4681)/(2*COUNTIF(A2:A4681,1))`, and with 0 | `compute_class_weight("balanced")` | 5 | Week 3, Day 3 |
| `AVERAGE` of the out-of-fold outputs | `proba.mean()` | 5 | Week 3, Day 3 |
| Add a SHAP row with `SUM` to the model's log-odds, turn it into a probability with `EXP`, and average absolute values with `AVERAGE(ABS(...))` | Split a company's score across its ratios with SHAP values, and never read a contribution as a cause | 5 | Week 3, Day 4 |
| `=AVERAGE(E2:E4681)` on the pasted log-odds for the base value | `raw.mean()` | 5 | Week 3, Day 4 |
| `=COUNTIF(E2:E4681,"<"&B1)` and `=MEDIAN(E2:E4681)` | `(raw < base).sum()` and `np.median(raw)` | 5 | Week 3, Day 4 |
| `=1/(1+EXP(-(B1+B47)))-1/(1+EXP(-B1))` for one contribution in probability terms | The difference of two `logistic_probability` calls | 5 | Week 3, Day 4 |
| `COUNTIFS` and `AVERAGEIFS` by band of a ratio, where the criterion `""` matches empty cells | Mask counts and means by band | 5 | Week 3, Day 4 |
| Check the capstone's confusion matrix with `COUNTIFS`, its interval with `PERCENTILE.INC`, and a SHAP row with `SUM` | Compare four models on a new file, test once, describe the chosen one with SHAP values, and write the results to Excel | 5 | Week 3, Day 5 |
| Chart a comparison of models as a clustered column, bar, line, or scatter chart, add custom error bars for a spread of fold scores, and shade a table with a conditional formatting color scale | Draw every comparison as a chart and show it as a formatted table with the best value in each column marked | 5 | Week 1, Day 1 to Week 3, Day 4 |
| Use `COUNTBLANK` on each column, and `NETWORKDAYS` less `ROWS` to count absent dates | Count blanks per column and the absent market dates, then find each gap's run and kind | 5B | Week 1, Day 1 |
| Fill a blank with the cell above, `=IF(B3="",C2,B3)` | Forward fill with `ffill`, and stop it at a long outage with `limit=` | 5B | Week 1, Day 1 |
| Interpolate a gap by row position, and by date, with a few cells of arithmetic | `interpolate` linear and by time, compared against the true values held back | 5B | Week 1, Day 1 |
| Fill blanks from a second sheet with `XLOOKUP` | `combine_first` from a second source, and `update` from a corrections table, with a change log | 5B | Week 1, Day 1 |
| Flag a wrong print with `AND` and `IFERROR`: a jump that reverses the next day | The same jump-and-back rule on every column at once | 5B | Week 1, Day 1 |
| Point at the cell one row up for a lag, and take `=B3-B2` for a change in bp; score the last value with `SUMPRODUCT`, the training mean, and the drift | `shift` and `diff`, three baselines scored walk-forward, and MAE, RMSE, and a MASE of 1 for the last value | 5B | Week 1, Day 2 |
| Take a trailing `AVERAGE` and `STDEV.S`, fit AR(1) with `SLOPE` and `INTERCEPT`, and get the Dickey-Fuller statistic from `LINEST`; Excel has no ADF or KPSS test | ADF and KPSS on levels and changes, and the spurious regression of two random walks seen in `RSQ` | 5B | Week 1, Day 3 |
| Get an autocorrelation at lag k as `CORREL` of two offset ranges, or by `SUMPRODUCT` and `DEVSQ`; take Ljung-Box Q with `CHISQ.DIST.RT` and the lag-2 PACF with `LINEST` | `acf_by_hand` against `acf` and `pacf`, the confidence band, and the identification grid | 5B | Week 1, Day 4 |
| Fit AR(1) with `SLOPE` and `INTERCEPT`, find the level it pulls toward, and score its one-step values with `SUMPRODUCT`; Excel has no ARIMA fitter | AR, MA, and ARIMA walk-forward against the last value, with an AIC and BIC grid | 5B | Week 1, Day 5 |
| Write the EWMA as one recursive formula, find the half-life of its weights, and run the RiskMetrics variance recursion; `FORECAST.ETS` is named and not used | `ewma`, simple and Holt smoothing scored walk-forward, and an EWMA volatility | 5B | Week 2, Day 1 |
| Write the GARCH(1,1) variance as one recursive formula and take persistence, half-life, and long-run volatility from it; Excel has no GARCH fitter | `arch_model`, `garch_half_life`, and walk-forward GARCH against a constant size | 5B | Week 2, Day 2 |
| Build lag features with `AVERAGE`, `STDEV.S`, a `SUMPRODUCT` mean of absolute values, `WEEKDAY`, and `MONTH`, and see a leaky mean beat the honest one; Excel has no boosted trees | `lag_features` shift first then roll, and LightGBM on lags walk-forward | 5B | Week 2, Day 3 |
| Take a hedge ratio with `SLOPE`, the gap as one filled column, `STDEV.S`, a `SUMPRODUCT` count beyond 2 sd, and a half-life as `=LN(0.5)/LN(b)`; Excel has no Engle-Granger test | `hedge_ratio`, `coint`, and `half_life` on two pairs | 5B | Week 2, Day 4 |
| Forward fill with `IF`, `CORREL`, `SLOPE`, and `INTERCEPT`, score the last value and an AR(1) on held-out changes with `SUMPRODUCT`, and average the last 20 sizes | The whole workflow on two series, with the held-out years opened once | 5B | Week 2, Day 5 |
| Check the capstone's results workbook with `AVERAGE`, a ratio of means, `SUMPRODUCT` over a comparison, and `COUNTIF` | Write the results with `pd.ExcelWriter` and read every sheet back | 5B | Week 2, Day 5 |
| Multiply PD, LGD, and EAD in one cell, `=E1*E2*E3` | The exact expected loss, then a simulation that has to find it on its own | 5C | Week 1, Day 1 |
| Draw with `RAND()`, turn it into a normal draw with `NORM.S.INV`, and mirror it with `NORM.S.INV(1-A2)` | `default_rng(SEED)`, `norm.ppf`, and antithetic pairs with `antithetic_normals` | 5C | Week 1, Day 1 |
| Simulate one year per row with `IF`, take `AVERAGE` and `STDEV.S` over `SQRT(COUNT(...))`, and repeat a sheet with a one-variable Data Table | `mc_mean`: a Monte Carlo mean with its standard error | 5C | Week 1, Day 1 |
| Get the chance of k defaults with `BINOM.DIST`, and the trials for a stated precision with `ROUNDUP` and `NORM.S.INV` | `binom.pmf` against a simulated count, and `trials_needed` | 5C | Week 1, Day 1 |
| Read a historical VaR with `PERCENTILE.INC`, its expected shortfall with `AVERAGEIF` and a criterion joined by `&`, and the other percentile method with `PERCENTILE.EXC` | `var_es` on the book's 2,000 development days, and `np.quantile`'s `method` setting | 5C | Week 1, Day 2 |
| Set the normal model's VaR with `AVERAGE`, `STDEV.S`, and `NORM.S.INV`, and scale it to 10 days with `SQRT(10)` | The normal model and a fitted Student's t beside the history, and three ways to a 10-day VaR | 5C | Week 1, Day 2 |
| Count backtest exceptions with `SUMPRODUCT` over two columns, type Kupiec's statistic with `LN`, and turn it into a p-value with `CHISQ.DIST.RT` | A walk-forward backtest of a rolling VaR with `kupiec_pof` | 5C | Week 1, Day 2 |
| Count a default rate with `AVERAGEIFS` over 0s and 1s, and evaluate a fitted logistic rate with `1/(1+EXP(-(a+b*score)))` | Default rates by rating from the synthetic cohort, and a pooled logistic fit for the low-default buckets | 5C | Week 1, Day 3 |
| Take a book's expected loss with `SUMPRODUCT` and the chance of 10 or more independent defaults with `BINOM.DIST` | `loss_distribution` and the one-factor model against the independent case | 5C | Week 1, Day 3 |
| Write the Vasicek default rate in one cell with `NORM.S.DIST` and `NORM.S.INV`, and draw a beta LGD with `BETA.INV(RAND(),6,4)`; Excel has no Cholesky | `vasicek_quantile` against a large simulated group, and a Cholesky factor in numpy | 5C | Week 1, Day 3 |
| Build a Kaplan-Meier table with `COUNTIF` for the firms at risk, `COUNTIFS` for the defaults, and a running product filled down; Excel has no Kaplan-Meier function and no log-rank test | `kaplan_meier` by hand on ten firms, then on the cohort with statsmodels' `SurvfuncRight` | 5C | Week 1, Day 4 |
| Take a flat hazard as two `SUM`s and its survival as `EXP(-h*t)`, and the credit triangle as `=s/(1-R)` | A flat hazard beside the Kaplan-Meier curve, and hazards from invented spreads | 5C | Week 1, Day 4 |
| Check a fitted hazard with `1/(1+EXP(-SUMPRODUCT(...)))`, a hazard ratio with `EXP`, and its interval with `NORM.S.INV(0.975)`; Excel has no Cox model | A Cox model with covariates that change year by year, and a logistic hazard on firm-years | 5C | Week 1, Day 5 |
| Chain ten yearly hazards into survival with `PRODUCT(1-G1:G10)`, and read a decile's observed default rate with `AVERAGEIFS`; Excel has no AUC | `hazard_to_survival`, and a walk-forward hazard model scored by AUC and calibration by decile | 5C | Week 1, Day 5 |
| Take the median with `MEDIAN`, the MAD as one array formula `MEDIAN(ABS(A2:A375-MEDIAN(A2:A375)))`, and a robust z with `1.4826` written in | `robust_z` against the ordinary z-score that masks the planted prints | 5C | Week 2, Day 1 |
| Set Tukey's fences from `QUARTILE.INC`, and count flags, precision, and recall with `SUMPRODUCT` over a flag column and a label column | `iqr_flags` and `precision_recall_at` against planted off-market prints | 5C | Week 2, Day 1 |
| Invert a covariance with `MINVERSE` and take one squared Mahalanobis distance with `MMULT` and `TRANSPOSE` in one cell; Excel has no minimum covariance determinant | `mahalanobis_flags` on daily curve changes, classical against robust | 5C | Week 2, Day 2 |
| Set the chi-squared cutoff with `CHISQ.INV(0.999,4)`; Excel has no isolation forest and no local outlier factor | Isolation forest and LOF on planted field errors, scored by precision and recall | 5C | Week 2, Day 2 |
| Cut decile edges with `PERCENTILE.INC`, count shares with `FREQUENCY` divided by `COUNT`, and add the PSI as one `SUMPRODUCT((A-E)*LN(A/E))` | `psi_edges` and `psi` on the 10 Yr level, 2019-2022 against 2015-2018 | 5C | Week 2, Day 3 |
| Floor an empty bin's share with `IF(H2#<0.0001,0.0001,H2#)`, since `LN(0)` returns `#NUM!` | The empty-bin problem and the floor, swept | 5C | Week 2, Day 3 |
| Divide two `SUM`s for defaults counted over the model's count, and read the chance of so few with `POISSON.DIST(x,mean,TRUE)` | A frozen hazard model's count checked year by year | 5C | Week 2, Day 4 |
| Take the AUC from ranks: `SUMPRODUCT(RANK.AVG(A,A,1),B)`, less n(n+1)/2, over the pairs; Excel has no AUC function | `roc_auc_score` on one monitored year, inside `monitoring_report` | 5C | Week 2, Day 4 |
| Count held-out days beyond a fixed VaR with `SUMPRODUCT(--(-C2:C940>F1))`, test the count with `LN` and `CHISQ.DIST.RT`, read the chance of that many defaults or more with `1-POISSON.DIST(x-1,mean,TRUE)`, and check the results workbook with `COUNTIF` | The whole course in one risk report, with the held-out years opened once | 5C | Week 2, Day 5 |
| Fill a neuron's output `=1/(1+EXP(-($H$1+$H$2*A2)))` down a column, take its gradient with `SUMPRODUCT` over `ROWS`, and fill a 100-step descent path | Compute a log loss and its gradient by hand, check them against `tf.GradientTape`, and take gradient steps | 6 | Week 1, Day 1 |
| Maximise a log-likelihood with Solver, scale columns with `AVERAGE` and `STDEV.P`, and score a row with `SUMPRODUCT` and `EXP` | Fit one Keras neuron and show that it is a logistic regression, with the same odds ratios | 6 | Week 1, Day 2 |
| Build a hidden layer from `SUMPRODUCT`, `MAX`, and `TANH`, and count a network's weights with `=19*32+32+32*1+1` | Add hidden layers, reproduce a network's output in numpy, and count its parameters | 6 | Week 1, Day 3 |
| Count steps per epoch with `ROUNDUP`, and find the best epoch on a pasted loss column with `MATCH(MIN(...))` | Read loss curves, change the batch size, and stop early on rows carved from the training rows | 6 | Week 1, Day 4 |
| Count a confusion matrix with `COUNTIFS` on a flag column, and read a bootstrap interval with `PERCENTILE.INC` | Put a network beside logistic regression and LightGBM, with thresholds from out-of-fold outputs and paired intervals | 6 | Week 1, Day 5 |
| Compute MSE with `SUMXMY2`, MAE with `AVERAGE(ABS(...))`, a Huber row with `IF`, and standardize a column with `STDEV.P` | Fit regression networks with three losses, turn the target back to bp, and compare them with OLS by five folds | 6 | Week 2, Day 1 |
| Fill a momentum path and three Adam steps with the bias correction, and a decaying learning rate with `=$B$1*$B$2^(A6/$B$3)` | Check momentum and Adam steps against Keras, and choose an optimizer and a learning rate on the stopping rows | 6 | Week 2, Day 2 |
| Normalize a batch with `AVERAGE`, `VAR.P`, and `SQRT`, and compute Glorot's limit and He's spread with `SQRT` | Start a network from the right weights, see gradients vanish, and add batch normalization | 6 | Week 2, Day 3 |
| Drop values with `=A2*(B2>=0.2)/(1-0.2)`, and compute an L2 penalty with `SUMSQ` | Brake overfitting with L2, dropout, and early stopping, scored by five folds | 6 | Week 2, Day 4 |
| Compute balanced class weights with `ROWS` and `COUNTIF`, and a weighted log loss with `SUMPRODUCT` over `SUM` | Fit a class-weighted network, read its output as a score, and decide on weights by numbers | 6 | Week 2, Day 5 |
| Write `=(B3-B2)*100` for a change in bp, average a 20-day window with `OFFSET`, and score zero change with `AVERAGE(ABS(...))` | Build windows of past changes with no lookahead, and score a network walk-forward against carrying the last value forward | 6 | Week 3, Day 1 |
| Take a SimpleRNN and an LSTM step with `TANH`, `EXP`, and `MMULT`, and compare two spreads with `STDEV.P` | Fit SimpleRNN, LSTM, and GRU networks walk-forward, and check one LSTM step against Keras | 6 | Week 3, Day 2 |
| Fill a weighted moving sum `=SUMPRODUCT(B2:B6,$K$2:$K$6)+$K$7` down a column, then pool with `MAX` and `AVERAGE` | Fit a one-dimensional convolution, feed all 11 tenors in as channels, and keep same-day changes out | 6 | Week 3, Day 3 |
| Average errors by fold with `AVERAGEIFS`, and count the folds a rule wins with `COUNTIF` over `COUNT` | Choose a sequence model on the development years, open the held-out years once, and write the results to Excel | 6 | Week 3, Day 4 |
| Check the capstone's workbook with `AVERAGE`, `STDEV.P`, paired differences, `COUNTIFS`, and `PERCENTILE.INC` | Compare a network with LightGBM by paired folds on three fold seeds, with intervals, and write the results to Excel | 6 | Week 3, Day 5 |
| Chart a loss curve or a comparison of networks as a line, clustered column, bar, or histogram chart, set a logarithmic axis, and shade a grid with a conditional formatting color scale | Draw every loss curve and every comparison as a chart and show it as a formatted table with the best value in each column marked | 6 | Week 1, Day 1 to Week 3, Day 4 |
| Find a word with `SEARCH` and `FIND`, count it with `LEN` and `SUBSTITUTE` (a substring count), split a sentence with `TEXTSPLIT`, and pull the target range with `REGEXEXTRACT` | Normalize look-alike characters, pull numbers out of text with regular expressions, and split text into tokens | 7 | Week 1, Day 1 |
| Count the statements that hold a word with `COUNTIF(range,"*inflation*")`, compute an IDF with `LN`, scale a row with `SQRT(SUMSQ(...))`, and a cosine with `SUMPRODUCT` | Build TF-IDF by hand, check it against scikit-learn, and compare documents by cosine similarity | 7 | Week 1, Day 2 |
| Count a confusion matrix with `COUNTIFS` on item codes stored as text, and see `COUNTIF` count "2.1" as "2.10" where `EXACT` does not | Train a TF-IDF classifier on 8-K sections split by date, catch the heading leak, and report recall on the rare items | 7 | Week 1, Day 3 |
| Compute the cosine of two pasted word vectors with `SUMPRODUCT` and `SUMSQ`, and see `MATCH` and `XLOOKUP` ignore case where `EXACT` does not | Find a word's nearest neighbours in pretrained vectors, and use mean vectors as classifier features | 7 | Week 1, Day 4 |
| Count a statement's words from two named lists with `SUMPRODUCT`, `LEN`, and `SUBSTITUTE`, and score them per thousand words | Score every statement with a word list and with a classifier fitted only on earlier years, the label's own sentence removed first | 7 | Week 1, Day 5 |
| Compute a question's score against a chunk as `SUMPRODUCT` over 384 pasted numbers, and check each vector's length with `SQRT(SUMSQ(...))` | Embed an indenture's chunks and search it by meaning | 7 | Week 2, Day 1 |
| Read the item over a row's largest score with `INDEX`, `MATCH`, and `MAX`, and the share where two models agree with `SUMPRODUCT` | Score a zero-shot classifier and an embedding classifier against TF-IDF, reading every score by its label's name | 7 | Week 2, Day 2 |
| Count risk factors by cluster and filing with `COUNTIFS` | Cluster risk factor embeddings with K-means and describe each cluster by its words and its counts | 7 | Week 2, Day 3 |
| Cut an item out of pasted filing text with `TEXTBEFORE` and `TEXTAFTER`, and count its words with `TEXTSPLIT` | Turn an EDGAR filing into text and cut a 10-K into its items | 7 | Week 2, Day 4 |
| Check three models' confusion matrices on the test rows with `COUNTIFS`, then recall, precision, F1, and `AVERAGE` | Open the test sections once and compare three models with paired bootstrap intervals | 7 | Week 2, Day 5 |
| Price a request with `=B2*C2+B3*C3` on token counts and per-token prices, and see `SUMPRODUCT` treat prices pasted as text as 0 | Send a request to an LLM from code with the key kept secret, count its tokens, and price it | 7 | Week 3, Day 1 |
| Check a quote against its section with `=LEN(C2)<>LEN(SUBSTITUTE(C2,B2,""))`, because `SEARCH` fails on long quotes and reads `*` and `?` as wildcards | Extract a covenant into a schema and check every quote and number against the indenture | 7 | Week 3, Day 2 |
| Pull a grower basket out of a pasted sentence with `TEXTBEFORE(TEXTAFTER(A2,"greater of "),"%")`, and see a cell cut a long section at 32,767 characters | Check a model's baskets against a regular expression, put two indentures in one table, and read a PDF page as text and as an image | 7 | Week 3, Day 3 |
| Score retrieval with `ISNUMBER(MATCH(B2,C2:G2,0))`, with the section numbers kept as text | Retrieve an indenture's chunks for a question, answer with citations, and judge each answer against the retrieved text | 7 | Week 3, Day 4 |
| Check the capstone's workbook, whose quote and number checks are `SUBSTITUTE` and `SEARCH` formulas | Build a covenant extraction tool that runs on an indenture you have never seen, with a checked table, and write it to Excel | 7 | Week 3, Day 5 |
| Chart a count, a score, or a comparison of models as a line, clustered column, stacked column, bar, XY scatter, or histogram chart, and shade a `COUNTIFS` grid or a cosine table with a conditional formatting color scale | Draw every count, score, embedding, and comparison as a chart and show each comparison as a formatted table with the best value in each column marked | 7 | Week 1, Day 1 to Week 3, Day 4 |
| Build a DV01 from `PRICE`, `MDURATION`, and the accrued from `COUPDAYBS` over `COUPDAYS`, and price a run with `=B2*C2+B3*C3`, where `SUMPRODUCT` treats prices pasted as text as 0 | Hand a model your own `dv01` as a tool, run the tool it requests on your machine, and price the run from its token counts | 8 | Week 1, Day 1 |
| Count a pasted trace table's rows for a tool with `COUNTIF(C2:C7,"price")`, its requests with `COUNTIFS`, and its tokens with `SUM` | Write the agent loop with a step limit, and read every run as a trace table before its answer | 8 | Week 1, Day 2 |
| Use `PRICE`, `YIELD`, `MDURATION`, and `COUPDAYBS` over `COUPDAYS` on one bond, and build its DV01 from three cells | Offer Course 2's bond functions to a model as tools, each docstring stating its units, and check the tool results against Excel | 8 | Week 1, Day 3 |
| Check a figure against its tool value with `=ROUND(B2,D2)=C2`, at the decimals the answer wrote | Ask for an answer in a schema, and reject any figure that is not the value of the tool result it cites | 8 | Week 1, Day 4 |
| Total a sector with `SUMIFS` over a helper column, take the k-th largest with `LARGE`, weight by market value with `SUMPRODUCT` over `SUM`, and find a CUSIP with `INDEX` and `MATCH` | Compute every answer key with pandas first, then check a risk agent's figures on the synthetic book against them | 8 | Week 1, Day 5 |
| Look up a yield and a change in bp with `INDEX` and `MATCH(...,0)`, and see `#N/A` for a date the file lacks | Give an agent the Treasury curve as tools that return an error for a missing date, never the nearest row | 8 | Week 2, Day 1 |
| Check a cited section with `=ISNUMBER(MATCH(B2,C2:G2,0))`, the section numbers kept as text | Give an agent documents as tools, and check every section its answer cites against the sections the run read | 8 | Week 2, Day 2 |
| Compute a change and a slope in bp as the difference of two `INDEX` and `MATCH` cells times 100 | Serve your market tools from an MCP server, and send the model exactly the requests it saw before | 8 | Week 2, Day 3 |
| Write each curve change with `INDEX`, `MATCH`, and `*100`, and see the change in percent when `*100` is missing | Run a macro agent on the last two FOMC statements, and check its note's figures against pandas and its quotes against the statements | 8 | Week 2, Day 5 |
| Total requests and tokens by agent with `SUMIF`, which matches `"pm"` to `PM` where pandas' `==` does not | Split the work between an orchestrator and four specialists, and keep the run log by agent | 8 | Week 3, Day 1 |
| Look up a value by key and date with `=XLOOKUP(1,(A2:A4="10 Yr par yield")*(D2:D4="2026-10-02"),B2:B4,"no value for that date")` | Keep a desk memory that returns a value only for the date asked, never the latest one | 8 | Week 3, Day 2 |
| Count passed rows by kind with `COUNTIFS`, and average requests with `AVERAGEIFS`, on the eval log | Grade an agent on questions whose answer keys were decided first, and keep the scorecard in Git | 8 | Week 3, Day 3 |
| Check a request budget with `=IF(SUM(B2:B10)>=10,"stop","ok")`, where `>` lets one more request through | Stop a run in code, with guardrails and a budget checked before each request is sent | 8 | Week 3, Day 4 |
| Check the capstone's workbook, whose figure checks are `=ROUND(G2,H2)=C2` and whose scorecard is `COUNTIFS` and `AVERAGEIFS` | Build a multi-agent credit desk with every figure traced and the guardrail asserted, and write its checks to Excel | 8 | Week 3, Day 5 |
| Total a size table in MB with `=SUM(C2:C200)/1024^2`, and judge it against a 500 MB limit with `=IF(E1>500,"over","fits")` | List what a server must install from a file's imports, measure it with its dependencies, and see why the desk ships as a snapshot | 9 | Week 1, Day 4 |
| Count green runs on `main` with `=COUNTIFS(D2:D9,"success",B2:B9,"main")`, and take a pass rate that leaves cancelled runs out | Read a repo's CI runs as a table and a pass rate, and follow one change through a red run and a green one | 9 | Week 1, Day 5 |
| Price a bond with `PRICE`, take the accrued from `COUPDAYBS` over `COUPDAYS` and the DV01 from `MDURATION` times the dirty price over 10,000, and read a service's `/health` with `WEBSERVICE`, which sends `GET` only | Put `bondmath` behind a FastAPI service, test it without a network, and match Excel at 6 decimals on six bonds | 9 | Week 2, Day 1 |
| Read the deployed DV01 into a cell with `WEBSERVICE` and `=VALUE(TEXTBEFORE(TEXTAFTER(A2,"""dv01_per_100"":"),"}"))`, equal at Excel's 15 significant digits, and see a refused request come back as `#VALUE!` | Deploy the service to a public URL on Vercel and check it against `bondmath` on your own machine | 9 | Week 2, Day 2 |
| Price the desk's saved run with `=SUMPRODUCT(B2:B3,C2:C3)` on tokens and prices per token, where prices typed into text cells count as 0 | Serve the Course 8 desk's brief as a snapshot with no key on the server, and refuse a request for a view at the API | 9 | Week 2, Day 3 |
| Open a CSV from a download button and see Excel turn the CUSIP `99123E105` into the number 9.9123E+109, keep the course's CUSIPs as text, and read `True` and `False` as booleans for `COUNTIF` | Give the same functions a Streamlit page and a Gradio app, and offer identifiers in a workbook, where they stay text | 9 | Week 2, Day 4 |
| Summarise a request log with `COUNTIFS` and `AVERAGEIFS`, take p95 latency with `PERCENTILE.INC` over `FILTER`, and see `PERCENTILE.EXC` and `SMALL` with `INT` give other answers on 20 values | Log every request without its body, and read requests, errors, and p50 and p95 latency by path, with alerts by rule | 9 | Week 3, Day 2 |
| Score drift with `=STANDARDIZE(AVERAGE(recent),AVERAGE(train),STDEV.S(train))`, not `STDEV.P`, and count inputs outside the training range with two `COUNTIFS` against `MAX` and `MIN` | Keep a model as a file with its card, serve it, and measure how far its inputs have moved from its training window | 9 | Week 3, Day 3 |
| Cost a live month with `=SUMPRODUCT(C2:C5,D2:D5)` on tokens and prices, and mark each free-tier line with `=IF(B2>C2,"over","within")` | Keep secrets in platform settings, list every name the code reads, and meter a month against the free tiers | 9 | Week 3, Day 4 |
| Check the capstone's workbook, whose free-tier status is `IF` and whose model cost is `SUMPRODUCT` | Ship the desk's brief as a public app with CI, a request log, a daily cap, and a cost line, and write its numbers to Excel | 9 | Week 3, Day 5 |
| Grade an answer against its key with `ISNUMBER(SEARCH(key,answer))` and count the matches by stage with `COUNTIFS` | Grade a model's closed-book and prompt-only answers against keys written first, and see that none matches | 10 | Week 1, Day 1 |
| Paste a page one line per row and read `LEN` of each, and see a line such as `December 31, 2025` become a date serial in a General cell | Load a 10-K as pages with `pdf_pages`, keep the empty page, and map every page to its item | 10 | Week 1, Day 2 |
| Count a chunk's characters with `LEN` and its words with `LEN` and `SUBSTITUTE` (with `CHAR(10)` turned into a space), and check an overlap with `=RIGHT(B2,64)=LEFT(B3,64)` | Write a recursive splitter with size and overlap, and read what 64 characters carry across a cut | 10 | Week 1, Day 3 |
| Compute a cosine with `SUMPRODUCT` over `SQRT(SUMSQ())` on two pasted 384-number vectors | Embed the chunks with three pinned models and search them exactly with NumPy and FAISS | 10 | Week 1, Day 4 |
| Count matched keys by stage with `COUNTIFS`, and fill a 2 by 2 table of retrieval against grade with three `COUNTIFS` | Run the first RAG pipeline on five questions beside the closed-book and prompt-only stages, and say which miss was retrieval | 10 | Week 1, Day 5 |
| Write one BM25 term weight out with `LN` and the length penalty, and fuse two rankings with `=1/(60+rank)` summed by `SUMIFS` | Write BM25 by hand, check it against `rank-bm25`, and fuse it with embedding search by reciprocal rank fusion | 10 | Week 2, Day 1 |
| Read a tuning grid with `AVERAGEIFS` and order it with `SORTBY` | Run twelve named settings on development questions and read the results table | 10 | Week 2, Day 3 |
| Filter a corpus table with `COUNTIFS`, `ROWS(FILTER())`, and `TAKE(SORTBY(FILTER()))`, and see `4.10` typed into a General cell become 4.1 | Filter chunks by document and section before search, across four filings | 10 | Week 2, Day 4 |
| Check each cited chunk against the chunks sent with `ISNUMBER(MATCH())` on ids stored as text | Demand a citation after every sentence and reject the answer that has none | 10 | Week 2, Day 5 |
| Compute recall with `ISNUMBER(MATCH())` and `COUNTIF` over `ROWS`, and MRR with `AVERAGE(IFERROR(1/MATCH(),0))` | Measure retrieval recall at k and MRR on a labelled question set, by item | 10 | Week 3, Day 1 |
| Fill a 3 by 3 agreement table with `COUNTIFS`, write Cohen's kappa out as `(po-pe)/(1-pe)`, and colour the table with a colour scale | Put two LLM judges beside a strict grader and read the agreement table and kappa | 10 | Week 3, Day 2 |
| Match chunk texts with `EXACT` inside `SUMPRODUCT`, where `COUNTIF` and `MATCH` refuse a criterion over 255 characters, and see `MAXIFS` return 0 for a date before the first filing | Refresh an index when a new filing arrives, embedding only the new chunks, and answer as of each filing's date | 10 | Week 3, Day 3 |
| Price a run with `SUMPRODUCT` on tokens and prices per token, where prices pasted as text count as 0, and average by setting with `AVERAGEIFS` | Serve the retriever behind a FastAPI service and price a thousand answers | 10 | Week 3, Day 4 |
| Check the capstone's workbook, whose recall, MRR, `COUNTIFS` grids, kappa, and `SUMPRODUCT` bill are formulas | Build a cited question-answering tool over public filings with its evaluation report, and write its numbers to Excel | 10 | Week 3, Day 5 |
| Open `bonds.csv` and see `bond_id` stay text and the maturity become a date, shown as `########` until the column is widened, then list the rows below BBB- with `=FILTER(A2:F7,ISNUMBER(MATCH(E2:E7,{"BB+","BB","BB-","B+","B","B-"},0)))` | Ask your own coding agent which bonds in the file are high yield, and check its answer against the file | Bonus | Week 1, Day 1 |
| Price with `=PV(0.06,3,-5,-100)` and `=PV(0.05,3,-5,-100)`, and take `=MDURATION(DATE(2026,10,2),DATE(2029,10,2),0.05,0.06,1)` | Have the agent write `bond_price` and `modified_duration`, and check them against 97.3270, 100.0, and 2.6956 before you trust them | Bonus | Week 1, Day 1 |
| Count an agent's edits with `=COUNTIFS(B2:B40,"edit_file")` and its refused requests with `=COUNTIFS(D2:D40,"ERROR*")`, and price its run with `=SUMPRODUCT(B2:B40*$G$1)+SUMPRODUCT(C2:C40*$G$2)` | Read the agent's tool log as a table, and price its saved run from the token counts | Bonus | Week 1, Day 1 |
