"""A notebook built in the workbook design system keeps to its rules. The system is in tools/workbook/README.md.

A notebook joins DESIGNED when it is rebuilt in the system. Day 0 is the reference.
"""
import base64
import io
import re
import sys
from pathlib import Path

import nbformat
import pytest
from nbformat.v4 import new_code_cell, new_markdown_cell
from PIL import Image

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
from plain_prose import plain_prose  # noqa: E402
from workbook import cells, components  # noqa: E402

DESIGNED = [REPO / "course01_python_foundations" / "week1" / "day0" / "0_start_here.ipynb"]
WITH_SOLUTIONS = DESIGNED + [path.with_name(path.stem + "_solutions.ipynb") for path in DESIGNED]
PICTURE = re.compile(r"!\[([^\]]*(?:\[[^\]]*\][^\]]*)*)\]\(data:image/(\w+);base64,([^)]+)\)")
ONLY_A_PICTURE = re.compile(r"!\[[^\n]*\]\(data:image/png;base64,[^)\s]+\)")


def ids(path: Path) -> str:
    return path.stem


def markdown(path: Path) -> list[str]:
    return [cell.source for cell in nbformat.read(path, as_version=4).cells if cell.cell_type == "markdown"]


def notebook_number(path: Path) -> int:
    return int(re.match(r"\d+", path.stem).group())


# ---------------------------------------------------------------- the rules a built notebook keeps
@pytest.mark.parametrize("path", WITH_SOLUTIONS, ids=ids)
def test_structure_is_drawn_and_never_styled_in_the_cell(path):
    for source in markdown(path):
        assert "<img" not in source and "style=" not in source, source[:120]


@pytest.mark.parametrize("path", WITH_SOLUTIONS, ids=ids)
def test_every_picture_is_a_full_width_png_with_alt_text(path):
    found = [match.groups() for source in markdown(path) for match in PICTURE.finditer(source)]
    assert found
    for alt, kind, encoded in found:
        assert kind == "png" and len(alt) > 20, alt
        assert Image.open(io.BytesIO(base64.b64decode(encoded))).width == components.WIDTH * components.SCALE, alt


@pytest.mark.parametrize("path", WITH_SOLUTIONS, ids=ids)
def test_first_cell_is_the_cover(path):
    first = nbformat.read(path, as_version=4).cells[0]
    assert "course-header" in first.metadata.get("tags", []) and ONLY_A_PICTURE.fullmatch(first.source)
    encoded = PICTURE.search(first.source).group(3)
    # the tall cover opens a course, the compact one is every other notebook's: both are far taller than the old banner
    assert Image.open(io.BytesIO(base64.b64decode(encoded))).height >= 800


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_every_numbered_section_opens_with_its_tracker(path):
    sources = markdown(path)
    openings = [i for i, source in enumerate(sources) if re.match(rf"## {notebook_number(path)}\.\d+ ", source)]
    assert openings
    for place, i in enumerate(openings, start=1):
        assert ONLY_A_PICTURE.fullmatch(sources[i - 1]), sources[i][:40]
        assert sources[i - 1].startswith(f"![Section {place} of {len(openings)}. "), sources[i][:40]


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_tracker_minutes_follow_the_time_rule(path):
    nb = nbformat.read(path, as_version=4)
    stated = [int(n) for n in re.findall(r"!\[Section \d+ of \d+\. [^\]]*? About (\d+) minutes?\.\]", "\n".join(markdown(path)))]
    assert stated == list(cells.section_minutes(nb.cells, notebook_number(path)).values())


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_figures_are_numbered_in_order_and_cited_ones_exist(path):
    text = "\n".join(markdown(path))
    numbers = [int(n) for n in re.findall(r"!\[Figure (\d+): ", text)]
    assert numbers and numbers == list(range(1, len(numbers) + 1))
    prose = PICTURE.sub(" ", text)
    assert {int(n) for n in re.findall(r"\bFigure (\d+)\b", prose)} <= set(numbers)


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_quick_checks_fold_their_answers(path):
    checks = [source for source in markdown(path) if "**Quick check.**" in source]
    assert checks
    for source in checks:
        assert source.startswith("**Quick check.** ") and "<details>\n<summary>Show the answer</summary>" in source
        assert source.rstrip().endswith("</details>")


@pytest.mark.parametrize("path", WITH_SOLUTIONS, ids=ids)
def test_notebook_ends_with_the_way_on(path):
    last = markdown(path)[-1]
    link = re.search(r"\[!\[Next: [^\]]*\]\(data:image/png;base64,[^)]+\)\]\(([^)]+\.ipynb)\)", last)
    assert link, "the last cell has no card to the next notebook"
    assert (path.parent / link.group(1)).exists(), link.group(1)


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_overview_pdf_is_the_same_system_at_16_9(path):
    pypdf = pytest.importorskip("pypdf", reason="reading the overview PDF needs pypdf, in requirements.txt")
    pages = pypdf.PdfReader(path.with_name(path.stem + "_overview.pdf")).pages
    text = [page.extract_text() for page in pages]
    # 1280 x 720 px slides are 960 x 540 points
    assert all((float(page.mediabox.width), float(page.mediabox.height)) == (960, 540) for page in pages)
    assert "educational content created in a personal capacity" in text[0]
    # spaced capitals are read back with their spaces, so compare with every space taken out
    squashed = re.sub(r"\s+", "", "\n".join(text))
    sections = re.findall(rf"^## ({notebook_number(path)}\.\d+ .+)$", "\n".join(markdown(path)), re.M)
    assert len(pages) >= len(sections) + 3
    for place, heading in enumerate(sections, start=1):
        assert f"SECTION{place}OF{len(sections)}" in squashed, heading
        assert re.sub(r"[`\s]", "", heading) in squashed, heading
    # a ligature would be saved as one odd character, which breaks search and copy
    assert "ﬁ" not in squashed and "ﬂ" not in squashed


# ---------------------------------------------------------------- the helpers
def test_time_rule_counts_words_code_cells_and_figures():
    run = [new_markdown_cell("## 9.1 A Section\n\n" + "word " * 148), new_code_cell("1 + 1"),
           new_markdown_cell("![Figure 1: a caption of six words](data:image/png;base64,AAAA)")]
    # 152 words in the first cell with its heading, 7 in the alt text, one code cell, one figure
    assert cells.minutes(run) == pytest.approx(159 / 150 + 0.5 + 0.5)
    assert cells.section_minutes(run + [new_markdown_cell("## You Can Now")], 9) == {"9.1": 2}


def test_quick_check_is_already_plain_prose():
    made = cells.quick_check("Which step is repeated?", "Import.\nInstall once.")
    assert plain_prose(made) == made


def test_house_curve_rises_from_zero_to_one_and_flattens():
    points = [components.curve(i / 10) for i in range(11)]
    assert points[0] == 0 and points[-1] == pytest.approx(1)
    steps = [b - a for a, b in zip(points, points[1:])]
    assert all(step > 0 for step in steps) and steps == sorted(steps, reverse=True)


def test_tracker_marks_the_sections_done_now_and_to_come():
    html = components.tracker("SECTION 3 OF 8", "Do the desk's first sum.", 11, index=3, count=8)
    assert html.count('class="done"') == 2 and html.count('class="now"') == 1 and html.count("<i ") == 8
    assert "Do the desk&#x27;s first sum." in html and "ABOUT 11 MIN" in html
    assert "<i " not in components.tracker("EXERCISES", "Six short jobs.", 18)


def test_a_slide_holds_its_strip_title_content_and_number():
    from workbook import slides
    made = slides.slide(slides.bar("SECTION 2 OF 8", "Know what Python is.", "ABOUT 2 MIN", index=2, count=8),
                        "0.2 What Python Is", slides.panel("Excel side by side", "Python is only the engine."), "FOOT", 5)
    assert made.count('class="done"') == 1 and made.count('class="now"') == 1
    assert "<h2>0.2 What Python Is</h2>" in made and '<div class="content">' in made and "<span>5</span>" in made
    # words become a paragraph; a block of HTML goes into a panel as it is
    assert "<p>Python is only the engine.</p>" in made
    assert "<p><div" not in slides.panel("", slides.codebox(["1 + 1"], "2"))


def test_press_refuses_a_slide_that_does_not_fit(tmp_path):
    pytest.importorskip("playwright", reason="the press needs the author tools in requirements-dev.txt")
    from workbook import slides
    tall = slides.slide("", "Too Much", "".join(slides.panel("", "A line.") for _ in range(20)), "FOOT", 2)
    with slides.Press() as press:
        with pytest.raises(ValueError, match="does not fit"):
            press.pdf([tall], tmp_path / "deck.pdf", "test")


def test_studio_draws_a_component_at_twice_its_size(tmp_path):
    pytest.importorskip("playwright", reason="the studio needs the author tools in requirements-dev.txt")
    with components.Studio() as studio:
        out = studio.png(components.tracker("SECTION 1 OF 2", "Run one line.", 3, index=1, count=2), tmp_path / "tracker.png")
    assert Image.open(out).size == (2400, 124)
