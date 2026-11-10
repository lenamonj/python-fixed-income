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
    html = escape(text, quote=False)
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
    html = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html)
    return re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", html)


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
        self.sections, self._heads = [], {}
        for i, cell in enumerate(self.cells):
            found = cell.cell_type == "markdown" and EMBEDDED.match(cell.source)
            tracker = found and TRACKER.match(found.group(1))
            if tracker:
                head = a.heading_of(self.cells[i + 1])
                number, title = head.split(" ", 1) if re.match(a.NUMBERED[3:], head) else (tracker.group(1), head)
                self.sections.append((number, title, tracker.group(3), int(tracker.group(4))))
                self._heads[number] = head
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
        shown = [out.get("text") or out.get("data", {}).get("text/plain", "") for out in self.code_cell(pattern).outputs]
        rows = "".join(shown).strip().split("\n")
        rows = [row for row in rows if not keep or re.search(keep, row)]
        return "\n".join(rows[:first] if first else rows)

    def error(self, pattern: str) -> str:
        """The last line of the error a code cell raised."""
        for out in self.code_cell(pattern).outputs:
            if out.output_type == "error":
                return f"{out.ename}: {out.evalue}"
        raise LookupError(f"the cell matching {pattern} raised no error")

    def frame(self, pattern: str, rows: int = 0, columns: int = 0) -> list:
        """The table a code cell showed (a DataFrame), as rows for slides.grid: the header first. `rows` and
        `columns` keep that many from the top and from the left."""
        for out in self.code_cell(pattern).outputs:
            table = re.search(r"<table.*?</table>", out.get("data", {}).get("text/html", ""), re.S)
            if table:
                found = [row for row in html_rows(table.group(0)) if row]
                found = [[re.sub(r"<[^>]+>", "", cell) for cell in row] for row in found]
                found = found[:rows + 1] if rows else found
                return [row[:columns] for row in found] if columns else found
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
        return " ".join(quoted)

    def table(self, pattern: str) -> list:
        """The table in the markdown cell matching the pattern, as rows for slides.grid: an HTML table or a pipe one."""
        text = self.markdown(pattern)
        block = re.search(r"<table.*?</table>", text, re.S)
        if block:
            return html_rows(block.group(0))
        piped = [row.strip().strip("|").split("|") for row in text.split("\n") if row.strip().startswith("|")]
        piped = [[inline(cell.strip()) for cell in row] for row in piped if not all(set(cell.strip()) <= set(":-") for cell in row)]
        if not piped:
            raise LookupError(f"the cell matching {pattern} holds no table")
        return piped

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

    def add(self, label: str, goal: str, title: str, *body: str) -> None:
        """A slide that is not a section's: the scenario, or anything before the route."""
        self.slides.append(s.slide(s.bar(label, goal, self.plate), title, "".join(body), self.foot, len(self.slides) + 1, "settled"))
        self.titles.append(re.sub(r"<[^>]+>", "", title))

    def route(self) -> None:
        """The route, as the notebook draws it, with the sections as a table when the route has no room for names."""
        cell = self.markdown(r"^## Your Route Through ")
        caption = next(alt for alt in (found.group(1) for c in self.cells for found in EMBEDDED.finditer(c.source))
                       if "sections, in order" in alt)
        number = int(re.match(r"Figure (\d+): ", caption).group(1))
        names = "| Section |" not in cell
        body = [self.figure(number, 1200 if names else 900)]
        if not names:
            rows = self.table(r"^## Your Route Through ")
            half = (len(rows) - 1 + 1) // 2 + 1
            body = [s.row(s.col(self.figure(number, 660), width=660),
                          s.col(s.grid(rows[:half], kind="tight")), s.col(s.grid([rows[0]] + rows[half:], kind="tight")))]
        self.add("THE ROUTE", re.sub(r"^Figure \d+: ", "", caption), line(r"^## .+$", cell)[3:], *body,
                 s.takeaway(inline(line(r"^\*\*Time\.\*\*.+$", cell))))

    def section(self, number: str, *body: str, title: str = "") -> None:
        """A section's slide: its tracker as the strip, its heading as the title unless another is given."""
        index = [section[0] for section in self.sections].index(number) + 1
        n, heading, goal, minutes = self.sections[index - 1]
        top = s.bar(f"SECTION {index} OF {len(self.sections)}", goal, f"ABOUT {minutes} MIN", index, len(self.sections))
        self.slides.append(s.slide(top, title or self.heading(number), "".join(body), self.foot, len(self.slides) + 1, "settled"))
        self.titles.append(re.sub(r"<[^>]+>", "", title or self.heading(number)))

    def closing(self, *body: str, card: bool = True) -> None:
        """The last slide: the You Can Now list, anything given, and the card to the next notebook."""
        can = self.markdown(r"^## You Can Now")
        items = [inline(text) for text in re.findall(r"^[*-] (.+)$", can, re.M)]
        lead = next((text for text in can.split("\n")[1:] if text.strip() and not text.startswith(("*", "-", "#"))), "You can now:")
        parts = [s.panel("", s.can_list(items)), *body]
        if card and any(re.search(r"\[!\[Next: ", cell.source) for cell in self.cells if cell.cell_type == "markdown"):
            parts.append(self.drawn(r"^Next: ", 1200))
        self.add("YOU CAN NOW", re.sub(r"[*`]", "", lead), "You Can Now", *parts)

    def press(self, argv: list | None = None, out: Path | None = None) -> int:
        """Print the PDF beside the notebook. With `--preview <folder>` on the command line, also save a PNG of each
        slide there and contact sheets of them, six slides to a sheet; with `--look` as well, stop there and print
        no PDF. Returns 1 when a slide does not fit."""
        argv = sys.argv if argv is None else argv
        out = out or self.notebook.with_name(self.notebook.stem + "_overview.pdf")
        title = f"{self.title}{': ' + self.subtitle if self.subtitle else ''}. Overview"
        with s.Press() as press:
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
