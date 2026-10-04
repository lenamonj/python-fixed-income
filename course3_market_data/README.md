<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="520">
</picture>

![Course 3](https://img.shields.io/badge/Course_3-Market_Data_and_Time_Series-123D2F?style=for-the-badge)
![Length](https://img.shields.io/badge/3_weeks-14_notebooks_%2B_capstone-1C7A57?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[Your FRED key](#your-fred-key)** &nbsp;·&nbsp; **[The three weeks](#the-three-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 3: Market Data and Time Series

**Three weeks from your first API key to a daily market snapshot that runs again on any date, with every measure defined, tested, and checked against Excel.**

</div>

On day one you get a free key for the FRED API and learn to keep it out of every file, notebook, and commit. Three weeks later you pull a public series, clean it against the bond market's own calendar, turn it into changes in bp, rolling volatility, z-scores, percentile ranks, slopes, and butterflies with no lookahead, query the desk's holdings and trades with SQL and prove each answer against pandas, review code written in the style of an AI assistant, and write a one-page snapshot to HTML and Excel. Then a vendor extract arrives with problems in it, and you clean it, reconcile it, and run the snapshot on two dates.

**That is the course: market data in, a stated definition behind every number, and a report that describes the data and never forecasts it.**

Every function goes into a second module of your own, `marketdata.py`, beside the `bondmath.py` you built in Course 2, with a test file that grows every day.

Four habits run through all of it.

| Habit | What it means |
|:---|:---|
| **The key never leaks** | Your key lives in `.env` in your own folder or in Colab's Secrets panel. Every notebook runs without it, and the saved notebooks are the keyless run. |
| **Excel as the answer key** | Rolling statistics, z-scores, and percentile ranks are checked against values computed by desktop Excel, and the Excel formula is written out beside the Python. |
| **No lookahead** | Every function that works over a window has a test that its answer on a date is the same whether the data stops there or runs on. |
| **Describe, never forecast** | Every sentence about the data says what it was, where it sits in its own history, or how it changed. Nothing says where rates or spreads are going. |

You need Courses 1 and 2, or the same ground: pandas and matplotlib, functions with docstrings and tests, pytest, local Git, and a `bondmath.py` of your own in `my_bondmath`. A notebook that needs `bondmath` writes a reference copy into its work folder, so a missing or unfinished module never stops it. This is the third course in [Python for Fixed Income](../README.md).

Status: <!-- count:ready -->14<!-- /count --> of <!-- count:total -->14<!-- /count --> notebooks are ready, and so is the capstone.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

*This product uses the FRED&reg; API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.*

## Before you start

Setup is on the [series front page](../README.md#start-here). Course 3 runs in the same `.venv` as Courses 1 and 2 and adds three things.

| Step | What to do |
|:---|:---|
| **Install the course's packages** | With the course's `.venv` active, run the install line below. It adds `requests` and `python-dotenv` to Course 2's pins. |
| **Keep your folder** | Your `my_bondmath` folder from Course 2, in your `projects` folder beside the course repo, gains `marketdata.py`, its tests, `.env`, and later `snapshot.py`. If you skipped Course 2, create it with the last line below. |
| **Get a FRED key** | Free, and one per person. See [Your FRED key](#your-fred-key). You can start without it: every notebook runs, and runs to its saved output, with no key. |
| **Or use Colab** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge. Keep your key in Colab's Secrets panel, never in a cell. At the end of each day, download your files from the Colab file browser. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course3_market_data\requirements.txt
New-Item -ItemType Directory -Force "$HOME\projects\my_bondmath" | Out-Null
```

Each notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Each day's "Bring It Home" section shows the PowerShell steps that move the day's functions and tests into `my_bondmath`, copy in any data file the tests read, run the tests, and commit.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. As in Course 2, every notebook ends in the same order: Excel side by side, save the day with Git, bring it home, then the exercises, with the AI check last.

## Your FRED key

| Step | What to do |
|:---|:---|
| **Register** | Sign in or create a free account at [fredaccount.stlouisfed.org/apikeys](https://fredaccount.stlouisfed.org/apikeys) and request a key: 32 lowercase letters and digits. FRED's rule is one key per person, so a colleague registers for their own. |
| **Put it in one place** | On your machine: `.env` in `$HOME\projects\my_bondmath`, one line, `FRED_API_KEY=` followed by the key. In Colab: the Secrets panel (the key icon in the left bar), named `FRED_API_KEY`, with notebook access turned on. Day 1 walks through both. |
| **Never in the repo** | The key never goes in the course repo, a notebook cell, a saved output, a screenshot, a chat window, or a commit. Day 1 sets up `.gitignore` before `.env` exists, and teaches what to do if a key leaks: rotate it. |
| **No key at all** | Every notebook still runs. Cells that call FRED, and only those, print `Live cell skipped: no FRED key was found. Every other cell runs without one.` Every analysis uses data in the repo. |
| **Licensed series** | ICE BofA and Moody's series on FRED are pulled live with your key and held in memory only: never cached, never written to a file, and never stored in this repo. Their values show only on your own screen, if you choose to show them. Their providers' terms forbid redistribution. |

## The three weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | Getting the data in | Keep a key secret, read FRED's JSON, find the days the bond market had no curve, pick the observation that stands for a week or a month, cache a pull, and build the course's daily dataset with every check |
| 2 | Time series measures | Compute changes in bp and returns in percent, rolling volatility, z-scores, percentile ranks, slopes, and butterflies with stated windows and no lookahead, and describe three years of the curve and spreads as of one date |
| 3 | SQL, AI, and the snapshot | Query the desk's tables with SQL and prove each answer against pandas, review AI-written data code with tests, and write a daily market snapshot to HTML and Excel that runs again on any date |

## Course map

<!-- map:start -->

### Week 1: Getting the data in

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [APIs, Keys, and Secrets](week1/day1/01_apis_keys_and_secrets.ipynb) | What an API request is, a FRED key and why it is a password, environment variables, `.env` and `.gitignore`, `get_secret`, Colab's Secrets panel, and a leak drill that ends in rotation | Ready |
| 2 | [JSON and the FRED API](week1/day2/02_json_and_the_fred_api.ipynb) | JSON, FRED's response and its `.` for a missing value, `fred_series` with errors that never show the key, and Power Query on the same file | Ready |
| 3 | [Market Calendars and Cleaning](week1/day3/03_market_calendars_and_cleaning.ipynb) | The Treasury file as its own market calendar, why a holiday calendar is not it, inner and outer joins, forward fill for display only, and stale values, beside `WORKDAY` and `NETWORKDAYS` | Ready |
| 4 | [Resampling and the As-Of Value](week1/day4/04_resampling_and_the_as_of_value.ipynb) | Month-end and week-end levels labelled by their real date, the week of Good Friday, and the as-of value, beside `EOMONTH`, `MAXIFS`, and `XLOOKUP` | Ready |
| 5 | [Case Study: The Market Dataset](week1/day5/05_case_study_the_market_dataset.ipynb) | A cache that never stores a licensed series, then the course's daily dataset built from the Treasury file and synthetic spreads with every check of the week | Ready |

### Week 2: Time series measures

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Changes in bp and Percent](week2/day1/06_changes_in_bp_and_percent.ipynb) | Changes in bp over rows and over calendar periods, why a percent change of a yield misleads, a price return from `bondmath`, and rounding before you rank | Ready |
| 2 | [Rolling Windows and Volatility](week2/day2/07_rolling_windows_and_volatility.ipynb) | Windows in rows, trailing and full, volatility with `STDEV.S`, annualising as a labelled choice, and the no-lookahead test | Ready |
| 3 | [Z-Scores and Percentile Ranks](week2/day3/08_z_scores_and_percentile_ranks.ipynb) | Where today sits in its own history with `STANDARDIZE` and `COUNTIF`, why `PERCENTRANK.INC` is a different measure, and words that describe against words that forecast | Ready |
| 4 | [Slopes and Butterflies](week2/day4/09_slopes_and_butterflies.ipynb) | 2s10s, 5s30s, 3m10y, and two butterflies with their signs, and DV01-neutral fly weights from your own `bondmath` | Ready |
| 5 | [Case Study: Three Years of Curve and Spreads](week2/day5/10_case_study_three_years_of_curve_and_spreads.ipynb) | `summary_table`, every measure as of one date and nothing after it, then three years of the curve and the synthetic spreads described | Ready |

### Week 3: SQL, AI, and the snapshot

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [SQL with sqlite3](week3/day1/11_sql_with_sqlite3.ipynb) | A database in one file, `SELECT` to `HAVING` beside pandas, parameters instead of pasted values, and a weighted OAS checked against `bondmath` | Ready |
| 2 | [SQL Joins and Time Series](week3/day2/12_sql_joins_and_time_series.ipynb) | Joins, the join that duplicates rows, dates as text, and window functions for daily changes and month ends | Ready |
| 3 | [Working with an AI Assistant](week3/day3/13_working_with_an_ai_assistant.ipynb) | The prompt as a spec, AI-style code reviewed with tests, a chart checked against its numbers, what never to paste, a package that does not exist, and JSON replies | Ready |
| 4 | [The Daily Market Snapshot](week3/day4/14_the_daily_market_snapshot.ipynb) | One function for any date, a book section with DV01 and a what-if, an HTML page and an Excel workbook, and `snapshot.py` run from the command line | Ready |
| 5 | [Course 3 Capstone](week3/day5/course3_capstone.ipynb) | A vendor extract tested, cleaned, reconciled, appended to history, and turned into the snapshot on two dates. A [worked version](week3/day5/course3_capstone_solutions.ipynb) sits beside it | Ready |

<!-- map:end -->

## The capstone

Day 5 of week 3 is yours, and it is more than one sitting: plan on two or three. The desk's market data vendor sends a daily extract for 1 July to 2 October 2026, with a cover note. The history before it is already clean. About 40 questions take you from your complete module to a written description of two dates. Nothing tells you what is wrong with the extract. You test it against the market calendar and the cover note, clean it with checks that stop, prove the result by reconciliation, and run the snapshot again on a second date.

You hand in your module with its tests passing, a cleaning function that logs every change, a reconciliation with nothing left unexplained, the snapshot for 2 October 2026 written to HTML and Excel, the same snapshot run again for 30 September from the command line, both snapshots' levels saved to a SQL table and queried back, a Git history with one commit per deliverable, a short log of any AI assistant use, and a written description. A live section with your key is optional and is not checked.

| File | What it is |
|:---|:---|
| [`course3_capstone.ipynb`](week3/day5/course3_capstone.ipynb) | The brief, the questions, and a check cell for every answer that can be checked. A check says correct or not yet, and never shows the answer |
| [`course3_capstone_overview.pdf`](week3/day5/course3_capstone_overview.pdf) | The brief as slides: the scenario, the files, the deliverables, and how the checks work |
| [`course3_capstone_solutions.ipynb`](week3/day5/course3_capstone_solutions.ipynb) | The worked version, with every decision stated. Open it after you finish |

The description you write covers levels, changes, where each series sits in its one-year history, the book's DV01 and its mechanical what-if, and the data problems you found. It never recommends, ranks, or forecasts a security, a sector, or a market. The snapshot holds only public and synthetic data, so you can share it.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| python-dotenv | Reading your key from `.env` without putting it in code | Week 1, Day 1 |
| requests | Asking the FRED API for a series, with errors that never show the key | Week 1, Day 1 |
| pytest and Git | Testing `marketdata.py` every day, and keeping secrets out of history | Week 1, Day 1 |
| pandas | Dated series: calendars, resampling, rolling windows, joins | Week 1, Day 1 |
| matplotlib | Charts of the curve, slopes, volatility, and spreads | Week 1, Day 3 |
| sqlite3 | A SQL database in one file, from Python's standard library | Week 3, Day 1 |
| openpyxl | Writing the snapshot workbook for Excel | Week 3, Day 4 |

Exact versions are pinned in [`requirements.txt`](requirements.txt). Git is installed separately (see [Course 2](../course2_bond_math/README.md#before-you-start)).

| Data | Kind | Used in |
|:---|:---|:---|
| U.S. Treasury daily par yield curve rates, 2015 to 2026: the market history and the market calendar | Real, public domain | Every day |
| FRED `DGS` Treasury series, pulled live with your key | Real, public; equal to the Treasury file on every common date | Live cells, optional |
| Treasury values for two series in FRED's JSON response format | Public-domain values in FRED's format, built for this course | Week 1 |
| Excel reference values: rolling statistics, z-scores, and percentile ranks | Computed by desktop Excel from the Treasury file | Week 2 onward |
| Daily investment grade and high yield spreads | Synthetic: invented for this course, not ICE, Moody's, or any index | Week 1 onward |
| The desk's portfolio: holdings, benchmark, issuers, ratings, and trades | Invented for this series | Week 3 and the capstone |
| The capstone extract, its cover note, and its answer key | Invented for this course | The capstone |
| ICE BofA and Moody's series on FRED | Licensed: pulled live with your key, held in memory, never stored | Live cells, optional |

Sources and terms for every file are in [The data](../README.md#the-data) on the front page.

## What comes next

Later courses import the `bondmath` and `marketdata` you built in Courses 2 and 3.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
