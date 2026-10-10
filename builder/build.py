"""python builder/build.py BRIEF TOOL_API [--extra-brief ...] [--deploy]."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import time
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from builder import __version__
from builder.core import ContractError, compile_workflow, digest, canonical
from builder.runtime import ROOT, Trace, check_environment, exclusive, official_client, verify_readback, write_json, utc_now


def deploy_workflow(client, slot, workflow, state_file, export_path):
    client.validate_workflow(slot, workflow)
    saved = client.save_workflow(slot, workflow, state_file=str(state_file))
    # The starter fixes the phone model and publishes on UPDATE. Do this on first create too.
    if "version" not in saved:
        saved["version"] = client.update_workflow(saved["workflow_id"], workflow)
    client.export_workflow(saved["workflow_id"], str(export_path))
    exported = json.loads(export_path.read_text(encoding="utf-8"))
    verify_readback(workflow, exported)
    return saved


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    parser.add_argument("tool_api", type=Path)
    parser.add_argument("--extra-brief", type=Path, action="append", default=[])
    parser.add_argument("--deploy", action="store_true", help="Validate, save, publish and export on Freya (requires local credentials)")
    parser.add_argument("--slot", default="baseline", help="Stable workflow slot; do not change it for every revision")
    parser.add_argument("--output", type=Path, default=ROOT / "runs")
    parser.add_argument("--max-seconds", type=int, default=1800)
    parser.add_argument("--test-brief", choices=["A", "B"], help="Run bounded official practice evaluation after deployment")
    parser.add_argument("--split", default="dev", choices=["dev", "holdout"])
    parser.add_argument("--reps", type=int, default=1, choices=[1, 3])
    args = parser.parse_args(argv)
    if not 1 <= args.max_seconds <= 1800 or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", args.slot):
        parser.error("max-seconds must be 1..1800 and slot a simple label")
    if args.test_brief and not args.deploy:
        parser.error("--test-brief requires --deploy")
    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-" + uuid.uuid4().hex[:8]
    out = args.output.resolve() / run_id
    out.mkdir(parents=True, exist_ok=False)
    trace = Trace(out / "trace.jsonl")
    start = time.monotonic()
    result = {"builder_version": __version__, "run_id": run_id, "started_at": utc_now(), "status": "failed",
              "mode": "live" if args.deploy else "offline", "benchmark_success": None,
              "builder_model_calls": 0, "builder_model_cost_usd": 0,
              "platform_cost_usd": None if args.deploy else 0, "tests": "not_run"}
    trace.emit("start", version=__version__, mode=result["mode"], strategy="lossless_policy_template_v1")
    try:
        briefs = []
        for path in [args.brief, *args.extra_brief]:
            raw = path.read_bytes()
            if len(raw) > 1_000_000: raise ContractError("Brief exceeds local 1 MB input guard")
            text = raw.decode("utf-8-sig")
            briefs.append((path.name, text))
            trace.emit("input", name=path.name, sha256=digest(raw), bytes=len(raw))
        raw = args.tool_api.read_bytes()
        if len(raw) > 2_000_000: raise ContractError("OpenAPI exceeds local 2 MB input guard")
        document = json.loads(raw.decode("utf-8-sig"))
        trace.emit("input", name=args.tool_api.name, sha256=digest(raw), bytes=len(raw))
        workflow, analysis = compile_workflow(briefs, document)
        write_json(out / "workflow.local.json", workflow)
        write_json(out / "analysis.json", analysis)
        result.update(workflow_sha256=digest(canonical(workflow)), nodes=len(workflow["nodes"]), tools=7)
        trace.emit("compiled", **{k: result[k] for k in ("workflow_sha256", "nodes", "tools")}, identity_gate=analysis["identity_gate"])
        if time.monotonic() - start >= args.max_seconds: raise TimeoutError("Builder time limit reached")
        if args.deploy:
            check_environment()
            scope = digest(os.environ["FREYA_WORKSPACE_ID"])[:16]
            with exclusive(ROOT / "state" / f"{scope}.lock"):
                client = official_client(start + args.max_seconds, trace)
                saved = deploy_workflow(client, args.slot, workflow, ROOT / "state" / f"{scope}.json", out / "workflow.export.json")
                result.update({"workflow_id": saved["workflow_id"], "agent_id": saved["agent_id"],
                               "platform_version": saved.get("version")})
                trace.emit("deployed", **saved, nodes=result["nodes"], tools=result["tools"])
            result["status"] = "deployed_verified"
            if args.test_brief:
                from builder.evaluate import main as evaluate
                remaining = int(args.max_seconds - (time.monotonic() - start))
                if remaining <= 0: raise TimeoutError("Builder time limit reached before evaluation")
                write_json(out / "result.json", result)
                code = evaluate([str(out), "--brief", args.test_brief, "--split", args.split,
                                 "--reps", str(args.reps), "--max-seconds", str(remaining)])
                measured = json.loads((out / "evaluation.json").read_text(encoding="utf-8"))
                result["tests"] = measured["status"]
                result["benchmark_success"] = measured["benchmark_success"]
                trace.emit("evaluation", status=measured["status"], success=measured["benchmark_success"],
                           reserved_upper_bound_usd=measured.get("reserved_upper_bound_usd"),
                           actual_cost_usd=measured.get("actual_cost_usd"))
                if code: raise ContractError("Requested evaluation did not complete; deployment export is preserved")
        else:
            result["status"] = "offline_validated"
            trace.emit("platform_validation", status="not_run", reason="offline_mode")
        if not args.test_brief: trace.emit("benchmark", status="not_run", success=None)
    except Exception as error:
        # Avoid exception text: file paths/server responses can carry secrets.
        result["status"] = "failed"
        result["error_type"] = type(error).__name__
        if isinstance(error, ContractError): result["error"] = str(error)
        trace.emit("failed", error_type=type(error).__name__)
    finally:
        result["ended_at"] = utc_now()
        result["seconds"] = round(time.monotonic() - start, 3)
        write_json(out / "result.json", result)
        trace.emit("end", status=result["status"], seconds=result["seconds"], builder_model_calls=0,
                   builder_model_cost_usd=0, platform_cost_usd=result["platform_cost_usd"])
    print(json.dumps({"status": result["status"], "run_directory": str(out),
                      "error": result.get("error"), "error_type": result.get("error_type")}, ensure_ascii=False))
    return 0 if result["status"] != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
