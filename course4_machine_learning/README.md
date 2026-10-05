<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="520">
</picture>

![Course 4](https://img.shields.io/badge/Course_4-Machine_Learning-123D2F?style=for-the-badge)
![Length](https://img.shields.io/badge/3_weeks-14_notebooks_%2B_capstone-1C7A57?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[The three weeks](#the-three-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 4: Machine Learning

**Three weeks from a fitted line to a three-model comparison on data you have never seen, with every model tested on rows it did not learn from and every number checked against Excel or a library.**

</div>

On day one you take Course 1's line of OAS on rating score and treat it as a model: fitted on training rows, judged on rows it never saw, with its error in bp. Three weeks later you fit and read regressions and classifiers, choose a threshold for the recall a desk asks for, prune a decision tree, validate a model on dated data with no lookahead, group bonds and issuers with clustering, and summarise the Treasury curve's history with PCA. Then a public file of Polish company statements arrives, and you compare three models on it, choose one with reasons, and write what it shows and where it fails.

**That is the course: models fitted, tested, and read honestly, on data that is described, never forecast.**

Every model in this course describes a dataset. Nothing in it is a forecast, a rating, or a lending rule. A fitted spread is the model's spread for a bond with those characteristics, never a fair value; a probability on the card file is a number about that file, never a credit decision about a person; a Treasury model describes the file's own past and is never fitted for a date after its last row.

Every function goes into a third module of your own, `mlkit.py`, beside the `bondmath.py` and `marketdata.py` you built in Courses 2 and 3, with a test file that grows every day.

Four habits run through all of it.

| Habit | What it means |
|:---|:---|
| **Test rows stay closed** | The split comes first. Scaling, encoding, imputation, thresholds, and settings are fitted on training rows only, every split has a no-leak test, and the test rows are opened once, for the reported numbers. |
| **Excel as the bridge** | Wherever Excel has a function for the job, from `LINEST` and Solver to `COUNTIFS` and `MMULT`, the formula is written out beside the Python and checked against it. Where Excel has none (ridge, lasso, trees, clustering, PCA), the notebook says so plainly. |
| **The same answer on every run** | One seed, `SEED = 42`, and one thread for the maths libraries, so a rerun prints the same numbers. |
| **Describe, never forecast** | Every model's output has a plain name and a list of names it is never given. Case studies end with "What the model shows, and where it fails" instead of recommendations. |

You need Courses 1 to 3, or the same ground: pandas and matplotlib, functions with docstrings and tests, pytest, local Git, and the no-lookahead test of Course 3. Each notebook writes the reference `mlkit.py` it starts from into its work folder, so a missing or unfinished module never stops it. This is the fourth course in [Python for Fixed Income](../README.md).

Status: <!-- count:ready -->14<!-- /count --> of <!-- count:total -->14<!-- /count --> notebooks are ready, and so is the capstone.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here). Course 4 runs in the same `.venv` as Courses 1 to 3.

| Step | What to do |
|:---|:---|
| **Install the course's packages** | With the course's `.venv` active, run the install line below. It adds scikit-learn, statsmodels, and scipy to Course 2's pins. |
| **No API key** | This course needs no key and no account. Every dataset is in the repo. |
| **Keep your folder** | Your `my_bondmath` folder, in your `projects` folder beside the course repo, gains `mlkit.py` and its tests. If you skipped the earlier courses, create it with the last line below. |
| **Or use Colab** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge. Colab's library versions can differ from the pins, so a printed number may differ in its last digits; the setup cell says so when it happens. At the end of each day, download your files from the Colab file browser. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course4_machine_learning\requirements.txt
New-Item -ItemType Directory -Force "$HOME\projects\my_bondmath" | Out-Null
```

Each notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Each day's "Bring It Home" section shows the PowerShell steps that move the day's functions and tests into `my_bondmath`, copy in any data file the tests read, run the tests, and commit.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. As in Courses 2 and 3, every notebook ends in the same order: Excel side by side, save the day with Git, bring it home, then the exercises, with the AI check last. In this course Git also keeps an experiment log: each model's results are committed beside its code, so a change of model is reviewed by its numbers.

## The three weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | Regression on the spread cross-section | Split, fit, and score a spread regression in bp; read coefficients, p-values, and VIFs; check the assumptions behind them; work in log spreads; and use ridge and lasso inside a pipeline that fits every step on training rows |
| 2 | Classification on the card file | Fit a logistic regression and read odds ratios, build a confusion matrix, say why 78 percent accuracy can catch no defaults, choose a threshold on validation rows, prune and read a decision tree, and open the test rows once in a case study |
| 3 | Dated data, unsupervised learning, and the capstone | Validate on dated rows with walk-forward splits and no lookahead, scale and cluster bonds and issuers and profile the groups in their own units, describe the curve with PCA, and compare three models on a file you have not seen |

## Course map

<!-- map:start -->

### Week 1: Regression on the spread cross-section

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [The ML Workflow and Simple Regression](week1/day1/01_the_ml_workflow_and_simple_regression.ipynb) | A model as a function fitted to rows and judged on rows it did not see, the train and test split, scikit-learn's fit pattern, R-squared, MAE, and RMSE in bp, beside `SLOPE`, `INTERCEPT`, and `RSQ`, and where the synthetic spreads came from | Ready |
| 2 | [Multiple Regression and Dummy Variables](week1/day2/02_multiple_regression_and_dummy_variables.ipynb) | More than one feature, dummy variables with a named reference level, the trap `get_dummies(drop_first=True)` sets, adjusted R-squared, and `LINEST` and `TREND` on the same rows | Ready |
| 3 | [Coefficients, P-Values, and Multicollinearity](week1/day3/03_coefficients_p_values_and_multicollinearity.ipynb) | statsmodels' summary read line by line, what a p-value is and is not, the joint F-test, VIF, perfect collinearity, and bonds of one issuer, beside `T.DIST.2T`, `T.INV.2T`, and `F.DIST.RT` | Ready |
| 4 | [Regression Assumptions and Log Spreads](week1/day4/04_regression_assumptions_and_log_spreads.ipynb) | Residuals, the fan, Breusch-Pagan and normality tests, Q-Q plots, why a log spread fits the way spreads are built, and MAE back in bp | Ready |
| 5 | [Case Study: Ridge, Lasso, and the Spread Cross-Section](week1/day5/05_case_study_ridge_lasso_and_the_spread_cross_section.ipynb) | Ridge and lasso, scaling, `Pipeline` and `ColumnTransformer`, alpha by cross-validation, the split by issuer, and the fitted rating effects beside the generator's own table | Ready |

### Week 2: Classification on the card file

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Logistic Regression and Odds](week2/day1/06_logistic_regression_and_odds.ipynb) | Why a line fails on a 0/1 outcome, the logistic curve, odds and odds ratios with units, statsmodels and scikit-learn side by side, and a logistic fit by Excel's Solver with its non-negative trap | Ready |
| 2 | [Confusion Matrix, Precision, and Recall](week2/day2/07_confusion_matrix_precision_and_recall.ipynb) | The all-zero model's accuracy, the confusion matrix by `COUNTIFS`, precision, recall, and F1 for the default class, and what a threshold trades | Ready |
| 3 | [ROC Curves and Choosing a Threshold](week2/day3/08_roc_curves_and_choosing_a_threshold.ipynb) | ROC and precision-recall curves, AUC and average precision, a threshold for a recall the desk asks for, chosen on validation rows, Youden's J, and one calibration chart | Ready |
| 4 | [Decision Trees](week2/day4/09_decision_trees.ipynb) | A tree as questions, Gini by hand, the default tree, class weights, pre-pruning and post-pruning, a tree read as nested `IF`, and what feature importance does not mean | Ready |
| 5 | [Case Study: Credit Card Default](week2/day5/10_case_study_credit_card_default.ipynb) | Heavy tails and a quantile transform, three models compared on validation rows, the test rows opened once, the people-attribute section, and a results workbook for Excel | Ready |

### Week 3: Dated data, unsupervised learning, and the capstone

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Dated Data and Walk-Forward Validation](week3/day1/11_dated_data_and_walk_forward_validation.ipynb) | Why a random split flatters a model on dated rows, walk-forward splits and `TimeSeriesSplit`, a relationship that drifts, ridge and lasso on collinear tenors, and lookahead in a feature | Ready |
| 2 | [Scaling and K-Means](week3/day2/12_scaling_and_k_means.ipynb) | Distance and why units decide it, K-means by hand and with scikit-learn, the elbow and the silhouette, choosing k as a judgement, and clusters described, never ranked | Ready |
| 3 | [Hierarchical Clustering and Cluster Profiling](week3/day3/13_hierarchical_clustering_and_cluster_profiling.ipynb) | Linkages, the dendrogram and where to cut it, cophenetic correlation, profiles in the data's own units, and a pivot table beside `MEDIAN(IF(...))` | Ready |
| 4 | [PCA and t-SNE](week3/day4/14_pca_and_t_sne.ipynb) | Level, slope, and curvature from PCA on the Treasury curve, scores as history, PCA inside a pipeline only, scaling on mixed units, and t-SNE as a picture | Ready |
| 5 | [Course 4 Capstone](week3/day5/course4_capstone.ipynb) | A real file of company statements checked, described, prepared without a leak, and modelled three ways, chosen on training folds and tested once. A [worked version](week3/day5/course4_capstone_solutions.ipynb) sits beside it | Ready |

<!-- map:end -->

## The capstone

Day 5 of week 3 is yours, and it is more than one sitting: plan on two or three. A colleague who covers emerging market corporates hands you a public file of Polish companies' financial ratios, each statement flagged by whether the company went bankrupt in the following year, and asks which of three standard models separates them, how well on rows it never saw, and where it fails. About 40 questions take you from your complete module to a written description. Nothing is planted in the file: its real missing values, duplicate rows, extreme ratios, and rare outcome are the work.

You hand in your module with its tests passing, a loading function that checks the file, a description of the whole file before any split, a preparation step that drops duplicates and splits without a leak, three models built as functions (a logistic regression and two pruned trees), thresholds for a recall of 70 percent chosen on training folds, one comparison on the test rows, a results workbook, a Git history with one commit per deliverable, a short log of any AI assistant use, and a written description of what the chosen model shows and where it fails.

| File | What it is |
|:---|:---|
| [`course4_capstone.ipynb`](week3/day5/course4_capstone.ipynb) | The brief, the questions, and a check cell for every answer that can be checked. A check says correct or not yet, and never shows the answer |
| [`course4_capstone_overview.pdf`](week3/day5/course4_capstone_overview.pdf) | The brief as slides: the scenario, the file, the deliverables, and how the checks work |
| [`course4_capstone_solutions.ipynb`](week3/day5/course4_capstone_solutions.ipynb) | The worked version, with every decision stated. Open it after you finish |

The description you write is about a historical, anonymised dataset. It is not a credit view on any company, and nothing you build is a rating, a credit decision, or a probability of default for any company going forward.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| scikit-learn | Splits, pipelines, linear and logistic models, trees, clustering, PCA, and t-SNE | Week 1, Day 1 |
| pytest and Git | Testing `mlkit.py` every day, and keeping each model's results beside its code | Week 1, Day 1 |
| pandas and matplotlib | Tables and charts of every dataset | Week 1, Day 1 |
| statsmodels | Coefficient tables, p-values, VIFs, residual tests, and the logistic fit read for odds ratios | Week 1, Day 2 |
| scipy | Distributions, normality tests, and hierarchical clustering | Week 1, Day 3 |
| openpyxl | Writing results workbooks for Excel | Week 2, Day 5 |

Exact versions are pinned in [`requirements.txt`](requirements.txt). Git is installed separately (see [Course 2](../course2_bond_math/README.md#before-you-start)).

| Data | Kind | Used in |
|:---|:---|:---|
| The benchmark: 821 bonds of 150 issuers, with the rating scale | Synthetic: invented for this series, spreads generated by `tools/make_holdings.py` | Week 1, and days 12 to 14 |
| Excel reference values for the regressions and the logistic fit | Computed by desktop Excel from the benchmark and the card file | Weeks 1 and 2 |
| Default of Credit Card Clients: 30,000 accounts in Taiwan in 2005 | Real, public: Yeh, I. (2009). Default of Credit Card Clients [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Week 2 |
| U.S. Treasury daily par yield curve rates, 2015 to 2026 | Real, public domain | Days 11 and 14 |
| Polish Companies Bankruptcy, 5th year: 5,910 financial statements | Real, public: Tomczak, S. (2016). Polish Companies Bankruptcy [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5F600. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | The capstone |

The card accounts describe people, so the four columns about them (sex, education, marriage, age) are never model features, and one section of day 10 describes the chosen model's flags by group with counts and nothing more. Consumer credit in Taiwan in 2005 differs from US credit, and the Polish companies are one country and period; every notebook that uses them says so. Sources, terms, and changes for every file are in [The data](../README.md#the-data) on the front page.

## What comes next

Later courses build on the `bondmath`, `marketdata`, and `mlkit` you wrote in Courses 2 to 4.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
