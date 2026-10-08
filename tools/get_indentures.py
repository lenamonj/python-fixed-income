"""Download the three indentures Course 7 reads and write data/course7_indentures/<name>.htm and .txt.

Source: SEC EDGAR, each indenture an exhibit to a Form 8-K (public records on sec.gov; see DATA.md, "EDGAR terms"):
    boyd_2021  Boyd Gaming Corporation, Indenture dated as of June 8, 2021, 4.750% Senior Notes due 2031,
               Exhibit 4.1 to the 8-K filed 2021-06-08, accession 0001193125-21-185495
    levi_2006  Levi Strauss & Co., Indenture dated as of March 17, 2006, 8-7/8% Senior Notes due 2016,
               Exhibit 4.1 to the 8-K filed 2006-03-17, accession 0000950134-06-005445
    lamar_2007 Lamar Media Corp., Indenture dated as of October 11, 2007, 6-5/8% Senior Subordinated Notes due 2015,
               Series C, Exhibit 4.1 to the 8-K filed 2007-10-16, accession 0000950134-07-021393

The .htm is the document as filed, byte for byte (never re-saved): sec.gov's delivery network adds one script tag
just before </BODY> (an address on its own host, no file name; found 2026-10-07, 109 bytes on the Boyd exhibit), which
is not part of the filing, so the tool removes exactly that tag and stops if it finds more than one; the sizes then
equal those the spec's probe recorded. The .txt is the reference textkit.html_to_text of those bytes, so it equals
what day 9's function makes of the .htm. Requests go through the reference textkit.edgar_get with a declared User-Agent built from PFI_SEC_CONTACT (read from the environment after
loading the repo-root .env; never written), at most one request per 0.11 s.

Usage (from the repo root, with the course Python):  python tools/get_indentures.py
"""
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import course7_reference  # noqa: E402

OUT = course7_reference.REPO / "data" / "course7_indentures"
# the tag sec.gov's delivery network injects before </BODY>: a script loaded from an address on its own host
INJECTED = re.compile(rb'<script type="text/javascript"\s+src="/[A-Za-z0-9/_-]+"></script>(?=</BODY>)', re.IGNORECASE)
INDENTURES = {
    "boyd_2021": "https://www.sec.gov/Archives/edgar/data/906553/000119312521185495/d185267dex41.htm",
    "levi_2006": "https://www.sec.gov/Archives/edgar/data/94845/000095013406005445/f18762exv4w1.htm",
    "lamar_2007": "https://www.sec.gov/Archives/edgar/data/899045/000095013407021393/d50558exv4w1.htm",
}


def main() -> None:
    textkit = course7_reference.textkit()
    headers = textkit.sec_headers(*course7_reference.sec_contact())
    OUT.mkdir(parents=True, exist_ok=True)
    for name, url in INDENTURES.items():
        served = textkit.edgar_get(url, headers)
        raw, injected = INJECTED.subn(b"", served)
        if injected > 1:
            raise SystemExit(f"{name}: {injected} injected script tags; expected at most one")
        if not raw.lstrip()[:200].lower().startswith((b"<html", b"<!doctype", b"<document", b"<?xml")) \
                and b"<html" not in raw[:2000].lower():
            raise SystemExit(f"{name}: the response does not look like an HTML document")
        (OUT / f"{name}.htm").write_bytes(raw)
        text = textkit.html_to_text(raw)
        (OUT / f"{name}.txt").write_text(text, encoding="utf-8", newline="\n")
        print(f"{name}: {len(served):,} bytes served, {injected} injected tag removed, {len(raw):,} bytes as filed "
              f"(SHA-256 {hashlib.sha256(raw).hexdigest()}), {len(text):,} characters and {len(text.split()):,} words of text")


if __name__ == "__main__":
    main()
