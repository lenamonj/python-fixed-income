"""The install section every notebook opens with, and the tool that adds it to a saved notebook.

The section is two cells placed right after the title cell: a heading that says what the cell does, and a code
cell that installs whatever the course's requirements.txt pins and the machine lacks (Colab lacks a few of them;
a .venv built from the repo's requirements.txt lacks none). The code cell checks presence, not version, so a
Colab runtime's own pandas or numpy is left alone and the saved output is the same on every machine that has
everything: "N packages checked, all present".

Used two ways:
- the course builders call install_section(course_folder) and put the two cells after the title cell;
- python tools/install_cell.py <notebook.ipynb> ...  adds the section to saved notebooks (idempotent).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell

from solutions_note import add_note

REPO = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

# pins whose import name differs from the package name
IMPORT_NAMES = {
    "beautifulsoup4": "bs4",
    "faiss-cpu": "faiss",
    "huggingface-hub": "huggingface_hub",
    "imbalanced-learn": "imblearn",
    "openai-agents": "agents",
    "pillow": "PIL",
    "python-dotenv": "dotenv",
    "pyyaml": "yaml",
    "rank-bm25": "rank_bm25",
    "scikit-learn": "sklearn",
    "sentence-transformers": "sentence_transformers",
}

HEADING = "## Before you start: install the libraries"

MARKDOWN = f"""{HEADING}

Run this cell first. It checks that every library this course pins in its `requirements.txt` is installed and installs only what is missing, so it finishes in a second on a machine set up from the repo's `requirements.txt` and does the installing for you in Google Colab. If it installs anything in Colab, restart the session (Runtime, Restart session) and run the notebook again from the top.
"""

CODE_TEMPLATE = '''# install what this notebook needs: the course's pinned libraries, only those not already present
import importlib.util
import subprocess
import sys

# import name: the pinned package, from {course}/requirements.txt
NEEDED = {{
{pins}
}}

# a package is present when Python can find its module; the version is left as the machine has it
missing = [pin for module, pin in NEEDED.items() if importlib.util.find_spec(module) is None]
if missing:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", *missing], check=True)
    print(f"{{len(NEEDED)}} packages checked, {{len(missing)}} installed: restart the session and run again from the top")
else:
    print(f"{{len(NEEDED)}} packages checked, all present")
'''


def pins(course_folder: str) -> dict[str, str]:
    """Import name to pin, from the course's requirements.txt, in the file's order."""
    path = REPO / course_folder / "requirements.txt"
    found = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        name = re.match(r"[A-Za-z0-9_.\-]+", line).group(0)
        module = IMPORT_NAMES.get(name.lower(), name.lower().replace("-", "_"))
        found[module] = line
    if not found:
        raise ValueError(f"{path} pins nothing")
    return found


def install_section(course_folder: str) -> tuple[str, str]:
    """The markdown source and the code source of the install section for one course."""
    body = "\n".join(f'    "{module}": "{pin}",' for module, pin in pins(course_folder).items())
    return MARKDOWN.rstrip("\n"), CODE_TEMPLATE.format(course=course_folder, pins=body).rstrip("\n")


def insert_cells(cells: list, course_folder: str) -> list:
    """The cells with the install section after the title cell (the first markdown cell that starts with '# ').
    Cells that already hold the section are returned unchanged. Every builder passes through here, so this is
    also where a teaching notebook's Exercises section gets its note on the worked answers (solutions_note.py)."""
    add_note(cells)
    if any(cell.cell_type == "markdown" and cell.source.startswith(HEADING) for cell in cells):
        return cells
    markdown, code = install_section(course_folder)
    for index, cell in enumerate(cells):
        if cell.cell_type == "markdown" and cell.source.lstrip().startswith("# "):
            return cells[:index + 1] + [new_markdown_cell(markdown), new_code_cell(code)] + cells[index + 1:]
    raise ValueError("no title cell (a markdown cell starting with '# ') to put the install section after")


def saved_output(code: str) -> str:
    """What the code cell prints on this machine, so a saved notebook carries a real output."""
    result = subprocess.run([PYTHON, "-c", code], capture_output=True, text=True, check=True, cwd=REPO)
    if result.stderr.strip():
        raise RuntimeError(f"the install cell wrote to stderr:\n{result.stderr}")
    return result.stdout


def add_to_notebook(path: Path) -> bool:
    """Add the section to one saved notebook, with its output. Returns False when it was already there."""
    course_folder = path.resolve().relative_to(REPO).parts[0]
    nb = nbformat.read(path, as_version=4)
    cells = insert_cells(list(nb.cells), course_folder)
    if cells is nb.cells:
        return False
    code_cell = next(cell for cell in cells if cell.cell_type == "code" and cell.source.startswith("# install what this notebook needs"))
    code_cell.outputs = [nbformat.v4.new_output("stream", name="stdout", text=saved_output(code_cell.source))]
    code_cell.execution_count = None
    nb.cells = cells
    text = nbformat.writes(nb) + "\n"
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return True


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    added = 0
    for arg in argv:
        path = Path(arg)
        if add_to_notebook(path):
            added += 1
            print(f"added: {path}")
        else:
            print(f"already there: {path}")
    print(f"{added} of {len(argv)} notebooks changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
