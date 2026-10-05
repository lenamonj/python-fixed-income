"""Download the UCI "Polish Companies Bankruptcy" dataset and write data/polish_bankruptcy_5year.csv.

Source: UCI Machine Learning Repository, dataset 365
    https://archive.ics.uci.edu/dataset/365/polish+companies+bankruptcy+data
Download, from the UCI site itself, with no account and no key:
    https://archive.ics.uci.edu/static/public/365/polish+companies+bankruptcy+data.zip
The zip holds five ARFF files, 1year.arff to 5year.arff. The course uses 5year.arff only.

Citation, as given on the dataset page:
    Tomczak, S. (2016). Polish Companies Bankruptcy [Dataset]. UCI Machine Learning Repository.
    https://doi.org/10.24432/C5F600.
License, as given on the dataset page: Creative Commons Attribution 4.0 International (CC BY 4.0).

The file in the repo was retrieved on 2026-10-04.

Changes made to the original, and the only ones:
  1. ARFF to CSV. The header row holds the file's own attribute names, Attr1 to Attr64, then class.
  2. The ARFF missing marker ? is written as an empty cell.
  3. class is decoded from the ARFF nominal text '0' or '1' to the whole number 0 or 1.
  4. Every other value is written with Python's repr of the float scipy.io.arff reads, the shortest text that
     reads back to the same number. So 15182 in the ARFF is written 15182.0 and -0.000003 is written -3e-06.

All 5,910 rows and 65 columns are kept, in the file's order. Nothing is recoded, renamed, corrected, sorted, or
dropped (the exact duplicate rows stay; the course drops them in the notebook, as a stated step). After writing,
every cell of the CSV is read back and compared with the ARFF parse: a number must be the same float, bit for bit.

A copy of the zip is kept outside the repo, in CACHE below, so tests/test_course4_data.py can compare the CSV with
the ARFF on the author's machine. The zip itself is never committed.

Author tool: standard library plus scipy, run with the course venv. Students read the CSV.
Usage (from the repo root):

    .venv\\Scripts\\python.exe tools\\get_polish_bankruptcy.py
"""
import csv
import hashlib
import io
import math
import urllib.request
import zipfile
from pathlib import Path

from scipy.io import arff

URL = "https://archive.ics.uci.edu/static/public/365/polish+companies+bankruptcy+data.zip"
ZIP_SHA256 = "17377929aa0b204bbf957e56462cf827c19fe4e2ce89f27dfbc77f9ea2bb16c9"
ARFF_NAME = "5year.arff"
ROWS = 5_910
COLUMNS = [f"Attr{k}" for k in range(1, 65)] + ["class"]
OUT = Path(__file__).resolve().parent.parent / "data" / "polish_bankruptcy_5year.csv"
CACHE = Path.home() / ".cache" / "python-fixed-income" / "polish+companies+bankruptcy+data.zip"


def download_zip() -> bytes:
    """Return the zip from the UCI site, after checking its SHA-256 against the one recorded in DATA.md."""
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != ZIP_SHA256:
        raise RuntimeError(f"the zip's SHA-256 is {digest}, not the recorded {ZIP_SHA256}: the file has changed")
    return payload


def read_arff(payload: bytes) -> list[list]:
    """Parse 5year.arff from the zip: one list per row, floats (nan for ?) then class as the text '0' or '1'."""
    text = zipfile.ZipFile(io.BytesIO(payload)).read(ARFF_NAME).decode("utf-8")
    data, meta = arff.loadarff(io.StringIO(text))
    if list(meta.names()) != COLUMNS:
        raise RuntimeError(f"unexpected attribute names in {ARFF_NAME}: {meta.names()}")
    # each record becomes a plain tuple: 64 floats, then the class as bytes
    records = [row.tolist() for row in data]
    return [[float(value) for value in record[:-1]] + [record[-1].decode("ascii")] for record in records]


def cell_text(value: float) -> str:
    """A ratio as CSV text: empty for a missing value, otherwise Python's repr."""
    return "" if math.isnan(value) else repr(value)


def write_csv(rows: list[list], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(COLUMNS)
        for row in rows:
            if row[-1] not in ("0", "1"):
                raise RuntimeError(f"class must be '0' or '1', found {row[-1]!r}")
            writer.writerow([cell_text(value) for value in row[:-1]] + [int(row[-1])])


def compare_with_arff(rows: list[list], path: Path) -> None:
    """Read the CSV back and stop on the first cell that differs from the ARFF parse."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        if next(reader) != COLUMNS:
            raise RuntimeError("the CSV header differs from the ARFF attribute names")
        written = list(reader)
    if len(written) != len(rows):
        raise RuntimeError(f"the CSV has {len(written)} rows, the ARFF {len(rows)}")
    for i, (parsed, text) in enumerate(zip(rows, written)):
        for name, value, cell in zip(COLUMNS[:-1], parsed[:-1], text[:-1]):
            same = cell == "" if math.isnan(value) else (cell != "" and float(cell) == value)
            if not same:
                raise RuntimeError(f"row {i + 1}, {name}: ARFF {value!r}, CSV {cell!r}")
        if text[-1] != parsed[-1]:
            raise RuntimeError(f"row {i + 1}, class: ARFF {parsed[-1]!r}, CSV {text[-1]!r}")


def main() -> None:
    payload = download_zip()
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_bytes(payload)
    rows = read_arff(payload)
    if len(rows) != ROWS:
        raise RuntimeError(f"expected {ROWS} rows, found {len(rows)}")
    write_csv(rows, OUT)
    compare_with_arff(rows, OUT)
    bankrupt = sum(row[-1] == "1" for row in rows)
    print(f"wrote {OUT.name}: {len(rows)} rows, {len(COLUMNS)} columns, {bankrupt} bankrupt, "
          f"{OUT.stat().st_size} bytes; every cell equals the ARFF parse")
    print(f"zip kept outside the repo for the data tests: {CACHE}")


if __name__ == "__main__":
    main()
