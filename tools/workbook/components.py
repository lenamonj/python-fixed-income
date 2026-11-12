"""The drawn components of a Python for Fixed Income workbook, and the studio that turns them into pictures.

Each function below returns the HTML of one component, styled by design.css. Studio.png() draws it with a headless
browser at twice its display size and saves a PNG, which a notebook builder embeds as a data URI. README.md in this
folder says what each component is for and where it goes in a notebook.

Needs the author tools in requirements-dev.txt (playwright, Pillow) and, once, `python -m playwright install chromium`.
"""
import base64
import math
import re
import tempfile
from html import escape
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
WIDTH = 1200  # every component is 1200 px wide on screen
SCALE = 2     # and drawn at twice that, so it stays sharp on a high-resolution display

SERIES = "Python for Fixed Income"
AUTHOR = "Jeff Lenamon"
# the series in two lines: under the title on the landing page and on the cover that opens a course
TAGLINE = ("From your first line of code to your own AI agents.", "Every lesson is a fixed income problem.")

# Run in the page before a component is drawn. It names anything that would be cut off or would collide:
# a part that runs outside the picture, words wider than their own box, and a block marked data-above="<selector>"
# that reaches the block it must stay above. Shapes inside an <svg> are placed by number and are not checked.
FIT_CHECK = """() => {
  const root = document.querySelector('.pfi');
  const box = root.getBoundingClientRect();
  const say = (el) => '"' + (el.textContent.trim() || el.className).slice(0, 48) + '"';
  const found = new Set();
  for (const el of root.querySelectorAll('*')) {
    if (el.closest('svg')) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.right > box.right + 0.5 || r.left < box.left - 0.5 || r.bottom > box.bottom + 0.5 || r.top < box.top - 0.5)
      found.add(say(el) + ' runs outside the picture');
    else if (el.children.length === 0 && el.clientWidth > 0 && el.scrollWidth > el.clientWidth + 1)
      found.add(say(el) + ' is wider than its box');
  }
  for (const el of root.querySelectorAll('[data-above]')) {
    const under = root.querySelector(el.dataset.above);
    if (el.getBoundingClientRect().bottom + 12 > under.getBoundingClientRect().top)
      found.add(say(el.lastElementChild || el) + ' reaches the foot of the picture');
  }
  return [...found].slice(0, 4);
}"""


class Studio:
    """A headless browser that draws components. Use it as a context manager and draw as many as you like."""

    def __enter__(self):
        # imported here, so the HTML builders below work on a machine with no browser installed
        from playwright.sync_api import sync_playwright
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch()
        self._page = self._browser.new_page(viewport={"width": WIDTH, "height": 800}, device_scale_factor=SCALE)
        self._folder = tempfile.TemporaryDirectory()
        return self

    def __exit__(self, *error):
        self._browser.close()
        self._playwright.stop()
        self._folder.cleanup()

    def png(self, html: str, out: Path, colors: int = 256) -> Path:
        """Draw one component and save it as a PNG with a palette of at most `colors` colours."""
        page_file = Path(self._folder.name) / "component.html"
        page_file.write_text(
            f'<!doctype html><html><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="{(HERE / "design.css").as_uri()}"></head><body>{html}</body></html>',
            encoding="utf-8")
        self._page.goto(page_file.as_uri())
        self._page.evaluate("document.fonts.ready")
        block = self._page.locator(".pfi").first
        height = block.bounding_box()["height"]
        if height != int(height):
            # a part-pixel edge would be drawn as a faint line: give the component whole-pixel line heights
            raise ValueError(f"{out.name} is {height} px tall: its height must be a whole number of pixels")
        faults = self._page.evaluate(FIT_CHECK)
        if faults:
            raise ValueError(f"{out.name} does not fit: " + "; ".join(faults) + ". Shorten the words; never shrink the type.")
        block.screenshot(path=str(out))
        image = Image.open(out).convert("RGB")
        image.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(out, optimize=True)
        return out


def data_uri(path: Path) -> str:
    """A picture file as a data URI, ready for a markdown image link."""
    kind = "image/png" if path.suffix == ".png" else "image/jpeg"
    return f"data:{kind};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def curve(t: float, bend: float = 2.6) -> float:
    """The house curve: 0 at t = 0, 1 at t = 1, rising fast and then flattening, like a normal yield curve."""
    return (1 - math.exp(-bend * t)) / (1 - math.exp(-bend))


def curve_path(x0: float, x1: float, y0: float, y1: float, steps: int = 80) -> str:
    """The house curve as an SVG path from (x0, y0) to (x1, y1)."""
    points = [(x0 + (x1 - x0) * i / steps, y0 + (y1 - y0) * curve(i / steps)) for i in range(steps + 1)]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)


def badge() -> str:
    """The pfi badge: the letters over a short curve."""
    return (f'<span class="badge"><b>pfi</b><svg width="50" height="50" viewBox="0 0 50 50">'
            f'<path d="{curve_path(10, 40, 39.5, 34.5)}" fill="none" stroke="#17807F" stroke-width="2.4" '
            f'stroke-linecap="round"/></svg></span>')


def course_curve(width: int, height: int, left: int, right: int, base: int, top: int,
                 progress: float = 0.0, weeks: int = 4) -> str:
    """The house curve as the picture on a cover: the weeks of the course along the foot, and a marker where
    this notebook falls. progress runs from 0 (the course's first notebook) to 1 (its last)."""
    grid = "".join(f'<line x1="{left}" x2="{right}" y1="{y}" y2="{y}"/>'
                   for y in (base - (base - top) * k / 4 for k in range(1, 5)))
    ticks = ""
    for week in range(weeks + 1):
        x = left + (right - left) * week / weeks
        ticks += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{base}" y2="{base + 6}"/>'
    labels = "".join(
        f'<text x="{left + (right - left) * (week + 0.5) / weeks:.1f}" y="{base + 26}" text-anchor="middle">WEEK {week + 1}</text>'
        for week in range(weeks))
    here_x = left + (right - left) * progress
    here_y = base - 22 + (top + 14 - (base - 22)) * curve(progress)
    # the label sits where the curve is not: beside the marker while the curve climbs away from it, and above the
    # marker once the curve has flattened, where a label beside it would lie on the line
    label = (f'x="{here_x + 24:.1f}" y="{here_y + 4:.1f}" text-anchor="start"' if progress < 0.4 else
             f'x="{here_x + 13:.1f}" y="{here_y - 22:.1f}" text-anchor="end"')
    line = curve_path(left, right, base - 22, top + 14)
    area = f"{line} L{right} {base} L{left} {base} Z"
    return (
        f'<svg class="motif" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        f'<g stroke="#2A3D5C" stroke-width="1" stroke-dasharray="2 6" opacity=".8">{grid}</g>'
        f'<path d="{area}" fill="#5CC8C2" opacity=".055"/>'
        f'<g stroke="#2A3D5C" stroke-width="1"><line x1="{left}" x2="{right}" y1="{base}" y2="{base}"/>{ticks}</g>'
        f'<g fill="#8E9BB0" font-family="Plex Mono" font-weight="500" font-size="10.5" letter-spacing="1.6">{labels}</g>'
        f'<path d="{line}" fill="none" stroke="#5CC8C2" stroke-width="2.4" stroke-linecap="round"/>'
        f'<circle cx="{here_x:.1f}" cy="{here_y:.1f}" r="13" fill="none" stroke="#5CC8C2" stroke-width="1" opacity=".55"/>'
        f'<circle cx="{here_x:.1f}" cy="{here_y:.1f}" r="5.5" fill="#F7F3EA" stroke="#5CC8C2" stroke-width="2.4"/>'
        f'<text {label} fill="#5CC8C2" font-family="Plex Mono" font-weight="500" font-size="10.5" letter-spacing="1.6">'
        f'YOU ARE HERE</text></svg>')


def cover(course_line: str, plate: str, title: str, subtitle: str = "", statement: str = "", meta: tuple = (),
          progress: float = 0.0, weeks: int = 4, compact: bool = False) -> str:
    """The first picture of a notebook: series, course, week and day, the title, and where the day sits in the course.

    statement is one or two short lines under the title; meta is a few facts for the foot, such as "ABOUT 45 MIN".
    compact is the shorter cover: every notebook's but a course's first, and every solutions notebook's.
    The title's size steps down as the title gets longer, so no one sets it by hand."""
    height = 420 if compact else 600
    motif = course_curve(WIDTH, height, 742, 1144, height - 132, 132 if compact else 150, progress, weeks)
    step = 1 if len(title) <= 14 else 2 if len(title) <= 22 else 3 if len(title) <= 36 else 4
    sub = f'<p class="sub">{escape(subtitle)}</p>' if subtitle else ""
    lines = f'<p class="statement">{"<br>".join(escape(line) for line in statement.splitlines())}</p>' if statement else ""
    facts = "".join(f"<span>{escape(fact)}</span>" for fact in meta)
    return (
        f'<div class="pfi cover{" compact" if compact else ""}">{motif}'
        f'<header><div class="brand">{badge()}<span class="series">{escape(SERIES.upper())}</span></div>'
        f'<div class="course">{escape(course_line)}</div></header>'
        f'<main data-above="footer"><div class="plate">{escape(plate)}</div><h1 class="step{step}">{escape(title)}</h1>{sub}{lines}</main>'
        f'<footer><div>Created by <b>{escape(AUTHOR)}</b></div><div class="meta">{facts}</div></footer></div>')


def tracker(label: str, goal: str, minutes: int, index: int = 0, count: int = 0) -> str:
    """The strip above a part of the notebook: what it is, what it is for, and about how long it takes.
    For a numbered section, index and count draw its place among the sections ("SECTION 3 OF 8")."""
    marks = "".join(f'<i class="{"done" if i < index else "now" if i == index else ""}"></i>' for i in range(1, count + 1))
    track = f'<span class="track">{marks}</span>' if count else ""
    return (f'<div class="pfi tracker"><span class="count">{escape(label)}</span>{track}'
            f'<span class="goal">{escape(goal)}</span><span class="time">ABOUT {minutes} MIN</span></div>')


def figure(body: str, number: int, caption: str, flush: bool = False) -> str:
    """An ivory plate with a numbered caption: the frame of every diagram, screenshot, and chart of the course."""
    return (f'<div class="pfi figure"><div class="body{" flush" if flush else ""}">{body}</div>'
            f'<div class="cap"><span class="no">FIGURE {number}</span><span class="words">{escape(caption)}</span></div></div>')


def caption_strip(number: int, caption: str) -> str:
    """A figure's caption on its own, for apply.py to set under a picture the notebook already had."""
    return (f'<div class="pfi figure strip"><div class="cap"><span class="no">FIGURE {number}</span>'
            f'<span class="words">{escape(caption)}</span></div></div>')


def screenshot(path: Path, width: int) -> str:
    """A screenshot for a figure's body, shown `width` px wide, its height kept to a whole pixel."""
    wide, high = Image.open(path).size
    return f'<img class="shot" src="{path.resolve().as_uri()}" width="{width}" height="{round(high * width / wide)}">'


def stage(width: int, height: int, *parts: str) -> str:
    """A diagram: boxes, words, and arrows placed by position."""
    return f'<div class="stage" style="width:{width}px;height:{height}px">{"".join(parts)}</div>'


def box(x: int, y: int, w: int, h: int, kind: str = "") -> str:
    """A diagram box. kind: tint (the engine), code, soft, file (dashed), cell."""
    return f'<div class="box {kind}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>'


def words(x: int, y: int, w: int, text: str, kind: str = "") -> str:
    """Words in a diagram, centred in a strip w wide. kind: b (bold), h (heading), m (code), s (small), step, left."""
    return f'<div class="t {kind}" style="left:{x}px;top:{y}px;width:{w}px">{escape(text)}</div>'


def arrows(width: int, height: int, *lines: tuple) -> str:
    """Arrows over a diagram, each one (x1, y1, x2, y2); a fifth item "dash" draws a dashed line with no head."""
    drawn = ""
    for line in lines:
        x1, y1, x2, y2 = line[:4]
        if len(line) > 4:
            drawn += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#8C95A3" stroke-width="1.2" stroke-dasharray="5 5"/>'
        else:
            drawn += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#17807F" stroke-width="2.2" marker-end="url(#head)"/>'
    return (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs>'
            f'<marker id="head" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="#17807F"/></marker></defs>{drawn}</svg>')


ROUTE_LEFT, ROUTE_RIGHT = 96, 1104  # where the first and the last section's points sit on a route
ROUTE_ROOM = 2 * ROUTE_LEFT - 8  # the widest that words centred on the first or the last point can be and stay in the picture


def route_stop_width(count: int, tight: bool = False) -> int:
    """How wide the words under one point of a route can be: the room between two points less a gutter (12 px,
    or 10 in the small type), and never so wide that the first or the last point's words leave the picture."""
    return min(ROUTE_ROOM, (ROUTE_RIGHT - ROUTE_LEFT) // max(count - 1, 1) - (10 if tight else 12))


def wraps_into(title: str, letters: int, lines: int) -> bool:
    """Whether the title, wrapped word by word into lines of at most `letters` letters, needs no more than `lines`."""
    used, filled = 1, 0
    for word in re.findall(r"[^\s-]+-?|-", title):  # a browser may break a line after a hyphen
        if len(word) > letters:
            return False
        if filled and filled + 1 + len(word) > letters:
            used, filled = used + 1, len(word)
        else:
            filled += (1 if filled else 0) + len(word)
    return used <= lines


def route_lines(titles: list) -> int:
    """How many lines the route's names need: 2 in the house type (14.5 px), else 3 or 4 in the small type (13 px).
    0 means some title fits in neither: route_misfits names them."""
    letters = int(route_stop_width(len(titles)) / 7.9)  # 14.5 px semibold runs about 7.9 px a letter
    if all(wraps_into(title, letters, 2) for title in titles):
        return 2
    letters = int(route_stop_width(len(titles), tight=True) / 7.1)  # 13 px semibold runs about 7.1 px a letter
    for lines in (3, 4):
        if all(wraps_into(title, letters, lines) for title in titles):
            return lines
    return 0


def route_misfits(titles: list) -> list:
    """The titles too long to set under their points even in four lines of the small type."""
    letters = int(route_stop_width(len(titles), tight=True) / 7.1)
    return [title for title in titles if not wraps_into(title, letters, 4)]


def route(sections: list, flags: dict | None = None, head: str = "", total: str = "") -> str:
    """The day's sections as points on the house curve, each with its title and minutes under it. sections holds
    (number, title, minutes) for each one; flags maps a section's position (from 1) to a few words set above its
    point, for the moments that matter. Titles that need it are set smaller, in up to four lines (route_lines)."""
    flags = flags or {}
    left, right, low, high, floor = ROUTE_LEFT, ROUTE_RIGHT, 190, 78, 216
    count = len(sections)
    lines = route_lines([title for _, title, _ in sections])
    if not lines:
        raise ValueError(f"these route titles fit under no point: {route_misfits([title for _, title, _ in sections])}")
    wide = route_stop_width(count, tight=lines > 2)
    drawn = f'<path d="{curve_path(left, right, low, high)}" fill="none" stroke="#17807F" stroke-width="2.4" stroke-linecap="round"/>'
    stops = ""
    for i, (number, title, minutes) in enumerate(sections):
        t = i / max(count - 1, 1)
        x, y = left + (right - left) * t, low + (high - low) * curve(t)
        flagged = (i + 1) in flags
        drawn = (f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y + 9:.1f}" y2="{floor}" stroke="#D8D0BE" stroke-width="1" stroke-dasharray="2 4"/>'
                 + drawn)
        fill, edge = ("#A97A1F", "#A97A1F") if flagged else ("#F7F3EA", "#17807F")
        drawn += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{fill}" stroke="{edge}" stroke-width="2.4"/>'
        if flagged:
            drawn += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y - 12:.1f}" y2="{y - 24:.1f}" stroke="#A97A1F" stroke-width="1.2"/>'
            stops += (f'<div class="flag" style="left:{x - ROUTE_ROOM / 2:.1f}px;top:{y - 44:.1f}px;width:{ROUTE_ROOM}px">'
                      f'{escape(flags[i + 1])}</div>')
        stops += (f'<div class="stop" style="left:{x - wide / 2:.1f}px;width:{wide}px"><span class="no">{escape(number)}</span>'
                  f'<span class="name">{escape(title)}</span><span class="min">{minutes} MIN</span></div>')
    heads = (f'<div class="head">{escape(head)}</div>' if head else "") + (f'<div class="head right">{escape(total)}</div>' if total else "")
    look = {2: "", 3: " tight", 4: " tight four"}[lines]
    return (f'<div class="route{look}">{heads}<svg width="{WIDTH}" height="330" viewBox="0 0 {WIDTH} 330">'
            f'{drawn}</svg>{stops}</div>')


def note(sender: str, state: str, tasks: list, text: str = "") -> str:
    """The scenario as an object on the desk: who it is from, what it asks, and which asks are answered so far.
    tasks holds (words, answer) pairs; an empty answer is an open box. With no text it is the short progress strip."""
    listed = ""
    for task, answer in tasks:
        result = f"<b>{escape(answer)}</b>" if answer else ""
        listed += f'<span class="task{" done" if answer else ""}"><span class="tick"></span>{escape(task)}{result}</span>'
    said = f'<div class="words">{escape(text)}</div>' if text else ""
    return (f'<div class="pfi note{"" if text else " strip"}"><div class="head"><span class="from">{escape(sender)}</span>'
            f'<span class="state">{escape(state)}</span></div>{said}<div class="tasks">{listed}</div></div>')


def mistake(name: str, typed: str, got: str, why: str, instead: str, gives: str, how: str) -> str:
    """A common mistake as a plate: what was typed and what came back, beside what to type instead."""
    def side(kind: str, label: str, code: str, result: str, words_under: str) -> str:
        return (f'<div class="side {kind}"><span class="label">{escape(label)}</span><div class="line"><span>{escape(code)}</span>'
                f'<span class="gives">gives</span><span class="out">{escape(result)}</span></div>'
                f'<p>{escape(words_under)}</p></div>')
    return (f'<div class="pfi mistake"><div class="head"><span class="what">COMMON MISTAKE</span>'
            f'<span class="name">{escape(name)}</span></div><div class="sides">'
            f'{side("wrong", "YOU TYPED", typed, got, why)}{side("right", "TYPE THIS INSTEAD", instead, gives, how)}</div></div>')


def next_step(label: str, plate: str, title: str, line: str) -> str:
    """The card that closes a notebook: where to go next."""
    return (f'<div class="pfi next"><div class="where"><span class="label">{escape(label)}</span>'
            f'<span class="plate">{escape(plate)}</span></div><div class="what"><span class="title">{escape(title)}</span>'
            f'<span class="line">{escape(line)}</span></div><div class="go"><svg width="54" height="54" viewBox="0 0 54 54">'
            f'<path d="M17 27 H36 M29 20 L36 27 L29 34" fill="none" stroke="#5CC8C2" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round"/></svg></div></div>')
