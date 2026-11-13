<div align="center">

<a href="../README.md"><img src="../assets/readme/landing/course05b_time_series.png" width="830" alt="Python for Fixed Income. Course 5B: Time Series Models. 2 weeks, 10 notebooks, free. Stage 2 of 4, Machine learning. Created by Jeff Lenamon."></a>

[![Python](https://img.shields.io/badge/Python-3.13-17807F?style=for-the-badge&labelColor=0E1B2E&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-17807F?style=for-the-badge&labelColor=0E1B2E)](../README.md#run-in-google-colab-with-nothing-to-install)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-17807F?style=for-the-badge&labelColor=0E1B2E)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-17807F?style=for-the-badge&labelColor=0E1B2E)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[The two weeks](#the-two-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Course 5](../course05_advanced_ml/README.md)** &nbsp;·&nbsp; **[Course 5C](../course05c_risk_models/README.md)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 5B: Time Series Models

**Two weeks from a gap in a dated table to ARIMA, exponential smoothing, GARCH, and LightGBM on lag features, every model scored walk-forward against carrying the last value forward, and every result described, never forecast.**

</div>

On day one you take a copy of the U.S. Treasury's daily par yield curve with blank days, a feed outage, and wrong prints planted in it, and you find, correct, and fill each problem with a change log, checking every repair against the true values.
Two weeks later you set the development and held-out years before reading a value; build lags and changes and prove with the cut test that each reads only earlier dates; score the last value carried forward, the training mean, and drift over five walk-forward folds; run ADF and KPSS and difference a series; read an ACF and a PACF and name an order; fit AR and ARIMA, exponential smoothing, GARCH, and LightGBM on lag features; and test two series for cointegration and measure the half-life of their gap.
Then the capstone hands you a damaged copy of the curve and a synthetic HY spread, and you repair it, choose your models on the development years by a rule written first, open the held-out years once, and write what the models show and where they miss.

**That is the course: classical time series models, fitted and scored honestly, on data that is described, never forecast.**

Course 3 got dated data, cleaned it, and described it, and fitted no model.
Course 5B models a series, so it needs the regression and walk-forward folds of Course 4 and the boosting of Course 5.

Every model in this course describes the past.
A model's output is a fitted change, a one-step value for a date inside the file, or a fitted volatility, from a model fitted on earlier dates only.
Textbooks call these forecasting models; here every value is for a date from 2015 to 2026 that has already happened, scored against what happened, and never a forecast, a projection, or a view on rates or spreads.
The half-life of a gap between two series says how fast that gap closed over those years, never a trade.

Each notebook is one problem worked from start to finish: a problem statement, the data, the charts, the models, their scores on dates they never saw, and what they show.
Nothing is built outside the notebook.
The few functions a day reuses are defined on the page, where you can read every line.

Five habits run through all of it.

| Habit | What it means |
|:---|:---|
| **The past only** | The cut at 2022-12-30 is set on Day 2 before a value is read. Every model is fitted, scored, and chosen on the development years, 2015 to 2022, and the held-out years, 2023 to 2026, are opened once, in the capstone. Every lag, change, trailing statistic, and fill a model reads passes the cut test, and dated rows are never shuffled. |
| **One bar, five folds** | Day 2 cuts the development years into five walk-forward folds of 252 dates and scores the last value carried forward on them. Every later model is scored on the same folds, as MASE against that bar, and is called better only when its edge is larger than the folds disagree. |
| **Predict, then run** | Four times a notebook stops and asks you to write down a number or sketch a chart before the cell that answers it. The answer is never on the page before the question. |
| **The same answer on every run** | One seed, `SEED = 42`, one generator for every simulated series, one thread for the maths libraries, and `n_jobs=1` on LightGBM, so a rerun prints the same numbers. |
| **Describe, never forecast** | Every output has a plain name, said once: a fitted change, a one-step value, a fitted volatility, a residual. Case studies end with where the models miss, not with a recommendation. |

You need Course 5, or the same ground: Course 3's dated data and its cut test, Course 4's regression with statsmodels and its walk-forward folds on dated rows, and Course 5's LightGBM.
Course 5B sits between Course 5 and Course 5C in [Python for Fixed Income](../README.md).

Status: <!-- count:ready -->9<!-- /count --> of <!-- count:total -->9<!-- /count --> notebooks and the capstone are ready.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here).
Course 5B runs in the same `.venv` as Courses 1 to 5.

| Step | What to do |
|:---|:---|
| **Install the course's packages** | With the course's `.venv` active, run the install line below. It adds `arch`, the GARCH library, to the libraries of Courses 4 and 5, and changes none of their versions. |
| **No API key** | This course needs no key and no account. Every dataset is in the repo. An optional exercise on Day 9 and in the capstone shows a student with Course 3's FRED key how to run the same steps on licensed ICE BofA spread series on their own screen, never saved. |
| **Or use Colab** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge. Colab's library versions can differ from the pins, so a printed number may differ in its last digits. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course05b_time_series\requirements.txt
```

Each notebook reads its data from the repo's `data` folder, or from GitHub in Colab, and writes no file.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook.
[How a day works](../README.md#how-a-day-works) explains the pattern.
Every notebook in this course follows Course 4's ladder: a problem statement (the business context, the objectives, and the data dictionary), then numbered sections from Setting Up to Insights and Conclusion, then what you can now do and the exercises, with the AI check last: an answer written in the style of an AI assistant that runs and has one bug to find.
Every model is shown, not only printed: ten or more charts and pictures on a teaching day, among them fill strips against the held-back true values, a calendar heatmap, a filmstrip of simulated series as one setting climbs to 1, ACF and PACF bars with their band, the identification grid, a root map on the unit circle, a weight decay under a timeline, a news-impact curve, partial dependence with ICE lines, and a vector field of a pair's moves.
Every teaching day has a slider to move, with a still picture under it for where a widget cannot run.

## The two weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | A series, its gaps, and its memory | Find, correct, and fill the gaps in a dated table with a change log; set the cut, build lags and changes from earlier dates only, and score the naive baselines over five walk-forward folds; run ADF and KPSS and difference a series; read an ACF and a PACF and name an order; and fit AR and ARIMA and score them against the last value |
| 2 | Beyond ARIMA, and the capstone | Fit simple, Holt, and damped exponential smoothing and an EWMA of the size of a change; fit GARCH with arch and read its persistence and half-life; build lag features for LightGBM, catch a leak, and read importance against planted noise; test two series for cointegration and measure the half-life of their gap; and run the whole workflow on two series, opening the held-out years once |

## Course map

<!-- map:start -->

### Week 1: A series, its gaps, and its memory

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Missing Data, Gaps, and Corrections](week1/day1/01_missing_data_gaps_and_corrections.ipynb) | Four kinds of missing told apart and counted, the dated rows checked against the market calendar, wrong values found by their shape and by a second source and corrected with a change log, runs of blanks filled four ways and scored against held-back values, and the cut test and `limit=` on a fill | Ready |
| 2 | [Frequency, Lags, and the Naive Baselines](week1/day2/02_frequency_lags_and_the_naive_baselines.ipynb) | Development and held-out years set before a value is seen, lags and changes built by rows and proved with the cut test, the last value carried forward, the training mean and drift as baselines, MAE, RMSE and MASE, the walk-forward loop over five folds, and how far the folds disagree before one rule is called better | Ready |
| 3 | [Stationarity and Differencing](week1/day3/03_stationarity_and_differencing.ipynb) | A trailing mean with a band, AR(1) series built from one set of shocks as phi rises to 1, ADF and KPSS each read against its own null and together in four readings on five series, a regression between two wandering series, and differencing once, twice, and after a log | Ready |
| 4 | [Autocorrelation: ACF and PACF](week1/day4/04_autocorrelation_acf_and_pacf.ipynb) | An autocorrelation by hand and with `acf`, the ACF and its band, what white noise alone puts outside it, changes against their squares, the PACF as a regression coefficient, the identification grid for AR, MA and ARMA, Ljung-Box by hand and with `acorr_ljungbox`, and a lag checked window by window | Ready |
| 5 | [Case Study: AR and ARIMA on the Curve](week1/day5/05_case_study_ar_and_arima_on_the_curve.ipynb) | An AR(1) fitted by hand and with `ARIMA`, one-step values with `.append()`, MA and ARIMA and one shock traced through each, AIC and BIC over p and q, the roots on the unit circle, residual diagnostics, and every order scored walk-forward on five folds against the last value | Ready |

### Week 2: Beyond ARIMA

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Exponential Smoothing](week2/day1/06_exponential_smoothing.ipynb) | The EWMA by hand and as a weighted average, alpha chosen on training misses, simple, Holt and damped smoothing with every setting of `ExponentialSmoothing`, five series scored walk-forward against the last value, and an EWMA of the size of a change with RiskMetrics beside it | Ready |
| 2 | [Volatility Clustering and GARCH](week2/day2/07_volatility_clustering_and_garch.ipynb) | Where the largest days fall, the GARCH(1,1) recursion with a slider, half-lives of persistence, GARCH fitted on five series with arch, three volatilities through 2020, normal against Student's t and seven variance models by BIC, the news-impact curve, and the size of a change scored walk-forward | Ready |
| 3 | [Lag Features and Gradient Boosting](week2/day3/08_lag_features_and_gradient_boosting.ipynb) | Fifteen lag features built from past rows only and passed through the cut test, a weekday and correlation read, LightGBM on lags walked over five folds, one leaky column caught, four settings swept with early stopping, every rule scored by MASE on five series, shuffled importance against five noise columns, and the size with partial dependence | Ready |
| 4 | [Two Series: Cointegration and Mean Reversion](week2/day4/09_two_series_cointegration_and_mean_reversion.ipynb) | Two pairs drawn together, a hedge ratio by eye with a slider and by least squares, the gap and its bands, a map of each pair's past 20-row moves, the Engle-Granger test on each pair's gap, the half-life of a gap beside random walks, and the hedge ratio rolled through the years and tested on each fold | Ready |
| 5 | [Course 5B Capstone](week2/day5/course5b_capstone.ipynb) | The course's workflow on the 2s10s and the synthetic HY spread: a planted copy repaired with a log, stationarity and memory, Day 2's folds and bar, ARIMA, smoothing and LightGBM on lags, GARCH for the size, four choices by Day 2's rule, and the held-out years opened once on three refitted blocks | Ready |

<!-- map:end -->

## The capstone

Day 5 of week 2 is yours.
A colleague hands you a copy of the 2 Yr and 10 Yr yields and a synthetic HY spread, with blank days and a few wrong prints planted in it by a seeded generator, as on Day 1, and the true values kept aside to check your repair.
You repair the copy with a corrections table, a change log, and a capped fill, build the 2s10s slope and the HY in bp, and ask the course's two questions of each: does any model of the change get closer than the last value carried forward, and does any rule for the size of a change get closer than a constant?

You test both series for a unit root and read the memory in the change and in its size.
You score ARIMA, exponential smoothing, and LightGBM on lag features for the change, and an EWMA and GARCH for the size, all on Day 2's five folds, and you write the choice rule down before a held-out value is read.
Then you open the held-out years once, refit every model block by block as a fold was refitted, score each one there, and read where the misses fall with a Bland-Altman plot, a hanging rootogram, and a wedge plot.

| File | What it is |
|:---|:---|
| [`course5b_capstone.ipynb`](week2/day5/course5b_capstone.ipynb) | The brief, the questions, and a check line for every answer that can be checked. A check compares a fingerprint of your answer with a stored one, so it says correct or not yet and no answer is on the page |
| [`course5b_capstone_overview.pdf`](week2/day5/course5b_capstone_overview.pdf) | The brief as slides: the problem, the two series, and what each part of the work asks |
| [`course5b_capstone_solutions.ipynb`](week2/day5/course5b_capstone_solutions.ipynb) | The worked version, with every decision stated. Open it after you finish |

What you write describes the past of a real Treasury slope and a synthetic spread.
Nothing you build is a forecast, a view on rates or spreads, or a trade.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| pandas, matplotlib, and seaborn | Dated tables, gaps, corrections, fills, lags, and changes, and every chart | Week 1, Day 1 |
| ipywidgets | The sliders | Week 1, Day 1 |
| scikit-learn | The walk-forward folds (`TimeSeriesSplit`) and MAE and RMSE; later permutation importance and partial dependence | Week 1, Day 2 |
| statsmodels | The ADF test, least squares, ACF and PACF, Ljung-Box, AR and ARIMA, exponential smoothing, and the Engle-Granger test | Week 1, Day 3 |
| arch | The KPSS test, then GARCH and its variants | Week 1, Day 3 |
| scipy | The chi-squared, normal, and Student's t distributions behind Ljung-Box, the tails, and the Q-Q plots | Week 1, Day 4 |
| LightGBM | Gradient boosting on lag features | Week 2, Day 3 |

Exact versions are pinned in [`requirements.txt`](requirements.txt).
The file also pins a few libraries from Course 5 that no notebook here imports, so one environment runs Courses 4 to 6.

| Data | Kind | Used in |
|:---|:---|:---|
| Daily Treasury par yield curve rates, 2015-01-02 to 2026-10-02, 14 tenors | Real, public: U.S. Department of the Treasury, public domain | Every day |
| 2,940 daily investment grade and high yield spreads in bp, one per date of the Treasury file | Synthetic: invented for Course 3 by its generator, not ICE, Moody's, or any index | Days 2 to 9, and the capstone |

The course's five series, all in bp, are the 2 Yr and 10 Yr yields, the 2s10s slope, and the synthetic IG and HY spreads.
Day 2 cuts them at 2022-12-30.
The 2,001 rows from 2015 to 2022 are the development years, where every model is fitted, scored, and chosen on five walk-forward folds of 252 dates with the last value carried forward as the bar.
The 939 rows from 2023 on are the held-out years, opened once, in the capstone.
Day 1's blanks, outage, and wrong prints, and the capstone's blanks and wrong prints, are planted in a copy by a seeded generator inside the notebook, and the notebook says so; the true values are kept aside to check every repair against.
Course 5B adds no data file.
Sources and terms for every file are in [the data page](../data/README.md).

## What comes next

[Course 5C is Risk Models](../course05c_risk_models/README.md): two weeks of Monte Carlo and VaR, correlated defaults, survival and hazard models, screens for unusual data, and the population stability index.
[Course 6, Neural Networks](../course06_neural_networks/README.md), follows it, ending with sequence models on the same Treasury curve.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
