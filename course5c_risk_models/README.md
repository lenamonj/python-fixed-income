<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="325">
</picture>

[![Course 5C](https://img.shields.io/badge/Course_5C-Risk_Models-123D2F?style=for-the-badge)](../README.md)
[![Length](https://img.shields.io/badge/2_weeks-9_notebooks_%2B_capstone-1C7A57?style=for-the-badge)](#course-map)
[![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)](../README.md#run-in-google-colab-with-nothing-to-install)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[The two weeks](#the-two-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Course 5B](../course5b_time_series/README.md)** &nbsp;·&nbsp; **[Course 6](../course6_neural_networks/README.md)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 5C: Risk Models

**Two weeks of the models a risk desk runs: Monte Carlo and VaR, correlated defaults, survival and hazard models, screens for unusual data, and the population stability index, every one on synthetic or public data and every result described, never forecast.**

</div>

On day one you simulate one bond's credit loss year by year and check the simulation against the exact expected loss, then measure how far a Monte Carlo answer can be from the truth. Two weeks later you compute VaR and expected shortfall of the course's synthetic book and backtest them; simulate correlated defaults and read the tail of the loss distribution; estimate survival curves with censoring and fit Cox and discrete-time hazard models; flag unusual trades and curve days with robust rules, Mahalanobis distance, isolation forest, and local outlier factor; compute PSI by hand and on a model's inputs; and write a monitoring table that says, with numbers, what drifted and what did not.

**That is the course: risk models built, checked against what is known, and read for what they say and what they cannot.**

Every loss in this course is a conditional statement: had these past days repeated, or under these invented inputs. Default rates come from a synthetic cohort of invented firms, never from an agency study or a real issuer. A flagged trade is a print to check, never a mispriced bond. PSI says how far a mix moved, never where it goes next.

Every function goes into a module of your own, `riskkit.py`, beside the `mlkit.py`, `ensemblekit.py`, and `tskit.py` you built in Courses 4, 5, and 5B. It imports `mlkit` and never changes it, with a test file that grows every day.

Four habits run through all of it.

| Habit | What it means |
|:---|:---|
| **Check against a known answer** | Every simulation is first run on a case with an exact answer, and every model on data whose planted values are written down, so you can see it recover them. |
| **Excel as the bridge** | Excel draws with `RAND()` and `NORM.S.INV`, repeats a sheet with a Data Table, and has `BINOM.DIST`, `PERCENTILE.INC`, and `NORM.S.DIST`; it has no Cholesky factor, no Cox model, and no isolation forest, and each notebook says so where it applies. |
| **The same answer on every run** | One seed, `SEED = 42`, a fresh generator from it for every experiment, and one thread for the maths libraries, so a rerun prints the same digits. |
| **Describe, never forecast** | Every model output has a plain name and a list of names it is never given. Case studies end with "What the model shows, and where it fails" instead of recommendations. |

You need Course 5B, or the same ground: walk-forward splits and logistic regression from Course 4, and the development and held-out years of Course 5B. Each notebook writes the reference `mlkit.py` and the `riskkit.py` it starts from into its work folder, so a missing or unfinished module never stops it. Course 5C sits between Course 5B and [Course 6](../course6_neural_networks/README.md).

Status: <!-- count:ready -->7<!-- /count --> of <!-- count:total -->10<!-- /count --> notebooks are ready. The course is being built one day at a time.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here). Course 5C runs in the same `.venv` as Courses 1 to 5B.

| Step | What to do |
|:---|:---|
| **Install the course's packages** | With the course's `.venv` active, run the install line below. Course 5C uses Course 5B's pins unchanged: no new library. |
| **No API key** | This course needs no key and no account. Every dataset is in the repo. |
| **Keep your folder** | Your `my_bondmath` folder, in your `projects` folder beside the course repo, gains `riskkit.py` and its tests. If you skipped the earlier courses, create it with the last line below. |
| **Or use Colab** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge. Colab's library versions can differ from the pins, so a printed number may differ in its last digits; the setup cell says so when it happens. At the end of each day, download your files from the Colab file browser. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course5c_risk_models\requirements.txt
New-Item -ItemType Directory -Force "$HOME\projects\my_bondmath" | Out-Null
```

Each notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Each day's "Bring It Home" section shows the PowerShell steps that move the day's functions and tests into `my_bondmath`, run the tests, and commit.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. Every section that teaches a method opens with a short "How it works" paragraph, every setting is read from the installed library into a table, and every lesson is drawn.

## The two weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | Simulation and default | Run a seeded Monte Carlo and state its error; compute VaR and expected shortfall of the book and backtest them; simulate correlated defaults and read the loss tail against the Vasicek formula; estimate survival curves with censoring; and fit Cox and discrete-time hazard models |
| 2 | Unusual data and drift | Flag unusual trades and curve days with robust rules, Mahalanobis distance, isolation forest, and local outlier factor; compute PSI by hand and on a model's inputs; monitor a credit model year by year; and open the held-out years once in the capstone |

## Course map

<!-- map:start -->

### Week 1: Simulation and default

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Monte Carlo Foundations](week1/day1/01_monte_carlo_foundations.ipynb) | One bond's loss simulated year by year against PD x LGD x EAD, seeds and independent streams, the standard error and the price of precision, the normal, Student's t, lognormal, and beta, defaults among 50 bonds against the binomial, antithetic pairs, and how many trials a precision needs, beside `RAND`, `NORM.S.INV`, a Data Table, and `BINOM.DIST` in Excel | Ready |
| 2 | [Historical Simulation and VaR](week1/day2/02_historical_simulation_and_var.ipynb) | The book's exposure by key rate and by DTS, its daily P&L had each day of 2015 to 2022 repeated, VaR and expected shortfall from the history, a normal model, and a fitted Student's t, every setting swept, and a walk-forward backtest with Kupiec's test, beside `PERCENTILE.INC`, `AVERAGEIF`, and `CHISQ.DIST.RT` in Excel | Ready |
| 3 | [Correlated Defaults and the Loss Distribution](week1/day3/03_correlated_defaults_and_the_loss_distribution.ipynb) | Default rates from the synthetic cohort and the low-default problem, defaults that cluster by year, the one-factor model with its correlation swept, the Vasicek formula against a simulation, the book's credit loss with VaR and expected shortfall by sector, and Cholesky, beside `AVERAGEIFS`, `NORM.S.DIST`, and `BETA.INV` in Excel | Ready |
| 4 | [Survival Curves and Kaplan-Meier](week1/day4/04_survival_curves_and_kaplan_meier.ipynb) | Censoring and the bias of dropping it, Kaplan-Meier by hand and in statsmodels with its band, curves by rating, the log-rank test, the hazard and a flat hazard, and the credit triangle on invented numbers, beside `COUNTIF`, `COUNTIFS`, and `EXP` in Excel | Ready |
| 5 | [Case Study: Hazard Models](week1/day5/05_case_study_hazard_models.ipynb) | A firm-year table, the Cox model with covariates that change year by year and its settings swept, the proportional-hazards check, a logistic hazard against the generator's planted coefficients, survival curves from hazards, then a case study scored walk-forward by AUC and calibration: what the model shows, and where it fails, beside `SUMPRODUCT`, `EXP`, and `PRODUCT` in Excel | Ready |

### Week 2: Unusual data and drift

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Outliers: Robust Rules](week2/day1/06_outliers_robust_rules.ipynb) | Off-market prints planted in a copy of the blotter, each trade's distance from a reference, masking shown, the robust z-score at the published 3.5 and Tukey's fences, precision and recall against the planted labels with a threshold sweep, and rolling scores on past trades only, beside `MEDIAN`, the MAD as an array formula, and `QUARTILE.INC` in Excel | Ready |
| 2 | [Isolation Forest and Local Outlier Factor](week2/day2/07_isolation_forest_and_local_outlier_factor.ipynb) | The robust Mahalanobis distance on daily curve changes with masking drawn and the unusual days listed as history, field errors planted in a copy of the book, isolation forest with every setting read and swept, local outlier factor and its neighbourhood, three screens judged on planted and untouched books, and why contamination never comes from the labels, beside `MINVERSE`, `MMULT`, and `CHISQ.INV` in Excel | Ready |
| 3 | Population Stability and Drift | PSI by hand and by function, the 10 Yr level against its change, per-feature PSI on the cohort, KS and Jensen-Shannon | Planned |
| 4 | Case Study: Monitoring a Credit Model | A hazard model watched year by year: score and input PSI, AUC, calibration, and a monitoring table | Planned |
| 5 | Course 5C Capstone | A risk report on the book and the cohort, with the held-out years opened once | Planned |

<!-- map:end -->

## The capstone

Day 5 of week 2 is yours: a risk report on the synthetic book and the synthetic cohort. Monte Carlo credit loss with VaR and expected shortfall, historical VaR with its backtest, a hazard model chosen on the development years and opened once on the held-out years, an anomaly screen of a planted month of trades, and a PSI table between the two periods. A worked version sits beside it.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| numpy | Seeded generators, independent streams, and every simulation | Week 1, Day 1 |
| scipy | The normal and binomial distributions, and later the KS test | Week 1, Day 1 |
| statsmodels | Kaplan-Meier, the log-rank test, and the Cox model | Week 1, Day 4 |
| scikit-learn | Isolation forest, local outlier factor, robust covariance, and the logistic hazard | Week 2, Day 2 |
| pandas | The book, the cohort, the blotter, and the curve | Week 1, Day 1 |
| pytest and Git | Testing `riskkit.py` every day, and keeping the code under version control | Week 1, Day 1 |
| matplotlib and `plotkit.py` | Every chart, and formatted comparison tables with pandas' Styler; `plotkit.py` is Course 4's helper file, written unchanged into every work folder | Week 1, Day 1 |

Exact versions are pinned in [`requirements.txt`](requirements.txt), Course 5B's file unchanged, among them numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, statsmodels 0.15.0, scikit-learn 1.9.1, and pytest 9.1.1. Git is installed separately (see [Course 2](../course2_bond_math/README.md#before-you-start)).

| Data | Kind | Used in |
|:---|:---|:---|
| The course's book of 200 bonds, with the rating scale | Synthetic: invented issuers and CUSIPs | Days 1 to 3, and the capstone |
| Daily Treasury par yield curve rates, 2015-01-02 to 2026-10-02 | Real, public: U.S. Department of the Treasury, public domain | Days 2, 7, and 8 |
| 2,940 daily investment grade and high yield spreads in bp | Synthetic: invented for Course 3, not ICE, Moody's, or any index | Day 2 |
| The desk's 374 trades in September 2026 | Synthetic: invented trades and counterparties | Day 6 |
| 4,000 invented firms followed over 20 study years | Synthetic: ids only, no calendar years, and no agency statistic | Days 3, 4, 5, 8, and 9, and the capstone |

Sources and terms for every file are in [the data page](../data/README.md).

## What comes next

[Course 6 is Neural Networks](../course6_neural_networks/README.md): three weeks from one neuron worked out by hand to dense, recurrent, and convolutional networks, ending with sequence models on the Treasury curve.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
