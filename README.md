<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/wordmark-dark.png">
  <img src="assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="325">
</picture>

[![Course 1](https://img.shields.io/badge/Course_1-Python_Foundations-123D2F?style=for-the-badge)](course1_python_foundations/README.md)
[![Course 2](https://img.shields.io/badge/Course_2-Bond_Math-123D2F?style=for-the-badge)](course2_bond_math/README.md)
[![Course 3](https://img.shields.io/badge/Course_3-Market_Data_and_Time_Series-123D2F?style=for-the-badge)](course3_market_data/README.md)
[![Course 4](https://img.shields.io/badge/Course_4-Machine_Learning-123D2F?style=for-the-badge)](course4_machine_learning/README.md)
[![Course 5](https://img.shields.io/badge/Course_5-Advanced_Machine_Learning-123D2F?style=for-the-badge)](course5_advanced_ml/README.md)
[![Course 6](https://img.shields.io/badge/Course_6-Neural_Networks-123D2F?style=for-the-badge)](course6_neural_networks/README.md)
[![Course 7](https://img.shields.io/badge/Course_7-NLP%2C_RAG%2C_and_LLMs-123D2F?style=for-the-badge)](course7_nlp_and_llms/README.md)
[![Course 8](https://img.shields.io/badge/Course_8-Implementing_Agentic_AI-123D2F?style=for-the-badge)](course8_agentic_ai/README.md)
[![Course 9](https://img.shields.io/badge/Course_9-Deployment-123D2F?style=for-the-badge)](course9_deployment/README.md)
[![Course 10](https://img.shields.io/badge/Course_10-Implementing_RAG-123D2F?style=for-the-badge)](course10_rag/README.md)
[![Bonus](https://img.shields.io/badge/Bonus-Build_Your_Own_Coding_Agent-123D2F?style=for-the-badge)](course_bonus_coding_agent/README.md)
[![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)](#run-in-google-colab-with-nothing-to-install)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](LICENSE-CONTENT)

**[Start here](#start-here)** &nbsp;·&nbsp; **[Coming from Excel](#if-you-know-excel-you-already-know-how-to-think-about-this)** &nbsp;·&nbsp; **[The courses](#the-courses)** &nbsp;·&nbsp; **[How a day works](#how-a-day-works)** &nbsp;·&nbsp; **[The data](#the-data)** &nbsp;·&nbsp; **[License](#license)**

## From Fixed Income to Python: A Practical Guide for Fixed Income Professionals

</div>

You know what a coupon is. You understand spread, duration, yield, and credit. You live in Excel. You understand the business, but you have never written a line of code.

**That's exactly where this course begins.**

Most Python courses teach programming through shopping carts, movie ratings, and toy datasets. This one teaches Python through the work of a credit desk.

Your first variables describe a bond: its ticker, its coupon, its maturity. Your first loop totals a portfolio. Your first data table is a holdings file. Your first analysis answers a question you already know how to ask.

Nothing is abstracted away into contrived examples. Every programming concept is introduced in the context of fixed income, portfolio management, and credit analysis, so you learn the code and immediately understand why it matters.

You already know the investment problem. **This course teaches you how to solve more of it with code.**

The series starts with [Course 1, Python Foundations](course1_python_foundations/README.md): four weeks, one notebook a day, 19 notebooks and a project. [Course 2, Bond Math](course2_bond_math/README.md) follows: three weeks, 14 notebooks and a capstone, in which you build price, yield, accrued interest, duration, DV01, convexity, spread, and DTS yourself, test every function against Excel, and finish with a risk report on a whole book. [Course 3, Market Data and Time Series](course3_market_data/README.md) comes next: three weeks, 14 notebooks and a capstone, in which you pull market data from an API with a key that never leaks, clean it against the bond market's own calendar, compute changes, volatility, z-scores, percentile ranks, slopes, and butterflies with no lookahead, query the book with SQL, and finish with a daily market snapshot that runs again on any date. [Course 4, Machine Learning](course4_machine_learning/README.md) follows: three weeks, 14 notebooks and a capstone, in which you fit and read regressions and classifiers on credit data, choose a threshold on rows the test set never saw, prune a decision tree, validate on dated data with no lookahead, cluster bonds and issuers, describe the Treasury curve with PCA, and finish with a three-model comparison on a public file of company statements. [Course 5, Advanced Machine Learning](course5_advanced_ml/README.md) comes next: three weeks, 14 notebooks and a capstone, in which you fit and read bagging, random forests, AdaBoost, gradient boosting, XGBoost, and LightGBM, stack models on out-of-fold outputs, tune without fooling yourself, engineer features from financial ratios, handle a rare outcome with weights, resampling, or a threshold, describe a model with SHAP values, and finish with a four-model comparison on a public file of company ratios. [Course 6, Neural Networks](course6_neural_networks/README.md) follows: three weeks, 14 notebooks and a capstone, in which you compute gradients by hand and check them against TensorFlow, show that one neuron is a logistic regression, train networks in Keras one setting at a time, score recurrent and convolutional networks on the Treasury curve against carrying the last value forward, and finish with a network measured against LightGBM on a public file of company ratios. [Course 7, NLP, RAG, and LLMs](course7_nlp_and_llms/README.md) comes next: three weeks, 14 notebooks and a capstone, in which you read FOMC statements, 8-K filings, and real indentures with Python, turn text into TF-IDF vectors, word vectors, and sentence embeddings, classify and search it on the CPU, send requests to large language models with the key kept secret, extract an indenture's covenants with every number checked against the text, and finish with a covenant extraction tool run on an indenture you have never seen. [Course 8, Implementing Agentic AI](course8_agentic_ai/README.md) follows: three weeks, 14 notebooks and a capstone, in which you send a model its first tool request by hand, write the agent loop yourself, hand an agent your own bond math, the synthetic book, the Treasury curve, FOMC statements, and a real indenture as tools, reject any figure that is not the value of the tool result it cites, serve tools through MCP, rebuild the loop in the OpenAI Agents SDK, split the work between an orchestrator and four specialists, grade the desk against answer keys written first, stop it with guardrails and a budget, and finish with a multi-agent credit desk whose every number is traced; every agent run was recorded once and replays without a key. [Course 9, Deployment](course9_deployment/README.md) comes next: three weeks, 14 notebooks and a capstone, in which you push your code to GitHub after a scan that proves nothing private goes with it, review every change by its diff, run your tests on Linux on every push, put your own bond math behind a FastAPI service at a public URL, serve the Course 8 desk's brief with no key on the server, give it Streamlit and Gradio front ends and a Hugging Face Space, package it in Docker, log and monitor every request, measure a model's drift, and finish with the desk's brief as a public app on free accounts; every notebook runs offline, with the cloud steps shown as masked transcripts. [Course 10, Implementing RAG](course10_rag/README.md) follows: three weeks, 14 notebooks and a capstone, in which you ask a model five questions about a 10-K with no document and grade the answers against keys written first, load the filing as pages and items, chunk it with a recursive splitter you write, embed the chunks with pinned models and search them exactly with NumPy and FAISS, add BM25 and reciprocal rank fusion, rerank with a cross-encoder, tune one setting at a time on development questions, filter by metadata across four filings, demand a citation after every sentence, measure recall and MRR on a labelled set, put LLM judges beside a strict grader, refresh the index when a new filing arrives, serve the retriever behind FastAPI and price it, and finish with a cited question-answering tool over a folder of public filings; every generated answer was recorded once and replays without a key, and the local-model route runs on Colab's T4 GPU. [The Bonus course, Build Your Own Coding Agent](course_bonus_coding_agent/README.md), closes the series: one notebook in which you build a coding agent from an empty file on OpenAI's Responses API, with three tools that read, list, and edit files in one fenced folder and none that runs code, check the bond math it writes against Excel, give it a chat page with your own name on it, and deploy it to a private Hugging Face Space of your own; every model request replays without a key. Every model describes its dataset; nothing is a forecast, a rating, or a lending rule, and work on a real filing is descriptive extraction only. All ten courses and the Bonus course are ready.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

*This product uses the FRED&reg; API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.*

## If you know Excel, you already know how to think about this

Nothing in this course asks you to forget Excel. Wherever Excel has a feature for the job, the new idea is introduced next to it, with the formula written out, so you are translating something you know and not learning from nothing.

| In Excel you would | In Python you will | Course | Where |
|:---|:---|:---:|:---|
| Fill a formula down a column | Write the formula once, in a loop or on a whole array | 1 | Week 1, Day 1 and Week 2, Day 1 |
| Write a nested `IF` | Write `if`, `elif`, `else`, one test per line | 1 | Week 1, Day 1 |
| Use `VLOOKUP` or `INDEX` and `MATCH` | Merge two tables on a shared column | 1 | Week 2, Day 3 and Day 5 |
| Build a pivot table | Group by a column and summarize | 1 | Week 2, Day 3 and Day 5 |
| Type `=1.025^10` for a power, and use `QUOTIENT`, `MOD`, and `ROUND` | Write `1.025 ** 10`, `//`, `%`, and `round()`, and see why `^` is not a power in Python and `round(2.5)` gives 2 | 1 | Week 1, Day 1 |
| Goal Seek a yield, halve a bracket with `IF` formulas, or use `RATE` and `YIELD` | Write a bisection loop that solves the yield from a price | 2 | Week 1, Day 4 |

That is a sample. Every course works this way: all 158 comparisons, course by course, are in [Excel to Python](EXCEL.md).

What changes is what you get to keep. A spreadsheet holds the answer. Code holds the steps that produced it, so the same steps can be run again on tomorrow's file without anyone dragging a formula or repointing a range.

## Start here

There are two ways to run the notebooks. Pick one.

### Run in Google Colab, with nothing to install

Open any notebook in the [Course 1 map](course1_python_foundations/README.md#course-map) and click the **Open in Colab** badge at the top. Colab runs in your browser and needs only a Google account.

Use Colab on a personal account, with the course data only. Do not upload anything from your employer.

### Run on your own Windows machine

You need [Python 3.13](https://www.python.org/downloads/), [VS Code](https://code.visualstudio.com/) with the Python and Jupyter extensions, and [git](https://git-scm.com/downloads). On a work machine, check your firm's policy before installing anything.

Two things to get right before Step 1.

| Check | What to do |
|:---|:---|
| **Python on the PATH** | In the Python installer, tick **Add python.exe to PATH** on the first screen. If `python` is still not found later, use `py -3.13` wherever a step says `python`. |
| **Scripts allowed in PowerShell** | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once. Without it, Step 2 stops at `Activate.ps1` with a message that running scripts is disabled. |

**Step 1.** Get the course and open its folder.

```powershell
mkdir $HOME\projects -Force
cd $HOME\projects
git clone https://github.com/lenamonj/python-fixed-income.git
cd python-fixed-income
```

No git, or not allowed to install it? On the repo's GitHub page choose **Code**, then **Download ZIP**, unzip it into `projects`, and `cd` into the unzipped folder.

**Step 2.** Create an environment and install everything the series needs, in one step. The root `requirements.txt` pins every library of Courses 1 to 10 and the Bonus course.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

It is a large install: TensorFlow and PyTorch are in it, so allow time and a few gigabytes of disk. To install one course only, use that course folder's own `requirements.txt` instead; the files are cumulative, so a later course's file covers the earlier ones.

Every notebook also opens with an install section: its first code cell checks the course's pinned libraries and installs only what is missing, so in Google Colab there is nothing to set up, and on a machine prepared with Step 2 it prints that everything is present.

What the courses need beyond the install:

- Courses 1, 2, 4, 5, 6, 9 and 10 need no API key. Course 2 uses git from its first day.
- Course 3 uses a free FRED API key of your own, kept in a `.env` file outside the course repo or in Colab's Secrets panel, never in the repo; every notebook runs without one. The [Course 3 README](course3_market_data/README.md#your-fred-key) explains.
- Course 7's week 3 asks for a free OpenRouter key of your own (an OpenAI key works as the alternative route), kept in `my_bondmath\.env` or Colab's Secrets panel; with no key every week 3 notebook replays the course's saved responses. The [Course 7 README](course7_nlp_and_llms/README.md#your-openrouter-key) explains. Its two small models download into the Hugging Face cache, about 118 MB, the first time a notebook needs them.
- Course 8 needs no key: every agent run was recorded once and replays from the repo; an OpenAI or OpenRouter key of your own lets a notebook go live. The [Course 8 README](course8_agentic_ai/README.md#no-key-needed-and-going-live) explains.
- Course 9 deploys to your own free GitHub, Vercel, and Hugging Face accounts and runs Docker Desktop on your own machine; create the Hugging Face account before you start, because a free account hosts a Space only once it is older than 30 days. Every notebook runs offline. The [Course 9 README](course9_deployment/README.md#your-accounts) explains.
- Course 10 replays every generated answer and judge verdict from its saved runs; a key of your own in `my_bondmath\.env` makes the same cells live. In Colab it advises the T4 GPU runtime for its local-model cells and never requires it. The [Course 10 README](course10_rag/README.md#before-you-start) explains.
- The Bonus course replays its saved responses; an OpenAI key of your own in `my_bondmath\.env` makes the notebook live, and its last step deploys the agent to a private Space on the Hugging Face account you created for Course 9. The [Bonus course README](course_bonus_coding_agent/README.md#start-here) explains.

**Step 3.** Open the folder in VS Code.

```powershell
code .
```

Open `course1_python_foundations\week1\day1\01_python_for_fixed_income_intro.ipynb`, choose the `.venv` kernel in the top right, and run the first cell.

Two Course 1 notebooks, Week 4 Days 2 and 3, download two small word lists the first time they run, so they need an internet connection once.

## How a day works

Inside a course, each day has its own folder, and each folder holds three files with the same name.

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
| **Exercises you can check** | Each exercise has a check cell that tells you whether your number is right. |
| **The AI check** | Each day ends with code written in the style of an AI assistant. It has one bug. You find it by checking the output against a number you worked out yourself. |

That last habit is the point of the course. You will use AI assistants to write code. Code that runs is not the same as code that is right, and the way to tell the difference is to know what the answer should be.

## The courses

Each course has its own folder, its own course map, and its own list of what to install. Weeks start again at 1 in every course.

| Course | What it covers | Status |
|:---:|:---|:---:|
| 1 | [Python Foundations](course1_python_foundations/README.md): variables to pandas, charts, exploratory data analysis, text, and a project, in four weeks | Ready |
| 2 | [Bond Math](course2_bond_math/README.md): price, yield, accrued interest, duration, DV01, convexity, spread, and DTS, built by hand in your own tested module, checked against Excel, and finished with a risk report, in three weeks | Ready |
| 3 | [Market Data and Time Series](course3_market_data/README.md): an API key kept secret, FRED's JSON, market calendars, resampling, changes, volatility, z-scores, percentile ranks, slopes, butterflies, SQL, AI-written code reviewed with tests, and a daily market snapshot, in three weeks | Ready |
| 4 | [Machine Learning](course4_machine_learning/README.md): regression on the spread cross-section, logistic regression, thresholds, decision trees, walk-forward validation, clustering, PCA, and a three-model capstone, each model tested on rows it never saw, shown in confusion heatmaps, curves, and formatted tables, and described, never forecast, in three weeks | Ready |
| 5 | [Advanced Machine Learning](course5_advanced_ml/README.md): bagging, random forests, impurity and permutation importance, AdaBoost, gradient boosting, XGBoost, LightGBM, stacking, honest tuning, feature engineering on financial ratios, rare events, SHAP values, and a four-model capstone, with Course 4's test rows kept closed, shown in confusion heatmaps, curves, importance bars, and formatted tables, in three weeks | Ready |
| 6 | [Neural Networks](course6_neural_networks/README.md): tensors and gradients by hand, one neuron as a logistic regression, dense networks in Keras trained one setting at a time, losses, optimizers, batch normalization, dropout, early stopping, class weights, sequence models on the Treasury curve described, never forecast, and a capstone against LightGBM, all on the CPU, shown in loss curves, confusion heatmaps, ROC and precision-recall curves, residual plots, and formatted tables, in three weeks | Ready |
| 7 | [NLP, RAG, and LLMs](course7_nlp_and_llms/README.md): regular expressions and tokens, TF-IDF, a text classifier on 8-K sections, word vectors, sentence embeddings and semantic search, zero-shot classification, EDGAR, requests to large language models through OpenRouter with the key kept secret, covenant extraction from real indentures with every number checked against the text, retrieval with citations, and a covenant extraction tool as the capstone, descriptive extraction only, shown in confusion heatmaps by split, embedding scatters, annotated cosine heatmaps, token and cost bars, and formatted tables, in three weeks | Ready |
| 8 | [Implementing Agentic AI](course8_agentic_ai/README.md): the first tool request by hand, the agent loop with a step limit, tools from your own `bondmath` module, structured answers with every figure traced to a tool result, market and document tools, MCP, the OpenAI Agents SDK, an orchestrator with four specialists, memory, evals with answer keys decided first, guardrails and a budget, and a multi-agent credit desk as the capstone, every run replayed from saved responses so no key is needed, shown in bars of tokens, requests, and cost, tool-call counts, pass and fail grids, and formatted tables, in three weeks | Ready |
| 9 | [Deployment](course9_deployment/README.md): remotes, branches, pull requests reviewed by their diff, CI on Linux with GitHub Actions, what a server installs, a FastAPI bond service deployed to Vercel, the Course 8 desk served as a snapshot with no key on the server, Streamlit and Gradio front ends, a Hugging Face Space, Docker, request logs and monitoring, model files and drift, secrets, limits, and a cost meter, and the desk's brief as a public app as the capstone, all on free accounts, every notebook offline with the cloud steps shown as masked transcripts, shown in bars of transcript durations, sizes, request counts, and status codes, run histories, and formatted tables, in three weeks | Ready |
| 10 | [Implementing RAG](course10_rag/README.md): five questions asked closed book and with a prompt alone, a filing as pages and items, a recursive splitter, embeddings from three pinned models, exact search with NumPy and FAISS, BM25 and hybrid search, a cross-encoder reranker, a tuning grid read on development questions, metadata filters across four documents, prompts that must cite, recall and MRR on a labelled set, LLM judges measured against a strict grader, index refresh and corpus drift, a retrieval service and its cost, and a cited question-answering tool over public filings as the capstone, every answer replayed from saved runs so no key is needed, in three weeks | Ready |
| Bonus | [Build Your Own Coding Agent](course_bonus_coding_agent/README.md): a coding agent from an empty file on OpenAI's Responses API, the switch from Chat Completions field by field, three tools fenced to one workspace folder with none that runs code, a loop with a round limit and a rollback, a refusal rule sent before any request, bond math the agent writes checked against Excel, a Gradio chat page with your own name on it, and a private ZeroGPU Space of your own, every request replayed so no key is needed, shown in bars of the tokens of each request, the cost per task, the tool requests, and the Space's build steps, and formatted tables, in one notebook | Ready |

The Bonus course, Build Your Own Coding Agent, closes the series.

## The data

Every issuer, ticker, CUSIP, price, position, trade, and counterparty in the portfolio files is invented. The courses share one invented portfolio. No real company and no real security appears in any holdings file.

| File | What it holds |
|:---|:---|
| `data/holdings.csv` | 200 bonds: price, accrued interest, yield, spread, duration, DTS, par held, and market value |
| `data/benchmark.csv` | 821 bonds from 150 issuers, with index weights |
| `data/issuers.csv` | One row per issuer: ticker, name, sector, and rating |
| `data/ratings.csv` | The rating scale, with a score, a bucket, and investment grade or high yield |
| `data/positions.csv` | A lean version of the holdings, for joining to the other tables |
| `data/holdings_messy.csv` | The holdings with problems planted on purpose, for the data cleaning lessons |
| `data/holdings_messy_answer_key.md` | Every planted problem, listed |
| `data/trade_blotter.csv` | 374 trades in September 2026, in bonds from the holdings, with invented counterparties |
| `data/project_holdings.csv` | The course project's extract: the same desk one month later, as of 2026-10-30, with new problems planted in it |
| `data/project_cover_note.txt` | The cover note that comes with the project extract, with its control totals |
| `data/project_answer_key.md` | Every problem planted in the project extract. Read it after you finish |
| `data/bondmath_excel_reference.csv` | 306 bond cases priced by desktop Excel: coupon dates, day counts, price, accrued interest, yield, duration, DV01, and bumped prices, for Course 2's tests |
| `data/bondmath_excel_reference_tvm.csv` | 153 week 1 cases from Excel: `FV`, `PV`, `RATE`, `EFFECT`, `NOMINAL`, `PRICE`, and `YIELD`, each with the exact formula |
| `data/course2_treasury_curve.csv` | 10 tenors of the invented Treasury curve the holdings were built on |
| `data/course2_capstone_holdings.csv` | The Course 2 capstone's extract: 201 rows, the desk as of 2026-11-30, with bond-math problems planted in it |
| `data/course2_capstone_cover_note.txt` | The cover note that comes with the capstone extract, with its control totals |
| `data/course2_capstone_answer_key.md` | Every problem planted in the capstone extract. Read it after you finish |
| `data/course3_synthetic_spreads.csv` | 2,940 daily investment grade and high yield spreads in bp, one per date of the Treasury file. **Synthetic**: invented for Course 3, not ICE, Moody's, or any index |
| `data/course3_capstone_extract.csv` | The Course 3 capstone's vendor extract: 69 rows, 2026-07-01 to 2026-10-02, four Treasury tenors and the two synthetic spreads, with data problems planted in it |
| `data/course3_capstone_cover_note.txt` | The cover note that comes with the Course 3 extract, with its control figures |
| `data/course3_capstone_answer_key.md` | Every problem planted in the Course 3 extract. Read it after you finish |
| `data/course4_excel_reference.csv` | 294 values computed by desktop Excel for Course 4's tests: `LINEST` statistics, p-values, intervals, and VIFs on the benchmark, Breusch-Pagan by hand, ridge in closed form, Solver's logistic fits on the card file, `COUNTIFS` confusion counts, and a trapezoid ROC AUC, each with its formula |

The data is built to behave like a real portfolio.

| Rule | What it means |
|:---|:---|
| **Price and yield always agree** | Each yield is a synthetic Treasury yield plus a spread, and each price is calculated from that yield. |
| **One convention throughout** | Fixed-rate bullet bonds, semiannual coupons, 30/360 day count, modified duration. |
| **Identical for every student** | Seeded scripts generate every file: `tools/make_holdings.py` for the portfolio, `tools/make_blotter.py` for the trades, `tools/make_project_data.py` for the project extract, `tools/make_course2_data.py` for the Course 2 curve and capstone, and `tools/make_course3_data.py` for the Course 3 spreads, FRED-format samples, and capstone. `tools/make_excel_reference.py`, `tools/make_course3_excel_reference.py`, and `tools/make_course4_excel_reference.py` wrote the Excel values once, through desktop Excel on Windows. |
| **Checked** | `python -m pytest` confirms the identifiers are valid and that each bond's price, accrued interest, and duration match its yield. |
| **No real CUSIPs** | Every CUSIP uses an issuer number in the range reserved for internal use, with a valid check digit. |

Five files are real, public data, and they are not part of the portfolio. Their values are unchanged.

| File | What it holds | Source and terms |
|:---|:---|:---|
| `data/treasury_par_yields.csv` | Daily Treasury par yield curve rates, 2015-01-02 to 2026-10-02, 14 tenors | U.S. Department of the Treasury, [Daily Treasury Par Yield Curve Rates](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve). Listed by Treasury as public data under a public-domain dedication. |
| `data/credit_card_default.csv` | 30,000 credit card accounts in Taiwan in 2005, with whether each defaulted the following month | Yeh, I. (2009). Default of Credit Card Clients [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: the extra header row was dropped and the file was saved as CSV. |
| `data/fomc_statements.csv` | The 46 FOMC post-meeting statements from 2021-01-27 to 2026-09-16 | Board of Governors of the Federal Reserve System, [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm). The Board states that information on its website is in the public domain unless otherwise indicated. Only white space was changed. |
| `data/polish_bankruptcy_5year.csv` | 5,910 financial statements of Polish companies, 64 financial ratios (`Attr1` to `Attr64`), and whether each company went bankrupt within a year: the 5th-year file of the dataset, anonymised | Tomczak, S. (2016). Polish Companies Bankruptcy [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5F600. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: `5year.arff` from the UCI zip converted to CSV, the missing marker `?` written as an empty cell, `class` decoded to 0 or 1, and every other value written as the shortest text that reads back to the same number. Nothing recoded, corrected, sorted, or dropped. |
| `data/taiwan_bankruptcy.csv` | 6,819 rows of Taiwanese companies' financial ratios, 1999 to 2009: 95 features and whether each company went bankrupt, anonymised | Taiwanese Bankruptcy Prediction [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5004D. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: none to the contents; `data.csv` from the UCI zip renamed and kept byte for byte. |

The first three were retrieved on 2026-10-03, the Polish file on 2026-10-04, and the Taiwanese file on 2026-10-05. The scripts `tools/get_treasury_yields.py`, `tools/get_credit_card_default.py`, `tools/get_fomc_statements.py`, `tools/get_polish_bankruptcy.py`, and `tools/get_taiwan_bankruptcy.py` download each one again from the same source.

Course 3 adds three files derived from the public Treasury file. They hold its values, unchanged or computed from them, and no data downloaded from FRED.

| File | What it holds | Source and terms |
|:---|:---|:---|
| `data/course3_fred_format_dgs10.json` | 43 observations of the 10 Yr, 2026-08-03 to 2026-09-30, in the FRED API's response format, with `.` for 2026-09-07 | Values copied from `data/treasury_par_yields.csv`; the response format is FRED's structure, not FRED data |
| `data/course3_fred_format_dgs2.json` | The same for the 2 Yr | As above |
| `data/course3_excel_reference.csv` | 190 market dates of 2026: the 2, 5, 10, and 30 Yr, and Excel's results for changes, rolling volatility, z-scores, percentile ranks, 2s10s, and 2s5s10s, with each formula | Computed by desktop Excel from `data/treasury_par_yields.csv` |

Nothing pulled from the FRED API is stored in this repo. Course 3's live cells pull public Treasury series with the student's own key, and pull ICE BofA and Moody's series only to the student's own screen: those are licensed, held in memory, and never cached, written to a file, or committed.

Course 7 adds text: public statements, public filings written by real issuers, a public-domain word vector file, and outputs the course computed itself. Real issuers appear only as the authors of the documents, which are quoted for descriptive extraction only: what the document says, never a view on the issuer or its securities. The 46-row `data/fomc_statements.csv` is unchanged.

| File | What it holds | Source and terms |
|:---|:---|:---|
| `data/course7_fomc_statements.csv` | 226 FOMC post-meeting statements, 2000-02-02 to 2026-09-16, 13 of them unscheduled | Board of Governors of the Federal Reserve System, [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm), public domain unless otherwise indicated. Only white space was changed. |
| `data/course7_indentures/` | Three indentures as filed, each with its text: Boyd Gaming Corporation, 4.750% Senior Notes due 2031 (Exhibit 4.1 to the 8-K filed 2021-06-08); Levi Strauss & Co., 8-7/8% Senior Notes due 2016 (filed 2006-03-17); Lamar Media Corp., 6-5/8% Senior Subordinated Notes due 2015, Series C (filed 2007-10-16) | Public records on [sec.gov](https://www.sec.gov/about/privacy-information), which states that information on its site may be copied and distributed without the SEC's permission. Kept byte for byte; the `.txt` files are the course's text of each. |
| `data/course7_boyd_2021_indenture.pdf` | The Boyd indenture printed to PDF by the course from the SEC copy, 132 pages | The SEC copy's text; the page layout is the browser's |
| `data/course7_boyd_10k_2025.htm` | Boyd Gaming Corporation's Form 10-K for fiscal 2025, as filed | A public record on sec.gov |
| `data/course7_risk_factors.csv` | 99 Item 1A risk factors from the fiscal 2025 10-Ks of Boyd Gaming Corporation, Levi Strauss & Co., and Lamar Media Corp. | Public records on sec.gov. Only white space was changed. |
| `data/course7_8k_items.csv` | 5,126 item sections of Form 8-K current reports filed 2019 to 2025, eight items, each labelled by the item its filer chose, the bodies cut at 300 words | Public records on sec.gov; a sample drawn by `tools/get_8k_items.py` with a fixed seed |
| `data/course7_glove_6b_100d.npz` | GloVe 6B word vectors, 44,558 words at 100 numbers each | Pennington, Socher, and Manning (2014), [nlp.stanford.edu/projects/glove](https://nlp.stanford.edu/projects/glove/), Public Domain Dedication and License v1.0. A subset of the published file. |
| `data/course7_8k_minilm.npy`, `data/course7_8k_zero_shot.csv` | The two pinned models' outputs on the 8-K sections, computed once on one thread | The course's own, under the repo's MIT license |
| `data/course7_llm_responses/` | 66 responses of large language models to the course's week 3 requests, one file per request, recorded on 2026-10-08 | The course's own, under the repo's MIT license. No key and no request header is stored. |

The scripts `tools/get_fomc_history.py`, `tools/get_indentures.py`, `tools/get_edgar_filings.py`, `tools/get_8k_items.py`, `tools/make_indenture_pdf.py`, `tools/make_glove_subset.py`, and `tools/make_8k_model_outputs.py` made these files on 2026-10-07; the EDGAR scripts declare a contact in their requests and stay under the SEC's limit of 10 requests a second.

Course 8 adds no external data. Its agents read the files above (the synthetic holdings, the Treasury curve, the synthetic spreads, and Course 7's statements, indentures, and 8-K sections), and it adds three files of its own.

| File | What it holds | Source and terms |
|:---|:---|:---|
| `data/course8_eval_set.csv` | 30 desk questions with answer keys decided before any request: 20 answerable, 3 whose answer is not in the data, 5 adversarial, and 2 with an instruction planted in a tool result | The course's own, under the repo's MIT license. The keys are computed from the committed files. |
| `data/course8_synthetic_desk_memo.txt` | A 13-line desk memo about the synthetic book, with one planted instruction for the lesson on prompt injection | **Synthetic**: written for the course, under the repo's MIT license. It names no real issuer. |
| `data/course8_agent_runs/` | 350 requests and responses of the course's agent runs, one file per request, recorded on `gpt-4.1-mini` from 2026-10-08 to 2026-10-11 | The course's own, under the repo's MIT license. No key, no request header, and no account identifier is stored, and every tool result inside a request is computed from the committed files. |

Course 9 adds no external data. Its notebooks read the files above (the synthetic holdings, the Treasury curve, Course 2's Excel reference values, and Course 8's eval set and the capstone's saved runs), and it adds one synthetic file and one folder of its own.

| File | What it holds | Source and terms |
|:---|:---|:---|
| `data/course9_request_log.csv` | 19,664 requests to a bond and desk service over 30 days, 2026-09-03 to 2026-10-02 UTC: path, status, latency in ms, bytes out, and whether the request was refused, never a body, query, header, or client address. Three features are planted for the lessons: a slow day on `/dv01`, a burst of 422s from one malformed client, and a refused share on `/ask` | **Synthetic**: invented by `tools/make_course9_request_log.py` with a fixed seed; no real service, client, or request produced it. Under the repo's MIT license. |
| `data/course9_transcripts/` | 75 masked transcripts in 11 day folders, recorded on 2026-10-12: what GitHub, Vercel, Hugging Face, and Docker printed when the course ran each cloud step on its own accounts | The course's own, under the repo's MIT license. Account names, emails, addresses, and ids are masked to `student` and `<id>`; no token is stored. |

Course 10 reuses Course 7's Boyd 10-K and three indentures (the files above) and adds one PDF print, one new public filing, and four folders and files of its own.

| File | What it holds | Source and terms |
|:---|:---|:---|
| `data/course10_boyd_10k_2025.pdf` | Boyd Gaming's Form 10-K for fiscal 2025 printed to PDF by the course from the SEC copy: 113 pages; the text is the SEC copy's, the page layout is the course's print | **Real**, a public record on sec.gov, quoted for descriptive extraction only; the print is the course's own |
| `data/course10_boyd_10q_2026q2.htm` | Boyd Gaming's Form 10-Q for the quarter ended June 30, 2026, filed 2026-07-30, as filed (inline XBRL) | **Real**, a public record on sec.gov ("Information presented on sec.gov is considered public information and may be copied or further distributed"), quoted for descriptive extraction only |
| `data/course10_questions.csv` | 75 questions with answer keys written first from the documents' pages, each key a quote with its page, item, or section: 5 for day 1, 25 development, 20 test, 25 capstone, including 8 the corpus cannot answer and 3 requests for a view | The course's own, under the repo's MIT license |
| `data/course10_embeddings/` | 8 sets of embeddings (16 files, 14.4 MB) of the chunk tables by MiniLM, bge-small, and gte-small at pinned revisions, each with a sidecar naming the model, the chunker, and the hash of the chunk texts | The course's own derived data, computed once on one thread, under the repo's MIT license |
| `data/course10_rag_runs/` | 352 requests and responses of the course's answers and judge verdicts in 9 day folders, one file per request, recorded on `gpt-4.1-mini` on 2026-10-12 and 2026-10-13 | The course's own, under the repo's MIT license. No key, no request header, and no account identifier is stored. |
| `data/course10_human_labels.csv` | A reviewer of the course's groundedness and relevance labels on day 12's 45 answers, made from the question, the answer, and the chunks before any judge's verdict was shown | The course's own, under the repo's MIT license |

The Bonus course adds no external data and reads no file above. Its agent works in a fictional workspace that its own module writes at run time: `README.txt`, a riddle, and a `bonds.csv` of six bonds from six invented issuers, with no CUSIP, labelled fictional in the folder and never a file in `data/`. It adds two folders of its own.

| File | What it holds | Source and terms |
|:---|:---|:---|
| `data/bonus_agent_runs/` | 29 requests and responses of the course's agent on OpenAI's Responses API (`gpt-6.1-sol`), one file per request, recorded on 2026-10-12 | The course's own, under the repo's MIT license. No key, no request header, no account identifier, and no absolute path is stored, and every tool result inside a request comes from the fictional workspace. |
| `data/bonus_transcripts/` | 7 masked transcripts, recorded on 2026-10-12: what Hugging Face printed when the course created its private Space, built it, sent it three requests, ran it once without the ZeroGPU placeholder, and deleted it | The course's own, under the repo's MIT license. Account names, addresses, and ids are masked to `student` and `<id>`; no token is stored. |

*This product uses the FRED&reg; API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.*

## What is in this repo

```
python-fixed-income/
  EXCEL.md              every Excel comparison in the series, course by course
  course1_python_foundations/
    README.md           the course map
    requirements.txt    what the course's notebooks need
    week1/ ... week4/
      day1/ ... day5/   the notebook, its solutions, and its overview PDF
  course2_bond_math/
    README.md           the course map
    requirements.txt    what the course's notebooks need
    week1/ ... week3/
      day1/ ... day5/   the notebook, its solutions, and its overview PDF
  course3_market_data/
    README.md           the course map
    requirements.txt    what the course's notebooks need
    week1/ ... week3/
      day1/ ... day5/   the notebook, its solutions, and its overview PDF
  course4_machine_learning/
    README.md           the course map
    requirements.txt    what the course's notebooks need
    week1/ ... week3/
      day1/ ... day5/   the notebook, its solutions, and its overview PDF
  course5_advanced_ml/
    README.md           the course map
    requirements.txt    what the course's notebooks need
    week1/ ... week3/
      day1/ ... day5/   the notebook, its solutions, and its overview PDF
  course6_neural_networks/
    README.md           the course map
    requirements.txt    what the course's notebooks need
    week1/ ... week3/
      day1/ ... day5/   the notebook, its solutions, and its overview PDF
  course7_nlp_and_llms/
    README.md           the course map
    requirements.txt    what the course's notebooks need
    week1/ ... week3/
      day1/ ... day5/   the notebook, its solutions, and its overview PDF
  course8_agentic_ai/
    README.md           the course map
    requirements.txt    what the course's notebooks need
    week1/ ... week3/
      day1/ ... day5/   the notebook, its solutions, and its overview PDF
  course9_deployment/
    README.md           the course map
    requirements.txt    what the course's notebooks need
    week1/ ... week3/
      day1/ ... day5/   the notebook, its solutions, and its overview PDF
  course10_rag/
    README.md           the course map
    requirements.txt    what the course's notebooks need
    week1/ ... week3/
      day1/ ... day5/   the notebook, its solutions, and its overview PDF
  course_bonus_coding_agent/
    README.md           the course map
    requirements.txt    what the course's notebook needs (Course 9's file)
    week1/day1/         the notebook, its solutions, and its overview PDF
    deploy/             the three files a Hugging Face Space receives
  data/                 the invented portfolio and the public datasets, shared by every course
  tools/                the scripts that build or download the data, and the notebook banner
  tests/                checks on the data
  assets/               fonts and images
```

## License

Code is released under the [MIT License](LICENSE). The notebooks' written content, the slide overviews, and the videos are released under [CC BY 4.0](LICENSE-CONTENT): you may share and adapt them, including commercially, as long as you give credit.

The public data files and documents keep their own terms, listed in [The data](#the-data). They are not relicensed by this repo.

The fonts in `assets/fonts` are under the SIL Open Font License, and their license files sit beside them.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
