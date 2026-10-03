# Course 1: Python Foundations

**Python from zero, for people who work in fixed income. Four weeks, one notebook a day, every example a bond.**

This is the first course in [Python for Fixed Income](../README.md). It assumes you know what a coupon, a spread, and a duration are, and that you have never written a line of code.

<!-- count:ready -->13<!-- /count --> of its <!-- count:total -->18<!-- /count --> notebooks are ready, and the rest are being built in order.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here): run in Google Colab with nothing to install, or on your own Windows machine. On your own machine, install what this course needs from the repo folder:

```powershell
python -m pip install -r course1_python_foundations\requirements.txt
```

Each day's folder holds the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern.

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

## What comes next

Course 2 is Bond Math: pricing, yield, duration, and convexity, built by hand and checked against Excel.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
