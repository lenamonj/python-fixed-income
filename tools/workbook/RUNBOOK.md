# Converting a notebook: the runbook

How to put one built notebook into the workbook design system. `README.md` beside this file is the standard; this file is the job.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

A converted notebook has the cover, the route, a tracker above each section, every picture as a numbered figure, the exercises strip, and the card to the next notebook. You do not draw any of that and you do not edit the notebook's builder. You write one small plan, run the builder, and read what comes out.

## The job, in order

1. **Read the notebook from top to bottom**, then skim Day 0 (`course01_python_foundations/week1/day0/0_start_here.ipynb`) to see the standard.
2. **Redraw the notebook's pictures.** Run the day's picture script. It draws them in the house style at 2400 px. Open each PNG and look at it: the layout must be as it was, with no word cut off or running into a box.
3. **Write the plan**: `instructor/_build/workbook_plans/<course folder>/<notebook name>.json`. The solutions notebook shares it.
4. **Run the notebook's builder.** If it stops, the message says what to fix. See "What the messages mean".
5. **Run the check** and open the sheets it saves:

   ```powershell
   .venv\Scripts\python.exe tools\workbook\check.py <path to the notebook> --sheet <a folder>
   ```

   The last line must say `passed` with no `failed`. Then look at every picture on the sheets, in order.
6. **Stop there.** Do not commit, push, or start the next notebook. Report: the plan you wrote, the check's last line, and anything you were unsure of.

## The plan

Only `goals` is required. Everything else the tool reads from the notebook: title, week and day, sections, minutes, exercises, pictures, and the next notebook.

| Key | What it is | Who writes it |
| --- | --- | --- |
| `goals` | A list with one goal for each section, in order. | Anyone |
| `sections` | `"numbered"` (the default: `## 3.1 ...` headings, and any unnumbered `##` section among them) or `"h1"` (a notebook whose sections are `# Topic` headings). | Anyone |
| `exercises` | One short sentence for the strip above the exercises. Default: "Practice, with a worked answer for each." | Anyone |
| `captions` | `{"3": "A caption for figure 3."}`. A figure's caption is its picture's alt text unless you give one here. | Anyone |
| `next_line` | The sentence on the card to the next notebook. Default: what the closing cell says comes next, or the next notebook's purpose line. | Anyone |
| `route_line` | One sentence above the route. | Editor |
| `route_flags` | `{"3": "ANSWER 1 · THE COUPON"}`: a few words above a section's point on the route. | Editor |
| `note` | The scenario as a note with boxes that get ticked. | Editor |
| `mistakes` | Common-mistake plates. | Editor |
| `quick_checks` | Questions with a folded answer. | Editor |

A minimal plan:

```json
{
  "goals": [
    "Store a bond's facts under names.",
    "Show a number the way the desk reads it."
  ]
}
```

The editor's keys, in full:

```json
{
  "note": {
    "in": "^## The Morning Note",
    "sender": "Note from the desk lead",
    "title": "The morning note",
    "asks": [
      ["What a 5.25 percent coupon pays each half year", "2.625 percent of face", "half the note answered"],
      ["A picture of our three bonds", "the coupon chart", "^The note is answered"]
    ]
  },
  "mistakes": [
    {"in": "^7, not 25", "name": "A power typed the Excel way", "typed": "5 ^ 2", "got": "7",
     "why": "No error message: a wrong answer that looks like a right one.",
     "instead": "5 ** 2", "gives": "25", "how": "In Python, two stars make a power."}
  ],
  "quick_checks": [
    {"after": "^`coupon = 5.25` stores", "question": "Which order does the kernel remember?",
     "answer": "The order you ran them.\nAfter a Restart it remembers nothing."}
  ]
}
```

Each `in`, `after`, and third item of an ask is a pattern that must match exactly one cell. `note.in` is the scenario cell: its quoted line (`> ...`) becomes the note. Each ask's pattern is the cell where the notebook gives that answer.

## Writing a goal

A goal is what the section is for, said to the student. It is the only writing every notebook needs, so it has to be right.

- One sentence, a command, eight words or fewer, ending in a full stop.
- It says what the student will do or be able to do, in the notebook's own words.
- It uses no term the notebook has not taught by the end of that section.
- It does not repeat the section's title.

| Section | Good | Not this |
| --- | --- | --- |
| 0.3 Python as a Calculator | Do the desk's first sum. | Learn about arithmetic operators in Python. |
| 1.4 Data Structures | Hold a whole bond, then a portfolio. | Lists, tuples, and dictionaries. |
| 0.5 What a .py File Is | Make a Python file and run it. | Understand .py files. |

If the build says a goal does not fit, shorten the goal. Never touch the type size.

## Captions

A caption says what the figure shows, in one sentence. The default, the picture's alt text, is usually right. Give a caption in the plan only when the alt text is longer than about 120 characters or is not a sentence. Where the notebook's text says "the first picture" or "the picture above", that is the builder's text: report it, do not edit it.

## The editor's pieces

These take judgment about what the notebook has taught, so one editor writes them for a whole course and looks at the result in VS Code and JupyterLab.

- **Note.** Only for a notebook whose scenario asks for things the notebook then delivers. Each ask is ticked in the cell where the notebook itself says it is answered.
- **Mistake plate.** Only after a real cell in which the mistake happens and the student has seen the result.
- **Quick check.** One question on what the section just taught, nothing later. It must not give away the answer to a Predict.

## What you must not do

- Change a sentence or a code cell of the notebook. The design goes around the lesson, not into it.
- Style anything inside a cell: no `<img>`, no `style=`, no HTML for looks.
- Edit `design.css`, `components.py`, `apply.py`, or the house style to make something fit. Shorten the words.
- Restyle an output. A chart looks the way the student's own code makes it look.
- Copy Day 0's builder. Day 0 was drawn by hand before this tool existed; a plan is the way now.
- Convert a notebook's overview PDF. That is a separate job (`slides.py`), done by hand for now.

## What the messages mean

| The build says | Do this |
| --- | --- |
| `the plan gives N goals and the notebook has M sections: [...]` | Write one goal for each section it lists, in that order. |
| `... does not fit: "..." runs outside the picture` or `is wider than its box` | Shorten those words in the plan. For a picture script, shorten the label there. |
| `... reaches the foot of the picture` | The title and subtitle are too long for the cover. Report it; do not change the title. |
| `the pattern '...' matches 0 cells` or `2 cells` | Make the pattern longer or more exact until it matches one cell. |
| `the plan has keys this tool does not know` | Fix the spelling of the key. |
| `the notebook has no numbered section` | Give the plan `"sections": "h1"`. |
| `this notebook is already in the design system` | Run the notebook's builder, which starts from a fresh notebook. Do not run the header tool on a built file. |
| `... is N.5 px tall` | A picture's height is not a whole pixel. Report it; this is a fault in the tool, not in your plan. |
