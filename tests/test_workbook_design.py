"""A notebook built in the workbook design system keeps to its rules. The system is in tools/workbook/README.md.

A notebook is in the system once it has section trackers, so every notebook is held to these rules from the build
that converts it, with no list to keep. Day 0 is the reference.
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

DESIGNED = sorted(path for path in REPO.glob("course*/week*/day*/*.ipynb")
                  if not path.stem.endswith("_solutions") and "![Section 1 of " in path.read_text(encoding="utf-8"))
WITH_SOLUTIONS = DESIGNED + [path.with_name(path.stem + "_solutions.ipynb") for path in DESIGNED]
STYLED = re.compile(r"<img|<[a-z][^>]*\sstyle=")  # an HTML picture, or a style attribute on any tag
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
        assert not STYLED.search(source), source[:120]


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
def test_every_section_opens_with_its_tracker(path):
    sources = markdown(path)
    trackers = [i for i, source in enumerate(sources) if source.startswith("![Section ")]
    for place, i in enumerate(trackers, start=1):
        # a tracker is a cell of its own, says its place, and sits on a heading
        assert ONLY_A_PICTURE.fullmatch(sources[i]) and sources[i].startswith(f"![Section {place} of {len(trackers)}. ")
        assert sources[i + 1].startswith("#"), sources[i + 1][:40]
    # and no numbered section is left without one
    for i, source in enumerate(sources):
        if re.match(r"## \d+\.\d+ ", source):
            assert i - 1 in trackers, source[:40]


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_tracker_minutes_follow_the_time_rule(path):
    nb = nbformat.read(path, as_version=4)
    stated = [int(n) for n in re.findall(r"!\[Section \d+ of \d+\. [^\]]*? About (\d+) minutes?\.\]", "\n".join(markdown(path)))]
    assert stated == list(cells.section_minutes(nb.cells).values())


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_figures_are_numbered_in_order_and_cited_ones_exist(path):
    text = "\n".join(markdown(path))
    numbers = [int(n) for n in re.findall(r"!\[Figure (\d+): ", text)]
    assert numbers and numbers == list(range(1, len(numbers) + 1))
    prose = PICTURE.sub(" ", text)
    assert {int(n) for n in re.findall(r"\bFigure (\d+)\b", prose)} <= set(numbers)


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_a_figure_caption_is_one_short_sentence(path):
    from workbook.apply import CAPTION_LIMIT
    for number, caption in re.findall(r"!\[Figure (\d+): ([^\]]*)\]\(", "\n".join(markdown(path))):
        assert len(caption) <= CAPTION_LIMIT, f"Figure {number}'s caption runs to {len(caption)} characters"
        assert caption.endswith("."), f"Figure {number}'s caption does not end in a full stop"


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_quick_checks_fold_their_answers(path):
    for source in (source for source in markdown(path) if "**Quick check.**" in source):
        assert source.startswith("**Quick check.** ") and "<details>\n<summary>Show the answer</summary>" in source
        assert source.rstrip().endswith("</details>")


@pytest.mark.parametrize("path", WITH_SOLUTIONS, ids=ids)
def test_notebook_ends_with_the_way_on(path):
    if path.parts[-4].startswith("course_bonus"):
        pytest.skip("the series ends here: there is no next notebook")
    last = markdown(path)[-1]
    link = re.search(r"\[!\[Next: [^\]]*\]\(data:image/png;base64,[^)]+\)\]\(([^)]+\.ipynb)\)", last)
    assert link, "the last cell has no card to the next notebook"
    assert (path.parent / link.group(1)).exists(), link.group(1)


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_overview_pdf_is_the_same_system_at_16_9(path):
    pypdf = pytest.importorskip("pypdf", reason="reading the overview PDF needs pypdf, in requirements.txt")
    reader = pypdf.PdfReader(path.with_name(path.stem + "_overview.pdf"))
    if "Skia" not in str((reader.metadata or {}).get("/Producer", "")):
        pytest.skip("this overview is still the PowerPoint export: it joins the system when it is redrawn with slides.py")
    pages = reader.pages
    text = [page.extract_text() for page in pages]
    # 1280 x 720 px slides are 960 x 540 points
    assert all((float(page.mediabox.width), float(page.mediabox.height)) == (960, 540) for page in pages)
    assert "educational content created in a personal capacity" in text[0]
    # spaced capitals are read back with their spaces, so compare with every space taken out
    squashed = re.sub(r"\s+", "", "\n".join(text))
    # a section is whatever the notebook gives a tracker to: its heading is the first line of the cell under the tracker
    cells = markdown(path)
    sections = [cells[i + 1].split("\n")[0].lstrip("# ") for i, source in enumerate(cells) if source.startswith("![Section ")]
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
    # a section runs from the cell after its tracker to the next tracker or the notebook's ending
    tracker = new_markdown_cell("![Section 1 of 1. A goal. About 2 minutes.](data:image/png;base64,AAAA)")
    assert cells.section_minutes([tracker] + run + [new_markdown_cell("## You Can Now"), new_markdown_cell("word " * 900)]) == {1: 2}


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


@pytest.mark.parametrize("path", DESIGNED, ids=ids)
def test_a_section_goal_is_one_short_sentence(path):
    from workbook.apply import check_goal
    goals = re.findall(r"!\[Section \d+ of \d+\. (.*?) About \d+ minutes?\.\]", "\n".join(markdown(path)))
    assert goals
    for goal in goals:
        check_goal(goal)


def test_apply_refuses_a_plan_it_cannot_follow():
    from workbook.apply import PlanError, apply, check_goal
    # nine words: one too many to read at a glance
    with pytest.raises(PlanError, match="9 words"):
        check_goal("Build a list in one line, then draw it.")
    with pytest.raises(PlanError, match="full stop"):
        check_goal("Understand .py files")
    nb = nbformat.read(DESIGNED[0], as_version=4)
    with pytest.raises(PlanError, match="does not know"):
        apply(nb, DESIGNED[0], {"gaols": []})
    # a built notebook is never converted twice: the builder starts from a fresh one
    with pytest.raises(PlanError, match="already in the design system"):
        apply(nb, DESIGNED[0], {"goals": []})


def test_a_route_sets_titles_under_its_points_only_when_they_fit():
    assert components.route_has_room(["Your First Cell", "What Python Is", "Python as a Calculator"])
    assert not components.route_has_room(["A Copy That Gives Back Every Digit: `write_cache` and `read_cache`", "Short"])
    # fifteen points leave 60 px each: room for a short word or two, not for a real title
    assert not components.route_has_room([f"Pandas Group Number {n}" for n in range(15)])
    assert "class=\"name\"" not in components.route([("1.1", "A Title", 3), ("1.2", "Another", 4)], names=False)


def test_a_route_of_any_length_stays_inside_the_picture(tmp_path):
    # the first and the last point sit 96 px from the picture's edges, so their words can never be wider than that allows
    assert all(components.route_stop_width(count) <= 2 * components.ROUTE_LEFT for count in range(1, 30))
    pytest.importorskip("playwright", reason="the studio needs the author tools in requirements-dev.txt")
    with components.Studio() as studio:
        for count in (1, 2, 4, 5, 6, 12):
            sections = [(f"1.{n}", "Conditional Statements", 9) for n in range(1, count + 1)]
            flags = {1: "ANSWER 1 · THE COUPON", count: "ANSWER 2 · THE CHART"}
            names = components.route_has_room([title for number, title, minutes in sections])
            drawn = components.route(sections, flags, "DAY 1, PART 2 · THE ROUTE", "LESSON · ABOUT 40 MIN", names)
            # the studio refuses a picture with a part outside it or words wider than their box
            studio.png(components.figure(drawn, 1, "The sections, in order.", flush=True), tmp_path / f"route{count}.png")


def test_landing_page_says_what_the_repo_holds():
    from workbook import landing
    facts = landing.counts()
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    # the pictures count the repo for themselves: the words typed beside them, and their alt text, must say the same
    for words in (f'{facts["notebooks"]} notebooks', f'{facts["excel"]} Excel comparisons', f'{facts["weeks"]} weeks',
                  f'All {facts["excel"]} comparisons', f'{facts["courses"]} courses and a bonus'):
        assert words in readme, words
    for name in ("hero", "numbers", "step1", "step2", "step3", "route", "inside", "next"):
        assert f'src="assets/readme/landing/{name}.png"' in readme and (landing.OUT / f"{name}.png").exists(), name
    assert "educational content created in a personal capacity" in readme
    # the series' two lines are kept in one place, and the page's alt text says them too
    assert all(line in readme for line in components.TAGLINE)
    # GitHub strips styles from a README, so none is written: the look is in the pictures
    assert " style=" not in readme


def test_every_course_page_opens_with_its_own_cover():
    from workbook import landing
    listed = landing.courses()
    assert len(listed) == 13
    for course in listed:
        readme = (REPO / course["folder"] / "README.md").read_text(encoding="utf-8")
        # the cover is a link back to the series, and its alt text says the course's own title and length
        assert f'<a href="../README.md"><img src="../assets/readme/landing/{course["folder"]}.png"' in readme, course["folder"]
        assert (landing.OUT / f'{course["folder"]}.png').exists(), course["folder"]
        assert f'{course["label"]}: {course["title"]}.' in readme and f'{course["notebooks"]} notebook' in readme, course["folder"]
        assert "wordmark" not in readme and " style=" not in readme, course["folder"]
        assert "educational content created in a personal capacity" in readme, course["folder"]


def test_a_slide_holds_its_strip_title_content_and_number():
    from workbook import slides
    made = slides.slide(slides.bar("SECTION 2 OF 8", "Know what Python is.", "ABOUT 2 MIN", index=2, count=8),
                        "0.2 What Python Is", slides.panel("Excel side by side", "Python is only the engine."), "FOOT", 5)
    assert made.count('class="done"') == 1 and made.count('class="now"') == 1
    assert "<h2>0.2 What Python Is</h2>" in made and '<div class="content">' in made and "<span>5</span>" in made
    # words become a paragraph; a block of HTML goes into a panel as it is
    assert "<p>Python is only the engine.</p>" in made
    assert "<p><div" not in slides.panel("", slides.codebox(["1 + 1"], "2"))


def test_the_front_never_ends_a_line_on_a_titles_hyphen():
    from workbook import slides
    made = slides.front("COURSE 4", "WEEK 3", "Scaling and K-Means", subtitle="Ridge & the Cross-Section")
    assert '<h1 class="s2">Scaling and <span class="nb">K-Means</span></h1>' in made
    assert 'Ridge &amp; the <span class="nb">Cross-Section</span>' in made
    # a title with no hyphen is set exactly as before
    assert "<h1 class=\"s1\">Bond Math</h1>" in slides.front("COURSE 2", "WEEK 1", "Bond Math")
    assert "white-space: nowrap" in (REPO / "tools" / "workbook" / "slides.css").read_text(encoding="utf-8")


def test_press_refuses_a_slide_that_does_not_fit(tmp_path):
    pytest.importorskip("playwright", reason="the press needs the author tools in requirements-dev.txt")
    from workbook import slides
    tall = slides.slide("", "Too Much", "".join(slides.panel("", "A line.") for _ in range(20)), "FOOT", 2)
    with slides.Press() as press:
        with pytest.raises(ValueError, match="does not fit"):
            press.pdf([tall], tmp_path / "deck.pdf", "test")
        # the message says how tall each part is; a code line that spills onto its neighbour is refused too,
        # though the slide is no wider for it, and so is a table wider than its column
        spilled = slides.slide("", "Spilled", slides.row(
            slides.col(slides.codebox(["x = 1" + " + 1" * 12]), width=300),
            slides.col(slides.grid([["Job", "Excel"], ["Total", "<code>=SUMIF(C2:C201,&quot;Energy&quot;,F2:F201)</code>"]]), width=200),
            slides.col(slides.panel("", "A line."))), "FOOT", 3)
        fits = slides.slide("", "Fits", slides.row(slides.col(slides.codebox(["x = 1"]), width=300), slides.col(slides.panel("", "A line."))), "FOOT", 4)
        said = press._load([tall, spilled, fits], "test")
    assert len(said) == 2
    assert re.match(r"slide 2: \d+ px too tall \(its parts, in px of height: panel \d+ \+ panel \d+", said[0])
    assert re.match(r"slide 3: a code line is \d+ px too long for its box, which holds 28 letters; a table is \d+ px wider than", said[1])


def test_a_capstone_whose_closing_has_no_list_closes_on_its_sentences():
    from workbook import overview
    deck = overview.Deck.__new__(overview.Deck)
    deck.cells = [new_markdown_cell(
        "## Congratulations!\n\nThe note is answered:\n\n<table><tr><th>The note asked</th><th>Answer</th></tr>"
        "<tr><td>One page</td><td>10.3</td></tr></table>\n<br clear=\"left\">\n\n"
        "Today your module is 29 functions and 55 tests.\n\nBe proud: you proved every row.\n\n"
        "[Open Day 1 in Colab](https://colab.research.google.com/)")]
    deck.slides, deck.titles, deck._light, deck.plate, deck.foot = [], [], set(), "WEEK 3 · DAY 5", "FOOT"
    deck.closing(card=False)
    made = deck.slides[0]
    assert "<p>Today your module is 29 functions and 55 tests.</p><p>Be proud: you proved every row.</p>" in made
    assert 'class="can"' not in made and "Open Day 1" not in made and "The note is answered" not in made


def test_a_deck_opens_a_problem_statement_notebook_on_its_problem():
    from workbook import overview
    deck = overview.Deck.__new__(overview.Deck)
    deck.cells = [new_markdown_cell("# Problem Statement\n\n## Business Context\n\nA credit team has 821 bonds.\n"
                                    "It asks what the rating says about spread."),
                  new_markdown_cell("## Objectives\n\n- Fit a line of `oas` on the rating.\n- Score it on unseen bonds.")]
    deck.slides, deck.titles, deck._light, deck.plate, deck.foot = [], [], set(), "WEEK 1 · DAY 1", "FOOT"
    deck.label, deck.facts = "Day 1", ("ABOUT 45 MIN", "11 SECTIONS")
    deck.problem()
    made = deck.slides[0]
    assert "<p>A credit team has 821 bonds.</p><p>It asks what the rating says about spread.</p>" in made
    assert "Problem Statement" in made and "# Problem" not in made and "## " not in made
    assert 'class="can"' in made and "<code>oas</code>" in made and "- Fit" not in made
    assert "11 SECTIONS" in made and deck._light == {1}


def test_a_deck_reads_a_projects_questions_under_either_ladder():
    from workbook import overview
    deck = overview.Deck.__new__(overview.Deck)
    # Courses 1 to 3: a numbered section, each question under its own ### heading
    deck.cells = [new_markdown_cell("tracker"), new_markdown_cell("## 2. Check the File"),
                  new_markdown_cell("### 2.1 Rows\n\nQ. How many rows? Store it in `rows`."),
                  new_markdown_cell("Q. A line with no heading above it in its cell.")]
    deck.sections, deck._at = [("2", "Check the File", "", 5)], [0]
    assert deck.questions("2") == [["Question", "What it asks"], ["2.1 Rows", "How many rows? Store it in <code>rows</code>."],
                                   ["", "A line with no heading above it in its cell."]]
    # Course 4 on: a # main topic, questions under ## headings and Predicts, ending where Wrapping Up begins
    deck.cells = [new_markdown_cell("tracker"),
                  new_markdown_cell("# Data Overview\n\n## Shape\n\nQ. How many rows? Store it in `rows`.\n\nQ. Draw them."),
                  new_markdown_cell("**Predict 1**\n\nQ. Write down a share."),
                  new_markdown_cell("## Gaps\n\nQ. How many cells are empty?"),
                  new_markdown_cell("# Wrapping Up"), new_markdown_cell("## Exercises\n\nQ. An exercise.")]
    assert deck.questions("2", sentences=1) == [["Question", "What it asks"], ["Shape", "How many rows?"], ["", "Draw them."],
                                                ["Predict 1", "Write down a share."], ["Gaps", "How many cells are empty?"]]
    assert deck.questions("2", keep=r"^Gaps") == [["Question", "What it asks"], ["Gaps", "How many cells are empty?"]]
    with pytest.raises(LookupError, match="asks no question"):
        deck.questions("2", keep=r"^Nothing")


def test_a_deck_reads_tables_by_what_they_are():
    from workbook import overview, slides
    cell = ("Value and income, by sector.\n\n| Sector | Value |\n| --- | --- |\n| Energy | 12 |\n\n"
            "**Excel side by side.**\n\n<table><tr><th>Job</th><th>Excel</th></tr>"
            "<tr><td>Total</td><td><code>=SUMIF(C:C,\"Energy\",F:F)</code></td></tr></table>\n")
    deck = overview.Deck.__new__(overview.Deck)
    deck.cells = [new_markdown_cell("**Excel side by side.** `=SUM(F:F)` adds the column."), new_markdown_cell(cell),
                  new_code_cell("book.plot()\nprint('drawn')", outputs=[
                      nbformat.v4.new_output("stream", name="stdout", text="\x1b[32mdrawn\x1b[0m\n"),
                      nbformat.v4.new_output("display_data", data={"image/png": "AAAA", "text/plain": "<Figure size 800x450 with 1 Axes>"})]),
                  new_code_cell("by_sector", outputs=[nbformat.v4.new_output("execute_result", data={"text/html": (
                      "<table><thead><tr><th></th><th>bonds</th><th>value</th></tr><tr><th>sector</th><th></th><th></th></tr></thead>"
                      "<tbody><tr><th>Energy</th><td>17</td><td>12.5</td></tr></tbody></table>")})])]
    # a cell's tables in order, and the one under the Excel lead-in found by a formula inside it
    assert deck.table(r"^Value and income")[1] == ["Energy", "12"]
    assert deck.table(r"^Value and income", which=2)[0] == ["Job", "Excel"]
    assert deck.excel_table(r"SUMIF")[1][0] == "Total"
    with pytest.raises(LookupError, match="holds 2 tables, not 3"):
        deck.table(r"^Value and income", which=3)
    # a comparison that is a sentence is read as words; one that is a table says which reader to use
    assert deck.excel(r"adds the column") == "<code>=SUM(F:F)</code> adds the column."
    with pytest.raises(LookupError, match="deck.excel_table"):
        deck.excel(r"^Value and income")
    # a named index goes over the row labels, columns are kept by name, and neither a chart's name nor a
    # colour code is part of what a cell printed
    assert deck.frame(r"^by_sector") == [["sector", "bonds", "value"], ["Energy", "17", "12.5"]]
    assert deck.frame(r"^by_sector", columns=["value"]) == [["sector", "value"], ["Energy", "12.5"]]
    with pytest.raises(LookupError, match="has no column"):
        deck.frame(r"^by_sector", columns=["price"])
    assert deck.output(r"^book\.plot") == "drawn"
    with pytest.raises(TypeError, match="list of lines"):
        slides.codebox(deck.output(r"^book\.plot"))


def test_studio_draws_a_component_at_twice_its_size(tmp_path):
    pytest.importorskip("playwright", reason="the studio needs the author tools in requirements-dev.txt")
    with components.Studio() as studio:
        out = studio.png(components.tracker("SECTION 1 OF 2", "Run one line.", 3, index=1, count=2), tmp_path / "tracker.png")
    assert Image.open(out).size == (2400, 124)
