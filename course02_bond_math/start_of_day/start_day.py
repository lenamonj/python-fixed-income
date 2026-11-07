"""Start a Course 2 notebook: a fresh work folder holding everything the day begins with.

Python for Fixed Income, Course 2: Bond Math. Every notebook's first cell imports start_day from this file.
start_day(7) makes a new folder in your computer's temp folder, outside the course repo, moves the notebook
into it, and copies in the two Excel reference files, the data files the notebook reads (DATA_FILES), and
bondmath.py and test_bondmath.py as notebook 06 left them, with notebook 06's .gitignore from notebook 07 on.
It also makes the folder a Git repository with one commit for each notebook before (the subjects in SUBJECTS)
and the tags week1 and week2 on the last commit of each finished week, so the day's Git steps have a history.
On your machine the files come from this folder and the repo's data folder; in Colab, from GitHub.

This course is educational content created in a personal capacity. Nothing here is investment advice or a
recommendation to buy or sell any security. All portfolio data is synthetic.
"""
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
ON_GITHUB = not (HERE / "bondmath_after_01.py").exists()
REFERENCE_FILES = ["bondmath_excel_reference.csv", "bondmath_excel_reference_tvm.csv"]
# the files of the repo's data folder each notebook reads, beside the two reference files (15 is the capstone)
DATA_FILES = {
    6: ["holdings.csv", "benchmark.csv"],
    7: ["holdings.csv"],
    8: ["holdings.csv", "trade_blotter.csv"],
    9: ["holdings.csv"],
    10: ["holdings.csv", "benchmark.csv"],
    11: ["course2_treasury_curve.csv", "treasury_par_yields.csv"],
    12: ["holdings.csv", "benchmark.csv", "ratings.csv", "course2_treasury_curve.csv"],
    13: ["holdings.csv", "benchmark.csv", "ratings.csv"],
    14: ["holdings.csv", "benchmark.csv", "ratings.csv"],
    15: ["course2_capstone_holdings.csv", "course2_capstone_cover_note.txt", "holdings.csv", "benchmark.csv",
         "ratings.csv", "course2_treasury_curve.csv"],
}
WEEK_TAGS = {5: "week1", 10: "week2"}
# one fixed commit subject per notebook; notebook 05 added tests only
SUBJECTS = {
    1: "Notebook 01: future_value and present_value",
    2: "Notebook 02: cash_flows and price_from_yield",
    3: "Notebook 03: convert_yield",
    4: "Notebook 04: yield_from_price",
    5: "Notebook 05: tests of par pricing and of price against yield",
    6: "Notebook 06: add_months, coupon_dates, and a .gitignore",
    7: "Notebook 07: days_30_360, coupon_period_days, and accrued_interest",
    8: "Notebook 08: price, dirty_price, and yield_to_maturity",
    9: "Notebook 09: macaulay_duration, modified_duration, and dv01",
    10: "Notebook 10: convexity",
    11: "Notebook 11: interpolate_yield",
    12: "Notebook 12: years_to_maturity and spread_to_curve_bp",
    13: "Notebook 13: spread_duration and dts",
    14: "Notebook 14: weighted_average and price_change_estimate",
}
# notebook 06 writes this .gitignore; it is in every work folder from notebook 07 on
GITIGNORE_FROM = 6


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


def copy_module(work: Path, after: int) -> None:
    """Put bondmath.py, test_bondmath.py, and from notebook 06 the .gitignore, as notebook `after` left them."""
    fetch_text(f"course02_bond_math/start_of_day/bondmath_after_{after:02d}.py", work / "bondmath.py")
    fetch_text(f"course02_bond_math/start_of_day/tests_after_{after:02d}.py", work / "test_bondmath.py")
    if after >= GITIGNORE_FROM:
        fetch_text("course02_bond_math/start_of_day/gitignore_from_06.txt", work / ".gitignore")


def plural(count: int, word: str) -> str:
    return f"{count} {word}" + ("" if count == 1 else "s")


def build_history(work: Path, after: int, data_files: list) -> list:
    """Make work a repository with one commit per notebook, 1 to after; returns the tags it made."""
    git(work, "init", "-q", "-b", "main")
    # Git's local ignore list, kept inside .git: the copied data files never show in git status
    (work / ".git" / "info" / "exclude").write_text("".join(name + "\n" for name in data_files), encoding="utf-8")
    # settings for this repository only: a course name, a reserved example email, line endings kept, no signing
    for key, value in (("user.name", "Course Student"), ("user.email", "student@example.com"),
                       ("core.autocrlf", "false"), ("commit.gpgsign", "false")):
        git(work, "config", key, value)
    # Git must report the work folder as the top of this repository, or nothing more happens
    if not os.path.samefile(git(work, "rev-parse", "--show-toplevel").strip(), work):
        raise RuntimeError("Git is not working in the work folder. Run the setup cell again.")
    tags = []
    for notebook in range(1, after + 1):
        copy_module(work, notebook)
        names = ["bondmath.py", "test_bondmath.py"] + ([".gitignore"] if notebook >= GITIGNORE_FROM else [])
        git(work, "add", *names)
        git(work, "commit", "-q", "-m", SUBJECTS[notebook])
        if notebook in WEEK_TAGS:
            git(work, "tag", WEEK_TAGS[notebook])
            tags.append(WEEK_TAGS[notebook])
    return tags


def start_day(notebook: int, after: int | None = None) -> Path:
    """Make the work folder for a notebook, move into it, and return it.

    after is the notebook whose bondmath.py and test_bondmath.py the folder starts with: by default the one
    before (a solutions notebook passes its own number). After 0, notebook 01, there is no module yet.
    """
    after = notebook - 1 if after is None else after
    work = Path(tempfile.mkdtemp(prefix=f"pfi_course2_{notebook:02d}_"))
    os.chdir(work)
    # Python looks for modules in the work folder first, so import bondmath finds this folder's file
    sys.path.insert(0, str(work))
    data_files = REFERENCE_FILES + DATA_FILES.get(notebook, [])
    for name in data_files:
        fetch(f"data/{name}", work / name)
    # only the folder's name is printed: its full path would show your user name
    start = f"Work folder {work.name}: {plural(len(data_files), 'data file')}"
    if after == 0:
        print(f"{start}, no module yet")
    elif shutil.which("git") is None:
        copy_module(work, after)
        print(f"{start}, the module as notebook {after:02d} left it. Git is not installed, "
              "so the Git steps will stop: notebook 01 shows how to install it")
    else:
        tags = build_history(work, after, data_files)
        tagged = f", tagged {' and '.join(tags)}" if tags else ""
        print(f"{start}, the module as notebook {after:02d} left it, "
              f"{plural(after, 'commit')}{tagged}")
    return work
