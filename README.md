<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/wordmark-dark.png">
  <img src="assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="325">
</picture>

<h3>From your first line of code to your own AI agents.<br>Taught entirely through the work of a credit desk.</h3>

[![Courses](https://img.shields.io/badge/Courses-12_%2B_Bonus-123D2F?style=for-the-badge)](#the-courses)
[![Notebooks](https://img.shields.io/badge/Notebooks-178-123D2F?style=for-the-badge)](#the-courses)
[![Price](https://img.shields.io/badge/Price-Free-1C7A57?style=for-the-badge)](#start-here)
[![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)](#run-in-google-colab-with-nothing-to-install)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](LICENSE-CONTENT)

**[Start here](#start-here)** &nbsp;·&nbsp; **[The courses](#the-courses)** &nbsp;·&nbsp; **[How a day works](#how-a-day-works)** &nbsp;·&nbsp; **[Coming from Excel](#coming-from-excel)**

<br>

<table>
  <tr>
    <td align="center" valign="top" width="25%"><h2>178</h2>notebooks, every lesson<br>with worked solutions</td>
    <td align="center" valign="top" width="25%"><h2>199</h2>Excel comparisons,<br>formula by formula</td>
    <td align="center" valign="top" width="25%"><h2>35</h2>weeks, one notebook<br>a day</td>
    <td align="center" valign="top" width="25%"><h2>$0</h2>to take, and no key<br>needed to run</td>
  </tr>
</table>

</div>

## Python for fixed income professionals

Fixed income runs on judgement and on data. The judgement you already have: how a bond is priced, where it sits in the capital structure, what its spread is telling you. This series builds the other half. It teaches you to work with data directly in Python, from your first line of code to models and AI agents that do real work on a credit desk.

It starts at zero. No programming background is assumed, and [Day 00](course1_python_foundations/week1/day00/00_setup_your_computer.ipynb) walks you through the setup screen by screen. From there, every lesson is built on the instruments, files, and questions of a fixed income portfolio: coupons and cash flows, holdings extracts and trade blotters, the Treasury curve, FOMC statements, 10-Ks, and bond indentures. Each course ends with a tool you built, tested, and can show.

> [!NOTE]
> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## The courses

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/readme/path-dark.png">
    <img src="assets/readme/path-light.png" width="720" alt="The path: Foundations (Courses 1 to 3), then Machine learning (4, 5, 5B, 5C, and 6), then Language models and agents (7 and 8), then Build and ship (9, 10, and the Bonus)">
  </picture>
</p>

| | Course | Weeks | What you build |
|:---:|:---|:---:|:---|
| **1** | [Python Foundations](course1_python_foundations/README.md) | 4 | A month-end review of a holdings extract: cleaned, checked against its control totals, compared with its benchmark, and written to Excel |
| **2** | [Bond Math](course2_bond_math/README.md) | 3 | Your own bond math module, tested against Excel, and a risk report on a whole book: duration, DV01, convexity, spread, and DTS |
| **3** | [Market Data and Time Series](course3_market_data/README.md) | 3 | A daily market snapshot from a vendor extract you test, clean, and reconcile, written to HTML and Excel |
| **4** | [Machine Learning](course4_machine_learning/README.md) | 3 | Three models compared on a public file of company statements, each tested on rows it never saw |
| **5** | [Advanced Machine Learning](course5_advanced_ml/README.md) | 3 | Logistic regression, a random forest, XGBoost, and LightGBM compared on company ratios where bankruptcies are rare |
| **5B** | [Time Series Models](course5b_time_series/README.md) | 2 | Two series modelled walk-forward with ARIMA, smoothing, GARCH, and LightGBM, each measured against carrying the last value forward |
| **5C** | [Risk Models](course5c_risk_models/README.md) | 2 | A risk report on a synthetic book: Monte Carlo credit loss, backtested VaR, a hazard model, a trade screen, and PSI |
| **6** | [Neural Networks](course6_neural_networks/README.md) | 3 | A neural network built in Keras and measured against LightGBM, on an ordinary laptop CPU |
| **7** | [NLP, RAG, and LLMs](course7_nlp_and_llms/README.md) | 3 | A covenant extraction tool, run on an indenture it has never seen, with every number checked against the text |
| **8** | [Implementing Agentic AI](course8_agentic_ai/README.md) | 3 | A multi-agent credit desk that writes a morning brief, with every figure traced to the tool that produced it |
| **9** | [Deployment](course9_deployment/README.md) | 3 | The morning brief as a public app: tested on every push, logged, costed, and deployed on free accounts |
| **10** | [Implementing RAG](course10_rag/README.md) | 3 | A question-answering tool over public filings that cites the document and page behind every sentence |
| **Bonus** | [Build Your Own Coding Agent](course_bonus_coding_agent/README.md) | 1 day | A coding agent written from an empty file, deployed to your own private Hugging Face Space |

### A look inside

<table>
  <tr>
    <td width="50%" valign="top"><img src="assets/readme/gallery/c2_price_yield.png" alt="Price against yield for four bonds"><br><sub><b>Course 2</b> · Price and yield</sub></td>
    <td width="50%" valign="top"><img src="assets/readme/gallery/c2_convexity.png" alt="Duration, convexity, and the full reprice"><br><sub><b>Course 2</b> · Duration and convexity</sub></td>
  </tr>
  <tr>
    <td width="50%" valign="top"><img src="assets/readme/gallery/c3_curve_slopes.png" alt="Treasury curve slopes in basis points"><br><sub><b>Course 3</b> · Treasury curve slopes</sub></td>
    <td width="50%" valign="top"><img src="assets/readme/gallery/c4_correlation_heatmap.png" alt="Correlation of daily changes across Treasury tenors"><br><sub><b>Course 4</b> · Correlation across the curve</sub></td>
  </tr>
  <tr>
    <td width="50%" valign="top"><img src="assets/readme/gallery/c5_shap_waterfall.png" alt="One company's model output split by SHAP value"><br><sub><b>Course 5</b> · A model output, by SHAP value</sub></td>
    <td width="50%" valign="top"><img src="assets/readme/gallery/c7_indenture_embeddings.png" alt="An indenture's sections as sentence embeddings"><br><sub><b>Course 7</b> · An indenture, as embeddings</sub></td>
  </tr>
</table>

## How a day works

Each day is one folder with three files of the same name: a short **overview PDF** to read first, the **notebook** to work through top to bottom, and a **solutions notebook** with worked answers.

| Every day has | What it means |
|:---|:---|
| **Desk questions** | Each step starts with a question a colleague would ask, then a few lines of code that answer it. |
| **Excel side by side** | Wherever Excel has a formula or feature for the job, it is shown next to the Python. |
| **Errors on purpose** | Code that fails is run for real, and the error is read line by line. |
| **Checked exercises** | A check cell tells you when your number is right. |
| **The AI check** | The last exercise is code in the style of an AI assistant's answer, with one bug. You find it by knowing what the answer should be. That skill is the point of the series. |

## Coming from Excel

You keep everything you know. The difference is that code keeps the steps, not just the answer, so the same work runs again on tomorrow's file.

| In Excel you would | In Python you will | Course |
|:---|:---|:---:|
| Fill a formula down a column | Write the formula once, in a loop or on a whole array | 1 |
| Use `VLOOKUP` or `INDEX` and `MATCH` | Merge two tables on a shared column | 1 |
| Build a pivot table | Group by a column and summarize | 1 |
| Goal Seek a yield, or use `RATE` and `YIELD` | Write a loop that solves the yield from a price | 2 |

**[All 199 comparisons, course by course](EXCEL.md)**

## Start here

### Run in Google Colab, with nothing to install

> [!TIP]
> 1. **[Day 00: Setup](course1_python_foundations/week1/day00/00_setup_your_computer.ipynb).** Choose Colab or your own Windows computer, with a screenshot of every step.
> 2. **[Day 0: Start Here](course1_python_foundations/week1/day0/0_start_here.ipynb).** What Python, a notebook, and a library are, from zero.
> 3. **[Course 1](course1_python_foundations/README.md#course-map).** Click the **Open in Colab** badge at the top of any notebook. All you need is a Google account.

In Colab, use the course data only. Never upload anything from your employer.

### Run on your own Windows machine

Follow [Day 00](course1_python_foundations/week1/day00/00_setup_your_computer.ipynb), Parts 1 to 4. On a work machine, check your firm's policy before installing anything.

<details>
<summary><b>Already set up with Python 3.13 and VS Code? The short version.</b></summary>

<br>

Tick **Add python.exe to PATH** when you install Python, and run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once so PowerShell can switch the environment on.

```powershell
mkdir $HOME\projects -Force
cd $HOME\projects
git clone https://github.com/lenamonj/python-fixed-income.git
cd python-fixed-income
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
code .
```

No git? Choose **Code**, then **Download ZIP** on this page, and unzip it into `projects`. The full install includes TensorFlow and PyTorch and takes a few gigabytes. For one course only, use that course folder's `requirements.txt`.

</details>

### Keys and accounts

<details>
<summary><b>No notebook needs a key to run. Here is what you can add, course by course.</b></summary>

<br>

| Course | What you can add |
|:---:|:---|
| 1, 2, 4, 5, 5B, 5C, 6 | Nothing. |
| 3 | A free [FRED API key](course3_market_data/README.md#your-fred-key) to pull live data. Without one, every notebook still runs. |
| 7 | A free [OpenRouter key](course7_nlp_and_llms/README.md#your-openrouter-key), or an OpenAI key, for live model requests. Without one, week 3 replays the course's saved responses. |
| 8 | An [OpenAI or OpenRouter key](course8_agentic_ai/README.md#no-key-needed-and-going-live) to run the agents live. Every run is recorded and replays without one. |
| 9 | Free [GitHub, Vercel, and Hugging Face accounts](course9_deployment/README.md#your-accounts) and Docker Desktop to deploy for real. A free Hugging Face account hosts a Space only once it is 30 days old, so create it early. |
| 10 | A [key of your own](course10_rag/README.md#before-you-start) for live answers. Colab's T4 GPU runtime helps the local-model cells and is never required. |
| Bonus | An [OpenAI key](course_bonus_coding_agent/README.md#start-here) for a live agent, and the Hugging Face account from Course 9. |

Keys live in a `.env` file outside the repo or in Colab's Secrets panel, never in a notebook or a commit.

</details>

## The data

Every issuer, ticker, CUSIP, price, position, and trade in the portfolio files is invented. Public files such as Treasury yields, FOMC statements, and SEC filings keep their values and their own terms. Licensed series such as ICE BofA are pulled live with your own FRED key and never stored here. The models describe their data: nothing in the series is a forecast, a rating, or a recommendation. Every file, its source, and its terms are on [the data page](data/README.md).

*This product uses the FRED&reg; API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.*

## License

Code is under the [MIT License](LICENSE). Written content, slide overviews, and videos are under [CC BY 4.0](LICENSE-CONTENT): share and adapt them, including commercially, with credit. Public data files keep their own terms, and the fonts in `assets/fonts` are under the SIL Open Font License.

---

<div align="center">

<h3>Ready? Open <a href="course1_python_foundations/week1/day00/00_setup_your_computer.ipynb">Day 00</a> and get set up.</h3>

Created by **Jeff Lenamon**

</div>
