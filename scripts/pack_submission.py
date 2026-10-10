"""One-click final submission packager for the Hackathon.

Executes both hidden brief builds with --deploy, gathers official workflow exports
and traces, populates submission.json with the exact Git commit, and packages the final bundle.
Standard library only (zero pip dependencies).
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def get_git_commit():
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True)
        return out.strip()
    except Exception:
        raise RuntimeError("Submission requires an exact Git commit") from None


def run_build(brief, api, slot, deploy=False, extra_brief=None):
    cmd = [sys.executable, str(ROOT / "builder" / "build.py"), str(brief), str(api), "--slot", slot]
    if extra_brief:
        cmd.extend(["--extra-brief", str(extra_brief)])
    if deploy:
        cmd.append("--deploy")
    print(f"[*] Running: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"Build failed for slot {slot}:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
    try:
        artifact = json.loads(proc.stdout.strip().splitlines()[-1])
        run_dir = Path(artifact["run_directory"])
    except Exception as exc:
        raise RuntimeError(f"Could not parse build artifact output for slot {slot}: {proc.stdout}") from exc
    result = json.loads((run_dir/'result.json').read_text(encoding='utf-8'))
    if result.get('status') != ('deployed_verified' if deploy else 'offline_validated'):
        raise RuntimeError('Build status is not valid for the requested packaging mode')
    return run_dir


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief-1", type=Path, help="Path to first final brief")
    parser.add_argument("--api-1", type=Path, help="Path to first final OpenAPI file")
    parser.add_argument("--brief-2", type=Path, help="Path to second final brief")
    parser.add_argument("--api-2", type=Path, help="Path to second final OpenAPI file")
    parser.add_argument("--team", default="Mirac Birlik & Mehmet Ali Mansuroglu", help="Team name")
    parser.add_argument("--repo", default="https://github.com/Mehmetalimans/freya-builder.git", help="GitHub repo URL")
    parser.add_argument("--deploy", action="store_true", help="Deploy to Freya and export platform workflows")
    parser.add_argument("--dry-run", action="store_true", help="Run practice verification using kit Brief A & B")
    args = parser.parse_args()
    if args.dry_run and args.deploy:
        parser.error('--dry-run is offline practice only; it cannot deploy final slots')
    if subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=ROOT,text=True).strip():
        parser.error('Commit source changes before packaging so the recorded commit is reproducible')

    if args.dry_run:
        kit = ROOT / "starter-v3" / "build-the-builder"
        args.brief_1 = kit / "briefs" / "brief-a.md"
        args.api_1 = kit / "tools" / "openapi.json"
        args.brief_2 = kit / "briefs" / "brief-a.md"
        args.api_2 = kit / "tools" / "openapi.json"
        extra_brief_2 = kit / "briefs" / "brief-b.md"
    else:
        if not (args.brief_1 and args.api_1 and args.brief_2 and args.api_2):
            parser.error("Either --dry-run or all four paths (--brief-1, --api-1, --brief-2, --api-2) must be supplied.")
        extra_brief_2 = None

    commit = get_git_commit()
    submission_dir = ROOT / "dist" / ('submission-' + uuid.uuid4().hex[:8])
    submission_dir.mkdir(parents=True, exist_ok=False)

    print(f"=== Hackathon Final Packager (Commit: {commit[:8]}) ===")

    # 1. Build Brief 1
    run_dir_1 = run_build(args.brief_1, args.api_1, "final-hidden-1", deploy=args.deploy)
    wf_file_1 = run_dir_1 / ("workflow.export.json" if args.deploy else "workflow.local.json")
    trace_file_1 = run_dir_1 / "trace.jsonl"
    if not wf_file_1.exists():
        raise FileNotFoundError(f"Missing workflow file: {wf_file_1}")
    shutil.copy2(wf_file_1, submission_dir / "hidden-1.workflow.json")
    shutil.copy2(trace_file_1, submission_dir / "hidden-1.trace.jsonl")

    # 2. Build Brief 2
    run_dir_2 = run_build(args.brief_2, args.api_2, "final-hidden-2", deploy=args.deploy, extra_brief=extra_brief_2)
    wf_file_2 = run_dir_2 / ("workflow.export.json" if args.deploy else "workflow.local.json")
    trace_file_2 = run_dir_2 / "trace.jsonl"
    if not wf_file_2.exists():
        raise FileNotFoundError(f"Missing workflow file: {wf_file_2}")
    shutil.copy2(wf_file_2, submission_dir / "hidden-2.workflow.json")
    shutil.copy2(trace_file_2, submission_dir / "hidden-2.trace.jsonl")

    # 3. Create populated submission.json
    submission_data = {
        "team": args.team,
        "repo": args.repo,
        "commit": commit,
        "run_command": "python builder/build.py {brief_path} {tool_api_path} --deploy --slot {brief_label}",
        "workflows": {
            "hidden-1": "hidden-1.workflow.json",
            "hidden-2": "hidden-2.workflow.json",
        },
        "traces": {
            "hidden-1": "hidden-1.trace.jsonl",
            "hidden-2": "hidden-2.trace.jsonl",
        },
        "status": "READY_FOR_SUBMISSION" if args.deploy else "PRACTICE_VALIDATED_NOT_DEPLOYED",
    }
    submission_json_path = submission_dir / "submission.json"
    submission_json_path.write_text(json.dumps(submission_data, indent=2) + "\n", encoding="utf-8")

    # 4. Create ZIP archive
    zip_path = ROOT / "dist" / f"{submission_dir.name}-{commit[:8]}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as arc:
        arc.write(submission_json_path, arcname="submission.json")
        arc.write(submission_dir / "hidden-1.workflow.json", arcname="hidden-1.workflow.json")
        arc.write(submission_dir / "hidden-1.trace.jsonl", arcname="hidden-1.trace.jsonl")
        arc.write(submission_dir / "hidden-2.workflow.json", arcname="hidden-2.workflow.json")
        arc.write(submission_dir / "hidden-2.trace.jsonl", arcname="hidden-2.trace.jsonl")

    sha256 = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    print("\n[+] SUCCESS! Final submission package ready:")
    print(f"    ZIP Archive: {zip_path}")
    print(f"    SHA-256:     {sha256}")
    print(f"    Commit:      {commit}")
    print(f"    Status:      {submission_data['status']}")
    print(json.dumps(submission_data, indent=2))


if __name__ == "__main__":
    main()
