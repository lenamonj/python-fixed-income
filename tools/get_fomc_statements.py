"""Download the FOMC post-meeting statements and write data/fomc_statements.csv.

Source: Board of Governors of the Federal Reserve System, Federal Open Market Committee statements.
    Calendar page that lists every meeting and links its statement:
        https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
    One press release page per statement:
        https://www.federalreserve.gov/newsevents/pressreleases/monetaryYYYYMMDDa.htm

The file in the repo was retrieved on 2026-10-03 and holds the 46 statements dated 2021-01-27 to
2026-09-16: every meeting of the whole years 2021 to 2025, and 2026 to the retrieval date. Every one
is the statement of a scheduled meeting. The calendar lists no statement of an unscheduled meeting in
that span.

Which pages are taken: on the calendar page, each link labelled "Statement:" with a PDF and an HTML
version, for the years from FIRST_YEAR on. Other documents on the calendar (implementation notes,
the Statement on Longer-Run Goals and Monetary Policy Strategy, minutes) are not taken.

What is kept from each page: the paragraphs of the statement, in order, including the voting
paragraph where there is one. The page heading, the media contact line, and the link to the
implementation note are left out. Every character of the text is the Board's. The only changes are
to white space: each run of spaces, line breaks, and non-breaking spaces becomes one space, and the
paragraphs are joined with a newline.

Reuse: https://www.federalreserve.gov/disclaimer.htm says "Unless otherwise indicated, information
on Board's website is in the public domain and may be copied and distributed without permission.
Please cite to the Board as the source of the information."

Usage (from the repo root):

    python tools/get_fomc_statements.py
"""
import csv
import re
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SITE = "https://www.federalreserve.gov"
CALENDAR = SITE + "/monetarypolicy/fomccalendars.htm"
FIRST_YEAR = 2021
OUT = Path(__file__).resolve().parent.parent / "data" / "fomc_statements.csv"

# on the calendar, a meeting's statement is the label "Statement:", a PDF link, then the HTML link
STATEMENT_LINK = re.compile(
    r"<strong>Statement:</strong><br>\s*<a href=\"[^\"]+\.pdf\">PDF</a>\s*\|\s*"
    r"<a href=\"(/newsevents/pressreleases/monetary(\d{4})(\d{2})(\d{2})a\.htm)\">HTML</a>"
)
# paragraphs inside the statement column that are not part of the statement
NOT_STATEMENT = ("For media inquiries", "Implementation Note issued")
BODY_CLASS = "col-xs-12 col-sm-8 col-md-8"


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read().decode("utf-8")


class StatementParser(HTMLParser):
    """Collect the text of each <p> inside the body column of the press release."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_article = False
        self.body_depth = 0  # depth of nested <div> inside the body column, 0 when outside it
        self.in_paragraph = False
        self.paragraphs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attributes = dict(attrs)
        if tag == "div":
            if attributes.get("id") == "article":
                self.in_article = True
            elif self.body_depth:
                self.body_depth += 1
            elif self.in_article and attributes.get("class") == BODY_CLASS:
                self.body_depth = 1
        elif tag == "p" and self.body_depth:
            self.in_paragraph = True
            self.paragraphs.append("")

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self.body_depth:
            self.body_depth -= 1
            if self.body_depth == 0:
                # the body column is closed, so nothing after it belongs to the statement
                self.in_article = False
        elif tag == "p":
            self.in_paragraph = False

    def handle_data(self, data: str) -> None:
        if self.in_paragraph and self.body_depth:
            self.paragraphs[-1] += data


def statement_text(page: str) -> str:
    parser = StatementParser()
    parser.feed(page)
    # str.split() with no argument splits on every kind of white space, non-breaking spaces included
    paragraphs = [" ".join(paragraph.split()) for paragraph in parser.paragraphs]
    paragraphs = [p for p in paragraphs if p and not p.startswith(NOT_STATEMENT)]
    return "\n".join(paragraphs)


def main() -> None:
    links = [m for m in STATEMENT_LINK.finditer(fetch(CALENDAR)) if int(m.group(2)) >= FIRST_YEAR]
    if not links:
        raise RuntimeError("no statement links found on the calendar page")

    rows = []
    for link in links:
        path, year, month, day = link.groups()
        text = statement_text(fetch(SITE + path))
        if len(text) < 300 or "<" in text or ">" in text:
            raise RuntimeError(f"unexpected statement text at {path}: {text[:200]!r}")
        rows.append({"date": f"{year}-{month}-{day}", "url": SITE + path, "text": text})
        time.sleep(0.5)

    rows.sort(key=lambda row: row["date"])
    years = sorted({row["date"][:4] for row in rows})
    if years[0] != str(FIRST_YEAR):
        raise RuntimeError(f"the calendar page no longer lists {FIRST_YEAR}: first year found {years[0]}")

    # newline="" and "\n" line endings give the same bytes on every run and every machine
    with open(OUT, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "url", "text"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} statements, {rows[0]['date']} to {rows[-1]['date']}, to {OUT}")


if __name__ == "__main__":
    main()
