<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="520">
</picture>

![Course 6](https://img.shields.io/badge/Course_6-Neural_Networks-123D2F?style=for-the-badge)
![Length](https://img.shields.io/badge/3_weeks-14_notebooks_%2B_capstone-1C7A57?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[The three weeks](#the-three-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Course 5](../course5_advanced_ml/README.md)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 6: Neural Networks

**Three weeks from one neuron worked out by hand to a network measured against boosting, with every gradient checked against TensorFlow, every setting chosen on rows the report never sees, and every sequence model on the Treasury curve scored on the past and described, never forecast.**

</div>

On day one you take one neuron on the card file, compute its log loss and its gradient by hand, check both against TensorFlow, and walk it downhill one step at a time to Course 4's logistic regression. Three weeks later you build and fit dense networks in Keras; show that one neuron is a logistic regression and that Excel's Solver finds the same weights; choose activations, width, depth, batch size, epochs, optimizer, learning rate, initialization, batch normalization, dropout, L2, early stopping, and class weights one setting at a time, with the seed's own spread as the yardstick; build windows of past changes on the Treasury curve and score SimpleRNN, LSTM, GRU, and one-dimensional convolutions walk-forward against carrying the last value forward; and open a set of held-out years once. Then a colleague asks whether a network beats the LightGBM model you chose on the Taiwanese companies' file, and you answer with paired folds and an interval.

**That is the course: networks fitted, tuned, and compared honestly, on data that is described, never forecast.**

Every model in this course describes a dataset. Nothing in it is a forecast, a rating, or a lending rule. A probability on the card file is a number about that file, never a credit decision about a person; a class-weighted network's output is a score, not a probability; a fitted spread is the network's spread for a bond with those characteristics, never a fair value; and a fitted change on the Treasury curve is how a rule would have scored on a past date, never a view on rates. The honest finding of week 3, that no network beat carrying the last value forward, is taught as the lesson.

Every function goes into a fifth module of your own, `netkit.py`, which imports the `mlkit.py` and `ensemblekit.py` you built in Courses 4 and 5 and never changes them, with a test file that grows every day.

Four habits run through all of it.

| Habit | What it means |
|:---|:---|
| **Closed rows stay closed** | Course 4's and Course 5's splits are rebuilt exactly, and a row an earlier course used as a test row is never scored again. Every setting is chosen on stopping rows carved from the training rows or by folds inside them; the Treasury file's held-out years, 2023 to 2026, are opened once, on day 14. |
| **Excel as the bridge** | Excel has no automatic differentiation, no network training, and no walk-forward routine, and each notebook says so plainly. Then it shows the pieces Excel can do, with the formula beside the Python: a neuron as `SUMPRODUCT` and `EXP`, a gradient step, Solver fitting one neuron, a ReLU as `MAX`, an Adam step, batch normalization by `VAR.P`, inverted dropout, an LSTM step, and a convolution as a weighted moving sum. |
| **The same answer on every run** | One seed, `SEED = 42`, set before every network is built, and one thread for TensorFlow and the maths libraries, so a rerun prints the same digits. The networks are kept small enough that a run on every core prints them too. |
| **Describe, never forecast** | Every model output has a plain name and a list of names it is never given. Case studies end with "What the model shows, and where it fails" instead of recommendations, and a sequence result's description passes a check for forecast words. |

You need Course 5, or the same ground: train, validation, and test rows, cross-validation, out-of-fold thresholds, early stopping on carved rows, class weights, bootstrap intervals, and LightGBM. Each notebook writes the reference `mlkit.py`, `ensemblekit.py`, and the `netkit.py` it starts from into its work folder, so a missing or unfinished module never stops it. This is the sixth course in [Python for Fixed Income](../README.md).

Status: <!-- count:ready -->14<!-- /count --> of <!-- count:total -->14<!-- /count --> notebooks are ready, and so is the capstone.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here). Course 6 runs in the same `.venv` as Courses 1 to 5.

| Step | What to do |
|:---|:---|
| **Install the course's packages** | With the course's `.venv` active, run the install line below. It adds TensorFlow and Keras to Course 5's pins, and changes none of them. TensorFlow is large: the download is about 350 MB and it takes about 1.5 GB once installed, so allow time and disk space. |
| **If `import tensorflow` fails** | If the last check line below stops with an `ImportError` or `OSError` about a DLL that could not be loaded, Windows is missing the Microsoft Visual C++ runtime, which TensorFlow's files rely on and pip does not install: install the Microsoft Visual C++ Redistributable for x64, a free download from Microsoft, and run the line again. The course has not tested this on a machine without that runtime. |
| **No GPU needed** | Every notebook runs on the CPU within its time budget. TensorFlow has no GPU support on native Windows, and the notebooks say so. Colab offers GPU runtimes; the course names that switch and never requires it. |
| **No API key** | This course needs no key and no account. Every dataset is in the repo. |
| **Keep your folder** | Your `my_bondmath` folder, in your `projects` folder beside the course repo, gains `netkit.py` and its tests beside `mlkit.py` and `ensemblekit.py`. If you skipped the earlier courses, create it with the last line below. |
| **Or use Colab** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge. Colab's library versions can differ from the pins, so a printed number may differ in its last digits; the setup cell says so when it happens. At the end of each day, download your files from the Colab file browser. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course6_neural_networks\requirements.txt
python -c "import tensorflow as tf; print(tf.__version__)"
New-Item -ItemType Directory -Force "$HOME\projects\my_bondmath" | Out-Null
```

Each notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Each day's "Bring It Home" section shows the PowerShell steps that move the day's functions and tests into `my_bondmath`, run the tests, and commit.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. As in Courses 2 to 5, every notebook ends in the same order: Excel side by side, save the day with Git, bring it home, then the exercises, with the AI check last. Git keeps the experiment log again: each network's results are committed beside its code.

## The three weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | From one neuron to a network | Compute a log loss and its gradient by hand and check them against TensorFlow, fit one neuron and show it is a logistic regression, add hidden layers and count their weights, read a pair of loss curves and the epoch early stopping picks, measure how much the seed alone moves a network, and put a network beside logistic regression and LightGBM on the card file with intervals |
| 2 | Training | Choose a loss and a learning rate on a regression, take momentum and Adam steps by hand and match Keras, see why a network starts where it starts and what batch normalization does, make overfitting visible and brake it with L2, dropout, and early stopping, and decide on class weights for a rare outcome by numbers |
| 3 | Sequences and the capstone | Build windows of past changes with no lookahead, score dense, recurrent, and convolutional networks walk-forward on the Treasury curve against carrying the last value forward, open held-out years once, and compare a network with LightGBM on a file you know |

## Course map

<!-- map:start -->

### Week 1: From one neuron to a network

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Tensors and Gradients](week1/day1/01_tensors_and_gradients.ipynb) | Where Courses 4 and 5 left the card file, the test-row rule, TensorFlow on the CPU, tensors, one neuron by hand, the gradient of a log loss checked against `tf.GradientTape`, and gradient descent by hand, beside a neuron and a 100-step path in Excel by `SUMPRODUCT` and `EXP` | Ready |
| 2 | [One Neuron Is a Logistic Regression](week1/day2/02_one_neuron_is_a_logistic_regression.ipynb) | Scaling on the fit rows only, `compile` and `fit`, one Keras neuron matching scikit-learn's logistic regression and Course 4's odds ratios, Solver finding the same weights, and what mini-batches leave short of the optimum | Ready |
| 3 | [Hidden Layers and Activations](week1/day3/03_hidden_layers_and_activations.ipynb) | Sigmoid, tanh, and ReLU, a two-unit layer by hand and in Excel by `MAX` and `TANH`, a forward pass in numpy, counting parameters, a ladder of one setting at a time, and why layers with no activation are one neuron | Ready |
| 4 | [Batch Size, Epochs, and Loss Curves](week1/day4/04_batch_size_epochs_and_loss_curves.ipynb) | Epochs, batches, and steps, loss curves on the fit and stopping rows, batch size at a fixed number of epochs, early stopping, where a GPU helps, and the seed's spread as the yardstick, beside `ROUNDUP` and `MATCH(MIN(...))` | Ready |
| 5 | [Case Study: A First Network on Credit Card Default](week1/day5/05_case_study_a_first_network_on_credit_card_default.ipynb) | Building in a function so every model is seeded, out-of-fold outputs and thresholds by five folds, then a case study: scaling chosen by folds, a ladder held to the seed's spread, and the network beside logistic regression and LightGBM with bootstrap intervals | Ready |

### Week 2: Training

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Loss Functions and the Learning Rate](week2/day1/06_loss_functions_and_the_learning_rate.ipynb) | A linear network that is OLS, MSE, MAE, and Huber by hand and in Excel, standardizing the target and turning it back to bp, learning rates too small and too large, and networks by five folds beside OLS on the spread cross-section | Ready |
| 2 | [Momentum, Adam, and Learning Rate Schedules](week2/day2/07_momentum_adam_and_learning_rate_schedules.ipynb) | Keras's SGD, momentum, Adam, and RMSprop checked against hand steps, Adam's bias correction, optimizers and learning rates chosen on the stopping rows, and a schedule, beside a momentum path and three Adam steps in Excel | Ready |
| 3 | [Initialization and Batch Normalization](week2/day3/08_initialization_and_batch_normalization.ipynb) | Glorot and He starting weights, why zeros never separate, vanishing gradients in a deep sigmoid network, batch normalization by hand and in Excel by `VAR.P`, and scoring mode's moving averages | Ready |
| 4 | [Overfitting, Dropout, and Early Stopping](week2/day4/09_overfitting_dropout_and_early_stopping.ipynb) | Overfitting made visible on the Polish file, an L2 penalty by `SUMSQ`, inverted dropout by hand, early stopping, all three by five folds beside logistic regression and LightGBM, and how many rows a network needs | Ready |
| 5 | [Case Study: Class Weights on Bankruptcy](week2/day5/10_case_study_class_weights_on_bankruptcy.ipynb) | Balanced class weights and the weighted log loss by hand and in Excel, why a weighted network's output is a score, then a case study: class weights against a lower threshold, and the network beside LightGBM with paired intervals | Ready |

### Week 3: Sequences and the capstone

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Windows and Walk-Forward on the Yield Curve](week3/day1/11_windows_and_walk_forward_on_the_yield_curve.ipynb) | The question in the past tense, development and held-out years set before any fit, windows of 20 past changes, zero change and the training mean as baselines, a dense network walk-forward, and levels against changes, beside `OFFSET` windows in Excel | Ready |
| 2 | [Recurrent Networks: LSTM and GRU](week3/day2/12_recurrent_networks_lstm_and_gru.ipynb) | A recurrent step by hand, parameter counts, the LSTM's gates checked against Keras and in Excel by `MMULT`, SimpleRNN, LSTM, and GRU walk-forward, and why a network ends near the mean when there is little to fit | Ready |
| 3 | [One-Dimensional Convolutions and Many Tenors](week3/day3/13_one_dimensional_convolutions_and_many_tenors.ipynb) | A filter as a weighted moving sum by `SUMPRODUCT`, pooling, a Conv1D walk-forward, all 11 tenors as channels, keeping same-day changes out, and every sequence model so far in one table | Ready |
| 4 | [Case Study: Sequence Models on the Treasury Curve](week3/day4/14_case_study_sequence_models_on_the_treasury_curve.ipynb) | Comparing folds, the words a sequence result may use, then a case study: two candidates chosen on the development years, the held-out years opened once, the seed's spread, and what the model shows, and where it fails, beside `AVERAGEIFS` by fold | Ready |
| 5 | [Course 6 Capstone](week3/day5/course6_capstone.ipynb) | Course 5's Taiwanese companies' training rows, a network built one setting at a time by five folds, LightGBM by the same folds on three fold seeds, paired differences and intervals, and a written choice. A [worked version](week3/day5/course6_capstone_solutions.ipynb) sits beside it | Ready |

<!-- map:end -->

## The capstone

Day 5 of week 3 is yours, and it is more than one sitting: plan on two or three. The colleague from Course 5's capstone comes back: you chose LightGBM on the Taiwanese companies' file, a network is what everyone asks about, so on the same rows and by the same folds, does a network do better, and how sure can anyone be? Thirty-three questions take you from your complete module to a written description. Nothing is planted in the file: its two scales, its rare outcome, and the small number of bankrupt rows in each fold are the work. Course 5's test rows stay closed: the whole comparison runs on its training rows, by cross-validation.

You hand in your module with its tests passing, a function that rebuilds Course 5's training rows and checks them, a short description of those rows, a network and its preparation chosen one setting at a time by five folds, a decision on class weights with numbers, LightGBM with Course 5's settings by the same folds, the comparison on three fold seeds with paired differences and bootstrap intervals, thresholds for a recall of 70 percent from out-of-fold outputs, a results workbook, a Git history with one commit per deliverable, a short log of any AI assistant use, and a written description of what the comparison shows and where it fails.

| File | What it is |
|:---|:---|
| [`course6_capstone.ipynb`](week3/day5/course6_capstone.ipynb) | The brief, the questions, and a check cell for every answer that can be checked. A check says correct or not yet, and never shows the answer |
| [`course6_capstone_overview.pdf`](week3/day5/course6_capstone_overview.pdf) | The brief as slides: the scenario, the rows, the deliverables, and how the checks work |
| [`course6_capstone_solutions.ipynb`](week3/day5/course6_capstone_solutions.ipynb) | The worked version, with every decision stated. Open it after you finish |

The description you write is about a historical, anonymised dataset. It is not a credit view on any company, and nothing you build is a rating, a credit decision, or a probability of default for any company going forward.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| TensorFlow | Tensors, `tf.GradientTape`, and the engine Keras runs on | Week 1, Day 1 |
| Keras | Every network: dense, recurrent, and convolutional layers, optimizers, losses, and early stopping | Week 1, Day 1 |
| scikit-learn | Splits, scalers and transformers fitted on the fit rows only, folds, metrics, and logistic regression | Week 1, Day 1 |
| LightGBM | The boosting model every network is compared with | Week 1, Day 1 |
| pytest and Git | Testing `netkit.py` every day, and keeping each network's results beside its code | Week 1, Day 1 |
| pandas and matplotlib | Tables, loss curves, and charts of every dataset | Week 1, Day 1 |
| openpyxl | Writing results workbooks for Excel | Week 1, Day 5 |
| statsmodels and scipy | Not used directly; Course 4's `mlkit.py` imports them | Week 1, Day 1 |
| XGBoost, imbalanced-learn, SHAP, ipywidgets | Not used; kept from Course 5's pins so one environment runs Courses 4 to 6 | |

Exact versions are pinned in [`requirements.txt`](requirements.txt): TensorFlow 2.21.0 and Keras 3.15.1 on top of Course 5's pins, among them numpy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1, LightGBM 4.7.0, and pytest 9.1.1. Git is installed separately (see [Course 2](../course2_bond_math/README.md#before-you-start)).

| Data | Kind | Used in |
|:---|:---|:---|
| Default of Credit Card Clients: 30,000 accounts in Taiwan in 2005 | Real, public: Yeh, I. (2009). Default of Credit Card Clients [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Days 1 to 5, 7, and 8 |
| The benchmark: 821 bonds of 150 issuers, with the rating scale | Synthetic: invented for this series, spreads generated by `tools/make_holdings.py` | Day 6 |
| Polish Companies Bankruptcy, 5th year: 5,910 financial statements | Real, public: Tomczak, S. (2016). Polish Companies Bankruptcy [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5F600. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Days 9 and 10 |
| Daily Treasury par yield curve rates, 2015-01-02 to 2026-10-02 | Real, public: U.S. Department of the Treasury, public domain | Days 11 to 14 |
| The UCI Taiwanese bankruptcy file: 6,819 rows of company financial ratios, 1999 to 2009 | Real, public: Taiwanese Bankruptcy Prediction [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5004D. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | The capstone |

Course 6 rebuilds Course 4's splits of the card, benchmark, and Polish files and Course 5's split of the Taiwanese file exactly, and never scores a row an earlier course used as a test row. On the Treasury file it sets its own development years (2015 to 2022) and held-out years (2023 to 2026-10-02) before any network is fitted, and nothing is fitted for or reported at any date after 2026-10-02. The card accounts describe people, so the four columns about them (sex, education, marriage, age) are never model features and no output is grouped by them. Consumer credit in Taiwan in 2005 differs from US credit, and the Polish and Taiwanese companies are each one market and period; every notebook that uses them says so. Course 6 adds no data file. Sources, terms, and changes for every file are in [The data](../README.md#the-data) on the front page.

## What comes next

Later courses build on the `bondmath`, `marketdata`, `mlkit`, `ensemblekit`, and `netkit` you wrote in Courses 2 to 6. Course 7, NLP and LLMs, is planned next.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
