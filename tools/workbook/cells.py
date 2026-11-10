"""The typed side of a workbook: the few helpers a notebook builder needs beside its own markdown.

components.py draws; this file writes. Nothing here styles text: a notebook's words stay plain markdown, so they read
the same in VS Code, JupyterLab, Colab, and on GitHub.
"""
import re
from pathlib import Path

from .components import data_uri

READING_WORDS_A_MINUTE = 150  # a beginner reading technical text, with a glance at each picture
MINUTES_A_CODE_CELL = 0.5     # run it, read what it shows
MINUTES_A_FIGURE = 0.5        # a figure is studied, not read: its alt text starts "Figure"
MINUTES_AN_EXERCISE = 3

_NOT_WORDS = re.compile(r"\(data:image[^)]*\)|<[^>]+>|```.*?```", re.S)


def picture(path: Path, alt: str) -> str:
    """A drawn component as a markdown image. Markdown, not an <img> tag: it is the form every viewer accepts."""
    return f"![{alt}]({data_uri(path)})"


def linked_picture(path: Path, alt: str, link: str) -> str:
    """A drawn component that is also a link, such as the next-step card."""
    return f"[{picture(path, alt)}]({link})"


def quick_check(question: str, answer: str) -> str:
    """A question with its answer folded away: the reader commits to an answer, then opens it.
    Give the answer as one sentence to a line, the way notebook prose is written."""
    return f"**Quick check.** {question}\n\n<details>\n<summary>Show the answer</summary>\n\n{answer}\n\n</details>"


def minutes(cells: list) -> float:
    """About how long a run of cells takes: its words at reading pace, plus a moment for each code cell and figure."""
    text = [cell.source for cell in cells if cell.cell_type == "markdown"]
    words = sum(len(_NOT_WORDS.sub(" ", source).split()) for source in text)
    figures = sum(source.count("![Figure ") for source in text)
    code = sum(1 for cell in cells if cell.cell_type == "code")
    return words / READING_WORDS_A_MINUTE + code * MINUTES_A_CODE_CELL + figures * MINUTES_A_FIGURE


ENDINGS = ("![Exercises. ", "## You Can Now", "## Summary", "## Tidying Up", "# Wrapping Up", "## Exercises", "## Congratulations!")


def section_minutes(cells: list) -> dict:
    """Whole minutes for each section of a notebook in the design system, at least one each, keyed by the section's
    place from 1. A section runs from the cell after its tracker to the next tracker or to the notebook's ending."""
    found, current = {}, 0
    for cell in cells:
        if cell.cell_type == "markdown" and cell.source.startswith("![Section "):
            current = len(found) + 1
            found[current] = []
        elif cell.cell_type == "markdown" and cell.source.startswith(ENDINGS):
            current = 0
        elif current:
            found[current].append(cell)
    return {place: max(1, round(minutes(run))) for place, run in found.items()}
