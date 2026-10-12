"""Draw the README wordmark: the pfi badge and the course name on two lines, for light and dark themes.

Usage (from the repo root, with Pillow installed):  python tools/make_wordmark.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

from notebook_header import bezier, mono, serif

OUT = Path(__file__).resolve().parent.parent / "assets" / "readme"

DARK_GREEN = "#123d2f"
PALE_GREEN = "#eaf4ee"
CURVE_GREEN = "#7fd1a8"
ACCENT_GREEN = "#1c7a57"


def draw(badge_fill: str, badge_text: str, curve: str, name_fill: str) -> Image.Image:
    image = Image.new("RGBA", (1100, 330), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(image)

    canvas.rounded_rectangle((20, 30, 290, 300), radius=36, fill=badge_fill)
    canvas.text((155, 186), "pfi", font=mono(100, bold=True), fill=badge_text, anchor="ms")
    line = bezier((70, 246), (106, 222), (162, 214), (240, 210))
    canvas.line(line, fill=curve, width=8, joint="curve")
    for end in (line[0], line[-1]):
        canvas.ellipse((end[0] - 4, end[1] - 4, end[0] + 4, end[1] + 4), fill=curve)

    # Two lines, left-aligned beside the badge, the block centred on the badge's middle (y = 165); Jeff, 2026-10-12
    font = serif(110, 600)
    canvas.text((350, 140), "Python for", font=font, fill=name_fill, anchor="ls")
    canvas.text((350, 260), "Fixed Income", font=font, fill=name_fill, anchor="ls")
    return image


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    draw(DARK_GREEN, PALE_GREEN, CURVE_GREEN, DARK_GREEN).save(OUT / "wordmark-light.png", optimize=True)
    draw(PALE_GREEN, DARK_GREEN, ACCENT_GREEN, PALE_GREEN).save(OUT / "wordmark-dark.png", optimize=True)
    print("wrote", OUT)
