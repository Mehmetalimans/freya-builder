"""Extract the source release, create a clean no-pip venv, test and compare builds."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import uuid
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def run(command, cwd, env):
    completed = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=120)
    if completed.returncode:
        raise RuntimeError(completed.stdout + completed.stderr)
    return completed


def main():
    latest = json.loads((ROOT / "dist/latest.json").read_text(encoding="utf-8"))
    archive = ROOT / "dist" / latest["archive"]
    if hashlib.sha256(archive.read_bytes()).hexdigest() != latest["sha256"]:
        raise RuntimeError("Archive checksum mismatch")
    clean = (ROOT / "dist" / ("clean-" + uuid.uuid4().hex[:8])).resolve()
    clean.mkdir()
    with zipfile.ZipFile(archive) as bundle:
        for item in bundle.infolist():
            if not (clean / item.filename).resolve().is_relative_to(clean):
                raise RuntimeError("Archive traversal")
        bundle.extractall(clean)
    manifest = json.loads((clean / "MANIFEST.json").read_text())
    for name, sha in manifest["files"].items():
        if hashlib.sha256((clean / name).read_bytes()).hexdigest() != sha:
            raise RuntimeError("Source checksum mismatch")
    env = {k: v for k, v in os.environ.items() if not (k.startswith("FREYA_") or k in {"ANTHROPIC_API_KEY", "OPENAI_API_KEY", "PYTHONPATH"})}
    env["PYTHONUTF8"] = "1"
    run([sys.executable, "-m", "venv", "--without-pip", str(clean / ".venv")], clean, env)
    python = clean / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    tests = run([str(python), "-m", "unittest", "discover", "-s", "tests", "-v"], clean, env)
    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)
    (report_dir / "unit-tests.txt").write_text(tests.stdout + tests.stderr, encoding="utf-8", newline="\n")
    cases = {}
    for brief in ("A", "B"):
        hashes, times = [], []
        for _ in range(2):
            command = [str(python), "builder/build.py", "starter-v3/build-the-builder/briefs/brief-a.md",
                       "starter-v3/build-the-builder/tools/openapi.json", "--slot", "practice-" + brief.lower()]
            if brief == "B": command.extend(["--extra-brief", "starter-v3/build-the-builder/briefs/brief-b.md"])
            start = time.monotonic()
            built = run(command, clean, env)
            artifact = json.loads(built.stdout)
            folder = Path(artifact["run_directory"])
            result = json.loads((folder / "result.json").read_text(encoding="utf-8"))
            if result["status"] != "offline_validated" or result["benchmark_success"] is not None:
                raise RuntimeError("Offline status/score invariant failed")
            hashes.append(result["workflow_sha256"])
            times.append(round(time.monotonic()-start, 4))
        if hashes[0] != hashes[1]: raise RuntimeError("Non-deterministic build")
        cases[brief] = {"repeat_workflow_hash_equal": True, "workflow_sha256": hashes[0], "wall_seconds": times}
    report = {"verified_at_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
              "platform": platform.platform(), "archive": latest, "verified_source_files": len(manifest["files"]),
              "clean_venv_without_pip": True, "third_party_dependencies": 0, "credential_environment_cleared": True,
              "unit_test_exit_code": tests.returncode, "offline_builds": cases, "freya_requests": 0,
              "model_calls": 0, "cost_usd": 0, "benchmark_pass_rate": None,
              "live_api_validation": "not_run", "holdout_behavioral_evaluation": "not_run", "clean_directory": str(clean)}
    (report_dir / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report))


if __name__ == "__main__": main()
