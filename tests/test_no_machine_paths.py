"""No saved notebook output shows a machine path or the author's Windows user name.

The repo is public. Each builder guards its own outputs; this test checks every notebook regardless.
IPython shortens the home folder to `~`, so a traceback frame such as `File ~\\projects\\...` is allowed.
"""
import re
from pathlib import Path

import nbformat
import pytest

REPO = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted(path for path in REPO.glob("course*/**/*.ipynb"))
# a Windows drive path, a Users folder on any system, or the user name (not the surname Lenamon,
# the GitHub handle lenamonj, or the word filename)
LEAK = re.compile(r"\b[A-Za-z]:\\\\?[A-Za-z]|[\\/]Users[\\/]|\blenam\b", re.I)
# paths a notebook shows on purpose: the Bonus agent's sandbox refusing a system file
TAUGHT = ["C:\\Windows\\win.ini"]


def output_text(output) -> str:
    parts = [output.get("text", "")] + output.get("traceback", [])
    data = output.get("data", {})
    for key in ("text/plain", "text/html", "text/markdown"):
        value = data.get(key, "")
        parts.append(value if isinstance(value, str) else "".join(value))
    return "\n".join(parts)


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda path: path.stem)
def test_no_machine_path_in_saved_outputs(path):
    leaks = []
    for index, cell in enumerate(nbformat.read(path, as_version=4).cells):
        for output in cell.get("outputs", []):
            text = output_text(output)
            for taught in TAUGHT:
                text = text.replace(taught, "")
            found = LEAK.search(text)
            if found:
                leaks.append((index, found.group(0)))
    assert leaks == []
