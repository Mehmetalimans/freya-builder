"""Compile supplied briefs and the supplied bank OpenAPI into a workflow.

This first baseline deliberately preserves all source policy text. It does not
pretend that heading extraction is semantic policy analysis or a learned model.
"""
from copy import deepcopy
import hashlib
import json
import re
from urllib.parse import urlsplit
from builder.calendar import calendar_spec, calendar_node, deadline_bands, offer_node, offer_extraction

TOOLS = frozenset({"verify_identity", "get_account", "create_promise", "add_note",
                   "schedule_callback", "transfer_to_agent", "close_call"})
BANK_ORIGIN = "https://freya-bank-mock.freyavoice.workers.dev"


class ContractError(ValueError):
    pass


def digest(value):
    data = value if isinstance(value, bytes) else value.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def resolve_refs(value, document, stack=()):
    if isinstance(value, list):
        return [resolve_refs(v, document, stack) for v in value]
    if not isinstance(value, dict):
        return value
    if "$ref" in value:
        ref = value["$ref"]
        if not ref.startswith("#/") or ref in stack:
            raise ContractError("Only non-recursive local OpenAPI references are supported")
        target = document
        try:
            for part in ref[2:].split("/"):
                target = target[part.replace("~1", "/").replace("~0", "~")]
        except (KeyError, TypeError):
            raise ContractError("Unresolved OpenAPI reference") from None
        resolved = resolve_refs(target, document, (*stack, ref))
        return {**resolved, **resolve_refs({k: v for k, v in value.items() if k != "$ref"}, document, stack)}
    return {k: resolve_refs(v, document, stack) for k, v in value.items()}


def read_contract(document):
    if not isinstance(document, dict) or not str(document.get("openapi", "")).startswith("3."):
        raise ContractError("Expected an OpenAPI 3 document")
    doc = resolve_refs(document, document)
    servers = doc.get("servers", [])
    if len(servers) != 1:
        raise ContractError("Expected exactly one bank server from the supplied API file")
    base = servers[0].get("url", "").rstrip("/")
    parsed = urlsplit(base)
    if (f"{parsed.scheme}://{parsed.netloc}" != BANK_ORIGIN or parsed.query or parsed.fragment
            or parsed.username or "{" in base):
        raise ContractError("Bank origin differs from kit v3; confirm an organizer update before enabling it")
    result = {}
    for path, item in doc.get("paths", {}).items():
        if not isinstance(item, dict) or not path.startswith("/") or "?" in path or "#" in path or ".." in path:
            raise ContractError("Unsupported API path")
        methods = set(item) & {"get", "put", "post", "delete", "patch", "head", "options", "trace"}
        if methods != {"post"} or item.get("parameters") or item.get("servers"):
            raise ContractError("Baseline supports the kit's POST JSON tools without path parameters")
        op = item["post"]
        name = op.get("operationId") or path.rsplit("/", 1)[-1]
        if name not in TOOLS or name in result or op.get("parameters") or op.get("servers") or op.get("security"):
            raise ContractError("Unsupported or duplicate bank operation")
        try:
            schema = op["requestBody"]["content"]["application/json"]["schema"]
        except KeyError:
            raise ContractError("Each tool must define a JSON request body") from None
        if schema.get("type") != "object" or not schema.get("properties"):
            raise ContractError("Tool body must have explicit object properties")
        props = schema["properties"]
        if props.get("customer_id", {}).get("type") != "string":
            raise ContractError("The kit call variable customer_id must remain a string field")
        if not set(schema.get("required", [])) <= set(props):
            raise ContractError("Unknown required body field")
        for field, spec in props.items():
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", field):
                raise ContractError("Unsupported body field name")
            if spec.get("type") not in {"string", "number", "integer", "boolean"} or any(
                    x in spec for x in ("oneOf", "anyOf", "allOf", "nullable")):
                raise ContractError("Baseline supports scalar body fields; nested/union schema needs an adapter")
        result[name] = {"name": name, "url": base + path, "schema": schema,
                        "summary": op.get("summary", ""), "description": op.get("description", ""),
                        "responses": op.get("responses", {})}
    if set(result) != TOOLS:
        raise ContractError("Expected exactly the seven bank tools supplied by the event")
    if not boolean_response(result["close_call"], "ok"):
        raise ContractError("close_call success signal changed; baseline needs a verified adapter")
    return result


def boolean_response(operation, field):
    for status, response in operation["responses"].items():
        if str(status).startswith("2"):
            schema = response.get("content", {}).get("application/json", {}).get("schema", {})
            if schema.get("properties", {}).get(field, {}).get("type") == "boolean":
                return True
    return False


TRIGGERS = {
    "verify_identity": "CALL for each complete identity answer required by the supplied brief. Do not guess missing fragments.",
    "get_account": "CALL only after all identity checks required by the supplied brief succeed. Use returned facts and identifiers.",
    "create_promise": "CALL only after the brief's amount/date checks and explicit confirmation. Do not claim success before the result.",
    "add_note": "CALL only when the supplied brief requires a note; never add notes merely because the tool exists.",
    "schedule_callback": "CALL only for a callback permitted by the supplied brief and agreed by the caller.",
    "transfer_to_agent": "CALL when the supplied brief requires transfer. Copy an allowed queue from this tool schema.",
    "close_call": "CALL exactly once at the end, after all required records and the spoken farewell. It is the last bank tool call.",
}


def make_tool(operation):
    name = operation["name"]
    body = deepcopy(operation["schema"])
    for field, spec in body["properties"].items():
        # Unique names avoid accidentally baking a previous tool's values on node entry.
        spec["default"] = "{{customer_id}}" if field == "customer_id" else "{{arg_" + name + "_" + field + "}}"
        if "enum" in spec:
            spec["description"] = spec.get("description", "") + " Allowed values: " + canonical(spec["enum"])
    body["required"] = [k for k in body.get("required", []) if k != "customer_id"]
    return {
        "type": "function", "config": {"timeoutMs": 12000, "maxRetries": 0},
        "function": {"name": name, "handler": "__function__:api_call",
            "description": TRIGGERS[name] + "\n" + operation["summary"] + "\n" + operation["description"],
            "parameters": {"type": "object", "properties": {
                "url": {"type": "string", "default": operation["url"]},
                "method": {"type": "string", "default": "POST"},
                "connect_retries": {"type": "number", "default": 0},
                "headers": {"type": "object", "properties": {
                    "Content-Type": {"type": "string", "default": "application/json"}}},
                "body": body}}},
    }


def success_transition(tool, field, target):
    return {"target_node": target, "description": "The bank explicitly confirmed success.", "condition": {
        "logic": "or", "conditions": [
            {"variable": f"{tool}_response.data.{field}", "operator": "equals", "operand": spelling, "mode": "exact"}
            for spelling in ("true", "True")]}}


GUIDANCE = """You are the bank's digital phone assistant. Speak English, one question at a time.
Follow the supplied policy, including its exception precedence and amended sections.
Use actual tool calls for every required bank record. Call one tool at a time. After
each result continue with a short relevant utterance or the next required tool; do not stall.
Check the response body, not just HTTP success. Never announce an action as completed
unless its result confirms it. Do not add transport retries; follow the brief's retry rules.
For identity checks, transport success or ok=true means the request was processed;
it does NOT mean the answer was correct. Use verified and all_verified for that.
A rejected identity answer is not a service error. While policy allows another attempt,
ask that same unanswered security question again. Do not skip to a different question
or claim a technical failure. Use the returned remaining-attempt count and hints.
Use ONLY now supplied with this call for dates; never use your real clock. Resolve relative
dates, weekends, holidays, minimum amounts and deadlines from this brief and account results.
Keep per-product decisions separate and preserve the bank's product order. Copy identifiers
from results, never infer them. Preserve partial answers until complete; use the caller's
latest correction and reconfirm any changed promise before recording it.
Questions, digressions and incidental dates are not consent, payment offers or refusals
unless the brief explicitly says so. Apply the brief's rules for third parties and identity.
Do not invent terms, policy, tools, services, facts or outcomes. Tool descriptions are
an interface reference; the supplied policy determines when each operation is allowed.
Say the required farewell BEFORE close_call. Never make another bank call after it succeeds.
"""


def compile_workflow(briefs, document):
    if not briefs or any(not text.strip() for _, text in briefs):
        raise ContractError("At least one non-empty brief is required")
    ops = read_contract(document)
    combined = "\n\n".join(f"--- INPUT DOCUMENT {i+1}: {name} ---\n{text}" for i, (name, text) in enumerate(briefs))
    references = canonical({name: {"request": op["schema"], "responses": op["responses"]} for name, op in ops.items()})
    system = GUIDANCE + "\nCall variables: customer_id={{customer_id}}, first_name={{first_name}}, last_name={{last_name}}, title={{title}}, now={{now}}.\n\nSUPPLIED POLICY (complete, unabridged):\n" + combined + "\n\nSUPPLIED TOOL CONTRACTS:\n" + references
    calendar = calendar_spec(briefs)
    gated = boolean_response(ops["verify_identity"], "all_verified")
    closing = success_transition("close_call", "ok", "finished")

    def conversation(name, tool_names, task, transitions):
        if calendar:
            task += ("\nDATE LOOKUP computed from call now and the supplied holiday calendar:\n{{calendar_facts}}\n"
                     "Use these computed dates, never mental weekday or business-day arithmetic. "
                     "For an Nth-business-day deadline select the line marked #N, separately for each product's policy band. "
                     "Keep the proposed date distinct from the deadline. When the customer clarifies a vague period with an exact day, use that exact day. "
                     "A holiday/weekend before the deadline is NOT a request beyond the deadline. "
                     "When the policy requires moving it forward, use its explicit NEXT BUSINESS DAY value, then check the deadline. "
                     "Do not substitute the deadline just because a day is a holiday or a prior answer was vague. "
                     "The calendar is arithmetic assistance, not a replacement for the supplied date policy.")
        return {"name": name, "node_type": "conversation", "task_message": task,
                "on_enter": {"type": "llm"}, "on_enter_first_entry_only": True,
                "tools": [make_tool(ops[t]) for t in sorted(tool_names)],
                "transitions": transitions, "extraction_schema": [],
                "suppress_tool_results": False, "truncation_strategy": "keep_all"}

    nodes = {}
    if gated:
        nodes["identity"] = conversation("identity", {"verify_identity", "schedule_callback", "transfer_to_agent", "close_call"},
            "Begin with the exact required opening, then establish who is on the line and perform the identity section. "
            "Handle questions, third parties, refusal, callback and human requests as the policy requires. "
            "Account and promise tools become available only after the bank confirms all identity checks. "
            "Never disclose account information before that. On failure or other early exit, complete required permitted records and close_call.",
            [closing, success_transition("verify_identity", "all_verified", "collection")])
        nodes["collection"] = conversation("collection", TOOLS - {"verify_identity"},
            "Identity is verified by the bank. Continue without greeting or repeating security questions. "
            "Call get_account before stating any account facts. Follow all supplied rules for each product, "
            "exceptions, confirmation, records and closing. Do not assume a successful promise is the only valid outcome.", [closing])
        initial = "identity"
    else:
        nodes["conversation"] = conversation("conversation", TOOLS,
            "Start with the brief's opening and follow the whole call policy. The API has no documented all_verified boolean, "
            "so track completion using its supplied verification response contract. Never read an account or disclose it "
            "until every required identity check succeeds. Complete all required bank records, speak the farewell and close_call.", [closing])
        initial = "conversation"
    bands = deadline_bands(briefs)
    if calendar and bands and gated:
        date_transition = {"target_node": "date_offer", "description": "A precise payment date needs calculation.",
            "condition": {"logic": "or", "conditions": [{"variable": "payment_offer_action", "operator": "equals", "operand": "resolve", "mode": "exact"}]}}
        nodes["collection"]["extraction_schema"] = offer_extraction()
        nodes["collection"]["transitions"].append(date_transition)
        nodes["date_offer"] = offer_node(calendar, bands)
        nodes["date_reply"] = conversation("date_reply", TOOLS - {"verify_identity"},
            "The bank account is already known. Resolve the customer's date using these freshly computed facts:\n"
            "{{payment_date_facts}}\n"
            "Use DATE TO OFFER for the relevant product. If a non-business offer is inside its window, briefly "
            "explain the business-day adjustment and offer that calculated date; do not replace it with the deadline. "
            "If it is outside the window, explain and offer the calculated deadline according to the policy. "
            "Then complete the amount agreement, explicit read-back confirmation and actual bank records. "
            "In a multi-product call apply the amended per-product rules, including one combined read-back. "
            "Answer any customer question and handle exceptions before continuing; a date proposal is not a refusal. "
            "Follow the rest of the supplied policy through closing.", [closing, date_transition])
        nodes["date_reply"]["extraction_schema"] = offer_extraction()
    nodes["finished"] = {"name": "finished", "node_type": "end_call", "on_enter": {"type": "silent"},
        "disable_inactivity_monitor": True, "transitions": [], "terminal": {"type": "function", "function": {
            "name": "finished_end", "handler": "__function__:end_call", "description": "", "parameters": {"type": "object",
            "properties": {"message_mode": {"type": "string", "default": "none"}}}}}}
    workflow = {"initial_node": initial, "system_prompt": system, "nodes": nodes, "global_nodes": {}}
    if calendar:
        nodes["calendar_setup"] = calendar_node(calendar, initial)
        workflow["initial_node"] = "calendar_setup"
    analysis = {"strategy": "lossless_policy_template_v1", "semantic_policy_extraction": False,
        "builder_model_calls": 0, "identity_gate": "bank_all_verified" if gated else "dialogue_only",
        "calendar": calendar or {"status": "unsupported_definition_policy_only"},
        "deadline_bands": bands,
        "documents": [{"name": name, "sha256": digest(text), "characters": len(text),
            "headings": re.findall(r"^#{1,6}\s+(.+)$", text, flags=re.M)} for name, text in briefs],
        "operations": [{"name": name, "url": op["url"], "required": op["schema"].get("required", [])} for name, op in sorted(ops.items())],
        "limitations": ["Policy interpretation remains the fixed phone model's responsibility; calendar arithmetic supports only the documented recognized definition and a 90-day horizon.",
            "No benchmark success is implied by compilation or local validation.",
            "Only scalar POST JSON tool bodies are supported; unsupported contracts fail explicitly."]}
    validate_workflow(workflow, ops)
    return workflow, analysis


def validate_workflow(workflow, operations):
    def reject_nulls(value):
        if value is None:
            raise ContractError("Null is not permitted in this baseline's workflow")
        if isinstance(value, dict):
            for child in value.values(): reject_nulls(child)
        if isinstance(value, list):
            for child in value: reject_nulls(child)
    reject_nulls(workflow)
    if "agent_config" in workflow or workflow.get("test_variables"):
        raise ContractError("Do not embed model overrides or test customers")
    nodes = workflow["nodes"]
    if workflow["initial_node"] not in nodes:
        raise ContractError("Missing entry node")
    seen_tools = set()
    for name, node in nodes.items():
        if node.get("name") != name or node.get("node_type") not in {"conversation", "end_call", "code"}:
            raise ContractError("Invalid baseline node")
        if node.get("pre_actions") and name not in {"calendar_setup", "date_offer"}:
            raise ContractError("Unexpected pre_actions")
        if name in {"calendar_setup", "date_offer"}:
            action = node.get("pre_actions", [{}])[0].get("function", {})
            code = action.get("parameters", {}).get("properties", {}).get("code", {}).get("default", "")
            if action.get("handler") != "__function__:code_exec" or not code or "{{" in code or "}}" in code:
                raise ContractError("Invalid calendar calculation")
            try:
                compile(code, name, "exec")
            except SyntaxError:
                raise ContractError("Generated calendar code has invalid syntax") from None
        for transition in node.get("transitions", []):
            if transition["target_node"] not in nodes:
                raise ContractError("Dangling transition")
        for tool in node.get("tools", []):
            func = tool["function"]
            tool_name = func["name"]
            if tool_name not in operations or tool != make_tool(operations[tool_name]):
                raise ContractError("Tool no longer matches its supplied API contract")
            seen_tools.add(tool_name)
    if seen_tools != TOOLS:
        raise ContractError("A required bank tool is missing")
    reachable, pending = set(), [workflow["initial_node"]]
    while pending:
        key = pending.pop()
        if key in reachable: continue
        reachable.add(key)
        pending.extend(t["target_node"] for t in nodes[key].get("transitions", []))
    if reachable != set(nodes) or "finished" not in reachable:
        raise ContractError("Unreachable workflow node")
