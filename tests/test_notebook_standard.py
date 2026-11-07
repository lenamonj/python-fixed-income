"""Every notebook follows one standard, so the series reads as one piece of work. A course joins COURSES at its pass.

The standard itself is in COURSE1_SPEC.md under "The notebook standard". Jeff, 2026-11-02: "assure there is a
standardization we are following otherwise it shows we are not professional".
"""
import re
from pathlib import Path

import nbformat
import pytest

REPO = Path(__file__).resolve().parents[1]
COURSES = ["course01_python_foundations", "course02_bond_math", "course03_market_data", "course04_machine_learning", "course05_advanced_ml"]
TEACHING = sorted(
    path for course in COURSES for path in (REPO / course).glob("week*/day*/*.ipynb")
    if not path.stem.endswith("_solutions")
)
SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "nor", "of", "on", "or", "per", "the", "to", "vs"}
LIBRARY_NAMES = {"os", "csv", "pathlib", "merge", "concat", "apply", "pandas", "plotly", "pivot_table", "pytest", "bp", "sqlite3", "t-SNE"}
INSTALL_HEADINGS = {"Before You Start: Install the Libraries", "Before You Start: Nothing to Install"}
LEAD_IN = "By the end of this notebook, you can:"
WITHIN_TITLE = re.compile(r"\b(with|from|into|over)\b")
# Code spans may teach f-strings, so a format code is only a fault in prose. A dictionary lookup is a fault anywhere.
CODE_TEXT = re.compile(r"```.*?```|`[^`\n]*`|<code>.*?</code>|\$\$.*?\$\$", re.S)
UNFILLED = re.compile(r"\{[A-Za-z_]\w*(?:\[|\(|!r|:[,+.0-9]*[a-z%]\})")
UNFILLED_LOOKUP = re.compile(r"\{[A-Za-z_]\w*\[['\"]")
# Jeff 2026-11-07: from Course 4 on, notebooks follow his sample template; a day joins this set when rebuilt
NEW_STYLE = {"01_the_ml_workflow_and_simple_regression", "0_start_here", "01_python_for_fixed_income_intro"}


def ids(path: Path) -> str:
    return path.stem


def is_project(path: Path) -> bool:
    return path.stem == "course1_project" or path.stem.endswith("_capstone")


def in_course_1(path: Path) -> bool:
    return "course01" in str(path)


def course_number(path: Path) -> int:
    return int(re.match(r"course(\d+)", path.relative_to(REPO).parts[0]).group(1))


def is_case_study(path: Path) -> bool:
    return "case_study" in path.stem


def number(path: Path) -> int:
    return int(re.match(r"\d+", path.stem).group())


def markdown(path: Path) -> list[str]:
    return [cell.source for cell in nbformat.read(path, as_version=4).cells if cell.cell_type == "markdown"]


def headings(path: Path, level: int) -> list[str]:
    return re.findall(rf"^{'#' * level} (.+)$", "\n".join(markdown(path)), re.M)


def expected_label(path: Path) -> str:
    week = re.search(r"week(\d)", str(path)).group(1)
    day, part = re.search(r"day(\d)(_part2)?", str(path).replace("\\", "/").split("/week")[1]).groups()
    if "_part" in path.stem or "Part 1" in markdown(path)[1].split("\n")[0]:
        return f"Week {week}, Day {day}, Part {2 if part else 1}."
    return f"Week {week}, Day {day}."


def title_cased(heading: str) -> bool:
    words = re.sub(r"`[^`]*`", "", heading).replace(":", " ").split()
    for word in words:
        bare = word.strip("?.,()'")
        if bare.lower() in SMALL_WORDS or bare in LIBRARY_NAMES or not bare or not bare[0].isalpha():
            continue
        if bare[0].islower():
            return False
    return True


def test_the_four_splits_are_in_place():
    stems = {path.stem for path in TEACHING}
    assert {"06_part2_numpy", "07_part2_pandas_series_and_dataframes", "08_part2_pandas_combining_and_loading",
            "17_part2_analyzing_text"} <= stems


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_title_is_title_case(path):
    assert title_cased(headings(path, 1)[0]) and not WITHIN_TITLE.search(headings(path, 1)[0])


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_no_builder_placeholder_reaches_the_student(path):
    for cell in markdown(path):
        prose = CODE_TEXT.sub("", cell)
        assert not UNFILLED.search(prose) and not UNFILLED_LOOKUP.search(cell), cell[:200]


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_each_notebook_has_its_solutions_and_overview(path):
    assert path.with_name(path.stem + "_solutions.ipynb").exists()
    assert path.with_name(path.stem + "_overview.pdf").exists()


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_opening(path):
    cells = nbformat.read(path, as_version=4).cells
    title = cells[1].source
    assert title.startswith("# ")
    assert expected_label(path) in title
    assert "educational content created in a personal capacity" in title
    assert "colab.research.google.com" in title


# Jeff, 2026-11-07: the new style has no install cell; requirements.txt and Colab cover it
@pytest.mark.parametrize("path", [p for p in TEACHING if p.stem not in NEW_STYLE], ids=ids)
def test_first_section_is_the_install_section(path):
    assert headings(path, 2)[0] in INSTALL_HEADINGS


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p)], ids=ids)
def test_sections_carry_the_notebook_number(path):
    for heading in headings(path, 2) + headings(path, 3):
        found = re.match(r"(\d+)\.(\d+)", heading)
        if found:
            assert int(found.group(1)) == number(path), heading
            assert found.group(2) != "0", heading


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_headings_are_title_case(path):
    wrong = [heading for heading in headings(path, 2) + headings(path, 3) + headings(path, 4)
             if not heading.startswith("Exercise") and not title_cased(heading)]
    assert wrong == []


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p)], ids=ids)
def test_ending(path):
    level_two = [heading for heading in headings(path, 2) if heading != "Tidying Up"]
    assert level_two[-3:] == ["You Can Now", "Exercises", "Congratulations!"]
    if is_case_study(path) and in_course_1(path):
        assert level_two[-4] == "Summary"


@pytest.mark.parametrize("path", [p for p in TEACHING if is_project(p)], ids=ids)
def test_project_ends_on_the_closing(path):
    assert headings(path, 2)[-1] == "Congratulations!"


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_last_cell_is_the_closing(path):
    last = nbformat.read(path, as_version=4).cells[-1]
    assert last.cell_type == "markdown" and last.source.startswith("## Congratulations!")


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p)], ids=ids)
def test_you_can_now_is_a_list_under_its_lead_in(path):
    cell = next(source for source in markdown(path) if source.startswith("## You Can Now"))
    assert LEAD_IN in cell
    assert len(re.findall(r"^\* ", cell, re.M)) >= 3


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p)], ids=ids)
def test_last_exercise_is_an_ai_check(path):
    exercises = [heading for heading in headings(path, 3) if heading.startswith("Exercise")]
    assert exercises[-1].endswith(": AI check")
    assert all(re.fullmatch(r"Exercise \d+(: AI check)?", heading) for heading in exercises)


@pytest.mark.parametrize("path", [p for p in TEACHING if is_case_study(p)], ids=ids)
def test_case_study_opens_with_the_problem_definition(path):
    assert "Problem Definition" in headings(path, 2)
    level_three = headings(path, 3)
    start = level_three.index("Context")
    assert level_three[start:start + 4] == ["Context", "Objective", "The Data", "How We Will Work"]


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_case_study(p) and not is_project(p)], ids=ids)
def test_hands_on_notebook_has_a_scenario_before_its_first_section(path):
    sources = markdown(path)
    if path.stem in NEW_STYLE and in_course_1(path):
        # sources[0] is the banner, sources[1] the title; a scenario cell sits before the first numbered section
        first_section = next(i for i, source in enumerate(sources) if re.match(rf"## {number(path)}\.\d", source))
        assert sources[1].startswith("# ") and first_section >= 3, "no scenario between the title and section 1"
        return
    if path.stem in NEW_STYLE:
        # sources[0] is the banner, sources[1] the title; the new style has no install section
        start = next(i for i, source in enumerate(sources) if source.startswith("# Problem Statement"))
        assert start == 2
        after = re.findall(r"^## (.+)$", "\n".join(sources[start:]), re.M)
        assert after[:3] == ["Business Context", "Objectives", "Data Dictionary"]
        return
    first_section = next(i for i, source in enumerate(sources) if re.match(rf"## {number(path)}\.\d", source))
    install = next(i for i, source in enumerate(sources) if source.startswith("## Before You Start"))
    assert first_section - install >= 2, "no scenario between the install section and section 1"


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p)], ids=ids)
def test_questions_are_q_lines_never_bold(path):
    text = "\n".join(markdown(path))
    assert re.findall(r"^\*\*[^*\n]*\?\*\*$", text, re.M) == []
    assert len(re.findall(r"^Q\. ", text, re.M)) >= 8


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p) and (not in_course_1(p) or number(p) >= 5)], ids=ids)
def test_predict_cells_run_from_day_5(path):
    found = re.findall(r"^\*\*Predict (\d+)\*\*$", "\n".join(markdown(path)), re.M)
    assert len(found) >= 3
    assert [int(n) for n in found] == list(range(1, len(found) + 1))


# Jeff 2026-11-07: no Excel from Course 4 on
@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p) and course_number(p) < 4], ids=ids)
def test_excel_comparisons_use_one_label(path):
    text = "\n".join(markdown(path))
    assert "**Excel side by side.**" in text
    assert "**Compared with Excel" not in text


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_stories_sit_in_a_cell_of_their_own(path):
    for source in markdown(path):
        if re.search(r"^> \*{0,2}STORY", source, re.M):
            assert all(line.startswith(">") or not line.strip() for line in source.split("\n")), source[:80]
