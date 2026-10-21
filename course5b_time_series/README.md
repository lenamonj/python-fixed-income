<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="325">
</picture>

[![Course 5B](https://img.shields.io/badge/Course_5B-Time_Series_Models-123D2F?style=for-the-badge)](../README.md)
[![Length](https://img.shields.io/badge/2_weeks-9_notebooks_%2B_capstone-1C7A57?style=for-the-badge)](#course-map)
[![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)](../README.md#run-in-google-colab-with-nothing-to-install)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[The two weeks](#the-two-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Course 5](../course5_advanced_ml/README.md)** &nbsp;·&nbsp; **[Course 6](../course6_neural_networks/README.md)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 5B: Time Series Models

**Two weeks from a gap in a dated table to ARIMA, exponential smoothing, GARCH, and gradient boosting on lags, every model scored walk-forward against carrying the last value forward, and every result described, never forecast.**

</div>

On day one you take the U.S. Treasury's daily yield curve, find every gap in it, tell a market holiday from an outage from a tenor that had not started yet, correct wrong values with a change log, and fill gaps on purpose with the method that suits each one. Two weeks later you set a frequency and build lags with no lookahead; test a series for stationarity and difference it; read an ACF and a PACF and pick an order from them; fit AR and ARIMA, exponential smoothing, and GARCH with statsmodels and arch and read every setting; build lag features for LightGBM with no leak; test two series for cointegration and measure a half-life of mean reversion; and say plainly, with numbers, which model beat carrying the last value forward and which did not.

**That is the course: classical time series models, fitted and scored honestly, on data that is described, never forecast.**

Course 3 got dated data, cleaned it, and described it, and fitted no model. Course 5B models a series, so it needs the regression of Course 4 and the boosting of Course 5.

Every model in this course describes the past. A model's output is a fitted change, the model's one-step value for a date inside the file, or a fitted volatility, and it is never a forecast, a projection, or a view on rates. Every value is for a date from 2015-01-02 to 2026-10-02, from a model fitted on earlier dates only. The honest finding of the course, that nothing fitted on past daily changes of the 10 Yr beats carrying the last value forward by more than the folds disagree, while the size of a change is far from random, is taught as the lesson.

Every function goes into a module of your own, `tskit.py`, beside the `mlkit.py` and `ensemblekit.py` you built in Courses 4 and 5. It imports `mlkit` and never changes it, with a test file that grows every day.

Four habits run through all of it.

| Habit | What it means |
|:---|:---|
| **The past only** | Every lag, change, rolling statistic, and fill is checked to use only earlier dates. Models are fitted and scored walk-forward inside the development years, 2015 to 2022, and the held-out years, 2023 to 2026, are opened once, in the capstone. |
| **Excel as the bridge** | Excel has no ADF test, no ARIMA, and no GARCH fitter, and each notebook says so where it applies. Then it shows what Excel can do, with the formula beside the Python: a forward fill as one `IF`, interpolation by hand, a lag as the cell one row up, an autocorrelation as `CORREL` of two offset ranges, AR(1) as `SLOPE` and `INTERCEPT`, EWMA and the GARCH(1,1) variance as one recursive formula each. |
| **The same answer on every run** | One seed, `SEED = 42`, and one thread for the maths libraries, so a rerun prints the same digits, and a run on every core prints them too. |
| **Describe, never forecast** | Every model output has a plain name and a list of names it is never given. Case studies end with "What the model shows, and where it fails" instead of recommendations. |

You need Course 5, or the same ground: walk-forward splits from Course 4, regression, and LightGBM. Each notebook writes the reference `mlkit.py` and the `tskit.py` it starts from into its work folder, so a missing or unfinished module never stops it. Course 5B sits between Course 5 and [Course 6](../course6_neural_networks/README.md), whose sequence networks on the Treasury curve come after it.

Status: <!-- count:ready -->5<!-- /count --> of <!-- count:total -->9<!-- /count --> notebooks are ready; the capstone is coming.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here). Course 5B runs in the same `.venv` as Courses 1 to 5.

| Step | What to do |
|:---|:---|
| **Install the course's packages** | With the course's `.venv` active, run the install line below. It adds `arch`, the GARCH library, to Course 5's pins, and changes none of them. |
| **No API key** | This course needs no key and no account. Every dataset is in the repo. An optional exercise later in the course shows a student with Course 3's FRED key how to run the same workflow on a licensed spread series on their own screen, never saved. |
| **Keep your folder** | Your `my_bondmath` folder, in your `projects` folder beside the course repo, gains `tskit.py` and its tests beside `mlkit.py` and `ensemblekit.py`. If you skipped the earlier courses, create it with the last line below. |
| **Or use Colab** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge. Colab's library versions can differ from the pins, so a printed number may differ in its last digits; the setup cell says so when it happens. At the end of each day, download your files from the Colab file browser. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course5b_time_series\requirements.txt
New-Item -ItemType Directory -Force "$HOME\projects\my_bondmath" | Out-Null
```

Each notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Each day's "Bring It Home" section shows the PowerShell steps that move the day's functions and tests into `my_bondmath`, run the tests, and commit.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. As in Courses 2 to 6, every notebook ends in the same order: Excel side by side, save the day with Git, bring it home, then the exercises, with the AI check last. Every section that teaches a method opens with a short "How it works" paragraph, every estimator's settings are read from the installed library into a table, and every lesson is drawn: small multiples with one thing changed per panel, and every comparison as a chart and a formatted table with the best value marked.

## The two weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | A series, its gaps, and its memory | Find, diagnose, correct, and fill every gap in a dated table with a change log; build lags and changes with no lookahead and score the naive baselines walk-forward; test for stationarity and difference; read an ACF and a PACF; and fit AR and ARIMA against the baselines |
| 2 | Beyond ARIMA | Fit exponential smoothing, describe volatility with GARCH and its half-life, build lag features for LightGBM with no leak, test two series for cointegration and measure a half-life of mean reversion, and open the held-out years once in the capstone |

## Course map

<!-- map:start -->

### Week 1: A series, its gaps, and its memory

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Missing Data, Gaps, and Corrections](week1/day1/01_missing_data_gaps_and_corrections.ipynb) | Four kinds of missing in a dated table, a heatmap of blanks over time and runs of blanks, absent weekdays checked against a holiday calendar, wrong values found and corrected with a change log (and why `update` cannot blank a cell), `combine_first` from a second source, every fill side by side against the true values, `limit` and `limit_area`, and a score a backfill improves falsely, beside `IF`, `NETWORKDAYS`, interpolation by hand, and `XLOOKUP` in Excel | Ready |
| 2 | [Frequency, Lags, and the Naive Baselines](week1/day2/02_frequency_lags_and_the_naive_baselines.ipynb) | Business-day frequency, `shift` and `diff` in bp, the development and held-out years, the last value carried forward, the mean, and drift as baselines, MAE, RMSE, and MASE, and walk-forward scoring | Ready |
| 3 | [Stationarity and Differencing](week1/day3/03_stationarity_and_differencing.ipynb) | AR(1) series side by side as phi rises to 1, rolling mean and spread, ADF and KPSS and what to do when they disagree, a spurious regression, and differencing | Ready |
| 4 | [Autocorrelation: ACF and PACF](week1/day4/04_autocorrelation_acf_and_pacf.ipynb) | Lag scatter plots, autocorrelation by hand and by `CORREL`, the confidence band, PACF, the identification grid, changes against their squares, and Ljung-Box | Ready |
| 5 | [Case Study: AR and ARIMA on the Curve](week1/day5/05_case_study_ar_and_arima_on_the_curve.ipynb) | AR, MA, and ARIMA, the AIC and BIC grid, every setting of `ARIMA`, residual diagnostics, and one-step values walk-forward against the baselines, then a case study: what the model shows, and where it fails | Ready |

### Week 2: Beyond ARIMA

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | Exponential Smoothing | EWMA by hand and in one Excel formula, alpha swept in panels, simple, Holt, and damped smoothing, every setting of `ExponentialSmoothing`, and EWMA of squared changes | Coming |
| 2 | Volatility Clustering and GARCH | Squared changes and their ACF, rolling, EWMA, and GARCH(1,1) volatility on one chart, persistence and the half-life of a shock, every setting of `arch_model`, and fitted volatility scored walk-forward | Coming |
| 3 | Lag Features and Gradient Boosting | `lag_features` built with no leak, LightGBM on lags walk-forward against the baselines, ARIMA, and smoothing, the settings that matter for a series, and a leak shown on purpose | Coming |
| 4 | Two Series: Cointegration and Mean Reversion | Levels against changes, Engle-Granger on the 5 Yr and 10 Yr and on the synthetic IG and HY spreads, the hedge ratio, the half-life of mean reversion, and a rolling hedge ratio, described, never traded | Coming |
| 5 | Course 5B Capstone | The course's workflow on 2s10s and the synthetic HY spread: repair, stationarity, ACF, baselines, ARIMA, smoothing, LightGBM on lags, GARCH, a choice on development, and the held-out years opened once | Coming |

<!-- map:end -->

## The capstone

Day 5 of week 2 is yours. You run the course's workflow on two series, 2s10s and the synthetic high yield spread: repair the planted gaps with a change log, set the development and held-out years, test stationarity, read the ACF and PACF, fit the baselines, ARIMA, exponential smoothing, and LightGBM on lags walk-forward on the development years, describe volatility with GARCH, choose on development, open the held-out years once, and write "What the models show, and where they fail". A worked version sits beside it.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| pandas | Dated tables, gaps, corrections, fills, lags, and changes | Week 1, Day 1 |
| statsmodels | ADF and KPSS tests, ACF and PACF, ARIMA, exponential smoothing, Ljung-Box, and cointegration | Week 1, Day 3 |
| arch | GARCH volatility models | Week 2, Day 2 |
| LightGBM | Gradient boosting on lag features | Week 2, Day 3 |
| pytest and Git | Testing `tskit.py` every day, and keeping the change log and each model's results beside the code | Week 1, Day 1 |
| matplotlib and `plotkit.py` | Every chart, and formatted comparison tables with pandas' Styler; `plotkit.py` is Course 4's helper file, written unchanged into every work folder | Week 1, Day 1 |
| scikit-learn and scipy | Metrics and Course 4's `mlkit.py`, which imports them | Week 1, Day 1 |
| XGBoost, CatBoost, Optuna, imbalanced-learn, SHAP, ipywidgets | Not used; kept from Course 5's pins so one environment runs Courses 4 to 6 | |

Exact versions are pinned in [`requirements.txt`](requirements.txt): `arch` 8.0.0 on top of Course 5's pins, among them numpy 2.5.3, pandas 3.0.6, statsmodels 0.15.0, scikit-learn 1.9.1, LightGBM 4.7.0, and pytest 9.1.1. Git is installed separately (see [Course 2](../course2_bond_math/README.md#before-you-start)).

| Data | Kind | Used in |
|:---|:---|:---|
| Daily Treasury par yield curve rates, 2015-01-02 to 2026-10-02 | Real, public: U.S. Department of the Treasury, public domain | Every day |
| 2,940 daily investment grade and high yield spreads in bp | Synthetic: invented for Course 3, not ICE, Moody's, or any index | Days 3, 4, 6, and 9, and the capstone |

Day 1's gaps, outage, and wrong values are planted in a copy of the Treasury file by a seeded generator inside the notebook, and the notebook says so; the published file is kept aside to check every repair against. Course 5B adds no data file. Sources and terms for every file are in [the data page](../data/README.md).

## What comes next

[Course 6 is Neural Networks](../course6_neural_networks/README.md): three weeks from one neuron worked out by hand to dense, recurrent, and convolutional networks, ending with sequence models on the same Treasury curve, scored walk-forward against the same last value carried forward.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
