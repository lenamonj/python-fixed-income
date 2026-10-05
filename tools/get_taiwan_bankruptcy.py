"""Download the UCI "Taiwanese Bankruptcy Prediction" dataset and write data/taiwan_bankruptcy.csv.

Source: UCI Machine Learning Repository, dataset 572
    https://archive.ics.uci.edu/dataset/572/taiwanese+bankruptcy+prediction
Download, from the UCI site itself, with no account and no key:
    https://archive.ics.uci.edu/static/public/572/taiwanese+bankruptcy+prediction.zip
The zip holds one file, data.csv.

Citation, as given on the dataset page:
    Taiwanese Bankruptcy Prediction [Dataset]. (2020). UCI Machine Learning Repository.
    https://doi.org/10.24432/C5004D.
License, as given on the dataset page: Creative Commons Attribution 4.0 International (CC BY 4.0).

The file in the repo was retrieved on 2026-10-05.

The only change made to the original is the file name: data.csv is written to data/taiwan_bankruptcy.csv byte for
byte. Nothing is parsed, recoded, renamed, sorted, or dropped. The column names keep their leading spaces and the
yen sign in three names; the Course 5 capstone cleans the names in the notebook, as a stated step.

The tool stops unless the zip's size and SHA-256 and the member's SHA-256 equal the ones recorded below (and in
DATA.md). A copy of the zip is kept outside the repo, in CACHE below, so tests/test_course5_data.py can compare the
CSV with the zip's member on the author's machine. The zip itself is never committed.

Author tool: standard library only. Students read the CSV.
Usage (from the repo root):

    .venv\\Scripts\\python.exe tools\\get_taiwan_bankruptcy.py
"""
import hashlib
import io
import urllib.request
import zipfile
from pathlib import Path

URL = "https://archive.ics.uci.edu/static/public/572/taiwanese+bankruptcy+prediction.zip"
ZIP_BYTES = 4_808_883
ZIP_SHA256 = "c346f5ad2618cb198e7ed8306cf2f31fe3bb2ec60acdbbe1736788d50f269aac"
MEMBER = "data.csv"
MEMBER_SHA256 = "67bf2e7c75490f7ad3f76bbce57d49cdc25967cdab607527b94f944863fa14d8"
OUT = Path(__file__).resolve().parent.parent / "data" / "taiwan_bankruptcy.csv"
CACHE = Path.home() / ".cache" / "python-fixed-income" / "taiwanese+bankruptcy+prediction.zip"


def download_zip() -> bytes:
    """Return the zip from the UCI site, after checking its size and SHA-256 against the recorded ones."""
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        payload = response.read()
    if len(payload) != ZIP_BYTES:
        raise RuntimeError(f"the zip is {len(payload)} bytes, not the recorded {ZIP_BYTES}: the file has changed")
    digest = hashlib.sha256(payload).hexdigest()
    if digest != ZIP_SHA256:
        raise RuntimeError(f"the zip's SHA-256 is {digest}, not the recorded {ZIP_SHA256}: the file has changed")
    return payload


def read_member(payload: bytes) -> bytes:
    """Return data.csv from the zip, after checking the zip holds only it and its SHA-256 is the recorded one."""
    archive = zipfile.ZipFile(io.BytesIO(payload))
    names = archive.namelist()
    if names != [MEMBER]:
        raise RuntimeError(f"the zip should hold only {MEMBER}, it holds {names}")
    member = archive.read(MEMBER)
    digest = hashlib.sha256(member).hexdigest()
    if digest != MEMBER_SHA256:
        raise RuntimeError(f"{MEMBER}'s SHA-256 is {digest}, not the recorded {MEMBER_SHA256}")
    return member


def main() -> None:
    payload = download_zip()
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_bytes(payload)
    member = read_member(payload)
    OUT.write_bytes(member)
    if OUT.read_bytes() != member:
        raise RuntimeError(f"{OUT.name} on disk differs from the zip's {MEMBER}")
    lines = member.count(b"\n")
    print(f"wrote {OUT.name}: {len(member)} bytes, {lines} lines, byte for byte the zip's {MEMBER} "
          f"(SHA-256 {MEMBER_SHA256[:12]}...)")
    print(f"zip kept outside the repo for the data tests: {CACHE.name}, in the user's cache folder")


if __name__ == "__main__":
    main()
