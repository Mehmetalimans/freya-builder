"""Trace, time limit, exclusive state and the unmodified official Freya client."""
from contextlib import contextmanager
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from builder.core import ContractError, digest

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "starter-v3" / "build-the-builder"
CLIENT_SHA256 = "881c5c86c784e16fe3b53d40a7e9a9d9318f45b6ce6fe4be992c27e522c7732b"
FREYA_ORIGIN = "https://staging-app.freyavoice.ai"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def redact(text):
    text = str(text)
    for name in ("FREYA_API_KEY", "FREYA_BANK_TEAM_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
        secret = os.environ.get(name)
        if secret: text = text.replace(secret, "[REDACTED]")
    return re.sub(r"\bfak_[A-Za-z0-9_-]+", "[REDACTED]", text)


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    os.replace(temp, path)


class Trace:
    def __init__(self, path):
        self.path = Path(path)
        self.started = time.monotonic()

    def emit(self, event, **fields):
        row = {"at_utc": utc_now(), "elapsed_seconds": round(time.monotonic() - self.started, 3),
               "event": event, **fields}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(redact(json.dumps(row, ensure_ascii=False)) + "\n")


@contextmanager
def exclusive(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ContractError("A local run is active, or a stale lock remains. Inspect it before retrying.") from None
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


def check_environment(require_bank=False):
    for name in ("FREYA_API_KEY", "FREYA_WORKSPACE_ID"):
        if not os.environ.get(name):
            raise ContractError(f"Set {name} locally; never send its value in chat")
    if os.environ.get("FREYA_API_URL", FREYA_ORIGIN).rstrip("/") != FREYA_ORIGIN:
        raise ContractError("This release is pinned to the official kit's staging origin")
    for name in ("FREYA_AGENT_MODEL", "FREYA_AGENT_PROVIDER"):
        if os.environ.get(name, "experimental-5") != "experimental-5":
            raise ContractError("Changing the event's phone model is forbidden")
    if require_bank:
        if len(os.environ.get("FREYA_BANK_TEAM_KEY", "")) < 16:
            raise ContractError("Set a local FREYA_BANK_TEAM_KEY of at least 16 characters")
        if os.environ.get("FREYA_BANK_HOST", "https://freya-bank-mock.freyavoice.workers.dev") != "https://freya-bank-mock.freyavoice.workers.dev":
            raise ContractError("Practice bank host must match kit v3")


def check_run_workspace(saved, workspace_id):
    """A recorded deployment must be evaluated with the same workspace context."""
    if not workspace_id or saved.get("workspace_id") != workspace_id:
        raise ContractError("Build workspace does not match the evaluation workspace; deploy separately in the intended workspace")


def verify_key_workspace(response, workspace_id):
    """Create routes infer the workspace from the key, so require one exact scope."""
    items = response.get("workspaces", response.get("items")) if isinstance(response, dict) else response
    if (not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict)
            or items[0].get("id") != workspace_id):
        raise ContractError("API key workspace is ambiguous or differs from FREYA_WORKSPACE_ID; no mutation was sent")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class FreyaTransport:
    def __init__(self, deadline, trace):
        self.deadline = deadline
        self.trace = trace
        self.opener = urllib.request.build_opener(NoRedirect())

    def __call__(self, method, path, body=None, **params):
        left = self.deadline - time.monotonic()
        if left <= 0: raise TimeoutError("Builder time limit reached")
        if not path.startswith("/api/v2/") or "?" in path or "#" in path or ".." in path:
            raise ContractError("Unexpected Freya route")
        query = "?" + urllib.parse.urlencode(params) if params else ""
        request = urllib.request.Request(FREYA_ORIGIN + path + query,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Authorization": "Bearer " + os.environ["FREYA_API_KEY"],
                     "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (build-the-builder)"}, method=method)
        start = time.monotonic()
        try:
            with self.opener.open(request, timeout=min(120, left)) as response:
                payload = json.load(response)
        except urllib.error.HTTPError as error:
            # Do not log server bodies, headers, requests or keys. Mutations are never blindly retried.
            self.trace.emit("api_error", method=method, route=path, status=error.code)
            # The organizer client explicitly waits on this rejection. Preserve its
            # signal without leaking the server response or retrying ambiguous writes.
            raw = error.read(65536).decode("utf-8", errors="replace")
            if error.code in (403, 409, 429) and "concurrent simulations" in raw.lower():
                raise RuntimeError("concurrent simulations: workspace is busy") from None
            raise ContractError(f"Freya returned HTTP {error.code}; inspect the platform privately") from None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            self.trace.emit("api_error", method=method, route=path, kind="transport_or_response")
            raise ContractError("Freya request failed; a mutation may have completed. Reconcile before rerunning.") from None
        if not isinstance(payload, dict) or payload.get("success") is not True or "result" not in payload.get("data", {}):
            raise ContractError("Unexpected or unsuccessful Freya response envelope")
        self.trace.emit("api", method=method, route=path, seconds=round(time.monotonic() - start, 3))
        return payload["data"]["result"]


def official_client(deadline, trace):
    file = KIT / "freya.py"
    if digest(file.read_bytes()) != CLIENT_SHA256:
        raise ContractError("Official client differs from the pinned kit v3")
    spec = importlib.util.spec_from_file_location("freya_kit_v3", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.api = FreyaTransport(deadline, trace)
    module._ws = os.environ["FREYA_WORKSPACE_ID"]
    verify_key_workspace(module.api("GET", "/api/v2/workspaces"), module._ws)
    trace.emit("workspace_verified", workspace_id=module._ws)
    return module


def verify_readback(expected, exported):
    actual = exported.get("workflow", {})
    if actual.get("initial_node") != expected["initial_node"] or actual.get("system_prompt") != expected["system_prompt"]:
        raise ContractError("Platform readback changed the entry point or policy")
    llm = actual.get("agent_config", {}).get("llmConfig", {})
    if (llm.get("provider"), llm.get("model")) != ("experimental-5", "experimental-5"):
        raise ContractError("Exported phone model is not the required event model")

    # Verify exact node set
    expected_nodes = set(expected["nodes"].keys())
    actual_nodes = set(actual.get("nodes", {}).keys())
    if actual_nodes != expected_nodes:
        raise ContractError(f"Platform readback node set mismatch: expected {expected_nodes}, got {actual_nodes}")

    # Verify global_nodes
    expected_global = expected.get("global_nodes", {})
    actual_global = actual.get("global_nodes", {})
    if actual_global != expected_global:
        raise ContractError("Platform readback modified global_nodes")

    # Complete behavioral fields comparison per node
    behavior_fields = (
        "node_type", "task_message", "tools", "transitions", "terminal",
        "pre_actions", "passthrough", "passthrough_default_transition",
        "extraction_schema", "on_enter", "on_enter_first_entry_only",
        "suppress_tool_results", "truncation_strategy"
    )
    for key, node in expected["nodes"].items():
        stored = actual.get("nodes", {}).get(key, {})
        for field in behavior_fields:
            if field in node and stored.get(field) != node[field]:
                raise ContractError(f"Platform readback changed behavioral field '{field}' on node '{key}'")
