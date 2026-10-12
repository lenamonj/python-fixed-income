"""Checks on the Bonus course's data (DATA.md, "Added 2026-10-12: Bonus course data").

Run with: python -m pytest

- The workspace seed (SEED_FILES in course_bonus_coding_agent/deploy/app.py, read by ast, not imported): three files,
  the fictional label, six bonds B001 to B006 of invented issuers (none in data/holdings.csv), no CUSIP, the high
  yield rows B002, B004, B006, ASCII.
- The saved runs (data/bonus_agent_runs/<key>.json), when they exist: Course 8's four fields, the file named by the
  SHA-256 of the request's method, path, and body, written as the transport writes, no header field, no key-like
  string, path /v1/responses, store false, no absolute path in a request.
- The masked transcripts (data/bonus_transcripts/*.txt), when they exist: Course 9's rules (ASCII, LF, the three
  header lines, no token, no IPv4 address, no email but student@example.com, no unmasked *.hf.space host, within the
  size budget). The account names are checked by the private build's scan, never written in a committed file.
"""
import ast
import csv
import hashlib
import io
import json
import re
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
APP = REPO / "course_bonus_coding_agent" / "deploy" / "app.py"
RUNS = REPO / "data" / "bonus_agent_runs"
TRANSCRIPTS = REPO / "data" / "bonus_transcripts"
TOKEN = re.compile(r"\bhf_[A-Za-z0-9]{8,}|\bghp_[A-Za-z0-9]{8,}|\bsk-(?:or-)?[A-Za-z0-9_-]{8,}|Bearer\s+\S+")
HEADER_FIELD = re.compile(r"authorization|api[_-]?key|^x-|cookie|token", re.I)
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
UNMASKED_HOST = re.compile(r"\b(?!student\b)(?!student-)[a-z0-9-]+\.hf\.space\b")
ABSOLUTE_PATH = re.compile(r"AppData|\\Users\\|/Users/|/home/|/tmp/|pfi_bonus_\d\d_", re.I)


def seed_files() -> dict:
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "SEED_FILES")
    return ast.literal_eval(node.value)


def test_seed_files_are_fictional_and_labelled():
    seed = seed_files()
    assert set(seed) == {"README.txt", "desk_riddle.txt", "bonds.csv"}
    assert all(text.isascii() for text in seed.values())
    assert "Every issuer, bond, and price in here is fictional" in seed["README.txt"]
    bonds = list(csv.DictReader(io.StringIO(seed["bonds.csv"])))
    assert list(bonds[0]) == ["bond_id", "issuer", "coupon", "maturity", "rating", "price"]
    assert [b["bond_id"] for b in bonds] == [f"B00{i}" for i in range(1, 7)]
    holdings = set(pd.read_csv(REPO / "data" / "holdings.csv")["issuer"])
    assert not {b["issuer"] for b in bonds} & holdings
    assert not any(re.fullmatch(r"[0-9A-Z]{9}", value) for b in bonds for value in b.values())
    high_yield = [b["bond_id"] for b in bonds if b["rating"] in ("BB+", "BB", "BB-", "B+", "B", "B-")]
    assert high_yield == ["B002", "B004", "B006"]
    assert "zero" not in seed["desk_riddle.txt"].lower() and "buy" not in seed["desk_riddle.txt"].lower()


def _keys(value):
    if isinstance(value, dict):
        for k, v in value.items():
            yield k
            yield from _keys(v)
    elif isinstance(value, list):
        for v in value:
            yield from _keys(v)


def test_saved_runs():
    files = sorted(RUNS.glob("*.json")) if RUNS.is_dir() else []
    if not files:
        pytest.skip("the saved runs are recorded at checkpoint 1")
    for path in files:
        raw = path.read_text(encoding="utf-8")
        record = json.loads(raw)
        assert set(record) == {"path", "recorded", "request", "response"}, path.name
        canonical = json.dumps({"method": "POST", "path": record["path"], "body": record["request"]},
                               sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        assert path.stem == hashlib.sha256(canonical.encode("ascii")).hexdigest(), path.name
        assert raw == json.dumps(record, sort_keys=True, indent=1, ensure_ascii=True) + "\n", path.name
        assert not any(HEADER_FIELD.search(str(k)) for k in _keys(record)), path.name
        assert not TOKEN.search(raw), path.name
        assert record["path"] == "/v1/responses" and record["request"]["store"] is False, path.name
        assert not ABSOLUTE_PATH.search(json.dumps(record["request"])), path.name


def test_transcripts():
    files = sorted(TRANSCRIPTS.glob("*.txt")) if TRANSCRIPTS.is_dir() else []
    if not files:
        pytest.skip("the transcripts are recorded at checkpoint 3")
    assert sum(p.stat().st_size for p in files) <= 60_000
    for path in files:
        raw = path.read_bytes()
        assert raw.isascii() and b"\r\n" not in raw and len(raw) <= 40_000, path.name
        text = raw.decode("ascii")
        assert [line.split(": ")[0] for line in text.splitlines()[:3]] == ["recorded", "command", "masked"], path.name
        assert not TOKEN.search(text) and not IPV4.search(text) and not UNMASKED_HOST.search(text), path.name
        assert all(e.lower() == "student@example.com" for e in EMAIL.findall(text)), path.name
