"""Check one converted notebook: what it now says about itself, its tests, and every drawn picture on one sheet.

    python tools/workbook/check.py course01_python_foundations/week1/day1/01_python_for_fixed_income_intro.ipynb --sheet <folder>

It prints the sections with their goals and minutes, runs the design and standard tests for this notebook and its
solutions, and saves both notebooks' pictures, in order, as sheets to look at. The exit code is 0 only when the
notebook is in the design system and its tests pass. Looking at the sheets is still a person's or a reviewer's job.

Two helpers for the work before the check, neither of which needs a converted notebook:

    python tools/workbook/check.py <notebook> --text
        the notebook as plain text, to read: its file is mostly pictures, so never open the file itself
    python tools/workbook/check.py --compare <pictures folder> --sheet <folder>
        each picture of the folder as it was at the last commit, beside as it is now
"""
import argparse
import base64
import io
import re
import subprocess
import sys
from pathlib import Path

import nbformat
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
PICTURE = re.compile(r"!\[((?:[^\[\]]|\[[^\]]*\])*)\]\(data:image/\w+;base64,([^)]+)\)")
SHEET_WIDTH, SHEET_HEIGHT, GAP = 1200, 2400, 24  # a sheet is short enough to be read in one look


def pictures(notebook: Path) -> list:
    """Every embedded picture of the notebook, in order, as (alt text, image)."""
    found = []
    for cell in nbformat.read(notebook, as_version=4).cells:
        if cell.cell_type == "markdown":
            for alt, encoded in PICTURE.findall(cell.source):
                found.append((alt, Image.open(io.BytesIO(base64.b64decode(encoded))).convert("RGB")))
    return found


def save_sheets(found: list, folder: Path, stem: str) -> list:
    """The pictures stacked at half size on white, cut into sheets short enough to look at."""
    folder.mkdir(parents=True, exist_ok=True)
    small = [image.resize((SHEET_WIDTH, round(image.height * SHEET_WIDTH / image.width)), Image.LANCZOS) for alt, image in found]
    sheets, batch, height = [], [], GAP
    for image in small + [None]:
        if image is None or (batch and height + image.height + GAP > SHEET_HEIGHT):
            sheet = Image.new("RGB", (SHEET_WIDTH + 2 * GAP, height), "#FFFFFF")
            y = GAP
            for part in batch:
                sheet.paste(part, (GAP, y))
                y += part.height + GAP
            path = folder / f"{stem}_sheet{len(sheets) + 1}.png"
            sheet.save(path)
            sheets.append(path)
            batch, height = [], GAP
        if image is not None:
            batch.append(image)
            height += image.height + GAP
    return sheets


def as_text(notebook: Path) -> str:
    """The notebook as plain text: each cell numbered, each picture as its alt text, each output cut short."""
    lines = []
    for i, cell in enumerate(nbformat.read(notebook, as_version=4).cells):
        source = PICTURE.sub(lambda found: f"[picture: {found.group(1)}]", cell.source)
        if cell.cell_type == "markdown":
            # an HTML table as rows of words
            source = re.sub(r"</t[dh]>\s*<t[dh][^>]*>", " | ", source)
            source = re.sub(r"</tr>\s*", "\n", source)
            source = re.sub(r"</?(?:table|tr|t[dh]|br)[^>]*>", "", source)
        tags = f" {cell.metadata['tags']}" if cell.metadata.get("tags") else ""
        lines += [f"--- cell {i}, {cell.cell_type}{tags}", source.strip()]
        for output in cell.get("outputs", []):
            data = output.get("data", {})
            words = output.get("text") or data.get("text/plain") or "\n".join(output.get("traceback", []))
            words = re.sub(r"\x1b\[[0-9;]*m", "", "".join(words) if isinstance(words, list) else words).strip()
            kind = ": a chart" if "image/png" in data else ": a table" if "text/html" in data else ""
            lines.append(f"[output{kind}] {words[:400]}{' ...' if len(words) > 400 else ''}")
    return "\n".join(lines)


def compare_sheets(folder: Path, out: Path) -> list:
    """Each picture of a folder as it was at the last commit, left, beside as it is now, right, on sheets to look at."""
    folder = folder.resolve()
    root = Path(subprocess.run(["git", "-C", str(folder), "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True, check=True).stdout.strip())
    half = (SHEET_WIDTH - GAP) // 2
    rows = []
    for path in sorted(folder.glob("*.png")):
        was = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{path.relative_to(root).as_posix()}"], capture_output=True)
        pair = [Image.open(io.BytesIO(was.stdout)).convert("RGB") if was.returncode == 0 else None, Image.open(path).convert("RGB")]
        pair = [image and image.resize((half, round(image.height * half / image.width)), Image.LANCZOS) for image in pair]
        row = Image.new("RGB", (SHEET_WIDTH, max(image.height for image in pair if image) + 22), "#FFFFFF")
        note = "" if pair[0] else " (no earlier picture)"
        ImageDraw.Draw(row).text((0, 4), f"{path.name}: as it was, left{note}; as it is now, right", fill="#000000")
        for x, image in zip((0, half + GAP), pair):
            if image:
                row.paste(image, (x, 22))
        rows.append((path.name, row))
    return save_sheets(rows, out, "compare")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check one notebook converted to the workbook design system.")
    parser.add_argument("notebook", type=Path, nargs="?")
    parser.add_argument("--sheet", type=Path, help="a folder for the sheets of the notebook's pictures")
    parser.add_argument("--text", action="store_true", help="print the notebook as plain text and stop")
    parser.add_argument("--compare", type=Path, help="a folder of pictures: save each as it was beside as it is now")
    args = parser.parse_args()
    if args.compare:
        for path in compare_sheets(args.compare, args.sheet or Path(".")):
            print("sheet:", path)
        return 0
    notebook = args.notebook.resolve()
    if args.text:
        sys.stdout.reconfigure(encoding="utf-8")
        print(as_text(notebook))
        return 0
    if notebook.stem.endswith("_solutions"):
        print(f"{notebook.name} is a solutions notebook: check its teaching notebook, and the one run covers both.")
        return 1
    found = pictures(notebook)
    trackers = [alt for alt, image in found if alt.startswith("Section ")]
    if not trackers:
        print(f"{notebook.name} is not in the design system: it has no section trackers. Give it a plan and run its builder.")
        return 1
    solutions = notebook.with_name(notebook.stem + "_solutions.ipynb")
    answers = pictures(solutions) if solutions.exists() else []
    narrow = [alt[:60] for alt, image in found + answers if image.width != 2400]
    figures = sum(1 for alt, image in found if alt.startswith("Figure "))
    print(f"{notebook.name}: {len(trackers)} sections, {figures} figures, {len(found)} pictures, {notebook.stat().st_size / 1024:.0f} KB")
    for alt in trackers:
        print("  ", alt)
    if narrow:
        print("NOT 2400 px wide:", narrow)
    if args.sheet:
        for path in save_sheets(found, args.sheet, notebook.stem) + (save_sheets(answers, args.sheet, solutions.stem) if answers else []):
            print("sheet:", path)
    tests = subprocess.run([sys.executable, "-m", "pytest", "tests/test_workbook_design.py", "tests/test_notebook_standard.py",
                            "-q", "-p", "no:cacheprovider", "-k", notebook.stem], cwd=REPO, capture_output=True, text=True)
    print(tests.stdout.strip().splitlines()[-1] if tests.stdout.strip() else tests.stderr.strip())
    if tests.returncode != 0:
        print(tests.stdout[-3000:])
    return 1 if tests.returncode != 0 or narrow else 0


if __name__ == "__main__":
    raise SystemExit(main())
