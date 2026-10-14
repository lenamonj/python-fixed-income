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
| Wrap a number in `TEXT` and join it to a sentence with `&` | Write an f-string with a format code | 1 | Week 1, Day 1 |
| Write a nested `IF` | Write `if`, `elif`, `else`, one test per line | 1 | Week 1, Day 1 |
| See `#N/A`, `#DIV/0!`, or `#NAME?` in a cell | Read an error that names the line and the cause | 1 | Week 1, Day 3 |
| Put an `IF` beside a total that shows OK or CHECK | Write an `assert` that stops the run when the total is wrong | 1 | Week 1, Day 3 |
| Turn on AutoFilter and sort a sheet | Filter and sort a table by condition | 1 | Week 2, Day 2 |
| Use `SUMIF` and `COUNTIF` | Filter, then sum or count | 1 | Week 2, Day 2 and Day 5 |
| Use `COUNTBLANK` and Remove Duplicates | Count missing values and repeated rows in one line each | 1 | Week 2, Day 4 |
| Use `VLOOKUP` or `INDEX` and `MATCH` | Merge two tables on a shared column | 1 | Week 2, Day 3 and Day 5 |
| Build a pivot table | Group by a column and summarize | 1 | Week 2, Day 3 and Day 5 |
| Open and save a workbook with several sheets | Read a sheet into a table, and write tables to the sheets of a new workbook | 1 | Week 2, Day 3 and Day 5 |
| Use `SUMPRODUCT` over `SUM` for a weighted average | Do the same arithmetic on two columns | 1 | Week 2, Day 3 and Day 5 |
| Insert a chart: Column, Line, Scatter, Histogram, Box and Whisker | Draw the same chart in a few lines of code | 1 | Week 3, Day 1 |
| Add a trendline, and use `SLOPE`, `INTERCEPT`, and `RSQ` | Fit the line and print its numbers with units | 1 | Week 3, Day 2 |
| Use Remove Duplicates, `TRIM`, and `QUARTILE.INC` to clean and check a sheet | Find and fix the same problems in code, and print the totals before and after | 1 | Week 3, Day 3 |
| Use `XLOOKUP` by date, and `AVERAGEIFS` by year | Select by date and group a time series by year | 1 | Week 3, Day 4 |
| Net buys against sells with two `SUMIFS`, and keep a running total | Sign the sells, group, and take a cumulative sum | 1 | Week 3, Day 5 |
| Use `AVERAGEIF` on a column of 0s and 1s to get a rate by group | Group, then take the mean and the count together | 1 | Week 4, Day 1 |
| Use `FIND`, `SUBSTITUTE`, `TRIM`, and Find and Replace on text | Search and clean text with patterns, across every row at once | 1 | Week 4, Day 2 |
| Count words from a list with `SUMPRODUCT`, and standardize with `STANDARDIZE` | Score every document against a word list and compare the scores | 1 | Week 4, Day 3 |
| Paste next month's rows into last month's workbook and re-point every range | Keep the steps as functions in one file and run them on the new file | 1 | Week 4, Day 4 |
| Use `FV` and `PV`, and read the minus sign `PV` returns | Write `future_value` and `present_value` and test them against Excel's values | 2 | Week 1, Day 1 |
| Price a bond on a coupon date with `NPV` over a column of cash flows, `-PV` with a payment, or `PRICE` | List the cash flows and discount them in one function | 2 | Week 1, Day 2 |
| Fill a column of `PRICE` formulas down a range of yields and chart it as a Scatter with Straight Lines | Price a grid of yields and plot the price-yield curve | 2 | Week 1, Day 3 |
| Restate a yield with `EFFECT` and `NOMINAL` | Write `convert_yield` between any two compounding frequencies | 2 | Week 1, Day 3 |
| Goal Seek a yield, halve a bracket with `IF` formulas, or use `RATE` and `YIELD` | Write a bisection loop that solves the yield from a price | 2 | Week 1, Day 4 |
| Round a coupon with `MROUND`, and open a workbook of live `PRICE` and `YIELD` formulas | Find the coupon on a 1/8 grid, and write a workbook of live formulas with openpyxl | 2 | Week 1, Day 5 |
| Read date serial numbers, and use `EDATE`, `EOMONTH`, `COUPPCD`, `COUPNCD`, and `COUPNUM` | Work with `date` values, add months, and build a coupon schedule back from maturity | 2 | Week 2, Day 1 |
| Use `COUPDAYBS`, `COUPDAYS`, `COUPDAYSNC`, `ACCRINT`, and `YEARFRAC` beside `DAYS360` | Count days on US 30/360 and actual/actual, and compute accrued interest | 2 | Week 2, Day 2 |
| Use `PRICE` between coupon dates, add accrued for the dirty price, use `YIELD`, and write the price out cell by cell | Write `price`, `dirty_price`, and `yield_to_maturity`, and invoice a month of trades | 2 | Week 2, Day 3 |
| Use `DURATION` and `MDURATION`, build DV01 from cells, and bump the yield in two `PRICE` cells | Write duration and DV01 functions, and check DV01 by bumping the yield | 2 | Week 2, Day 4 |
| Estimate convexity from three `PRICE` cells, and total a book's DV01 with `SUMPRODUCT` | Write `convexity`, and reprice a whole book with its DV01 and duration | 2 | Week 2, Day 5 |
| Interpolate a curve with `FORECAST.LINEAR`, `INDEX`, and `MATCH`, and chart it as a Scatter | Write `interpolate_yield`, with flat ends, and compare it with `numpy.interp` | 2 | Week 3, Day 1 |
| Use `YEARFRAC` for years to maturity, and subtract the curve yield for a spread | Measure every bond's spread to the curve, and reproduce the file's spread column | 2 | Week 3, Day 2 |
| Divide two bumped `PRICE` cells for spread duration, multiply for DTS, and total buckets with `SUMIFS` | Write `spread_duration` and `dts`, and group each bond's share of the book's DTS | 2 | Week 3, Day 3 |
| Add a calculated field to a pivot table, and run a What-If Data Table over a whole-book reprice | Group by sector and rating, and reprice the book under rate and spread scenarios | 2 | Week 3, Day 4 |
| Check a risk report workbook with `SUM` and `SUMPRODUCT`, and price a month-end and a final-period bond with the `COUP` functions, `PRICE`, and `YIELD` | Clean, recompute, and reconcile a month-end extract, and write the risk report to Excel | 2 | Week 3, Day 5 |
| Build a request URL in cells with `&` and `ENCODEURL`, and load a web CSV with Power Query From Web | Build the request in code, and read the key from `.env` so it is never typed into a cell or a file | 3 | Week 1, Day 1 |
| Load JSON with Power Query, and turn FRED's `.` into `#N/A` with `IFERROR(VALUE(...),NA())` | Parse FRED's JSON, reading `.` as missing and never as 0 | 3 | Week 1, Day 2 |
| Use `WEEKDAY`, `WORKDAY`, and `NETWORKDAYS` with a holiday list, and see `XLOOKUP` return `#N/A` on a date with no row | Take the market calendar from the data's own dates, and join two series inner or outer | 3 | Week 1, Day 3 |
| Find a month's last market date with `EOMONTH` and `MAXIFS`, look up a value as of a date with `XLOOKUP` match mode -1, and group a pivot table by month | Take the last observation of each week or month, labelled by its own date, and the as-of value | 3 | Week 1, Day 4 |
| Append and merge files with Power Query, and check a sheet with `SUMPRODUCT`, `UNIQUE`, and `COUNTBLANK` | Build one checked daily dataset from two files, and cache a download | 3 | Week 1, Day 5 |
| Write `=(B3-B2)*100` for a change in bp, `XLOOKUP` with `EDATE` for a one-month change, and `MAX` with `XLOOKUP` for the date of the largest move | Compute changes in bp over rows and over calendar periods, and price returns in percent | 3 | Week 2, Day 1 |
| Fill `STDEV.S` down a fixed-size range, with `STDEV.P`, `OFFSET`, and `*SQRT(252)` beside it | Compute rolling volatility over a trailing window of rows, and test that it uses no future data | 3 | Week 2, Day 2 |
| Use `STANDARDIZE`, and `COUNTIF` over `COUNT` for a percentile rank, beside `PERCENTRANK.INC`, `RANK.EQ`, and `RANK.AVG` | Compute rolling z-scores and percentile ranks that match Excel row for row | 3 | Week 2, Day 3 |
| Fill slope and butterfly formulas down the Treasury sheet, and weight a butterfly with `PRICE` and `MDURATION` | Compute slopes and butterflies in bp, and DV01-neutral weights from your own `bondmath` | 3 | Week 2, Day 4 |
| Build a summary sheet for one date with `XMATCH`, `XLOOKUP`, `INDEX`, `OFFSET`, `STANDARDIZE`, and `COUNTIF` | Build every measure as of one date in one table that reads nothing after it | 3 | Week 2, Day 5 |
| Use `COUNTIFS`, `SUMIFS`, `AVERAGEIFS`, `FILTER`, `TAKE` with `SORTBY`, and a pivot table | Write `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, and `LIMIT` in SQL, each checked against pandas | 3 | Week 3, Day 1 |
| Join with `XLOOKUP` or Power Query Merge, and find repeated keys with `COUNTIF` | Join tables in SQL, catch a join that duplicates rows, and use window functions for daily changes and month ends | 3 | Week 3, Day 2 |
| Check a suggested formula, `PERCENTRANK.INC`, against `COUNTIF` over `COUNT`, and a DV01 built from cells | Test code written in the style of an AI assistant against your own functions and Excel's values | 3 | Week 3, Day 3 |
| Open the snapshot workbook and check its numbers with `SUMIFS`, `STANDARDIZE`, and `COUNTIF` | Write a daily market snapshot to HTML and Excel from one function that runs on any date | 3 | Week 3, Day 4 |
| Test a pasted extract's dates and units with `DATE`, `WEEKDAY`, `COUNTIF`, and `IFERROR(VALUE(...),NA())` | Clean a vendor extract with checks that stop, reconcile it, and run the snapshot on two dates | 3 | Week 3, Day 5 |
| Fit `SLOPE`, `INTERCEPT`, and `RSQ` on a training sheet, and score a test sheet with `AVERAGE(ABS(...))` and `SQRT(SUMXMY2(...)/COUNT(...))` | Split the rows, fit on the training rows, and measure the error in bp on rows the model never saw | 4 | Week 1, Day 1 |
| Build dummy columns with `=--(D2="AAA")`, fit them with `LINEST`, and score the test rows with `TREND` | Encode ratings with a named reference level and fit a multiple regression | 4 | Week 1, Day 2 |
| Read `LINEST`'s standard errors, and compute p-values with `T.DIST.2T`, intervals with `T.INV.2T`, a VIF with `1/(1-R2)`, and a joint F-test with `F.DIST.RT` | Read statsmodels' coefficient table, test sector jointly, and measure multicollinearity | 4 | Week 1, Day 3 |
| Take `LN` and `EXP` of spreads, run Breusch-Pagan by hand with `LINEST` and `CHISQ.DIST.RT`, and compute Q-Q points with `NORM.S.INV` | Check a regression's assumptions with residual plots and tests, and model log spreads | 4 | Week 1, Day 4 |
| Standardize with `STANDARDIZE` and `STDEV.P`, and solve ridge in closed form with `MMULT`, `MINVERSE`, and `MUNIT` | Fit ridge and lasso inside a pipeline that scales on the training rows only | 4 | Week 1, Day 5 |
| Fill a logistic probability formula, sum a log-likelihood column, and maximise it with Solver, the non-negative box turned off | Fit a logistic regression and read odds ratios with `exp` | 4 | Week 2, Day 1 |
| Count a confusion matrix with `COUNTIFS` against a threshold cell | Count the confusion matrix and compute precision, recall, and F1 for the default class | 4 | Week 2, Day 2 |
| List thresholds with `SORT(UNIQUE(...))`, trace the ROC with `COUNTIFS`, take the AUC with `SUMPRODUCT`, and pick a threshold with `MAXIFS` | Draw ROC and precision-recall curves, and choose a threshold for a target recall on validation rows | 4 | Week 2, Day 3 |
| Compute Gini with `COUNTIFS`, a leaf's default share with `AVERAGEIFS`, and write a small tree as nested `IF` | Grow, prune, and read a decision tree | 4 | Week 2, Day 4 |
| Open the results workbook, recompute precision and recall, and find the best model with `INDEX` and `MATCH` | Compare three models on validation rows, open the test rows once, and write the comparison to Excel | 4 | Week 2, Day 5 |
| Fill `SLOPE(OFFSET(...))` down a trailing window, fit one fold with `TREND`, and compare a whole-history `STANDARDIZE` with a trailing one | Validate on dated rows with walk-forward splits, and show lookahead in a feature | 4 | Week 3, Day 1 |
| Measure distance to each centre with `SQRT(SUMXMY2(...))`, assign with `MATCH(MIN(...))`, and update the centres with `AVERAGEIF` | Scale the bonds and run K-means, with the elbow and the silhouette | 4 | Week 3, Day 2 |
| Count clusters with a pivot table, and take medians with `MEDIAN(IF(...))`, which a pivot table cannot give | Build a hierarchical clustering, cut it, and profile the clusters in their own units | 4 | Week 3, Day 3 |
| Build a `COVARIANCE.S` grid, and score each date with `MMULT` of the centred changes | Find level, slope, and curvature with PCA on the Treasury curve | 4 | Week 3, Day 4 |
| Check the capstone's results workbook with `COUNTIFS` against its threshold | Compare three models on a new file, test once, and write the results to Excel | 4 | Week 3, Day 5 |
| Chart a comparison of models as a clustered column or line chart, and shade a table with a conditional formatting color scale | Draw every comparison as a chart and show it as a formatted table with the best value in each column marked | 4 | Week 1, Day 1 to Week 3, Day 4 |
| Compute the share a sample leaves out with `=(1-1/n)^n`, count pasted positions with `FREQUENCY` and `COUNTIF`, and see `RANDARRAY` redraw on every recalculation | Draw a seeded bootstrap, count its rows, and measure how ten trees on ten samples disagree | 5 | Week 1, Day 1 |
| Average pasted tree columns with `AVERAGE`, and score a vote with `SUMPRODUCT` | Bag trees by hand and with scikit-learn, and read the out-of-bag score as the accuracy it is | 5 | Week 1, Day 2 |
| Count columns per split with `INT(SQRT(19))`, the chance one is tried with `COMBIN`, and two trees' agreement with `CORREL` | Fit a random forest, measure tree correlation, and summarise a search's fold scores | 5 | Week 1, Day 3 |
| Rank two importance columns with `RANK.EQ`, and compute a ROC AUC from `RANK.AVG` and `SUMIF` | Compare impurity and permutation importance, and catch a column of noise that one of them ranks second | 5 | Week 1, Day 4 |
| Turn a fitted log spread into bp with `EXP`, average the misses with `AVERAGE(ABS(...))`, and compute R-squared with `SUMXMY2` and `DEVSQ` | Score OLS, a tree, and a forest on the spread cross-section by cross-validation and by issuer | 5 | Week 1, Day 5 |
| Run an AdaBoost round with `SUMPRODUCT`, `LN`, and `EXP`, and see `LOG` return base 10 | Run three AdaBoost rounds by hand and match scikit-learn's stump weights | 5 | Week 2, Day 1 |
| Fit one boosting round from residuals with two `AVERAGEIFS` and an `IF` | Build gradient boosting from residuals and match the library to 1e-12 | 5 | Week 2, Day 2 |
| Add gradients with `SUMIFS` for an XGBoost leaf and its gain, and fill a log loss column with `LN` | Regularise XGBoost, stop it early on rows carved from the training rows, and compute log loss by hand | 5 | Week 2, Day 3 |
| Blend two pasted probability columns with `AVERAGE`, and apply a stack's logistic layer with `EXP` | Stack models on out-of-fold outputs and check whether the stack beats its best member | 5 | Week 2, Day 4 |
| Read a bootstrap interval with `PERCENTILE.INC`, and find the chosen model with `INDEX` and `MATCH` | Compare six models with bootstrap intervals and paired differences, and write the results to Excel | 5 | Week 2, Day 5 |
| Summarise five fold scores with `AVERAGE` and `STDEV.P`, not `STDEV.S` | Read a randomized search's results and report a nested score beside its best score | 5 | Week 3, Day 1 |
| Cap a column with `MIN`, guard a ratio with `IF(OR(...),NA(),...)`, clip with `PERCENTILE.INC`, and count gaps with `COUNTBLANK` | Engineer features from financial ratios, each statistic learned inside the fold | 5 | Week 3, Day 2 |
| Rebuild one SMOTE row with `=x+u*(nb-x)`, correct a resampled score by formula, and compute a Brier score with `SUMXMY2` | Compare class weights, resampling, and a threshold on a rare outcome, and recalibrate the score | 5 | Week 3, Day 3 |
| Add a SHAP row with `SUM` to the model's log-odds, turn it into a probability with `EXP`, and average absolute values with `AVERAGE(ABS(...))` | Split a company's score across its ratios with SHAP values, and never read a contribution as a cause | 5 | Week 3, Day 4 |
| Check the capstone's confusion matrix with `COUNTIFS`, its interval with `PERCENTILE.INC`, and a SHAP row with `SUM` | Compare four models on a new file, test once, describe the chosen one with SHAP values, and write the results to Excel | 5 | Week 3, Day 5 |
| Chart a comparison of models as a clustered column, bar, line, or scatter chart, add custom error bars for a spread of fold scores, and shade a table with a conditional formatting color scale | Draw every comparison as a chart and show it as a formatted table with the best value in each column marked | 5 | Week 1, Day 1 to Week 3, Day 4 |
| Fill a neuron's output `=1/(1+EXP(-($H$1+$H$2*A2)))` down a column, take its gradient with `SUMPRODUCT` over `ROWS`, and fill a 100-step descent path | Compute a log loss and its gradient by hand, check them against `tf.GradientTape`, and take gradient steps | 6 | Week 1, Day 1 |
| Maximise a log-likelihood with Solver, scale columns with `AVERAGE` and `STDEV.P`, and score a row with `SUMPRODUCT` and `EXP` | Fit one Keras neuron and show that it is a logistic regression, with the same odds ratios | 6 | Week 1, Day 2 |
| Build a hidden layer from `SUMPRODUCT`, `MAX`, and `TANH`, and count a network's weights with `=19*32+32+32*1+1` | Add hidden layers, reproduce a network's output in numpy, and count its parameters | 6 | Week 1, Day 3 |
| Count steps per epoch with `ROUNDUP`, and find the best epoch on a pasted loss column with `MATCH(MIN(...))` | Read loss curves, change the batch size, and stop early on rows carved from the training rows | 6 | Week 1, Day 4 |
| Count a confusion matrix with `COUNTIFS` on a flag column, and read a bootstrap interval with `PERCENTILE.INC` | Put a network beside logistic regression and LightGBM, with thresholds from out-of-fold outputs and paired intervals | 6 | Week 1, Day 5 |
| Compute MSE with `SUMXMY2`, MAE with `AVERAGE(ABS(...))`, a Huber row with `IF`, and standardize a column with `STDEV.P` | Fit regression networks with three losses, turn the target back to bp, and compare them with OLS by five folds | 6 | Week 2, Day 1 |
| Fill a momentum path and three Adam steps with the bias correction, and a decaying learning rate with `=$B$1*$B$2^(A6/$B$3)` | Check momentum and Adam steps against Keras, and choose an optimizer and a learning rate on the stopping rows | 6 | Week 2, Day 2 |
| Normalize a batch with `AVERAGE`, `VAR.P`, and `SQRT`, and compute Glorot's limit and He's spread with `SQRT` | Start a network from the right weights, see gradients vanish, and add batch normalization | 6 | Week 2, Day 3 |
| Drop values with `=A2*(B2>=0.2)/(1-0.2)`, and compute an L2 penalty with `SUMSQ` | Brake overfitting with L2, dropout, and early stopping, scored by five folds | 6 | Week 2, Day 4 |
| Compute balanced class weights with `ROWS` and `COUNTIF`, and a weighted log loss with `SUMPRODUCT` over `SUM` | Fit a class-weighted network, read its output as a score, and decide on weights by numbers | 6 | Week 2, Day 5 |
| Write `=(B3-B2)*100` for a change in bp, average a 20-day window with `OFFSET`, and score zero change with `AVERAGE(ABS(...))` | Build windows of past changes with no lookahead, and score a network walk-forward against carrying the last value forward | 6 | Week 3, Day 1 |
| Take a SimpleRNN and an LSTM step with `TANH`, `EXP`, and `MMULT`, and compare two spreads with `STDEV.P` | Fit SimpleRNN, LSTM, and GRU networks walk-forward, and check one LSTM step against Keras | 6 | Week 3, Day 2 |
| Fill a weighted moving sum `=SUMPRODUCT(B2:B6,$K$2:$K$6)+$K$7` down a column, then pool with `MAX` and `AVERAGE` | Fit a one-dimensional convolution, feed all 11 tenors in as channels, and keep same-day changes out | 6 | Week 3, Day 3 |
| Average errors by fold with `AVERAGEIFS`, and count the folds a rule wins with `COUNTIF` over `COUNT` | Choose a sequence model on the development years, open the held-out years once, and write the results to Excel | 6 | Week 3, Day 4 |
| Check the capstone's workbook with `AVERAGE`, `STDEV.P`, paired differences, `COUNTIFS`, and `PERCENTILE.INC` | Compare a network with LightGBM by paired folds on three fold seeds, with intervals, and write the results to Excel | 6 | Week 3, Day 5 |
| Chart a loss curve or a comparison of networks as a line, clustered column, bar, or histogram chart, set a logarithmic axis, and shade a grid with a conditional formatting color scale | Draw every loss curve and every comparison as a chart and show it as a formatted table with the best value in each column marked | 6 | Week 1, Day 1 to Week 3, Day 4 |
| Find a word with `SEARCH` and `FIND`, count it with `LEN` and `SUBSTITUTE` (a substring count), split a sentence with `TEXTSPLIT`, and pull the target range with `REGEXEXTRACT` | Normalize look-alike characters, pull numbers out of text with regular expressions, and split text into tokens | 7 | Week 1, Day 1 |
| Count the statements that hold a word with `COUNTIF(range,"*inflation*")`, compute an IDF with `LN`, scale a row with `SQRT(SUMSQ(...))`, and a cosine with `SUMPRODUCT` | Build TF-IDF by hand, check it against scikit-learn, and compare documents by cosine similarity | 7 | Week 1, Day 2 |
| Count a confusion matrix with `COUNTIFS` on item codes stored as text, and see `COUNTIF` count "2.1" as "2.10" where `EXACT` does not | Train a TF-IDF classifier on 8-K sections split by date, catch the heading leak, and report recall on the rare items | 7 | Week 1, Day 3 |
| Compute the cosine of two pasted word vectors with `SUMPRODUCT` and `SUMSQ`, and see `MATCH` and `XLOOKUP` ignore case where `EXACT` does not | Find a word's nearest neighbours in pretrained vectors, and use mean vectors as classifier features | 7 | Week 1, Day 4 |
| Count a statement's words from two named lists with `SUMPRODUCT`, `LEN`, and `SUBSTITUTE`, and score them per thousand words | Score every statement with a word list and with a classifier fitted only on earlier years, the label's own sentence removed first | 7 | Week 1, Day 5 |
| Compute a question's score against a chunk as `SUMPRODUCT` over 384 pasted numbers, and check each vector's length with `SQRT(SUMSQ(...))` | Embed an indenture's chunks and search it by meaning | 7 | Week 2, Day 1 |
| Read the item over a row's largest score with `INDEX`, `MATCH`, and `MAX`, and the share where two models agree with `SUMPRODUCT` | Score a zero-shot classifier and an embedding classifier against TF-IDF, reading every score by its label's name | 7 | Week 2, Day 2 |
| Count risk factors by cluster and filing with `COUNTIFS` | Cluster risk factor embeddings with K-means and describe each cluster by its words and its counts | 7 | Week 2, Day 3 |
| Cut an item out of pasted filing text with `TEXTBEFORE` and `TEXTAFTER`, and count its words with `TEXTSPLIT` | Turn an EDGAR filing into text and cut a 10-K into its items | 7 | Week 2, Day 4 |
| Check three models' confusion matrices on the test rows with `COUNTIFS`, then recall, precision, F1, and `AVERAGE` | Open the test sections once and compare three models with paired bootstrap intervals | 7 | Week 2, Day 5 |
| Price a request with `=B2*C2+B3*C3` on token counts and per-token prices, and see `SUMPRODUCT` treat prices pasted as text as 0 | Send a request to an LLM from code with the key kept secret, count its tokens, and price it | 7 | Week 3, Day 1 |
| Check a quote against its section with `=LEN(C2)<>LEN(SUBSTITUTE(C2,B2,""))`, because `SEARCH` fails on long quotes and reads `*` and `?` as wildcards | Extract a covenant into a schema and check every quote and number against the indenture | 7 | Week 3, Day 2 |
| Pull a grower basket out of a pasted sentence with `TEXTBEFORE(TEXTAFTER(A2,"greater of "),"%")`, and see a cell cut a long section at 32,767 characters | Check a model's baskets against a regular expression, put two indentures in one table, and read a PDF page as text and as an image | 7 | Week 3, Day 3 |
| Score retrieval with `ISNUMBER(MATCH(B2,C2:G2,0))`, with the section numbers kept as text | Retrieve an indenture's chunks for a question, answer with citations, and judge each answer against the retrieved text | 7 | Week 3, Day 4 |
| Check the capstone's workbook, whose quote and number checks are `SUBSTITUTE` and `SEARCH` formulas | Build a covenant extraction tool that runs on an indenture you have never seen, with a checked table, and write it to Excel | 7 | Week 3, Day 5 |
| Chart a count, a score, or a comparison of models as a line, clustered column, stacked column, bar, XY scatter, or histogram chart, and shade a `COUNTIFS` grid or a cosine table with a conditional formatting color scale | Draw every count, score, embedding, and comparison as a chart and show each comparison as a formatted table with the best value in each column marked | 7 | Week 1, Day 1 to Week 3, Day 4 |
| Build a DV01 from `PRICE`, `MDURATION`, and the accrued from `COUPDAYBS` over `COUPDAYS`, and price a run with `=B2*C2+B3*C3`, where `SUMPRODUCT` treats prices pasted as text as 0 | Hand a model your own `dv01` as a tool, run the tool it requests on your machine, and price the run from its token counts | 8 | Week 1, Day 1 |
| Count a pasted trace table's rows for a tool with `COUNTIF(C2:C7,"price")`, its requests with `COUNTIFS`, and its tokens with `SUM` | Write the agent loop with a step limit, and read every run as a trace table before its answer | 8 | Week 1, Day 2 |
| Use `PRICE`, `YIELD`, `MDURATION`, and `COUPDAYBS` over `COUPDAYS` on one bond, and build its DV01 from three cells | Offer Course 2's bond functions to a model as tools, each docstring stating its units, and check the tool results against Excel | 8 | Week 1, Day 3 |
| Check a figure against its tool value with `=ROUND(B2,D2)=C2`, at the decimals the answer wrote | Ask for an answer in a schema, and reject any figure that is not the value of the tool result it cites | 8 | Week 1, Day 4 |
| Total a sector with `SUMIFS` over a helper column, take the k-th largest with `LARGE`, weight by market value with `SUMPRODUCT` over `SUM`, and find a CUSIP with `INDEX` and `MATCH` | Compute every answer key with pandas first, then check a risk agent's figures on the synthetic book against them | 8 | Week 1, Day 5 |
| Look up a yield and a change in bp with `INDEX` and `MATCH(...,0)`, and see `#N/A` for a date the file lacks | Give an agent the Treasury curve as tools that return an error for a missing date, never the nearest row | 8 | Week 2, Day 1 |
| Check a cited section with `=ISNUMBER(MATCH(B2,C2:G2,0))`, the section numbers kept as text | Give an agent documents as tools, and check every section its answer cites against the sections the run read | 8 | Week 2, Day 2 |
| Compute a change and a slope in bp as the difference of two `INDEX` and `MATCH` cells times 100 | Serve your market tools from an MCP server, and send the model exactly the requests it saw before | 8 | Week 2, Day 3 |
| Write each curve change with `INDEX`, `MATCH`, and `*100`, and see the change in percent when `*100` is missing | Run a macro agent on the last two FOMC statements, and check its note's figures against pandas and its quotes against the statements | 8 | Week 2, Day 5 |
| Total requests and tokens by agent with `SUMIF`, which matches `"pm"` to `PM` where pandas' `==` does not | Split the work between an orchestrator and four specialists, and keep the run log by agent | 8 | Week 3, Day 1 |
| Look up a value by key and date with `=XLOOKUP(1,(A2:A4="10 Yr par yield")*(D2:D4="2026-10-02"),B2:B4,"no value for that date")` | Keep a desk memory that returns a value only for the date asked, never the latest one | 8 | Week 3, Day 2 |
| Count passed rows by kind with `COUNTIFS`, and average requests with `AVERAGEIFS`, on the eval log | Grade an agent on questions whose answer keys were decided first, and keep the scorecard in Git | 8 | Week 3, Day 3 |
| Check a request budget with `=IF(SUM(B2:B10)>=10,"stop","ok")`, where `>` lets one more request through | Stop a run in code, with guardrails and a budget checked before each request is sent | 8 | Week 3, Day 4 |
| Check the capstone's workbook, whose figure checks are `=ROUND(G2,H2)=C2` and whose scorecard is `COUNTIFS` and `AVERAGEIFS` | Build a multi-agent credit desk with every figure traced and the guardrail asserted, and write its checks to Excel | 8 | Week 3, Day 5 |
| Total a size table in MB with `=SUM(C2:C200)/1024^2`, and judge it against a 500 MB limit with `=IF(E1>500,"over","fits")` | List what a server must install from a file's imports, measure it with its dependencies, and see why the desk ships as a snapshot | 9 | Week 1, Day 4 |
| Count green runs on `main` with `=COUNTIFS(D2:D9,"success",B2:B9,"main")`, and take a pass rate that leaves cancelled runs out | Read a repo's CI runs as a table and a pass rate, and follow one change through a red run and a green one | 9 | Week 1, Day 5 |
| Price a bond with `PRICE`, take the accrued from `COUPDAYBS` over `COUPDAYS` and the DV01 from `MDURATION` times the dirty price over 10,000, and read a service's `/health` with `WEBSERVICE`, which sends `GET` only | Put `bondmath` behind a FastAPI service, test it without a network, and match Excel at 6 decimals on six bonds | 9 | Week 2, Day 1 |
| Read the deployed DV01 into a cell with `WEBSERVICE` and `=VALUE(TEXTBEFORE(TEXTAFTER(A2,"""dv01_per_100"":"),"}"))`, equal at Excel's 15 significant digits, and see a refused request come back as `#VALUE!` | Deploy the service to a public URL on Vercel and check it against `bondmath` on your own machine | 9 | Week 2, Day 2 |
| Price the desk's saved run with `=SUMPRODUCT(B2:B3,C2:C3)` on tokens and prices per token, where prices typed into text cells count as 0 | Serve the Course 8 desk's brief as a snapshot with no key on the server, and refuse a request for a view at the API | 9 | Week 2, Day 3 |
| Open a CSV from a download button and see Excel turn the CUSIP `99123E105` into the number 9.9123E+109, keep the course's CUSIPs as text, and read `True` and `False` as booleans for `COUNTIF` | Give the same functions a Streamlit page and a Gradio app, and offer identifiers in a workbook, where they stay text | 9 | Week 2, Day 4 |
| Summarise a request log with `COUNTIFS` and `AVERAGEIFS`, take p95 latency with `PERCENTILE.INC` over `FILTER`, and see `PERCENTILE.EXC` and `SMALL` with `INT` give other answers on 20 values | Log every request without its body, and read requests, errors, and p50 and p95 latency by path, with alerts by rule | 9 | Week 3, Day 2 |
| Score drift with `=STANDARDIZE(AVERAGE(recent),AVERAGE(train),STDEV.S(train))`, not `STDEV.P`, and count inputs outside the training range with two `COUNTIFS` against `MAX` and `MIN` | Keep a model as a file with its card, serve it, and measure how far its inputs have moved from its training window | 9 | Week 3, Day 3 |
| Cost a live month with `=SUMPRODUCT(C2:C5,D2:D5)` on tokens and prices, and mark each free-tier line with `=IF(B2>C2,"over","within")` | Keep secrets in platform settings, list every name the code reads, and meter a month against the free tiers | 9 | Week 3, Day 4 |
| Check the capstone's workbook, whose free-tier status is `IF` and whose model cost is `SUMPRODUCT` | Ship the desk's brief as a public app with CI, a request log, a daily cap, and a cost line, and write its numbers to Excel | 9 | Week 3, Day 5 |
| Grade an answer against its key with `ISNUMBER(SEARCH(key,answer))` and count the matches by stage with `COUNTIFS` | Grade a model's closed-book and prompt-only answers against keys written first, and see that none matches | 10 | Week 1, Day 1 |
| Paste a page one line per row and read `LEN` of each, and see a line such as `December 31, 2025` become a date serial in a General cell | Load a 10-K as pages with `pdf_pages`, keep the empty page, and map every page to its item | 10 | Week 1, Day 2 |
| Count a chunk's characters with `LEN` and its words with `LEN` and `SUBSTITUTE` (with `CHAR(10)` turned into a space), and check an overlap with `=RIGHT(B2,64)=LEFT(B3,64)` | Write a recursive splitter with size and overlap, and read what 64 characters carry across a cut | 10 | Week 1, Day 3 |
| Compute a cosine with `SUMPRODUCT` over `SQRT(SUMSQ())` on two pasted 384-number vectors | Embed the chunks with three pinned models and search them exactly with NumPy and FAISS | 10 | Week 1, Day 4 |
| Count matched keys by stage with `COUNTIFS`, and fill a 2 by 2 table of retrieval against grade with three `COUNTIFS` | Run the first RAG pipeline on five questions beside the closed-book and prompt-only stages, and say which miss was retrieval | 10 | Week 1, Day 5 |
| Write one BM25 term weight out with `LN` and the length penalty, and fuse two rankings with `=1/(60+rank)` summed by `SUMIFS` | Write BM25 by hand, check it against `rank-bm25`, and fuse it with embedding search by reciprocal rank fusion | 10 | Week 2, Day 1 |
| Read a tuning grid with `AVERAGEIFS` and order it with `SORTBY` | Run twelve named settings on development questions and read the results table | 10 | Week 2, Day 3 |
| Filter a corpus table with `COUNTIFS`, `ROWS(FILTER())`, and `TAKE(SORTBY(FILTER()))`, and see `4.10` typed into a General cell become 4.1 | Filter chunks by document and section before search, across four filings | 10 | Week 2, Day 4 |
| Check each cited chunk against the chunks sent with `ISNUMBER(MATCH())` on ids stored as text | Demand a citation after every sentence and reject the answer that has none | 10 | Week 2, Day 5 |
| Compute recall with `ISNUMBER(MATCH())` and `COUNTIF` over `ROWS`, and MRR with `AVERAGE(IFERROR(1/MATCH(),0))` | Measure retrieval recall at k and MRR on a labelled question set, by item | 10 | Week 3, Day 1 |
| Fill a 3 by 3 agreement table with `COUNTIFS`, write Cohen's kappa out as `(po-pe)/(1-pe)`, and colour the table with a colour scale | Put two LLM judges beside a strict grader and read the agreement table and kappa | 10 | Week 3, Day 2 |
| Match chunk texts with `EXACT` inside `SUMPRODUCT`, where `COUNTIF` and `MATCH` refuse a criterion over 255 characters, and see `MAXIFS` return 0 for a date before the first filing | Refresh an index when a new filing arrives, embedding only the new chunks, and answer as of each filing's date | 10 | Week 3, Day 3 |
| Price a run with `SUMPRODUCT` on tokens and prices per token, where prices pasted as text count as 0, and average by setting with `AVERAGEIFS` | Serve the retriever behind a FastAPI service and price a thousand answers | 10 | Week 3, Day 4 |
| Check the capstone's workbook, whose recall, MRR, `COUNTIFS` grids, kappa, and `SUMPRODUCT` bill are formulas | Build a cited question-answering tool over public filings with its evaluation report, and write its numbers to Excel | 10 | Week 3, Day 5 |
| Open `bonds.csv` and see `bond_id` stay text and the maturity become a date, shown as `########` until the column is widened, then list the rows below BBB- with `=FILTER(A2:F7,ISNUMBER(MATCH(E2:E7,{"BB+","BB","BB-","B+","B","B-"},0)))` | Ask your own coding agent which bonds in the file are high yield, and check its answer against the file | Bonus | Week 1, Day 1 |
| Price with `=PV(0.06,3,-5,-100)` and `=PV(0.05,3,-5,-100)`, and take `=MDURATION(DATE(2026,10,2),DATE(2029,10,2),0.05,0.06,1)` | Have the agent write `bond_price` and `modified_duration`, and check them against 97.3270, 100.0, and 2.6956 before you trust them | Bonus | Week 1, Day 1 |
| Count an agent's edits with `=COUNTIFS(B2:B40,"edit_file")` and its refused requests with `=COUNTIFS(D2:D40,"ERROR*")`, and price its run with `=SUMPRODUCT(B2:B40*$G$1)+SUMPRODUCT(C2:C40*$G$2)` | Read the agent's tool log as a table, and price its saved run from the token counts | Bonus | Week 1, Day 1 |

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
