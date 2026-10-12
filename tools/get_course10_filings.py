"""Download Boyd Gaming's latest Form 10-Q from EDGAR: data/course10_boyd_10q_2026q2.htm.

Source: SEC EDGAR (public records on sec.gov; DATA.md, "EDGAR terms"). Two requests in all, through the reference
textkit.edgar_get (at most one request per 0.11 s, retried only on 429 and 503) with the declared User-Agent from
PFI_SEC_CONTACT, read from the repo-root .env inside this script and never printed or written:

    1. the company's filing index, https://data.sec.gov/submissions/CIK0000906553.json (Boyd Gaming Corporation),
       from which the most recent filing of form 10-Q is taken (accession, filing date, report date, main document);
    2. that main document, written byte for byte as filed, with the one script tag sec.gov's delivery network adds
       before </body> removed (tools/get_indentures.py's INJECTED, as Course 7 did).

The tool prints the accession, the dates, the size, and the SHA-256, which DATA.md records. If the latest 10-Q's
report date is not 2026-06-30 the file name (2026q2) would be wrong, so the tool stops and says so.

Usage (from the repo root, with the course Python):  python tools/get_course10_filings.py
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import course7_reference  # noqa: E402
from get_indentures import INJECTED  # noqa: E402

CIK = 906553
INDEX = f"https://data.sec.gov/submissions/CIK{CIK:010d}.json"
OUT = course7_reference.REPO / "data" / "course10_boyd_10q_2026q2.htm"
EXPECTED_REPORT_DATE = "2026-06-30"


def latest_10q(index: dict) -> dict:
    """The most recent 10-Q in the submissions index's recent filings (they are listed newest first)."""
    recent = index["filings"]["recent"]
    for position, form in enumerate(recent["form"]):
        if form == "10-Q":
            return {key: recent[key][position] for key in ("accessionNumber", "filingDate", "reportDate",
                                                           "primaryDocument")}
    raise SystemExit("no 10-Q among the recent filings")


def main() -> None:
    textkit = course7_reference.textkit()
    name, email = course7_reference.sec_contact()
    headers = textkit.sec_headers(name, email)
    filing = latest_10q(json.loads(textkit.edgar_get(INDEX, headers)))
    if filing["reportDate"] != EXPECTED_REPORT_DATE:
        raise SystemExit(f"the latest 10-Q reports on {filing['reportDate']}, not {EXPECTED_REPORT_DATE}: rename "
                         "the output file and DATA.md's entry before writing it")
    folder = filing["accessionNumber"].replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{folder}/{filing['primaryDocument']}"
    raw, injected = INJECTED.subn(b"", textkit.edgar_get(url, headers))
    OUT.write_bytes(raw)
    print(f"10-Q accession {filing['accessionNumber']}, filed {filing['filingDate']}, period ended "
          f"{filing['reportDate']}")
    print(f"url {url}")
    print(f"wrote {OUT.name}: {len(raw):,} bytes, SHA-256 {hashlib.sha256(raw).hexdigest()}, delivery script tags "
          f"removed: {injected}")


if __name__ == "__main__":
    sys.exit(main())
