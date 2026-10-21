"""Draw the README's "The path" diagram: the series' four stages, each a band of course cards, for light and dark themes.

An image rather than a Mermaid block, because the GitHub mobile app shows Mermaid as raw code (Jeff, 2026-10-18).

Usage (from the repo root, with Pillow installed):  python tools/make_path_diagram.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

from notebook_header import mono, sans

OUT = Path(__file__).resolve().parent.parent / "assets" / "readme"

STAGES = [
    ("Foundations", [("Course 1", "Python Foundations"), ("Course 2", "Bond Math"), ("Course 3", "Market Data")]),
    ("Machine learning", [("Course 4", "Machine Learning"), ("Course 5", "Advanced ML"),
                          ("Course 5B", "Time Series Models"), ("Course 6", "Neural Networks")]),
    ("Language models and agents", [("Course 7", "NLP, RAG, and LLMs"), ("Course 8", "Agentic AI")]),
    ("Build and ship", [("Course 9", "Deployment"), ("Course 10", "Implementing RAG"),
                        ("Bonus", "Your Own Coding Agent")]),
]

WIDTH = 1000
PAD = 30
CARD_W = 270
CARD_H = 140
CARD_GAP = (WIDTH - 2 * PAD - 3 * CARD_W) // 2
NARROW_GAP = 40  # a band of four cards (Course 5B joined Machine learning, 2026-10-20) uses narrower cards
BAND_H = 250
BAND_GAP = 70

THEMES = {
    "light": dict(band="#e8f3ec", band_line="#1c7a57", title="#123d2f", card="#123d2f", label="#7fd1a8",
                  name="#ffffff", arrow="#1c7a57"),
    "dark": dict(band="#11281f", band_line="#1c7a57", title="#eaf4ee", card="#1c7a57", label="#cdeedd",
                 name="#ffffff", arrow="#7fd1a8"),
}


def wrap(text: str, font, width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if font.getlength(trial) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def arrow(canvas: ImageDraw.ImageDraw, start: tuple, end: tuple, color: str) -> None:
    canvas.line((start, end), fill=color, width=5)
    (x0, y0), (x1, y1) = start, end
    if y0 == y1:  # right-pointing head
        canvas.polygon([(x1 + 4, y1), (x1 - 12, y1 - 11), (x1 - 12, y1 + 11)], fill=color)
    else:  # down-pointing head
        canvas.polygon([(x1, y1 + 4), (x1 - 13, y1 - 12), (x1 + 13, y1 - 12)], fill=color)


def draw(theme: dict) -> Image.Image:
    height = len(STAGES) * BAND_H + (len(STAGES) - 1) * BAND_GAP
    image = Image.new("RGBA", (WIDTH, height), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(image)
    title_font, label_font, name_font = sans(34, 600), mono(22, bold=True), sans(30, 500)

    for i, (stage, courses) in enumerate(STAGES):
        top = i * (BAND_H + BAND_GAP)
        canvas.rounded_rectangle((0, top, WIDTH - 1, top + BAND_H), radius=24, fill=theme["band"],
                                 outline=theme["band_line"], width=3)
        canvas.text((PAD, top + 58), stage, font=title_font, fill=theme["title"], anchor="ls")

        card_top = top + BAND_H - PAD - CARD_H
        card_w, gap = (CARD_W, CARD_GAP) if len(courses) <= 3 else             ((WIDTH - 2 * PAD - (len(courses) - 1) * NARROW_GAP) // len(courses), NARROW_GAP)
        for j, (label, name) in enumerate(courses):
            left = PAD + j * (card_w + gap)
            canvas.rounded_rectangle((left, card_top, left + card_w, card_top + CARD_H), radius=18,
                                     fill=theme["card"])
            canvas.text((left + 22, card_top + 42), label.upper(), font=label_font, fill=theme["label"],
                        anchor="ls")
            for k, line in enumerate(wrap(name, name_font, card_w - 44)):
                canvas.text((left + 22, card_top + 84 + k * 36), line, font=name_font, fill=theme["name"],
                            anchor="ls")
            if j:
                mid = card_top + CARD_H // 2
                arrow(canvas, (left - gap + 10, mid), (left - 10, mid), theme["arrow"])

        if i < len(STAGES) - 1:
            arrow(canvas, (WIDTH // 2, top + BAND_H + 10), (WIDTH // 2, top + BAND_H + BAND_GAP - 10),
                  theme["arrow"])
    return image


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        draw(theme).save(OUT / f"path-{name}.png", optimize=True)
