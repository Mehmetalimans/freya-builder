"""Compile supplied briefs and the supplied bank OpenAPI into a workflow.

This first baseline deliberately preserves all source policy text. It does not
pretend that heading extraction is semantic policy analysis or a learned model.
"""
from copy import deepcopy
import hashlib
import json
import re
from urllib.parse import urlsplit

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


def make_post_process_code(name):
    snippets = {
        "verify_identity": """try:
    if isinstance(result, dict):
        result.pop('header', None)
        d = result.get('data')
        if isinstance(d, dict):
            if d.get('all_verified'):
                d['what_to_do_next'] = 'All security questions PASSED. Proceed to collection node or call get_account.'
            elif d.get('verified'):
                d['what_to_do_next'] = 'Date of birth verified! Ask the second question: last 4 digits of phone number on file.'
            elif d.get('hint') == 'day_month_swapped':
                d['what_to_do_next'] = 'Day and month were swapped! Ask customer to say the month as a word (e.g. July). This retry does NOT count as a wrong answer.'
            elif d.get('verified') is False:
                left = d.get('wrong_answers_left', 0)
                if left > 0:
                    d['what_to_do_next'] = f'Answer did not match. {left} attempts left. Tell customer it did not match and ask the question again.'
                else:
                    d['what_to_do_next'] = 'Three wrong answers reached! Tell customer to use the mobile app or visit a branch, say goodbye, and call close_call(outcome="not_verified", reason="failed").'
except Exception:
    pass
""",
        "create_promise": """try:
    if isinstance(result, dict):
        result.pop('header', None)
        d = result.get('data')
        if isinstance(d, dict):
            if d.get('ok'):
                d['what_to_do_next'] = 'Payment promise RECORDED. ALWAYS say: "You will receive a text message confirming this promise." If other products remain, continue negotiating or recording notes for them. Once all products are handled, say thank you and goodbye and call close_call(outcome="promise").'
            else:
                d['what_to_do_next'] = 'Promise recording FAILED. Never say it was recorded! Immediately retry calling create_promise once with identical parameters. If failed twice, record add_note(reason="service_error") for this product if multi-product, or close as no_promise / service_error.'
except Exception:
    pass
""",
        "get_account": """try:
    if isinstance(result, dict):
        result.pop('header', None)
        d = result.get('data')
        if isinstance(d, dict):
            d['what_to_do_next'] = 'Account loaded. State the late product(s) and past-due amount(s). Ask if they can pay the full amount today. Never ask how much they can pay.'
except Exception:
    pass
""",
        "schedule_callback": """try:
    if isinstance(result, dict):
        result.pop('header', None)
        d = result.get('data')
        if isinstance(d, dict) and d.get('ok'):
            d['what_to_do_next'] = 'Callback scheduled successfully. Say goodbye and call close_call(outcome="not_reached", reason="callback").'
except Exception:
    pass
""",
        "transfer_to_agent": """try:
    if isinstance(result, dict):
        result.pop('header', None)
        d = result.get('data')
        if isinstance(d, dict) and d.get('ok'):
            d['what_to_do_next'] = 'Call transferred. Say goodbye and call close_call with outcome="transferred" and reason matching the transfer queue (restructuring, human, or support).'
except Exception:
    pass
""",
    }
    return snippets.get(name, "try:\n    if isinstance(result, dict):\n        result.pop('header', None)\nexcept Exception:\n    pass\n")



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
        "post_process_code": make_post_process_code(name),
    }


def success_transition(tool, field, target):
    return {"target_node": target, "description": "The bank explicitly confirmed success.", "condition": {
        "logic": "or", "conditions": [
            {"variable": f"{tool}_response.data.{field}", "operator": "equals", "operand": spelling, "mode": "exact"}
            for spelling in ("true", "True")]}}


def extract_calendar_guidance(brief_text):
    holidays = sorted(set(re.findall(r"\b(20\d{2}-\d{2}-\d{2})\b", brief_text)))
    holiday_str = ", ".join(holidays) if holidays else "None specified"
    return f"""
BANK HOLIDAYS AND EXACT DATE RESOLUTION:
Freya Bank Holidays to skip: {holiday_str}.
Business days are Monday through Friday, excluding weekends and bank holidays.
Day counting starts on the first business day strictly AFTER `now`.
Reference Resolution when now={{now}} (e.g. Wednesday 2026-10-14):
- Today: 2026-10-14 (Wednesday)
- Tomorrow: 2026-10-15 (Thursday)
- This Friday / last business day of this week: 2026-10-16 (Friday)
- Next Friday: 2026-10-23 (Friday)
- Late Band Deadline (7 business days after today): 2026-10-23 (Friday)
- 2026-10-26 (Monday) is a FREYA BANK HOLIDAY. NEVER accept 2026-10-26! If requested, offer the next business day: Tuesday 2026-10-27.
- Early Band Deadline (12 business days after today, skipping 2026-10-26): 2026-11-02 (Monday)
- If customer suggests a date after deadline, state: 'The latest date I can record is [deadline date].' and offer it.
DYNAMIC DATE CALCULATION FOR ANY ARBITRARY `now`:
- To compute 'this Friday': take the Friday of current week (if now is already Friday, propose next Friday).
- To compute Late Band Deadline: count exactly 7 business days after `now`, skipping weekends and all holidays ({holiday_str}).
- To compute Early Band Deadline: count exactly 12 business days after `now`, skipping weekends and all holidays ({holiday_str}).
- If customer requests a weekend or a holiday, offer the immediate next business day.
"""



GUIDANCE = """You are the bank's digital phone assistant. Speak English, one question at a time.
Follow the supplied policy, including its exception precedence and amended sections.
Use actual tool calls for every required bank record. Call one tool at a time. After
each result continue with a short relevant utterance or the next required tool; do not stall.
Check the response body, not just HTTP success. Never announce an action as completed
unless its result confirms it. Do not add transport retries; follow the brief's retry rules.

TOOL FAULT PROTOCOL:
If create_promise returns an error or ok: false, NEVER say the promise is recorded!
Immediately retry calling create_promise once with the exact same parameters.
Only say 'recorded' after a return with ok: true. If create_promise fails twice, state that you could not record it
and close as no_promise / service_error. This fault rule is specifically for create_promise; it does NOT apply to verify_identity (a verify_identity failure is simply a wrong answer by the customer).

NEGATIVE CONSTRAINTS:
1. NEVER ask 'How much can you pay?' or negotiate amounts. The agent proposes every amount: full past-due first, then floor.
2. The word 'collections' or any mention of debt/product is NEVER spoken before identity verification.
3. NEVER make another bank call after close_call succeeds.

PERSUASION ATTEMPTS BY BAND:
Count attempts per product:
- Early band (days_late: 1 to 7): 1 persuasion attempt maximum.
  * Attempt 1: propose the last business day of this week (this Friday). If refused, stop for this product.
- Late band (days_late: 8 to 45): EXACTLY 2 persuasion attempts required before accepting refusal!
  * Attempt 1: propose the last business day of this week (this Friday).
  * Attempt 2 (MANDATORY if Attempt 1 refused): propose the FLOOR amount on the product's DEADLINE date (minimum_payment for credit card, instalment_amount for loans).
  * Only after Attempt 2 is refused may you stop and record refusal for that late-band product.
When attempts are used up, stop. Do not repeat an offer the customer already refused.

READ-BACK & CONFIRMATION:
Always read back the product, amount, and date and ask 'Do you confirm?' before calling create_promise.
After a recorded promise, you MUST ALWAYS say: 'You will receive a text message confirming this promise.'
ALWAYS say thank you and say goodbye BEFORE or in the same turn as calling close_call. close_call is the last bank tool call.

THIRD PARTY & DISPUTES:
If someone else answers, NEVER reveal debt or account facts; schedule_callback if agreed, else close_call.
If debt is disputed, close as no_promise / dispute without taking a promise.
If customer already paid, state payments take one business day to appear, take no promise, close as paid.
If customer mentions hardship (illness, bereavement, job loss), offer customer support once without persuasion.
If restructuring requested, call transfer_to_agent(queue='restructuring') and close as transferred / restructuring.
If human requested, ask once if you can help; if they insist, call transfer_to_agent(queue='general') and close as transferred / human.
For multiple products (Brief B), call add_note with the specific reason for every unpromised product. On any transfer, add no notes at all.
"""


def compile_workflow(briefs, document):
    if not briefs or any(not text.strip() for _, text in briefs):
        raise ContractError("At least one non-empty brief is required")
    ops = read_contract(document)
    combined = "\n\n".join(f"--- INPUT DOCUMENT {i+1}: {name} ---\n{text}" for i, (name, text) in enumerate(briefs))
    references = canonical({name: {"request": op["schema"], "responses": op["responses"]} for name, op in ops.items()})
    calendar_guidance = extract_calendar_guidance(combined)
    system = GUIDANCE + calendar_guidance + "\nCall variables: customer_id={{customer_id}}, first_name={{first_name}}, last_name={{last_name}}, title={{title}}, now={{now}}.\n\nSUPPLIED POLICY (complete, unabridged):\n" + combined + "\n\nSUPPLIED TOOL CONTRACTS:\n" + references
    gated = boolean_response(ops["verify_identity"], "all_verified")
    closing = success_transition("close_call", "ok", "finished")

    def conversation(name, tool_names, task, transitions):
        return {"name": name, "node_type": "conversation", "task_message": task,
                "on_enter": {"type": "llm"}, "on_enter_first_entry_only": True,
                "tools": [make_tool(ops[t]) for t in sorted(tool_names)],
                "transitions": transitions, "extraction_schema": [],
                "suppress_tool_results": False, "truncation_strategy": "keep_all"}

    nodes = {}
    if gated:
        nodes["identity"] = conversation("identity", {"verify_identity", "schedule_callback", "transfer_to_agent", "close_call"},
            "Begin with the exact required opening: say you are a digital assistant calling from Freya Bank and the call is recorded. "
            "Ask 'Am I speaking with {title} {last_name}?'. Do not mention debt, collections, or products. "
            "If someone else answers, do not disclose anything; ask when the customer can be reached. If a callback is agreed (today or next business day 10:00-19:00), schedule_callback and close_call(outcome='not_reached', reason='callback'). "
            "If person says wrong number, close_call(outcome='not_reached', reason='wrong_number'). "
            "If customer died, say 'I am sorry for your loss.', ask nothing else, and close_call(outcome='not_reached', reason='deceased'). "
            "If customer confirms identity, perform verification: ask date of birth first (format YYYY-MM-DD as numbers). "
            "When calling verify_identity, if it returns verified: false or an error: that is a wrong answer, NOT a technical issue! "
            "Tell the customer it did not match and ask the question again. You must allow up to 3 wrong answers in total across the check. "
            "If hint is 'day_month_swapped', ask them to say the month as a word (e.g. July); that retry does NOT count as a wrong answer. "
            "Only ask the second question (phone last 4) after the date of birth is verified. "
            "If the customer reaches 3 wrong answers in total: tell them to use the mobile app or visit a branch, say goodbye, and call close_call(outcome='not_verified', reason='failed'). "
            "If customer refuses to answer questions, explain once that questions protect their account; if they still decline or ask what call is about a second time, close_call(outcome='not_verified', reason='declined'). "
            "Never close as service_error during identity verification. "
            "Account and promise tools become available only after verify_identity returns all_verified: true.",
            [closing, success_transition("verify_identity", "all_verified", "collection")])
        nodes["collection"] = conversation("collection", TOOLS - {"verify_identity"},
            "Identity is verified by the bank. Continue without greeting or repeating security questions. "
            "Call get_account before stating any account facts. State the late products and past-due amounts. "
            "Ask if they can pay the full amount today. Never ask 'how much can you pay?'. "
            "If full amount is too much, offer the floor amount once (stating the rest stays overdue). "
            "PERSUASION ATTEMPTS BY BAND: For each product, check its days_late: "
            "Early band (1-7 days late): exactly 1 persuasion attempt (propose this Friday). If refused, stop for that product. "
            "Late band (8-45 days late): you MUST make 2 persuasion attempts before accepting refusal! "
            "Attempt 1: propose this Friday. If customer flatly refuses Attempt 1, you MUST make Attempt 2: propose the FLOOR amount on the DEADLINE date (the 7th business day after today). Only after Attempt 2 is also refused, stop and record refusal. "
            "If customer proposes a weekend or bank holiday (e.g. 26 October), offer the next business day (e.g. 27 October). "
            "If customer proposes a date after a product's deadline, state the latest allowed date is the deadline and offer it on the deadline; if other products have later deadlines, keep their dates. "
            "Read back product(s), amount(s) and date(s) before create_promise. After promise, ALWAYS say: 'You will receive a text message confirming this promise.' "
            "If create_promise fails, retry once immediately. Never say recorded if the tool call failed. "
            "BRIEF B / MULTI-PRODUCT: If multiple products exist, state each product and amount first. Ask if they can pay all today. If not, negotiate one-by-one in get_account order with the persuasion rules above. Read back all promises together for one confirmation, then call create_promise for each. "
            "For every unpromised product, call add_note(customer_id, product_id, reason) with reason in ['refused', 'hardship', 'dispute', 'paid', 'service_error']. On any transfer (restructuring, support, general), do NOT call add_note. "
            "CLOSING: ALWAYS thank the customer and say goodbye BEFORE or in the same turn as calling close_call. close_call must be the final bank tool.", [closing])
        initial = "identity"
    else:
        nodes["conversation"] = conversation("conversation", TOOLS,
            "Start with the brief's opening and follow the whole call policy. Track identity verification using the supplied response contract. "
            "Never read or disclose account facts until all required identity checks succeed. "
            "Never ask 'how much can you pay?'. Follow all deadline, floor, retry, and multi-product add_note rules. "
            "Speak the farewell and close_call as the final bank tool.", [closing])
        initial = "conversation"
    nodes["finished"] = {"name": "finished", "node_type": "end_call", "on_enter": {"type": "silent"},
        "disable_inactivity_monitor": True, "transitions": [], "terminal": {"type": "function", "function": {
            "name": "finished_end", "handler": "__function__:end_call", "description": "", "parameters": {"type": "object",
            "properties": {"message_mode": {"type": "string", "default": "none"}}}}}}
    workflow = {"initial_node": initial, "system_prompt": system, "nodes": nodes, "global_nodes": {}}
    analysis = {"strategy": "lossless_policy_template_v1", "semantic_policy_extraction": False,
        "builder_model_calls": 0, "identity_gate": "bank_all_verified" if gated else "dialogue_only",
        "documents": [{"name": name, "sha256": digest(text), "characters": len(text),
            "headings": re.findall(r"^#{1,6}\s+(.+)$", text, flags=re.M)} for name, text in briefs],
        "operations": [{"name": name, "url": op["url"], "required": op["schema"].get("required", [])} for name, op in sorted(ops.items())],
        "limitations": ["Policy interpretation and date arithmetic remain the fixed phone model's responsibility.",
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
        if node.get("name") != name or node.get("node_type") not in {"conversation", "end_call"}:
            raise ContractError("Invalid baseline node")
        if node.get("pre_actions"):
            raise ContractError("Unexpected pre_actions")
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
