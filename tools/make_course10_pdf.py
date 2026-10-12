"""Print the Boyd 10-K to PDF with Microsoft Edge: data/course10_boyd_10k_2025.pdf.

Course 7's method (tools/make_indenture_pdf.py): data/course7_boyd_10k_2025.htm, the 10-K as filed (tools/
get_edgar_filings.py), is opened from disk by Edge in headless mode and printed with no header or footer. The text is
the SEC copy's; the page layout is Edge's. Nothing is fetched: Edge reads the local file only, with a fresh profile in
a temp folder.

After printing, the tool checks the text layer: every page's text, read by the reference textkit.pdf_text (pypdf,
then normalize_text), is looked for in textkit.html_to_text of the HTML, after both are reduced to letters and digits
(a PDF's text layer breaks lines and table cells differently from the HTML). It prints the page count, the size,
the SHA-256, Edge's version, and the pages whose text is not found, with the share of their characters found.

A PDF holds its creation date, so two runs give different bytes; DATA.md records the committed file's SHA-256, page
count, and the Edge version that printed it. Author tool, Windows with Edge only; a student never runs it.

Usage (from the repo root, with the course Python):  python tools/make_course10_pdf.py
"""
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import course7_reference  # noqa: E402
from make_indenture_pdf import EDGE, edge_version  # noqa: E402

REPO = course7_reference.REPO
SOURCE = REPO / "data" / "course7_boyd_10k_2025.htm"
OUT = REPO / "data" / "course10_boyd_10k_2025.pdf"


def squeeze(text: str) -> str:
    """Letters and digits only, lower case: the form in which a page's text is compared with the HTML's."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def page_check(pdf: Path, html: Path) -> list[tuple[int, int, float]]:
    """(page from 1, characters, share of the page's squeezed text found in the HTML in pieces of 40 characters)
    for every page whose squeezed text is not found whole in the squeezed HTML text."""
    textkit = course7_reference.textkit()
    whole = squeeze(textkit.html_to_text(html.read_bytes()))
    missing = []
    for number, text in enumerate(textkit.pdf_text(pdf), start=1):
        page = squeeze(text)
        if page and page not in whole:
            pieces = [page[i:i + 40] for i in range(0, len(page), 40)]
            found = sum(piece in whole for piece in pieces) / len(pieces)
            missing.append((number, len(text), found))
    return missing


def main() -> None:
    if not EDGE.is_file():
        raise SystemExit("Microsoft Edge is not installed where this tool looks for it")
    profile = Path(tempfile.mkdtemp(prefix="pfi_course10_edge_"))
    try:
        result = subprocess.run([str(EDGE), "--headless", "--disable-gpu", "--no-first-run", "--no-pdf-header-footer",
                                 f"--user-data-dir={profile}", f"--print-to-pdf={OUT}", SOURCE.as_uri()],
                                capture_output=True, text=True, timeout=600)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    if not OUT.is_file():
        raise SystemExit(f"Edge wrote no PDF (return code {result.returncode})")
    from pypdf import PdfReader
    pages = len(PdfReader(OUT).pages)
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(f"wrote {OUT.name}: {pages} pages, {OUT.stat().st_size:,} bytes, SHA-256 {digest}, Edge {edge_version()}")
    missing = page_check(OUT, SOURCE)
    print(f"pages whose text is not found whole in the HTML text: {len(missing)}")
    for number, chars, share in missing:
        print(f"  page {number}: {chars} characters, {share:.1%} of its 40-character pieces found")


if __name__ == "__main__":
    sys.exit(main())
