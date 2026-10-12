"""Checks on the Bonus course's app (course_bonus_coding_agent/deploy/): offline, no key, no network.

Run with: python -m pytest

- deploy/ holds exactly app.py, requirements.txt, README.md: ASCII, LF, the Space's YAML with every version in
  quotes and no emoji key, no gradio in requirements.txt, the @spaces.GPU placeholder, the disclaimer, no key-like
  string, and no code-running name in the agent.
- The sync: app.py is the placeholder, the module's text, and the tail; the module's text, saved as coding_agent.py,
  writes these three files again byte for byte through its own space_files. Once the teaching notebook exists, its
  %%writefile cells of coding_agent.py are that same text.
- The fence on paths outside the workspace, with the Windows cases the foundation probed (a junction, a drive-relative
  path, an alternate data stream, a reserved name); the three tools; the loop on scripted responses through the real
  openai client; the refusal of a request for a view with no request sent; the chat handler; the page served once on
  127.0.0.1 and closed.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import httpx2
import nbformat
import pytest
import yaml
from openai import OpenAI

os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"

REPO = Path(__file__).resolve().parent.parent
COURSE = REPO / "course_bonus_coding_agent"
DEPLOY = COURSE / "deploy"
NOTEBOOK = COURSE / "week1" / "day1" / "01_build_your_own_coding_agent.ipynb"
KEY_LIKE = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}|\bhf_[A-Za-z0-9]{16,}|Bearer\s+[A-Za-z0-9._-]{12,}")
DISCLAIMER = ("This course is educational content created in a personal capacity. Nothing here is investment advice or "
              "a recommendation to buy or sell any security. All portfolio data is synthetic.")
REFUSAL = "REFUSED: this course asks only what the document says"


@pytest.fixture()
def app(tmp_path, monkeypatch):
    """deploy/app.py imported fresh, with its workspace in a temporary folder."""
    monkeypatch.setenv("AGENT_WORKSPACE", str(tmp_path / "workspace"))
    # importing app.py must not write __pycache__ into deploy/, which holds exactly the Space's three files
    monkeypatch.setattr(sys, "dont_write_bytecode", True)
    spec = importlib.util.spec_from_file_location("bonus_app", DEPLOY / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    yield module
    sys.modules.pop("bonus_app", None)


def module_text(app_module) -> str:
    text = (DEPLOY / "app.py").read_text(encoding="utf-8")
    assert text.startswith(app_module.SPACE_PLACEHOLDER) and text.endswith(app_module.APP_TAIL)
    return text[len(app_module.SPACE_PLACEHOLDER):-len(app_module.APP_TAIL)]


def run(app_module, name, **arguments) -> str:
    return app_module.execute_tool(name, json.dumps(arguments))


def test_deploy_holds_exactly_three_ascii_files():
    assert {p.name for p in DEPLOY.iterdir()} == {"app.py", "requirements.txt", "README.md"}
    for path in DEPLOY.iterdir():
        raw = path.read_bytes()
        assert raw.isascii() and b"\r\n" not in raw and not KEY_LIKE.search(raw.decode("ascii")), path.name


def test_space_readme_and_requirements():
    readme = (DEPLOY / "README.md").read_text(encoding="ascii")
    header = yaml.safe_load(readme.split("---\n")[1])
    assert header["sdk"] == "gradio" and header["app_file"] == "app.py" and "emoji" not in header
    assert header["sdk_version"] == "6.30.0" and header["python_version"] == "3.12.12"
    assert re.search(r'^sdk_version: "6\.30\.0"$', readme, re.M) and re.search(r'^python_version: "3\.12\.12"$', readme,
                                                                               re.M)
    assert DISCLAIMER in readme and "fictional" in readme
    assert (DEPLOY / "requirements.txt").read_text(encoding="ascii") == "openai==3.26.0\n"
    app_text = (DEPLOY / "app.py").read_text(encoding="ascii")
    assert "@spaces.GPU" in app_text and app_text.startswith("try:\n    import spaces\n")


def test_no_tool_runs_code(app):
    text = module_text(app)
    for name in ("subprocess", "os.system", "exec(", "eval(", "importlib", "__import__"):
        assert name not in text, name
    assert [tool["name"] for tool in app.TOOLS] == list(app.TOOL_FUNCTIONS) == ["read_file", "list_files", "edit_file"]
    assert app.REFUSAL_LINE == REFUSAL


def test_the_module_writes_deploy_again(app, tmp_path):
    (tmp_path / "coding_agent.py").write_text(module_text(app), encoding="utf-8", newline="\n")
    script = "import sys, coding_agent\ncoding_agent.space_files(sys.argv[1], 'Desk Coder', '6.30.0')"
    result = subprocess.run([sys.executable, "-c", script, str(tmp_path / "out")], cwd=tmp_path, capture_output=True,
                            text=True, env=os.environ | {"AGENT_WORKSPACE": str(tmp_path / "ws")})
    assert result.returncode == 0, result.stderr
    for name in ("app.py", "requirements.txt", "README.md"):
        assert (tmp_path / "out" / name).read_bytes() == (DEPLOY / name).read_bytes(), name


def test_the_notebook_teaches_the_same_module(app):
    if not NOTEBOOK.exists():
        pytest.skip("the teaching notebook is built at checkpoint 1")
    text = ""
    for cell in nbformat.read(NOTEBOOK, as_version=4).cells:
        first, _, body = cell.source.partition("\n")
        # the exercises' cells append the student's own code under a "# Exercise N" line: not the module's text
        if (cell.cell_type == "code" and first.startswith("%%writefile") and first.split()[-1] == "coding_agent.py"
                and not body.strip("\n").startswith("# Exercise")):
            text = (text + "\n\n" if " -a " in first else "") + body.strip("\n") + "\n"
    # the notebook grows by checkpoint (BONUS_SPEC.md, "The pilot"): until checkpoint 3 it teaches the module's first
    # steps, so its text must be the start of the module, ending where a step ends
    if text != module_text(app):
        assert module_text(app).startswith(text) and module_text(app)[len(text):].startswith("\n\n"), "not a prefix"
        pytest.skip("the notebook teaches the module through a checkpoint; the whole module from checkpoint 3")


@pytest.mark.parametrize("path", ["../secrets.txt", "a/../../x", "/etc/passwd", "/proc/self/environ", "../app.py",
                                  "C:\\Windows\\win.ini", "\\\\localhost\\c$\\Windows\\win.ini",
                                  "../workspace_old/secret.txt"])
def test_paths_outside_the_workspace_are_refused(app, path):
    if path[:2] in ("C:", "\\\\") and os.name != "nt":
        pytest.skip("a drive-letter or UNC path is absolute only on Windows")
    (app.WORKSPACE.parent / "workspace_old").mkdir(exist_ok=True)
    for tool, extra in [("read_file", {}), ("list_files", {}), ("edit_file", {"old_str": "", "new_str": "x"})]:
        result = run(app, tool, path=path, **extra)
        assert result.startswith("ERROR") and "outside the workspace" in result


@pytest.mark.skipif(os.name != "nt", reason="junctions, drive-relative paths, and alternate streams are Windows'")
def test_windows_cases_stay_inside(app):
    outside = app.WORKSPACE.parent / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("outside the fence\n", encoding="utf-8")
    made = subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(app.WORKSPACE / "jump"), str(outside)],
                          capture_output=True, text=True)
    assert made.returncode == 0, made.stdout
    assert "outside the workspace" in run(app, "read_file", path="jump/secret.txt")
    assert "outside the workspace" in run(app, "edit_file", path="jump/new.txt", old_str="", new_str="x")
    assert json.loads(app.list_files(".")) == ["README.txt", "bonds.csv", "desk_riddle.txt"]
    # a drive-relative path on the workspace's drive joins inside it
    assert run(app, "edit_file", path="C:planted.txt", old_str="", new_str="x").startswith("Created")
    assert (app.WORKSPACE / "planted.txt").is_file()
    # an alternate data stream stays on its file, inside the workspace
    assert run(app, "edit_file", path="bonds.csv:x", old_str="", new_str="hidden").startswith("Created")
    assert app.read_file("bonds.csv").startswith("bond_id,issuer")
    assert sorted(p.name for p in outside.iterdir()) == ["secret.txt"]


def test_symlink_escape_is_refused(app):
    try:
        (app.WORKSPACE / "sneaky").symlink_to(Path(app.WORKSPACE).anchor, target_is_directory=True)
    except OSError:
        pytest.skip("making a symlink needs a privilege this machine does not grant")
    assert "outside the workspace" in run(app, "list_files", path="sneaky")


def test_the_three_tools(app):
    assert json.loads(app.list_files(".")) == ["README.txt", "bonds.csv", "desk_riddle.txt"]
    assert "fictional" in app.read_file("README.txt") and "buy" not in app.read_file("desk_riddle.txt")
    assert run(app, "edit_file", path="t.py", old_str="", new_str="a = 1\nb = 1\n").startswith("Created")
    assert "appears 2 times" in run(app, "edit_file", path="t.py", old_str=" = 1", new_str=" = 2")
    assert run(app, "edit_file", path="t.py", old_str="b = 1", new_str="b = 2") == "Edited t.py."
    assert "no tool named" in app.execute_tool("run_python", "{}")
    assert "bad arguments" in app.execute_tool("read_file", "{not json")


def reply(output: list) -> dict:
    return {"id": "resp_test", "object": "response", "created_at": 1, "status": "completed", "model": "test-model",
            "output": output, "parallel_tool_calls": False, "tool_choice": "auto", "tools": [], "error": None,
            "incomplete_details": None, "instructions": None, "metadata": {}, "temperature": 1.0, "top_p": 1.0,
            "usage": {"input_tokens": 100, "input_tokens_details": {"cached_tokens": 0}, "output_tokens": 20,
                      "output_tokens_details": {"reasoning_tokens": 0}, "total_tokens": 120}}


SCRIPT = [
    reply([{"type": "reasoning", "id": "rs_1", "summary": [], "encrypted_content": "opaque"},
           {"type": "function_call", "id": "fc_1", "call_id": "call_1", "name": "read_file",
            "arguments": json.dumps({"path": "desk_riddle.txt"}), "status": "completed"}]),
    reply([{"type": "message", "id": "msg_1", "role": "assistant", "status": "completed",
            "content": [{"type": "output_text", "text": "A zero-coupon bond.", "annotations": []}]}]),
]


@pytest.fixture()
def scripted():
    sent = []

    def handler(request):
        sent.append(json.loads(request.content))
        return httpx2.Response(200, json=SCRIPT[(len(sent) - 1) % len(SCRIPT)])

    client = OpenAI(api_key="test-key", base_url="https://api.openai.com/v1", max_retries=0,
                    http_client=httpx2.Client(transport=httpx2.MockTransport(handler)))
    client.sent = sent
    return client


def test_the_loop_on_scripted_responses(app, scripted):
    conversation = []
    events = list(app.run_agent_turn(scripted, conversation, "Solve the riddle in desk_riddle.txt"))
    assert [e["type"] for e in events] == ["tool_call", "tool_result", "text"]
    assert events[-1]["text"] == "A zero-coupon bond."
    first, second = scripted.sent
    assert first["store"] is False and first["parallel_tool_calls"] is False
    assert first["prompt_cache_key"] == "bonus-coding-agent" and "seed" not in first
    # the reasoning item goes back whole, then the tool request, then its result
    assert [item.get("type", "user") for item in second["input"]] == ["user", "reasoning", "function_call",
                                                                      "function_call_output"]
    assert second["input"][1]["encrypted_content"] == "opaque"


def test_a_request_for_a_view_sends_nothing(app, scripted):
    for text in ("Which bond in bonds.csv should I buy?", "Rank these issuers as investments.",
                 "Where will B004's price be next month?"):
        assert list(app.run_agent_turn(scripted, [], text)) == [{"type": "text", "text": REFUSAL}]
    assert scripted.sent == []


def test_round_limit_and_rollback(app):
    def looping(**settings):
        item = SimpleNamespace(type="function_call", name="list_files", arguments='{"path": "."}', call_id="c1")
        return SimpleNamespace(output=[item], output_text="")

    events = list(app.run_agent_turn(SimpleNamespace(responses=SimpleNamespace(create=looping)), [], "loop"))
    assert sum(e["type"] == "tool_call" for e in events) == app.MAX_TOOL_ROUNDS and "stopped after" in events[-1]["text"]

    def broken(**settings):
        raise RuntimeError("network down")

    conversation = [{"role": "user", "content": "earlier"}]
    with pytest.raises(RuntimeError):
        list(app.run_agent_turn(SimpleNamespace(responses=SimpleNamespace(create=broken)), conversation, "hello"))
    assert conversation == [{"role": "user", "content": "earlier"}]


def test_the_chat_handler(app, scripted, monkeypatch):
    *_, (box, history, conversation) = app.respond("Solve the riddle in desk_riddle.txt", [], [], client=scripted)
    assert box == "" and [(m.metadata or {}).get("title") for m in history] == [None, "Tool: read_file", None]
    assert history[1].metadata["status"] == "done" and len(conversation) == 5
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    *_, (box, history, conversation) = app.respond("hello", [], [])
    assert history[-1].metadata["title"] == "Something went wrong" and conversation == []


def test_the_page_is_served(app):
    import urllib.request

    app.demo.launch(prevent_thread_lock=True, inline=False, inbrowser=False, quiet=True, server_name="127.0.0.1")
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        assert opener.open(app.demo.local_url, timeout=30).status == 200
    finally:
        app.demo.close()
