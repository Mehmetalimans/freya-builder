"""Prepare/score an official public case for a manual Freya UI integration test.

This does not start a Freya call or claim an official judge result. Private session
data stays in ignored state/ and runs/. The seven development cases alone are allowed.
"""
import argparse
import html
import json
import os
from pathlib import Path
import secrets
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "starter-v3" / "build-the-builder"
sys.path[:0] = [str(KIT), str(KIT / "tools")]
from run_cases import persona_for
from score import http, score_ledger


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["prepare", "score"])
    ap.add_argument("run", type=Path)
    ap.add_argument("--case", default="PUB-01", choices=[f"PUB-{i:02d}" for i in range(1, 8)])
    args = ap.parse_args()
    keyfile = ROOT / "state" / "browser-bank-team-key"
    keyfile.parent.mkdir(exist_ok=True)
    if not keyfile.exists():
        keyfile.write_text(secrets.token_urlsafe(32), encoding="utf-8")
    os.environ["FREYA_BANK_TEAM_KEY"] = keyfile.read_text(encoding="utf-8").strip()
    cases = json.loads((KIT / "public-test-set.json").read_text(encoding="utf-8"))
    case = next(c for c in cases if c["id"] == args.case)
    args.run.mkdir(parents=True, exist_ok=True)
    session_path = args.run / "browser-session.private.json"
    if args.action == "prepare":
        if session_path.exists():
            raise SystemExit("A session already exists here; do not accidentally replace it.")
        response = http("/v1/practice/sessions", {"case": args.case})
        if "variables" not in response:
            raise SystemExit("Bank did not return session variables; no Freya call started.")
        data = {"case": args.case, "prepared_at": time.time(), "variables": response["variables"],
                "persona": persona_for(case, {"identity": case["identity"]})}
        session_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        # A temporary localhost page lets browser automation transfer the exact
        # supplied persona through visible UI without accessing browser credentials.
        (args.run / "case-transfer.html").write_text(
            "<!doctype html><meta charset=utf-8><title>Local official practice case</title><pre>"
            + html.escape(json.dumps(data, indent=2)) + "</pre>", encoding="utf-8")
        print(json.dumps({"status": "prepared", "case": args.case, "freya_calls_started": 0}))
    else:
        session = json.loads(session_path.read_text(encoding="utf-8"))
        if session["case"] != args.case:
            raise SystemExit("Case does not match the prepared session")
        ledger = http("/v1/practice/ledger/" + session["variables"]["customer_id"])
        if "calls" not in ledger:
            raise SystemExit("Bank did not return a ledger")
        verdict = score_ledger(case, ledger)
        report = {"mode": "browser_integration", "case": args.case,
                  "ledger_pass": verdict["pass"], "ledger_failures": verdict["failed"],
                  "official_judge_pass": None, "benchmark_success": None,
                  "tools": [c["tool"] for c in ledger["calls"]],
                  "tool_errors": [c["result"].get("error") for c in ledger["calls"] if c["result"].get("error")],
                  "freya_cost_usd": None, "external_model_cost_usd": 0}
        (args.run / "browser-ledger.private.json").write_text(json.dumps(ledger, indent=2), encoding="utf-8")
        (args.run / "browser-smoke-result.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report))


if __name__ == "__main__":
    main()
