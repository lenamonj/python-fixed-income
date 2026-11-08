"""Start a Course 3 notebook: a fresh work folder holding everything the day begins with.

Python for Fixed Income, Course 3: Market Data and Time Series. Every notebook's first cell imports start_day
from this file. start_day(7) makes a new folder in your computer's temp folder, outside the course repo, moves
the notebook into it, and copies in the Excel reference file, the data files the notebook reads (DATA_FILES),
Course 2's finished bondmath.py, and marketdata.py, test_marketdata.py, and the other files earlier notebooks
committed (DAY_FILES: .gitignore, .env.example, slopes_2026.csv, queries.sql, snapshot.py) as notebook 06 left
them. It also makes the folder a Git repository with one commit for each notebook before (the subjects in
SUBJECTS), holding what that notebook committed, and the tags week1 and week2 on the last commit of each
finished week.
Notebook 01 starts with a repository and no commits: its first commit comes after its .gitignore.
On your machine the files come from the course repo; in Colab, from GitHub.

This course is educational content created in a personal capacity. Nothing here is investment advice or a
recommendation to buy or sell any security. All portfolio data is synthetic.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
GITHUB = "https://raw.githubusercontent.com/lenamonj/python-fixed-income/main/"
# beside the repo's copy of this file sit the module files; in Colab this file is alone
ON_GITHUB = not (HERE / "marketdata_after_01.py").exists()
FOLDER = "course03_market_data/start_of_day/"
# Course 2's finished module: every notebook has it, whether or not you took Course 2
BONDMATH = "course02_bond_math/start_of_day/bondmath_after_14.py"
REFERENCE_FILES = ["course3_excel_reference.csv"]
# the files of the repo's data folder each notebook reads, beside the reference file (15 is the capstone)
TREASURY, SPREADS = "treasury_par_yields.csv", "course3_synthetic_spreads.csv"
DGS10, DGS2 = "course3_fred_format_dgs10.json", "course3_fred_format_dgs2.json"
BOOK = ["holdings.csv", "ratings.csv", "trade_blotter.csv"]
DATA_FILES = {
    1: [TREASURY, DGS10],
    2: [TREASURY, DGS10, DGS2],
    3: [TREASURY, SPREADS, DGS10],
    4: [TREASURY, SPREADS, DGS10],
    5: [TREASURY, SPREADS, DGS10],
    6: [TREASURY, SPREADS, DGS10],
    7: [TREASURY, SPREADS, DGS10],
    8: [TREASURY, DGS10],
    9: [TREASURY, DGS10],
    10: [TREASURY, SPREADS, DGS10],
    11: [TREASURY, SPREADS, DGS10, DGS2, *BOOK, "issuers.csv", "benchmark.csv"],
    12: [TREASURY, SPREADS, DGS10, DGS2, *BOOK, "issuers.csv", "benchmark.csv"],
    13: [TREASURY, SPREADS, DGS10, *BOOK, "bondmath_excel_reference.csv"],
    14: [TREASURY, SPREADS, DGS10, DGS2, *BOOK],
    15: [TREASURY, SPREADS, DGS10, DGS2, *BOOK,
         "course3_capstone_extract.csv", "course3_capstone_cover_note.txt"],
}
WEEK_TAGS = {5: "week1", 10: "week2"}
# one fixed commit subject per notebook; notebook 12 added tests only
SUBJECTS = {
    1: "Notebook 01: get_secret, a .gitignore, and .env.example",
    2: "Notebook 02: fred_params, parse_fred_observations, and fred_series",
    3: "Notebook 03: missing_weekdays, align, and stale_runs",
    4: "Notebook 04: last_per_period and value_as_of",
    5: "Notebook 05: write_cache, read_cache, and cached_fred_series",
    6: "Notebook 06: change_bp, return_pct, and change_since_bp",
    7: "Notebook 07: rolling_vol_bp and assert_no_lookahead",
    8: "Notebook 08: rolling_zscore and rolling_percentile_rank",
    9: "Notebook 09: slope_bp, butterfly_bp, fly_weights, and slopes_2026.csv",
    10: "Notebook 10: summary_table",
    11: "Notebook 11: load_tables, run_query, assert_same_rows, and queries.sql",
    12: "Notebook 12: tests of joins and month ends, and the day's queries.sql",
    13: "Notebook 13: parse_json_reply",
    14: "Notebook 14: snapshot_tables, write_snapshot_html, write_snapshot_excel, and snapshot.py",
}
# the other files a notebook commits, as that notebook ends: the name in the work folder, then the file here
DAY_FILES = {
    1: {".gitignore": "day01_gitignore.txt", ".env.example": "day01_env_example.txt"},
    9: {"slopes_2026.csv": "day09_slopes_2026.csv"},
    11: {"queries.sql": "day11_queries.sql"},
    12: {"queries.sql": "day12_queries.sql"},
    14: {".gitignore": "day14_gitignore.txt", "snapshot.py": "day14_snapshot.py"},
}


def fetch(repo_path: str, target: Path) -> None:
    """Copy one file of the course repo to target: from the repo on your machine, from GitHub in Colab."""
    if ON_GITHUB:
        urllib.request.urlretrieve(GITHUB + repo_path, target)
    else:
        shutil.copy(HERE.parent.parent / repo_path, target)


def fetch_text(repo_path: str, target: Path) -> None:
    """Copy one text file of the course repo, written with this machine's line endings, as %%writefile
    writes them, so an edit in a notebook changes only the lines it changes."""
    if ON_GITHUB:
        with urllib.request.urlopen(GITHUB + repo_path) as response:
            text = response.read().decode("utf-8")
    else:
        text = (HERE.parent.parent / repo_path).read_text(encoding="utf-8")
    with open(target, "w", encoding="utf-8") as file:
        file.write(text)


def git(work: Path, *args: str) -> str:
    """Run one Git command in the work folder, and only there, and return what it printed."""
    return subprocess.run(["git", "-C", str(work), *args], check=True, capture_output=True, text=True).stdout


def copy_day(work: Path, notebook: int) -> list:
    """Put the files notebook `notebook` committed into work, as it left them; returns their names."""
    fetch_text(f"{FOLDER}marketdata_after_{notebook:02d}.py", work / "marketdata.py")
    fetch_text(f"{FOLDER}tests_after_{notebook:02d}.py", work / "test_marketdata.py")
    for name, stored in DAY_FILES.get(notebook, {}).items():
        fetch_text(FOLDER + stored, work / name)
    return ["marketdata.py", "test_marketdata.py", *DAY_FILES.get(notebook, {})]


def plural(count: int, word: str) -> str:
    return f"{count} {word}" + ("" if count == 1 else "s")


def build_history(work: Path, after: int, copies: list) -> list:
    """Make work a repository with one commit per notebook, 1 to after; returns the tags it made."""
    git(work, "init", "-q", "-b", "main")
    # Git's local ignore list, kept inside .git: the copied data files and bondmath.py are not your work, so
    # git status leaves them out (git status --ignored lists them as !!)
    (work / ".git" / "info" / "exclude").write_text("".join(name + "\n" for name in copies), encoding="utf-8")
    # settings for this repository only: a course name, a reserved example email, line endings kept, no signing
    for key, value in (("user.name", "Course Student"), ("user.email", "student@example.com"),
                       ("core.autocrlf", "false"), ("commit.gpgsign", "false")):
        git(work, "config", key, value)
    # Git must report the work folder as the top of this repository, or nothing more happens
    if not os.path.samefile(git(work, "rev-parse", "--show-toplevel").strip(), work):
        raise RuntimeError("Git is not working in the work folder. Run the setup cell again.")
    tags = []
    for notebook in range(1, after + 1):
        git(work, "add", *copy_day(work, notebook))
        git(work, "commit", "-q", "-m", SUBJECTS[notebook])
        if notebook in WEEK_TAGS:
            git(work, "tag", WEEK_TAGS[notebook])
            tags.append(WEEK_TAGS[notebook])
    return tags


def start_day(notebook: int, after: int | None = None) -> Path:
    """Make the work folder for a notebook, move into it, and return it.

    after is the notebook whose marketdata.py and test_marketdata.py the folder starts with: by default the one
    before (a solutions notebook passes its own number). After 0, notebook 01, there is no marketdata.py yet.
    """
    after = notebook - 1 if after is None else after
    if ON_GITHUB and importlib.util.find_spec("dotenv") is None:
        # Colab has requests and pytest, but may lack python-dotenv, which get_secret uses to read a .env file
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "python-dotenv==1.2.4"], check=True)
    work = Path(tempfile.mkdtemp(prefix=f"pfi_course3_{notebook:02d}_"))
    os.chdir(work)
    # Python looks for modules in the work folder first, so import marketdata finds this folder's file
    sys.path.insert(0, str(work))
    data_files = REFERENCE_FILES + DATA_FILES[notebook]
    for name in data_files:
        fetch(f"data/{name}", work / name)
    fetch_text(BONDMATH, work / "bondmath.py")
    # only the folder's name is printed: its full path would show your user name
    start = f"Work folder {work.name}: {plural(len(data_files), 'data file')}, Course 2's bondmath.py"
    module = "no marketdata.py yet" if after == 0 else f"marketdata.py as notebook {after:02d} left it"
    if shutil.which("git") is None:
        # without Git there is no history to replay: each earlier notebook's files, oldest first
        for notebook in range(1, after + 1):
            copy_day(work, notebook)
        print(f"{start}, {module}. Git is not installed, so the Git steps will stop: "
              "Course 2's notebook 01 shows how to install it")
    else:
        tags = build_history(work, after, data_files + ["bondmath.py"])
        tagged = f", tagged {' and '.join(tags)}" if tags else ""
        commits = "a Git repository with no commits" if after == 0 else plural(after, "commit")
        print(f"{start}, {module}, {commits}{tagged}")
    return work
