"""A notebook's overview PDF, built from the notebook itself.

A day's overview script opens its built notebook as a Deck, adds a slide for each section, and prints the PDF
beside the notebook. Everything a slide shows is read from the notebook by a pattern: a code cell's lines, what it
printed, a table, a sentence, a figure. Nothing is typed again, so the PDF cannot say what the notebook does not, and
a pattern that no longer finds its cell stops the build. RUNBOOK_OVERVIEW.md is the job, step by step.

    deck = Deck(notebook)
    deck.front()
    deck.add("THE SCENARIO", "One line from the scenario.", "The Desk Lead's Note", s.statement(deck.quote(r"^## The Desk")))
    deck.route()
    deck.section("2.1", s.row(...), s.takeaway(...))
    deck.closing()
    deck.press()

Needs the author tools in requirements-dev.txt (playwright) and, once, `python -m playwright install chromium`.
"""
import base64
import io
import re
import sys
import tempfile
from html import escape
from pathlib import Path

import nbformat
from PIL import Image

from . import apply as a
from . import slides as s

REPO = Path(__file__).resolve().parents[2]
EMBEDDED = re.compile(r"!\[([^\]]*)\]\(data:image/png;base64,([^)]+)\)")
TRACKER = re.compile(r"Section (\d+) of (\d+)\. (.+) About (\d+) minutes?\.$")
SHEET_COLUMNS, SHEET_WIDTH = 2, 800  # a contact sheet shows the slides two across, each 800 px wide
FIGURE_MIN = 680  # px: a figure shown narrower than this cannot be read on a slide
FULL_ENOUGH = 0.6  # the share of a slide's height that its parts must take, or the slide reads as unfinished


def inline(text: str) -> str:
    """A line of the notebook's markdown as HTML: code spans, bold, italics, and links kept as their words."""
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    spans = []

    def keep(found) -> str:
        spans.append(f"<code>{escape(found.group(1), quote=False)}</code>")
        return f"\x00{len(spans) - 1}\x00"

    html = escape(re.sub(r"`([^`]+)`", keep, text), quote=False)
    html = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html)
    html = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", html)
    return re.sub(r"\x00(\d+)\x00", lambda found: spans[int(found.group(1))], html)


def line(pattern: str, text: str) -> str:
    """The whole line of a cell's text that the pattern matches some part of."""
    found = re.search(pattern, text, re.M)
    if not found:
        raise LookupError(f"no line matches {pattern}")
    return text[text.rfind("\n", 0, found.start()) + 1:].split("\n", 1)[0]


def last_bold(text: str) -> str:
    """A cell's closing bold line, as HTML: the hand-off that ends it."""
    found = re.findall(r"^\*\*(.+)\*\*(.*)$", text, re.M)
    if not found:
        raise LookupError("the cell has no bold line")
    return inline(f"**{found[-1][0]}**{found[-1][1]}")


def html_rows(table: str) -> list:
    """The rows of an HTML table, each cell kept as HTML."""
    return [[re.sub(r"\s+", " ", cell).strip() for cell in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", found, re.S)]
            for found in re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S)]


def tables(text: str) -> list:
    """Every table in a markdown cell's text, in the order they appear, each as rows: HTML tables and pipe tables."""
    found = [(block.start(), html_rows(block.group(0))) for block in re.finditer(r"<table.*?</table>", text, re.S)]
    for run in re.finditer(r"(?:^[ \t]*\|.*(?:\n|$))+", text, re.M):
        rows = [row.strip().strip("|").split("|") for row in run.group(0).strip().split("\n")]
        found.append((run.start(), [[inline(cell.strip()) for cell in row] for row in rows
                                    if not all(set(cell.strip()) <= set(":-") for cell in row)]))
    return [rows for _, rows in sorted(found, key=lambda pair: pair[0])]


class Deck:
    """One notebook's overview. The notebook must be in the design system: its trackers give each section's goal
    and minutes, and its cover's facts are worked out the same way."""

    def __init__(self, notebook: Path):
        self.notebook = Path(notebook).resolve()
        self.cells = nbformat.read(self.notebook, as_version=4).cells
        course = REPO / self.notebook.relative_to(REPO).parts[0]
        order = a.teaching_notebooks(course)
        place = order.index(self.notebook)
        self.plate, self.label = a.where(self.cells)
        self.title, _, self.subtitle = a.heading_of(a.title_cell(self.cells)).partition(": ")
        self.course_line = a.course_line_of(course)
        self.weeks = len({path.parts[-3] for path in order})
        self.progress = place / (len(order) - 1) if len(order) > 1 else 0.0
        self.statement = a.SERIES_LINE if place == 0 else ""
        self.foot = f"PYTHON FOR FIXED INCOME · {self.course_line.split(' · ')[0]} · {self.plate}"
        # the sections, from each tracker and the heading under it: number, title, goal, minutes
        self.sections, self._heads, self._at = [], {}, []
        for i, cell in enumerate(self.cells):
            found = cell.cell_type == "markdown" and EMBEDDED.match(cell.source)
            tracker = found and TRACKER.match(found.group(1))
            if tracker:
                head = a.heading_of(self.cells[i + 1])
                number, title = head.split(" ", 1) if re.match(a.NUMBERED[3:], head) else (tracker.group(1), head)
                self.sections.append((number, title, tracker.group(3), int(tracker.group(4))))
                self._heads[number] = head
                self._at.append(i)
        if not self.sections:
            raise LookupError(f"{self.notebook.name} is not in the design system: convert the notebook first")
        self.exercises = a.count_exercises(self.cells)
        self.lesson_minutes = sum(section[3] for section in self.sections)
        total = 5 * round((self.lesson_minutes + a.MINUTES_AN_EXERCISE * self.exercises) / 5)
        self.facts = (f"ABOUT {total} MIN" + (" WITH EXERCISES" if self.exercises else ""), f"{len(self.sections)} SECTIONS")
        self.facts += (f"{self.exercises} EXERCISES",) if self.exercises else ()
        self.slides, self.titles, self._light = [], [], set()
        self._files = Path(tempfile.mkdtemp(prefix="pfi_overview_"))

    # ------------------------------------------------------------ reading the notebook
    def code_cell(self, pattern: str):
        """The first code cell whose source matches the pattern."""
        for cell in self.cells:
            if cell.cell_type == "code" and re.search(pattern, cell.source, re.M):
                return cell
        raise LookupError(f"no code cell matches {pattern}")

    def lines(self, pattern: str, comments: bool = False, keep: str = "") -> list:
        """A code cell's lines, without its comments unless asked for. `keep` is a pattern: only matching lines stay."""
        return [text for text in self.code_cell(pattern).source.split("\n")
                if text.strip() and (comments or not text.strip().startswith("#")) and (not keep or re.search(keep, text))]

    def output(self, pattern: str, keep: str = "", first: int = 0) -> str:
        """What a code cell printed or showed, as text. `keep` is a pattern for the lines to keep; `first` keeps
        that many lines from the top."""
        # a chart's output also carries its name as text ("<Figure size ...>"), which the notebook does not show
        shown = [out.get("text") or out.get("data", {}).get("text/plain", "") for out in self.code_cell(pattern).outputs
                 if "image/png" not in out.get("data", {})]
        # pytest and git colour their words with escape codes, which the notebook draws as colour, not as text
        rows = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", "".join(shown)).strip().split("\n")
        rows = [row for row in rows if not keep or re.search(keep, row)]
        return "\n".join(rows[:first] if first else rows)

    def error(self, pattern: str) -> str:
        """The last line of the error a code cell raised."""
        for out in self.code_cell(pattern).outputs:
            if out.output_type == "error":
                # a SyntaxError's message ends with the cell's temporary file name, which says nothing
                return f"{out.ename}: " + re.sub(r"\s*\([\w<>.-]+, line \d+\)$", "", out.evalue)
        raise LookupError(f"the cell matching {pattern} raised no error")

    def frame(self, pattern: str, rows: int = 0, columns=0) -> list:
        """The table a code cell showed (a DataFrame), as rows for slides.grid: the header first. `rows` keeps that
        many from the top. `columns` keeps that many from the left, the row labels counted as the first, or, given
        a list of the header's names, the row labels and those columns in that order."""
        for out in self.code_cell(pattern).outputs:
            table = re.search(r"<table.*?</table>", out.get("data", {}).get("text/html", ""), re.S)
            if table:
                found = [row for row in html_rows(table.group(0)) if row]
                found = [[re.sub(r"<[^>]+>|&nbsp;", "", cell).strip() for cell in row] for row in found]
                # pandas gives a named index a header row of its own: the name belongs over the row labels
                if len(found) > 1 and found[1][0] and not any(found[1][1:]) and not found[0][0] and "<thead>" in table.group(0) \
                        and table.group(0).split("</thead>")[0].count("<tr") == 2:
                    found = [[found[1][0]] + found[0][1:]] + found[2:]
                found = found[:rows + 1] if rows else found
                if isinstance(columns, int):
                    return [row[:columns] for row in found] if columns else found
                missing = [name for name in columns if name not in found[0]]
                if missing:
                    raise LookupError(f"the table of the cell matching {pattern} has no column {missing}: it has {found[0][1:]}")
                keep = [0] + [found[0].index(name) for name in columns]
                return [[row[i] for i in keep] for row in found]
        raise LookupError(f"the cell matching {pattern} showed no table")

    def chart(self, pattern: str, width: int) -> str:
        """The picture a code cell drew, `width` px wide on the slide, exactly as the notebook shows it."""
        for out in self.code_cell(pattern).outputs:
            if "image/png" in out.get("data", {}):
                return self._shot(base64.b64decode(out["data"]["image/png"]), width)
        raise LookupError(f"the cell matching {pattern} drew no picture")

    def markdown(self, pattern: str) -> str:
        """The first markdown cell whose text matches the pattern, without its pictures."""
        for cell in self.cells:
            if cell.cell_type == "markdown":
                text = EMBEDDED.sub("", cell.source)
                if re.search(pattern, text, re.M):
                    return text
        raise LookupError(f"no markdown cell matches {pattern}")

    def quote(self, pattern: str) -> str:
        """The quoted lines ("> ...") of the markdown cell matching the pattern, as one sentence run."""
        quoted = [text[2:].strip() for text in self.markdown(pattern).split("\n") if text.startswith("> ") and text[2:].strip()]
        if not quoted:
            raise LookupError(f"the cell matching {pattern} has no quoted line")
        # the statement is set as plain words, so a code span or a bold run gives up its marks
        return re.sub(r"`([^`]+)`|\*\*(.+?)\*\*", lambda found: found.group(1) or found.group(2), " ".join(quoted))

    def excel(self, pattern: str) -> str:
        """The Excel side by side of the markdown cell matching the pattern, when it is a sentence: its words as
        HTML, without the bold lead-in. A comparison that is a table is read with excel_table."""
        found = line(r"^\*\*Excel side by side\.\*\*", self.markdown(pattern))
        words = re.sub(r"^\*\*Excel side by side\.\*\*\s*", "", found)
        if not words:
            raise LookupError(f"the Excel side by side of the cell matching {pattern} is a table, not a sentence: "
                              "read it with deck.excel_table")
        return inline(words)

    def excel_table(self, pattern: str) -> list:
        """The table of an Excel side by side, as rows for slides.grid: the first table under the bold lead-in, in
        the first markdown cell that has both and matches the pattern. A formula from the table is a good pattern."""
        for cell in self.cells:
            text = EMBEDDED.sub("", cell.source) if cell.cell_type == "markdown" else ""
            lead = re.search(r"^\*\*Excel side by side\.\*\*", text, re.M)
            found = lead and re.search(pattern, text, re.M) and tables(text[lead.start():])
            if found:
                return found[0]
        raise LookupError(f"no markdown cell matching {pattern} has a table under an Excel side by side")

    def table(self, pattern: str, which: int = 1) -> list:
        """A table in the markdown cell matching the pattern, as rows for slides.grid: an HTML table or a pipe one.
        `which=2` is the cell's second table."""
        found = tables(self.markdown(pattern))
        if len(found) < which:
            raise LookupError(f"the cell matching {pattern} holds {len(found) or 'no'} table{'' if len(found) == 1 else 's'}"
                              + (f", not {which}" if found else ""))
        return found[which - 1]

    def block(self, pattern: str, keep: str = "") -> list:
        """The fenced block of the markdown cell matching the pattern (commands, a note, a file's text), as lines
        for slides.codebox. `keep` is a pattern for the lines to keep."""
        found = re.search(r"^```[^\n]*\n(.*?)^```", self.markdown(pattern), re.S | re.M)
        if not found:
            raise LookupError(f"the cell matching {pattern} holds no fenced block")
        return [text for text in found.group(1).rstrip("\n").split("\n") if not keep or re.search(keep, text)]

    def items(self, pattern: str) -> list:
        """The bulleted or numbered list in the markdown cell matching the pattern, each item as HTML, for
        slides.can_list."""
        found = re.findall(r"^(?:[*-]|\d+\.) (.+)$", self.markdown(pattern), re.M)
        if not found:
            raise LookupError(f"the cell matching {pattern} holds no list")
        return [inline(text) for text in found]

    def questions(self, number: str, keep: str = "") -> list:
        """What a section of a project asks, as rows for slides.grid: each question's heading beside its `Q.` line.
        `keep` is a pattern for the headings to keep, when the section asks more than one slide holds."""
        index = [section[0] for section in self.sections].index(number)
        stop = self._at[index + 1] if index + 1 < len(self._at) else len(self.cells)
        rows = [["Question", "What it asks"]]
        for cell in self.cells[self._at[index] + 1:stop]:
            head = ""
            for text in cell.source.split("\n") if cell.cell_type == "markdown" else ():
                if text.startswith("### "):
                    head = text[4:]
                elif text.startswith("Q. ") and (not keep or re.search(keep, head)):
                    rows.append([inline(head), inline(text[3:])])
        if len(rows) == 1:
            raise LookupError(f"section {number} asks no question" + (f" under a heading that matches {keep}" if keep else ""))
        return rows

    def heading(self, number: str) -> str:
        """A section's heading as the notebook has it, with its number, as HTML."""
        return inline(self._heads[number])

    def drawn(self, alt: str, width: int) -> str:
        """A picture drawn into the notebook (a figure, the route, the next card), found by its alt text."""
        for cell in self.cells:
            if cell.cell_type == "markdown":
                for found in EMBEDDED.finditer(cell.source):
                    if re.search(alt, found.group(1)):
                        return self._shot(base64.b64decode(found.group(2)), width)
        raise LookupError(f"no picture in the notebook has alt text matching {alt}")

    def figure(self, number: int, width: int = 1200) -> str:
        """Figure `number` as the notebook shows it, on its plate with its caption."""
        if width < FIGURE_MIN:
            raise ValueError(f"figure {number} at {width} px is too small to read: show a figure {FIGURE_MIN} px wide or wider")
        return self.drawn(rf"^Figure {number}: ", width)

    def _shot(self, png: bytes, width: int) -> str:
        """A picture on a slide: a copy at two and a half times its shown width, never larger than it was made,
        so the PDF carries the detail a screen can show and no more."""
        image = Image.open(io.BytesIO(png))
        wide = min(image.width, round(width * 2.5))
        if wide < image.width:
            image = image.convert("RGB").resize((wide, round(image.height * wide / image.width)), Image.LANCZOS)
        path = self._files / f"picture_{len(list(self._files.iterdir())):03d}.png"
        image.save(path, optimize=True)
        return s.shot(path, width)

    # ------------------------------------------------------------ the slides
    def front(self) -> None:
        """The first slide: the notebook's cover."""
        self.slides.append(s.front(self.course_line, f"{self.plate} · OVERVIEW", self.title, self.subtitle, self.statement,
                                   self.facts, self.progress, self.weeks))
        self.titles.append("the front")

    def scenario(self, pattern: str, *body: str) -> None:
        """The scenario's slide: the heading of the cell that matches, the desk lead's note set large, anything
        given under it, and the day's facts at the foot."""
        text = self.markdown(pattern)
        title = re.sub(r"^#+ ", "", line(r"^#+ .+$", text))
        middle = f'<div class="middle">{s.statement(self.quote(pattern))}{"".join(body)}</div>'
        self.add("THE SCENARIO", f"{self.label}: what the desk asks for.", inline(title), middle, s.facts(*self.facts))
        self._light.add(len(self.slides))

    def problem(self, *body: str) -> None:
        """The slide of a notebook that opens with a Problem Statement where another has a desk lead's note: what
        its Business Context says beside its Objectives, anything given under them, and the day's facts at the foot."""
        def said(pattern: str) -> list:
            lines = [text for text in self.markdown(pattern).split("\n") if text.strip() and not text.startswith("#")]
            item = r"(?:[*-]|\d+\.) "
            listed = [inline(re.sub(item, "", text, count=1)) for text in lines if re.match(item, text)]
            return [inline(text) for text in lines if not re.match(item, text)] + ([s.can_list(listed)] if listed else [])
        both = s.row(s.col(s.panel("Business Context", *said(r"^## Business Context")), width=680),
                     s.col(s.panel("Objectives", *said(r"^## Objectives"))))
        middle = f'<div class="middle">{both}{"".join(body)}</div>'
        self.add("THE PROBLEM", f"{self.label}: the question the day answers.", "Problem Statement", middle,
                 s.facts(*self.facts))
        self._light.add(len(self.slides))

    def add(self, label: str, goal: str, title: str, *body: str) -> None:
        """A slide that is not a section's: the scenario, or anything before the route."""
        self.slides.append(s.slide(s.bar(label, goal, self.plate), title, "".join(body), self.foot, len(self.slides) + 1, "settled"))
        self.titles.append(re.sub(r"<[^>]+>", "", title))

    def whole(self, label: str, width: int = 1180) -> None:
        """A project's slide before the route: Figure 1, its picture of the whole assignment, under the heading
        that stands above it in the notebook, with the bold line under it as the goal."""
        at = next(i for i, cell in enumerate(self.cells) if cell.cell_type == "markdown" and "![Figure 1: " in cell.source)
        before, _, after = self.cells[at].source.partition("![Figure 1: ")
        heads = re.findall(r"^#+ (.+)$", before, re.M) or re.findall(r"^#+ (.+)$", self.cells[at - 1].source, re.M)
        goal = re.search(r"^\*\*(.+)\*\*", EMBEDDED.sub("", after), re.M)
        if not heads or not goal:
            raise LookupError("Figure 1 has no heading above it or no bold line under it: lay this slide out with deck.add")
        self.add(label, re.sub(r"[*`]", "", goal.group(1)), inline(heads[-1]), self.figure(1, width))

    def route(self) -> None:
        """The route, as the notebook draws it, with the sections as a table when the route has no room for names."""
        cell = self.markdown(r"^## Your Route Through ")
        caption = next(alt for alt in (found.group(1) for c in self.cells for found in EMBEDDED.finditer(c.source))
                       if "sections, in order" in alt)
        number = int(re.match(r"Figure (\d+): ", caption).group(1))
        names = not re.search(r"<table|^[|]", cell, re.M)  # the notebook lists the sections under a route with no room for them
        rows = [] if names else self.table(r"^## Your Route Through ")
        half = len(rows) // 2 + 1
        # the table grows a row for every two sections past ten, and the figure gives up that room
        width = 1200 if names else max(700, 820 - 120 * max(0, half - 6))
        at = len(self.slides)

        def drawn(width: int) -> None:
            body = [self.figure(number, width)]
            if not names:
                body.append(s.row(s.col(s.grid(rows[:half], kind="tight")), s.col(s.grid([rows[0]] + rows[half:], kind="tight"))))
            del self.slides[at:], self.titles[at:]
            self.add("THE ROUTE", re.sub(r"^Figure \d+: ", "", caption), line(r"^## .+$", cell)[3:], *body,
                     s.takeaway(inline(line(r"^\*\*Time\.\*\*.+$", cell))))

        drawn(width)
        # a section name that wraps makes the table taller than this allows for: press() then asks for less
        self._route = None if names else (at, width, drawn)

    def section(self, number: str, *body: str, title: str = "") -> None:
        """A section's slide: its tracker as the strip, its heading as the title unless another is given."""
        index = [section[0] for section in self.sections].index(number) + 1
        n, heading, goal, minutes = self.sections[index - 1]
        top = s.bar(f"SECTION {index} OF {len(self.sections)}", goal, f"ABOUT {minutes} MIN", index, len(self.sections))
        self.slides.append(s.slide(top, title or self.heading(number), "".join(body), self.foot, len(self.slides) + 1, "settled"))
        self.titles.append(re.sub(r"<[^>]+>", "", title or self.heading(number)))

    def closing(self, *body: str, card: bool = True) -> None:
        """The last slide: the You Can Now list, anything given, and the card to the next notebook. A project has
        no such cell: its slide shows the list that ends its Congratulations cell, under the sentences that lead to it."""
        project = not any(cell.cell_type == "markdown" and re.search(r"^## You Can Now", cell.source, re.M) for cell in self.cells)
        can = self.markdown(r"^## Congratulations!" if project else r"^## You Can Now")
        items = [inline(text) for text in re.findall(r"^[*-] (.+)$", can, re.M)]
        lead = next((text for text in can.split("\n")[1:] if text.strip() and not text.startswith(("*", "-", "#"))), "You can now:")
        parts = [s.panel("", s.can_list(items)), *body]
        if project:
            # the sentences after the cell's table say where the student started: they lead to its list, or,
            # in a cell with no list, they are what the slide says, up to the card
            listed, said = re.search(r"^[*-] ", can, re.M), []
            for text in can[:listed.start() if listed else len(can)].split("\n")[1:]:
                if text.lstrip().startswith("["):
                    break
                said = [] if text.lstrip().startswith(("<", "|")) else said + [text] if text.strip() else said
            lead = "What the course has taught you."
            parts = [s.panel("", *([inline(" ".join(said))] if said else []), s.can_list(items)), *body]
            if not listed:
                parts = [s.panel("", *[inline(text) for text in said]), *body]
        if card and any(re.search(r"\[!\[Next: ", cell.source) for cell in self.cells if cell.cell_type == "markdown"):
            parts.append(self.drawn(r"^Next: ", 1200))
        self.add("YOU CAN NOW", re.sub(r"[*`]", "", lead), "You Can Now", *parts)
        self._light.add(len(self.slides))

    def press(self, argv: list | None = None, out: Path | None = None) -> int:
        """Print the PDF beside the notebook. With `--preview <folder>` on the command line, also save a PNG of each
        slide there and contact sheets of them, six slides to a sheet; with `--look` as well, stop there and print
        no PDF. Returns 1 when a slide does not fit."""
        argv = sys.argv if argv is None else argv
        out = out or self.notebook.with_name(self.notebook.stem + "_overview.pdf")
        title = f"{self.title}{': ' + self.subtitle if self.subtitle else ''}. Overview"
        with s.Press() as press:
            if getattr(self, "_route", None):
                # the route's figure gives up 40 px at a time until its slide holds the table under it
                at, width, drawn = self._route
                after = self.slides[at + 1:], self.titles[at + 1:]
                while width > 700 and press._load([self.slides[at]], title):
                    width -= 40
                    drawn(width)
                self.slides[at + 1:], self.titles[at + 1:] = after
            if "--preview" in argv:
                folder = Path(argv[argv.index("--preview") + 1])
                for number, name in enumerate(self.titles, start=1):
                    print(f"  slide {number}: {name}")
                shots = press.previews(self.slides, folder, title)
                for path in contact_sheets(shots, folder):
                    print("sheet:", path)
                if "--look" in argv:
                    return 0
            faults = press._load(self.slides, title)
            thin = [f"slide {number} ({self.titles[number - 1]}) fills {share:.0%} of its height"
                    for number, share in enumerate(press.fill(), start=2) if share < FULL_ENOUGH and number not in self._light]
            if faults or thin:
                print("NOT PRINTED:", "; ".join(faults + [f"SPARSE: {text}" for text in thin]))
                return 1
            press.pdf(self.slides, out, title)
        print(f"wrote {out.name}: {len(self.slides)} slides, {out.stat().st_size / 1024:.0f} KB")
        return 0


def contact_sheets(shots: list, folder: Path, per_sheet: int = 6) -> list:
    """The slide previews six to a sheet, two across, so a whole deck can be looked at in a few pictures."""
    made = []
    for start in range(0, len(shots), per_sheet):
        group = [Image.open(path).convert("RGB") for path in shots[start:start + per_sheet]]
        height = round(group[0].height * SHEET_WIDTH / group[0].width)
        rows = -(-len(group) // SHEET_COLUMNS)
        sheet = Image.new("RGB", (SHEET_COLUMNS * SHEET_WIDTH + (SHEET_COLUMNS + 1) * 12, rows * (height + 12) + 12), "#888888")
        for k, image in enumerate(group):
            sheet.paste(image.resize((SHEET_WIDTH, height), Image.LANCZOS),
                        (12 + (k % SHEET_COLUMNS) * (SHEET_WIDTH + 12), 12 + (k // SHEET_COLUMNS) * (height + 12)))
        path = folder / f"sheet_{start // per_sheet + 1}.png"
        sheet.save(path)
        made.append(path)
    return made
