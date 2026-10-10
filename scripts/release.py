"""Create a deterministic source archive from an explicit allowlist (no secrets)."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from builder import __version__


def files():
    result = []
    for folder in ("builder", "tests", "scripts", "docs", "starter-v3"):
        result.extend(p for p in (ROOT / folder).rglob("*") if p.is_file()
                      and not set(p.relative_to(ROOT).parts) & {"__pycache__", "results", "traces", "freya_docs"}
                      and p.suffix in {".py", ".md", ".json"})
    result.extend(ROOT / name for name in ("README.md", "AGENTS.md", ".env.example", "requirements.lock", ".python-version", ".gitignore", ".gitattributes", "budget.json",
        "submission.template.json", "starter-v3/build-the-builder/VERSION", "starter-v3/build-the-builder/env.example"))
    result.extend(p for p in (ROOT / ".github").rglob("*") if p.is_file() and p.suffix in {".md", ".yml", ".yaml"})
    result.extend(ROOT / "evidence" / name for name in ("hackathon.txt", "build-the-builder-v3.zip"))
    return sorted(set(result))


def main():
    entries = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in files()}
    manifest = {"builder_version": __version__, "python": "3.12.14", "status": "offline_baseline_not_final_submission",
                "files": {name: hashlib.sha256(data).hexdigest() for name, data in entries.items()}}
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    fingerprint = hashlib.sha256(manifest_bytes).hexdigest()[:12]
    dest = ROOT / "dist"
    dest.mkdir(exist_ok=True)
    target = dest / f"freya-builder-{__version__}-{fingerprint}.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in {**entries, "MANIFEST.json": manifest_bytes}.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 10, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    sha = hashlib.sha256(target.read_bytes()).hexdigest()
    (dest / "latest.json").write_text(json.dumps({"archive": target.name, "sha256": sha, "manifest_fingerprint": fingerprint}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"archive": str(target), "sha256": sha, "source_files": len(entries)}))


if __name__ == "__main__": main()
