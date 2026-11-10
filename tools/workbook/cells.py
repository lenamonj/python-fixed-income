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


def section_minutes(cells: list, notebook_number: int) -> dict:
    """Whole minutes for each numbered section, at least one each, keyed by the section's number ("0.3")."""
    found, current = {}, None
    for cell in cells:
        opening = re.match(rf"## ({notebook_number}\.\d+) ", cell.source) if cell.cell_type == "markdown" else None
        ending = cell.cell_type == "markdown" and re.match(r"## (?!\d)", cell.source)
        if opening:
            current = opening.group(1)
            found[current] = []
        elif ending:
            current = None
        if current:
            found[current].append(cell)
    return {number: max(1, round(minutes(run))) for number, run in found.items()}
