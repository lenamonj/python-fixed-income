"""The series' landing pages: the pictures of the repo's README.md and of each course's README.md, drawn in the
workbook design system.

    .venv\\Scripts\\python.exe tools\\workbook\\landing.py

GitHub shows a README in a column 830 px wide and strips every style, so a page keeps the system's one rule:
words are typed, structure is drawn. This file draws the structure into assets/readme/landing/, 830 px wide and
saved at twice that. The words, the tables, and every link are typed in the README itself.

The numbers on the pictures are counted from the repo, never typed: run this file again when a notebook, a course,
or an Excel comparison is added, and change the same numbers where README.md types them (a test compares the two).
Each run also sets the cover at the top of every course's README, so a course page never falls behind.
"""
import re
from html import escape
from pathlib import Path

try:
    from . import components as c
except ImportError:  # run as a script
    import components as c

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "assets" / "readme" / "landing"
STYLE = f'<link rel="stylesheet" href="{(Path(__file__).with_name("landing.css")).as_uri()}">'

# stage, its short name for a cover's axis, the courses it holds there, then (label, short name, course folder) for each course
STAGES = [
    ("Foundations", "FOUNDATIONS", "COURSES 1 TO 3", [
        ("Course 1", "Python Foundations", "course01_python_foundations"),
        ("Course 2", "Bond Math", "course02_bond_math"),
        ("Course 3", "Market Data", "course03_market_data")]),
    ("Machine learning", "MACHINE LEARNING", "COURSES 4 TO 6", [
        ("Course 4", "Machine Learning", "course04_machine_learning"),
        ("Course 5", "Advanced ML", "course05_advanced_ml"),
        ("Course 5B", "Time Series Models", "course05b_time_series"),
        ("Course 5C", "Risk Models", "course05c_risk_models"),
        ("Course 6", "Neural Networks", "course06_neural_networks")]),
    ("Language models and agents", "LLMS AND AGENTS", "COURSES 7 AND 8", [
        ("Course 7", "NLP, RAG, and LLMs", "course07_nlp_and_llms"),
        ("Course 8", "Agentic AI", "course08_agentic_ai")]),
    ("Build and ship", "BUILD AND SHIP", "9, 10, AND BONUS", [
        ("Course 9", "Deployment", "course09_deployment"),
        ("Course 10", "Implementing RAG", "course10_rag"),
        ("Bonus", "Your Own Coding Agent", "course_bonus_coding_agent")]),
]
STEPS = [
    ("STEP 1", "Setup", "Colab in your browser, or Python and VS Code on Windows."),
    ("STEP 2", "Day 0: Start Here", "Python, a notebook, a library. Your first lines of code."),
    ("STEP 3", "Day 1: Introduction", "The first full lesson, on a desk of four bonds."),
]
INSIDE = [
    ("c2_price_yield.png", "Course 2", "Price and yield"),
    ("c2_convexity.png", "Course 2", "Duration and convexity"),
    ("c3_curve_slopes.png", "Course 3", "Treasury curve slopes"),
    ("c4_correlation_heatmap.png", "Course 4", "Correlation across the curve"),
    ("c5_shap_waterfall.png", "Course 5", "A model output, by SHAP value"),
    ("c7_indenture_embeddings.png", "Course 7", "An indenture, as embeddings"),
]


# ---------------------------------------------------------------- the numbers, counted from the repo
def weeks_of(folder: str) -> int:
    """A course's length in weeks. The Bonus is one day, so it counts as none."""
    return 0 if folder.startswith("course_bonus") else len(list((REPO / folder).glob("week*")))


def notebooks_of(folder: str) -> int:
    """A course's teaching notebooks: every notebook in its folder but the solutions."""
    return sum(1 for path in (REPO / folder).glob("**/*.ipynb")
               if not path.stem.endswith("_solutions") and ".ipynb_checkpoints" not in path.parts)


def courses() -> list:
    """Every course in the order it is taken, with its stage, the week of the series it starts in, its length, and
    its full title, which is the heading of its own README ("## Course 2: Bond Math")."""
    listed, week = [], 0
    for place, (stage, short, held, held_courses) in enumerate(STAGES, start=1):
        for label, name, folder in held_courses:
            heading = re.search(r"^## (?:Course \w+|Bonus): (.+)$", (REPO / folder / "README.md").read_text(encoding="utf-8"), re.M)
            listed.append({"label": label, "name": name, "title": heading.group(1) if heading else name, "folder": folder,
                           "stage": stage, "stage_short": short, "stage_place": place, "start": week,
                           "weeks": weeks_of(folder), "notebooks": notebooks_of(folder)})
            week += weeks_of(folder)
    return listed


def counts() -> dict:
    """What the page says about the series: its notebooks, its weeks, and its Excel comparisons."""
    listed = courses()
    table = [line for line in (REPO / "EXCEL.md").read_text(encoding="utf-8").splitlines() if line.startswith("|")]
    # every table row but the heading and the rule under it is one comparison
    excel = sum(1 for line in table if not re.match(r"\|\s*:?-{2,}", line) and not line.lower().startswith("| in excel"))
    return {"notebooks": sum(course["notebooks"] for course in listed), "weeks": sum(course["weeks"] for course in listed),
            "excel": excel, "courses": sum(1 for course in listed if course["label"] != "Bonus")}


def land(html: str) -> str:
    """A component of the system, set at the landing page's width."""
    return html.replace('class="pfi ', 'class="pfi land ', 1)


# ---------------------------------------------------------------- the components
def series_curve(height: int, base: int, low: int, high: int, here: int | None = None) -> str:
    """The house curve as the picture on a cover: every course a point on it, the weeks of the series along the
    foot, and the four stages marked there. here is the place of the course to mark, from 0; with none, the
    series' own page marks where to start."""
    left, right = 40, 790
    listed = courses()
    total = sum(course["weeks"] for course in listed)

    def at(week: float) -> tuple:
        t = week / total
        return left + (right - left) * t, low + (high - low) * c.curve(t)

    line = c.curve_path(left, right, low, high)
    drawn = f'<path d="{line} L{right} {base} L{left} {base} Z" fill="#5CC8C2" opacity=".055"/>'
    drawn += f'<line x1="{left}" x2="{right}" y1="{base}" y2="{base}" stroke="#2A3D5C" stroke-width="1"/>'
    labels = ""
    for stage, short, held, held_courses in STAGES:
        inside = [course for course in listed if course["stage"] == stage]
        (x0, y0), (x1, y1) = at(inside[0]["start"]), at(inside[-1]["start"] + inside[-1]["weeks"])
        # a stage's edge runs from the curve down to the foot
        for x, y in ((x0, y0), (x1, y1)):
            drawn += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y:.1f}" y2="{base + 6}" stroke="#2A3D5C" stroke-width="1" stroke-dasharray="2 4"/>'
        middle = (x0 + x1) / 2
        labels += (f'<text x="{middle:.1f}" y="{base + 22}" text-anchor="middle" fill="#C5CEDB">{escape(short)}</text>'
                   f'<text x="{middle:.1f}" y="{base + 37}" text-anchor="middle" fill="#8E9BB0" font-size="8.5">{escape(held)}</text>')
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="#0E1B2E" stroke="#5CC8C2" stroke-width="1.8"/>'
                   for x, y in (at(course["start"]) for course in listed))
    marked = listed[here or 0]
    x, y = at(marked["start"])
    if here is not None and marked["weeks"]:
        # the course's own weeks, heavier on the foot
        drawn += f'<line x1="{x:.1f}" x2="{at(marked["start"] + marked["weeks"])[0]:.1f}" y1="{base}" y2="{base}" stroke="#5CC8C2" stroke-width="3"/>'
    words = "START HERE" if here is None else "YOU ARE HERE"
    side = (x - 22, "end") if x > 600 else (x + 22, "start")
    mark = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="none" stroke="#5CC8C2" stroke-width="1" opacity=".55"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#F7F3EA" stroke="#5CC8C2" stroke-width="2.2"/>'
            f'<text x="{side[0]:.1f}" y="{y + 19:.1f}" text-anchor="{side[1]}" fill="#5CC8C2" font-size="10">{words}</text>')
    return (f'<svg class="motif" width="830" height="{height}" viewBox="0 0 830 {height}">{drawn}'
            f'<path d="{line}" fill="none" stroke="#5CC8C2" stroke-width="2.2" stroke-linecap="round"/>{dots}'
            f'<g font-family="Plex Mono" font-weight="500" font-size="9.5" letter-spacing="1.3">{labels}{mark}</g></svg>')


def cover(kind: str, plate: str, title: str, lines: tuple, meta: tuple, motif: str, course: bool = False) -> str:
    """A landing page's cover: the series' brand, a plate, the title, and the house curve under them."""
    step = "" if not course or len(title) <= 18 else ' class="s2"' if len(title) <= 25 else ' class="s3"'
    sub = f'<p class="sub">{"<br>".join(escape(part) for part in lines)}</p>' if lines else ""
    facts = "".join(f"<span>{escape(fact)}</span>" for fact in meta)
    return (f'<div class="pfi land hero{" course" if course else ""}">{motif}'
            f'<header><div class="brand">{c.badge()}<span class="series">{escape(c.SERIES.upper())}</span></div>'
            f'<div class="kind">{escape(kind)}</div></header>'
            f'<main><div class="plate">{escape(plate)}</div><h1{step}>{escape(title)}</h1>{sub}</main>'
            f'<footer><div>Created by <b>{escape(c.AUTHOR)}</b></div><div class="meta">{facts}</div></footer></div>')


def hero(facts: dict) -> str:
    """The series' cover, at the top of the repo's README."""
    return cover("THE SERIES", f'{facts["courses"]} COURSES AND A BONUS · FROM ZERO', c.SERIES, c.TAGLINE,
                 (f'{facts["notebooks"]} NOTEBOOKS', f'{facts["weeks"]} WEEKS', "FREE"), series_curve(548, 440, 410, 322))


def length_of(course: dict) -> tuple:
    """A course's length as two short facts."""
    return ((f'{course["weeks"]} WEEKS' if course["weeks"] else "1 DAY"),
            f'{course["notebooks"]} NOTEBOOK{"" if course["notebooks"] == 1 else "S"}')


def course_hero(place: int) -> str:
    """A course's cover, at the top of its README: its name, and where it sits in the series."""
    course = courses()[place]
    return cover(f'STAGE {course["stage_place"]} OF {len(STAGES)} · {course["stage_short"]}', course["label"].upper(), course["title"], (),
                 length_of(course) + ("FREE",), series_curve(452, 344, 318, 262, place), course=True)


def numbers(facts: dict) -> str:
    """Four facts about the series on one plate."""
    shown = [(str(facts["notebooks"]), "NOTEBOOKS", "With worked solutions."),
             (str(facts["excel"]), "EXCEL COMPARISONS", "Formula by formula."),
             (str(facts["weeks"]), "WEEKS", "One notebook a day."),
             ("$0", "TO TAKE", "No key needed to run.")]
    return '<div class="pfi land numbers">' + "".join(
        f'<div class="fact"><span class="n">{escape(n)}</span><span class="what">{escape(what)}</span>'
        f'<span class="more">{escape(more)}</span></div>' for n, what, more in shown) + "</div>"


def step(plate: str, title: str, line: str) -> str:
    """One of the three cards under Start here. Each is a link in the README."""
    return (f'<div class="pfi land step"><span class="plate">{escape(plate)}</span><span class="title">{escape(title)}</span>'
            f'<span class="line">{escape(line)}</span><div class="go"><svg width="30" height="30" viewBox="0 0 30 30">'
            f'<path d="M9 15 H20 M16 11 L20 15 L16 19" fill="none" stroke="#5CC8C2" stroke-width="1.6" stroke-linecap="round" '
            f'stroke-linejoin="round"/></svg></div></div>')


def series_map(facts: dict) -> str:
    """The courses in their four stages, in the order they are taken, as a numbered figure."""
    then = ('<svg class="then" width="24" height="12" viewBox="0 0 24 12"><path d="M5 6 H18 M14 2 L18 6 L14 10" fill="none" '
            'stroke="#17807F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    rows = ""
    for place, (name, short, held, held_courses) in enumerate(STAGES, start=1):
        span = sum(weeks_of(folder) for label, title, folder in held_courses)
        length = f"{span} WEEKS" + (" AND A DAY" if any(label == "Bonus" for label, title, folder in held_courses) else "")
        cards = then.join(f'<div class="card"><span class="label">{escape(label.upper())}</span>'
                          f'<span class="name">{escape(title)}</span></div>' for label, title, folder in held_courses)
        rows += (f'<div class="row"><div class="stage-name"><span class="no">STAGE {place}</span>'
                 f'<span class="name">{escape(name)}</span><span class="weeks">{length}</span></div>'
                 f'<div class="cards">{cards}</div></div>')
    body = (f'<div class="series-map"><div class="head">THE SERIES · THE ROUTE</div>'
            f'<div class="head right">{facts["weeks"]} WEEKS · {facts["notebooks"]} NOTEBOOKS</div>{rows}</div>')
    return land(c.figure(body, 1, "Twelve courses and a bonus in four stages, in the order they are taken.", flush=True))


def inside() -> str:
    """Six charts as six notebooks draw them, on one plate. A chart is never restyled: it is what the student's code draws."""
    charts = "".join(
        f'<div class="chart"><img src="{(REPO / "assets" / "readme" / "gallery" / name).as_uri()}" alt="">'
        f'<span class="label"><b>{escape(course.upper())}</b>{escape(words)}</span></div>' for name, course, words in INSIDE)
    return land(c.figure(f'<div class="inside">{charts}</div>', 2, "Six charts, each as the student's own code draws it.", flush=True))


def closing() -> str:
    """The card that ends the page: the way in."""
    return land(c.next_step("START", "STEP 1 · SETUP", "Get your computer ready", STEPS[0][2]))


# ---------------------------------------------------------------- the course pages
WORDMARK = re.compile(r'<picture>\s*<source[^>]*wordmark-dark\.png">\s*<img[^>]*wordmark-light\.png"[^>]*>\s*</picture>')
COVER = re.compile(r'<a href="\.\./README\.md"><img src="\.\./assets/readme/landing/course[^"]*\.png"[^>]*></a>')
OWN_BADGES = re.compile(r'^\[!\[(?:Course \w+|Bonus|Length)\]\(https://img\.shields\.io/[^\n]*\n', re.M)
OLD_COLOUR = re.compile(r"-(?:123D2F|1C7A57|0EA5E9|22C55E)\?style=for-the-badge")


def course_page(place: int) -> bool:
    """Set a course README's top to the system: its cover in place of the old wordmark, as a link back to the
    series, and its badges in the system's two colours. The cover says the course and its length, so the two
    badges that said the same go. Returns whether the file changed. Nothing below the top is touched."""
    course = courses()[place]
    path = REPO / course["folder"] / "README.md"
    text = path.read_text(encoding="utf-8")
    weeks, notebooks = (fact.lower() for fact in length_of(course))
    alt = (f'{c.SERIES}. {course["label"]}: {course["title"]}. {weeks}, {notebooks}, free. '
           f'Stage {course["stage_place"]} of {len(STAGES)}, {course["stage"]}. Created by {c.AUTHOR}.')
    tag = f'<a href="../README.md"><img src="../assets/readme/landing/{course["folder"]}.png" width="830" alt="{escape(alt)}"></a>'
    if not (WORDMARK.search(text) or COVER.search(text)):
        raise ValueError(f"{path} has neither the old wordmark nor a cover at its top")
    made = COVER.sub(lambda found: tag, WORDMARK.sub(lambda found: tag, text, count=1), count=1)
    made = OLD_COLOUR.sub("-17807F?style=for-the-badge&labelColor=0E1B2E", OWN_BADGES.sub("", made))
    if made != text:
        path.write_text(made, encoding="utf-8", newline="\n")
    return made != text


def draw() -> dict:
    """Draw every picture of the landing pages, set each course page's top, and return the numbers they carry."""
    facts = counts()
    OUT.mkdir(parents=True, exist_ok=True)
    pictures = {"hero": hero(facts), "numbers": numbers(facts), "route": series_map(facts), "inside": inside(), "next": closing()}
    pictures.update({f"step{place}": step(*parts) for place, parts in enumerate(STEPS, start=1)})
    pictures.update({course["folder"]: course_hero(place) for place, course in enumerate(courses())})
    with c.Studio() as studio:
        for name, html in pictures.items():
            path = studio.png(STYLE + html, OUT / f"{name}.png")
            print(path.name, c.Image.open(path).size, f"{path.stat().st_size / 1024:.0f} KB")
    for place, course in enumerate(courses()):
        if course_page(place):
            print("set the top of", f'{course["folder"]}/README.md')
    return facts


if __name__ == "__main__":
    print(draw())
