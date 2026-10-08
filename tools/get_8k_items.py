"""Sample item sections of Form 8-K current reports from EDGAR and write data/course7_8k_items.csv.

Source: SEC EDGAR (public records on sec.gov; see DATA.md, "EDGAR terms"): EDGAR full-text search
(https://efts.sec.gov/LATEST/search-index) for the hits, then each sampled 8-K's main document from the archives.

The sampling design (COURSE7_SPEC.md, "Data"; the counts it gives are in DATA.md):
- Eight items, each searched by a phrase of its own title (ITEM_QUERIES), forms=8-K, one search per calendar month
  of 2019 to 2025 (84 per item), the first page of each (up to 100 hits, in the order the search returns them).
- A hit is eligible for an item when its form and file type are "8-K" (no amendments), its own `items` metadata
  lists the item, and its document is HTML. Duplicates (the same accession) are kept once per item.
- For each item and filing year the eligible filings are shuffled with numpy's default_rng(SEED + k), k the item's
  position times 100 plus the year's offset, and taken in that order until 100 sections are kept or the filings
  run out. So the rare items are rare in the file by the course's design, and the common ones are capped.
- A section is cut from the document's text (the reference textkit.html_to_text) by the reference
  textkit.split_items with the filing's own `items` list, in that order, so a cross-reference to another item inside
  a paragraph never cuts it. The body keeps no heading: split_items removes the heading line, and the item's title
  is removed if the body still starts with it, and a first line that is the title on its own (however the filer
  spaced or cut it) is removed after the 300-word cut. A section of fewer than 20 words before that step is skipped (for example "Not
  applicable" or a section that only points to an exhibit), and the next filing is taken.
- text is the body cut at 300 words (whole lines kept until the 300th word, the last line cut); words is the
  body's full word count before the cut.

Columns: accession, cik, company (the first filer, as EDGAR displays it, without the ticker and CIK), filed, item
(text, "2.04"), item_title, words, text, url.

Requests go through the reference textkit.edgar_get (at most one per 0.11 s) with the declared User-Agent from
PFI_SEC_CONTACT; a search that returns HTTP 500 (seen on about one in twelve probe queries) is tried again after 2,
4, 8, 16 seconds.

Usage (from the repo root, with the course Python):  python tools/get_8k_items.py
"""
import calendar
import csv
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import course7_reference  # noqa: E402

SEED = 42
YEARS = range(2019, 2026)
PER_ITEM_YEAR = 100
MAX_WORDS = 300
MIN_WORDS = 20
OUT = course7_reference.REPO / "data" / "course7_8k_items.csv"
SEARCH = "https://efts.sec.gov/LATEST/search-index?q={q}&forms=8-K&dateRange=custom&startdt={start}&enddt={end}"
ITEM_QUERIES = {
    "1.01": "Entry into a Material Definitive Agreement",
    "1.03": "Bankruptcy or Receivership",
    "2.02": "Results of Operations and Financial Condition",
    "2.03": "Creation of a Direct Financial Obligation",
    "2.04": "Triggering Events That Accelerate",
    "2.06": "Material Impairments",
    "3.01": "Notice of Delisting or Failure to Satisfy",
    "5.02": "Departure of Directors or Certain Officers",
}
COLUMNS = ["accession", "cik", "company", "filed", "item", "item_title", "words", "text", "url"]


def get(textkit, url: str, headers: dict) -> bytes:
    """edgar_get, tried again on HTTP 500 after 2, 4, 8, 16 seconds (the full-text search's occasional error)."""
    for wait in (2, 4, 8, 16, None):
        try:
            return textkit.edgar_get(url, headers)
        except RuntimeError as error:
            if "HTTP 500" not in str(error) or wait is None:
                raise
            time.sleep(wait)


def month_ranges(year: int):
    """(first day, last day) of each month of the year, as text."""
    for month in range(1, 13):
        yield f"{year}-{month:02d}-01", f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}"


def company_name(display: str) -> str:
    """'Strategic Realty Trust, Inc.  (SGIC)  (CIK 0001446371)' gives 'Strategic Realty Trust, Inc.'."""
    return re.sub(r"\s*\((?:CIK \d+|[A-Z0-9.,\- ]+)\)", "", display).strip()


def eligible_filings(textkit, headers: dict, item: str, year: int) -> dict:
    """accession -> hit fields, for every eligible hit of the item's monthly searches in one year."""
    found = {}
    for start, end in month_ranges(year):
        url = SEARCH.format(q=urllib.parse.quote(f'"{ITEM_QUERIES[item]}"'), start=start, end=end)
        hits = json.loads(get(textkit, url, headers))["hits"]["hits"]
        for hit in hits:
            source = hit["_source"]
            name = hit["_id"].split(":", 1)[1]
            if source.get("form") != "8-K" or source.get("file_type") != "8-K" or item not in source.get("items", []):
                continue
            if not name.lower().endswith((".htm", ".html")):
                continue
            cik = int(source["ciks"][0])
            found.setdefault(source["adsh"], {
                "accession": source["adsh"], "cik": cik, "company": company_name(source["display_names"][0]),
                "filed": source["file_date"], "items": source["items"],
                "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{source['adsh'].replace('-', '')}/{name}"})
    return found


def section_body(textkit, html: bytes, items: list[str], item: str) -> tuple[str, int] | None:
    """The item's body cut at MAX_WORDS, and its full word count; None when it is not found or too short."""
    try:
        sections = textkit.split_items(textkit.html_to_text(html), items)
    except ValueError:
        return None
    match = sections[sections["item"] == item]
    if match.empty:
        return None
    body = match["text"].iloc[0]
    # a heading written on the same line as its body: remove the title words too
    title = re.escape(textkit.ITEM_TITLES[item]).replace(r"\ ", r"\s+")
    body = re.sub(rf"^[\s.:\-]*{title}[\s.:;\-]*", "", body, flags=re.IGNORECASE).strip()
    words = len(body.split())
    if words < MIN_WORDS or re.match(r"(?i)item\b", body):
        return None
    kept, count = [], 0
    for line in body.split("\n"):
        line_words = line.split()
        if count + len(line_words) >= MAX_WORDS:
            kept.append(" ".join(line_words[:MAX_WORDS - count]))
            break
        kept.append(line)
        count += len(line_words)
    text, dropped = drop_title_line("\n".join(kept), textkit.ITEM_TITLES[item])
    return text, words - dropped


def _letters(text: str) -> str:
    return re.sub(r"[^a-z]", "", text.lower())


def drop_title_line(text: str, title: str) -> tuple[str, int]:
    """Remove a first line that is the item's title on its own (a short line whose letters begin the title's,
    however the filer spaced or cut it, for example "Creation of a Direct Financial Obligation"); applied after the
    300-word cut. Returns the text and the number of words removed."""
    first, _, rest = text.partition("\n")
    letters = _letters(first)
    if rest and len(first) <= 200 and len(letters) >= 10 and _letters(title).startswith(letters[:40]):
        return rest, len(first.split())
    return text, 0


def main() -> None:
    textkit = course7_reference.textkit()
    headers = textkit.sec_headers(*course7_reference.sec_contact())
    rows, counts = [], {}
    for position, item in enumerate(ITEM_QUERIES):
        for offset, year in enumerate(YEARS):
            filings = eligible_filings(textkit, headers, item, year)
            # filed in the year (a search by date range already ensures it), in a fixed order before the shuffle
            order = sorted(a for a, f in filings.items() if f["filed"].startswith(str(year)))
            rng = np.random.default_rng(SEED + position * 100 + offset)
            kept = skipped = 0
            for accession in rng.permutation(np.array(order, dtype=object)) if order else []:
                if kept == PER_ITEM_YEAR:
                    break
                filing = filings[accession]
                result = section_body(textkit, textkit.edgar_get(filing["url"], headers), filing["items"], item)
                if result is None:
                    skipped += 1
                    continue
                text, words = result
                rows.append({k: filing[k] for k in ("accession", "cik", "company", "filed", "url")}
                            | {"item": item, "item_title": textkit.ITEM_TITLES[item], "words": words, "text": text})
                kept += 1
            counts[(item, year)] = (len(order), kept, skipped)
            print(f"item {item} {year}: {len(order)} eligible filings, {kept} sections kept, {skipped} skipped",
                  flush=True)
    rows.sort(key=lambda row: (row["filed"], row["accession"], row["item"]))
    with open(OUT, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows):,} sections to {OUT.name}, {OUT.stat().st_size:,} bytes")
    print(json.dumps({f"{item} {year}": value for (item, year), value in counts.items()}))


if __name__ == "__main__":
    main()
