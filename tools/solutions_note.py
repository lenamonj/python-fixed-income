"""The line that opens every teaching notebook's Exercises section: the worked answers exist, and where they are.

Said first so a learner knows the answers are there before deciding whether to try. The note goes into the
markdown cell that starts with "## Exercises", right under the heading. Solutions notebooks (title ending in
"Solutions") get nothing.

Used two ways:
- install_cell.insert_cells calls add_note, so every course builder writes the note;
- python tools/solutions_note.py <notebook.ipynb> ...  adds it to saved notebooks (idempotent).
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat

HEADING = "## Exercises"

NOTE = ("**Every exercise has a worked answer** in the solutions notebook in this folder: the one with this "
        "notebook's name ending in `_solutions.ipynb`. Give each exercise a real try first, then check your work "
        "against it.")


def _is_solutions(cells: list) -> bool:
    title = next((cell.source.lstrip() for cell in cells
                  if cell.cell_type == "markdown" and cell.source.lstrip().startswith("# ")), "")
    return title.splitlines()[0].rstrip().endswith("Solutions") if title else False


def add_note(cells: list) -> bool:
    """Put the note under the Exercises heading, in place. Returns False when there is nothing to change: a
    solutions notebook, no Exercises section, or the note already there."""
    if _is_solutions(cells):
        return False
    for cell in cells:
        if cell.cell_type == "markdown" and cell.source.startswith(HEADING):
            if NOTE in cell.source:
                return False
            rest = cell.source[len(HEADING):].lstrip("\n")
            cell.source = f"{HEADING}\n\n{NOTE}" + (f"\n\n{rest}" if rest else "")
            return True
    return False


def add_to_notebook(path: Path) -> bool:
    nb = nbformat.read(path, as_version=4)
    if not add_note(nb.cells):
        return False
    path.write_text((nbformat.writes(nb) + "\n").replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return True


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    added = sum(add_to_notebook(Path(arg)) for arg in argv)
    print(f"{added} of {len(argv)} notebooks changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
