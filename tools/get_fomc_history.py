"""Download the FOMC post-meeting statements from 2000 on and write data/course7_fomc_statements.csv.

Source: Board of Governors of the Federal Reserve System, Federal Open Market Committee statements.
    Historical pages, one per year, 2000 to 2020 (each meeting's panel links its statement):
        https://www.federalreserve.gov/monetarypolicy/fomchistoricalYYYY.htm
    Calendar page, 2021 on:
        https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
    Statement pages, in three formats:
        /boarddocs/press/general/YYYY/YYYYMMDD/ and /boarddocs/press/monetary/YYYY/YYYYMMDD/ (2000 to 2005)
        /newsevents/press/monetary/YYYYMMDDa.htm, which redirects to the next form (2006 to 2010)
        /newsevents/pressreleases/monetaryYYYYMMDDa.htm (2011 on)

Which pages are taken: on a historical page, every link whose text is exactly "Statement" inside a meeting's panel
(so the "Statement on Longer-Run Goals and Monetary Policy Strategy" and the 2014 "Statement Regarding Monetary Policy
Implementation and Balance Sheet Normalization" are not taken); from 2021 on, the calendar's "Statement:" HTML links,
read exactly as tools/get_fomc_statements.py reads them (its parser is imported, so the two files agree on every
statement from 2021).

Columns: date (from the statement page's address), url (the page as served, after any redirect), scheduled (False
when the panel heading names a conference call, an unscheduled meeting, or a notation vote), text (the release's
paragraphs in order, joined by a newline).

What is kept: every paragraph of the press release, including the voting paragraph, footnotes, and, on the older pages,
the paragraph on the Board's related discount rate action, which is part of the same release. Left out: the release
date line, "For immediate release", the media contact line, the link to the implementation note, the page's
navigation, and, on the 2006 to 2020 pages, run-in headings, links after a paragraph's last sentence ("Return to
text", a related statement), and paragraphs that are headings or lists of links (new_statement_text says how).
Every character of the text is the Board's; the only changes are to white space (each run of spaces, line breaks, and
non-breaking spaces becomes one space).

Reuse: https://www.federalreserve.gov/disclaimer.htm says "Unless otherwise indicated, information on Board's website
is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source
of the information."

Standard library only. Usage (from the repo root):

    python tools/get_fomc_history.py
"""
import csv
import html
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import get_fomc_statements  # noqa: E402  (the 2021-on reader, unchanged)

SITE = "https://www.federalreserve.gov"
FIRST_YEAR, LAST_HISTORICAL_YEAR = 2000, 2020
OUT = Path(__file__).resolve().parent.parent / "data" / "course7_fomc_statements.csv"
PAUSE_SECONDS = 0.5

PANEL = re.compile(r'<div class="panel panel-default')
HEADING = re.compile(r"<h5[^>]*>(.*?)</h5>", re.S)
STATEMENT = re.compile(r'<a href="([^"]+)"[^>]*>\s*Statement\s*</a>')
# the statement date is the last eight-digit run in the address (some old pages redirect to .../default.htm)
DATE_IN_URL = re.compile(r"(\d{4})(\d{2})(\d{2})")
# the old pages: the release sits between "For immediate release" and the link back to the year's list
OLD_START = re.compile(r"For immediate release", re.I)
OLD_END = re.compile(r"<HR\b|<a href=\"[^\"]*\">\s*\d{4} Monetary policy|Last update:", re.I)
OLD_BREAK = re.compile(r"<\s*p\b[^>]*>", re.I)


def fetch(url: str) -> tuple[str, str]:
    """The page text and the address it was finally served from."""
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        final = response.geturl().replace("http://", "https://", 1)
        return response.read().decode("utf-8", errors="strict"), final


def old_statement_text(page: str) -> str:
    """Paragraphs of a 2000 to 2005 release (unclosed <p> tags, a table around the text). A <br> inside a paragraph
    is a line break in the HTML source only, so it becomes a space."""
    start = OLD_START.search(page)
    if not start:
        raise RuntimeError("no 'For immediate release' line")
    end = OLD_END.search(page, start.end())
    body = re.sub(r"<!--.*?-->", "", page[start.end():end.start() if end else len(page)], flags=re.S)
    paragraphs = []
    for chunk in OLD_BREAK.split(body):
        text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", chunk)).split())
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs)


class ReleaseParser(HTMLParser):
    """The paragraphs of a 2006 to 2020 release: each <p> inside the body column, up to the "Related Information"
    heading. Each piece of text is recorded with its kind: "text", "link" (inside <a>), or "bold" (inside <strong>
    or <b>)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_article = False
        self.body_depth = 0
        self.in_paragraph = False
        self.in_link = False
        self.in_bold = False
        self.stopped = False
        self.paragraphs: list[list[tuple[str, str]]] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attributes = dict(attrs)
        if self.stopped:
            return
        if tag == "div":
            if attributes.get("id") == "article":
                self.in_article = True
            elif attributes.get("id") == "relatedItems" and self.body_depth:
                self.stopped = True
            elif self.body_depth:
                self.body_depth += 1
            elif self.in_article and attributes.get("class") == get_fomc_statements.BODY_CLASS:
                self.body_depth = 1
        elif tag == "h4" and self.body_depth:
            self.stopped = True
        elif tag == "p" and self.body_depth:
            self.in_paragraph = True
            self.paragraphs.append([])
        elif tag == "a":
            self.in_link = True
        elif tag in ("strong", "b"):
            self.in_bold = True
        elif tag == "br" and self.in_paragraph and self.body_depth:
            # a line break inside a paragraph separates words, as a space does
            self.paragraphs[-1].append(("text", " "))

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self.body_depth and not self.stopped:
            self.body_depth -= 1
            if self.body_depth == 0:
                self.in_article = False
        elif tag == "p":
            self.in_paragraph = False
        elif tag == "a":
            self.in_link = False
        elif tag in ("strong", "b"):
            self.in_bold = False

    def handle_data(self, data: str) -> None:
        if self.in_paragraph and self.body_depth and not self.stopped:
            kind = "link" if self.in_link else "bold" if self.in_bold else "text"
            self.paragraphs[-1].append((kind, data))


# a paragraph of the statement ends as a sentence does; a heading or a list of links does not
SENTENCE_END = re.compile(r"[.:;][\"')\u201d]?$")


def new_statement_text(page: str) -> str:
    """The statement's paragraphs from a 2006 to 2020 page. Three rules, each leaving out page furniture only:
    a bold run that opens a paragraph is a run-in heading ("Federal Reserve Actions") and is left out; links after a
    paragraph's last sentence (a "Return to text" after a footnote, a link to a related statement) are left out; and
    a paragraph that then does not end as a sentence ends (a heading, a list of central banks' or FAQ links) is left
    out. Link text inside a sentence is kept."""
    parser = ReleaseParser()
    parser.feed(page)
    kept = []
    for parts in parser.paragraphs:
        while parts and (parts[0][0] == "bold" or not parts[0][1].strip()):
            parts = parts[1:]
        while parts and (parts[-1][0] == "link" or not parts[-1][1].strip()):
            parts = parts[:-1]
        text = " ".join("".join(data for _, data in parts).split())
        if text and SENTENCE_END.search(text) and not text.startswith(get_fomc_statements.NOT_STATEMENT):
            kept.append(text)
    return "\n".join(kept)


def historical_links(year: int) -> list[tuple[str, bool]]:
    """(statement address, scheduled) for every "Statement" link in a historical year's meeting panels."""
    page, _ = fetch(f"{SITE}/monetarypolicy/fomchistorical{year}.htm")
    links = []
    for panel in PANEL.split(page)[1:]:
        heading = HEADING.search(panel)
        if not heading:
            continue
        title = " ".join(heading.group(1).split())
        scheduled = "Meeting" in title and "unscheduled" not in title.lower()
        links += [(m.group(1), scheduled) for m in STATEMENT.finditer(panel)]
    if not links:
        raise RuntimeError(f"no statement links on the {year} historical page")
    return links


def check(text: str, url: str) -> None:
    if len(text) < 200 or "<" in text or ">" in text or "Release Date" in text or "Last update" in text:
        raise RuntimeError(f"unexpected statement text at {url}: {text[:200]!r}")


def main() -> None:
    rows = []
    for year in range(FIRST_YEAR, LAST_HISTORICAL_YEAR + 1):
        for path, scheduled in historical_links(year):
            page, final = fetch(SITE + path)
            text = old_statement_text(page) if "/boarddocs/" in final else new_statement_text(page)
            check(text, final)
            y, m, d = DATE_IN_URL.findall(final)[-1]
            rows.append({"date": f"{y}-{m}-{d}", "url": final, "scheduled": scheduled, "text": text})
            time.sleep(PAUSE_SECONDS)
        print(f"{year}: {sum(r['date'].startswith(str(year)) for r in rows)} statements")

    calendar, _ = fetch(get_fomc_statements.CALENDAR)
    for link in get_fomc_statements.STATEMENT_LINK.finditer(calendar):
        path, y, m, d = link.groups()
        if int(y) <= LAST_HISTORICAL_YEAR:
            continue
        page, final = fetch(get_fomc_statements.SITE + path)
        text = get_fomc_statements.statement_text(page)
        check(text, final)
        rows.append({"date": f"{y}-{m}-{d}", "url": final, "scheduled": True, "text": text})
        time.sleep(PAUSE_SECONDS)

    rows.sort(key=lambda row: row["date"])
    dates = [row["date"] for row in rows]
    if len(set(dates)) != len(dates):
        raise RuntimeError("two statements share a date")
    with open(OUT, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "url", "scheduled", "text"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} statements, {rows[0]['date']} to {rows[-1]['date']}, "
          f"{sum(not r['scheduled'] for r in rows)} unscheduled, to {OUT.name}")


if __name__ == "__main__":
    main()
