"""Compute the course's two pinned models on the 8-K sections once: data/course7_8k_minilm.npy and
data/course7_8k_zero_shot.csv.

Days 7 and 10 need the embeddings of every section and the zero-shot scores of every validation and test section,
which take far longer than a notebook's budget on one thread; so they are computed here, once, with the reference
textkit (the same functions, models, revisions, labels, and template the notebooks use), and each notebook recomputes
a seeded sample live and checks it against these files (COURSE7_SPEC.md, "Run-time budget").

- course7_8k_minilm.npy: float32, one row per row of course7_8k_items.csv in file order, 384 numbers, each row of
  length 1: textkit.embed(load_model("embedding"), texts, batch_size=64) on the section texts as stored.
- course7_8k_zero_shot.csv: one row per section filed in 2024 (validation) or 2025 (test): accession, item (the
  filer's item, text), split, the score of each of the eight labels (columns score_1.01 ... score_5.02, in
  ITEM_LABELS' order, six decimals), and revision (the zero-shot model's pinned commit). Each text is the section's
  first 120 words; textkit.zero_shot_scores with LABEL_TEMPLATE, multi_label=False.

One thread for every library (set before numpy and torch are imported). Usage (from the repo root, with the course
Python, after tools/get_8k_items.py):  python tools/make_8k_model_outputs.py
"""
import os

for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[name] = "1"
os.environ.update(TOKENIZERS_PARALLELISM="false", HF_HUB_DISABLE_PROGRESS_BARS="1", TRANSFORMERS_VERBOSITY="error")

import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import torch  # noqa: E402

torch.set_num_threads(1)
torch.set_num_interop_threads(1)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import course7_reference  # noqa: E402

DATA = course7_reference.REPO / "data"
WORDS = 120
# the course's eight label descriptions, in item order, and the hypothesis template (COURSE7_SPEC.md, "Conventions")
ITEM_LABELS = {
    "1.01": "an agreement the company entered into",
    "1.03": "a bankruptcy or receivership filing",
    "2.02": "the company's financial results for a quarter or a year",
    "2.03": "a new loan, note, or other debt of the company",
    "2.04": "an event that accelerates a debt obligation",
    "2.06": "an impairment charge on assets",
    "3.01": "a notice of delisting from a stock exchange",
    "5.02": "a director or officer leaving or joining the company",
}
LABEL_TEMPLATE = "This section of a company's current report is about {}."


def main() -> None:
    textkit = course7_reference.textkit()
    sections = pd.read_csv(DATA / "course7_8k_items.csv", dtype={"item": str})
    started = time.perf_counter()
    model = textkit.load_model("embedding")
    vectors = textkit.embed(model, sections["text"].tolist(), batch_size=64)
    np.save(DATA / "course7_8k_minilm.npy", vectors, allow_pickle=False)
    print(f"course7_8k_minilm.npy: {vectors.shape}, {vectors.dtype}, {time.perf_counter() - started:.0f} s", flush=True)

    started = time.perf_counter()
    year = sections["filed"].str[:4]
    chosen = sections[year.isin(["2024", "2025"])].copy()
    texts = [" ".join(text.split()[:WORDS]) for text in chosen["text"]]
    pipe = textkit.load_model("zero_shot")
    scores = textkit.zero_shot_scores(pipe, texts, list(ITEM_LABELS.values()), LABEL_TEMPLATE)
    scores.columns = [f"score_{item}" for item in ITEM_LABELS]
    table = pd.concat([chosen[["accession", "item"]].reset_index(drop=True),
                       pd.Series(np.where(chosen["filed"].str[:4] == "2024", "validation", "test"), name="split"),
                       scores.reset_index(drop=True)], axis=1)
    table["revision"] = textkit.MODELS["zero_shot"]["revision"]
    table.to_csv(DATA / "course7_8k_zero_shot.csv", index=False, float_format="%.6f", lineterminator="\n")
    print(f"course7_8k_zero_shot.csv: {len(table)} rows ({(table['split'] == 'validation').sum()} validation), "
          f"{time.perf_counter() - started:.0f} s")


if __name__ == "__main__":
    main()
