# Freya Phone Agent Builder Optimization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the Freya Phone Agent Builder into a high-scoring, resilient, and fully autonomous agent generator capable of achieving 100% pass rates across all public practice cases (PUB-01 to PUB-13) and acing unseen competition briefs on Sunday.

**Architecture:** 
1. Deterministic Python OpenAPI compiler (`builder/core.py`) with zero external runtime dependencies.
2. Sandboxed tool post-processing hooks (`post_process_code`) injecting prescriptive `what_to_do_next` instructions into tool responses and stripping extraneous headers to eliminate LLM silence and misinterpretation.
3. Automated brief policy extraction that dynamically extracts bank holidays, business day rules, and band deadlines from supplied briefs to eliminate calendar hallucinations.
4. Robust state machine handling both single-product (Brief A) and multi-product (Brief B) debt collections with notes, callbacks, transfers, and error recovery.

**Tech Stack:** Python 3.12 (standard library only: `json`, `re`, `hashlib`, `urllib`, `datetime`), Freya Voice API v2/v3, Freya Bank Mock Service.

---

### Task 1: Add Tool Post-Processing Hooks (`post_process_code`) in `builder/core.py`

**Files:**
- Modify: `builder/core.py:120-142`
- Test: `tests/test_builder.py`

**Step 1: Write the failing test**
In `tests/test_builder.py`, add a test verifying that `make_tool` equips tools with safe, exception-wrapped `post_process_code` hooks that strip HTTP headers and append actionable guidance.

```python
def test_tools_include_post_process_hooks(self):
    wf, _ = self.compile()
    for node in wf["nodes"].values():
        for tool in node.get("tools", []):
            name = tool["function"]["name"]
            self.assertIn("post_process_code", tool, f"Tool {name} missing post_process_code")
            self.assertIn("result.pop('header'", tool["post_process_code"])
```

**Step 2: Run test to verify it fails**
Run: `python -m unittest tests.test_builder.CompilerTests.test_tools_include_post_process_hooks -v`
Expected: FAIL (`AssertionError: Tool verify_identity missing post_process_code`)

**Step 3: Write minimal implementation**
In `builder/core.py`, define hook generator `make_post_process_code(operation_name)`:
```python
def make_post_process_code(name):
    # Verified in starter kit docs (docs/tools-and-code.md):
    # Strips header to save token context and injects 'what_to_do_next' to prevent agent silence or misinterpretation.
    snippets = {
        "verify_identity": """try:
    if isinstance(result, dict):
        result.pop('header', None)
        d = result.get('data')
        if isinstance(d, dict):
            if d.get('all_verified'):
                d['what_to_do_next'] = 'All identity questions PASSED. Proceed to collection node or call get_account.'
            elif d.get('verified'):
                d['what_to_do_next'] = 'This question passed! Ask the second question (last 4 digits of phone number).'
            elif d.get('hint') == 'day_month_swapped':
                d['what_to_do_next'] = 'Day and month were swapped! Ask customer to say the month as a word (e.g., July). This retry does NOT count as a wrong answer.'
            else:
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
                d['what_to_do_next'] = 'Payment promise RECORDED. ALWAYS say: "You will receive a text message confirming this promise." Then say thank you and goodbye and call close_call(outcome="promise").'
            else:
                d['what_to_do_next'] = 'Promise recording FAILED. Never say it was recorded! Immediately retry calling create_promise once with identical parameters. If failed twice, close as no_promise / service_error.'
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
        if isinstance(d, dict):
            d['what_to_do_next'] = 'Callback scheduled. Say goodbye and call close_call(outcome="not_reached", reason="callback").'
except Exception:
    pass
""",
        "transfer_to_agent": """try:
    if isinstance(result, dict):
        result.pop('header', None)
        d = result.get('data')
        if isinstance(d, dict):
            d['what_to_do_next'] = 'Call transferred. Say goodbye and call close_call(outcome="transferred", reason=chosen_queue).'
except Exception:
    pass
""",
        "close_call": """try:
    if isinstance(result, dict):
        result.pop('header', None)
except Exception:
    pass
""",
        "add_note": """try:
    if isinstance(result, dict):
        result.pop('header', None)
except Exception:
    pass
"""
    }
    return snippets.get(name, "try:\n    if isinstance(result, dict): result.pop('header', None)\nexcept Exception:\n    pass\n")
```
Attach `"post_process_code": make_post_process_code(name)` inside `make_tool`.

**Step 4: Run test to verify it passes**
Run: `python -m unittest tests.test_builder.CompilerTests.test_tools_include_post_process_hooks -v`
Expected: PASS

**Step 5: Commit**
`git add builder/core.py tests/test_builder.py`
`git commit -m "feat(core): add tool post_process_code hooks for explicit agent guidance"`

---

### Task 2: Automated Calendar Policy Extraction & Dynamic Calendar Facts

**Files:**
- Modify: `builder/core.py`
- Test: `tests/test_builder.py`

**Step 1: Write the failing test**
In `tests/test_builder.py`, verify that `compile_workflow` extracts bank holidays and business day limits from brief text and formats a deterministic date guide into the system prompt:
```python
def test_calendar_facts_extracted_from_brief(self):
    wf, analysis = self.compile()
    self.assertIn("2026-10-26", wf["system_prompt"])
    self.assertIn("BANK HOLIDAYS", wf["system_prompt"])
    self.assertIn("DEADLINE RULES", wf["system_prompt"])
```

**Step 2: Run test to verify it fails**
Run: `python -m unittest tests.test_builder.CompilerTests.test_calendar_facts_extracted_from_brief -v`
Expected: FAIL

**Step 3: Implement minimal code**
In `builder/core.py`, write a brief extractor that finds:
- All dates formatted `YYYY-MM-DD` associated with holidays: `re.findall(r"(\d{4}-\d{2}-\d{2})", holiday_text)`
- Early and late band rules from table: (1-7 days late -> 12 business days, 8-45 days late -> 7 business days)
- Builds an explicit, high-priority system prompt block instructing the dialogue model how to resolve dates relative to `{{now}}`, with exact examples for the practice dates (14 October 2026 -> Friday 16 October, Friday 23 October deadline, skipping 26 October holiday).

**Step 4: Run test to verify it passes**
Run: `python -m unittest tests.test_builder.CompilerTests.test_calendar_facts_extracted_from_brief -v`
Expected: PASS

**Step 5: Commit**
`git add builder/core.py tests/test_builder.py`
`git commit -m "feat(core): extract calendar policy and inject explicit calendar resolution guidelines"`

---

### Task 3: Comprehensive Dialogue Policy Hardening (Rules 1-47)

**Files:**
- Modify: `builder/core.py`
- Test: `tests/test_builder.py`

**Step 1: Write the failing test**
In `tests/test_builder.py`, verify prompt instructions cover:
- Saying the farewell BEFORE or with `close_call`
- Text message confirmation sentence requirement
- Floor proposal rule (never asking "how much can you pay?")
- Third-party callback constraints
- Hardship and dispute handling without taking promises

```python
def test_prompt_covers_critical_judge_criteria(self):
    wf, _ = self.compile()
    prompt = wf["system_prompt"]
    self.assertIn("You will receive a text message confirming this promise", prompt)
    self.assertIn("Never ask 'How much can you pay?'", prompt)
    self.assertIn("Thank the customer and say goodbye before", prompt)
```

**Step 2: Run test to verify it fails**
Run: `python -m unittest tests.test_builder.CompilerTests.test_prompt_covers_critical_judge_criteria -v`
Expected: FAIL or PASS depending on exact phrasing.

**Step 3: Implement minimal code**
Refine `GUIDANCE` and `task_message` strings in `builder/core.py` to leave zero ambiguity for the `experimental-5` model. Specifically:
- **Rule 47 (Closing)**: "ALWAYS say: 'Thank you for your time. Have a great day, goodbye.' BEFORE or in the same turn as calling close_call. close_call is the last tool call."
- **Rule 38 (SMS)**: "Immediately upon promise recording, you MUST say: 'You will receive a text message confirming this promise.'"
- **Rule 24 & 26 (Amounts)**: "NEVER ask 'How much can you pay?'. Always propose the full past-due amount first. If they say it is too much, offer the minimum floor once, stating the rest remains overdue."
- **Rule 13 (Swapped DOB)**: "If day and month were swapped, ask for the month as a word; do not penalize as wrong."
- **Rule 32 (Hardship)**: "If illness, job loss, or bereavement mentioned, offer customer support once. If declined, close as no_promise / hardship."

**Step 4: Run all unit tests**
Run: `python -m unittest discover -s tests -v`
Expected: 31+ tests PASS.

**Step 5: Commit**
`git add builder/core.py tests/test_builder.py`
`git commit -m "feat(core): strengthen guidance and task prompts for all 47 brief rules"`

---

### Task 4: Multi-Product Workflow Support (Brief B)

**Files:**
- Modify: `builder/core.py`
- Test: `tests/test_builder.py`

**Step 1: Write the failing test**
In `tests/test_builder.py`, add a test compiling Brief A + Brief B together:
```python
def test_compile_brief_b_multi_product(self):
    brief_b = (KIT / "briefs/brief-b.md").read_text(encoding="utf-8")
    wf, analysis = compile_workflow([("brief-a.md", BRIEF), ("brief-b.md", brief_b)], self.doc)
    prompt = wf["system_prompt"]
    self.assertIn("Brief B", prompt)
    self.assertIn("add_note", [t["function"]["name"] for t in wf["nodes"]["collection"]["tools"]])
```

**Step 2: Run test to verify it fails/passes**
Run: `python -m unittest tests.test_builder.CompilerTests.test_compile_brief_b_multi_product -v`

**Step 3: Implement minimal code**
In `builder/core.py`:
- Ensure `collection` node prompt explicitly checks whether multi-product instructions from Brief B are active.
- Instruct:
  1. Announce all late products (one sentence each) before asking for anything.
  2. Ask if they can pay all today. If not, go through products in order.
  3. Single combined read-back for all promised products.
  4. Call `create_promise` for each promised product.
  5. Call `add_note` for every unpromised product with the appropriate reason (`refused`, `hardship`, `dispute`, `paid`, `service_error`).
  6. Final outcome logic: `promise` if any promised; otherwise follow first unpromised product's reason.

**Step 4: Run all unit tests**
Run: `python -m unittest discover -s tests -v`
Expected: All tests PASS.

**Step 5: Commit**
`git add builder/core.py tests/test_builder.py`
`git commit -m "feat(core): support Brief B multi-product rules, notes, and closing logic"`

---

### Task 5: Live Deploy & Verification of Brief A Fixes on Freya Staging

**Files:**
- Run deploy command with `--deploy` and `--slot practice-a`.

**Step 1: Deploy updated workflow**
```powershell
$env:FREYA_API_KEY="<YOUR_FREYA_API_KEY>"
$env:FREYA_WORKSPACE_ID="<YOUR_FREYA_WORKSPACE_ID>"
$env:FREYA_BANK_TEAM_KEY="<YOUR_FREYA_BANK_TEAM_KEY>"
python builder/build.py starter-v3/build-the-builder/briefs/brief-a.md starter-v3/build-the-builder/tools/openapi.json --slot practice-a --deploy
```
Expected: `deployed_verified` status with new `workflow_id` and `agent_id`.

**Step 2: Run PUB-03 (The previous failure case)**
```powershell
python starter-v3/build-the-builder/tools/run_cases.py <new_agent_id> --brief A --only PUB-03 --cases starter-v3/build-the-builder/public-test-set.json
```
Expected: `PASS PUB-03 medium Identity | verify > verify > verify > close_call`.

**Step 3: Run Remaining Development Cases (PUB-01, PUB-02, PUB-04, PUB-05, PUB-06, PUB-07)**
```powershell
python starter-v3/build-the-builder/tools/run_cases.py <new_agent_id> --brief A --only PUB-01,PUB-02,PUB-04,PUB-05,PUB-06,PUB-07 --cases starter-v3/build-the-builder/public-test-set.json
```
Expected: All 6 dev cases PASS (6/6).

---

### Task 6: Deploy & Verify Multi-Product Practice Cases (Brief B)

**Files:**
- Deploy with `--slot practice-b` and `--extra-brief starter-v3/build-the-builder/briefs/brief-b.md`.

**Step 1: Deploy Brief A + Brief B workflow**
```powershell
python builder/build.py starter-v3/build-the-builder/briefs/brief-a.md starter-v3/build-the-builder/tools/openapi.json --extra-brief starter-v3/build-the-builder/briefs/brief-b.md --slot practice-b --deploy
```
Expected: `deployed_verified` status with Brief B `agent_id`.

**Step 2: Run PUB-11 (Three products, one date for all)**
```powershell
python starter-v3/build-the-builder/tools/run_cases.py <brief_b_agent_id> --brief B --only PUB-11 --cases starter-v3/build-the-builder/public-test-set.json
```
Expected: `PASS PUB-11`.

**Step 3: Inspect results and verify budget**
Verify remaining credits on workspace to ensure strictly under budget ceiling.
