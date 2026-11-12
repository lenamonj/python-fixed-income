"""Redraw the route cell of built notebooks in place, from the notebook itself and its plan, with no rebuild.

Everything route_cell() needs is read back from the saved notebook: the sections and their minutes from the
trackers, the label from the route's heading, the figure number from its alt text, and the exercises from the
**Time.** line. The cell is then exactly what a rebuild would draw.

    python tools/workbook/redraw_routes.py --check <notebook.ipynb> ...   list titles that need a route_names label
    python tools/workbook/redraw_routes.py <notebook.ipynb> ...           redraw each route cell and save
"""
import re
import sys
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # tools/, for notebook_header and the prose helpers

from notebook_header import workbook_plan  # noqa: E402
from workbook import components as c  # noqa: E402
from workbook.apply import COUNT_WORDS, NUMBERED, Drawer, heading_of, route_cell  # noqa: E402

TRACKER = re.compile(r"^!\[Section (\d+) of (\d+)\. .*? About (\d+) minutes?\.\]\(")
TIME = re.compile(r"\*\*Time\.\*\* About (\d+) minutes for the lesson(?:, then about (\d+) for the (\w+) exercises\.)?")


def read_route(notebook: Path) -> dict:
    """What the route cell was drawn from, read back from the saved notebook."""
    nb = nbformat.read(notebook, as_version=4)
    cells = nb.cells
    at = next((i for i, cell in enumerate(cells) if cell.source.startswith("## Your Route Through ")), None)
    if at is None:
        raise LookupError(f"{notebook.name} has no route cell")
    source = cells[at].source
    label = re.match(r"## Your Route Through (.+)", source).group(1).strip()
    figure = int(re.search(r"!\[Figure (\d+): ", source).group(1))
    minutes, heads = [], []
    for i, cell in enumerate(cells):
        found = TRACKER.match(cell.source)
        if found:
            minutes.append(int(found.group(3)))
            heads.append(heading_of(cells[i + 1]))
    if not heads or len(heads) != int(TRACKER.match(cells[at + 1].source).group(2)):
        raise LookupError(f"{notebook.name}: the trackers do not match their count")
    stops = [tuple(head.split(" ", 1)) if re.match(NUMBERED[3:], head) else (str(k), head) for k, head in enumerate(heads, start=1)]
    time = TIME.search(source)
    if not time or int(time.group(1)) != sum(minutes):
        raise LookupError(f"{notebook.name}: the Time line does not match the trackers' {sum(minutes)} minutes")
    word = time.group(3)
    exercises = 0 if word is None else (COUNT_WORDS.index(word) if word in COUNT_WORDS else int(word))
    practice = int(time.group(2) or 0)
    return {"nb": nb, "at": at, "label": label, "figure": figure, "stops": stops, "minutes": minutes,
            "practice": practice, "exercises": exercises}


def titles_for(stops: list, plan: dict) -> list:
    short = {int(place): words for place, words in plan.get("route_names", {}).items()}
    return [short.get(k, re.sub(r"`", "", title)) for k, (number, title) in enumerate(stops, start=1)]


def main(args: list) -> None:
    check = args[:1] == ["--check"]
    notebooks = [Path(arg) for arg in (args[1:] if check else args)]
    if not notebooks:
        raise SystemExit(__doc__)
    if check:
        for notebook in notebooks:
            found = read_route(notebook)
            titles = titles_for(found["stops"], workbook_plan(notebook) or {})
            lines = c.route_lines(titles)
            misfits = c.route_misfits(titles) if not lines else []
            print(f"{notebook}: {len(titles)} sections, {lines or 'NO'} lines" + (f", misfits {misfits}" if misfits else ""))
        return
    failed = []
    with Drawer() as draw:
        for notebook in notebooks:
            plan = workbook_plan(notebook)
            if plan is None:
                raise LookupError(f"{notebook} has no plan in the workbook design system")
            found = read_route(notebook)
            nb = found["nb"]
            try:
                nb.cells[found["at"]].source = route_cell(draw, plan, found["stops"], found["minutes"], found["label"],
                                                          found["practice"], found["exercises"], found["figure"])
            except ValueError as error:  # PlanError, or the studio refusing words wider than their box
                failed.append(f"{notebook}: {error}")
                continue
            nbformat.write(nb, notebook)
            print(f"redrew {notebook}")
    if failed:
        raise SystemExit("not redrawn, give these a route_names label:\n" + "\n".join(failed))


if __name__ == "__main__":
    main(sys.argv[1:])
