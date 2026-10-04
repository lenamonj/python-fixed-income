<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="520">
</picture>

![Course 2](https://img.shields.io/badge/Course_2-Bond_Math-123D2F?style=for-the-badge)
![Length](https://img.shields.io/badge/3_weeks-14_notebooks_%2B_capstone-1C7A57?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[The three weeks](#the-three-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 2: Bond Math

**Three weeks from discounting one cash flow to a risk report on a whole book, with every number checked against Excel.**

</div>

On day one you grow 100 dollars at a semiannual rate and match Excel's `FV` to the last digit. Three weeks later you price any bullet bond on any settlement date, solve its yield, and measure its accrued interest, duration, DV01, convexity, spread to the curve, spread duration, and DTS. Then a month-end extract arrives with problems in it, and you clean it, reconcile it to its cover note to the cent, and turn it into a risk report with rate and spread scenarios.

**That is the course: the bond math a desk relies on, written by you, tested by you, and kept by you.**

Every function goes into your own module, `bondmath.py`, beside a test file that grows every day. Later courses import it.

Four habits run through all of it.

| Habit | What it means |
|:---|:---|
| **Excel is the answer key** | Every function is checked against a value Excel produced, and the Excel formula is written out beside the Python. When Excel and a textbook differ, the course follows Excel and says so. |
| **Your own tested module** | One or two functions a day, each with a docstring that states its units and convention, and tests run with `python -m pytest`. |
| **Git as the undo button** | One Git step a day: commit, read a change by its diff, restore a file, revert a commit, tag a week. |
| **A harder AI check** | Each day ends with code in the style of an AI assistant's answer. It runs, returns a plausible number, and breaks a convention: a day count, a compounding frequency, a percent read as a decimal. You catch it with a test built from Excel's values. |

You need Course 1, or the same ground: Python, pandas, functions with docstrings, `assert`, and a `.py` module you import. Course 1 teaches no Git and no pytest; this course starts both from zero. This is the second course in [Python for Fixed Income](../README.md).

Status: <!-- count:ready -->14<!-- /count --> of <!-- count:total -->14<!-- /count --> notebooks are ready, and so is the capstone.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here). Course 2 runs in the same `.venv` as Course 1 and adds four things.

| Step | What to do |
|:---|:---|
| **Install the course's packages** | With the course's `.venv` active, run the install line below. Every pin matches Course 1's, so after Course 1 it installs nothing new; on a new machine it installs everything this course needs, pytest included. |
| **Install Git for Windows** | From [git-scm.com/downloads](https://git-scm.com/downloads) with the default choices, or `winget install --id Git.Git` where your firm allows it. Check your firm's policy first. Colab has Git already. Day 1 walks through it. |
| **Make your own folder** | Day 1 has you create `my_bondmath` in your `projects` folder, beside the course repo, with the lines below. Your `bondmath.py`, your tests, and your Git history live there. |
| **Or use Colab** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge. At the end of each day, download your two files from the Colab file browser. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course2_bond_math\requirements.txt
git --version
New-Item -ItemType Directory -Force "$HOME\projects\my_bondmath" | Out-Null
```

Each notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Each day's "Bring It Home" section shows the PowerShell steps that move the day's functions and tests into `my_bondmath`, run the tests, and commit.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. In this course every notebook also ends in the same order: Excel side by side, save the day with Git, bring it home, then the exercises, with the AI check last.

## The three weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | Price and yield on a coupon date | Grow and discount money, price a bond from its cash flows, chart price against yield, and solve a yield from a price, each function tested against Excel |
| 2 | Dates, accrued interest, and risk | Build coupon schedules, count days as Excel does, price between coupon dates clean and dirty, and measure duration, DV01, and convexity across the September book |
| 3 | Curve, spread, and the book | Interpolate a curve, measure each bond's spread to it, compute spread duration and DTS, roll the book up by sector and rating with scenarios, and deliver a risk report |

## Course map

<!-- map:start -->

### Week 1: Price and yield on a coupon date

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Time Value of Money](week1/day1/01_time_value_of_money.ipynb) | Future and present value with semiannual compounding, your first functions in `bondmath.py`, your first test, and your first Git commit | Ready |
| 2 | [Cash Flows and Price from Yield](week1/day2/02_cash_flows_and_price_from_yield.ipynb) | A bullet bond's cash flows, and its price as their discounted sum on a coupon date, beside `NPV`, `PV`, and `PRICE` | Ready |
| 3 | [The Price-Yield Relationship](week1/day3/03_the_price_yield_relationship.ipynb) | Par, premium, and discount, the price-yield curve, which bond moves more, pull to par, and restating a yield with `EFFECT` and `NOMINAL` | Ready |
| 4 | [Yield from Price](week1/day4/04_yield_from_price.ipynb) | Goal Seek, bisection by hand and in a loop, a check that stops on bad input, and undoing a bad edit with Git | Ready |
| 5 | [Case Study: A New Issue Calendar](week1/day5/05_case_study_a_new_issue_calendar.ipynb) | Eight new issues described with the week's functions, and a workbook of live `PRICE` and `YIELD` formulas to open in Excel | Ready |

### Week 2: Dates, accrued interest, and risk

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Dates and Coupon Schedules](week2/day1/06_dates_and_coupon_schedules.ipynb) | Dates in Python and in Excel, adding months, coupon dates counted back from maturity, and the month-end rule | Ready |
| 2 | [Day Counts and Accrued Interest](week2/day2/07_day_counts_and_accrued_interest.ipynb) | The US 30/360 rules one at a time, actual/actual, `COUPDAYBS` and its family, and the holdings' accrued interest reproduced | Ready |
| 3 | [Clean and Dirty Price](week2/day3/08_clean_and_dirty_price.ipynb) | The quote and the invoice, pricing between coupon dates, the final coupon period, yield to maturity, and invoices for a month of trades | Ready |
| 4 | [Duration and DV01](week2/day4/09_duration_and_dv01.ipynb) | Macaulay and modified duration, DV01 per 100 and per position, the bump check, and the holdings' duration reproduced | Ready |
| 5 | [Case Study: Convexity and the September Book](week2/day5/10_case_study_convexity_and_the_september_book.ipynb) | Convexity and where duration's straight line misses, then every bond in the September book repriced, with its book DV01 and duration | Ready |

### Week 3: Curve, spread, and the book

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Treasury Curve Interpolation](week3/day1/11_treasury_curve_interpolation.ipynb) | A curve as tenors and yields, straight-line interpolation by hand, in a function, and with `numpy.interp`, on the real Treasury curve and an invented one | Ready |
| 2 | [Spread over the Curve](week3/day2/12_spread_over_the_curve.ipynb) | Years to maturity on 30/360, the curve yield at each maturity, spread to the curve, and the holdings' spread column reproduced exactly | Ready |
| 3 | [Spread Duration and DTS](week3/day3/13_spread_duration_and_dts.ipynb) | Spread duration by bumping the spread, DTS, and each bond's and each rating bucket's share of the book's DTS | Ready |
| 4 | [Portfolio Aggregation and Scenarios](week3/day4/14_portfolio_aggregation_and_scenarios.ipynb) | Market-value weights, book duration, spread, DTS, and DV01 by sector and rating, and rate and spread scenarios repriced in full | Ready |
| 5 | [Course 2 Capstone](week3/day5/course2_capstone.ipynb) | A November extract tested, cleaned, recomputed, reconciled to its cover note, and turned into a risk report. A [worked version](week3/day5/course2_capstone_solutions.ipynb) sits beside it | Ready |

<!-- map:end -->

## The capstone

Day 5 of week 3 is yours, and it is more than one sitting: plan on two or three. The desk's book as of 30 November 2026 arrives as a raw extract with a cover note, and 39 questions take you from your complete module to a written description of the book's risk. Nothing tells you what is wrong with the extract. You test it against the cover note, fix what is an error, recompute every bond with your own `bondmath`, and explain every difference between your numbers and the file's.

You hand in eight things: your module with its tests passing, a cleaning function with checks that stop the run, a reconciliation to the cover note's control totals to the cent, a risk report written to an Excel workbook with three sheets, the same report run again on the September book, a Git history with one commit per deliverable, a short log of any AI assistant use, and a written description.

| File | What it is |
|:---|:---|
| [`course2_capstone.ipynb`](week3/day5/course2_capstone.ipynb) | The brief, the questions, and a check cell for every answer that can be checked. A check says correct or not yet, and never shows the answer |
| [`course2_capstone_overview.pdf`](week3/day5/course2_capstone_overview.pdf) | The brief as slides: the scenario, the files, the deliverables, and how the checks work |
| [`course2_capstone_solutions.ipynb`](week3/day5/course2_capstone_solutions.ipynb) | The worked version, with every decision stated. Open it after you finish |

The description you write covers the book's risk by sector and rating, under each scenario, and the data problems you found. It never recommends, ranks, or forecasts a bond, an issuer, or a sector, and every scenario is a mechanical what-if, not a forecast.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| pandas | Reading Excel's reference values, and the holdings as a table | Week 1, Day 1 |
| pytest | Testing every function in your module against Excel's values | Week 1, Day 1 |
| Git | Saving each day's work, reading a change by its diff, and undoing it | Week 1, Day 1 |
| NumPy and matplotlib | Grids of yields, and charts of price against yield and of the curve | Week 1, Day 3 |
| openpyxl | Writing workbooks for Excel: live formulas, a scenario grid, the risk report | Week 1, Day 5 |

Exact versions are pinned in [`requirements.txt`](requirements.txt). Git is installed separately (see [Before you start](#before-you-start)).

| Data | Kind | Used in |
|:---|:---|:---|
| Excel reference values: every Excel number the tests compare with | Computed by desktop Excel from invented bonds | Every day |
| The desk's portfolio: holdings, benchmark, issuers, ratings, and trades | Invented for this series | Week 2, Week 3, and the capstone |
| The invented Treasury curve the holdings were built on | Invented for this course | Week 3 and the capstone |
| The capstone extract, its cover note, and its answer key | Invented for this course | The capstone |
| U.S. Treasury daily par yield curve rates | Real, public | Week 3, Day 1 |

Sources and terms for every file are in [The data](../README.md#the-data) on the front page.

## What comes next

[Course 3 is Market Data and Time Series](../course3_market_data/README.md): three weeks on pulling market data with a key that never leaks, market calendars, changes, volatility, z-scores, slopes, butterflies, SQL, and a daily market snapshot, with your `bondmath` imported where bond math is needed.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
