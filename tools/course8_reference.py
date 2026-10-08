"""The reference agentkit of Course 8, for the author's Course 8 data tools and tests.

The tools that make Course 8's data (tools/make_course8_evals.py, tools/make_course8_memo.py) compute every answer
key with the functions the notebooks teach (agentkit's tools over the committed files, Course 2's bondmath, Course 7's
textkit), so a key in data/ is exactly what a student's own tool returns. The reference module is assembled from the
private build folder (instructor/_build/course8), which only the author has; a student never runs these tools.
"""
import atexit
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ASSEMBLE = REPO / "instructor" / "_build" / "course8" / "assemble.py"


def available() -> bool:
    """Whether the private build folder that holds the reference agentkit is here."""
    return ASSEMBLE.is_file()


def agentkit():
    """Import the reference agentkit at the end of day 14 (with bondmath, marketdata, mlkit, and textkit)."""
    if "agentkit" in sys.modules:
        return sys.modules["agentkit"]
    if not available():
        raise SystemExit("this author tool needs the private build folder instructor/_build/course8")
    spec = importlib.util.spec_from_file_location("course8_assemble", ASSEMBLE)
    assemble = importlib.util.module_from_spec(spec)
    sys.modules["course8_assemble"] = assemble
    spec.loader.exec_module(assemble)
    folder = Path(tempfile.mkdtemp(prefix="pfi_course8_reference_"))
    atexit.register(shutil.rmtree, folder, True)
    assemble.write_day(14, folder)
    sys.path.insert(0, str(folder))
    import agentkit as module
    return module
