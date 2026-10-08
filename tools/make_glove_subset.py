"""Write data/course7_glove_6b_100d.npz: a subset of the GloVe 6B word vectors, 100 numbers per word.

Source: Jeffrey Pennington, Richard Socher, Christopher D. Manning, GloVe: Global Vectors for Word Representation,
https://nlp.stanford.edu/projects/glove/ (read 2026-10-07): vectors trained on Wikipedia 2014 and Gigaword 5 (6
billion tokens, a 400,000-word uncased vocabulary). "This data is made available under the Public Domain Dedication
and License v1.0", so a subset may be redistributed; the course cites the authors.

What is kept, in GloVe's own order (the file lists the most frequent words first): the first 40,000 words, plus every
token of the course's texts that GloVe has (the FOMC statements, the three indentures, and the 8-K sections, each
tokenized by the reference textkit.tokenize, lower case). A text file not yet in data/ is skipped and named.

The zip (glove.6B.zip, 862,182,613 bytes) is downloaded once to the user's cache folder (~/.cache/python-fixed-income),
outside the repo, and never committed; the tool stops if its SHA-256 differs from the one recorded below. The .npz is
written with a fixed date in its zip entries, so two runs on the same inputs give the same bytes.

Usage (from the repo root, with the course Python):  python tools/make_glove_subset.py
"""
import hashlib
import io
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import course7_reference  # noqa: E402

URL = "https://nlp.stanford.edu/data/glove.6B.zip"
ZIP = Path.home() / ".cache" / "python-fixed-income" / "glove.6B.zip"
ZIP_SHA256 = "617afb2fe6cbd085c235baf7a465b96f4112bd7f7ccb2b2cbd649fed9cbcf2fb"
MEMBER = "glove.6B.100d.txt"
TOP_WORDS = 40_000
DATA = course7_reference.REPO / "data"
OUT = DATA / "course7_glove_6b_100d.npz"
TEXT_FILES = ["course7_fomc_statements.csv", "course7_8k_items.csv", "course7_indentures/boyd_2021.txt",
              "course7_indentures/levi_2006.txt", "course7_indentures/lamar_2007.txt"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for block in iter(lambda: file.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def course_tokens() -> set[str]:
    textkit = course7_reference.textkit()
    tokens = set()
    for name in TEXT_FILES:
        path = DATA / name
        if not path.is_file():
            print(f"not in data/ yet, skipped: {name}")
            continue
        texts = pd.read_csv(path)["text"].tolist() if path.suffix == ".csv" else [path.read_text(encoding="utf-8")]
        for text in texts:
            tokens.update(textkit.tokenize(text))
    return tokens


def main() -> None:
    if not ZIP.is_file():
        ZIP.parent.mkdir(parents=True, exist_ok=True)
        partial = ZIP.with_suffix(".part")
        with urllib.request.urlopen(URL, timeout=600) as response, open(partial, "wb") as file:
            shutil.copyfileobj(response, file)
        partial.rename(ZIP)
    if sha256(ZIP) != ZIP_SHA256:
        raise SystemExit(f"{ZIP.name} has another SHA-256 than the one recorded: check the download")
    wanted = course_tokens()
    words, rows = [], []
    with zipfile.ZipFile(ZIP) as archive, archive.open(MEMBER) as raw:
        for position, line in enumerate(io.TextIOWrapper(raw, encoding="utf-8")):
            word, *numbers = line.rstrip("\n").split(" ")
            if position < TOP_WORDS or word in wanted:
                words.append(word)
                rows.append(np.array(numbers, dtype=np.float32))
    vectors = np.vstack(rows)
    if vectors.shape != (len(words), 100) or len(set(words)) != len(words):
        raise SystemExit("unexpected shape or repeated words")
    # an .npz is a zip of .npy files; written by hand so each entry has a fixed date and the file is reproducible
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as out:
        for name, array in (("vectors", vectors), ("words", np.array(words))):
            buffer = io.BytesIO()
            np.lib.format.write_array(buffer, array, allow_pickle=False)
            out.writestr(zipfile.ZipInfo(f"{name}.npy", date_time=(1980, 1, 1, 0, 0, 0)), buffer.getvalue(),
                         compress_type=zipfile.ZIP_DEFLATED)
    found = len(words) - TOP_WORDS
    print(f"wrote {len(words):,} words ({TOP_WORDS:,} most frequent plus {found:,} course words), "
          f"{OUT.stat().st_size:,} bytes, to {OUT.name}; course tokens {len(wanted):,}, "
          f"{len(wanted & set(words)):,} in GloVe")


if __name__ == "__main__":
    main()
