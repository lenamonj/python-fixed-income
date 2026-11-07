"""Every section number a Course 1 notebook cites in its markdown names a heading that exists in Course 1.

A citation is "section 7.4", "7.4's", "in 7.4" before punctuation, or "(7.4)". Inline code and pictures are
skipped, and a number with a leading zero after the point (0.05, 7.05) is a decimal, not a section.
"""
import re
from pathlib import Path

import nbformat

REPO = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((REPO / "course01_python_foundations").glob("**/*.ipynb"))
NUMBER = r"(\d{1,2}\.[1-9]\d?(?:\.[1-9]\d?)?)"
CITATION = re.compile(rf"\b[Ss]ection {NUMBER}\b|\b{NUMBER}'s\b|\bin {NUMBER}(?=[.,;:)]|$)|\({NUMBER}\)", re.M)
HEADING = re.compile(r"^#{2,4} (\d+(?:\.\d+)+)\b", re.M)
# inline code, HTML code, and pictures hold numbers that are not citations
SKIP = re.compile(r"`[^`\n]*`|<code>.*?</code>|\(data:image[^)]*\)")


def markdown(path: Path) -> list[str]:
    return [SKIP.sub(" ", cell.source) for cell in nbformat.read(path, as_version=4).cells
            if cell.cell_type == "markdown"]


def test_every_section_citation_resolves():
    texts = {path: markdown(path) for path in NOTEBOOKS}
    headings = {number for cells in texts.values() for text in cells for number in HEADING.findall(text)}
    stale = []
    for path, cells in texts.items():
        for text in cells:
            for match in CITATION.finditer(text):
                number = next(group for group in match.groups() if group)
                if number not in headings:
                    stale.append(f"{path.stem}: {match.group(0)}")
    assert stale == []
