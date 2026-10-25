"""Markdown tables as left-aligned HTML tables.

GitHub's notebook viewer centres every markdown table, so a short table floats in the middle of the page with the text
around it on the left. An HTML table with align="left", followed by <br clear="left">, sits on the left there and in
VS Code and Colab (tested on GitHub 2026-10-25). notebook_header.apply_header runs left_tables() on every markdown
cell, so every builder gets it. Bold, italics, `code`, links, and escaped pipes inside the cells are kept.
"""
import html
import re

SEPARATOR = re.compile(r"\s*\|(\s*:?-+:?\s*\|)+\s*")


def _inline(cell: str) -> str:
    """Escape the cell text, then turn the markdown it uses into HTML."""
    out = []
    for part in re.split(r"(`[^`]+`)", cell.strip().replace("\\|", "|")):
        if len(part) > 1 and part.startswith("`") and part.endswith("`"):
            out.append("<code>" + html.escape(part[1:-1], quote=False) + "</code>")
            continue
        text = html.escape(part.replace("&#96;", "`"), quote=False)
        text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
        out.append(text)
    return "".join(out)


def _cells(line: str) -> list[str]:
    """A table row's cells, split on pipes that are not escaped."""
    return re.split(r"(?<!\\)\|", line.strip().removeprefix("|").removesuffix("|"))


def _table(lines: list[str]) -> str:
    aligns = []
    for spec in _cells(lines[1]):
        spec = spec.strip()
        aligns.append("center" if spec.startswith(":") and spec.endswith(":") else "right" if spec.endswith(":") else "left")
    rows = ["<tr>" + "".join(f'<th align="{a}">{_inline(c)}</th>' for c, a in zip(_cells(lines[0]), aligns)) + "</tr>"]
    for line in lines[2:]:
        rows.append("<tr>" + "".join(f'<td align="{a}">{_inline(c)}</td>' for c, a in zip(_cells(line), aligns)) + "</tr>")
    return '<table align="left">\n' + "\n".join(rows) + '\n</table>\n<br clear="left">'


def left_tables(text: str) -> str:
    """The text with every markdown table (a header line, an alignment line, then rows) as a left-aligned HTML table."""
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        if not (lines[i].lstrip().startswith("|") and i + 1 < len(lines) and SEPARATOR.fullmatch(lines[i + 1])):
            out.append(lines[i])
            i += 1
            continue
        block = []
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            block.append(lines[i])
            i += 1
        out.append(_table(block))
        if i < len(lines) and lines[i].strip():
            out.append("")  # an HTML block ends at a blank line, so the markdown after it still renders
    return "\n".join(out)
