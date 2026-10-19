# The data

Every file the series reads, where it came from, and its terms. Back to the [series front page](../README.md).

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

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
