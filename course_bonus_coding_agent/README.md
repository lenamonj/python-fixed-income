<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="325">
</picture>

[![Bonus](https://img.shields.io/badge/Bonus-Build_Your_Own_Coding_Agent-123D2F?style=for-the-badge)](../README.md)
[![Length](https://img.shields.io/badge/1_notebook-2_or_3_sittings-1C7A57?style=for-the-badge)](#course-map)
[![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)](../README.md#run-in-google-colab-with-nothing-to-install)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Start here](#start-here)** &nbsp;&middot;&nbsp; **[The lesson](#the-lesson)** &nbsp;&middot;&nbsp; **[Course map](#course-map)** &nbsp;&middot;&nbsp; **[The app](#the-app)** &nbsp;&middot;&nbsp; **[What it uses](#what-it-uses)** &nbsp;&middot;&nbsp; **[The data](#the-data)** &nbsp;&middot;&nbsp; **[Course 9](../course09_deployment/README.md)** &nbsp;&middot;&nbsp; **[Series front page](../README.md)**

## Bonus: Build Your Own Coding Agent

**One notebook from an empty file to a coding agent of your own: one model, one loop, three tools, a fence around one folder, a chat page with your name on it, and a private Space to put it on.**

</div>

You write a coding agent in plain Python, one cell at a time. It reads, lists, and edits files in one workspace folder, and nothing outside it. You ask it to solve a riddle in a file, to list the high yield bonds in a CSV, and to write a bond pricing function, then you check the function it wrote against 100.0, 97.3270, and 2.6956 before you trust it. Then you give it a Gradio chat page that shows every tool request as a step, put your own product name on it, and deploy it to a private ZeroGPU Space on your own Hugging Face account, with the key held as a Space secret.

**That is the course: an agent you can read top to bottom in one file, `coding_agent.py`, that runs no code, describes only what its files hold, and refuses any request for a view before a request is sent.**

The model is OpenAI's `gpt-6.1-sol` on the Responses API. Course 8 taught the agent loop on Chat Completions; section 2.3 sends the same question both ways and names every field that changed. Every request in the notebook was recorded once by the course and replays from the repo with no key, through Course 8's transport. Every Hugging Face step was run once on the course's own account and is shown as a masked transcript, as in Course 9. The notebook runs top to bottom, offline, for free.

Four habits run through it.

| Habit | What it means |
|:---|:---|
| **One folder** | Every path the model gives goes through `resolve_in_workspace`: resolved first, then refused unless it is inside the workspace. `../.env`, `C:\Windows\win.ini`, `/proc/self/environ`, and a sibling folder whose name starts with the workspace's are all refused. |
| **No code runs** | The agent has exactly three tools, `read_file`, `list_files`, and `edit_file`. None runs code, a shell, or an import. When the agent writes Python, you read it, and you run it in a cell of your own. |
| **Excel as the bridge** | Excel has no loop, no tool, and no model, and the notebook says so. Where Excel can check the agent's work, the formula sits beside the Python, tested in Excel first: `FILTER` on the bonds file, `PV` and `MDURATION` against the agent's own bond math, `COUNTIFS` on the tool log, and `SUMPRODUCT` for the bill. |
| **Describe, never judge** | The workspace holds six fictional bonds and a riddle. The agent describes what the files hold; a message that asks for a view on any bond, issuer, price, or yield gets one refusal line and no request. |

You need Courses 8 and 9, or the same ground: Course 8's `agentkit` and its replay of saved runs, and Course 9's `deploykit`, its masked transcripts, and the Hugging Face account and write token from Course 9's day 1. The notebook's setup cell writes the earlier modules it imports into its work folder, so a missing or unfinished module never stops it. This is the Bonus course of [Python for Fixed Income](../README.md).

Status: <!-- count:ready -->1<!-- /count --> of <!-- count:total -->1<!-- /count --> notebook is ready.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Start here

Setup is on the [series front page](../README.md#start-here). The Bonus course runs in the same `.venv` as Courses 1 to 9.

| Step | What to do |
|:---|:---|
| **Nothing new to install** | The course's [`requirements.txt`](requirements.txt) is Course 9's file, unchanged. If you installed Course 9, you are done. If not, run the install line below. |
| **No key needed** | With no key, every request replays the course's saved responses, and the notebook prints exactly what is saved in it. It prints `OpenAI key loaded: False. Mode: replay.` and never a key, its length, or its last characters. |
| **Your OpenAI key, to go live** | Put `OPENAI_API_KEY=` and your key in `my_bondmath\.env`, the file Course 3 started. The same cells then send live requests, which you pay for, and the model's wording will differ from the saved run. Section 8.7 prices the saved run of sections 2 to 8 at OpenAI's list price as read on 2026-10-12: US$0.0433. Keep the setup cell's product name, Desk Coder, in replay; put your own in when you go live. |
| **Your Hugging Face account** | The one from Course 9, day 1, with a verified email and a write token after `HF_TOKEN=` in `my_bondmath\.env`. A free account may host a Gradio app on a ZeroGPU Space only once it is older than 30 days, and at most two such Spaces. Nothing waits on it: the Space is the last step, and the rest of the notebook needs no account. |
| **Or use Colab** | Open the notebook in the [course map](#course-map) and click the **Open in Colab** badge. Its library versions can differ from the pins; the setup cell says so when it happens. The deploy step is typed in PowerShell on your own machine. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course_bonus_coding_agent\requirements.txt
python -m pip check
```

The notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Its "Bring It Home" section copies `coding_agent.py`, its tests, and `deploy_space.py` into `my_bondmath`. The day folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. Plan on two or three sittings.

## The lesson

| Part | What you do |
|:---:|:---|
| 0 | What you will have, the model, the loop, and the tools, what it costs, and what never goes into the workspace |
| 1 | Keys as environment variables in `my_bondmath\.env`, checked as loaded or not, and the module's settings |
| 2 | A first request on the Responses API, its output items and token counts, and the same request as Chat Completions beside it |
| 3 | Two requests that forget each other, and a conversation kept as a list: the memory and the cost |
| 4 | A tool faked by hand, to show that the model asks and your code does the work |
| 5 | The workspace seeded with fictional files, and the fence tried on five paths: the bond file allowed, four escapes refused |
| 6 | `read_file`, its schema, the system prompt with its no-views lines, and the agent loop with a round limit and a rollback; the agent solves the riddle |
| 7 | `list_files`; the agent lists the high yield bonds in `bonds.csv` |
| 8 | `edit_file`; the agent writes `bond_math.py` and adds modified duration, you check it, three requests for a view are refused with no request, and the run is priced |
| 9 | A Gradio chat page with every tool request as a step, driven without a browser, then launched from PowerShell |
| 10 | Your own product name, and an honest answer to what powers it |
| 11 | The Space: three files written by the module, the configuration read key by key, the key as a secret, the deploy script, and the course's own Space as masked transcripts |
| 12 | What commercial coding agents add, and each extension with its risk |

The notebook closes as every course does: Excel side by side, save the day with Git, bring it home, then five exercises with the AI check last. The AI check is a fence that tests a path as a string and lets a sibling folder through.

## Course map

<!-- map:start -->

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Build Your Own Coding Agent](week1/day1/01_build_your_own_coding_agent.ipynb) | A coding agent from an empty file on the Responses API: three tools, a fence around one folder, a loop with a round limit and a rollback, a refusal rule, a chat page, and a private ZeroGPU Space of your own, beside `FILTER`, `PV`, `MDURATION`, `COUNTIFS`, and `SUMPRODUCT` checking the agent's work. A [worked version](week1/day1/01_build_your_own_coding_agent_solutions.ipynb) of the exercises sits beside it | Ready |

<!-- map:end -->

## The app

| Item | What it is |
|:---|:---|
| [`deploy/`](deploy/) | The three files a Space receives, written by the module's own `space_files` and committed as the course left them: [`app.py`](deploy/app.py) (a ZeroGPU placeholder, the whole of `coding_agent.py`, and the launch lines), [`requirements.txt`](deploy/requirements.txt) (`openai==3.26.0` alone; the Space installs Gradio from the README), and [`README.md`](deploy/README.md) (the Space's configuration, with no key in it) |
| Its name | Yours. `PRODUCT_NAME` is read from the environment, so the page's title, its heading, and the system prompt carry the name you set; the course's placeholder is Desk Coder and its renaming example is Coupon Clerk. Asked what powers it, the app says it runs on an OpenAI model |
| Your Space | `deploy_space.py`, written in section 11.6 and run by you from PowerShell, writes the three files, creates a **private** Gradio Space on ZeroGPU, copies your key from `.env` into the Space's secret in code, sets the name and the model as two variables, uploads, and prints the stage until it runs. Making it public is left as text with three conditions first: a monthly budget on the OpenAI project, a key made only for this app, and a password |
| The course's own Space | Created once on the course's account to record the transcripts, sent three requests (the riddle, `/proc/self/environ`, `../app.py`), and deleted the same day. It showed that a ZeroGPU Space with no `@spaces.GPU` function stops at a runtime error, so the placeholder stays |

Nothing on the Space runs a workspace file. Free hardware sleeps when unused, its disk is not persistent, and every visitor shares one workspace; the notebook says so before you deploy.

## What it uses

| Tool | Used for |
|:---|:---|
| `openai` and the Responses API | Every request to the model, with tools in the flat Responses shape, `store` false, and one tool at a time |
| Course 8's `agentkit` | `desk_client`, which replays every saved request with no key and goes live with yours; `body_diff` for the side by side of the two APIs |
| Course 9's `deploykit` | `check_space_folder` and `public_scan` on the Space's folder, `secret_names`, `space_status`, and the masked transcripts |
| Gradio | The chat page, built and driven as a function in the notebook, launched only from PowerShell |
| `huggingface_hub` | The deploy script: the private Space, its secret and variables, the upload, and the stage |
| pytest | `test_coding_agent.py`, which grows beside the module: the fence, the tools, the loop on scripted responses, the refusal rule, and the page's handler |
| Course 4's `plotkit.py` with matplotlib and pandas Styler (jinja2) | Every run shown: the tokens of each request as bars, the cost per task, the tool requests by tool with the refused ones beside them, the Space's build steps and stages from the masked log, and a formatted table under each comparison |

Exact versions are pinned in [`requirements.txt`](requirements.txt), Course 9's file: openai 3.26.0, gradio 6.30.0, huggingface-hub 1.33.0, python-dotenv 1.2.4, and pytest 9.1.1 among them. `coding_agent.py` imports only the standard library, `openai`, and `gradio`, so the same text runs on your machine and on a Space.

## The data

| Data | Kind | Used in |
|:---|:---|:---|
| The workspace: `README.txt`, `desk_riddle.txt`, and `bonds.csv` with 6 bonds, written by the module at run time | **Fictional**, labelled fictional in the folder: six invented issuers from Alpha Rail to Foxtrot Steel, no CUSIP, no real issuer | Every section, and the Space |
| `bonus_agent_runs/`: 29 saved exchanges with OpenAI's Responses API on `gpt-6.1-sol`, recorded 2026-10-12 | The course's own, MIT with the code: every request the two notebooks send and its response, recorded once and replayed with no key; no key, no header, and no account identifier stored | The notebook and its solutions |
| `bonus_transcripts/`: 7 masked transcripts, recorded 2026-10-12 | The course's own, MIT with the code: what Hugging Face printed when the course created its private Space, built it, sent three requests, ran it once without the placeholder, and deleted it, with account names, addresses, and ids masked | Section 11 |

No workspace, no Space, no key, and no `.env` is in the repo. The guardrail in one sentence: the agent never leaves its workspace folder, never runs code, and never gives a view on any bond, issuer, price, or yield. Sources and terms for every file are in [the data page](../data/README.md).

## Credit

The idea and the three tools come from Thorsten Ball, ["How to Build an Agent"](https://ampcode.com/notes/how-to-build-an-agent) (April 15, 2025), which builds the same agent in Go. This course writes every sentence and every cell fresh, in Python, on OpenAI's Responses API.

## What comes next

The series ends here. You have built `bondmath`, `marketdata`, `mlkit`, `ensemblekit`, `netkit`, `textkit`, `agentkit`, `deploykit`, and now `coding_agent` in Courses 2 to 9 and the Bonus course. Course 10, Implementing RAG, is in progress.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
