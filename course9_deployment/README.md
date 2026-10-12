<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="325">
</picture>

[![Course 9](https://img.shields.io/badge/Course_9-Deployment-123D2F?style=for-the-badge)](../README.md)
[![Length](https://img.shields.io/badge/3_weeks-14_notebooks_%2B_capstone-1C7A57?style=for-the-badge)](#course-map)
[![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)](../README.md#run-in-google-colab-with-nothing-to-install)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[Your accounts](#your-accounts)** &nbsp;·&nbsp; **[The three weeks](#the-three-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Course 8](../course8_agentic_ai/README.md)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 9: Deployment

**Three weeks from your first remote to the Course 8 credit desk's brief at a public address, tested on a machine nobody owns, with nothing private on the way.**

</div>

On day one you open the accounts the course uses, give your code a remote of its own, and scan a folder before anything goes public. Three weeks later you work on branches and review every change by its diff, make GitHub run your tests on Linux on every push, list exactly what a server must install, put your own bond math behind a FastAPI service and deploy it to a public URL on Vercel, serve the Course 8 desk's brief as a snapshot with no key on the server, give it a Streamlit page and a Gradio app, host the Gradio app on a Hugging Face Space, package the service in a Docker image, log every request and read latency and errors from the log, measure how far a model's inputs have drifted from its training window, keep every secret in a platform's settings, and put a dollar figure and a free-tier line on the month. Then the desk head asks for the morning brief on a link a colleague can open.

**That is the course: your code in a public repo with tests that run on every change, and a public app that states the date of its figures, refuses a request for a view, holds no key, and costs nothing on the free tiers.**

Deployment means three moves: code goes from your laptop to a shared repository, is tested on a machine nobody owns, and runs on a server strangers can reach. Every notebook runs offline. A remote is a bare repository in the work folder, a service is tested through FastAPI's test client with no port and no network, and one real server is started and stopped inside one cell. The steps that happen on GitHub, Vercel, Hugging Face, and Docker were run once on the course's own accounts and are shown as **masked transcripts**: what the platform printed, with account names, addresses, and ids replaced by `student` and `<id>`, never re-run. You run the same steps yourself, on your own free accounts, from PowerShell.

Every function goes into an eighth module of your own, `deploykit.py`, which imports the `bondmath.py` you built in Course 2 and never changes it, with a test file that grows every day: 48 functions, 8 request and response models, and 63 tests by day 14. It imports nothing heavy at module level, so a deployed service installs FastAPI and nothing else; the desk's modules are imported inside the functions that replay it. The bash of the series appears here for the first time, and only inside files that run on Linux, the workflow YAML and the Dockerfile, each read line by line. You type PowerShell only.

Four habits run through all of it.

| Habit | What it means |
|:---|:---|
| **Nothing private goes public** | `public_scan` runs before every push: no `.env` file, no key-like string, no email but `student@example.com`, no file over the size limit. A deploy folder, a Space folder, and a Docker image each have their own check, and a secret lives in `my_bondmath\.env` or a platform's settings, read by name, never in code. |
| **Every notebook runs offline** | No saved notebook reaches GitHub, Vercel, Hugging Face, Docker Hub, or a model. Cloud steps are masked transcripts, your own steps are PowerShell in "On your own account" cells, and a `live-deploy` cell checks your own deployment only when you give it its address. |
| **Excel as the bridge** | Excel has no remote, no branch, no CI, no server, and no container, and each notebook says so. Where Excel has an honest counterpart it is shown with the formula beside the Python and tested in Excel first: `PRICE` and `MDURATION` against the service, `WEBSERVICE` reading the deployed DV01, `COUNTIFS`, `AVERAGEIFS`, and `PERCENTILE.INC` on a request log, `STANDARDIZE` with `STDEV.S` for drift, `SUMPRODUCT` and `IF` for a cost sheet, and a CSV that turns a CUSIP into a number. |
| **Describe, never judge** | A service returns, refuses, and logs. Nothing deployed predicts, forecasts, recommends, or decides: the desk serves Course 8's brief as of 2026-10-02 and refuses any request for a view at the API, before anything is looked up. |

You need Course 8, or the same ground: Course 2's `bondmath` and Git habits, Course 3's `.env` and `get_secret`, and Course 8's credit desk, which replays from its saved runs with no key. Each notebook writes the reference `bondmath.py` and `marketdata.py`, from day 8 the desk's modules too, and the `deploykit.py` it starts from into its work folder, so a missing or unfinished module never stops it. This is the ninth course in [Python for Fixed Income](../README.md).

Status: <!-- count:ready -->15<!-- /count --> of <!-- count:total -->15<!-- /count --> notebooks are ready: 14 teaching notebooks and the capstone.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here). Course 9 runs in the same `.venv` as Courses 1 to 8.

| Step | What to do |
|:---|:---|
| **Create your Hugging Face account first** | Do it today, before day 1 if you can. A free account can host a Gradio app on a ZeroGPU Space only once its email is verified and it is older than 30 days. At one notebook a day you reach day 10, the Space, about 9 days after day 1, before the account qualifies. Nothing waits on it: every notebook runs offline, and the Space step keeps until your date comes. |
| **Install the course's packages** | With the course's `.venv` active, run the install line below. It adds seven lines to Course 8's pins (`fastapi`, `gradio`, `streamlit`, `uvicorn`, `httpx`, `pyyaml`, `joblib`; the last four were already installed through earlier courses) and changes none of them. Pip adds 21 packages, about 255 MB once installed, most of it `pyarrow` for Streamlit and Gradio itself. |
| **No key needed** | The course sends no request to a model. The desk replays Course 8's saved runs, and the deployed desk holds no key. Your Hugging Face write token goes in `my_bondmath\.env` as `HF_TOKEN` (day 1); the notebooks print only whether it loaded. |
| **Keep your folder** | Your `my_bondmath` folder, in your `projects` folder beside the course repo, gains `deploykit.py` and its tests. The public repos you make (`pfi-bondmath`, `pfi-bond-service`, `pfi-desk-app`) are new, clean folders beside it, built from named files after the scan passes, never `my_bondmath` itself. |
| **Or use Colab** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge. Its library versions can differ from the pins; the setup cell says so when it happens. The platform steps are typed in PowerShell on your own machine. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course9_deployment\requirements.txt
python -c "import fastapi, gradio, streamlit; print('ok')"
New-Item -ItemType Directory -Force "$HOME\projects\my_bondmath" | Out-Null
```

Each notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Each day's "Bring It Home" section shows the PowerShell steps that move the day's functions and tests into `my_bondmath`, run the tests, and commit, and, where the day ships something, the steps on your own accounts.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. As in Courses 2 to 8, every notebook ends in the same order: Excel side by side, save the day with Git, bring it home, then the exercises, with the AI check last.

## Your accounts

Every account the course uses is free, and no lesson asks for a card. Each platform's free tier was read on its own page on 2026-10-12; platforms change their terms, and the page wins.

| Account | Free, as read on 2026-10-12 | What the course uses it for | Never required |
|:---|:---|:---|:---|
| **GitHub** | Public repositories; GitHub Actions free on public repositories with standard GitHub-hosted runners | Week 1: your public repos, pull requests, and your tests run on Linux on every push; the capstone's repo and CI; a scheduled workflow (day 14) | A paid plan; Windows runners |
| **Vercel** (Hobby) | Free, for non-commercial personal use only; 1,000,000 function invocations, 4 hours of active CPU, and 100 GB of fast data transfer a month; 100 deployments a day | Week 2: the bond service at a public URL (day 7), the desk's snapshot service (day 8), and the capstone, through Vercel's GitHub import in the browser | Pro; the Vercel CLI, shown once |
| **Hugging Face** | The account; up to 2 Gradio Spaces on ZeroGPU for a free personal account with a verified email that is older than 30 days, 5 GPU minutes a day | Day 1: the account and a write token. Day 10: the desk's Gradio app on a Space, once your account qualifies; optional in the capstone | PRO; a CPU or Docker Space |
| **Docker Desktop** | Docker Personal, US$0, an install on your own machine (Windows runs it through WSL 2) | Day 11: one image of the bond service, built and run on your machine | A Docker Hub push; any paid plan |

Deploy the course's synthetic examples only. Deploying anything at work goes through your firm's own process: Vercel's Hobby plan is personal and non-commercial by its own terms, and Docker's licence states whether Docker Desktop without a paid plan covers you at work. Read Docker's own pages before you install it on a work machine.

**What never goes public.** No `.env` file and no token, in a repo, an image, a log, a screenshot, or a command line; no personal email in a public commit (GitHub's private noreply address, set on day 1); no request body, query, header, or client address in a request log; no firm code, data, or position; and never `my_bondmath` itself, whose history holds exercise files and Course 3's leak drill.

### The free route and the paid route

| Platform | The free route | The paid route, named and never needed |
|:---|:---|:---|
| GitHub | Public repos, Actions on public repos | Private repos past 2,000 Actions minutes a month on GitHub Free |
| Vercel | Hobby, personal and non-commercial; a project past a limit is paused for 30 days, not billed | Pro, for commercial use |
| Hugging Face | Two ZeroGPU Gradio Spaces on a free account older than 30 days | PRO, US$9 a month, for a CPU Gradio Space or a Docker Space; Jobs, US$0.01 an hour on `cpu-basic` with a credit balance |
| Docker | Docker Personal and Docker Desktop on your own machine | A paid plan where Docker's licence requires one |
| Render | Named once (day 11) as where an image could go public for free: spins down after 15 minutes without traffic, 750 instance hours a month | Never used |
| Streamlit Community Cloud | Named once (day 9) as Streamlit's free host, linked to your GitHub repos | Never used |

## The three weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | Git and GitHub in depth, and CI | Push your code to a remote after a scan that proves nothing private goes with it, work on a branch, merge two ways and resolve a conflict, review a pull request by its diff, make GitHub Actions run your tests on Linux and read its log when it fails, list what a server must install and why the desk ships as a snapshot, and follow one change to `bondmath` through a red run and a green one |
| 2 | Serving | Put `bondmath` behind a FastAPI service with typed requests, test it without a network, deploy it to Vercel and check it against `bondmath` on your machine, serve the Course 8 desk's brief with no key on the server and refuse a request for a view at the API, give it a Streamlit page and a Gradio app, and host the Gradio app on a Hugging Face Space |
| 3 | Keeping it running | Package the service in a Docker image with `.env` kept out, log every request without its body, read requests, errors, and p95 latency by rule, keep a model as a file with its card and measure its inputs against its training window, keep secrets in platform settings, and meter a month against the free tiers, then ship the desk's brief as a public app in the capstone |

## Course map

<!-- map:start -->

### Week 1: Git and GitHub in depth, and CI

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Deployment and Your Accounts](week1/day1/01_deployment_and_your_accounts.ipynb) | What deployment is, the free route as read on each platform's page, your GitHub and Hugging Face accounts (the 30-day rule), what `origin` is, a remote of your own, `public_scan` before anything goes public, the first push to GitHub, and a log masked before you share it. Excel has no counterpart today | Ready |
| 2 | [Branches and Pull Requests](week1/day2/02_branches_and_pull_requests.ipynb) | Branches beside `main`, a fast-forward and a merge commit, a conflict on purpose resolved by reading both sides, a pull request on GitHub, a review by diff, three ways to merge, and deleting merged branches. Excel has no counterpart today | Ready |
| 3 | [CI with GitHub Actions](week1/day3/03_ci_with_github_actions.ipynb) | A workflow that runs your tests on Linux on every push, the first bash of the series read line by line, YAML's traps (`3.10` read as `3.1`), Linux against Windows, a matrix of two Pythons, the course's two red runs and one green, and secrets in CI. Excel has no counterpart today | Ready |
| 4 | [What the Server Installs](week1/day4/04_what_the_server_installs.ipynb) | `requirements_for` from a file's imports, `installed_size` with dependencies, Vercel's 500 MB limit, `pins_check`, four Pythons, and why the desk ships as a snapshot, beside the size tables totalled by `SUM` and judged by `IF` | Ready |
| 5 | [Case Study: bondmath through CI](week1/day5/05_case_study_bondmath_through_ci.ipynb) | The course's CI runs as a table and a pass rate, then a case study: a public repo, three scans empty, a pull request that breaks DV01, a red run on Linux, the fix, a green run, the merge, and what the deployment shows, and where it fails, beside the runs counted by `COUNTIFS` | Ready |

### Week 2: Serving

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [FastAPI: A Bond Math Service](week2/day1/06_fastapi_a_bond_math_service.ipynb) | Request and response models with units in their names, `bond_app` over `bondmath`, the test client with no port, a bad request as a 422 naming its field, one real server started and stopped in a cell, and five bonds through the service, beside `PRICE`, the accrued from `COUPDAYBS` over `COUPDAYS`, the DV01 from `MDURATION`, and `WEBSERVICE` on `/health` | Ready |
| 2 | [Deploying the Service to Vercel](week2/day2/07_deploying_the_service_to_vercel.ipynb) | A deploy folder built by code, `check_deploy_folder` before it leaves, the Hobby plan as read, deploying it yourself, the course's own deploy as recorded, `check_live` against `bondmath`, and a deploy log, beside the deployed DV01 read into a worksheet by `WEBSERVICE` | Ready |
| 3 | [The Credit Desk as a Service](week2/day3/08_the_credit_desk_as_a_service.ipynb) | The Course 8 desk without a key, why a snapshot, `desk_snapshot` with the hash of every saved exchange, `desk_app` with its date on every figure, the live switch shown by its names only, the guardrail at the API, and the deploy, beside the capstone's recording priced by `SUMPRODUCT` | Ready |
| 4 | [Streamlit and Gradio Front Ends](week2/day4/09_streamlit_and_gradio_front_ends.ipynb) | Two pages over the same functions and the same snapshot, chat basics, a Gradio app built and never launched, a Streamlit script run in `AppTest`, and launching from PowerShell, beside a CSV download opened in Excel and a CUSIP turned into a number | Ready |
| 5 | [Case Study: The Desk on a Hugging Face Space](week2/day5/10_case_study_the_desk_on_a_hugging_face_space.ipynb) | What a Space is and what is free today, `space_folder` and its checks, then a case study: the course's own Space from creation to deletion as recorded, and what the deployment shows, and where it fails. Excel has no counterpart today | Ready |

### Week 3: Keeping it running

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Docker: One Image Everywhere](week3/day1/11_docker_one_image_everywhere.ipynb) | What an image is, the Dockerfile line by line, `.dockerignore` and `check_dockerfile`, Docker Desktop on Windows, the course's build, run, request, and stop as recorded, and where an image could go public. Excel has no counterpart today | Ready |
| 2 | [Request Logs and Monitoring](week3/day2/12_request_logs_and_monitoring.ipynb) | What to log and what never to, `log_middleware` on a fake clock, the log on a platform, a month of requests by `log_summary`, three percentiles that differ, and alerts by rule, beside the log summarised by `COUNTIFS`, `AVERAGEIFS`, `PERCENTILE.INC`, and `PERCENTILE.EXC` | Ready |
| 3 | [Model Files and Drift](week3/day3/13_model_files_and_drift.ipynb) | A fitted model as a file with a card and its hash, the model behind an endpoint, the held-out days arriving as requests, drift against the training window, flags, and what drift does not say, beside the z-score by `STANDARDIZE` with `STDEV.S` and the outside count by `COUNTIFS` | Ready |
| 4 | [Secrets, Limits, and a Cost Meter](week3/day4/14_secrets_limits_and_a_cost_meter.ipynb) | One secrets method end to end, every name the code reads in `.env.example`, where each platform keeps secrets, a leaked token, the free-tier limits as read, what a live desk would cost, a daily cap, and scheduled work for free, beside the cost by `SUMPRODUCT` and the status by `IF` | Ready |
| 5 | [Course 9 Capstone](week3/day5/course9_capstone.ipynb) | Ship a model as a public app: the desk's brief at a public address with its date on every response, the checks it passed, every request for a view refused, no key, a public repo with CI, a request log, a cost line, a workbook, and a written description. A [worked version](week3/day5/course9_capstone_solutions.ipynb) sits beside it | Ready |

<!-- map:end -->

## The capstone

Day 5 of week 3 is yours, and it is more than one sitting: plan on two or three. The desk head wants the morning brief on a link a colleague can open: it has to say what date its figures are from, show the checks it passed, refuse anything that asks it for a view, and never hold a key, with the code in a public repo whose tests run on every change, a log of every request with latency and errors, and a line on what it costs each month and where the free tier stops. Thirty-three questions take you from your complete module to a written description.

You build `desk_app_main.py`: the desk's snapshot service, rebuilt from Course 8's saved runs with every exchange hash checked, a daily cap, the as-of date on every response, and a request log to standard output on the platform. Then you test every endpoint, find the fake key planted in the starter folder before any scan passes, write the repo's files and its CI, push your public repo `pfi-desk-app`, import it on Vercel, check the deployment against the app on your machine, read the platform's log, meter the month against the free tiers, write a workbook whose checks are formulas, and keep a Git history with one commit per deliverable, a pull request read by its diff, and the tag `course9`.

| File | What it is |
|:---|:---|
| [`course9_capstone.ipynb`](week3/day5/course9_capstone.ipynb) | The brief, the questions, and a check cell for every answer that can be checked. A check says correct or not yet, and never shows the answer |
| [`course9_capstone_overview.pdf`](week3/day5/course9_capstone_overview.pdf) | The brief as slides: the scenario, the app, the deliverables, and how the checks work |
| [`course9_capstone_solutions.ipynb`](week3/day5/course9_capstone_solutions.ipynb) | The worked version, with every decision stated and the course's own deploy read as masked transcripts. Open it after you finish |

The app describes public documents, a public curve, and a synthetic book, as of 2026-10-02 in the course's files. It is not a view on any security, issuer, or rate, and it refuses to give one.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| Git, and the GitHub CLI if you have it | Remotes, branches, pull requests, and tags; `gh` is optional, every step also works in the browser | Week 1, Day 1 |
| pytest | Testing `deploykit.py` every day, with temporary folders, bare repositories, and the test client, never the network | Week 1, Day 1 |
| PyYAML | Reading a workflow file the way GitHub reads it | Week 1, Day 3 |
| GitHub Actions | Your tests on Linux on every push and pull request, Python 3.12 and 3.13 | Week 1, Day 3 |
| pandas, openpyxl | CI histories, size tables, request logs, drift tables, cost sheets, and workbooks for Excel | Week 1, Day 4 |
| FastAPI and its test client | The bond service, the desk's snapshot service, and the capstone's app | Week 2, Day 1 |
| uvicorn | The one real server of day 6, and the server inside the Docker image | Week 2, Day 1 |
| Vercel | The public URL of the bond service, the desk service, and the capstone | Week 2, Day 2 |
| Course 8's `agentkit` and `credit_desk` | The desk's brief, replayed from its saved runs with no key | Week 2, Day 3 |
| Streamlit and Gradio | Two front ends over the same functions, tested without a browser | Week 2, Day 4 |
| Hugging Face Spaces and `huggingface_hub` | The desk's Gradio app on a ZeroGPU Space, from a script that reads your token from `.env` | Week 2, Day 5 |
| Docker Desktop | One image of the bond service, built and run on your machine | Week 3, Day 1 |
| scikit-learn and joblib | Course 4's same-day 30 Yr task as a model file with its card | Week 3, Day 3 |

Exact versions are pinned in [`requirements.txt`](requirements.txt): fastapi 0.143.0, gradio 6.30.0, streamlit 1.65.0, uvicorn 0.54.0, httpx 0.28.1, pyyaml 6.0.3, and joblib 1.6.0 on top of Course 8's pins, among them pandas 3.0.6, pydantic 2.13.5, openai-agents 0.23.1, and pytest 9.1.1. A deployed folder has its own small requirements file: the bond service and the desk's snapshot service install `fastapi==0.143.0` alone, about 9 MB on Linux, where replaying the desk on a server would install about 5.7 GB.

| Data | Kind | Used in |
|:---|:---|:---|
| `course9_request_log.csv`: 19,664 requests to a bond and desk service over 30 days, 2026-09-03 to 2026-10-02 UTC | **Synthetic**: invented by the course, no real service, client, or request; three features planted for the lessons (a slow day on `/dv01`, a burst of 422s from one malformed client, a refused share on `/ask`) | Days 12 and 14, and the capstone |
| `course9_transcripts/`: 75 masked transcripts in 11 day folders, recorded 2026-10-12 | The course's own, MIT with the code: what GitHub, Vercel, Hugging Face, and Docker printed when the course ran the steps on its own accounts, account names, addresses, and ids masked | Days 1, 2, 3, 5, 7, 8, 10, 11, 12, and 14, and the capstone |
| `course8_agent_runs/day15/`: 59 saved exchanges of Course 8's capstone desk | The course's own, MIT with the code; recorded once in Course 8 and replayed with no key | Days 8, 9, 10, and 14, and the capstone |
| `course8_eval_set.csv`: 30 desk questions with answer keys decided before any request | The course's own, MIT with the code (Course 8) | Days 8, 9, 10, and 14, and the capstone |
| `holdings.csv`: 200 bonds as of 2026-09-30 | **Synthetic**: invented issuers and invented CUSIPs (Course 1) | Days 6, 8, 9, and 10, and the capstone |
| `treasury_par_yields.csv`: 2,940 days of U.S. Treasury daily par yield curve rates, 2015-01-02 to 2026-10-02 | Real, public: U.S. Department of the Treasury, public domain | Day 13 |
| `bondmath_excel_reference.csv` and `bondmath_excel_reference_tvm.csv`: 306 and 153 cases | Excel's own results for Course 2's bond math, which the tests that run on GitHub compare with | Days 1, 3, and 5 |

No student's deployment, no request log from a real service, no desk snapshot, no model file, no Docker image, and no token is in the repo: each notebook rebuilds the snapshot and the model from the committed files. The guardrail in one sentence: nothing deployed predicts, forecasts, recommends, or decides; the desk serves a 2026-10-02 snapshot of Course 8's descriptive brief and refuses a request for a view. Sources, terms, and changes for every file are in [The data](../README.md#the-data) on the front page.

## What comes next

Later courses build on the `bondmath`, `marketdata`, `mlkit`, `ensemblekit`, `netkit`, `textkit`, `agentkit`, and `deploykit` you wrote in Courses 2 to 9. Next comes [the Bonus course, Build Your Own Coding Agent](../course_bonus_coding_agent/README.md), which closes the series. It deploys its app to a ZeroGPU Space of your own, with the Hugging Face account and token you set up on day 1 of this course, once the account is older than 30 days.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
