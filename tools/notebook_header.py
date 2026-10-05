"""Draw the course banner and put it at the top of a notebook.

Every notebook in the course opens with the same banner: the "pfi" badge, the course
name, the course line, the author byline, and on the right the week, day, and notebook title.

The banner is embedded in the first markdown cell as a base64 PNG, so it shows in
VS Code and Colab without the repo being public. A copy is saved in assets/headers.

Usage (from the repo root, with Pillow and nbformat installed):

    python tools/notebook_header.py course1_python_foundations/week1/day2/02_files_and_folders.ipynb --week 1 --day 2 --title "Files and Folders"

Course 1 is the default. A later course passes --course, which changes the course line, the alt text,
and the saved copy's name (assets/headers/course2_<notebook>.png), so it cannot collide with Course 1's:

    python tools/notebook_header.py course2_bond_math/week1/day1/01_time_value_of_money.ipynb --course 2 --week 1 --day 1 --title "Time Value of Money"

Courses 1 to 5 are known (course 4 added 2026-10-04, course 5 added 2026-10-05; the banners of the earlier courses
are unchanged).
"""
import argparse
import base64
import io
from pathlib import Path

import nbformat
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
FONTS = REPO / "assets" / "fonts"
HEADERS = REPO / "assets" / "headers"

COURSE_NAME = "Python for Fixed Income"
# course number: (course line on the banner, course in the alt text, prefix of the saved copy's file name)
COURSES = {
    1: ("COURSE 1 · PYTHON FOUNDATIONS", "Course 1: Python Foundations", ""),
    2: ("COURSE 2 · BOND MATH", "Course 2: Bond Math", "course2_"),
    3: ("COURSE 3 · MARKET DATA AND TIME SERIES", "Course 3: Market Data and Time Series", "course3_"),
    4: ("COURSE 4 · MACHINE LEARNING", "Course 4: Machine Learning", "course4_"),
    5: ("COURSE 5 · ADVANCED MACHINE LEARNING", "Course 5: Advanced Machine Learning", "course5_"),
}
COURSE_LINE = COURSES[1][0]
BYLINE_PREFIX = "Created by "
AUTHOR = "Jeff Lenamon"
HEADER_TAG = "course-header"

# drawn at twice the display size so it stays sharp on high-resolution screens
WIDTH, HEIGHT = 2400, 480
BACKGROUND = "#eef3f0"
DARK_GREEN = "#123d2f"
PALE_GREEN = "#eaf4ee"
CURVE_GREEN = "#7fd1a8"
MUTED_GREEN = "#4e6b5f"
ACCENT_GREEN = "#1c7a57"
RIGHT_EDGE = 2304
TITLE_MAX_WIDTH = 520


def serif(size: int, weight: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(FONTS / "Newsreader-Variable.ttf"), size)
    font.set_variation_by_axes([weight, min(size, 72)])  # axes: weight, optical size
    return font


def sans(size: int, weight: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(FONTS / "IBMPlexSans-Variable.ttf"), size)
    font.set_variation_by_axes([weight, 100])  # axes: weight, width
    return font


def mono(size: int, bold: bool) -> ImageFont.FreeTypeFont:
    name = "IBMPlexMono-Bold.ttf" if bold else "IBMPlexMono-Medium.ttf"
    return ImageFont.truetype(str(FONTS / name), size)


def spaced_width(text: str, font: ImageFont.FreeTypeFont, spacing: int) -> float:
    return sum(font.getlength(ch) for ch in text) + spacing * (len(text) - 1)


def draw_spaced(draw: ImageDraw.ImageDraw, x: float, y: float, text: str,
                font: ImageFont.FreeTypeFont, fill: str, spacing: int) -> None:
    """Draw text on a baseline with extra space between letters."""
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += font.getlength(ch) + spacing


def bezier(p0, p1, p2, p3, steps: int = 60) -> list:
    points = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        points.append((x, y))
    return points


def draw_banner(week: int, day: int, title: str, course: int = 1) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    # badge
    draw.rounded_rectangle((96, 104, 368, 376), radius=36, fill=DARK_GREEN)
    draw.text((232, 260), "pfi", font=mono(100, bold=True), fill=PALE_GREEN, anchor="ms")
    curve = bezier((148, 320), (184, 296), (240, 288), (316, 284))
    draw.line(curve, fill=CURVE_GREEN, width=8, joint="curve")
    for end in (curve[0], curve[-1]):
        draw.ellipse((end[0] - 4, end[1] - 4, end[0] + 4, end[1] + 4), fill=CURVE_GREEN)

    # course name and course line
    draw.text((456, 222), COURSE_NAME, font=serif(104, 600), fill=DARK_GREEN, anchor="ls")
    draw_spaced(draw, 460, 296, COURSES[course][0], sans(38, 500), MUTED_GREEN, spacing=7)

    # byline: name only, no title and no employer
    prefix_font = sans(36, 400)
    draw.text((460, 364), BYLINE_PREFIX, font=prefix_font, fill=MUTED_GREEN, anchor="ls")
    draw.text((460 + prefix_font.getlength(BYLINE_PREFIX), 364), AUTHOR, font=sans(36, 600), fill=DARK_GREEN, anchor="ls")

    # week and day, right-aligned
    label = f"WEEK {week} · DAY {day}"
    label_font = mono(34, bold=False)
    draw_spaced(draw, RIGHT_EDGE - spaced_width(label, label_font, 4), 220, label, label_font, ACCENT_GREEN, spacing=4)

    # notebook title, right-aligned, shrunk until it fits
    size = 50
    while serif(size, 500).getlength(title) > TITLE_MAX_WIDTH and size > 28:
        size -= 2
    draw.text((RIGHT_EDGE, 296), title, font=serif(size, 500), fill=DARK_GREEN, anchor="rs")
    return image


def header_markdown(week: int, day: int, title: str, image: Image.Image, course: int = 1) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    alt = f"{COURSE_NAME} | {COURSES[course][1]} | Created by {AUTHOR} | Week {week}, Day {day} | {title}"
    return f"![{alt}](data:image/png;base64,{encoded})"


def apply_header(notebook_path: Path, week: int, day: int, title: str, course: int = 1) -> None:
    """Insert the banner as the first cell, replacing an earlier banner if there is one."""
    if course not in COURSES:
        raise ValueError(f"course must be one of {sorted(COURSES)}, not {course}")
    image = draw_banner(week, day, title, course)
    HEADERS.mkdir(parents=True, exist_ok=True)
    image.save(HEADERS / f"{COURSES[course][2]}{notebook_path.stem}.png", optimize=True)

    nb = nbformat.read(notebook_path, as_version=4)
    cell = nbformat.v4.new_markdown_cell(header_markdown(week, day, title, image, course))
    cell.metadata["tags"] = [HEADER_TAG]
    if nb.cells and HEADER_TAG in nb.cells[0].metadata.get("tags", []):
        nb.cells[0] = cell
    else:
        nb.cells.insert(0, cell)
    nbformat.write(nb, notebook_path)
    print("header applied:", notebook_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Put the course banner at the top of a notebook.")
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--week", type=int, required=True)
    parser.add_argument("--day", type=int, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--course", type=int, default=1, choices=sorted(COURSES))
    args = parser.parse_args()
    apply_header(args.notebook, args.week, args.day, args.title, args.course)
