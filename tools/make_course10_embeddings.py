"""Embed the Course 10 chunk sets once, on one thread, and write data/course10_embeddings/.

The chunk sets are made by the reference ragkit (the functions the notebooks teach), from the committed documents:

    boyd10k_512_64_<model>      the 10-K PDF (data/course10_boyd_10k_2025.pdf), items from its HTML, recursive_split at
    boyd10k_1024_128_<model>    512/64 and 1,024/128, by each of minilm, bge_small, and gte_small
    corpus_512_64_minilm        the 10-K and the three indentures (Boyd 2021, Levi 2006, Lamar 2007) at 512/64
    boyd10q_512_64_minilm       the 10-Q (Part I and Part II items) at 512/64

Each .npy holds float32, one unit-length row per chunk in chunk-table order (ragkit.embed_chunks: textkit.embed with
batch 64, normalize_embeddings=True). Each .json sidecar holds the model's key, id, and revision, the chunker's
settings, the documents, the chunk count, the SHA-256 of the chunk texts (what ragkit.load_embeddings checks), and the
SHA-256 of the matrix's bytes. A notebook embeds a seeded sample live and compares it with these rows within 1e-6.

Author tool, run with the course Python and the Course 10 build cache:
    set HF_HOME=%LOCALAPPDATA%\\pfi_course10_hf_cache & set HF_HUB_OFFLINE=1
    python tools/make_course10_embeddings.py
It prints the seconds each set took on one thread (for the build README), never writes them to a data file.
"""
import os

if __name__ == "__main__":
    # one thread for the maths libraries, before numpy is imported: the rows must not depend on threads (the data
    # test imports this module for chunk_sets only and sets nothing)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[name] = "1"
    os.environ.update(TOKENIZERS_PARALLELISM="false", HF_HUB_DISABLE_PROGRESS_BARS="1", TRANSFORMERS_VERBOSITY="error")

import hashlib  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import course10_reference  # noqa: E402

REPO = course10_reference.REPO
DATA = REPO / "data"
OUT = DATA / "course10_embeddings"
TEN_Q_PART_I = ["1", "2", "3", "4"]
TEN_Q_PART_II = ["1", "1A", "2", "5", "6"]


def tenk_pieces(ragkit) -> pd.DataFrame:
    """The 10-K's pages cut at its items (ragkit.page_items with textkit.split_items on the HTML)."""
    import textkit
    items = textkit.split_items(textkit.html_to_text((DATA / "course7_boyd_10k_2025.htm").read_bytes()),
                                ragkit.TEN_K_ITEMS)
    return ragkit.page_items(ragkit.pdf_pages(DATA / "course10_boyd_10k_2025.pdf"), items)


def tenq_pieces() -> pd.DataFrame:
    """The 10-Q's text cut at its items, part by part, in page_items' shape (page 0: no page layout is committed);
    items are named "I.2" and "II.1A"; text before Part I's Item 1 is "cover"."""
    import textkit
    text = textkit.html_to_text((DATA / "course10_boyd_10q_2026q2.htm").read_bytes())
    cut = text.index("\nPART II. Other Information")
    rows = [{"page": 0, "item": "cover", "text": text[:textkit.split_items(text[:cut], TEN_Q_PART_I)["start"].iloc[0]]}]
    for part, body, codes in (("I", text[:cut], TEN_Q_PART_I), ("II", text[cut:], TEN_Q_PART_II)):
        table = textkit.split_items(body, codes)
        for item, start, end in zip(table["item"], table["start"], table["end"]):
            rows.append({"page": 0, "item": f"{part}.{item}", "text": body[start:end]})
    frame = pd.DataFrame(rows)
    return frame.assign(chars=frame["text"].str.len(), printed_page="")


def chunk_sets(ragkit) -> dict:
    """{set name: (chunk table, documents)} for every committed set."""
    tenk = tenk_pieces(ragkit)
    indentures = {doc: (DATA / "course7_indentures" / f"{file}.txt").read_text(encoding="utf-8")
                  for doc, file in (("boyd2021", "boyd_2021"), ("levi2006", "levi_2006"), ("lamar2007", "lamar_2007"))}
    sets = {}
    for size, overlap in ((512, 64), (1024, 128)):
        sets[f"boyd10k_{size}_{overlap}"] = (ragkit.chunk_table(tenk, size, overlap, "boyd10k"), ["boyd10k"])
    corpus = ragkit.corpus_chunks({"boyd10k": tenk} | indentures, 512, 64, as_of={"boyd10k": "2025-12-31"})
    sets["corpus_512_64"] = (corpus, ["boyd10k", "boyd2021", "levi2006", "lamar2007"])
    sets["boyd10q_512_64"] = (ragkit.chunk_table(tenq_pieces(), 512, 64, "boyd10q"), ["boyd10q"])
    return sets


PLAN = {"boyd10k_512_64": ("minilm", "bge_small", "gte_small"), "boyd10k_1024_128": ("minilm", "bge_small", "gte_small"),
        "corpus_512_64": ("minilm",), "boyd10q_512_64": ("minilm",)}


def main() -> None:
    import torch
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    ragkit = course10_reference.ragkit()
    OUT.mkdir(exist_ok=True)
    sets = chunk_sets(ragkit)
    for key in ("minilm", "bge_small", "gte_small"):
        model = ragkit.load_embedder(key)
        for name, models in PLAN.items():
            if key not in models:
                continue
            chunks, documents = sets[name]
            started = time.perf_counter()
            matrix = ragkit.embed_chunks(model, chunks)
            seconds = time.perf_counter() - started
            stem = f"{name}_{key}"
            np.save(OUT / f"{stem}.npy", matrix)
            size, overlap = int(name.split("_")[-2]), int(name.split("_")[-1])
            sidecar = {"model": {"key": key, "id": ragkit.EMBEDDERS[key]["id"],
                                 "revision": ragkit.EMBEDDERS[key]["revision"]},
                       "chunker": {"size": size, "overlap": overlap}, "documents": documents, "chunks": len(chunks),
                       "chunk_text_sha256": ragkit._text_hash(chunks["text"]),
                       "matrix_sha256": hashlib.sha256(matrix.tobytes()).hexdigest(),
                       "embed": "ragkit.embed_chunks (textkit.embed, batch 64, normalize_embeddings=True), one thread"}
            (OUT / f"{stem}.json").write_text(json.dumps(sidecar, indent=1, sort_keys=True) + "\n", encoding="ascii",
                                              newline="\n")
            print(f"{stem}: {len(chunks)} chunks, {seconds:.1f} s on one thread, {(OUT / f'{stem}.npy').stat().st_size:,} bytes")


if __name__ == "__main__":
    sys.exit(main())
