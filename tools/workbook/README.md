# The workbook design system

What every notebook in Python for Fixed Income looks and feels like, and the code that draws it.

The reference is [Day 0: Start Here](../../course01_python_foundations/week1/day0/0_start_here.ipynb). When a rule here and that notebook disagree, the notebook is wrong: fix it.

> This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.

## The one rule

**Words are typed. Structure is drawn.**

Everything a student reads as a sentence is plain markdown: headings, questions, explanations, tables, labels. Everything that gives the page its identity and its bearings is a picture drawn by this folder: the cover, the route, the section trackers, the figures, the scenario's note, the mistake plates, the card to the next notebook.

The reason is the four places a notebook is read. VS Code and JupyterLab keep inline styles; GitHub strips them; Colab is its own case. An embedded picture and plain markdown are the only two things all four show the same way, in a light theme and a dark one. So the design never depends on CSS inside a cell, and a student who double-clicks a text cell sees words, not markup.

## Identity

| Token | Value | Used for |
| --- | --- | --- |
| Midnight navy | `#0E1B2E` | Covers, section trackers, the next-step card |
| Warm ivory | `#F7F3EA` | Figures: every diagram, screenshot, and route |
| Paper | `#FFFDF8` | Objects on the desk: the scenario's note, a mistake plate |
| Graphite | `#1B2430` | Text and outlines on ivory |
| Teal | `#17807F`, `#5CC8C2` on navy | The one accent: where you are, what moves |
| Brass | `#A97A1F` | The scenario and its answers |
| Rust | `#A4472F` | A mistake, and only a mistake |

| Typeface | Role |
| --- | --- |
| Newsreader | Titles, the scenario's words, a tracker's goal |
| IBM Plex Sans | Labels, captions, the words inside a diagram |
| IBM Plex Mono | Code, numbers, week and day plates, times |

All three are open-licensed and live in `assets/fonts` with their licenses. Corners are square and nothing casts a shadow: hairlines and flat colour only.

**The house curve.** One curve, rising fast and then flattening like a normal yield curve, is the mark of the series. It sits under the letters in the pfi badge, it carries a marker on the cover showing where the notebook falls in its course, and it carries the day's sections in the route. Draw it with `curve_path`; never draw another curve beside it.

## Anatomy of a workbook

A notebook is built in this order. "Drawn" parts come from `components.py`; "typed" parts are markdown in the builder.

| Part | Form | Rule |
| --- | --- | --- |
| Cover | Drawn: `cover` | First cell. Series, course, week and day, title, and the marker on the curve. The tall cover with the series line opens a course; every other notebook, and every solutions notebook, takes the compact one. |
| Title cell | Typed | `# Title`, the purpose line starting `Week W, Day D.`, the disclaimer, the Colab badge. |
| Scenario | Typed, with a drawn `note` | A desk situation that asks for something. The note lists what is asked as open boxes. |
| Route | Typed heading, drawn `route` in a `figure` | The chapter introduction: the sections in order, the minutes for each, and a flag at each point where the scenario gets an answer. One line of time under it. |
| Section opener | Drawn: `tracker`, in a cell of its own | Before each `## N.M` heading: which section of how many, its goal in one short sentence, about how many minutes. The goal is the section's learning objective. |
| Concept | Typed | Short lines, one sentence to a line. A term is bold where it is first named. |
| Question | Typed | A line starting `Q. `. |
| Code | A code cell | One idea to a cell, a comment on each step. |
| Reading the output | Typed | One or two lines under the output saying what it shows. |
| Hand-off | Typed | A bold sentence that closes a cell and leads to the next heading. |
| Figure | Drawn: `figure` | Every diagram and screenshot, numbered from 1 in the notebook, with its caption in the frame. The text refers to it as "Figure 2". |
| Common mistake | Drawn: `mistake` | After the student has met the mistake in a real cell: what was typed and what came back, beside what to type instead. |
| Excel side by side | Typed | The label `**Excel side by side.**`, then the comparison. Courses 1 to 3 only. |
| Story | Typed | A `> STORY:` block in a cell of its own, with its sources. |
| Knowledge check | Typed: `quick_check` | The label `**Quick check.**`, one question, and the answer folded under "Show the answer". It uses only what the section taught. |
| Scenario progress | Drawn: `note` as a strip | Where the scenario gets an answer: the box ticked, the answer beside it. |
| Summary | Typed | `## You Can Now`, the lead-in, and the list. |
| Exercises | Drawn `tracker`, then typed | `## Exercises`, `### Exercise N`, the last an AI check. |
| Closing | Typed, with drawn `note` and `next_step` | `## Congratulations!`, the note with every box ticked, then the card to the next notebook, which is a link. |

A numbered heading must start its cell, because the tests and the outline both find sections that way. That is why a tracker has a cell of its own above the heading.

## The drawn components

Each function in `components.py` returns the HTML of one component. `Studio.png` draws it at twice its display size and saves a PNG.

| Function | What it draws |
| --- | --- |
| `cover(course_line, plate, title, subtitle, statement, meta, progress, weeks, compact)` | The cover. `progress` runs from 0, the course's first notebook, to 1, its last. |
| `tracker(label, goal, minutes, index, count)` | The strip above a section, or above the exercises when `count` is left out. |
| `figure(body, number, caption)` | The ivory frame and its caption. The body is a `screenshot`, a `route`, or a diagram. |
| `screenshot(path, width)` | A screenshot for a figure's body. |
| `stage`, `box`, `words`, `arrows` | A diagram, placed by position: boxes, words, arrows. |
| `route(sections, flags, head, total)` | The day's sections on the house curve. |
| `note(sender, state, tasks, text)` | The scenario's note. Without `text` it is the short progress strip. |
| `mistake(name, typed, got, why, instead, gives, how)` | A common mistake as a plate. |
| `next_step(label, plate, title, line)` | The card to the next notebook. |

The typed helpers are in `cells.py`: `picture` and `linked_picture` embed a drawn component, `quick_check` writes a knowledge check, and `minutes` and `section_minutes` apply the time rule.

## The overview PDF

Each notebook's overview PDF is the same system at 16:9, built by `slides.py` and styled by `slides.css` on top of `design.css`.

| Function | What it makes |
| --- | --- |
| `front(course_line, plate, title, subtitle, statement, meta, progress, weeks)` | The first slide: the notebook's cover, with the disclaimer at its foot. |
| `bar(label, goal, mark, index, count)` | The strip at the top of a slide: the notebook's tracker for that section. |
| `slide(top, title, content, foot, number)` | A content slide. |
| `row`, `col`, `panel`, `codebox`, `grid`, `takeaway`, `statement`, `facts`, `shot`, `scaled`, `pushed`, `can_list` | What goes on a slide. |
| `Press.pdf(slides, out, title)` | Prints the slides to one PDF. `Press.previews` saves a PNG of each for looking at first. |

A slide's content is 1200 px wide, as a drawn component is, so `note`, `route`, `mistake`, `next_step`, and any diagram go on a slide as they stand, and `scaled` shrinks one that is too tall.

The PDF is printed from the browser, not exported from PowerPoint, which cannot draw the system's typefaces. The text stays text, the diagrams stay sharp at any size, and the typefaces travel inside the file.

1. One slide for each section, with the scenario and the route before them and You Can Now after: 12 to 14 slides.
2. Every code line, output, table, and sentence is read from the built notebook, never typed again. A pattern that no longer finds its cell stops the build.
3. A slide whose content does not fit is refused. Look at every slide's preview before printing.
4. The first slide carries the disclaimer.
5. Leave out anything that answers a Predict: its output, the picture drawn from it, the sentence after it.

## The time rule

Times on a cover, a route, and a tracker are estimates from one rule, so they mean the same thing in every notebook: 150 words a minute, half a minute for each code cell, half a minute for each figure, three minutes for each exercise. Section times are whole minutes; the cover's total is rounded to five. A builder checks its trackers against the rule and stops if they have drifted.

## Rules that keep it working everywhere

1. A drawn component is embedded as a markdown image, `![alt](data:image/png;base64,...)`. No `<img>` tag and no `style` attribute, ever.
2. Every component is 1200 px wide and drawn at 2400 px, so every picture spans the column and they all scale together.
3. Every component has an opaque background. Nothing relies on the colour of the page behind it.
4. Every picture has alt text that says what the picture says. A figure's alt text is `Figure N:` and its caption.
5. A component's height is a whole number of pixels. `Studio.png` refuses anything else, because a part pixel shows as a stray line.
6. Text inside a picture is short: a label, a caption, a goal. A sentence that teaches is typed.
7. Outputs are never restyled. A chart looks the way the student's own code will make it look; a house chart style arrives in the notebook that teaches styling, as code the student runs.
8. Colour carries one meaning each: teal is place, brass is the scenario, rust is a mistake.

## Putting a notebook into the system

No builder draws any of this itself. `notebook_header.apply_header`, which every builder already calls, hands a notebook to `apply.py` when the notebook has a plan, and `apply.py` reads the rest from the notebook: title, week and day, sections, minutes, exercises, pictures and their alt text, and the notebook that comes next.

| File | What it does |
| --- | --- |
| `apply.py` | Puts a built notebook into the system from its plan, on every rebuild. |
| `check.py` | Checks one converted notebook: its sections and minutes, its tests, and a sheet of every picture. |
| `RUNBOOK.md` | The job of converting one notebook, step by step, with every key of a plan. |

A plan is a small JSON file, `instructor/_build/workbook_plans/<course folder>/<notebook name>.json`. It holds what a person has to write: one goal for each section, and the optional pieces that take judgment (the scenario's note, mistake plates, quick checks).

The pictures a notebook already has are drawn by its own picture script in the house style, which carries this system's palette, typefaces, and 2400 px width; `apply.py` sets each one on the plate with its numbered caption. Every drawn component refuses words that do not fit, so a plan that is wrong stops the build with a sentence that says what to change.

Install the author tools once: `pip install -r requirements-dev.txt`, then `python -m playwright install chromium`.
