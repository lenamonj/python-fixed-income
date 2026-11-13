"""Notebook prose as short lines: no bullets on running text, and one sentence to a paragraph.

A bullet wrapping several sentences is hard for a student to follow. notebook_header.apply_header runs plain_prose() on
every markdown cell, so every builder gets it. A bullet stays only on a real list: two or more items under a lead-in
that ends in a colon or is a bold label, or items that are fragments and not sentences. Headings, tables, HTML, quoted
stories, numbered steps, code fences, and Q. lines are left alone.
"""
import re

DISCLAIMER = "educational content created in a personal capacity"
ABBREVIATIONS = {"e.g", "i.e", "vs", "cf", "al", "approx", "Mr", "Mrs", "Ms", "Dr", "St", "Inc", "Corp", "Co", "Ltd",
                 "U.S", "J.P", "Fig", "Eq", "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Sept", "Oct", "Nov", "Dec"}
BOUNDARY = re.compile(r"[.?!][\"')]?\s+(?=[A-Z0-9\"'`$(*\[])")
# code, bold, links, and quotes are masked first: a period inside one of them does not end a sentence
MASK = re.compile(r"`[^`]*`|\*\*.+?\*\*|\[[^\]]*\]\([^)]*\)|\"[^\"]*\"|(?<!\w)'[^']*'(?!\w)")
BULLET = re.compile(r"[*-] ")
NUMBERED = re.compile(r"\d+[.)] ")
LABEL = re.compile(r"\*\*[^*]+\*\*")
NOT_PROSE = ("#", "|", "<", ">", "![", "[!", "$$", "Q.", "---")


def sentences(line: str) -> list[str]:
    """Split a line of prose into its sentences."""
    masked = MASK.sub(lambda match: "X" * len(match.group()), line)
    out, start = [], 0
    for match in BOUNDARY.finditer(masked):
        words = masked[:match.start()].split()
        word = words[-1].lstrip("(\"'") if words else ""
        if masked[match.start()] == "." and (word in ABBREVIATIONS or (len(word) == 1 and word.isupper())
                                             or (word in ("No", "p") and masked[match.end()].isdigit())):
            continue
        out.append(line[start:match.end()].rstrip())
        start = match.end()
    out.append(line[start:])
    return out


def is_real_list(items: list[str], lead_in: str) -> bool:
    """Two or more related items: fragments, or items introduced by a colon or a bold label."""
    if len(items) < 2:
        return False
    fragments = all(not item.rstrip().rstrip("*").endswith((".", "?", "!", ":")) for item in items)
    return fragments or lead_in.endswith(":") or bool(LABEL.fullmatch(lead_in))


def plain_prose(text: str) -> str:
    """The cell's text with running bullets removed and each sentence in a paragraph of its own."""
    if DISCLAIMER in text:
        return text
    lines = text.split("\n")
    out: list[str] = []

    def paragraphs(items: list[str]) -> None:
        for item in items:
            if out and out[-1]:
                out.append("")
            out.append(item)

    i = 0
    fenced = False
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if fenced or line.lstrip().startswith("```"):
            out.append(line)
            i += 1
        elif BULLET.match(line):
            run = []
            while i < len(lines) and (BULLET.match(lines[i]) or lines[i].startswith((" ", "\t")) and lines[i].strip()):
                run.append(lines[i])
                i += 1
            lead_in = next((previous for previous in reversed(out) if previous.strip()), "")
            if any(item.startswith((" ", "\t")) for item in run) or is_real_list(run, lead_in):
                out.extend(run)
            else:
                paragraphs([sentence for item in run for sentence in sentences(item[2:].strip())])
                if i < len(lines) and lines[i].strip():
                    out.append("")
        elif line.strip() and not line.startswith((" ", "\t", *NOT_PROSE)) and not NUMBERED.match(line):
            split = sentences(line)
            if len(split) > 1:
                paragraphs(split)
                if i + 1 < len(lines) and lines[i + 1].strip():
                    out.append("")
            else:
                out.append(line)
            i += 1
        else:
            out.append(line)
            i += 1
    return "\n".join(out)
