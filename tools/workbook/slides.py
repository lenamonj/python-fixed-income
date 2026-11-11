"""The overview deck of a workbook: 16:9 pages in the same design system, drawn straight to a PDF.

Each function below returns the HTML of a slide or of a part of one, styled by slides.css on top of design.css.
A slide's body can hold any component from components.py as it stands, because a component is 1200 px wide and a
slide's body is too. Press.pdf() lays the slides out in a headless browser and prints them: the text stays text,
the diagrams stay sharp at any size, and the typefaces travel inside the file.

Needs the author tools in requirements-dev.txt (playwright) and, once, `python -m playwright install chromium`.
"""
import tempfile
from html import escape
from pathlib import Path

from .components import AUTHOR, SERIES, badge, course_curve

HERE = Path(__file__).resolve().parent
PAGE_WIDTH, PAGE_HEIGHT = 1280, 720
BLOCKS = ("<div", "<p", "<img", "<table", "<ul")  # how a part of a panel starts when it is not a line of words
DISCLAIMER = ("This course is educational content created in a personal capacity. Nothing here is investment advice or a "
              "recommendation to buy or sell any security. All portfolio data is synthetic.")


class Press:
    """A headless browser that prints slides. Use it as a context manager."""

    def __enter__(self):
        from playwright.sync_api import sync_playwright
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch()
        self._page = self._browser.new_page(viewport={"width": PAGE_WIDTH, "height": PAGE_HEIGHT}, device_scale_factor=1.25)
        self._folder = tempfile.TemporaryDirectory()
        return self

    def __exit__(self, *error):
        self._browser.close()
        self._playwright.stop()
        self._folder.cleanup()

    def _load(self, slides: list, title: str) -> list:
        """Lay the slides out, and return a line for each one whose body does not fit."""
        links = "".join(f'<link rel="stylesheet" href="{(HERE / name).as_uri()}">' for name in ("design.css", "slides.css"))
        page_file = Path(self._folder.name) / "deck.html"
        page_file.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title>'
                             f'{links}</head><body>{"".join(slides)}</body></html>', encoding="utf-8")
        self._page.goto(page_file.as_uri())
        self._page.evaluate("document.fonts.ready")
        # content that needs more room than its slide has would be cut off in print: measure it, slide by slide.
        # A code line longer than its box, or a table or picture wider than its panel, spills onto its neighbour
        # without widening the slide, so each is measured against its own box, and the message names it.
        over = self._page.evaluate(
            "[...document.querySelectorAll('.slide .content')].map(b => { const size = e => e.getBoundingClientRect();"
            " const spills = [];"
            " for (const e of b.querySelectorAll('.codebox')) { const long = e.scrollWidth - e.clientWidth;"
            "   const letters = Math.floor((e.clientWidth - 34) / (parseFloat(getComputedStyle(e).fontSize) * 0.6));"
            "   if (long > 1) spills.push(`a code line is ${long} px too long for its box, which holds ${letters} letters`); }"
            " for (const e of b.querySelectorAll('.grid, .shot')) { const holder = e.closest('.panel, .col') || b;"
            "   const past = Math.round(size(e).right - size(holder).right);"
            "   if (past > 1) spills.push(`a ${e.classList.contains('grid') ? 'table' : 'picture'} is ${past} px wider than the room it has`); }"
            " const parts = [...b.children].map(e => (e.classList[0] || e.tagName.toLowerCase()) + ' ' + Math.round(size(e).height));"
            " return [b.scrollHeight - b.clientHeight, b.scrollWidth - b.clientWidth, spills, parts.join(' + '), b.clientHeight] })")
        faults = []
        for number, (tall, wide, spills, parts, room) in enumerate(over, start=2):
            said = [f"{tall} px too tall (its parts, in px of height: {parts}, with 18 between them; the slide holds {room})"] if tall > 0 else []
            said += [f"{wide} px too wide"] if wide > 0 else []
            if said or spills:
                faults.append(f"slide {number}: " + "; ".join(said + spills))
        # the front has no content box: its title and subtitle must end above the line at its foot
        low = self._page.evaluate(
            "[...document.querySelectorAll('.slide.front')].map(f => f.querySelector('main').getBoundingClientRect().bottom"
            " - f.querySelector('footer').getBoundingClientRect().top)")
        return [f"slide 1: the title and subtitle reach the foot by {round(gap) + 12} px" for gap in low if gap > -12] + faults

    def fill(self) -> list:
        """For each content slide of the deck that was last laid out, the share of its height that its parts take."""
        return self._page.evaluate(
            "[...document.querySelectorAll('.slide .content')].map(b => { const kids = [...b.children];"
            " const used = kids.reduce((sum, k) => sum + k.getBoundingClientRect().height, 0) + 18 * Math.max(kids.length - 1, 0);"
            " return used / b.clientHeight })")

    def pdf(self, slides: list, out: Path, title: str) -> Path:
        """Print the slides to one PDF, a page each. A slide that does not fit stops the print."""
        faults = self._load(slides, title)
        if faults:
            raise ValueError("a slide's body does not fit: " + "; ".join(faults))
        self._page.pdf(path=str(out), width=f"{PAGE_WIDTH}px", height=f"{PAGE_HEIGHT}px", print_background=True)
        return out

    def previews(self, slides: list, folder: Path, title: str = "preview") -> list:
        """One PNG for each slide, for looking at before the PDF is printed. A slide that does not fit is still
        drawn, cut off as it would print, and named on the screen."""
        for fault in self._load(slides, title):
            print("does not fit:", fault)
        folder.mkdir(parents=True, exist_ok=True)
        made = []
        for i, block in enumerate(self._page.locator(".slide").all(), start=1):
            path = folder / f"slide_{i:02d}.png"
            block.screenshot(path=str(path))
            made.append(path)
        return made


# ---------------------------------------------------------------- slides
def front(course_line: str, plate: str, title: str, subtitle: str = "", statement: str = "", meta: tuple = (),
          progress: float = 0.0, weeks: int = 4) -> str:
    """The first slide: the notebook's cover at 16:9, with the disclaimer at its foot."""
    sub = f'<p class="sub">{escape(subtitle)}</p>' if subtitle else ""
    lines = f'<p class="lines">{"<br>".join(escape(line) for line in statement.splitlines())}</p>' if statement else ""
    facts = "".join(f"<span>{escape(fact)}</span>" for fact in meta)
    step = 1 if len(title) <= 14 else 2 if len(title) <= 22 else 3 if len(title) <= 36 else 4
    return (f'<section class="slide front">{course_curve(PAGE_WIDTH, PAGE_HEIGHT, 800, 1220, 532, 190, progress, weeks)}'
            f'<header><div class="brand">{badge()}<span class="series">{escape(SERIES.upper())}</span></div>'
            f'<div class="course">{escape(course_line)}</div></header>'
            f'<main><div class="plate">{escape(plate)}</div><h1 class="s{step}">{escape(title)}</h1>{sub}{lines}</main>'
            f'<footer><div>Created by <b>{escape(AUTHOR)}</b></div><div class="meta">{facts}</div></footer>'
            f'<p class="disclaimer">{escape(DISCLAIMER)}</p></section>')


def bar(label: str, goal: str, mark: str, index: int = 0, count: int = 0) -> str:
    """The strip at the top of a slide: the notebook's tracker for that section."""
    marks = "".join(f'<i class="{"done" if i < index else "now" if i == index else ""}"></i>' for i in range(1, count + 1))
    track = f'<span class="track">{marks}</span>' if count else ""
    return (f'<div class="bar"><span class="count">{escape(label)}</span>{track}'
            f'<span class="goal">{escape(goal)}</span><span class="mark">{escape(mark)}</span></div>')


def slide(top: str, title: str, body: str, foot: str, number: int, kind: str = "") -> str:
    """A content slide: the strip, the title, the body, and the foot with the slide's number."""
    return (f'<section class="slide {kind}">{top}<h2>{title}</h2><div class="content">{body}</div>'
            f'<div class="foot"><span>{escape(foot)}</span><span>{number}</span></div></section>')


# ---------------------------------------------------------------- what goes in a body
def row(*parts: str, kind: str = "") -> str:
    """Parts side by side."""
    return f'<div class="row {kind}">{"".join(parts)}</div>'


def col(*parts: str, width: int = 0) -> str:
    """Parts one under another, `width` px wide, or taking the room that is left."""
    size = f' style="width:{width}px;flex:none"' if width else ""
    return f'<div class="col{"" if width else " grow"}"{size}>{"".join(parts)}</div>'


def panel(label: str, *parts: str, kind: str = "") -> str:
    """A paper panel with a small label. A part that is words becomes a paragraph; a block of HTML goes in as it is."""
    inner = "".join(part if part.lstrip().startswith(BLOCKS) else f"<p>{part}</p>" for part in parts)
    head = f'<span class="label">{escape(label)}</span>' if label else ""
    return f'<div class="panel {kind}">{head}{inner}</div>'


def codebox(lines: list, output: str = "", bad: bool = False, small: bool = False) -> str:
    """Code as it is typed, with what it showed under a rule. A comment line is drawn dimmer. With no lines, the
    box holds the output alone."""
    if isinstance(lines, str):
        raise TypeError("codebox takes a list of lines: deck.lines(...) for the code, and output=deck.output(...) for what it showed")
    typed ="\n".join(f'<span class="cm">{escape(line)}</span>' if line.lstrip().startswith("#") else escape(line) for line in lines)
    shown = f'<span class="out{" bad" if bad else ""}">{escape(output)}</span>' if output else ""
    return f'<div class="codebox{" small" if small else ""}">{typed}{shown}</div>'


def grid(rows: list, kind: str = "") -> str:
    """A table. rows holds the header row first; each cell is HTML, so <code> and <b> are kept."""
    head = "".join(f"<th>{cell}</th>" for cell in rows[0])
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in line) + "</tr>" for line in rows[1:])
    return f'<table class="grid {kind}"><tr>{head}</tr>{body}</table>'


def takeaway(words: str) -> str:
    """The one line a slide leaves behind. The words are HTML, so <code> is kept."""
    return f'<div class="takeaway">{words}</div>'


def statement(words: str) -> str:
    """A sentence set large, in the scenario's serif."""
    return f'<p class="statement">{escape(words)}</p>'


def pushed(html: str) -> str:
    """A part pushed to the foot of the slide, with the room that is left above it."""
    return f'<div class="push">{html}</div>'


def facts(*items: str) -> str:
    """A few short facts in a line."""
    return '<div class="facts">' + "".join(f"<span>{escape(item)}</span>" for item in items) + "</div>"


def shot(path: Path, width: int) -> str:
    """A screenshot or a chart, shown `width` px wide."""
    return f'<img class="shot" src="{path.resolve().as_uri()}" width="{width}">'


def scaled(html: str, factor: float) -> str:
    """A component drawn smaller or larger than it was made, still sharp."""
    return f'<div style="zoom:{factor}">{html}</div>'


def can_list(items: list) -> str:
    """The notebook's You Can Now list, in two columns. Each item is HTML."""
    return '<ul class="can">' + "".join(f"<li>{item}</li>" for item in items) + "</ul>"
