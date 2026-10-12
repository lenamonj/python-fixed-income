"""Checks on the Course 9 data (DATA.md, "Added 2026-10-12: Course 9 data").

Run with: python -m pytest

- The synthetic request log (tools/make_course9_request_log.py): columns, row count, every time_utc inside the 30 days
  and sorted, request_id unique, statuses in the stated set, latencies positive, the three planted features present
  with their stated sizes, and the file rebuilt byte for byte by the tool.
- The masked transcripts (data/course9_transcripts/dayNN/*.txt), when any exist: ASCII, LF, the three-line header,
  no token pattern, no IPv4 address, no email but student@example.com, no unmasked *.vercel.app or *.hf.space host,
  and within the size budget. The account names are checked by the private build's transcript scan, which reads
  them on the build machine; they are never written in a committed file, this one included.
"""
import re
import sys
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
LOG = DATA / "course9_request_log.csv"
TRANSCRIPTS = DATA / "course9_transcripts"
sys.path.insert(0, str(REPO / "tools"))
import make_course9_request_log as maker  # noqa: E402

ROWS = 19_664
STATUSES = {200, 404, 422, 500}
PATHS = {"/health", "/price", "/yield", "/accrued", "/dv01", "/brief", "/checks", "/ask"}
TOKEN = re.compile(r"\bhf_[A-Za-z0-9]{8,}|\bghp_[A-Za-z0-9]{8,}|\bgithub_pat_\w{8,}|\bvercel_[A-Za-z0-9]{8,}"
                   r"|\bsk-(?:or-)?[A-Za-z0-9_-]{8,}|Bearer\s+\S+")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
UNMASKED_HOST = re.compile(r"\b(?!student\b)(?!student-)[a-z0-9-]+\.(?:vercel\.app|hf\.space)\b")
HEADER = ("recorded: ", "command: ", "masked: ")
TRANSCRIPT_BYTES_LIMIT = 40_000


@pytest.fixture(scope="module")
def log() -> pd.DataFrame:
    frame = pd.read_csv(LOG)
    frame["day"] = frame["time_utc"].str[:10]
    return frame


def test_request_log_shape(log: pd.DataFrame) -> None:
    assert list(log.columns[:-1]) == maker.COLUMNS and len(log) == ROWS
    raw = LOG.read_bytes()
    assert raw.isascii() and b"\r\n" not in raw


def test_request_log_times_ids_statuses(log: pd.DataFrame) -> None:
    times = pd.to_datetime(log["time_utc"], format="%Y-%m-%dT%H:%M:%S.%fZ")
    assert times.is_monotonic_increasing
    assert times.min() >= pd.Timestamp("2026-09-03") and times.max() < pd.Timestamp("2026-10-03")
    assert log["day"].nunique() == 30
    assert log["request_id"].is_unique and log["request_id"].str.fullmatch(r"[0-9a-f]{16}").all()
    assert set(log["status"]) == STATUSES and set(log["path"]) == PATHS
    assert (log["latency_ms"] > 0).all() and (log["bytes_out"] > 0).all()
    assert log["refused"].dtype == bool
    assert (log.loc[log["status"] == 404, "path"] == "/ask").all()
    assert (log.loc[log["refused"], "path"] == "/ask").all() and (log.loc[log["refused"], "status"] == 200).all()


def test_planted_slow_day(log: pd.DataFrame) -> None:
    p95 = log[log["path"] == "/dv01"].groupby("day")["latency_ms"].quantile(0.95)
    assert p95.idxmax() == "2026-09-17"
    assert p95["2026-09-17"] > 5 * p95.drop("2026-09-17").median()


def test_planted_422_burst(log: pd.DataFrame) -> None:
    bad = log[log["status"] == 422]
    hour = bad[(bad["day"] == "2026-09-24") & (bad["time_utc"].str[11:13] == "14") & (bad["path"] == "/price")]
    assert len(hour) >= maker.BURST_ROWS
    by_day = bad.groupby("day").size()
    assert by_day.idxmax() == "2026-09-24" and by_day["2026-09-24"] > 10 * by_day.drop("2026-09-24").median()


def test_planted_refused_share(log: pd.DataFrame) -> None:
    ask = log[log["path"] == "/ask"]
    assert abs(ask["refused"].mean() - maker.REFUSED_SHARE) < 0.02
    assert not log.loc[log["path"] != "/ask", "refused"].any()


def test_request_log_rebuilt_by_the_tool() -> None:
    assert maker.log_text().encode("ascii") == LOG.read_bytes()


def _transcripts() -> list[Path]:
    return sorted(TRANSCRIPTS.glob("day*/*.txt")) if TRANSCRIPTS.is_dir() else []


def test_transcripts_masked() -> None:
    for path in _transcripts():
        raw = path.read_bytes()
        assert raw.isascii() and b"\r\n" not in raw, path.name
        assert len(raw) <= TRANSCRIPT_BYTES_LIMIT, path.name
        text = raw.decode("ascii")
        lines = text.splitlines()
        assert len(lines) >= 3 and all(line.startswith(head) for line, head in zip(lines, HEADER)), path.name
        assert not TOKEN.search(text), path.name
        assert not IPV4.search(text), path.name
        assert all(email == "student@example.com" for email in EMAIL.findall(text)), path.name
        assert not UNMASKED_HOST.search(text), path.name
