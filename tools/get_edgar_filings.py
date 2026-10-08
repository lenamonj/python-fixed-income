"""Download the Boyd Gaming 10-K and the risk factors of three 10-Ks: data/course7_boyd_10k_2025.htm and
data/course7_risk_factors.csv.

Source: SEC EDGAR (public records on sec.gov; see DATA.md, "EDGAR terms"). Three Form 10-K annual reports for fiscal
2025, each the filing's main document:
    Boyd Gaming Corporation, fiscal year ended December 31, 2025, filed 2026-02-20, accession 0001437749-26-004908
    Levi Strauss & Co., fiscal year ended November 30, 2025, filed 2026-01-28, accession 0000094845-26-000008
    Lamar Advertising Company and Lamar Media Corp. (one combined report), fiscal year ended December 31, 2025, filed
        2026-02-20, accession 0001090425-26-000008; read for its risk factors only

course7_boyd_10k_2025.htm is Boyd's 10-K as filed (inline XBRL), byte for byte, with the one script tag sec.gov's
delivery network adds before </body> removed (as tools/get_indentures.py does).

course7_risk_factors.csv holds one row per risk factor of Item 1A of each report: cik, company, form, filed,
accession, url, order (1, 2, ... within the filing), category (the bold heading of the group it sits under, as the
filer wrote it), heading, text. How the rows are found, from the HTML (checked by eye on all three filings,
2026-10-07): Item 1A runs from the last paragraph that starts "Item 1A" to the next that starts "Item 1B"; inside
it, a paragraph whose text is all bold with some of it italic is a risk factor's heading, a paragraph all bold and
not italic is a group heading (category), and the plain paragraphs after a heading, up to the next heading, are its
text. Page numbers (a paragraph of digits only) and "Table of Contents" links are left out. Text is kept as
published; only white space is changed (each run becomes one space; paragraphs are joined by a newline).

Requests go through the reference textkit.edgar_get with the declared User-Agent from PFI_SEC_CONTACT.

Usage (from the repo root, with the course Python):  python tools/get_edgar_filings.py
"""
import csv
import hashlib
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

sys.path.insert(0, str(Path(__file__).resolve().parent))
import course7_reference  # noqa: E402
from get_indentures import INJECTED  # noqa: E402

DATA = course7_reference.REPO / "data"
TEN_K = DATA / "course7_boyd_10k_2025.htm"
RISK_FACTORS = DATA / "course7_risk_factors.csv"
FILINGS = [
    {"cik": 906553, "company": "Boyd Gaming Corporation", "form": "10-K", "filed": "2026-02-20",
     "accession": "0001437749-26-004908",
     "url": "https://www.sec.gov/Archives/edgar/data/906553/000143774926004908/bgc20251121_10k.htm"},
    {"cik": 94845, "company": "Levi Strauss & Co.", "form": "10-K", "filed": "2026-01-28",
     "accession": "0000094845-26-000008",
     "url": "https://www.sec.gov/Archives/edgar/data/94845/000009484526000008/lvis-20251130.htm"},
    {"cik": 899045, "company": "Lamar Media Corp.", "form": "10-K", "filed": "2026-02-20",
     "accession": "0001090425-26-000008",
     "url": "https://www.sec.gov/Archives/edgar/data/1090425/000109042526000008/lamr-20251231.htm"},
]
COLUMNS = ["cik", "company", "form", "filed", "accession", "url", "order", "category", "heading", "text"]


def _style(node) -> tuple[bool, bool]:
    """(bold, italic) of a piece of text, from its tags and inline styles up to its paragraph."""
    bold = italic = False
    for parent in node.parents:
        style = (parent.get("style") or "").lower().replace(" ", "")
        bold |= parent.name in ("b", "strong") or re.search(r"font-weight:(bold|[6-9]00)", style) is not None
        italic |= parent.name in ("i", "em") or "font-style:italic" in style
        if parent.name in ("p", "div", "td"):
            break
    return bold, italic


def risk_factors(html: bytes, filing: dict) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["script", "style", "ix:header"]):
        tag.decompose()
    leaves = [b for b in soup.find_all(["p", "div"]) if not b.find(["p", "div"])]
    texts = [" ".join(b.get_text("").split()) for b in leaves]
    starts = [i for i, t in enumerate(texts) if re.match(r"(?i)item\s*1a\b", t)]
    if not starts:
        raise SystemExit(f"{filing['company']}: no Item 1A heading")
    start = starts[-1]
    end = next(i for i, t in enumerate(texts) if i > start and re.match(r"(?i)item\s*1b\b", t))
    rows, category, current = [], "", None
    for leaf, text in zip(leaves[start + 1:end], texts[start + 1:end]):
        if not text or text.isdigit() or text == "Table of Contents":
            continue
        styles = {_style(s) for s in leaf.find_all(string=True) if type(s) is NavigableString and s.strip()}
        all_bold = all(bold for bold, _ in styles)
        if all_bold and any(italic for _, italic in styles):
            current = {"category": category, "heading": text, "paragraphs": []}
            rows.append(current)
        elif all_bold:
            category, current = text, None
        elif current is not None:
            current["paragraphs"].append(text)
    return [{k: filing[k] for k in ("cik", "company", "form", "filed", "accession", "url")}
            | {"order": order, "category": row["category"], "heading": row["heading"],
               "text": "\n".join(row["paragraphs"])}
            for order, row in enumerate(rows, start=1)]


def main() -> None:
    textkit = course7_reference.textkit()
    headers = textkit.sec_headers(*course7_reference.sec_contact())
    rows = []
    for filing in FILINGS:
        served = textkit.edgar_get(filing["url"], headers)
        html, injected = INJECTED.subn(b"", served)
        if injected > 1:
            raise SystemExit(f"{filing['company']}: {injected} injected script tags; expected at most one")
        if filing["cik"] == 906553:
            TEN_K.write_bytes(html)
            print(f"{TEN_K.name}: {len(served):,} bytes served, {injected} injected tag removed, {len(html):,} bytes "
                  f"as filed (SHA-256 {hashlib.sha256(html).hexdigest()})")
        found = risk_factors(html, filing)
        empty = [row["order"] for row in found if not row["text"]]
        if empty:
            raise SystemExit(f"{filing['company']}: risk factors with no text after the heading: {empty}")
        rows += found
        print(f"{filing['company']}: {len(found)} risk factors in {len({r['category'] for r in found})} groups, "
              f"{sum(len(r['text'].split()) + len(r['heading'].split()) for r in found):,} words")
    with open(RISK_FACTORS, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {RISK_FACTORS.name}, {RISK_FACTORS.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
