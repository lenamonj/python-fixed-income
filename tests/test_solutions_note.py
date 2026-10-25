"""Checks on the worked-answers note (tools/solutions_note.py): every teaching notebook with an Exercises section
opens it with the note, no solutions notebook carries it, and the builders' hook in install_cell adds it.

Run with: python -m pytest
"""
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
from install_cell import insert_cells  # noqa: E402
from solutions_note import HEADING, NOTE, add_note  # noqa: E402


def _exercise_cell(path: Path):
    nb = nbformat.read(path, as_version=4)
    return next((cell for cell in nb.cells if cell.cell_type == "markdown" and cell.source.startswith(HEADING)), None)


def test_every_teaching_notebook_opens_its_exercises_with_the_note():
    teaching = [p for p in REPO.glob("course*/week*/day*/*.ipynb") if not p.stem.endswith("_solutions")]
    with_exercises = [p for p in teaching if _exercise_cell(p) is not None]
    assert len(with_exercises) >= 155
    for path in with_exercises:
        assert _exercise_cell(path).source.startswith(f"{HEADING}\n\n{NOTE}"), path


def test_no_solutions_notebook_carries_the_note():
    for path in REPO.glob("course*/week*/day*/*_solutions.ipynb"):
        cell = _exercise_cell(path)
        assert cell is None or NOTE not in cell.source, path


def test_hook_adds_the_note_once_and_skips_solutions():
    cells = [new_markdown_cell("# Day 1"), new_markdown_cell(HEADING), new_markdown_cell("Replace each `...`.")]
    insert_cells(cells, "course01_python_foundations")
    assert cells[1].source == f"{HEADING}\n\n{NOTE}"
    assert add_note(cells) is False

    merged = [new_markdown_cell("# Day 1"), new_markdown_cell(f"{HEADING}\n\nReplace each `...`.")]
    add_note(merged)
    assert merged[1].source == f"{HEADING}\n\n{NOTE}\n\nReplace each `...`."

    solutions = [new_markdown_cell("# Day 1: Solutions"), new_markdown_cell(HEADING)]
    assert add_note(solutions) is False
    assert solutions[1].source == HEADING
