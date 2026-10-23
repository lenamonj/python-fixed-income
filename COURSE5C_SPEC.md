# COURSE5C_SPEC.md

**Course 5C: Risk Models** - two weeks of five days, nine notebooks, one capstone
Status: v0.2, 2026-10-22: plan approved by Jeff with every default below accepted (scope approved in principle 2026-10-21: Monte Carlo, survival and hazard models, anomaly detection, PSI); not yet built. Written in the shape of `COURSE5B_SPEC.md`, whose conventions Course 5C keeps unless a line below states a change and its reason. Facts found by probes on 2026-10-22 (the repo `.venv`, Python 3.13.8, warnings as errors, the repo's data files read only) are marked "probed 2026-10-22"; every number here is a probe result that the build recomputes, and a notebook never quotes this file.

## Why this course exists, and its name

- Jeff (2026-10-21): the series fits models that score and classify but teaches no risk model: nothing simulates a loss distribution, models time to default, screens data for the unusual, or watches a model's inputs drift. Course 5C adds the four: Monte Carlo, survival and hazard models, anomaly detection, and the population stability index (PSI). None of them appears in any earlier course (checked 2026-10-22 across every spec).
- **Name and place:** "Course 5C" so nothing public is renumbered, as 5B (Jeff, 2026-10-20). Taken after Course 5B and before Course 6, and drawn there in the README's path. Folder `course5c_risk_models`.
- **What it needs:** Course 2's bond math and DTS, Course 4's regression, logistic regression, and walk-forward rules, Course 5's trees and boosting, and Course 5B's development and held-out years and `tskit`. Course 6 does not depend on it.

## Shape

- Two weeks, five days each, one notebook per day. Folders `course5c_risk_models/week1/day1` through `week2/day5`. Notebook numbers 01 to 09 restart inside the course; week 2 day 5 is the capstone `course5c_capstone`. Each day folder holds exactly three files: the notebook, `_solutions.ipynb`, `_overview.pdf`.
- Week 1 is simulation and default: Monte Carlo foundations; historical simulation and VaR of the book; correlated defaults and the portfolio loss distribution; survival curves; a case study with hazard models on day 5. Week 2 is the unusual and the drifting: robust rules for outliers; isolation forest and its neighbours; population stability and drift; a case study monitoring a credit model on day 9; the capstone.
- Hands-on and case study notebooks as before; days 5 and 9 are hands-on, then case study, with Course 4's skeleton and the closing section **What the model shows, and where it fails**.
- Every example is fixed income or credit. Windows, PowerShell, VS Code, `venv` plus `pip`, Colab in principle. No `input()`, outputs saved, runs unattended. **No API key in this course**: every dataset is in the repo.

## Goal

A student finishes able to run a seeded Monte Carlo and state its standard error; compute VaR and expected shortfall of the synthetic book by historical simulation, a normal model, and Monte Carlo, and backtest the count of exceptions; simulate correlated defaults with a one-factor model and read the loss distribution's tail against the Vasicek formula; estimate a survival curve with censoring by Kaplan-Meier, compare groups with a log-rank test, and fit a Cox model and a discrete-time hazard model and read every coefficient as a hazard ratio; flag unusual trades and curve days with robust rules, Mahalanobis distance, isolation forest, and local outlier factor, scored against planted labels; compute PSI by hand and with a function, per feature and on a model score; and write a monitoring table that says, with numbers, what drifted and what did not.

## Notebook style

Course 5B's style, unchanged: banner via `tools/notebook_header.py --course 5c` (add support backward compatibly), title, purpose line, the data line, disclaimer, Colab badge with the `course5c_risk_models` path, scenario, numbered sections, `Q.` cells, small commented code cells, one-line takeaways, real errors tagged `raises-exception`, outputs saved, Excel side by side, a story where one fits, an AI check as the last exercise, three to five exercises with a `_solutions` notebook. The install section from `tools/install_cell.py` after the title. From the start: **How it works.** paragraphs, **Every setting** tables read from the installed library with a sweep for each "tune first" setting, and **Pictures that teach** (at least 4 figures and 1 styled table per teaching notebook, course chart style), as in `COURSE5B_SPEC.md`.

## The threads

- **A. Excel side by side, tested.** A uniform draw is `RAND()`, a normal draw `=NORM.S.INV(RAND())`; a thousand trials are a column or a one-variable Data Table; VaR is `PERCENTILE.INC` of the losses and expected shortfall `AVERAGEIF` beyond it; a bond's expected loss is `=PD*LGD*EAD`; the Vasicek tail is one `NORM.S.DIST` formula; `BINOM.DIST` checks the count of defaults in independent bonds; Kaplan-Meier is a table of at-risk counts (`COUNTIF`) and a running product; survival at a flat hazard is `=EXP(-h*t)`; the robust z-score is `MEDIAN` and the median of absolute deviations; the IQR fences are `QUARTILE.INC`; PSI is `=SUMPRODUCT((A-E)*LN(A/E))` over `FREQUENCY` bins. Excel has no Cholesky factor, no Cox model, no isolation forest; the notebook says so once where it applies. Every Excel statement has its COM check in `instructor/_build/course5c/excel_checks/`.
- **B. The student's module.** `riskkit.py` beside `mlkit.py`, `ensemblekit.py`, and `tskit.py` in `my_bondmath`, two or three functions a day, docstring first, imports `mlkit` (frozen) and nothing else of the student's, with `test_riskkit.py` on small seeded arrays only.
- **C. Local Git**, Course 5's rules: one Git step a day in the throwaway work folder.
- **D. The AI check** in Course 5's shape. Planted bugs: the seed set inside the loop so every trial draws the same numbers; legacy `np.random.seed` mixed with a `Generator`; VaR taken from the wrong tail or with P&L's sign flipped; expected shortfall computed as the VaR; a correlation matrix that is not positive definite passed to Cholesky; censored firms dropped from a survival curve; a censored exit counted as a default; a Cox hazard ratio read as a probability; a discrete-time hazard fitted on covariates from the year of default (lookahead); a z-score whose mean and spread include the outliers it hunts; `contamination` set from the planted labels; PSI bins cut on the actual sample instead of the reference; a PSI of infinity from an empty bin.
- **E. Course 1 threads**: f-strings with units (US$, bp, percent per year), checks that stop, a function in every exercise set, Excel in and out on days 5 and 10.

## No market views, in a course about risk

1. **Losses are conditional statements about the past or about invented inputs.** Historical VaR reads "had the daily moves of 2015 to 2022 repeated, with the book as of 2026-09-30 held fixed, the 99th percentile one-day loss was US$N". Monte Carlo losses read "under these invented default rates and this correlation". Neither is a statement about what a real security or market will do.
2. **Default rates are synthetic.** Every default rate, hazard, and survival curve comes from the synthetic cohort file below, labelled at every load. No agency default study, no real issuer's default probability, and no real rating's default rate is quoted.
3. **An anomaly is a data question, never a value judgment.** A flagged trade is "a print far from the day's mid, to be checked"; a flagged curve day is a day the daily changes were unusual together. Never mispriced, rich, cheap, an opportunity, or a signal.
4. **Drift is described.** PSI says the held-out years' 10 Yr levels sit outside the development years' range; it never says where they go next.

**Names.** As Course 5B: `c5clib.FORBIDDEN_NAMES` is `c5blib.FORBIDDEN_NAMES` unchanged (probed 2026-10-22: "expected loss" and "expected shortfall" pass; only "expected move" is refused). A model's output is "fitted hazard", "the model's default probability for that firm-year", "simulated loss", "VaR", "flag", "score".

## Leakage and the test-row rule

- **Treasury and spread series** (days 2, 7, 8): Course 5B's development years 2015-01-02 to 2022-12-30 and held-out years 2023-01-03 to 2026-10-02. Day 2's VaR is estimated on development and backtested walk-forward with a rolling window inside development; the held-out years are opened once, in the capstone.
- **The cohort** (days 3, 4, 5, 8, 9): development study years 1 to 14, held-out years 15 to 20, set on day 3 before any default rate is counted. Every covariate in a firm-year row is dated at the start of that year; the generator's tests and `mlkit.assert_past_only` check it. The held-out years are opened once, in the capstone.
- **Anomaly detection**: thresholds and `contamination` are chosen without the planted labels; the labels only score. Rolling robust statistics use past rows only.
- **PSI**: the reference sample and its bin edges are fixed before the compared sample is read.

## Data

| File | Use | Licence |
|---|---|---|
| `data/holdings.csv` (200 bonds, 115 issuers, 10 sectors, US$490.8m market value, AAA to CCC; probed 2026-10-22) | Days 1 to 3 and the capstone: the book whose losses are simulated. | **Synthetic** (`tools/make_holdings.py`). |
| `data/treasury_par_yields.csv` (2,940 rows, 2015-01-02 to 2026-10-02) | Day 2 (rate moves for historical simulation), day 7 (unusual curve days), day 8 (drift). | Real; U.S. Treasury, public domain. |
| `data/course3_synthetic_spreads.csv` (IG and HY spreads in bp, same dates) | Day 2: spread moves applied to the book by DTS. | **Synthetic** (Course 3's generator). Every load says so. |
| `data/trade_blotter.csv` (374 trades, 2026-09) | Day 6: off-market prints planted in a copy, seeded, in the notebook, and scored against the untouched file. | **Synthetic** (`tools/make_blotter.py`). |
| **New:** `data/course5c_cohort.csv` | Days 3, 4, 5, 8, 9 and the capstone: invented firms followed year by year to default, exit, or the end of the study. | **Synthetic**, MIT with the code. |

**The new file.** `tools/make_cohort.py`, seed 20261022, numpy `default_rng`; reads `ratings.csv` for the rating scale and nothing else; writes `data/course5c_cohort.csv` only. About 4,000 invented firms with ids only (`F0001` and up; no names, so nothing can collide with a real issuer), entering in study years 1 to 16 and followed to year 20. One row per firm-year: `firm_id`, `study_year`, `years_since_entry`, `rating`, `rating_score`, `sector` (the sector list of `issuers.csv`), `leverage` (debt to EBITDA), `coverage` (EBITDA to interest), `default` (1 in the year of default), `exit` (1 in a year the firm leaves for a reason other than default: refinanced or called, independent of default). Covariates are dated at the start of the year. The annual hazard is a baseline by years since entry times `exp(b_lev*leverage + b_cov*coverage + rating effect + a common year factor)`; the year factor makes defaults cluster, which day 3 measures. From study year 11 the entering population shifts gradually toward higher leverage and a lower rating mix, which days 8 and 9 find with PSI. Every planted coefficient is written in `DATA.md`, so the notebooks show the models recovering them. Uses calendar-free study years so no reader maps a default wave onto real history. `tests/test_data.py` gains: the generator run twice gives byte-identical output equal to the committed file; one row per firm and year; no row after a default or an exit; at most one default per firm; every rating on the `ratings.csv` scale; overall and per-rating default counts inside ranges the build fixes. The build fixes the firm count and the coefficients so that every rating bucket from BBB down has enough defaults to fit, and AAA and AA have zero or a few: day 3 teaches the low-default problem from that.

## Libraries

**No new library.** Course 5B's pins unchanged. Probed 2026-10-22: `lifelines` 0.30.3, the usual survival library, would force pandas from 3.0.6 down to 2.3.3, so it is out; statsmodels 0.15.0 (pinned since Course 4) supplies `SurvfuncRight` (Kaplan-Meier), `survdiff` (log-rank), and `PHReg` (Cox), and on a seeded toy cohort with warnings as errors recovered a planted coefficient of 0.70 as 0.717 and a survival of 0.727 as 0.734. scikit-learn 1.9.1 supplies `IsolationForest`, `LocalOutlierFactor`, `MinCovDet`, and `LogisticRegression` (the discrete-time hazard, also fitted with statsmodels `Logit` for its standard errors). scipy supplies `norm`, `ks_2samp`, and `jensenshannon`. `course5c_risk_models/requirements.txt` is Course 5B's file unchanged.

Other probes, 2026-10-22: Vasicek's large-portfolio 99.9th percentile default rate at PD 2 percent and correlation 0.2 is 22.6 percent; PSI of the 10 Yr level, held-out against development, is 12.4, and of its daily change in bp 0.067; the largest robust Mahalanobis distances of daily 2, 5, 10, and 30 Yr changes fall on 2023-03-13, 2020-03-06, 2023-03-17, 2022-06-13, and 2020-03-17.

## The `riskkit.py` API (the foundation fixes exact signatures)

Day 1 `mc_mean(draws)` (estimate and standard error), `antithetic_normals(rng, n)`; day 2 `var_es(pnl, level)`, `historical_pnl(book, rate_moves, spread_moves)`, `kupiec_pof(exceptions, n, level)`; day 3 `one_factor_defaults(pd, rho, n_sims, rng)`, `vasicek_quantile(pd, rho, q)`, `loss_distribution(book, defaults, lgd)`; day 4 `kaplan_meier(time, event)`; day 5 `person_period(cohort)` (one row per firm-year at risk), `hazard_to_survival(hazards)`; day 6 `robust_z(x)`, `iqr_flags(x, k)`, `precision_recall_at(flags, labels)`; day 7 `mahalanobis_flags(frame, quantile)`; day 8 `psi(expected, actual, bins)`, `psi_table(reference, current, columns)`; day 9 `monitoring_report(reference, current, score_col, target_col)`. Every function has a test on small seeded arrays; `test_riskkit.py` runs in under 10 seconds.

## Day plan

### Week 1: Simulation and default

#### Day 1: `01_monte_carlo_foundations` (hands-on)
How it works for Monte Carlo; `numpy.random.default_rng`, seeds, and why legacy `np.random.seed` is not used; the law of large numbers drawn as the running mean of one bond's simulated loss converging on `PD*LGD*EAD`, with the standard error band shrinking as one over root n; draws from normal, Student's t, lognormal, and beta (recovery) side by side with one setting changed per panel; the count of defaults among 50 independent bonds simulated and checked against `BINOM.DIST`; antithetic variates and the variance they save, in a styled table; how many trials a stated precision needs. Excel: `RAND`, `NORM.S.INV(RAND())`, a Data Table of 1,000 trials. Story candidate: Metropolis and Ulam, "The Monte Carlo Method", JASA, 1949.

#### Day 2: `02_historical_simulation_and_var` (hands-on)
The book's one-day P&L from a rate move (each bond's Treasury change read at its maturity from the curve, times duration and market value) and a spread move (each bond's OAS times the relative change in the synthetic IG or HY index, times spread duration: the DTS approach, published); historical simulation over the development years; VaR and expected shortfall at 95 and 99 percent (`var_es`), the tail drawn; the normal model and a Student's t Monte Carlo beside it; the backtest: exceptions counted walk-forward against a rolling 500-day window, Kupiec's proportion-of-failures test (`kupiec_pof`); every setting (window, level, horizon) swept. Excel: `PERCENTILE.INC` and `AVERAGEIF`. Story candidates: J.P. Morgan's RiskMetrics technical document (1996); Kupiec (1995).

#### Day 3: `03_correlated_defaults_and_the_loss_distribution` (hands-on)
Default rates by rating counted from the cohort's development years, with the low-default problem (AAA and AA show few or none) and a pooled logistic fit on `rating_score` to fill them; the one-factor model: a common factor, an idiosyncratic factor, and a default threshold, drawn; correlation swept in panels (0, 0.1, 0.2, 0.4) showing the same mean loss and a fattening tail; the book's loss distribution with LGD from a beta draw, credit VaR and expected shortfall, losses by sector and by issuer; the Vasicek formula checked against a large homogeneous simulated portfolio; Cholesky for a two-sector correlation matrix, and the error raised by one that is not positive definite (`raises-exception`). The cohort's year factor shown as default clustering by study year. Story candidate: Li (2000) on default correlation, and how the Gaussian copula was later described in the press (source-checked at build or dropped).

#### Day 4: `04_survival_curves_and_kaplan_meier` (hands-on)
How it works for survival: the survival function, the hazard, and censoring; why dropping censored firms biases the curve, shown side by side with the right answer; Kaplan-Meier by hand on ten firms (an Excel table) and with `SurvfuncRight` on the cohort; curves by rating bucket with confidence bands; the log-rank test (`survdiff`) and how to read it; cumulative hazard; a flat hazard and `EXP(-h*t)` beside the empirical curve; the link to Course 2: a constant hazard is how a spread and a recovery rate are turned into a default probability (the credit triangle, a published identity), stated as arithmetic on invented numbers. Story candidate: Kaplan and Meier, JASA, 1958.

#### Day 5: `05_case_study_hazard_models` (hands-on, then case study)
How it works for the Cox model and the discrete-time hazard; `PHReg` on leverage, coverage, rating score, and sector, hazard ratios with intervals, every setting of `PHReg` (ties, strata, and the rest); the proportional-hazards check by fitting on early and late years since entry; `person_period` and a logistic hazard on firm-years (the Shumway approach, published), its coefficients set beside the generator's planted ones; `hazard_to_survival` turning annual hazards into a firm's survival curve; walk-forward by study year inside development, scored by AUC and calibration by decile. Case study with Course 4's skeleton; What the model shows, and where it fails. Story candidates: Cox (1972); Shumway (2001).

### Week 2: The unusual and the drifting

#### Day 6: `06_outliers_robust_rules` (hands-on)
Off-market prints planted in a copy of the blotter (seeded, shown, labelled planted); the z-score and why the outliers it hunts inflate its own spread (masking), shown; the robust z-score from the median and MAD (`robust_z`); Tukey's IQR fences (`iqr_flags`); each trade's distance from its bond's day mid; precision and recall against the planted labels (`precision_recall_at`) across a threshold sweep drawn as a curve; rolling robust statistics on past rows only. Excel: `MEDIAN`, `QUARTILE.INC`, and the MAD as one array formula.

#### Day 7: `07_isolation_forest_and_local_outlier_factor` (hands-on)
Mahalanobis distance on daily 2, 5, 10, and 30 Yr changes, classical against robust (`MinCovDet`), the masking effect drawn; the unusual days listed as history with a dated source for any day the notebook explains; How it works for isolation forest (random splits, path length) and every setting (`n_estimators`, `max_samples`, `contamination`, `max_features`) with sweeps; local outlier factor and `n_neighbors`; the three methods side by side on one planted data set of bonds whose fields disagree (a duration longer than the maturity, a coupon in percent typed as a decimal, a price off by a factor of ten), scored by precision and recall; why `contamination` must not come from the labels.

#### Day 8: `08_population_stability_and_drift` (hands-on)
How it works for PSI: the bins from the reference sample, the share in each, the sum, the empty-bin problem and its floor; PSI by hand in Excel and with `psi`; the 10 Yr level against its daily change (probed: 12.4 against 0.067), drawn as overlaid histograms; bin count and binning method swept; PSI over rolling windows as a line chart; per-feature PSI (`psi_table`) on the cohort's entering firms, finding the planted shift from study year 11; PSI against the KS test and Jensen-Shannon divergence in one table, and what each misses. Thresholds quoted only with their source, found at build (candidate: Yurdakul, 2018, Western Michigan University); without one, the notebook gives none.

#### Day 9: `09_case_study_monitoring_a_credit_model` (hands-on, then case study)
Day 5's discrete-time hazard fitted on study years 1 to 10, then monitored year by year over 11 to 14: PSI of the score and of each input, AUC by year, calibration (fitted default rate against the counted one), robust flags on each year's inputs; `monitoring_report` as a styled table with a green, amber, and red column whose bands are stated and sourced or stated as the course's choice for the exercise; a model whose inputs drift while its ranking holds, and the reverse. Case study with Course 4's skeleton; What the model shows, and where it fails. Story candidate: the Federal Reserve's SR 11-7, Supervisory Guidance on Model Risk Management (2011), on ongoing monitoring.

#### Day 10: `course5c_capstone`
A risk report on the synthetic book and the cohort: Monte Carlo credit loss with VaR and expected shortfall, historical VaR of the book with its backtest on the held-out years, the hazard model chosen on development and opened once on held-out study years 15 to 20, an anomaly screen of a planted month of trades, and a PSI table between development and held-out years for both the cohort and the curve; closing "What the models show, and where they fail". Excel in and out. Solutions notebook complete.

## Where the files live

As Course 5B: `instructor/_build/course5c/` holds `c5clib.py` (built on `c5blib`, extended only where this spec says), `c5cdeck.js`, `assemble.py`, `fragments/` (the `riskkit` reference, day by day), `notebooks/build_NN_*.py`, `script_wWdD.json`, `wWdD_deck.js`, `excel_checks/`, `notes/`, and a build `README.md`. Runtime budget: a teaching notebook 7 minutes on one thread, the capstone's solutions 11 (Jeff, 2026-10-20).

## READMEs and series files to update when the course is built

`course5c_risk_models/README.md` (the course README standard), the root README's course table and the path image (`tools/make_path_diagram.py`, Course 5C between 5B and 6), `EXCEL.md` rows, `DATA.md` and `data/README.md` (the cohort file, its generator, its planted coefficients), `tests/test_data.py`, `CURRICULUM.md`, `CLAUDE.md` status and layout lines. The root `requirements.txt` is unchanged.

## Questions settled (Jeff accepted every default, 2026-10-22)

1. Survival data is a new synthetic cohort, because no free, redistributable corporate default history exists to commit. Default: yes.
2. Default rates come from that cohort, not from an agency default study (copyrighted and revised yearly). Default: yes.
3. Order: Monte Carlo and VaR first, then default models, then anomalies and drift. Default: as written.
4. Copulas beyond the one-factor Gaussian (Student's t copula, multi-factor) are out. Default: out, with the t copula as an optional exercise on day 3.
