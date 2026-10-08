"""Print the Boyd indenture to PDF with Microsoft Edge: data/course7_boyd_2021_indenture.pdf.

EDGAR holds no PDF of the indenture (each filing's index lists HTML, XBRL, and images only), so the course prints
the SEC copy itself: data/course7_indentures/boyd_2021.htm, the exhibit as filed (tools/get_indentures.py), is
opened from disk by Edge in headless mode and printed with no header or footer. The text is the SEC copy's; the
page layout is Edge's. Nothing is fetched: Edge reads the local file only, with a fresh profile in a temp folder.

A PDF holds its creation date, so two runs give different bytes; DATA.md records the committed file's SHA-256, page
count, and the Edge version that printed it. Author tool, Windows with Edge only; a student never runs it.

Usage (from the repo root, with the course Python):  python tools/make_indenture_pdf.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from pypdf import PdfReader

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "data" / "course7_indentures" / "boyd_2021.htm"
OUT = REPO / "data" / "course7_boyd_2021_indenture.pdf"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def edge_version() -> str:
    command = f"(Get-Item '{EDGE}').VersionInfo.ProductVersion"
    return subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True,
                          check=True).stdout.strip()


def main() -> None:
    if not EDGE.is_file():
        raise SystemExit("Microsoft Edge is not installed where this tool looks for it")
    profile = Path(tempfile.mkdtemp(prefix="pfi_course7_edge_"))
    try:
        result = subprocess.run([str(EDGE), "--headless", "--disable-gpu", "--no-first-run", "--no-pdf-header-footer",
                                 f"--user-data-dir={profile}", f"--print-to-pdf={OUT}", SOURCE.as_uri()],
                                capture_output=True, text=True, timeout=300)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    if not OUT.is_file():
        raise SystemExit(f"Edge wrote no PDF (return code {result.returncode})")
    pages = len(PdfReader(OUT).pages)
    print(f"wrote {OUT.name}: {pages} pages, {OUT.stat().st_size:,} bytes, Edge {edge_version()}")


if __name__ == "__main__":
    sys.exit(main())
