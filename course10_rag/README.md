<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme/wordmark-dark.png">
  <img src="../assets/readme/wordmark-light.png" alt="Python for Fixed Income" width="325">
</picture>

[![Course 10](https://img.shields.io/badge/Course_10-Implementing_RAG-123D2F?style=for-the-badge)](../README.md)
[![Length](https://img.shields.io/badge/3_weeks-14_notebooks_%2B_capstone-1C7A57?style=for-the-badge)](#course-map)
[![Python](https://img.shields.io/badge/Python-3.13-1C7A57?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Google%20Colab-0EA5E9?style=for-the-badge)](../README.md#run-in-google-colab-with-nothing-to-install)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-22C55E?style=for-the-badge)](../LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC_BY_4.0-22C55E?style=for-the-badge)](../LICENSE-CONTENT)

**[Before you start](#before-you-start)** &nbsp;·&nbsp; **[The three weeks](#the-three-weeks)** &nbsp;·&nbsp; **[Course map](#course-map)** &nbsp;·&nbsp; **[The capstone](#the-capstone)** &nbsp;·&nbsp; **[What it uses](#what-it-uses)** &nbsp;·&nbsp; **[Course 9](../course9_deployment/README.md)** &nbsp;·&nbsp; **[Series front page](../README.md)**

## Course 10: Implementing RAG

**Three weeks from five questions a model cannot answer about a 10-K to a question-answering tool over a folder of public filings, where every sentence names the document and page it came from and the tool says so when the folder does not hold the answer.**

</div>

On day one you ask a model five questions about a company's debt with no document in front of it, then with a careful prompt, and grade all ten answers against keys written first from the filing: none matches. Three weeks later you load that filing as pages and items, split it with a recursive splitter whose size and overlap you set, embed the chunks with a pinned model and search them exactly with NumPy and with FAISS, add BM25 keyword search and fuse the two lists, rerank with a cross-encoder, tune one setting at a time on development questions and report once on held-out ones, filter by metadata across four documents, demand a citation after every sentence and reject the answer that has none, measure recall and MRR on a labelled question set, put an LLM judge beside a strict grader and see what it misses, refresh the index when a new filing arrives, serve the retriever behind a FastAPI service, and put a dollar figure on a thousand answers. Then a colleague asks for a tool that answers questions of the filings folder with answers they can check.

**That is the course: retrieval-augmented generation built by hand on real public filings, every answer cited or refused, every step measured, and no view on any issuer or security.**

RAG means three moves: find the passages of a document that bear on a question, hand only those to a model, and ask it to answer from them with citations or say the document does not hold the answer. The course builds each move itself, in plain NumPy and pandas first and the libraries second, on one document for most of three weeks: Boyd Gaming's Form 10-K for fiscal 2025, printed to PDF by the course so that a page is what a citation names. A multi-document corpus (the 10-K and three indentures) arrives in week 2, and the company's next 10-Q in week 3, for the lesson on a corpus that changes.

Every function goes into a ninth module of your own, `ragkit.py`, which imports the `textkit.py` you built in Course 7 and never changes it, with a test file that grows every day: 57 functions, 4 small classes, and 65 tests by day 14. Every generated answer and every judge verdict in the course was recorded once on the author's key and is **replayed** from the committed files, byte for byte, so no key is needed to run any notebook; a key of your own makes the same cells live. The local-model route (a 7B model in GGUF through `llama-cpp-python`) is taught in cells marked `t4-only`, which run on Colab's T4 GPU runtime and print a skip line everywhere else.

Four habits run through all of it.

| Habit | What it means |
|:---|:---|
| **Cite or refuse** | Every sentence of an answer ends with a citation to a chunk that was sent, in the form `[boyd10k; Item 7; p. 37; c0412]`; `check_citations` rejects an answer that does not, and a question the corpus does not answer returns exactly `NOT IN CORPUS`. A request for a view is refused before anything is retrieved, and no request is sent for it. |
| **Keys written first, held-out questions opened once** | The 75 questions and their answer keys were written from the documents' pages before any request. Choices are made on the development questions; the test questions are opened once on day 11 and the capstone's own set only in the capstone. |
| **Excel as the bridge** | Excel has no tokenizer, embedding model, vector index, BM25, reranker, or LLM, and each notebook says so. Where it has an honest counterpart it is shown with the formula beside the Python and tested in Excel first: `LEN` and `SUBSTITUTE` on a chunk table, `RIGHT` and `LEFT` for an overlap, `SUMPRODUCT` over `SQRT(SUMSQ())` for a cosine, a BM25 weight with `LN`, reciprocal rank fusion with `SUMIFS`, `ISNUMBER(MATCH())` for recall, `AVERAGE(IFERROR(1/MATCH()))` for MRR, `COUNTIFS` and Cohen's kappa written out, `AVERAGEIFS` and `SORTBY` on a tuning grid, and `SUMPRODUCT` for a cost sheet. |
| **Describe, never judge** | An answer states what a filing says and the date its figure stands at; a sentence the filing writes about its own expectations is quoted as the issuer's. Nothing predicts, forecasts, recommends, ranks, or decides. Real issuers appear only as the authors of their public documents. |

You need Course 7, or the same ground: Course 7's `textkit` (text normalisation, embeddings, EDGAR, the LLM client) and Course 3's `.env` and `get_secret`. The course follows Course 7 day 14 directly and can be taken right after Course 7; Course 8's recording transport is written into each notebook from its saved files and explained in one paragraph, and only day 14 uses Course 9's FastAPI pattern, which it introduces as new. Each notebook writes the reference `textkit.py`, `agentkit.py`, and the other earlier modules, and the `ragkit.py` it starts from, into its work folder, so a missing or unfinished module never stops it. This is the tenth course in [Python for Fixed Income](../README.md); the Bonus course closes the series after it.

Status: <!-- count:ready -->15<!-- /count --> of <!-- count:total -->15<!-- /count --> notebooks are ready: 14 teaching notebooks and the capstone.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## Before you start

Setup is on the [series front page](../README.md#start-here). Course 10 runs in the same `.venv` as Courses 1 to 9.

| Step | What to do |
|:---|:---|
| **Install the course's packages** | With the course's `.venv` active, run the install line below. It adds two lines to Course 9's pins, `faiss-cpu` and `rank-bm25`, and changes none of them: pip adds 2 packages, about 64 MB once installed. |
| **No key needed** | Every generated answer and judge verdict replays from `data/course10_rag_runs/`, recorded once on the author's key. The key cell of each notebook prints only whether a key loaded and the mode: `OpenAI key loaded: False. Mode: replay.` |
| **Going live is optional** | An OpenAI key (`OPENAI_API_KEY`) or an OpenRouter key (`OPENROUTER_API_KEY`) of your own in `my_bondmath\.env`, or in Colab's Secrets panel, makes the same cells send live requests; your answers will differ from the saved ones, and each answer's line says live or replayed. Course 7 shows where to get a key. A full live run of all fifteen days cost the course about 12 cents at the list prices read in October 2026. |
| **The models download once** | MiniLM is in your Hugging Face cache from Course 7; bge-small, gte-small, and the cross-encoder (about 300 MB together) download the first time days 4 and 7 run. Their revisions are pinned in `ragkit.EMBEDDERS` and `ragkit.RERANKER`. |
| **Colab: choose the T4 GPU runtime** | The course advises Colab's T4 GPU runtime and never requires it. In Colab: Runtime, Change runtime type, choose the T4 GPU under Hardware accelerator, Save, then run the notebook from the top. The local-model cells (`t4-only`, days 5, 8, 12, and 14) run only on a GPU and install `llama-cpp-python` into the runtime; everywhere else they print `No GPU in this runtime: this cell is skipped.` and the notebook still runs top to bottom. Google's FAQ says the GPUs offered vary over time and free access to them is heavily restricted. |
| **On Windows** | Everything runs on your CPU in replay. Embeddings are computed live on samples and read from committed files where the full set would not fit a day; a live sample is compared with the committed rows first. |
| **Keep your folder** | Your `my_bondmath` folder gains `ragkit.py`, its tests, and the capstone's `filing_qa.py`. |

```powershell
Set-Location "$HOME\projects\python-fixed-income"
.venv\Scripts\Activate.ps1
python -m pip install -r course10_rag\requirements.txt
python -c "import faiss, rank_bm25; print('ok')"
New-Item -ItemType Directory -Force "$HOME\projects\my_bondmath" | Out-Null
```

Each notebook works in a fresh work folder in your temp folder, prints its name, and writes nothing into the course repo. Each day's "Bring It Home" section shows the PowerShell steps that move the day's functions and tests into `my_bondmath`, run the tests, and commit.

Each day's folder holds three files with the same name: the notebook, a short overview PDF to read first, and a solutions notebook. [How a day works](../README.md#how-a-day-works) explains the pattern. As in Courses 2 to 9, every notebook ends in the same order: Excel side by side, save the day with Git, bring it home, then the exercises, with the AI check last.

## The three weeks

| Week | Theme | By the end you can |
|:---:|:---|:---|
| 1 | Documents, chunking, embeddings, and a vector store | Grade a model's closed-book and prompt-only answers against keys written first, load a filing as pages and items and find the table whose heads sit on another line, split it with a recursive splitter and say what size and overlap do, embed the chunks with three pinned models, search them exactly with NumPy and FAISS and measure an approximate index against the exact one, and run the first full pipeline on five questions beside the two earlier stages, saying which miss was retrieval and which generation |
| 2 | Retrieval quality | Find by BM25 the exact term that embedding search ranks low and fuse the two lists, rerank a pool of candidates with a cross-encoder and measure the gain and its cost, run a named grid of settings on development questions and read the table, ask one question across four documents with metadata filters applied before search, and demand a citation after every sentence and reject the answer that has none |
| 3 | Evaluation at scale, and keeping it running | Report recall at k and MRR by item on a labelled set with a bootstrap interval, put two LLM judges beside a strict grader and read the agreement table and Cohen's kappa, refresh an index when a new filing arrives without re-embedding the old chunks and answer as of each filing's date, serve the retriever behind a FastAPI service and price a thousand answers, and build the capstone's cited question-answering tool with its evaluation report |

## Course map

<!-- map:start -->

### Week 1: Documents, chunking, embeddings, and a vector store

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Five Questions Without Retrieval](week1/day1/01_five_questions_without_retrieval.ipynb) | What RAG is in three sentences, the key cell and the replay transport, five questions about a 10-K's debt with keys written first from its pages, the model asked closed book and then with a careful prompt, a strict grader, and the first finding as a count (0 of 10), beside the grade by `ISNUMBER(SEARCH())` and `COUNTIFS` | Ready |
| 2 | [A Filing as Pages and Items](week1/day2/02_a_filing_as_pages_and_items.ipynb) | `pdf_pages` with every empty page kept, characters by page, the cover and contents pages, a page of Item 7 prose and a page of a Note 7 debt table, pages against the HTML, `page_items` and the 23 items, the printed page against the PDF page, and what a text layer loses, beside `LEN` per pasted line and a date typed into a General cell | Ready |
| 3 | [Chunking: Size and Overlap](week1/day3/03_chunking_size_and_overlap.ipynb) | `recursive_split` written from its docstring, the 10-K at 512/64 and at 1,024/128, what 64 characters carry across a cut, where the splitter cut the debt table, MiniLM's 256 word pieces as the trap a larger chunk sets, and `chunk_table` with item, page, and citation, beside `LEN`, the `SUBSTITUTE` word count, and `=RIGHT(B2,64)=LEFT(B3,64)` | Ready |
| 4 | [Embeddings and a Vector Index](week1/day4/04_embeddings_and_a_vector_index.ipynb) | MiniLM, bge-small, and gte-small at pinned revisions, a live sample checked against the committed matrix, exact search with NumPy and with FAISS returning the same ranks, HNSW's recall against exact, the index manifest, a wrong model's query vectors, and the three models' top pages side by side, beside the cosine by `SUMPRODUCT` over `SQRT(SUMSQ())` | Ready |
| 5 | [Case Study: The First RAG Pipeline](week1/day5/05_case_study_the_first_rag_pipeline.ipynb) | `RagSettings` and the settings line, the retriever, the prompt that must cite, one answer read with its LLM line, the local route on a T4, then a case study: the five questions through closed book, prompt only, and RAG, three hit rules, a retrieval miss against a generation miss, and what the pipeline shows, and where it fails, beside the stage table counted by `COUNTIFS` | Ready |

### Week 2: Retrieval quality

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [BM25 and Hybrid Search](week2/day1/06_bm25_and_hybrid_search.ipynb) | Why keyword search is not dead, BM25 on three texts by hand and on the 10-K, the one place `rank-bm25`'s idf differs, the development questions by BM25 and by MiniLM, reciprocal rank fusion by hand and on the 10-K, and hybrid at 3 against each alone, beside one BM25 weight written out with `LN` and RRF by `=1/(60+rank)` and `SUMIFS` | Ready |
| 2 | [Reranking with a Cross-Encoder](week2/day2/07_reranking_with_a_cross_encoder.ipynb) | A bi-encoder against a cross-encoder, the MS MARCO cross-encoder at its revision with its licence and data terms, hits at 3 before and after reranking 20 to 3, pairs per question and seconds in words, a score that is not a probability, and the miss a reranker cannot fix. Excel has no counterpart today | Ready |
| 3 | [Tuning the Pipeline: A Results Grid](week2/day3/08_tuning_the_pipeline_a_results_grid.ipynb) | One setting at a time, twelve named settings (k, chunk size, neighbour expansion, hybrid, reranking, temperature, `top_p`, `max_tokens`), `run_grid` in replay and `grid_summary` with no column named best, the temperature rows, chunk size and depth together, the local model's grid on a T4, and choosing on development questions only, beside the grid read with `AVERAGEIFS` and `SORTBY` | Ready |
| 4 | [Metadata Filters and Many Documents](week2/day4/09_metadata_filters_and_many_documents.ipynb) | One corpus of four documents, metadata as columns, a question with no filter answered from two documents, `filter_chunks` applied before search, the 10-K's note and the indenture's section joined, a question the corpus cannot answer, and an answer built from the wrong document caught by its citation, beside `COUNTIFS`, `FILTER`, and `TAKE(SORTBY())` | Ready |
| 5 | [Case Study: Prompts That Must Cite](week2/day5/10_case_study_prompts_that_must_cite.ipynb) | `check_citations` sentence by sentence, `refuse_first` before retrieval on four adversarial questions with nothing sent, a planted instruction inside a chunk that is retrieved and not followed, then a case study: cited answers across the corpus, valid citations against matched keys, a valid citation of the wrong document, and what the pipeline shows, and where it fails, beside `ISNUMBER(MATCH())` on chunk ids stored as text | Ready |

### Week 3: Evaluation at scale, and keeping it running

| Day | Notebook | You learn | Status |
|:---:|:---|:---|:---:|
| 1 | [Retrieval Evaluation: Recall and MRR](week3/day1/11_retrieval_evaluation_recall_and_mrr.ipynb) | Evaluating retrieval before answers with no request, how the labelled set was written, `evaluate`, `recall_at_k`, and `mrr` on four retrievers, recall by item, a miss counted as zero, the test questions opened once with a bootstrap interval, and what recall does not say, beside recall by `ISNUMBER(MATCH())` and `COUNTIF` and MRR by `AVERAGE(IFERROR(1/MATCH()))` | Ready |
| 2 | [LLM Judges and Their Limits](week3/day2/12_llm_judges_and_their_limits.ipynb) | Three ways to check an answer, the groundedness and relevance judges with their prompts printed, 90 verdicts replayed, the judge against the strict grader as an annotated heatmap, agreement tables and Cohen's kappa, a judge that says yes to every answer, both judges against a reviewer's labels on the same 45 answers, and a model judging its own answers, beside `COUNTIFS` grids and kappa written out cell by cell | Ready |
| 3 | [Index Refresh and Corpus Drift](week3/day3/13_index_refresh_and_corpus_drift.ipynb) | `content_hash` and the manifest, `refresh_index` with the 10-Q added embedding only the new chunks, as-of dates as metadata and one question answered as of each filing, a stale saved answer found by its chunks' hashes, a model change that re-embeds everything, and the drift of a corpus described, beside `EXACT` inside `SUMPRODUCT` and the 255-character limit of `COUNTIF` and `MATCH` | Ready |
| 4 | [Serving the Retriever and What It Costs](week3/day4/14_serving_the_retriever_and_what_it_costs.ipynb) | `rag_app` with `/search` and `/answer` tested through the test client, BM25 on the server and why not torch, what the service installs, the five questions through the service, `cost_table` at the dated price, a thousand answers a month, and the local route's break-even, beside the cost by `SUMPRODUCT` and prices pasted as text | Ready |
| 5 | [Course 10 Capstone](week3/day5/course10_capstone.ipynb) | Build a cited question-answering tool over five public filings: `filing_qa.py`, settings chosen on development questions, recall and MRR by document with an interval, 25 capstone answers replayed and checked, four unanswerable questions, three refusals, a planted note not followed, two judges, a cost line, a workbook, and the report "What the tool shows, and where it fails". A [worked version](week3/day5/course10_capstone_solutions.ipynb) sits beside it | Ready |

<!-- map:end -->

## The capstone

Day 5 of week 3 is yours, and it is more than one sitting: plan on two or three. A colleague on the desk wants to ask questions of the filings folder and get answers they can check: every sentence with the document and page it came from, `NOT IN CORPUS` when the folder does not say, no view on anything, and then a statement of how good the tool is, with numbers, and what it costs. Thirty questions take you from your complete module to a written evaluation report.

You build `filing_qa.py`: `build_corpus` over the 10-K, the 10-Q, and the three indentures, `ask` with a refusal rule before retrieval, an as-of date read from the question, one request, and `check_citations` on the answer, and `evaluate_tool` over the capstone's own 25 questions, never seen before. Then you choose the settings on the development questions and keep them, score retrieval by document with a bootstrap interval, replay the 25 answers and grade them, assert the four `NOT IN CORPUS` replies and the three refusals, add a synthetic note with a planted instruction and show it is cited and not followed, run both judges, price the run, write a workbook whose checks are formulas, keep a Git history with one commit per deliverable and the tag `course10`, and write the report.

| File | What it is |
|:---|:---|
| [`course10_capstone.ipynb`](week3/day5/course10_capstone.ipynb) | The brief, the questions, and a check cell for every answer that can be checked. A check says correct or not yet, and never shows the answer |
| [`course10_capstone_overview.pdf`](week3/day5/course10_capstone_overview.pdf) | The brief as slides: the scenario, the tool, the deliverables, and how the checks work |
| [`course10_capstone_solutions.ipynb`](week3/day5/course10_capstone_solutions.ipynb) | The worked version, with every decision stated and the course's saved answers replayed. Open it after you finish |

The tool describes public documents. Its figures are as of each document's date, it is not a view on any issuer or security, and it refuses to give one.

## What it uses

| Tool | Used for | First appears |
|:---|:---|:---|
| `textkit` (Course 7) and `agentkit` (Course 8) | Text normalisation, the PDF and EDGAR readers, embeddings, the LLM client, and the recording transport that replays every request | Week 1, Day 1 |
| pandas, matplotlib, openpyxl | Chunk tables, results grids, styled tables and charts, and workbooks for Excel | Week 1, Day 1 |
| pytest | Testing `ragkit.py` every day with inline texts, fake clients, and fake models, never the network | Week 1, Day 1 |
| pypdf | The 10-K's pages, through Course 7's `pdf_text` | Week 1, Day 2 |
| sentence-transformers and PyTorch, on the CPU | The three embedding models and the cross-encoder | Week 1, Day 3 |
| FAISS (`faiss-cpu`) | The exact `IndexFlatIP` beside NumPy, and `IndexHNSWFlat` once, to measure an approximate index | Week 1, Day 4 |
| OpenAI's Chat Completions (`gpt-4.1-mini`), replayed | Every generated answer and judge verdict, recorded once and replayed without a key | Week 1, Day 5 |
| `llama-cpp-python` and a GGUF model, in Colab only | The local route on a T4 GPU, in `t4-only` cells | Week 1, Day 5 |
| `rank-bm25` | The check on the BM25 you write by hand | Week 2, Day 1 |
| pydantic | The judge's verdict and the service's request models | Week 3, Day 2 |
| FastAPI and its test client | The retrieval service of day 14 | Week 3, Day 4 |

Exact versions are pinned in [`requirements.txt`](requirements.txt): `faiss-cpu` 1.15.1 and `rank-bm25` 0.2.2 on top of Course 9's pins, among them torch 2.14.1, sentence-transformers 6.1.0, transformers 5.19.0, openai 3.26.0, pandas 3.0.6, and pytest 9.1.1.

| Model | Repository and pinned revision | Licence | Size | Used for |
|:---|:---|:---|:---|:---|
| MiniLM (`minilm`) | `sentence-transformers/all-MiniLM-L6-v2` at `1110a243` | Apache-2.0 | 91 MB | The running embedding model (384 numbers, 256 word pieces), from Course 7 |
| bge-small (`bge_small`) | `BAAI/bge-small-en-v1.5` at `5c38ec7c` | MIT | 133 MB | Compared on day 4 (384 numbers, 512 pieces, a query instruction) |
| gte-small (`gte_small`) | `thenlper/gte-small` at `17e1f347` | MIT | 67 MB | Compared on day 4 (384 numbers, 512 pieces) |
| Cross-encoder | `cross-encoder/ms-marco-MiniLM-L6-v2` at `233902d2` | Apache-2.0 (trained on MS MARCO, whose terms are quoted on day 7) | 91 MB | The reranker of days 7 to 15 |
| Local generator | `bartowski/Mistral-7B-Instruct-v0.3-GGUF`, `Mistral-7B-Instruct-v0.3-Q4_K_M.gguf`, at `61fd4167` | Apache-2.0 (a third-party quantisation) | 4.37 GB | The `t4-only` cells, in Colab on a T4; never downloaded by the build or on Windows |

| Data | Kind | Used in |
|:---|:---|:---|
| `course7_boyd_10k_2025.htm`: Boyd Gaming Corporation, Form 10-K for fiscal 2025, filed 2026-02-20 (Course 7's file) | **Real**, a public record on sec.gov, quoted for descriptive extraction only | Every day |
| `course10_boyd_10k_2025.pdf`: the same 10-K printed to PDF by the course from the SEC copy, 113 pages | **Real** text, the SEC copy's; the page layout is the course's print | Days 2 to 15 |
| `course10_boyd_10q_2026q2.htm`: Boyd Gaming's Form 10-Q for the quarter ended June 30, 2026, filed 2026-07-30 | **Real**, a public record on sec.gov, quoted for descriptive extraction only | Days 13 and 15 |
| `course7_indentures/`: the Boyd 2021, Levi Strauss 2006, and Lamar Media 2007 indentures (Course 7's files) | **Real**, public records on sec.gov | Days 9, 10, and 15 |
| `course10_questions.csv`: 75 questions with answer keys, each key a quote with its page, item, or section; splits `arc`, `dev`, `test`, and `capstone` | The course's own, written by hand from the documents' pages before any request; MIT with the code | Every day |
| `course10_embeddings/`: 8 embedding sets (16 files, 14.4 MB) of the chunk tables by the three models | The course's own derived data, computed once on one thread at the pinned revisions; a live sample is checked against them first | Days 4 to 15 |
| `course10_human_labels.csv`: a reviewer of the course's groundedness and relevance labels on day 12's 45 answers (42 and 38 yes, 3 and 7 partly, no no), made from the question, the answer, and the chunks before any verdict was shown | The course's own, MIT with the code | Days 12 and 15 |
| `course10_rag_runs/`: 352 saved requests and responses in 9 day folders, recorded on `gpt-4.1-mini` on 2026-10-12 and 2026-10-13 | The course's own, MIT with the code; no key, no header, and no account identifier is stored | Days 1, 5, 8, 9, 10, 12, 13, 14, and 15 |

No model file, FAISS index, 10-Q exhibit, or student's live run is in the repo: each notebook rebuilds its index from the committed embeddings in under a second. Day 12 reads `course10_human_labels.csv`, a reviewer of the course's labels on its 45 answers, made before any verdict was shown, and sets both judges beside them; the `t4-only` cells are yours to run in Colab on a T4, and the course keeps no recording of them. The guardrail in one sentence: an answer cites chunks that were sent or says `NOT IN CORPUS`, a request for a view is refused before retrieval, a filing's forward-looking sentences are quoted as the issuer's, and real issuers appear only as the authors of their documents. Sources, terms, and changes for every file are in [The data](../README.md#the-data) on the front page.

## What comes next

Later work builds on the `bondmath`, `marketdata`, `mlkit`, `ensemblekit`, `netkit`, `textkit`, `agentkit`, `deploykit`, and `ragkit` you wrote in Courses 2 to 10. Next comes [the Bonus course, Build Your Own Coding Agent](../course_bonus_coding_agent/README.md), which closes the series.

---

<div align="center">

Created by **Jeff Lenamon**

</div>
