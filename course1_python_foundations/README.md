<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="520">
</picture>

![Course 1](https://img.shields.io/badge/Course_1-Python_Foundations-123D2F?style=for-the-badge)
![Length](https://img.shields.io/badge/4_weeks-18_notebooks_%2B_project-1C7A57?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[The four weeks](#the-four-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The project](#the-project)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 1: Python Foundations

**Four weeks from your first line of code to a month-end portfolio review you run yourself.**

</div>

On day one you store a bond: its ticker, its coupon, its maturity. Four weeks later a month-end holdings extract arrives that does not tie to its cover note. You find what is wrong with it, fix it, state every decision, and write up what the book holds and how it differs from its benchmark. Nobody walks you through it.

**That is the course: from storing one bond to reviewing a whole book on your own.**

Every skill is taught on the job it does on a desk. Loops total a portfolio. Joins attach issuers and ratings to positions, with a check on the row count and the face amount around each one. Charts show where the spread and the duration sit. Your first time series is Treasury yields since 2015. Your first text analysis is on FOMC statements.

Two habits run through all of it.

| Habit | What it means |
|:---|:---|
| **The Excel bridge** | Every new idea sits beside the formula you would write today, so you are translating something you know. |
| **Check before you trust** | You work out what the answer should be before you rely on code, yours or an AI assistant's. Each day ends with code that runs cleanly and is wrong, and you find the bug. |

You need no coding experience. You do need to know what a coupon, a spread, and a duration are. This is the first course in [Python for Fixed Income](../README.md).

Status: <!-- count:ready -->18<!-- /count --> of <!-- count:total -->18<!-- /count --> notebooks are ready, and so is the course project.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here). Pick one of two ways to run the notebooks.

| Way | What to do |
|:---|:---|
| **Google Colab, nothing to install** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge at the top. |
| **Your own Windows machine** | Follow the three steps on the front page. The install line for this course is below. |

```powershell
python -m pip install -r course1_python_foundations\requirements.txt
```

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern.

## The four weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | Python foundations | Write variables, loops, functions, and a class, read an error, and turn an email of holdings into a table |
| 2 | NumPy and pandas | Hold a portfolio in a table, filter and group it, and join it to issuer and rating tables with checks around each join |
| 3 | Visualization and exploratory data analysis | Draw finished charts, test a new file before trusting it, and work with a time series |
| 4 | Consumer credit, text, and the project | Analyze a yes or no outcome, turn text into numbers, and report on a month-end extract on your own |

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
| 2 | [More Visualization](week3/day2/12_visualization_more.ipynb) | Regression plots, joint plots, violin, strip and swarm plots, interactive and 3D charts with plotly, and customizing a chart | Ready |
| 3 | [Exploratory Data Analysis](week3/day3/13_exploratory_data_analysis.ipynb) | Sanity checks, missing values, distributions, outliers, and relationships, on a holdings file with problems planted in it | Ready |
| 4 | [Case Study: Treasury Yields](week3/day4/14_case_study_treasury_yields.ipynb) | A first time series: Treasury par yields by tenor and year, a spread between two tenors, and daily changes | Ready |
| 5 | [Case Study: A Trade Blotter](week3/day5/15_case_study_trade_blotter.ipynb) | The week's capstone: a month of trades checked, summarized, joined to the holdings, and reported | Ready |

### Week 4: Consumer credit, text, and the project

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Case Study: Consumer Credit](week4/day1/16_case_study_consumer_credit.ipynb) | A full analysis of a public credit card default dataset: 30,000 accounts, a yes or no outcome, and rates with their counts | Ready |
| 2 | [Analyzing Text](week4/day2/17_analyzing_text.ipynb) | Regular expressions, cleaning, stopwords, stemming, and turning text into numbers, on FOMC statements | Ready |
| 3 | [Case Study: Statement Sentiment](week4/day3/18_case_study_statement_sentiment.ipynb) | Turning the wording of FOMC statements into a score with three word lists, and how far to trust it | Ready |
| 4 and 5 | [Course Project](week4/day4/course1_project.ipynb) | A new month-end extract and 40 numbered questions, answered on your own, ending in a written picture of the book. A [worked version](week4/day4/course1_project_solutions.ipynb) sits beside it | Ready |

<!-- map:end -->

## The project

Days 4 and 5 of week 4 are yours. A new month-end extract arrives with a cover note, and 40 numbered questions take you from the structure of the file to a written picture of the book.

| File | What it is |
|:---|:---|
| [`course1_project.ipynb`](week4/day4/course1_project.ipynb) | The brief, the questions, and a check cell for every answer that can be checked |
| [`course1_project_overview.pdf`](week4/day4/course1_project_overview.pdf) | The brief as slides: the scenario, the files, the rules, and how the checks work |
| [`course1_project_solutions.ipynb`](week4/day4/course1_project_solutions.ipynb) | The worked version, with every decision stated. Open it after you finish |

The conclusion you write describes the data. It never recommends, ranks, or forecasts a bond, an issuer, or a sector.

## What it uses

| Library | Used for | First appears |
|:---|:---|:---|
| NumPy | Arithmetic on whole columns at once | Week 2, Day 1 |
| pandas | Tables: loading, filtering, grouping, joining | Week 2, Day 2 |
| matplotlib and seaborn | Charts | Week 3, Day 1 |
| plotly | Interactive and 3D charts | Week 3, Day 2 |
| nltk | Stopwords, stemming, and a published sentiment word list | Week 4, Day 2 |

Exact versions are pinned in [`requirements.txt`](requirements.txt).

| Data | Kind | Used in |
|:---|:---|:---|
| The desk's portfolio: holdings, benchmark, issuers, ratings, trades, and the project extract | Invented for this course | Weeks 1 to 3 and the project |
| U.S. Treasury daily par yield curve rates | Real, public | Week 3, Day 4 and Week 4, Day 3 |
| UCI Default of Credit Card Clients | Real, public, CC BY 4.0 | Week 4, Day 1 |
| FOMC post-meeting statements | Real, public | Week 4, Days 2 and 3 |

Sources and terms for every file are in [The data](../README.md#the-data) on the front page.

## What comes next

Course 2 is Bond Math: pricing, yield, duration, and convexity, built by hand and checked against Excel.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
