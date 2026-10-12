"""The reference ragkit of Course 10, for the author's Course 10 data tools and tests.

The tools that make Course 10's derived data (tools/make_course10_embeddings.py) and the data tests chunk and embed
with the functions the notebooks teach, so a file in data/ is exactly what a student's own functions make of the
documents. The reference module is assembled from the private build folder (instructor/_build/course10), which only
the author has; a student never runs these tools.
"""
import atexit
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ASSEMBLE = REPO / "instructor" / "_build" / "course10" / "assemble.py"


def available() -> bool:
    """Whether the private build folder that holds the reference ragkit is here."""
    return ASSEMBLE.is_file()


def ragkit(day: int = 14):
    """Import the reference ragkit at the end of `day` (with the earlier modules it needs)."""
    if "ragkit" in sys.modules:
        return sys.modules["ragkit"]
    if not available():
        raise SystemExit("this author tool needs the private build folder instructor/_build/course10")
    spec = importlib.util.spec_from_file_location("course10_assemble", ASSEMBLE)
    assemble = importlib.util.module_from_spec(spec)
    sys.modules["course10_assemble"] = assemble
    spec.loader.exec_module(assemble)
    last = max(d for d in range(1, day + 1) if (assemble.FRAGMENTS / f"day{d:02d}_ragkit.py").exists())
    folder = Path(tempfile.mkdtemp(prefix="pfi_course10_reference_"))
    atexit.register(shutil.rmtree, folder, True)
    assemble.write_day(last, folder)
    sys.path.insert(0, str(folder))
    import ragkit as module
    return module
