"""Day 1 is two notebooks. Each stands alone, ends on an AI check and a closing, and follows the prose rule."""
import sys
from pathlib import Path

import nbformat
import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
from plain_prose import plain_prose  # noqa: E402

WEEK1 = REPO / "course01_python_foundations" / "week1"
DAY0 = WEEK1 / "day0" / "0_start_here.ipynb"
PART1 = WEEK1 / "day1" / "01_python_for_fixed_income_intro.ipynb"
PART2 = WEEK1 / "day1_part2" / "01_part2_python_for_fixed_income_intro.ipynb"


def markdown(path: Path) -> list[str]:
    return [cell.source for cell in nbformat.read(path, as_version=4).cells if cell.cell_type == "markdown"]


@pytest.mark.parametrize("path", [PART1, PART2])
def test_each_part_has_its_solutions_and_overview(path):
    assert path.with_name(path.stem + "_solutions.ipynb").exists()
    assert path.with_name(path.stem + "_overview.pdf").exists()


@pytest.mark.parametrize("path", [DAY0, PART1, PART2])
def test_the_last_cell_is_the_closing(path):
    last = nbformat.read(path, as_version=4).cells[-1]
    assert last.cell_type == "markdown" and last.source.startswith("## Congratulations!")


@pytest.mark.parametrize("path", [PART1, PART2])
def test_the_last_exercise_is_an_ai_check(path):
    headings = [source.splitlines()[0] for source in markdown(path) if source.startswith("### Exercise")]
    assert headings[-1].endswith("AI check")


def test_the_split_falls_at_section_1_6():
    first = [source.splitlines()[0] for source in markdown(PART1) if source.startswith("## 1.")]
    second = [source.splitlines()[0] for source in markdown(PART2) if source.startswith("## 1.")]
    assert [line[3:6] for line in first] == ["1.1", "1.2", "1.3", "1.4", "1.5"]
    assert [line[3:6] for line in second] == ["1.6", "1.7", "1.8", "1.9"]


@pytest.mark.parametrize("path", [DAY0, PART1, PART2])
def test_prose_follows_the_rule(path):
    for source in markdown(path):
        assert plain_prose(source) == source
