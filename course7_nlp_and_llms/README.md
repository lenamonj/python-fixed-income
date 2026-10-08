<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="520">
</picture>

![Course 7](https://img.shields.io/badge/Course_7-NLP_and_LLMs-123D2F?style=for-the-badge)
![Length](https://img.shields.io/badge/3_weeks-14_notebooks_%2B_capstone-1C7A57?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[Your OpenRouter key](#your-openrouter-key)** &nbsp;·&nbsp; **[The three weeks](#the-three-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Course 6](../course6_neural_networks/README.md)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 7: NLP and LLMs

**Three weeks from a regular expression on an FOMC statement to a covenant extraction tool that reads a real indenture and checks every number it returns against the text.**

</div>

On day one you pull the target range out of 226 FOMC statements with one regular expression and find the sections and defined terms of a real high yield indenture. Three weeks later you turn text into counts, TF-IDF vectors, word vectors, and sentence embeddings, and say what each one keeps and loses; train a classifier that assigns an 8-K section its item, split by filing date, and catch the leak a section's own heading creates; search an indenture by meaning; read filings the way EDGAR serves them, within the SEC's rules; send a request to a large language model from code with the key kept secret, the tokens counted, and the answer cached; extract an indenture's covenants into a schema with every quoted number checked against the source; and build retrieval that answers only from the indenture and cites the section. Then a colleague asks for a tool that takes an indenture you have never seen and gives back the covenant terms in a table anyone can check.

**That is the course: text read, measured, and extracted with Python, every number traced back to the sentence it came from.**

Every piece of work on a real filing is descriptive extraction: what the document says. Real issuers appear only as the authors of the public documents being read, with a source line under every excerpt. No prompt asks a model for an opinion, a rating, a ranking, or a view about the future, and the course's fixed system prompt instructs the model to reply "REFUSED" to any such request. Two indentures are compared by their numbers and their words, never by a judgement of their terms. A classifier's output on an 8-K section is the item the model assigns, never a signal about the company, and an FOMC score is a count from a stated word list, never a reading of policy.

Every function goes into a sixth module of your own, `textkit.py`, which imports the `mlkit.py` you built in Course 4 and `get_secret` from Course 3's `marketdata.py` and never changes them, with a test file that grows every day.

Four habits run through all of it.

| Habit | What it means |
|:---|:---|
| **Check against the source** | Every quote a model returns is searched for in the cited section of the indenture, and every number in an extracted value is searched for inside its own quote. A value that fails is kept, shown, and marked "not confirmed", never repaired. |
| **Excel as the bridge** | Excel has no tokenizer, no TF-IDF, no embedding model, no transformer, and no worksheet function this course relies on that sends text to a model, and each notebook says so plainly. Then it shows the pieces Excel can do, with the formula beside the Python: word counts by `LEN` and `SUBSTITUTE`, `COUNTIF` with wildcards, `TEXTSPLIT`, `REGEXEXTRACT`, a cosine by `SUMPRODUCT`, a confusion matrix by `COUNTIFS`, and a checked table whose quote check is a formula. |
| **The same answer on every run** | One seed, one thread for the maths libraries and PyTorch, and each list of texts embedded once, so a rerun prints the same digits. Week 3 replays the course's saved responses, so a notebook run with no key prints exactly what the saved notebook shows. |
| **Describe, never judge** | Every output has a plain name and a list of names it is never given. Case studies end with "What the model shows, and where it fails", and every prompt and written description passes a check for words of opinion and words about the future. |

You need Course 6, or the same ground: Course 3's `.env` habits and JSON, Course 4's pipelines, logistic regression, the confusion matrix, K-means and PCA, Course 5's class weights and bootstrap intervals, and Course 6's rule that every run prints the same text. Each notebook writes the reference `mlkit.py` (and from week 3 `marketdata.py` and `bondmath.py`) and the `textkit.py` it starts from into its work folder, so a missing or unfinished module never stops it. This is the seventh course in [Python for Fixed Income](../README.md).

Status: <!-- count:ready -->15<!-- /count --> of <!-- count:total -->15<!-- /count --> notebooks are ready: 14 teaching notebooks and the capstone.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here). Course 7 runs in the same `.venv` as Courses 1 to 6.

| Step | What to do |
|:---|:---|
| **Install the course's packages** | With the course's `.venv` active, run the install line below. It adds PyTorch, transformers, sentence-transformers, the `openai` package, pydantic, beautifulsoup4, pypdf, and pypdfium2 to Course 6's pins, and changes none of them. PyTorch is the large one: its Windows wheel is about 125 MB to download (the CPU build, no extra index needed), and the new packages take about 650 MB once installed. |
| **The Hugging Face cache** | Week 2 runs two small pretrained models on your CPU: a sentence model (`sentence-transformers/all-MiniLM-L6-v2`, about 92 MB) and a zero-shot classifier (`MoritzLaurer/xtremedistil-l6-h256-zeroshot-v1.1-all-33`, about 26 MB). The first notebook that needs one downloads it from huggingface.co into the Hugging Face cache, `~\.cache\huggingface\hub` on Windows (`HF_HOME` moves it), about 118 MB for both; on the course's build machine the first download of each took under 10 seconds. Every later run reads the files from there with no network. `hf cache ls` lists what the cache holds, and `hf cache rm` removes a model (day 6 shows both). |
| **No GPU needed** | Every model runs on the CPU, one thread, within the notebook's time budget. The slow model outputs on all 5,126 8-K sections were computed once and committed; days 7 and 10 recompute a sample live and check it against the file. |
| **An OpenRouter key for week 3** | Weeks 1 and 2 need no key and no account. Week 3 sends requests to large language models through OpenRouter, with a free key of your own. Without a key, every week 3 notebook replays the course's saved responses. See [Your OpenRouter key](#your-openrouter-key). |
| **Keep your folder** | Your `my_bondmath` folder, in your `projects` folder beside the course repo, gains `textkit.py` and its tests beside the earlier modules, and a `cache\llm\` folder that Git ignores. If you skipped the earlier courses, create it with the last line below. |
| **Or use Colab** | Open any notebook in the [course map](#course-map) and click the **Open in Colab** badge. Colab has its own PyTorch: do not install the course's `torch` pin there. Its library versions can differ from the pins, so a printed number may differ in its last digits; the setup cell says so when it happens. Colab's model cache belongs to the runtime, so a new runtime downloads the models again. Put a key in Colab's Secrets panel, never in a cell. At the end of each day, download your files from the Colab file browser. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course7_nlp_and_llms\requirements.txt
python -c "import torch, sentence_transformers; print(torch.__version__)"
New-Item -ItemType Directory -Force "$HOME\projects\my_bondmath" | Out-Null
```

Each notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Each day's "Bring It Home" section shows the PowerShell steps that move the day's functions and tests into `my_bondmath`, run the tests, and commit.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. As in Courses 2 to 6, every notebook ends in the same order: Excel side by side, save the day with Git, bring it home, then the exercises, with the AI check last. Git keeps two logs: each classifier's results, and from week 3 every extracted value with its check results, committed beside the code.

## Your OpenRouter key

Week 3 reaches large language models through [OpenRouter](https://openrouter.ai), a service that passes a request on to the company that runs the model you name. One account and one key reach many models through the request format OpenAI's API uses, so the `openai` Python package works with it after a change of address.

| Question | Answer |
|:---|:---|
| **Where to get one** | Make an account at openrouter.ai, create a key on its Keys page, and copy it. Day 11's "Bring It Home" walks through it. |
| **Where it goes** | In `my_bondmath\.env`, the file Course 3 made for your FRED key, on a line of its own: `OPENROUTER_API_KEY=` followed by the key. In Colab, in the Secrets panel under the same name. Course 3's `get_secret` reads it, and the notebook prints only whether a key loaded. Never in a notebook cell, a prompt, a command line, or the course repo; day 11 checks that Git ignores `.env` before the first request. |
| **What the free models cost** | Nothing. A model whose id ends in `:free` has a price of 0, and the course's default text model is one. The course names a paid fallback, `google/gemini-2.5-flash-lite`, for a student who wants it: at its list price on 2026-10-08, one of day 11's requests cost US$0.000046, and the capstone's 15 requests, at their token counts, would come to about US$0.02. |
| **What limits them** | OpenRouter's [limits page](https://openrouter.ai/docs/api-reference/limits), read on 2026-10-08, sets free models at 20 requests a minute, and at **50 requests a day** for an account that has bought fewer than 10 credits (1,000 a day once it has bought 10). Each week 3 day sends well under 50 requests on its teaching path. A free model's daily cap answers with HTTP 429, and waiting minutes does not clear it. On the day the course recorded days 14 and 15, its account had used its free requests, so those two days were recorded through the OpenAI route; the notebooks say so. |
| **With no key** | Every week 3 notebook runs top to bottom in replay mode: it reads the course's saved responses from `data/course7_llm_responses/` and prints exactly what the saved notebook shows, with "replayed (no key loaded)" in the line under each response. With a key, the notebook sends its requests live, saves each response in its own work folder, and runs the same checks on them; a live response's text can differ from the saved one. |
| **The OpenAI route** | With `OPENAI_API_KEY` in the same `.env`, `textkit.llm_client("openai")` switches the address and the key name and nothing else (day 11). A request on that route goes to your OpenAI account, under OpenAI's prices and limits, which the course did not read. |

## The three weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | Text as data | Clean and split real text with Python and regular expressions, find an indenture's sections and defined terms, weight words by TF-IDF and compare documents by cosine, train a text classifier on 8-K sections split by date and report its rare items, use pretrained word vectors, and describe the wording of 26 years of FOMC statements with a word list and a classifier fitted only on earlier years |
| 2 | Transformers on the CPU | Cut an indenture into chunks and search it by meaning with sentence embeddings, score a zero-shot classifier and an embedding classifier against TF-IDF, cluster 10-K risk factors and describe the clusters, read filings the way EDGAR serves them within the SEC's rules, and open the 8-K test sections once to compare three models with intervals |
| 3 | LLMs and covenant extraction | Send a request to a model from code with the key kept secret and the cost counted, extract an indenture's covenants into a schema and check every quote and number against the text, read baskets and carve-outs and put two indentures fifteen years apart side by side, read a page image, and answer questions from an indenture with citations and a judge |

## Course map

<!-- map:start -->

### Week 1: Text as data

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Text in Python: FOMC Statements and an Indenture](week1/day1/01_text_in_python_fomc_statements_and_an_indenture.ipynb) | Strings, characters that look alike and `normalize_text`, regular expressions that pull the target range out of every statement, `tokenize`, an indenture's sections and defined terms, beside `LEN`, `SEARCH`, `TEXTSPLIT`, and `REGEXEXTRACT` | Ready |
| 2 | [Bag of Words and TF-IDF](week1/day2/02_bag_of_words_and_tf_idf.ipynb) | Counts, IDF and TF-IDF by hand checked against scikit-learn, cosine similarity across statements and across an indenture's covenants, and what a bag of words loses, beside `COUNTIF` with wildcards, IDF by `LN`, and a cosine by `SUMPRODUCT` | Ready |
| 3 | [Classifying 8-K Items with TF-IDF](week1/day3/03_classifying_8k_items_with_tf_idf.ipynb) | What an 8-K is, a split by filing date, the leak a section's own heading creates, a TF-IDF classifier with per-item recall and the rare items reported, and class weights, beside a confusion matrix by `COUNTIFS` on item codes stored as text | Ready |
| 4 | [Word Embeddings](week1/day4/04_word_embeddings.ipynb) | Pretrained GloVe vectors, nearest words, what the vectors miss in an indenture, arithmetic on vectors shown once, and mean vectors as classifier features beside TF-IDF, beside a cosine of two words by `SUMPRODUCT` | Ready |
| 5 | [Case Study: FOMC Statement Tone over Time](week1/day5/05_case_study_fomc_statement_tone_over_time.ipynb) | The course's own word lists, the action each statement states, then a case study: the label's own sentence removed, a dictionary score and a classifier fitted only on earlier years, side by side, beside a dictionary count by `SUMPRODUCT` over named ranges | Ready |

### Week 2: Transformers on the CPU

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Sentence Embeddings and Semantic Search](week2/day1/06_sentence_embeddings_and_semantic_search.ipynb) | Chunks that never cross a section, a sentence model on the CPU and its cache, normalized embeddings, why the last digits depend on the batch, search by meaning against search by words, and word pieces, beside a cosine on 384 pasted numbers | Ready |
| 2 | [Zero-Shot Classification against TF-IDF](week2/day2/07_zero_shot_classification_against_tf_idf.ipynb) | A model that labels text with names it never trained on, label wording, a cached model output checked against a live sample, embeddings as features, and three models side by side, beside the item over a row's largest score by `INDEX` and `MATCH` | Ready |
| 3 | [Clustering 10-K Risk Factors](week2/day3/08_clustering_10k_risk_factors.ipynb) | One embedding per risk factor, K-means with the rule for k stated first, clusters described by their words and their counts per filing, and PCA for a picture, beside `COUNTIFS` of cluster by filing | Ready |
| 4 | [Reading EDGAR](week2/day4/09_reading_edgar.ipynb) | EDGAR's addresses, the SEC's rules for programs, a fetch function tested without the network, HTML to text with the inline XBRL removed, and a 10-K cut into its items, beside `TEXTBEFORE` and `TEXTAFTER` on pasted filing text | Ready |
| 5 | [Case Study: Where the Classifier and the Transformer Disagree](week2/day5/10_case_study_where_the_classifier_and_the_transformer_disagree.ipynb) | Where two models part, ten disagreements read, then a case study: the 2025 test sections opened once, three models compared with paired bootstrap intervals, and what the model shows, and where it fails | Ready |

### Week 3: LLMs and covenant extraction

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [First LLM Request](week3/day1/11_first_llm_call.ipynb) | What a request is, OpenRouter and its free models, the key kept secret, `ask` with its cache and replay, tokens and cost, temperature and seed, failures in plain words, and the OpenAI route, beside a request's cost by formula | Ready |
| 2 | [Covenants 1: The Anatomy of an Indenture](week3/day2/12_covenants_1_the_anatomy_of_an_indenture.ipynb) | Defined terms as the dictionary, the key covenants section by section, a pydantic schema, the first extraction checked quote by quote and number by number, prompt changes one at a time, and five covenants in one checked table, beside a quote check by formula | Ready |
| 3 | [Covenants 2: Baskets, Carve-Outs, and Two Vintages](week3/day3/13_covenants_2_baskets_carve_outs_and_two_vintages.ipynb) | Grower baskets found by a regular expression and by the model, permitted liens and restricted payments, an indenture fifteen years older under the same schema, one comparable table, and a PDF page read as text and as an image | Ready |
| 4 | [RAG over an Indenture](week3/day4/14_rag_over_an_indenture.ipynb) | Why not send the whole indenture, retrieval and a prompt that must cite, ten questions with answers decided first, retrieval scored without the model, a judge that checks grounding, NOT IN TEXT, and the guardrail, beside `MATCH` on a retrieval table | Ready |
| 5 | [Course 7 Capstone](week3/day5/course7_capstone.ipynb) | Your own covenant extraction tool, run on an indenture the course never opened before and then on day 12's, with a checked table, the guardrail, the cost, a workbook, and a written description. A [worked version](week3/day5/course7_capstone_solutions.ipynb) sits beside it | Ready |

<!-- map:end -->

## The capstone

Day 5 of week 3 is yours, and it is more than one sitting: plan on two or three. A colleague on the desk asks for a tool that takes an indenture in and gives back the covenant terms in a table anyone can check: every number beside its section and the sentence it came from, and a flag on anything the checks could not confirm. You run it on an indenture the course has never opened: Lamar Media Corp.'s 2007 indenture for its 6-5/8% Senior Subordinated Notes due 2015, Series C, a different shape from the one you learned on. Thirty-four questions take you from your complete module to a written description. Nothing is planted in the document: its cross-reference table, its housekeeping covenants, its leverage test, and the covenant kinds outside the schema are the work.

You hand in your module with its tests passing, `covenant_tool.py` with a loader, a map of Article 4, an extraction function, a checked table with three statuses (confirmed, not confirmed, not in text), and the whole tool in one function that runs on both indentures; the guardrail, asserted; the requests, tokens, and cost; a workbook whose quote checks are formulas; a Git history with one commit per deliverable; a short log of any AI assistant use; and a written description of what the tool shows and where it fails.

| File | What it is |
|:---|:---|
| [`course7_capstone.ipynb`](week3/day5/course7_capstone.ipynb) | The brief, the questions, and a check cell for every answer that can be checked. A check says correct or not yet, and never shows the answer |
| [`course7_capstone_overview.pdf`](week3/day5/course7_capstone_overview.pdf) | The brief as slides: the scenario, the document, the deliverables, and how the checks work |
| [`course7_capstone_solutions.ipynb`](week3/day5/course7_capstone_solutions.ipynb) | The worked version, with every decision stated. Open it after you finish |

The table you build describes what one public document says. It is not a credit view on the notes or the issuer, and the tool refuses to give one.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| Python's `re`, `unicodedata`, and `collections` | Regular expressions, look-alike characters, and counting | Week 1, Day 1 |
| scikit-learn | `CountVectorizer`, `TfidfVectorizer` inside a pipeline, logistic regression, K-means, PCA, and metrics | Week 1, Day 2 |
| PyTorch, transformers, and sentence-transformers | The sentence model and the zero-shot pipeline, on the CPU | Week 2, Day 1 |
| beautifulsoup4 | HTML to text, for EDGAR's documents | Week 2, Day 4 |
| `openai` | Requests to OpenRouter and to OpenAI | Week 3, Day 1 |
| pydantic | The covenant schema a response must satisfy | Week 3, Day 2 |
| pypdf and pypdfium2 | A PDF's text layer, and a page rendered as an image | Week 3, Day 3 |
| pytest and Git | Testing `textkit.py` every day, and keeping each result and extracted value beside its code | Week 1, Day 1 |
| pandas, matplotlib, and openpyxl | Tables, charts, and workbooks for Excel | Week 1, Day 1 |
| TensorFlow, Keras, XGBoost, LightGBM, and the rest of Course 6's pins | Not used; kept so one environment runs Courses 4 to 7 | |

Exact versions are pinned in [`requirements.txt`](requirements.txt): torch 2.14.1, transformers 5.19.0, sentence-transformers 6.1.0, huggingface-hub 1.33.0, openai 3.26.0, pydantic 2.13.5, beautifulsoup4 4.15.0, pypdf 6.19.0, and pypdfium2 5.14.0 on top of Course 6's pins, among them numpy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1, and pytest 9.1.1. The two Hugging Face models are loaded at pinned revisions, so a later upload to their pages cannot change a notebook's numbers. No framework and no vector database: retrieval over one indenture is a matrix product in numpy, and day 14 says why.

| Data | Kind | Used in |
|:---|:---|:---|
| FOMC post-meeting statements, 226 from 2000-02-02 to 2026-09-16 | Real, public: Board of Governors of the Federal Reserve System, federalreserve.gov, public domain | Days 1, 2, 5, and 11 |
| Boyd Gaming Corporation, indenture for the 4.750% Senior Notes due 2031, Exhibit 4.1 to the 8-K filed 2021-06-08, as filed, with its text and a PDF print made by the course | Real, a public record on sec.gov, quoted for descriptive extraction only | Days 1, 2, 4, 6, 9, and 11 to 14, and the capstone |
| Levi Strauss & Co., indenture for the 8-7/8% Senior Notes due 2016, Exhibit 4.1 to the 8-K filed 2006-03-17 | Real, a public record on sec.gov, quoted for descriptive extraction only | Day 13 |
| Lamar Media Corp., indenture for the 6-5/8% Senior Subordinated Notes due 2015, Series C, Exhibit 4.1 to the 8-K filed 2007-10-16 | Real, a public record on sec.gov, quoted for descriptive extraction only | The capstone only |
| 8-K item sections: 5,126 sections of current reports filed 2019 to 2025, each labelled by the item its filer chose | Real, public records on sec.gov; a sample drawn by the course, the bodies cut at 300 words | Days 3, 4, 7, 9, and 10 |
| Boyd Gaming Corporation's Form 10-K for fiscal 2025, as filed, and 99 Item 1A risk factors from the fiscal 2025 10-Ks of Boyd Gaming Corporation, Levi Strauss & Co., and Lamar Media Corp. | Real, public records on sec.gov | Days 8 and 9 |
| GloVe 6B word vectors, a subset of 44,558 words at 100 numbers each | Real, public domain: Pennington, Socher, and Manning (2014), https://nlp.stanford.edu/projects/glove/, Public Domain Dedication and License v1.0 | Day 4 |
| The two models' outputs on the 8-K sections, and the course's saved LLM responses (66 files) | The course's own, computed once by the course and committed under its MIT license | Days 7, 10, and 11 to 15 |

The 8-K sections are split by filing date: training 2019 to 2023, validation 2024, and the 2025 test sections opened once, on day 10. The rare items are rare in the file by the course's sampling design, and the notebooks say so. Item 5.02 sections name officers and directors; they are counted by item only and no name is printed. The Lamar indenture is never opened before the capstone. Sources, terms, and changes for every file are in [The data](../README.md#the-data) on the front page.

## What comes next

Later courses build on the `bondmath`, `marketdata`, `mlkit`, `ensemblekit`, `netkit`, and `textkit` you wrote in Courses 2 to 7. Course 8, Implementing Agentic AI, is planned next.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
