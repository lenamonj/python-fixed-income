<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/wordmark-dark.png">
  <img src="assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="520">
</picture>

![Course 1](https://img.shields.io/badge/Course_1-Python_Foundations-123D2F?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](LICENSE-CONTENT)

**[Start here](#start-here)** &nbsp;·&nbsp; **[Coming from Excel](#if-you-know-excel-you-already-know-how-to-think-about-this)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[How a day works](#how-a-day-works)** &nbsp;·&nbsp; **[The data](#the-data)** &nbsp;·&nbsp; **[License](#license)**

## A free course that teaches Python from zero to people who work in fixed income. Every example is a bond.

</div>

You know what a coupon, a spread, and a duration are. You live in Excel. You have never written a line of code. This course starts there.

Most Python courses teach with shopping carts and movie ratings. This one teaches with a credit desk. You store a bond before you store anything else, your first loop totals a portfolio, and your first table is a holdings file. By the time a new idea arrives, you already know why a desk would want it.

Course 1 is Python Foundations: four weeks, one notebook a day. <!-- count:ready -->11<!-- /count --> of its <!-- count:total -->18<!-- /count --> notebooks are ready, and the rest are being built in order.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## If you know Excel, you already know how to think about this

Nothing in this course asks you to forget Excel. Every new idea is introduced next to the Excel feature you would reach for today, with the formula written out, so you are translating something you know and not learning from nothing.

| In Excel you would | In Python you will | Where |
|:---|:---|:---|
| Fill a formula down a column | Write the formula once, in a loop or on a whole array | Week 1, Day 1 and Week 2, Day 1 |
| Write a nested `IF` | Write `if`, `elif`, `else`, one test per line | Week 1, Day 1 |
| See `#N/A`, `#DIV/0!`, or `#NAME?` in a cell | Read an error that names the line and the cause | Week 1, Day 3 |
| Turn on AutoFilter and sort a sheet | Filter and sort a table by condition | Week 2, Day 2 |
| Use `SUMIF` and `COUNTIF` | Filter, then sum or count | Week 2, Day 2 and Day 5 |
| Use `COUNTBLANK` and Remove Duplicates | Count missing values and repeated rows in one line each | Week 2, Day 4 |
| Use `VLOOKUP` or `INDEX` and `MATCH` | Merge two tables on a shared column | Week 2, Day 3 and Day 5 |
| Build a pivot table | Group by a column and summarize | Week 2, Day 3 and Day 5 |
| Use `SUMPRODUCT` over `SUM` for a weighted average | Do the same arithmetic on two columns | Week 2, Day 3 and Day 5 |

What changes is what you get to keep. A spreadsheet holds the answer. Code holds the steps that produced it, so tomorrow's file runs through the same steps without anyone dragging a formula or repointing a range.

## Start here

There are two ways to run the notebooks. Pick one.

### Run in Google Colab, with nothing to install

Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge at the top. Colab runs in your browser and needs only a Google account.

Use Colab on a personal account, with the course data only. Do not upload anything from your employer.

### Run on your own Windows machine

You need [Python 3.13](https://www.python.org/downloads/), [VS Code](https://code.visualstudio.com/) with the Python and Jupyter extensions, and [git](https://git-scm.com/downloads). On a work machine, check your firm's policy before installing anything.

**Step 1.** Get the course and open its folder.

```powershell
cd $HOME\projects
git clone https://github.com/lenamonj/python-fixed-income.git
cd python-fixed-income
```

**Step 2.** Create an environment for the course and install what it needs.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**Step 3.** Open the folder in VS Code.

```powershell
code .
```

Open `week1\day1\01_python_for_fixed_income_intro.ipynb`, choose the `.venv` kernel in the top right, and run the first cell.

If PowerShell says running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and repeat Step 2.

## How a day works

Each day has its own folder, and each folder holds three files with the same name.

| File | What it is |
|:---|:---|
| `NN_name.ipynb` | The notebook. Work through it top to bottom. |
| `NN_name_overview.pdf` | A short slide overview of the day's ideas. Read it first. |
| `NN_name_solutions.ipynb` | Worked answers to the exercises. Try each one yourself before you look. |

Every notebook teaches the same way.

| Step | What happens |
|:---|:---|
| **A question** | A question the desk would ask, marked `Q.` |
| **A few lines of code** | A small cell that answers it, with a comment on each step. |
| **The takeaway** | One line on what the output shows. |

Four habits run through every day.

| Habit | What it means |
|:---|:---|
| **Excel side by side** | Wherever Excel has a function or feature for the job, it is shown next to the Python, formula included. |
| **Errors on purpose** | Code that fails is run for real, and the error is read line by line. |
| **Exercises you can check** | Each exercise has a check cell that tells you whether your answer is right. |
| **The AI check** | Each day ends with code written in the style of an AI assistant. It has one bug. You find it by checking the output against a number you worked out yourself. |

That last habit is the point of the course. You will use AI assistants to write code. Code that runs is not the same as code that is right, and the way to tell the difference is to know what the answer should be.

## Course map

<!-- map:start -->

### Week 1: Python foundations

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Introduction to Python](week1/day1/01_python_for_fixed_income_intro.ipynb) | Variables, lists, dictionaries, conditions, loops, and functions, on four bonds | Ready |
| 2 | [Files and Folders](week1/day2/02_files_and_folders.ipynb) | Finding, creating, writing, and reading the desk's holdings file | Ready |
| 3 | [Debugging](week1/day3/03_debugging.ipynb) | Reading an error, the common error types, and bugs that raise no error | Ready |
| 4 | [Classes: A Bond Object](week1/day4/04_classes_a_bond_object.ipynb) | A bond that carries its own data and calculations | Ready |
| 5 | [Case Study: Organizing a Small Portfolio](week1/day5/05_case_study_a_small_portfolio.ipynb) | One job from start to finish: an email of holdings becomes a table | Ready |

### Week 2: NumPy and pandas

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [NumPy](week2/day1/06_numpy.ipynb) | Arrays, arithmetic on a whole portfolio at once, and pricing a bond from its cash flows | Ready |
| 2 | [pandas: Series and DataFrames](week2/day2/07_pandas_series_and_dataframes.ipynb) | Tables with names, selecting, filtering, and sorting 200 holdings | Ready |
| 3 | [pandas: Combining and Loading](week2/day3/08_pandas_combining_and_loading.ipynb) | Joining tables, reading and saving files, summaries, and dates | Ready |
| 4 | [Case Study: A First Look at the Data](week2/day4/09_case_study_first_look_at_the_data.ipynb) | Three linked tables: positions, issuers, and ratings, checked before any join | Ready |
| 5 | [Case Study: Joining the Tables](week2/day5/10_case_study_joining_the_tables.ipynb) | Joining the three tables, checking each join, and answering the desk's questions from the result | Ready |

### Week 3: Visualization and exploratory data analysis

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Visualization](week3/day1/11_visualization.ipynb) | Histograms, box plots, bar charts, line plots, scatter plots, pair plots, and heatmaps, on the 200 holdings | Ready |
| 2 | More Visualization | Regression plots, joint plots, interactive charts, and customizing a chart | Planned |
| 3 | Exploratory Data Analysis | Sanity checks, distributions, relationships, missing values, and outliers | Planned |
| 4 | Case Study: Treasury Yields | Yields by tenor and year, and how they changed over time | Planned |
| 5 | Case Study: A Trade Blotter | A short guided analysis of a small set of trades | Planned |

### Week 4: Consumer credit, text, and the project

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | Case Study: Consumer Credit | A full analysis of a public credit card default dataset | Planned |
| 2 | Analyzing Text | Cleaning text and turning it into numbers | Planned |
| 3 | Case Study: Complaint Sentiment | Measuring sentiment in consumer credit complaints | Planned |
| 4 and 5 | Course Project | A holdings file and a set of questions, answered on your own | Planned |

<!-- map:end -->

Python Foundations is the first course in a planned series. Bond Math comes next: pricing, yield, duration, and convexity, built by hand and checked against Excel.

## The data

Every issuer, ticker, CUSIP, price, and position in this course is invented. No real company and no real security appears in any holdings file.

| File | What it holds |
|:---|:---|
| `data/holdings.csv` | 200 bonds: price, accrued interest, yield, spread, duration, DTS, par held, and market value |
| `data/benchmark.csv` | 821 bonds from 150 issuers, with index weights |
| `data/issuers.csv` | One row per issuer: ticker, name, sector, and rating |
| `data/ratings.csv` | The rating scale, with a score, a bucket, and investment grade or high yield |
| `data/positions.csv` | A lean version of the holdings, for joining to the other tables |
| `data/holdings_messy.csv` | The holdings with problems planted on purpose, for the data cleaning lessons |
| `data/holdings_messy_answer_key.md` | Every planted problem, listed |

The data is built to behave like a real portfolio.

| Rule | What it means |
|:---|:---|
| **Price and yield always agree** | Each yield is a synthetic Treasury yield plus a spread, and each price is calculated from that yield. |
| **One convention throughout** | Fixed-rate bullet bonds, semiannual coupons, 30/360 day count, modified duration. |
| **Identical for every student** | One seeded script, `tools/make_holdings.py`, generates every file. |
| **Checked** | `python -m pytest` confirms the identifiers are valid and that each bond's price, accrued interest, and duration match its yield. |
| **No real CUSIPs** | Every CUSIP uses an issuer number in the range reserved for internal use, with a valid check digit. |

## What is in this repo

```
python-fixed-income/
  week1/ ... week4/
    day1/ ... day5/     the notebook, its solutions, and its overview PDF
  data/                 the invented portfolio
  tools/                the scripts that build the data and the notebook banner
  tests/                checks on the data
  assets/               fonts and images
  requirements.txt      what the notebooks need
```

## License

Code is released under the [MIT License](LICENSE). The notebooks' written content, the slide overviews, and the videos are released under [CC BY 4.0](LICENSE-CONTENT): you may share and adapt them, including commercially, as long as you give credit.

The fonts in `assets/fonts` are under the SIL Open Font License, and their license files sit beside them.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
