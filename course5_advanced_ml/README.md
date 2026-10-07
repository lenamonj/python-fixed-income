<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="520">
</picture>

![Course 5](https://img.shields.io/badge/Course_5-Advanced_Machine_Learning-123D2F?style=for-the-badge)
![Length](https://img.shields.io/badge/3_weeks-14_notebooks_%2B_capstone-1C7A57?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[The three weeks](#the-three-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Course 4](../course4_machine_learning/README.md)** &nbsp;·&nbsp; **[Course 6](../course6_neural_networks/README.md)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 5: Advanced Machine Learning

**Three weeks from one unstable tree to a four-model comparison on a file you have never seen, with every ensemble scored on rows it did not learn from, every tuned number reported honestly, and every contribution described, never read as a cause.**

</div>

On day one you take Course 4's default decision tree on the card file, draw ten bootstrap samples, and watch its leaves move while its first question stays put. Three weeks later you fit and read bagging, random forests, AdaBoost, gradient boosting, XGBoost, and LightGBM; build boosting by hand from residuals and match the library; tune with a randomized search and say when the gain is smaller than the noise between folds; engineer features from financial ratios inside the folds; choose among class weights, resampling, and a threshold for a rare outcome; and split a company's score across its ratios with SHAP values. Then a public file of Taiwanese companies' ratios arrives, and you compare four models on it, choose one with reasons, open the test rows once, and write what the model shows and where it fails.

**That is the course: ensembles fitted, tuned, and read honestly, on data that is described, never forecast.**

Every model in this course describes a dataset. Nothing in it is a forecast, a rating, or a lending rule. A probability on the card file is a number about that file, never a credit decision about a person; a fitted spread is the model's spread for a bond with those characteristics, never a fair value; an importance says what the model leans on, and a SHAP value is a contribution to the model's score, never a driver or a reason for default.

Every function goes into a fourth module of your own, `ensemblekit.py`, which imports the `mlkit.py` you built in Course 4 and never changes it, with a test file that grows every day.

Four habits run through all of it.

| Habit | What it means |
|:---|:---|
| **Closed rows stay closed** | Course 4's splits are rebuilt exactly, and a row Course 4 used as a test row is never scored again. Settings, thresholds, early stopping, stacking, and resampling are all decided inside the training rows; a tuned score is reported nested. |
| **Excel as the bridge** | Excel has no forest, booster, search, SMOTE, or SHAP, and each notebook says so plainly. Then it shows the pieces Excel can do, with the formula beside the Python: one AdaBoost round by `SUMPRODUCT` and `LN`, one boosting round by `AVERAGEIFS`, fold scores by `STDEV.P`, a guarded ratio, a SHAP row adding up. |
| **The same answer on every run** | One seed, `SEED = 42`, and one thread, written out as `n_jobs=1` on every booster, forest, search, and cross-validation, so a rerun prints the same numbers. |
| **Describe, never forecast** | Every model output, importance, and SHAP value has a plain name and a list of names it is never given. Case studies end with "What the model shows, and where it fails" instead of recommendations. |

You need Course 4, or the same ground: train, validation, and test rows, `Pipeline` and `ColumnTransformer`, logistic regression and decision trees, cross-validation, ROC AUC and average precision, and the threshold rule. Each notebook writes the reference `mlkit.py` and the `ensemblekit.py` it starts from into its work folder, so a missing or unfinished module never stops it. This is the fifth course in [Python for Fixed Income](../README.md).

Status: <!-- count:ready -->14<!-- /count --> of <!-- count:total -->14<!-- /count --> notebooks are ready, and so is the capstone.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here). Course 5 runs in the same `.venv` as Courses 1 to 4.

| Step | What to do |
|:---|:---|
| **Install the course's packages** | With the course's `.venv` active, run the install line below. It adds XGBoost, LightGBM, imbalanced-learn, SHAP, and ipywidgets to Course 4's pins, and changes none of them. |
| **If `import lightgbm` fails** | If it stops with an `OSError` that names `lib_lightgbm.dll`, Windows is missing a runtime library LightGBM needs and pip does not install: install the Microsoft Visual C++ Redistributable for x64, a free download from Microsoft, and run the line again. The course has not tested this on a machine without that runtime. |
| **No API key** | This course needs no key and no account. Every dataset is in the repo. |
| **Keep your folder** | Your `my_bondmath` folder, in your `projects` folder beside the course repo, gains `ensemblekit.py` and its tests beside `mlkit.py`. If you skipped the earlier courses, create it with the last line below. |
| **Or use Colab** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge. Colab's library versions can differ from the pins, so a printed number may differ in its last digits; the setup cell says so when it happens. At the end of each day, download your files from the Colab file browser. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course5_advanced_ml\requirements.txt
python -c "import lightgbm; print(lightgbm.__version__)"
New-Item -ItemType Directory -Force "$HOME\projects\my_bondmath" | Out-Null
```

Each notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Each day's "Bring It Home" section shows the PowerShell steps that move the day's functions and tests into `my_bondmath`, copy in any data file the tests read, run the tests, and commit.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. As in Courses 2 to 4, every notebook ends in the same order: Excel side by side, save the day with Git, bring it home, then the exercises, with the AI check last. Git keeps the experiment log again: each model's results are committed beside its code, so a change of model is reviewed by its numbers.

## The three weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | Bagging | Say how much of a tree's output is noise from the rows it happened to see, bag trees and read an out-of-bag score for what it is, fit a random forest, rank features by impurity and by permutation and say why a column of random numbers fools one of them, and fit forests to the spread cross-section |
| 2 | Boosting | Run AdaBoost's rounds by hand, build gradient boosting from residuals and match the library, regularise XGBoost and stop it early on rows carved from the training rows, fit LightGBM, stack models on out-of-fold outputs, and say with bootstrap intervals which gaps on the card file are noise |
| 3 | Tuning, rare events, and the capstone | Tune with a randomized search and report a nested score, engineer features from financial ratios inside the folds, compare class weights, resampling, and a threshold for a rare outcome and recalibrate a moved score, describe a model with SHAP values, and compare four models on a file you have not seen |

## Course map

<!-- map:start -->

### Week 1: Bagging

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Tree Instability and the Bootstrap](week1/day1/01_tree_instability_and_the_bootstrap.ipynb) | Course 4's split rebuilt with its test rows closed, the bootstrap and the share of rows it leaves out, ten trees on ten samples whose leaves move while the root stays, and averaging named, beside `FREQUENCY`, `COUNTIF`, and `STDEV.P` | Ready |
| 2 | [Bagging and Out-of-Bag Scores](week1/day2/02_bagging_and_out_of_bag_scores.ipynb) | Bagging by hand and with scikit-learn, how many trees, the out-of-bag score as an accuracy and the out-of-bag ROC AUC beside it, bagging a stable model, and what bagging cannot fix | Ready |
| 3 | [Random Forests](week1/day3/03_random_forests.ipynb) | A random subset of columns at each split, tree correlation, leaf size against tree count, class weights and the model's score, a small search on training folds, and extra trees, beside `INT(SQRT(19))`, `COMBIN`, and `CORREL` | Ready |
| 4 | [Impurity and Permutation Importance](week1/day4/04_impurity_and_permutation_importance.ipynb) | A column of random numbers that impurity importance ranks second and permutation importance ranks near last, correlated columns sharing importance, training rows against validation rows, and ROC AUC from ranks by `RANK.AVG` and `SUMIF` | Ready |
| 5 | [Case Study: Bagging and the Spread Cross-Section](week1/day5/05_case_study_bagging_and_the_spread_cross_section.ipynb) | Regression forests and out-of-bag R-squared, thresholds from out-of-fold probabilities, then OLS, a tree, and a forest on the benchmark by cross-validation, with and without coupon, and by issuer | Ready |

### Week 2: Boosting

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [AdaBoost](week2/day1/06_adaboost.ipynb) | Trees one after another, a stump, three rounds by hand matching scikit-learn, learning rate and rounds by cross-validation, and AdaBoost's score as a weighted vote, beside `SUMPRODUCT`, `LN`, and `EXP` | Ready |
| 2 | [Gradient Boosting from Residuals](week2/day2/07_gradient_boosting_from_residuals.ipynb) | Start from the mean and fit trees to residuals, boosting by hand matching the library to 1e-12, learning rate and depth, the generator's maturity cap the straight line misses, and two rounds in Excel by `AVERAGEIFS` and `IF` | Ready |
| 3 | [XGBoost, Regularization, and Early Stopping](week2/day3/08_xgboost_regularization_and_early_stopping.ipynb) | One XGBoost leaf and its gain by hand, why `n_jobs=1` is written out, each penalty one at a time, early stopping on rows carved from the training rows, `scale_pos_weight`, and log loss by formula | Ready |
| 4 | [LightGBM and Stacking](week2/day4/09_lightgbm_and_stacking.ipynb) | Leaf-wise trees and `num_leaves`, three boosters on one validation set, stacking on out-of-fold outputs by hand and with `StackingClassifier`, and whether the stack beats its best member, beside a blend and the stack's formula in Excel | Ready |
| 5 | [Case Study: Boosting on Credit Card Default](week2/day5/10_case_study_boosting_on_credit_card_default.ipynb) | Bootstrap intervals and paired differences on validation scores, six models compared with thresholds from out-of-fold probabilities, the chosen model's importance, and a results workbook checked with `PERCENTILE.INC` and `INDEX` and `MATCH` | Ready |

### Week 3: Tuning, rare events, and the capstone

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Randomized Search and Honest Tuning](week3/day1/11_randomized_search_and_honest_tuning.ipynb) | A grid's cost, `RandomizedSearchCV` with `scipy.stats` distributions, reading `cv_results_`, a tuning gain smaller than reshuffling the folds, and nested cross-validation, beside `AVERAGE` and `STDEV.P` of fold scores | Ready |
| 2 | [Feature Engineering on Financial Ratios](week3/day2/12_feature_engineering_on_financial_ratios.ipynb) | A feature that writes down a shape, ratios from ratios with a guarded denominator, missingness as a feature, transforms and clipping inside the pipeline, and a feature built from the outcome as the worst leak | Ready |
| 3 | [Resampling, SMOTE, and Class Weights](week3/day3/13_resampling_smote_and_class_weights.ipynb) | Class weights, oversampling, undersampling, and SMOTE inside an imbalanced-learn pipeline, the trap of resampling before the split, what each does to ranking and to the average output, a threshold instead, and recalibration | Ready |
| 4 | [SHAP Values](week3/day4/14_shap_values.ipynb) | A company's score split across its ratios in log-odds, waterfall, beeswarm, and dependence plots described, SHAP against gain and split counts, correlated columns, and the words a contribution may and may not be given | Ready |
| 5 | [Course 5 Capstone](week3/day5/course5_capstone.ipynb) | A real file of company ratios checked, described, prepared without a leak, and modelled four ways, tuned on training folds, tested once, and described with SHAP values. A [worked version](week3/day5/course5_capstone_solutions.ipynb) sits beside it | Ready |

<!-- map:end -->

## The capstone

Day 5 of week 3 is yours, and it is more than one sitting: plan on two or three. A colleague who covers Asian corporates hands you a public file of Taiwanese companies' financial ratios, each row flagged by whether the company went bankrupt, and asks which of four models separates the bankrupt rows best on rows it never saw, how sure anyone can be with so few bankrupt rows in the test set, which ratios the chosen model leans on, and where it fails. About 40 questions take you from your complete module to a written description. Nothing is planted in the file: its constant column, its identical column pairs, its columns that hold two scales, its row order, and its rare outcome are the work.

You hand in your module with its tests passing, a loading function that checks the file and cleans its column names, a description of the whole file before any split, a preparation step that splits without a leak, four models built as functions (a logistic regression, a random forest, XGBoost, and LightGBM) tuned on training folds, one decision on class imbalance with numbers, thresholds for a recall of 70 percent from out-of-fold probabilities, one comparison on the test rows with bootstrap intervals, SHAP values for the chosen model, a results workbook, a Git history with one commit per deliverable, a short log of any AI assistant use, and a written description of what the chosen model shows and where it fails.

| File | What it is |
|:---|:---|
| [`course5_capstone.ipynb`](week3/day5/course5_capstone.ipynb) | The brief, the questions, and a check cell for every answer that can be checked. A check says correct or not yet, and never shows the answer |
| [`course5_capstone_overview.pdf`](week3/day5/course5_capstone_overview.pdf) | The brief as slides: the scenario, the file, the deliverables, and how the checks work |
| [`course5_capstone_solutions.ipynb`](week3/day5/course5_capstone_solutions.ipynb) | The worked version, with every decision stated. Open it after you finish |

The description you write is about a historical, anonymised dataset. It is not a credit view on any company, and nothing you build is a rating, a credit decision, or a probability of default for any company going forward. The capstone's last section names the Freddie Mac loan-level dataset as further practice for students who register and download it themselves; it cannot be redistributed, so no notebook reads it.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| scikit-learn | Splits, pipelines, bagging, random forests, AdaBoost, gradient boosting, stacking, searches, permutation importance, and calibration | Week 1, Day 1 |
| pytest and Git | Testing `ensemblekit.py` every day, and keeping each model's results beside its code | Week 1, Day 1 |
| pandas and matplotlib | Tables and charts of every dataset | Week 1, Day 1 |
| XGBoost | Regularised gradient boosting with early stopping | Week 2, Day 3 |
| LightGBM | Leaf-wise gradient boosting, and the model SHAP describes | Week 2, Day 4 |
| openpyxl | Writing results workbooks for Excel | Week 2, Day 5 |
| scipy | The distributions a randomized search draws from | Week 2, Day 5 |
| imbalanced-learn | SMOTE, random oversampling and undersampling, inside its own pipeline | Week 3, Day 3 |
| SHAP | Tree SHAP values, and the waterfall, beeswarm, and dependence plots | Week 3, Day 4 |
| statsmodels | Not used directly; Course 4's `mlkit.py` imports it | Week 1, Day 1 |
| ipywidgets | Not used directly; it keeps `import shap` quiet in a notebook | Week 3, Day 4 |

Exact versions are pinned in [`requirements.txt`](requirements.txt). Git is installed separately (see [Course 2](../course2_bond_math/README.md#before-you-start)).

| Data | Kind | Used in |
|:---|:---|:---|
| Default of Credit Card Clients: 30,000 accounts in Taiwan in 2005 | Real, public: Yeh, I. (2009). Default of Credit Card Clients [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Days 1 to 4, 6, and 8 to 10 |
| The benchmark: 821 bonds of 150 issuers, with the rating scale | Synthetic: invented for this series, spreads generated by `tools/make_holdings.py` | Days 5, 7, and 12 |
| Polish Companies Bankruptcy, 5th year: 5,910 financial statements | Real, public: Tomczak, S. (2016). Polish Companies Bankruptcy [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5F600. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Days 11 to 14 |
| The UCI Taiwanese bankruptcy file: 6,819 rows of company financial ratios, 1999 to 2009 | Real, public: Taiwanese Bankruptcy Prediction [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5004D. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | The capstone |

Course 5 rebuilds Course 4's splits of the card, benchmark, and Polish files exactly and never scores a row Course 4 used as a test row. The card accounts describe people, so the four columns about them (sex, education, marriage, age) are never model features and no output is grouped by them. Consumer credit in Taiwan in 2005 differs from US credit, and the Polish and Taiwanese companies are each one market and period; every notebook that uses them says so. Sources, terms, and changes for every file are in [The data](../README.md#the-data) on the front page.

## What comes next

[Course 6 is Neural Networks](../course6_neural_networks/README.md): three weeks of tensors and gradients by hand, one neuron as a logistic regression, networks in Keras trained one setting at a time, losses, optimizers, batch normalization, dropout, early stopping, and class weights, sequence models on the Treasury curve described, never forecast, and a capstone that measures a network against LightGBM on the Taiwanese file's training rows. Your `mlkit` and `ensemblekit` are imported by a new module, `netkit`, and never changed.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
