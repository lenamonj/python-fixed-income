try:
    import spaces

    @spaces.GPU(duration=1)
    def _zerogpu_placeholder():
        return None

except ImportError:
    pass

"""coding_agent: a small coding agent for a fixed income desk. One model, one loop, three tools, one fenced folder.

Written in Python for Fixed Income, the Bonus course: Build Your Own Coding Agent. The idea comes from Thorsten Ball,
"How to Build an Agent" (ampcode.com/notes/how-to-build-an-agent, April 15, 2025), which builds the same three tools
in Go; every line here is the course's own, in Python, on OpenAI's Responses API.

Conventions, the same in every function:
- The model returns text and tool requests, nothing else. Your code runs each tool, on your machine, and only inside
  WORKSPACE. No tool runs code, a shell, or an import.
- Every tool returns a string. A tool that cannot do what was asked returns "ERROR: <reason>", which the model reads
  and can act on.
- Settings come from environment variables, so the same text runs in a notebook, from PowerShell, and on a Space.
- The agent describes what the files hold. It gives no view on any bond, issuer, price, or yield.
"""
import json
import os
import re
from pathlib import Path

import gradio as gr
import openai
from openai import OpenAI

# the name on the product, and the model behind it: on a Space both are variables, so you rename without code
PRODUCT_NAME = os.environ.get("PRODUCT_NAME", "Desk Coder")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-6.1-sol")
# the one folder the tools may touch, as its true location on disk
WORKSPACE = Path(os.environ.get("AGENT_WORKSPACE", "workspace")).resolve()
MAX_TOOL_ROUNDS = 12  # a confused model stops here instead of looping on your bill
MAX_READ_CHARS = 50_000  # one huge file should not fill the whole context window
MAX_LISTED_FILES = 500
# sent with every request: nothing stored at OpenAI, one tool request at a time, no random field in a request
REQUEST_SETTINGS = {"store": False, "parallel_tool_calls": False, "prompt_cache_key": "bonus-coding-agent"}


SEED_FILES = {
    "README.txt": (
        "This folder is the agent's workspace.\n"
        "Every issuer, bond, and price in here is fictional and exists only for teaching.\n"
    ),
    "desk_riddle.txt": (
        "I pay you nothing for years, then everything at once.\n"
        "You pay less than face for me and I never send a coupon.\n"
        "What am I?\n"
    ),
    "bonds.csv": (
        "bond_id,issuer,coupon,maturity,rating,price\n"
        "B001,Alpha Rail,4.250,2031-06-15,A-,98.40\n"
        "B002,Bravo Energy,5.875,2030-03-01,BB+,101.25\n"
        "B003,Charlie Foods,3.750,2029-09-15,BBB,96.10\n"
        "B004,Delta Cable,7.500,2032-11-01,B,99.00\n"
        "B005,Echo Health,4.875,2033-02-15,BBB-,97.85\n"
        "B006,Foxtrot Steel,6.625,2031-08-01,BB-,100.50\n"
    ),
}


def ensure_workspace() -> None:
    """Create the workspace and write each starter file that is not there yet. Never overwrites a file."""
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    for name, text in SEED_FILES.items():
        target = WORKSPACE / name
        if not target.exists():
            target.write_text(text, encoding="utf-8")


class ToolError(Exception):
    """A tool could not do what was asked. Its message goes back to the model as the tool's result."""


def resolve_in_workspace(relative_path: str) -> Path:
    """The true location of a path the model gave, refused unless it is inside the workspace.

    Input: relative_path, as the model wrote it ("bonds.csv", "notes/a.txt").
    Output: the resolved Path, always inside WORKSPACE.
    Raises ToolError, quoting only the path the model gave, for anything that lands outside: "..", an absolute or
    drive-letter path, a link or junction that points out, or a sibling folder whose name starts with the
    workspace's.
    """
    # resolve() collapses ".." and follows links, so the check sees where the path really points
    candidate = (WORKSPACE / relative_path).resolve()
    if not candidate.is_relative_to(WORKSPACE):
        raise ToolError(f"'{relative_path}' is outside the workspace. Use a relative path inside it.")
    return candidate


def read_file(path: str) -> str:
    """The text of one file in the workspace, cut at MAX_READ_CHARS with a marker that gives both lengths."""
    target = resolve_in_workspace(path)
    if target.is_dir():
        raise ToolError(f"'{path}' is a directory. Use list_files instead.")
    if not target.exists():
        raise ToolError(f"No file at '{path}'. Use list_files to see what exists.")
    try:
        text = target.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ToolError(f"'{path}' is not a UTF-8 text file.") from error
    if len(text) > MAX_READ_CHARS:
        return text[:MAX_READ_CHARS] + f"\n\n[truncated: showing the first {MAX_READ_CHARS} of {len(text)} characters]"
    return text


READ_FILE_TOOL = {
    "type": "function",
    "name": "read_file",
    "description": "Read the contents of a text file in the workspace. Use this to see what is inside a file before "
                   "answering questions about it or editing it. Do not use it on directories.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string",
                     "description": "Relative path of the file inside the workspace, for example 'bonds.csv'."},
        },
        "required": ["path"],
        "additionalProperties": False,
    },
}

# two registries: what the model is told it can use, and the Python function behind each name
TOOLS = [READ_FILE_TOOL]
TOOL_FUNCTIONS = {"read_file": read_file}


def execute_tool(name: str, arguments_json: str) -> str:
    """Run one tool request and return its result as a string. Never raises: the model needs an answer either way.

    Inputs: name, the tool the model asked for; arguments_json, its arguments as JSON text.
    Output: the tool's string, or "ERROR: <reason>" for an unknown tool, arguments that are not JSON or do not fit
    the function, a ToolError, or a refusal from the operating system.
    """
    function = TOOL_FUNCTIONS.get(name)
    if function is None:
        return f"ERROR: there is no tool named '{name}'."
    try:
        return function(**json.loads(arguments_json))
    except ToolError as error:
        return f"ERROR: {error}"
    except (json.JSONDecodeError, TypeError) as error:
        return f"ERROR: bad arguments for {name}: {error}"
    except OSError as error:
        return f"ERROR: the operating system refused: {error}"


SYSTEM_PROMPT = f"""You are {PRODUCT_NAME}, a coding agent that works inside one folder called the workspace.
You can list files, read files, and edit files with your tools. All paths are relative to the workspace.
Read a file before you edit it. Make the smallest edit that does the job.
If a tool returns an error, read the message and try a different approach.
When you finish, say briefly what you did.
Describe only what the files hold. Never give a view on any bond, issuer, price, or yield.
If someone asks what powers you, say you run on an OpenAI model."""

# the line the series returns to any request for a view (Course 8's agentkit.REFUSAL, word for word)
REFUSAL_LINE = "REFUSED: this course asks only what the document says"
# Course 8's input rule, written here as data so this file needs no earlier module: the forecast and opinion words
# (mlkit.FORECAST_WORDS, textkit.OPINION_WORDS), counted only in a sentence with no negation, and an ordering of
# securities (credit_desk.ORDERING)
VIEW_WORDS = ["will", "expect", "expects", "should", "forecast", "forecasts", "cheap", "rich", "attractive", "signal",
              "signals", "buy", "sell", "approve", "decline", "lend", "invest", "loose", "looser", "tight", "tighter",
              "weak", "weaker", "strong", "stronger", "protective", "aggressive", "covenant-lite", "cov-lite",
              "borrower-friendly", "investor-friendly", "favourable", "favorable", "better", "worse", "riskier",
              "safer"]
NEGATION = re.compile(r"\b(?:no|not|never|nothing|neither|nor|without|cannot)\b|n't\b", re.IGNORECASE)
ORDERING = re.compile(r"\b(?:recommend\w*|rank\w*|best|worst|prefer\w*)\b", re.IGNORECASE)


def asks_for_a_view(text: str) -> bool:
    """True when a message asks for a view: a VIEW_WORDS word in a sentence with no negation, or an ordering.

    Matched as whole words in any case. A reminder, not a proof: a message can ask for a view in other words, and
    a harmless message can hold one of these words ("What will this function return?" is refused too).
    """
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if NEGATION.search(sentence):
            continue
        if any(re.search(rf"(?<![\w-]){re.escape(word)}(?![\w-])", sentence, re.IGNORECASE) for word in VIEW_WORDS):
            return True
    return bool(ORDERING.search(text))


def run_agent_turn(client: OpenAI, conversation: list, user_text: str):
    """Handle one user message: request, run the tools, send the results back, until the model answers.

    Inputs: client, an OpenAI client (the course's replay client in the notebook, get_client() in the app);
    conversation, the list of items sent so far, changed in place: it is the agent's memory and goes back in on
    the next turn; user_text, the message.
    Yields one event per step: {"type": "text", "text"}, {"type": "tool_call", "name", "arguments"},
    {"type": "tool_result", "name", "arguments", "result"}.
    Convention: a message that asks for a view gets REFUSAL_LINE and no request is sent. At most MAX_TOOL_ROUNDS
    requests a turn. On any error the items this turn added are removed before the error goes on.
    """
    checkpoint = len(conversation)
    conversation.append({"role": "user", "content": user_text})
    if asks_for_a_view(user_text):
        conversation.append({"role": "assistant", "content": REFUSAL_LINE})
        yield {"type": "text", "text": REFUSAL_LINE}
        return
    try:
        for _ in range(MAX_TOOL_ROUNDS):
            response = client.responses.create(model=MODEL, instructions=SYSTEM_PROMPT, tools=TOOLS,
                                               input=conversation, **REQUEST_SETTINGS)
            # keep every item the model returned, reasoning items included: the API needs them back next time
            conversation += response.output
            if response.output_text:
                yield {"type": "text", "text": response.output_text}
            tool_requests = [item for item in response.output if item.type == "function_call"]
            if not tool_requests:
                return  # an answer with no tool request ends the turn
            for request in tool_requests:
                yield {"type": "tool_call", "name": request.name, "arguments": request.arguments}
                result = execute_tool(request.name, request.arguments)
                conversation.append({"type": "function_call_output", "call_id": request.call_id, "output": result})
                yield {"type": "tool_result", "name": request.name, "arguments": request.arguments, "result": result}
        yield {"type": "text", "text": f"I stopped after {MAX_TOOL_ROUNDS} rounds of tool use. "
                                       "Ask me to continue if you want more."}
    except Exception:
        # a half-finished turn would leave tool requests with no results in memory, which the API refuses next
        # time: go back to the state before this turn
        del conversation[checkpoint:]
        raise


def shorten(text: str, limit: int = 1500) -> str:
    """At most limit characters of a text, with the number of characters left out stated."""
    return text if len(text) <= limit else text[:limit] + f"\n... [{len(text) - limit} more characters]"


def list_files(path: str) -> str:
    """Every file and folder under a folder of the workspace, as a JSON list of relative paths, folders ending in /.

    Sorted by the text of each path (capitals first, as on Linux), with __pycache__ and anything whose true location
    is outside the workspace left out, and cut at MAX_LISTED_FILES with a marker.
    """
    target = resolve_in_workspace(path)
    if not target.is_dir():
        raise ToolError(f"'{path}' is not a directory inside the workspace.")
    entries = []
    # sorted by the path's text, so the order is the same on Windows, Linux, and a Space (a request's key holds it)
    for item in sorted(target.rglob("*"), key=lambda found: found.relative_to(target).as_posix()):
        relative = item.relative_to(target)
        # a link or junction inside the workspace may point out of it: its entries are left out, as the fence says
        if "__pycache__" in relative.parts or not item.resolve().is_relative_to(WORKSPACE):
            continue
        entries.append(relative.as_posix() + "/" if item.is_dir() else relative.as_posix())
        if len(entries) >= MAX_LISTED_FILES:
            entries.append(f"[truncated at {MAX_LISTED_FILES} entries]")
            break
    return json.dumps(entries)


LIST_FILES_TOOL = {
    "type": "function",
    "name": "list_files",
    "description": "List every file and folder under a directory in the workspace. Folders end with a slash. Use this "
                   "to get your bearings before reading or editing.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Relative directory to list. Use '.' for the top of the workspace."},
        },
        "required": ["path"],
        "additionalProperties": False,
    },
}

TOOLS.append(LIST_FILES_TOOL)
TOOL_FUNCTIONS["list_files"] = list_files


def edit_file(path: str, old_str: str, new_str: str) -> str:
    """Replace old_str with new_str in one file of the workspace, or create the file when old_str is empty.

    On an existing file old_str must appear exactly once. Refused: identical strings, a directory, an empty
    old_str on a file that exists, an old_str found zero times or more than once (the count is given).
    """
    if old_str == new_str:
        raise ToolError("old_str and new_str are identical, so there is nothing to change.")
    target = resolve_in_workspace(path)
    if target.is_dir():
        raise ToolError(f"'{path}' is a directory, not a file.")
    if not target.exists():
        if old_str != "":
            raise ToolError(f"No file at '{path}'. To create it, use edit_file with old_str set to an empty string.")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_str, encoding="utf-8")
        return f"Created {path} ({len(new_str)} characters)."
    if old_str == "":
        raise ToolError(f"'{path}' already exists. Read it, then pass the exact text you want to replace as old_str.")
    content = target.read_text(encoding="utf-8")
    matches = content.count(old_str)
    if matches == 0:
        raise ToolError(f"old_str was not found in '{path}'. It must match exactly, including spaces and line breaks. "
                        "Read the file again.")
    if matches > 1:
        raise ToolError(f"old_str appears {matches} times in '{path}'. Include more surrounding text so it matches "
                        "exactly once.")
    target.write_text(content.replace(old_str, new_str, 1), encoding="utf-8")
    return f"Edited {path}."


EDIT_FILE_TOOL = {
    "type": "function",
    "name": "edit_file",
    "description": "Edit a text file by replacing old_str with new_str. old_str must appear exactly once in the file. "
                   "To create a new file, pass a path that does not exist yet and set old_str to an empty string; "
                   "new_str becomes the whole file.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Relative path of the file inside the workspace."},
            "old_str": {"type": "string", "description": "Exact text to replace. Must match once and only once. "
                                                         "Empty string when creating a new file."},
            "new_str": {"type": "string", "description": "Text that replaces old_str."},
        },
        "required": ["path", "old_str", "new_str"],
        "additionalProperties": False,
    },
}

TOOLS.append(EDIT_FILE_TOOL)
TOOL_FUNCTIONS["edit_file"] = edit_file


def trace_rows(events) -> list[dict]:
    """The tool-request log: one row per tool result, with step, tool, arguments, and result (its first 80
    characters), for a table on screen and a CSV for Excel."""
    rows = []
    for event in events:
        if event["type"] == "tool_result":
            rows.append({"step": len(rows) + 1, "tool": event["name"], "arguments": event["arguments"],
                         "result": event["result"][:80]})
    return rows


def usage_table(exchanges, prices: dict) -> list[dict]:
    """Tokens and US dollars per request, from the responses' usage.

    Inputs: exchanges, the requests sent or replayed (each with its "response" as JSON, as the course's client keeps
    them in client.exchanges); prices, US dollars per token, {"input": ..., "output": ...}, read on a dated page.
    Output: one row per exchange: request, input_tokens, output_tokens, usd.
    """
    rows = []
    for number, exchange in enumerate(exchanges, start=1):
        usage = exchange["response"]["usage"]
        usd = usage["input_tokens"] * float(prices["input"]) + usage["output_tokens"] * float(prices["output"])
        rows.append({"request": number, "input_tokens": usage["input_tokens"], "output_tokens": usage["output_tokens"],
                     "usd": usd})
    return rows


def get_client() -> OpenAI:
    """An OpenAI client that reads OPENAI_API_KEY from the environment; a plain message when the key is not set."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set. On your machine, put it in my_bondmath\\.env. "
            "On Hugging Face, add it under Settings, Variables and secrets, as a secret."
        )
    return OpenAI()


def respond(user_text: str, history: list, conversation: list, client=None):
    """The chat page's handler. history is what the screen shows; conversation is what the model sees.

    Yields ("", history, conversation) after every event, so the page updates as the agent works. A tool request
    shows as a collapsible step titled "Tool: <name>", pending until its result replaces it as done. An error from
    OpenAI, or a missing key, becomes one plain message titled "Something went wrong". client: None means
    get_client(); the notebook passes its replay client.
    """
    user_text = (user_text or "").strip()
    if not user_text:
        yield "", history, conversation
        return
    history = history + [gr.ChatMessage(role="user", content=user_text)]
    yield "", history, conversation
    try:
        client = client or get_client()
        for event in run_agent_turn(client, conversation, user_text):
            if event["type"] == "text":
                history.append(gr.ChatMessage(role="assistant", content=event["text"]))
            elif event["type"] == "tool_call":
                history.append(gr.ChatMessage(
                    role="assistant", content=f"Arguments:\n```json\n{event['arguments']}\n```",
                    metadata={"title": f"Tool: {event['name']}", "status": "pending"}))
            elif event["type"] == "tool_result":
                # the finished step replaces the pending one
                history[-1] = gr.ChatMessage(
                    role="assistant",
                    content=(f"Arguments:\n```json\n{event['arguments']}\n```\n"
                             f"Result:\n```\n{shorten(event['result'])}\n```"),
                    metadata={"title": f"Tool: {event['name']}", "status": "done"})
            yield "", history, conversation
    except openai.AuthenticationError:
        message = "OpenAI refused the API key. Check OPENAI_API_KEY."
    except openai.RateLimitError:
        message = "OpenAI's rate limit or your quota was reached. Check your usage and billing, then try again."
    except openai.APIConnectionError:
        message = "Could not reach OpenAI. Check your internet connection."
    except openai.APIStatusError as error:
        message = f"OpenAI returned an error ({error.status_code}): {error.message}"
    except RuntimeError as error:
        message = str(error)
    else:
        return
    history.append(gr.ChatMessage(role="assistant", content=message, metadata={"title": "Something went wrong"}))
    yield "", history, conversation


def build_app() -> gr.Blocks:
    """The chat page: a heading, the chat, a text box, Send, New conversation, and four example requests.

    Gradio's usage data is off. gr.State gives each browser session its own conversation.
    """
    with gr.Blocks(title=PRODUCT_NAME, analytics_enabled=False) as demo:
        gr.Markdown(f"# {PRODUCT_NAME}\nA coding agent that lists, reads, and edits files in its workspace. "
                    f"It runs on OpenAI `{MODEL}`.")
        chatbot = gr.Chatbot(label=PRODUCT_NAME, height=520)
        conversation = gr.State([])
        with gr.Row():
            box = gr.Textbox(placeholder="Ask me to read, explain, create, or change a file", show_label=False,
                             scale=8, autofocus=True)
            send = gr.Button("Send", variant="primary", scale=1)
        new_chat = gr.Button("New conversation")
        gr.Examples(
            examples=[
                "What files do you have?",
                "Solve the riddle in desk_riddle.txt",
                "Which bonds in bonds.csv are high yield?",
                "Create bond_math.py with a function bond_price(face, coupon_rate, ytm, years, freq=1)",
            ],
            inputs=box,
        )
        wiring = dict(fn=respond, inputs=[box, chatbot, conversation], outputs=[box, chatbot, conversation])
        box.submit(**wiring)
        send.click(**wiring)
        # a new conversation clears both: the screen and the model's memory
        new_chat.click(lambda: ([], []), inputs=None, outputs=[chatbot, conversation])
    return demo


# the top of app.py on a Space: a ZeroGPU Space expects a @spaces.GPU function. This agent needs no GPU, so the
# function is a placeholder that is never used; the spaces package exists only on Hugging Face, so on your machine
# the block does nothing
SPACE_PLACEHOLDER = '''try:
    import spaces

    @spaces.GPU(duration=1)
    def _zerogpu_placeholder():
        return None

except ImportError:
    pass

'''
# the bottom of app.py: seed the workspace, build the page, and start it (with a password only if one is set)
APP_TAIL = '''

ensure_workspace()
demo = build_app()

if __name__ == "__main__":
    # an optional password: APP_USERNAME and APP_PASSWORD, as Space secrets
    password = os.environ.get("APP_PASSWORD")
    login = (os.environ.get("APP_USERNAME", "student"), password) if password else None
    demo.launch(auth=login)
'''
SPACE_PYTHON = "3.12.12"
SPACE_DISCLAIMER = ("This course is educational content created in a personal capacity. Nothing here is investment "
                    "advice or a recommendation to buy or sell any security. All portfolio data is synthetic.")


def space_files(folder, product_name: str, gradio_version: str) -> list[Path]:
    """The three files a Hugging Face Space runs this agent from, written into folder (created if missing).

    Inputs: folder; product_name, the name on the Space's page (ASCII); gradio_version, the Gradio the Space
    installs from sdk_version (the version you tested with, gr.__version__).
    Output: the paths of app.py (SPACE_PLACEHOLDER, then this file's own text, then APP_TAIL), requirements.txt
    (openai only: the Space installs Gradio from sdk_version), and README.md (the Space's YAML header with every
    version in quotes and no emoji key, then what the app is, the date, the model, the credit, and the disclaimer),
    LF endings, ASCII.
    Convention: run it from coding_agent.py, whose text it copies, so the app on the Space is the code you tested.
    """
    if not product_name.isascii():
        raise ValueError("product_name must be ASCII: the Space's README is ASCII")
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    module_text = Path(__file__).read_text(encoding="utf-8")
    header = (f"---\ntitle: {json.dumps(product_name)}\ncolorFrom: green\ncolorTo: blue\nsdk: gradio\n"
              f'sdk_version: "{gradio_version}"\npython_version: "{SPACE_PYTHON}"\napp_file: app.py\npinned: false\n'
              "short_description: A small coding agent built in a notebook\n---\n")
    readme = (header + f"\n# {product_name}\n\nA coding agent with three tools: it lists, reads, and edits files in "
              "its own workspace folder and nothing outside it. No tool runs code. It runs on an OpenAI model "
              f"(`{MODEL}` unless the Space's OPENAI_MODEL variable names another); the key is a Space secret, never "
              "in these files. Every issuer, bond, and price in its workspace is fictional.\n\nBuilt 2026-10-12 in "
              "the Bonus course of Python for Fixed Income, a course series. The idea comes from Thorsten Ball, "
              '"How to Build an Agent" (https://ampcode.com/notes/how-to-build-an-agent, April 15, 2025).\n\n'
              + SPACE_DISCLAIMER + "\n")
    files = {"app.py": SPACE_PLACEHOLDER + module_text.rstrip("\n") + "\n" + APP_TAIL,
             "requirements.txt": "openai==3.26.0\n", "README.md": readme}
    written = []
    for name, text in files.items():
        if not text.isascii():
            raise ValueError(f"{name} would hold a character outside ASCII")
        (folder / name).write_text(text, encoding="utf-8", newline="\n")
        written.append(folder / name)
    return written


ensure_workspace()
demo = build_app()

if __name__ == "__main__":
    # an optional password: APP_USERNAME and APP_PASSWORD, as Space secrets
    password = os.environ.get("APP_PASSWORD")
    login = (os.environ.get("APP_USERNAME", "student"), password) if password else None
    demo.launch(auth=login)
