<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/wordmark-dark.png">
  <img src="assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="520">
</picture>

![Course 1](https://img.shields.io/badge/Course_1-Python_Foundations-123D2F?style=for-the-badge)
![Course 2](https://img.shields.io/badge/Course_2-Bond_Math-123D2F?style=for-the-badge)
![Course 3](https://img.shields.io/badge/Course_3-Market_Data_and_Time_Series-123D2F?style=for-the-badge)
![Course 4](https://img.shields.io/badge/Course_4-Machine_Learning-123D2F?style=for-the-badge)
![Course 5](https://img.shields.io/badge/Course_5-Advanced_Machine_Learning-123D2F?style=for-the-badge)
![Course 6](https://img.shields.io/badge/Course_6-Neural_Networks-123D2F?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)
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

The series starts with [Course 1, Python Foundations](course1_python_foundations/README.md): four weeks, one notebook a day, 19 notebooks and a project. [Course 2, Bond Math](course2_bond_math/README.md) follows: three weeks, 14 notebooks and a capstone, in which you build price, yield, accrued interest, duration, DV01, convexity, spread, and DTS yourself, test every function against Excel, and finish with a risk report on a whole book. [Course 3, Market Data and Time Series](course3_market_data/README.md) comes next: three weeks, 14 notebooks and a capstone, in which you pull market data from an API with a key that never leaks, clean it against the bond market's own calendar, compute changes, volatility, z-scores, percentile ranks, slopes, and butterflies with no lookahead, query the book with SQL, and finish with a daily market snapshot that runs again on any date. [Course 4, Machine Learning](course4_machine_learning/README.md) follows: three weeks, 14 notebooks and a capstone, in which you fit and read regressions and classifiers on credit data, choose a threshold on rows the test set never saw, prune a decision tree, validate on dated data with no lookahead, cluster bonds and issuers, describe the Treasury curve with PCA, and finish with a three-model comparison on a public file of company statements. [Course 5, Advanced Machine Learning](course5_advanced_ml/README.md) comes next: three weeks, 14 notebooks and a capstone, in which you fit and read bagging, random forests, AdaBoost, gradient boosting, XGBoost, and LightGBM, stack models on out-of-fold outputs, tune without fooling yourself, engineer features from financial ratios, handle a rare outcome with weights, resampling, or a threshold, describe a model with SHAP values, and finish with a four-model comparison on a public file of company ratios. [Course 6, Neural Networks](course6_neural_networks/README.md) follows: three weeks, 14 notebooks and a capstone, in which you compute gradients by hand and check them against TensorFlow, show that one neuron is a logistic regression, train networks in Keras one setting at a time, score recurrent and convolutional networks on the Treasury curve against carrying the last value forward, and finish with a network measured against LightGBM on a public file of company ratios. Every model describes its dataset; nothing is a forecast, a rating, or a lending rule. All six are ready.

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

**Step 2.** Create an environment and install what Course 1 needs. Each course folder has its own `requirements.txt`.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r course1_python_foundations\requirements.txt
```

For Course 2, install its file into the same environment. Course 2 also uses git from the first day.

```powershell
python -m pip install -r course2_bond_math\requirements.txt
```

For Course 3, install its file too. Course 3 uses a free FRED API key of your own, kept in a `.env` file outside the course repo or in Colab's Secrets panel, never in the repo; every notebook runs without one. The [Course 3 README](course3_market_data/README.md#your-fred-key) explains.

```powershell
python -m pip install -r course3_market_data\requirements.txt
```

For Course 4, install its file too. It adds scikit-learn, statsmodels, and scipy, and needs no API key.

```powershell
python -m pip install -r course4_machine_learning\requirements.txt
```

For Course 5, install its file too. It adds XGBoost, LightGBM, imbalanced-learn, and SHAP, and needs no API key. If `import lightgbm` fails, the [Course 5 README](course5_advanced_ml/README.md#before-you-start) says what to install.

```powershell
python -m pip install -r course5_advanced_ml\requirements.txt
```

For Course 6, install its file too. It adds TensorFlow and Keras and needs no API key. TensorFlow is a large download, about 350 MB and about 1.5 GB once installed, so allow time and disk space. If `import tensorflow` fails, the [Course 6 README](course6_neural_networks/README.md#before-you-start) says what to install.

```powershell
python -m pip install -r course6_neural_networks\requirements.txt
```

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
| 4 | [Machine Learning](course4_machine_learning/README.md): regression on the spread cross-section, logistic regression, thresholds, decision trees, walk-forward validation, clustering, PCA, and a three-model capstone, each model tested on rows it never saw and described, never forecast, in three weeks | Ready |
| 5 | [Advanced Machine Learning](course5_advanced_ml/README.md): bagging, random forests, impurity and permutation importance, AdaBoost, gradient boosting, XGBoost, LightGBM, stacking, honest tuning, feature engineering on financial ratios, rare events, SHAP values, and a four-model capstone, with Course 4's test rows kept closed, in three weeks | Ready |
| 6 | [Neural Networks](course6_neural_networks/README.md): tensors and gradients by hand, one neuron as a logistic regression, dense networks in Keras trained one setting at a time, losses, optimizers, batch normalization, dropout, early stopping, class weights, sequence models on the Treasury curve described, never forecast, and a capstone against LightGBM, all on the CPU, in three weeks | Ready |

More courses are planned after these.

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
  data/                 the invented portfolio and the public datasets, shared by every course
  tools/                the scripts that build or download the data, and the notebook banner
  tests/                checks on the data
  assets/               fonts and images
```

## License

Code is released under the [MIT License](LICENSE). The notebooks' written content, the slide overviews, and the videos are released under [CC BY 4.0](LICENSE-CONTENT): you may share and adapt them, including commercially, as long as you give credit.

The four public data files keep their own terms, listed in [The data](#the-data). They are not relicensed by this repo.

The fonts in `assets/fonts` are under the SIL Open Font License, and their license files sit beside them.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
