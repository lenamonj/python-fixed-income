"""The reference textkit of Course 7, for the author's Course 7 data tools.

The tools that make Course 7's data (tools/get_indentures.py, get_edgar_filings.py, get_8k_items.py,
make_glove_subset.py, make_8k_model_outputs.py) use the same textkit functions the notebooks teach, so a file in
data/ is exactly what a student's own function makes of its source. The reference module is assembled from the
private build folder (instructor/_build/course7), which only the author has; a student never runs these tools.

Also loads the repo-root .env into the process environment (python-dotenv; values are never printed) and reads the
SEC contact for EDGAR's User-Agent from PFI_SEC_CONTACT.
"""
import atexit
import importlib.util
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ASSEMBLE = REPO / "instructor" / "_build" / "course7" / "assemble.py"


def textkit():
    """Import the reference textkit at the end of day 14 (with Course 4's mlkit and Course 3's marketdata)."""
    if "textkit" in sys.modules:
        return sys.modules["textkit"]
    if not ASSEMBLE.is_file():
        raise SystemExit("this author tool needs the private build folder instructor/_build/course7")
    spec = importlib.util.spec_from_file_location("course7_assemble", ASSEMBLE)
    assemble = importlib.util.module_from_spec(spec)
    sys.modules["course7_assemble"] = assemble
    spec.loader.exec_module(assemble)
    folder = Path(tempfile.mkdtemp(prefix="pfi_course7_reference_"))
    atexit.register(shutil.rmtree, folder, True)
    assemble.write_day(14, folder)
    sys.path.insert(0, str(folder))
    import textkit as module
    return module


def sec_contact() -> tuple[str, str]:
    """(name, email) for the SEC's User-Agent, from PFI_SEC_CONTACT ("Name email@domain"), after loading the
    repo-root .env. The value is never printed or written anywhere."""
    from dotenv import load_dotenv
    load_dotenv(REPO / ".env", override=False)
    contact = os.environ.get("PFI_SEC_CONTACT", "").strip()
    if not contact or " " not in contact:
        raise SystemExit("PFI_SEC_CONTACT is not set: add a line PFI_SEC_CONTACT=<name> <email> to the repo .env "
                         "(the SEC asks every automated request to declare a contact)")
    name, email = contact.rsplit(" ", 1)
    return name, email
