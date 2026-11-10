# Overview runbook: one notebook's overview PDF

The job of making one notebook's overview: the short deck, saved as a PDF beside the notebook, that introduces the day. The standard it has to meet is in [README.md](README.md) under "The overview PDF". The reference is Day 0's, `course01_python_foundations/week1/day0/0_start_here_overview.pdf`.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

An overview is not a summary of the notebook. It is what a student sees for a minute before opening the notebook: for each section, the one example that shows what the section teaches. You choose that example and lay it out. You do not write it: every code line, output, table, and sentence on a slide is read from the built notebook by a pattern, so the PDF cannot say what the notebook does not.

Your brief names three files: the notebook, the script to write, and a folder for previews. Run everything from the repo root with `.venv\Scripts\python.exe`. The notebook must already be in the design system.

## The job, in order

1. **Read the notebook from top to bottom**, as plain text, sent to a file and read in parts, all of it:

   ```powershell
   .venv\Scripts\python.exe tools\workbook\check.py <path to the notebook> --text > <your folder>\notebook.txt
   ```

   Never open the `.ipynb` file itself.
2. **Look at a finished deck**, so you know what a finished slide looks like: full, ordered, and easy to read. This prints the slides of Day 1, Part 1 into a folder of its own, with contact sheets, and writes no PDF. Open the sheets. Do not read or copy that script.

   ```powershell
   .venv\Scripts\python.exe instructor\_build\redesign_c1\day1\make_overview.py --preview <your folder>\reference --look
   ```
3. **Choose the slides.** The front, the scenario, the route, the sections, the closing: 9 to 16 slides. A section takes one slide. A section with two separate big ideas may take two, the second under a title of your own; never three.
4. **For each section, choose what goes on its slide**, enough to fill it: the section's figure if it has one, shown large; the one or two code cells that carry the section, with what they printed; its Excel comparison if it has one (Courses 1 to 3); and the bold line that closes it, as the takeaway. A good slide has a main part that takes most of the room and one or two smaller parts beside or under it.
5. **Write the script** from the skeleton below, a slide at a time.
6. **Run it with previews** and read what it prints:

   ```powershell
   .venv\Scripts\python.exe <your script> --preview <your folder>
   ```

   It saves a PNG of each slide and contact sheets of them (`sheet_1.png`, six slides to a sheet), and lists the slides by number. Open every sheet and look at every slide, after every run that changes one. Open a single slide's PNG when a sheet is too small to judge it. Look for: a code line cut off by its box, a picture too small to read, parts that do not line up, and a slide that looks top-heavy or thin.
7. **Run the test**: `.venv\Scripts\python.exe -m pytest tests/test_workbook_design.py -q -p no:cacheprovider -k "<notebook name> and overview"`. It must say `passed`, not `skipped`.
8. **Stop there.** Do not commit, push, or start another notebook. Report: the slides in order with what each shows, the script's last line, the test's last line, and anything you were unsure of.

## The skeleton

```python
"""Print <notebook>'s overview PDF. Run from the repo root: .venv\\Scripts\\python.exe <this file> [--preview <folder>]"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tools"))
from workbook import slides as s  # noqa: E402
from workbook.overview import Deck, inline, last_bold, line  # noqa: E402

deck = Deck(REPO / "course01_python_foundations" / "week1" / "day2" / "02_files_and_folders.ipynb")
deck.front()

deck.scenario(r"^## The Desk Lead's Fourth Note")   # the cell that holds the desk lead's quoted note
deck.route()

# 2.1: the figure large, the code that goes with it beside it, the section's closing line under both
where = r"^os\.getcwd\(\)"
deck.section("2.1",
             s.row(s.col(deck.figure(2, 760), width=760),
                   s.col(s.panel("Ask where Python is working", s.codebox(deck.lines(where), deck.output(where))))),
             s.takeaway(last_bold(deck.markdown(r"^The working directory is"))))

deck.closing()
sys.exit(deck.press())
```

## Reading the notebook

Every reader takes a pattern, a regular expression matched against each line of a cell. Make it long enough to match one cell: the first match is used. A reader that finds nothing stops the build and says which pattern.

| Reader | What it gives |
| --- | --- |
| `deck.lines(pattern, comments=False, keep="")` | A code cell's lines, for `s.codebox`. `keep` is a pattern for the lines to keep, when the cell is longer than the slide needs. |
| `deck.output(pattern, keep="", first=0)` | What that cell printed, as text. `first=6` keeps six lines; `keep` keeps the lines that match. |
| `deck.error(pattern)` | The last line of the error a cell raised, for `s.codebox(..., bad=True)`. A long one needs a wide column: it cannot be cut. |
| `deck.frame(pattern, rows=0, columns=0)` | The table a cell showed, for `s.grid`. `rows` and `columns` keep that many; the row labels count as the first column. |
| `deck.chart(pattern, width)` | The chart a cell drew, exactly as the notebook shows it. |
| `deck.figure(number, width)` | A figure from the notebook, on its plate with its caption. |
| `deck.markdown(pattern)` | A text cell's words, to take lines from. |
| `line(pattern, text)` | The whole line of that text that the pattern matches a part of. Wrap it in `inline(...)` to keep its `code` and **bold**. |
| `last_bold(text)` | The bold line that closes a cell: the usual takeaway. To find that cell, match words inside the line, not `^` and the stars. |
| `deck.excel(pattern)` | A cell's Excel side by side, without its bold lead-in, for a panel labelled "Excel side by side". |
| `deck.quote(pattern)` | A cell's quoted lines (the desk lead's note), for `s.statement`. |
| `deck.table(pattern)` | The table in a text cell, as rows: wrap it, `s.grid(deck.table(...))`. The pattern matches a sentence in the same cell as the table, not a row of it. |
| `deck.heading(number)` | A section's heading. A section's slide uses it unless you give `title=`. |
| `deck.sections` | The sections as the notebook's trackers count them: number, title, goal, minutes. An unnumbered section's number is its place, as text: `"6"`. |
| `deck.section(number, *parts, title="")` | A section's slide. `title=` names a section's second slide. |
| `deck.closing(*parts, card=True)` | The last slide: the You Can Now list, your parts if any (the closing cell's table of answers is a good one), and the card to the next notebook. |
| `deck.scenario(pattern, *parts)` | The scenario's slide, whole: the cell's heading, the desk lead's quoted note set large, your parts if any, and the day's facts. |

## Laying out a slide

A slide's content is 1200 px wide and 526 px tall, with 18 px between parts.

| Part | What it is |
| --- | --- |
| `s.row(part, part, ...)` | Parts side by side. |
| `s.col(part, ..., width=560)` | Parts one under another. A column with no width takes the room that is left. |
| `s.panel("Label", part, ...)` | A paper panel with a small label. A part that is words becomes a paragraph. |
| `s.codebox(lines, output="", bad=False, small=False)` | Code as typed, with what it showed under a rule. Leave the output out for code that shows nothing. |
| `s.grid(rows, kind="")` | A table; the first row is the header. `kind="tight"` is smaller, `kind="wide"` spans the slide. |
| `s.takeaway(html)` | The one line the slide leaves behind. At most one a slide, last. |
| `s.statement(words)` | A sentence set large, for the scenario. |
| `s.pushed(part)` | A part pushed to the foot of the slide. |

How much fits:

- A code line runs about 9.3 px a letter, so about 120 letters across the whole slide and about 55 in a half-width column. With `small=True`, about 7.8 px a letter. A line that is too long is cut off by its box, which the build does not catch: look for it on the sheets, and give that codebox more width.
- About nine lines of code and output fit beside a takeaway. Use `keep` and `first` to show the lines that matter, never a retyped line.
- A figure is the main part of its slide: 700 to 900 px wide beside a panel, or 1200 px with only a takeaway under it. The build refuses a figure under 680 px, because its words cannot be read.
- A slide must be full enough: the build refuses one whose parts take less than 60 percent of its height (`SPARSE`). Fill it with what the section has: show its figure or chart larger, add its second-best example as another panel, add its Excel comparison, or set two short code cells one under the other. Never fill a slide with words of your own, and never repeat something another slide shows.
- If the build says a slide is too tall, take a part off it or show a picture smaller. Do not use `small=True` to rescue a crowded slide: take something off.
- Parts in a row are as tall as the tallest, so put parts of like height side by side.
- A column must hold its longest line of code. A row that is "too wide" nearly always has a code line longer than its column: give that column more width, or show fewer lines with `keep`. Beside a 680 px figure a column has 502 px, about 50 letters of code.
- When you cut a cell with `keep`, cut its output the same way, so each line shown still has its answer under it, and keep a loop's `for` line with its body.

## Rules

1. The only words you type are a panel's label (a few words: "The code", "What it prints", "Excel side by side"), the title of a section's second slide, and patterns. Everything else is read from the notebook.
2. Never answer a Predict. Leave out the output of a cell that a `**Predict N**` asks about, the picture drawn from it, and the sentence after it.
3. Outputs are never restyled. A chart looks the way the notebook shows it.
4. A slide carries one idea. Three panels side by side is the most a slide holds.
5. Slides follow the notebook's order.
6. No em dashes or en dashes, and no emojis, in anything you type.

## What you must not do

- Change the notebook, its builder, its plan, or anything under `tools/` or `tests/`.
- Retype a code line, an output, a number, or a sentence that the notebook has.
- Copy Day 0's script: it was written before `Deck` existed and carries its own readers.
- Leave a slide that does not fit, or one with a line cut off.

## What the messages mean

| The script says | Do this |
| --- | --- |
| `no code cell matches ...`, `no markdown cell matches ...`, `no line matches ...` | The pattern finds nothing. Copy the words from the notebook's text and escape `( ) [ ] . * + ?` with a backslash. |
| `does not fit: slide N: X px too tall` | Take a part off slide N, or show its picture smaller. |
| `SPARSE: slide N (...) fills 46% of its height` | Slide N is too empty. Fill it from its section, as "How much fits" says. |
| `figure N at W px is too small to read` | Show that figure 680 px wide or wider, and make it the slide's main part. |
| `slide 1: the title and subtitle reach the foot` | The notebook's title is too long for the front slide. Report it; do not change the title. |
| `does not fit: slide N: ... X px too wide` | A row is wider than the slide: give its columns widths that add to 1200 less the gaps. |
| `NOT PRINTED: ...` | A slide does not fit, so no PDF was written. Fix the slides it names. |
| `... is not in the design system` | The notebook has not been converted. Stop and report it. |
