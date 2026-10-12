"""Write data/course9_request_log.csv: a synthetic request log for a small bond and desk service, 30 days.

Course 9 (Deployment) reads it on days 12, 14, and the capstone to teach request logs, latency percentiles, error
counts, and a free-tier line. It is invented here: no real service, no real client, and no real request produced it.

Columns, one row per request, sorted by time:
    time_utc     ISO 8601 in UTC with milliseconds, "2026-09-03T14:05:09.123Z"
    request_id   16 hexadecimal characters, unique (the first 16 of the SHA-256 of the seed and the row's draw)
    path         /health, /price, /yield, /accrued, /dv01, /brief, /checks, /ask
    status       HTTP status: 200, 404 (a question not in the saved runs, /ask only), 422 (a request body the service
                 refused), 500 (rare, any path but /health)
    latency_ms   milliseconds from request to response, 1 decimal, positive
    bytes_out    size of the response body in bytes
    refused      true when the desk service returned its refusal line to a request for a view (/ask only), else false

No query value, request body, header, or client address is in the log (COURSE9_SPEC.md, "Leakage", rule 4).

Three features are planted for the lessons, each stated in DATA.md and in the notebooks:
    1. A slow day on /dv01: on 2026-09-17 every /dv01 latency is multiplied by SLOW_FACTOR.
    2. A burst of 422s: on 2026-09-24 from 14:00 to 14:59 UTC, BURST_ROWS extra POSTs to /price, every one 422
       (one client sending a malformed body; the log cannot say which client, by design).
    3. A refused share on /ask: each /ask request is refused with probability REFUSED_SHARE (status 200, refused
       true, the refusal line's size).

Deterministic: numpy's default_rng(SEED). Rerunning it gives the same bytes. ASCII, LF.

Usage:  .venv\\Scripts\\python.exe tools\\make_course9_request_log.py
"""
import hashlib
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "course9_request_log.csv"
SEED = 9
FIRST_DAY = date(2026, 9, 3)
DAYS = 30
COLUMNS = ["time_utc", "request_id", "path", "status", "latency_ms", "bytes_out", "refused"]
# mean requests a day, before the planted burst
DAILY_MEAN = 660
# share of requests by path, and each path's median latency in ms and typical response size in bytes
PATHS = {
    "/health": (0.15, 3.0, 60),
    "/price": (0.24, 11.0, 140),
    "/yield": (0.08, 13.0, 140),
    "/accrued": (0.07, 9.0, 140),
    "/dv01": (0.24, 12.0, 150),
    "/brief": (0.10, 24.0, 5200),
    "/checks": (0.05, 18.0, 2400),
    "/ask": (0.07, 28.0, 900),
}
# relative traffic by UTC hour: quiet overnight, busiest in the hours a US desk works
HOUR_WEIGHTS = np.array([2, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 8, 10, 12, 13, 13, 12, 11, 10, 8, 6, 4, 3, 2], float)
LATENCY_SIGMA = 0.45
SLOW_DAY = date(2026, 9, 17)
SLOW_FACTOR = 6.0
BURST_DAY = date(2026, 9, 24)
BURST_HOUR = 14
BURST_ROWS = 240
REFUSED_SHARE = 0.08
NOT_FOUND_SHARE = 0.12
BAD_BODY_SHARE = 0.01
SERVER_ERROR_SHARE = 0.0005
POST_PATHS = ("/price", "/yield", "/accrued", "/dv01", "/ask")
BYTES_422, BYTES_404, BYTES_500, BYTES_REFUSED = 190, 70, 40, 160


def _rows(rng: np.random.Generator) -> list[tuple]:
    """Every request as (time, path, status, latency_ms, bytes_out, refused), unsorted."""
    names = list(PATHS)
    shares = np.array([PATHS[p][0] for p in names])
    hours = HOUR_WEIGHTS / HOUR_WEIGHTS.sum()
    rows = []
    for offset in range(DAYS):
        day = FIRST_DAY + timedelta(days=offset)
        start = datetime(day.year, day.month, day.day)
        count = int(rng.poisson(DAILY_MEAN))
        hour = rng.choice(24, size=count, p=hours)
        millis = rng.integers(0, 3_600_000, size=count)
        path = rng.choice(len(names), size=count, p=shares)
        noise = rng.normal(0.0, LATENCY_SIGMA, size=count)
        size_noise = rng.integers(-20, 21, size=count)
        draw = rng.random(size=count)
        server = rng.random(size=count)
        for i in range(count):
            name = names[path[i]]
            _, median_ms, size = PATHS[name]
            when = start + timedelta(hours=int(hour[i]), milliseconds=int(millis[i]))
            latency = median_ms * float(np.exp(noise[i]))
            if name == "/dv01" and day == SLOW_DAY:
                latency *= SLOW_FACTOR
            status, refused, out = 200, False, size + int(size_noise[i])
            if name == "/ask" and draw[i] < REFUSED_SHARE:
                refused, out = True, BYTES_REFUSED
            elif name == "/ask" and draw[i] < REFUSED_SHARE + NOT_FOUND_SHARE:
                status, out = 404, BYTES_404
            elif name in POST_PATHS and draw[i] > 1.0 - BAD_BODY_SHARE:
                status, out = 422, BYTES_422
            if name != "/health" and server[i] < SERVER_ERROR_SHARE:
                status, refused, out = 500, False, BYTES_500
            rows.append((when, name, status, latency, out, refused))
    burst_start = datetime(BURST_DAY.year, BURST_DAY.month, BURST_DAY.day, BURST_HOUR)
    millis = np.sort(rng.integers(0, 3_600_000, size=BURST_ROWS))
    noise = rng.normal(0.0, LATENCY_SIGMA, size=BURST_ROWS)
    for i in range(BURST_ROWS):
        # FastAPI refuses the body before the endpoint runs, so a 422 returns faster than a priced request
        latency = 0.5 * PATHS["/price"][1] * float(np.exp(noise[i]))
        rows.append((burst_start + timedelta(milliseconds=int(millis[i])), "/price", 422, latency, BYTES_422, False))
    return rows


def log_text() -> str:
    """The whole file as text: the header, then one line per request sorted by time (ties by path)."""
    rng = np.random.default_rng(SEED)
    rows = sorted(_rows(rng), key=lambda row: (row[0], row[1]))
    lines = [",".join(COLUMNS)]
    seen = set()
    for index, (when, path, status, latency, out, refused) in enumerate(rows):
        request_id = hashlib.sha256(f"{SEED}:{index}:{when.isoformat()}:{path}".encode("ascii")).hexdigest()[:16]
        if request_id in seen:
            raise RuntimeError(f"request_id {request_id} repeats; change the id rule")
        seen.add(request_id)
        stamp = when.strftime("%Y-%m-%dT%H:%M:%S.") + f"{when.microsecond // 1000:03d}Z"
        lines.append(f"{stamp},{request_id},{path},{status},{max(latency, 0.1):.1f},{out},{str(refused).lower()}")
    return "\n".join(lines) + "\n"


def main() -> None:
    text = log_text()
    if not text.isascii():
        raise SystemExit("the log must be ASCII")
    OUT.write_bytes(text.encode("ascii"))
    print(f"wrote {OUT.relative_to(REPO).as_posix()}: {len(text.splitlines()) - 1:,} rows, {len(text):,} bytes")


if __name__ == "__main__":
    main()
