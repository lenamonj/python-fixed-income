"""Download the UCI "Default of Credit Card Clients" dataset and write data/credit_card_default.csv.

Source: UCI Machine Learning Repository, dataset 350
    https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
Download, from the UCI site itself, with no account and no key:
    https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip
The zip holds one file, "default of credit card clients.xls", with one sheet, "Data".

Citation, as given on the dataset page:
    Yeh, I. (2009). Default of Credit Card Clients [Dataset]. UCI Machine Learning Repository.
    https://doi.org/10.24432/C55S3H.
License, as given on the dataset page: Creative Commons Attribution 4.0 International (CC BY 4.0),
    https://creativecommons.org/licenses/by/4.0/legalcode

The file in the repo was retrieved on 2026-10-03.

Changes made to the original, and the only ones:
  1. The sheet carries two header rows. The first holds the labels X1 to X23 and Y, and the second
     holds the column names (ID, LIMIT_BAL, ... , default payment next month). The first is dropped
     and the second is kept as the header.
  2. The sheet is saved as CSV. Every cell of the sheet is a whole number, and is written as one.

All 30,000 rows and all 25 columns are kept, with their original names and values. Nothing is
recoded, renamed, corrected, sorted, or dropped.

Reading .xls needs the xlrd package, which is pinned in requirements-dev.txt. It is an author tool
and is not in the course requirements: students read the CSV.

Usage (from the repo root):

    python tools/get_credit_card_default.py
"""
import io
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

URL = "https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip"
XLS_NAME = "default of credit card clients.xls"
ROWS, COLUMNS = 30_000, 25
OUT = Path(__file__).resolve().parent.parent / "data" / "credit_card_default.csv"


def download_sheet() -> pd.DataFrame:
    """Return the sheet as published, with its second row as the header."""
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        archive = zipfile.ZipFile(io.BytesIO(response.read()))
    with archive.open(XLS_NAME) as xls:
        # header=1 skips the first row (X1 to X23, Y) and takes the names from the second
        return pd.read_excel(io.BytesIO(xls.read()), sheet_name="Data", header=1, engine="xlrd")


def main() -> None:
    table = download_sheet()
    if table.shape != (ROWS, COLUMNS):
        raise RuntimeError(f"expected {ROWS} rows and {COLUMNS} columns, found {table.shape}")
    if table.columns[0] != "ID" or table.columns[-1] != "default payment next month":
        raise RuntimeError(f"unexpected column names: {list(table.columns)}")
    if not all(pd.api.types.is_integer_dtype(dtype) for dtype in table.dtypes):
        raise RuntimeError(f"a column is not whole numbers:\n{table.dtypes}")

    table.to_csv(OUT, index=False, lineterminator="\n")
    print("wrote", OUT, "-", len(table), "rows,", table.shape[1], "columns,", OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
