"""Put a built notebook into the workbook design system, from the notebook itself and a small plan.

notebook_header.apply_header calls apply() for any notebook that has a plan, so the design is put back on every
rebuild and no builder has to know about it. What the notebook already says is read from it: its title, its week
and day, its sections, its exercises, its pictures and their alt text, and the notebook that comes next. The plan
holds only what a person has to write: one goal for each section, and the optional pieces that take judgment.

A plan is a JSON file named after the notebook. RUNBOOK.md beside this file explains every key:

    {"goals": ["Run your first line of Python.", "Know what Python is."]}

Anything the plan gets wrong stops the build with a sentence that says what to fix.
"""
import base64
import io
import os
import re
import tempfile
from pathlib import Path

import nbformat
from PIL import Image, ImageDraw

from . import components as c
from .cells import ENDINGS, MINUTES_AN_EXERCISE, quick_check, section_minutes

REPO = Path(__file__).resolve().parents[2]
SERIES_LINE = "\n".join(c.TAGLINE)
COLAB = "https://colab.research.google.com/github/lenamonj/python-fixed-income/blob/main/"
COUNT_WORDS = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
PICTURE = re.compile(r"!\[((?:[^\[\]]|\[[^\]]*\])*)\]\(data:image/(\w+);base64,([^)]+)\)")
IVORY, RULE, INK = "#F7F3EA", "#D8D0BE", "#1B2430"
KEYS = {"goals", "sections", "exercises", "route_line", "route_flags", "captions", "next_line", "note", "mistakes", "quick_checks"}


class PlanError(ValueError):
    """The plan and the notebook disagree. The message says what to change."""


def check_goal(goal: str) -> None:
    """A goal is read at a glance on its tracker: one sentence, eight words or fewer, ending in a full stop."""
    if len(goal.split()) > 8 or not goal.endswith(".") or ". " in goal:
        raise PlanError(f'the goal "{goal}" has {len(goal.split())} words: a goal is one sentence of eight words or fewer, '
                        f"ending in a full stop")


# ---------------------------------------------------------------- reading the notebook
def teaching_notebooks(course: Path) -> list:
    """A course's teaching notebooks in the order they are taken."""
    return sorted(path.resolve() for path in course.glob("week*/day*/*.ipynb") if not path.stem.endswith("_solutions"))


def title_cell(cells: list):
    for cell in cells:
        if cell.cell_type == "markdown" and cell.source.startswith("# "):
            return cell
    raise PlanError("the notebook has no title cell starting '# '")


def where(cells: list) -> tuple:
    """The plate ("WEEK 1 · DAY 1, PART 2") and the spoken label ("Day 1, Part 2"), from the purpose line."""
    found = re.search(r"^Week (\d+), Day (\d+)(?:, Part (\d+))?\.", title_cell(cells).source, re.M)
    if not found:
        raise PlanError("the title cell has no purpose line starting 'Week W, Day D.'")
    week, day, part = found.groups()
    return (f"WEEK {week} · DAY {day}" + (f", PART {part}" if part else ""),
            f"Day {day}" + (f", Part {part}" if part else ""))


def heading_of(cell) -> str:
    """A heading cell's words, without its # marks."""
    return cell.source.split("\n")[0].lstrip("#").strip()


def find(cells: list, pattern: str, what: str) -> int:
    """The index of the one cell whose source matches the pattern."""
    hits = [i for i, cell in enumerate(cells) if re.search(pattern, cell.source, re.M)]
    if len(hits) != 1:
        raise PlanError(f"{what}: the pattern {pattern!r} matches {len(hits)} cells, and it must match exactly one")
    return hits[0]


CAPTION_LIMIT = 120  # characters in a figure's caption: one sentence that says what the figure shows
NUMBERED = r"## \d+(?:\.\d+)? "  # a numbered section's heading: "## 3.1 Slicing", or "## 3 Data Quality" in a project


def headings_start_cells(cells: list) -> None:
    """A numbered heading must start its cell, so that its tracker can sit above it: a cell that reaches such a
    heading after other words is cut in two there. No word of the notebook changes."""
    i = 0
    while i < len(cells):
        cell = cells[i]
        found = re.search(rf"\n+(?={NUMBERED})", cell.source) if cell.cell_type == "markdown" else None
        if found:
            cells.insert(i + 1, markdown_cell(cell.source[found.end():]))
            cell.source = cell.source[:found.start()]
        i += 1


def section_starts(cells: list, kind: str) -> list:
    """The index of each section's heading cell. kind is "numbered" (## 3.1 ..., with any unnumbered ## section
    that follows the first of them and comes before the notebook's ending) or "h1" (# A Topic)."""
    if kind == "numbered":
        numbered = [i for i, cell in enumerate(cells) if cell.cell_type == "markdown" and re.match(NUMBERED, cell.source)]
        if not numbered:
            raise PlanError('the notebook has no numbered section ("## 3.1 ..."): give the plan "sections": "h1"')
        ending = next((i for i, cell in enumerate(cells) if i > numbered[0] and cell.source.startswith(ENDINGS)), len(cells))
        return [i for i, cell in enumerate(cells) if numbered[0] <= i < ending and cell.cell_type == "markdown" and cell.source.startswith("## ")]
    if kind != "h1":
        raise PlanError(f'"sections" must be "numbered" or "h1", not {kind!r}')
    title = cells.index(title_cell(cells))
    skip = ("# Problem Statement", "# Wrapping Up")
    return [i for i, cell in enumerate(cells) if i > title and cell.cell_type == "markdown"
            and cell.source.startswith("# ") and not cell.source.startswith(skip)]


def count_exercises(cells: list) -> int:
    return sum(1 for cell in cells if cell.cell_type == "markdown" and re.match(r"### Exercise \d+", cell.source))


def course_line_of(course: Path) -> str:
    """The course line on the cover, from the table the banner tool keeps."""
    from notebook_header import COURSES
    for key, (line, _, _) in COURSES.items():
        number = "_bonus" if key == "bonus" else f"{int(key):02d}_" if isinstance(key, int) else f"{int(key[:-1]):02d}{key[-1]}_"
        if course.name.startswith("course" + number):
            return line
    raise PlanError(f"notebook_header.COURSES has no course for the folder {course.name}")


def next_notebook(order: list, place: int, course: Path):
    """The notebook taken after this one: the next in the course, or the first of the next course, or None."""
    if place + 1 < len(order):
        return order[place + 1]
    courses = sorted(path for path in REPO.glob("course*") if path.is_dir())
    for later in courses[courses.index(course) + 1:]:
        if teaching_notebooks(later):
            return teaching_notebooks(later)[0]
    return None


# ---------------------------------------------------------------- drawing
def as_markdown(png: bytes, alt: str) -> str:
    return f"![{alt}](data:image/png;base64,{base64.b64encode(png).decode('ascii')})"


class Drawer:
    """Draws components to PNG bytes, with one browser for the whole notebook."""

    def __enter__(self):
        self.studio = c.Studio().__enter__()
        self.folder = tempfile.TemporaryDirectory()
        self.count = 0
        return self

    def __exit__(self, *error):
        self.studio.__exit__(*error)
        self.folder.cleanup()

    def png(self, html: str, name: str) -> bytes:
        self.count += 1
        return self.studio.png(html, Path(self.folder.name) / f"{self.count:03d}_{name}.png").read_bytes()

    def figure(self, raw: bytes, kind: str, number: int, caption: str) -> bytes:
        """A picture the notebook already had, on the ivory plate with its numbered caption under it."""
        picture = Image.open(io.BytesIO(raw)).convert("RGB")
        full = c.WIDTH * c.SCALE
        if picture.width >= 2000:
            # drawn for the system at full width: it is the plate
            body = picture if picture.width == full else picture.resize((full, round(picture.height * full / picture.width)), Image.LANCZOS)
        else:
            # an older or smaller picture: up to twice its size, set on ivory; a screenshot gets a hairline
            factor = min(2.0, (full - 160) / picture.width)
            shown = picture.resize((round(picture.width * factor), round(picture.height * factor)), Image.LANCZOS)
            body = Image.new("RGB", (full, shown.height + 136), IVORY)
            left = (full - shown.width) // 2
            body.paste(shown, (left, 68))
            if kind != "png":
                ImageDraw.Draw(body).rectangle((left - 2, 66, left + shown.width + 1, 69 + shown.height), outline=INK, width=2)
        strip = Image.open(io.BytesIO(self.png(c.caption_strip(number, caption), "caption"))).convert("RGB")
        whole = Image.new("RGB", (full, body.height + strip.height), IVORY)
        whole.paste(body, (0, 0))
        whole.paste(strip, (0, body.height))
        ImageDraw.Draw(whole).rectangle((0, 0, full - 1, whole.height - 1), outline=RULE, width=2)
        out = io.BytesIO()
        whole.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(out, format="PNG", optimize=True)
        return out.getvalue()


# ---------------------------------------------------------------- cells
def split_hand_off(cell) -> str:
    """Take a cell's closing bold line off it and return the line, or "" when the cell does not end on one."""
    lines = cell.source.rstrip().split("\n")
    if len(lines) > 1 and re.fullmatch(r"\*\*.+\*\*.*", lines[-1]):
        cell.source = "\n".join(lines[:-1]).rstrip()
        return lines[-1]
    return ""


def put_before_hand_off(cell, text: str) -> None:
    """Add a block at the end of a cell, above its closing bold line when it has one."""
    hand_off = split_hand_off(cell)
    cell.source = cell.source + "\n\n" + text + (f"\n\n{hand_off}" if hand_off else "")


def markdown_cell(text: str):
    return nbformat.v4.new_markdown_cell(text)


# ---------------------------------------------------------------- the applier
def apply(nb, notebook: Path, plan: dict) -> Image.Image:
    """Put the notebook's cells into the design system, in place, and return its cover."""
    from plain_prose import plain_prose  # the notebook's own prose rule, for the words this tool adds
    unknown = set(plan) - KEYS
    if unknown:
        raise PlanError(f"the plan has keys this tool does not know: {sorted(unknown)}. It knows {sorted(KEYS)}")
    cells = nb.cells
    if any(cell.source.startswith("![Section ") for cell in cells):
        raise PlanError("this notebook is already in the design system: rebuild it from its builder")
    notebook = notebook.resolve()
    solutions = notebook.stem.endswith("_solutions")
    lesson = notebook.with_name(notebook.stem.removesuffix("_solutions") + ".ipynb")
    course = REPO / notebook.relative_to(REPO).parts[0]
    order = teaching_notebooks(course)
    if lesson not in order:
        raise PlanError(f"{lesson.name} is not one of {course.name}'s week and day notebooks")
    place = order.index(lesson)
    plate, label = where(cells)
    title, _, subtitle = heading_of(title_cell(cells)).partition(": ")
    course_line = course_line_of(course)
    weeks = len({path.parts[-3] for path in order})
    progress = place / (len(order) - 1) if len(order) > 1 else 0.0
    after = next_notebook(order, place, course)

    with Drawer() as draw:
        way_on = next_card(draw, cells, after, plan, notebook) if after else ""
        if solutions:
            if way_on:
                cells.append(markdown_cell(way_on))
            facts = (f"{count_exercises(cells)} WORKED ANSWERS",)
            return Image.open(io.BytesIO(draw.png(c.cover(course_line, plate, title, subtitle, "", facts, progress, weeks, True), "cover")))

        kind = plan.get("sections", "numbered")
        goals = plan.get("goals", [])
        headings_start_cells(cells)
        starts = section_starts(cells, kind)
        if len(goals) != len(starts):
            raise PlanError(f"the plan gives {len(goals)} goals and the notebook has {len(starts)} sections: "
                            f"{[heading_of(cells[i]) for i in starts]}")
        for goal in goals:
            check_goal(goal)
        exercises = count_exercises(cells)

        # 1. every picture the notebook already had becomes a numbered figure, in the order a reader meets them.
        # The route goes in above the first section, so it takes the number after any picture that opens the notebook.
        number = 0
        route_number = None
        captions = plan.get("captions", {})

        too_long = {}

        def framed(found) -> str:
            nonlocal number
            number += 1
            caption = captions.get(str(number), re.sub(r"^Figure \d+: ", "", found.group(1))).rstrip(".") + "."
            if len(caption) > CAPTION_LIMIT:
                too_long[number] = len(caption)
                return found.group(0)
            return as_markdown(draw.figure(base64.b64decode(found.group(3)), found.group(2), number, caption), f"Figure {number}: {caption}")

        for i, cell in enumerate(cells):
            if i == starts[0]:
                number += 1
                route_number = number
            if cell.cell_type == "markdown":
                cell.source = PICTURE.sub(framed, cell.source)
        own = [str(n) for n in range(1, number + 1) if n != route_number]
        stray = set(captions) - set(own)
        if stray:
            raise PlanError(f"the plan captions figures {sorted(stray)}, and the notebook's own pictures are figures "
                            f"{', '.join(own) or 'none'} (the route is Figure {route_number})")
        if too_long:
            sizes = ", ".join(f"figure {n} ({size} characters)" for n, size in too_long.items())
            raise PlanError(f"a caption is one sentence of {CAPTION_LIMIT} characters or fewer, and these run over: {sizes}. "
                            f'Give each one under "captions" in the plan')

        # 2. the pieces that take judgment, each found by a pattern that must match one cell
        done_note = scenario(draw, cells, plan["note"]) if plan.get("note") else ""
        for item in plan.get("mistakes", []):
            alt = (f"Common mistake: {item['name'][:1].lower() + item['name'][1:]}. You typed {item['typed']} and got {item['got']}. "
                   f"Type {item['instead']} instead, which gives {item['gives']}.")
            plate_png = draw.png(c.mistake(item["name"].upper(), item["typed"], item["got"], item["why"],
                                           item["instead"], item["gives"], item["how"]), "mistake")
            put_before_hand_off(cells[find(cells, item["in"], "a mistake plate")], as_markdown(plate_png, alt))
        for item in plan.get("quick_checks", []):
            i = find(cells, item["after"], "a quick check")
            hand_off = split_hand_off(cells[i])
            check = markdown_cell(plain_prose(quick_check(item["question"], item["answer"])))
            cells[i + 1:i + 1] = [check] + ([markdown_cell(hand_off)] if hand_off else [])

        # 3. the trackers, the route, the exercises strip, and the way on. Minutes are not known yet: 0 for now.
        for k, i in reversed(list(enumerate(section_starts(cells, kind), start=1))):
            cells.insert(i, markdown_cell(f"![Section {k} of {len(goals)}. {goals[k - 1]} About 0 minutes.]()"))
        cells.insert(next(i for i, cell in enumerate(cells) if cell.source.startswith("![Section 1 ")), markdown_cell("ROUTE"))
        practice = next((i for i, cell in enumerate(cells) if cell.source.startswith("## Exercises")), None)
        if practice is not None:
            cells.insert(practice, markdown_cell(f"![Exercises. {plan.get('exercises', 'Practice, with a worked answer for each.')}]()"))
        if way_on:
            closing = next((cell for cell in reversed(cells) if cell.source.startswith("## Congratulations!")), None)
            if closing is None:
                raise PlanError("the notebook has no '## Congratulations!' cell for the card to the next notebook")
            closing.source = closing.source.rstrip() + (f"\n\n{done_note}" if done_note else "") + "\n\n" + way_on

        # 4. the time rule on the finished cells, then the pictures that state it
        minutes = list(section_minutes(cells).values())
        lesson_minutes, practice_minutes = sum(minutes), MINUTES_AN_EXERCISE * exercises
        heads = [heading_of(cells[i]) for i in section_starts(cells, kind)]
        # a section's number is its heading's when it has one, and its place when it has not
        stops = [tuple(head.split(" ", 1)) if re.match(NUMBERED[3:], head) else (str(k), head) for k, head in enumerate(heads, start=1)]
        k = 0
        for cell in cells:
            if cell.source.startswith("![Section "):
                unit = "minute" if minutes[k] == 1 else "minutes"
                alt = f"Section {k + 1} of {len(goals)}. {goals[k]} About {minutes[k]} {unit}."
                cell.source = as_markdown(draw.png(c.tracker(f"SECTION {k + 1} OF {len(goals)}", goals[k], minutes[k], k + 1, len(goals)), "tracker"), alt)
                k += 1
            elif cell.source.startswith("![Exercises. "):
                goal = cell.source[len("![Exercises. "):-len("]()")]
                alt = f"Exercises. {goal} About {practice_minutes} minutes."
                cell.source = as_markdown(draw.png(c.tracker("EXERCISES", goal, practice_minutes), "exercises"), alt)
            elif cell.source == "ROUTE":
                cell.source = route_cell(draw, plan, stops, minutes, label, practice_minutes, exercises, route_number)

        total = 5 * round((lesson_minutes + practice_minutes) / 5)
        facts = (f"ABOUT {total} MIN" + (" WITH EXERCISES" if exercises else ""), f"{len(goals)} SECTIONS")
        facts += (f"{exercises} EXERCISES",) if exercises else ()
        first = place == 0  # a course's first notebook takes the tall cover with the series line
        cover = c.cover(course_line, plate, title, subtitle, SERIES_LINE if first else "", facts, progress, weeks, not first)
        return Image.open(io.BytesIO(draw.png(cover, "cover")))


def next_card(draw: Drawer, cells: list, after: Path, plan: dict, notebook: Path) -> str:
    """The card to the next notebook, as a link, with a line that opens it in Colab."""
    theirs = nbformat.read(after, as_version=4).cells
    plate, label = where(theirs)
    heading = heading_of(title_cell(theirs))
    line = plan.get("next_line", "")
    if not line:
        # what this notebook's closing says comes next, or failing that the next notebook's own purpose line
        closing = next((cell.source for cell in reversed(cells) if cell.source.startswith("## Congratulations!")), "")
        said = re.search(r"^Next, (?:on|in) [^,]+, (.+)$", closing, re.M)
        purpose = re.search(r"^Week \d+, Day \d+(?:, Part \d+)?\. (.+)$", title_cell(theirs).source, re.M)
        line = said.group(1) if said else purpose.group(1) if purpose else ""
        line = re.sub(r"[`*]", "", line[:1].upper() + line[1:])
    spoken = plate.title().replace(" · ", ", ")
    card = as_markdown(draw.png(c.next_step("NEXT", plate, heading, line), "next"), f"Next: {spoken}. {heading}.")
    link = Path(os.path.relpath(after, notebook.parent)).as_posix()
    return f"[{card}]({link})\n\n[Open {label} in Colab]({COLAB}{after.relative_to(REPO).as_posix()})"


def scenario(draw: Drawer, cells: list, note: dict) -> str:
    """Put the scenario's note in place of its quoted line and a progress strip where each ask is answered.
    Returns the note with every box ticked, for the closing cell."""
    asks = note["asks"]
    i = find(cells, note["in"], "the scenario's note")
    quoted = [line for line in cells[i].source.split("\n") if line.startswith("> ")]
    if not quoted:
        raise PlanError("the scenario cell has no quoted line (starting '> ') for the note to take the place of")
    text = " ".join(line[2:] for line in quoted)
    sender, name = note["sender"], note["title"]
    still_open = "; ".join(ask for ask, answer, _ in asks)
    card = draw.png(c.note(sender.upper(), f"0 OF {len(asks)} ANSWERED", [(ask, "") for ask, answer, _ in asks], text), "note")
    cells[i].source = cells[i].source.replace("\n".join(quoted), as_markdown(card, f"{sender}: {text} Still open: {still_open}."))
    for done, (ask, answer, pattern) in enumerate(asks, start=1):
        state = [(a, b if n < done else "") for n, (a, b, _) in enumerate(asks)]
        alt = f"{name}, {done} of {len(asks)} answered. " + " ".join(f"{a}: {b or 'still open'}." for a, b in state)
        strip = draw.png(c.note(name.upper(), f"{done} OF {len(asks)} ANSWERED", state), "strip")
        put_before_hand_off(cells[find(cells, pattern, f"where ask {done} of the note is answered")], as_markdown(strip, alt))
    full = [(a, b) for a, b, _ in asks]
    done_card = draw.png(c.note(sender.upper(), f"{len(asks)} OF {len(asks)} ANSWERED", full, text), "note_done")
    return as_markdown(done_card, f"{sender}, with every box ticked: {text} " + " ".join(f"{a}: {b}." for a, b in full))


def route_cell(draw: Drawer, plan: dict, stops: list, minutes: list, label: str, practice: int, exercises: int, figure: int) -> str:
    """The route cell: its heading, an optional line, the figure, the sections as a table when the figure has no
    room for their titles, and the time. figure is the route's number: 1, unless a picture opens the notebook."""
    from left_tables import left_tables
    flags = {int(place): words for place, words in plan.get("route_flags", {}).items()}
    titles = [re.sub(r"`", "", title) for number, title in stops]
    names = c.route_has_room(titles)
    count = COUNT_WORDS[len(stops)].capitalize() if len(stops) < len(COUNT_WORDS) else str(len(stops))
    caption = f"{count} sections, in order, with about how long each takes."
    lesson = sum(minutes)
    drawn = c.route([(number, title, spent) for (number, _), title, spent in zip(stops, titles, minutes)], flags,
                    f"{label.upper()} · THE ROUTE", f"LESSON · ABOUT {lesson} MIN", names)
    picture = as_markdown(draw.png(c.figure(drawn, figure, caption, flush=True), "route"), f"Figure {figure}: {caption}")
    table = ""
    if not names:
        rows = "\n".join(f"| {number} | {title} | {spent} min |" for (number, title), spent in zip(stops, minutes))
        table = "\n\n" + left_tables(f"| | Section | About |\n| --- | --- | --- |\n{rows}")
    many = COUNT_WORDS[exercises] if exercises < len(COUNT_WORDS) else str(exercises)
    time = f"**Time.** About {lesson} minutes for the lesson" + (f", then about {practice} for the {many} exercises." if exercises else ".")
    lead = f"{plan['route_line']}\n\n" if plan.get("route_line") else ""
    return f"## Your Route Through {label}\n\n{lead}{picture}{table}\n\n{time}"
