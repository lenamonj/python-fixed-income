# COURSE5B_SPEC.md

**Course 5B: Time Series Models** - two weeks of five days, nine notebooks, one capstone
Status: v0.1, 2026-10-20: scope approved by Jeff, not yet built. Written in the shape of `COURSE5_SPEC.md` and `COURSE6_SPEC.md`, whose conventions Course 5B keeps unless a line below states a change and its reason. Decisions Jeff made are marked as his. Facts found by probes on 2026-10-20 (the repo `.venv`, Python 3.13.8, the repo's data files read only) are marked "probed 2026-10-20"; every number here is a probe result that the build recomputes, and a notebook never quotes this file.

## Why this course exists, and its name

- Jeff (2026-10-20): the series handled dated data (Course 3, Course 4 day 11, Course 6 days 11 to 14) but taught no classical time series model. Course 5B adds them: stationarity, autocorrelation, AR and ARIMA, exponential smoothing, GARCH, lag features with gradient boosting, and two series together. It opens with a day on missing data and data corrections (Jeff).
- **Name and place (Jeff):** "Course 5B" so nothing public is renumbered or reordered. It is taken after Course 5 and before Course 6, and is drawn there in the README's path. Folder `course5b_time_series`.
- **Course 3 and Course 5B:** Course 3 ("Market Data and Time Series") gets and handles dated data and fits no model. Course 5B models a series: it needs regression (Course 4) and boosting (Course 5). Each README says this in one line.
- Course 6 days 11 to 14 (sequence networks on the Treasury curve) come after Course 5B and may refer back to its baselines and its walk-forward numbers.

## Shape

- Two weeks, five days each, one notebook per day. Folders `course5b_time_series/week1/day1` through `week2/day5`. Notebook numbers 01 to 09 restart inside the course; week 2 day 5 is the capstone `course5b_capstone`. Each day folder holds exactly three files: the notebook, `_solutions.ipynb`, `_overview.pdf`.
- Week 1 is a series, its gaps, and its memory: missing data and corrections; frequency, lags, and the naive baselines; stationarity; autocorrelation; a case study with AR and ARIMA on day 5. Week 2 is models beyond ARIMA: exponential smoothing; volatility and GARCH; lag features and gradient boosting; two series together; the capstone.
- Hands-on and case study notebooks as before; day 5 is hands-on, then case study, with Course 4's skeleton and the closing section **What the model shows, and where it fails**.
- Every example is fixed income. Windows, PowerShell, VS Code, `venv` plus `pip`, Colab in principle. No `input()`, outputs saved, runs unattended. **No API key in this course**: every dataset is in the repo. An optional exercise on day 9 and in the capstone tells a student with Course 3's FRED key how to run the same workflow on an ICE BofA spread series on their own screen (licensed data, never saved), as Course 3 does; no build cell calls FRED.
- Students arrive with Courses 1 to 5: `bondmath.py`, `marketdata.py`, `mlkit.py` (with `walk_forward_splits` and `assert_past_only`, Course 4 day 11), `ensemblekit.py`; LightGBM (Course 5 day 9); the rule that every sentence describes.

## Goal

A student finishes able to find and diagnose every gap in a dated table, correct wrong values with an audit trail, and fill gaps by the method that suits the gap; set a frequency, build lags and changes without lookahead, and score any model walk-forward against the naive baselines; test a series for stationarity and difference it; read an ACF and a PACF and pick an AR or MA order from them; fit ARIMA, exponential smoothing, and GARCH with statsmodels and arch and read every setting; build lag features for LightGBM with no leak; test two series for cointegration and measure a half-life of mean reversion; and say plainly, with numbers, which model beat carrying the last value forward and which did not.

## Notebook style

Course 5's style, unchanged: banner via `tools/notebook_header.py --course 5b` (add support backward compatibly), title, purpose line, the data line, disclaimer, Colab badge with the `course5b_time_series` path, scenario, numbered sections, `Q.` cells, small commented code cells, one-line takeaways, real errors tagged `raises-exception`, outputs saved, Excel side by side, a story where one fits, an AI check as the last exercise, three to five exercises with a `_solutions` notebook. Closing sections as Course 5. The install section from `tools/install_cell.py` after the title.

From the start (the 2026-10-19/20 standard, `instructor/_build/COVERAGE_C4C6_BRIEF.md`):

- **How it works.** Every section that introduces a method opens with a bold **How it works.** paragraph of 4 to 7 sentences: the problem, the mechanism step by step, the settings that matter, what comes out.
- **Every setting.** Each estimator first taught (`ARIMA`, `ExponentialSmoothing`, `arch_model`, `LGBMRegressor` on lags, `coint`) gets a styled table of its settings: default (read from the installed library), what it controls, what raising and lowering it does, and which to tune first, then a sweep for each "tune first" setting.
- **Pictures that teach.** Side-by-side small multiples with one thing changed per panel, the point that matters annotated, and a takeaway that says how to read it. At least 4 figures and 1 styled table per teaching notebook, course chart style, `plt.show()`.

## The threads

- **A. Excel side by side, tested.** A lag is a cell one row up; a change is `=B3-B2`; a forward fill is `=IF(B3="",C2,B3)`; linear interpolation between two known days is a few cells; an autocorrelation at lag k is `CORREL` of two offset ranges; AR(1) is `SLOPE` and `INTERCEPT` on the lagged column; EWMA and the GARCH(1,1) variance are one recursive formula each; a half-life is `=LN(0.5)/LN(b)`. Excel has no ADF test, no ARIMA, and no GARCH fitter; the notebook says so once where it applies. Excel's own functions whose names contain a forbidden word (for example `FORECAST.LINEAR`, `FORECAST.ETS`) may be named as function names in code formatting, the way `predict` is. Every Excel statement has its COM check in `instructor/_build/course5b/excel_checks/`.
- **B. The student's module.** `tskit.py` beside `mlkit.py` and `ensemblekit.py` in `my_bondmath`, two or three functions a day, docstring first, imports `mlkit` (frozen), with `test_tskit.py` on small seeded arrays only. API below.
- **C. Local Git**, Course 5's rules: one Git step a day in the throwaway work folder.
- **D. The AI check** in Course 5's shape. Planted bugs for this course: a backfill that puts a later value into an earlier date; `interpolate` across a 20-day outage with no `limit`; `df.update` that overwrites good values with blanks' neighbours; a change computed with `shift(-1)`; a rolling mean that includes the scored day; an ADF p-value read the wrong way round; an ACF bar read without its band; `ARIMA` on levels scored against changes; `.fit()` on the whole file before walk-forward; GARCH fitted on yields instead of changes; a half-life from the wrong sign of the slope; lag features built before the split from the full file.
- **E. Course 1 threads**: f-strings with units (bp for yields and spreads), checks that stop, a function in every exercise set, Excel in and out on days 5 and 10.

## No market views, in a course about time series models

Course 6's framing ("The sequence model, framed") holds word for word and applies to every model in this course:

1. **The task is in the past tense.** The target is "the change in the 10 Yr yield on a date, in bp" from information dated before it. Text never says "tomorrow", "next day's move", "where yields go", or "what the curve will do".
2. **Walk-forward only, inside the file.** Every fitted value is for a date inside 2015-01-02 to 2026-10-02 from a model fitted on earlier dates only. Nothing is fitted for, or reported at, any date after 2026-10-02. statsmodels' `.forecast()` and `get_forecast()` are not used; one-step-ahead values inside the file come from `.predict()`, `.append()`, or `.extend()` on fitted results, and are called "the model's one-step value" or "fitted change".
3. **The honest finding is the lesson.** Probed 2026-10-20 and by Course 6: nothing fitted on past daily changes of the 10 Yr beat carrying the last value forward by a margin larger than the folds disagree. Volatility is different: squared changes are autocorrelated, and GARCH describes the clustering. The notebooks say both plainly and never tune until a model wins.
4. **Two series together** (day 9) are described: "the gap between the two series closed at a half-life of N trading days over these years". Never a trade, a signal, an entry, rich or cheap.

**Names.** A model's output is "fitted change", "one-step value", "fitted volatility", "residual", "the model's value for that date", "the last value carried forward" (the baseline). Never a forecast, prediction, projection, outlook, expected move, signal, call, or view on rates. `c5blib.FORBIDDEN_NAMES` is Course 6's list plus: projection(s), projected. A forbidden word may appear only in a sentence with a negation; Excel function names in code formatting are exempt.

## Leakage and the test-row rule

- **Development years** 2015-01-02 to 2022-12-30 (2,001 rows) and **held-out years** 2023-01-03 to 2026-10-02 (939 rows), the same split as Course 6, set on day 2 before any model is fitted. Days 2 to 9 fit and score walk-forward inside the development years with `mlkit.walk_forward_splits(dates, min_train=504, test_size=252)` (5 folds). The held-out years are opened once, in the capstone, for the models chosen on development.
- Every lag, change, rolling statistic, and fill is checked with `mlkit.assert_past_only` or an elementwise test before it is used.
- Day 1 (missing data) works on the whole file because it describes and repairs data and fits nothing; it says so.

## Data

| File | Use | Licence |
|---|---|---|
| `data/treasury_par_yields.csv` (2,940 rows, 2015-01-02 to 2026-10-02, 14 tenors) | Every day. Its own gaps are day 1's first lesson: market holidays are absent rows; `1.5 Month`, `2 Mo`, `4 Mo` start partway through the file (series not yet started). | Real; U.S. Treasury, public domain. |
| `data/course3_synthetic_spreads.csv` (2,940 rows, IG and HY spreads in bp) | Days 3, 4, 6, 9, capstone: a second kind of series (spreads), and day 9's pair. | **Synthetic** (Course 3's generator). Every load says so. |

No new data file. Day 1's planted problems (blanked days, a 20-day outage, wrong prints, a second source) are made in the notebook from the real file with a seeded generator, shown, and checked against the untouched values; the notebook says they were planted for the lesson.

## Libraries

Course 5's pins plus **`arch==8.0.0`** (probed 2026-10-20: adds only `arch`, keeps every pin; GARCH(1,1) on 10 Yr changes fits with no warning). statsmodels (pinned since Course 4) supplies `adfuller` (pass `result_object=True`: without it statsmodels 0.15 raises a FutureWarning, which the stderr rule refuses; probed), `kpss`, `acf`, `pacf`, `plot_acf`, `plot_pacf`, `ARIMA`, `ExponentialSmoothing`, `acorr_ljungbox`, `coint`. `course5b_time_series/requirements.txt` holds Course 5's file plus `arch`; the root file gains `arch==8.0.0` (sorted). Probed 2026-10-20 with warnings as errors: ADF p-value 0.934 on 10 Yr levels and 0.0 on changes; ARIMA(1,1,1) on the last 500 levels fits; Holt's linear trend fits; GARCH(1,1) on changes in bp: alpha 0.0503, beta 0.9391.

## The `tskit.py` API (the foundation fixes exact signatures)

Day 1 `gap_report(frame)`, `gap_runs(series)`, `apply_corrections(frame, corrections)` (returns the frame and a change log); day 2 `naive_values(series, kind)`, `mae`, `mase`, `walk_forward_score(series, fit_one, splits)`; day 3 `adf_summary(series)`, `kpss_summary(series)`; day 4 `acf_by_hand(series, lag)`; day 5 `walk_forward_arima(series, order, splits)`; day 6 `ewma(series, alpha)`; day 7 `garch_half_life(alpha, beta)`, `walk_forward_garch(changes, splits)`; day 8 `lag_features(frame, column, lags, windows)`; day 9 `half_life(spread)`, `hedge_ratio(y, x)`. Every function has a test on small seeded arrays; `test_tskit.py` runs in under 10 seconds.

## Day plan

### Week 1: A series, its gaps, and its memory

#### Day 1: `01_missing_data_gaps_and_corrections` (hands-on; Jeff asked for it)
Sections: 1.1 Kinds of missing in a dated table: an absent row (a market holiday), a blank cell in a present row (an outage), a series that had not started yet, a wrong value that is present. 1.2 Finding gaps: `isna().sum()`, a missing-over-time heatmap of all tenors, gap runs (`gap_runs`) as a styled table and a bar chart of run lengths; the not-yet-started tenors found by their first valid date (`first_valid_index`). 1.3 Diagnosing: is a gap a holiday, an outage, or a not-yet-started series, and why each needs a different fix (a decision table). 1.4 Correcting wrong values: one wrong print fixed with `.loc`; a corrections table applied with `df.update()` (and the trap: `update` skips NaN in the corrections, so it never blanks a value); filling from a second source with `combine_first`; every change written to a change log (date, column, old, new, source) shown styled. 1.5 Filling gaps in a series: Course 3's `ffill` recalled, then `bfill`, `interpolate(method="linear")`, `interpolate(method="time")`, and `limit=` and `limit_area=`; the same planted gaps filled every way, side by side on one figure against the held-back true values, with the error of each method in a styled table. 1.6 Which fill when: forward fill for a stale quote you could have traded on; interpolation for a missing point on a curve or a description of history; never a backfill or an interpolation into anything scored walk-forward (it uses a later value), shown with a small walk-forward score that improves falsely. 1.7 A long outage: `limit=` stops a fill, and the gap stays visible. Excel: `IF` forward fill, linear interpolation by hand, a lookup from a second sheet as `combine_first`. AI check: an `interpolate` with no `limit` across the 20-day outage, scored as if it were data.

#### Day 2: `02_frequency_lags_and_the_naive_baselines` (hands-on)
Business-day frequency and `asfreq` recalled from Course 3; `shift` and `diff`, changes in bp; the development and held-out years set and counted; the naive baselines (the last value carried forward, the training mean, drift) as values and as a picture against the series; MAE, RMSE, and MASE (scaled by the last-value baseline), how to read a MASE of 1; walk-forward scoring recalled from Course 4 day 11 and drawn on a timeline; the baseline table for 2 Yr, 10 Yr, 2s10s, IG and HY spreads. Every later day's models sit beside these numbers.

#### Day 3: `03_stationarity_and_differencing` (hands-on)
How it works for stationarity; simulated series side by side with one setting changed per panel (AR(1) with phi 0, 0.5, 0.9, 0.99, 1.0); rolling mean and spread of yield levels against changes; ADF and KPSS on levels and changes (`adf_summary`, `kpss_summary`), the null hypothesis of each written out, and what to do when they disagree (a table); the spurious-regression demonstration: two independent random walks with a high R-squared; differencing and when a log helps; the stationarity checklist.

#### Day 4: `04_autocorrelation_acf_and_pacf` (hands-on)
Lag scatter plots at lags 1, 2, 5, 20 side by side; autocorrelation by hand (`acf_by_hand`, `CORREL` in Excel) against `acf`; the confidence band and how to read a bar outside it; PACF; the identification grid: simulated AR(1), AR(2), MA(1), ARMA(1,1), each with its ACF and PACF in one row (the picture students use to pick an order); the real 10 Yr changes (close to no memory) against their squares (clear memory: volatility clusters, which sets up day 7); Ljung-Box.

#### Day 5: `05_case_study_ar_and_arima_on_the_curve` (hands-on, then case study)
How it works for AR, MA, and ARIMA(p, d, q); the AIC and BIC grid over p and q as a heatmap; every setting of `ARIMA` (order, trend, enforce_stationarity, and the rest); residual diagnostics (residual ACF, Ljung-Box, Q-Q); `walk_forward_arima` one-step values on the development years for 10 Yr changes, 2s10s, and the synthetic IG spread, against day 2's baselines; fold by fold chart. Case study with Course 4's skeleton; What the model shows, and where it fails.

### Week 2: Beyond ARIMA

#### Day 6: `06_exponential_smoothing` (hands-on)
EWMA by hand (`ewma`, one Excel formula) and alpha swept in panels; simple exponential smoothing, Holt's linear trend, damped trend; every setting of `ExponentialSmoothing`; the smoothing as a description of level, scored walk-forward against the baselines and ARIMA; EWMA of squared changes as a volatility estimate (the published RiskMetrics decay of 0.94 named with its source), leading into day 7.

#### Day 7: `07_volatility_clustering_and_garch` (hands-on)
Squared and absolute changes and their ACF; rolling, EWMA, and GARCH(1,1) volatility on one chart; How it works for GARCH (the variance recursion, one Excel formula); alpha, beta, persistence, and the half-life of a volatility shock (`garch_half_life`); every setting of `arch_model` (mean, vol, p, o, q, dist), normal against Student's t with standardized residuals on a Q-Q plot; `walk_forward_garch` one-step volatility scored against realized absolute changes; the honest contrast with day 5: the level of the change is close to unpredictable from its past, its size is not.

#### Day 8: `08_lag_features_and_gradient_boosting` (hands-on)
`lag_features`: lags, rolling statistics, other tenors' lagged changes, calendar fields, all built with `shift` before any rolling window and checked with `assert_past_only`; LightGBM (Course 5) on those features walk-forward against the baselines, ARIMA, and smoothing; every setting that matters for a time series (learning rate, number of trees, leaves, minimum rows per leaf) with sweeps; importance by permutation within folds; the leak shown on purpose: a rolling mean that includes the scored day gives a far better score that is false.

#### Day 9: `09_two_series_cointegration_and_mean_reversion` (hands-on)
Correlation of levels against changes; Engle-Granger (`coint`) on the 5 Yr and 10 Yr and on the synthetic IG and HY spreads; the hedge ratio (`hedge_ratio`), the residual spread drawn with bands of its own standard deviation (description only); the half-life of mean reversion (`half_life`, an AR(1) on the residual), with the sign checked; a rolling hedge ratio showing the relationship drifting; what this describes and what it does not (rule 4).

#### Day 10: `course5b_capstone`
The student runs the course's workflow on two series (2s10s and the synthetic HY spread): repair the planted gaps with a change log, set the development and held-out years, test stationarity, read the ACF and PACF, fit the baselines, ARIMA, exponential smoothing, and LightGBM on lags walk-forward on development, fit GARCH for volatility, choose on development, open the held-out years once, and write "What the models show, and where they fail". Excel in and out. Solutions notebook complete.

## Where the files live

As Course 5: `instructor/_build/course5b/` holds `c5blib.py` (built on `c5lib` and Course 6's Treasury helpers, extended only where this spec says), `c5bdeck.js`, `assemble.py`, `fragments/` (the `tskit` reference, day by day), `notebooks/build_NN_*.py`, `script_wWdD.json`, `wWdD_deck.js`, `excel_checks/`, `notes/`, and a build `README.md`. Runtime budget: a teaching notebook 7 minutes on one thread, the capstone's solutions 11 (Jeff, 2026-10-20).

## READMEs and series files to update when the course is built

`course5b_time_series/README.md` (the course README standard), the root README's course table and the path image (`tools/make_path_diagram.py`, Course 5B between 5 and 6), `EXCEL.md` rows, `CURRICULUM.md`, `CLAUDE.md` status and layout lines, the root `requirements.txt`.

## Open questions for Jeff (defaults chosen)

1. Day 9 (two series) uses the synthetic IG and HY spreads for the credit pair. Default: yes, with the 5 Yr and 10 Yr as the real pair.
2. Prophet and deep sequence models are out (Course 6 has the networks). Default: out.
3. The FRED exercise on a real ICE BofA spread is optional and student-run only. Default: yes.
