"""Check committed history and index for local secrets without printing values."""
import re
import subprocess
import sys


def git(*args):
    return subprocess.check_output(["git", *args])


def forbidden_path(path):
    path = path.replace("\\", "/")
    parts = path.lower().split("/")
    if parts[0] in {"runs", "state", "handoff", ".venv"}:
        return True
    if any(part in {"__pycache__", ".idea", ".vscode"} for part in parts):
        return True
    name = parts[-1]
    return (name == ".env" or name.startswith(".env.") and name != ".env.example"
            or name.endswith(".local.env") or name in {"env.sh", ".freya-agents.json", ".personas.json"})


TOKEN = re.compile(rb"(?:\bfak_[A-Za-z0-9_-]{20,}|\bghp_[A-Za-z0-9]{20,}|\bgho_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}|\bsk-(?:proj-|ant-)[A-Za-z0-9_-]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)")
ASSIGNMENT = re.compile(rb"(?m)^[ \t]*(?:export[ \t]+)?(?:FREYA_API_KEY|FREYA_BANK_TEAM_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY)[ \t]*=[ \t]*[^\s#]+")


def check(path, data, findings):
    if forbidden_path(path):
        findings.add((path, "local path"))
    # The pinned, unmodified organizer kit contains documented sample assignments.
    if TOKEN.search(data) or (not path.startswith("starter-v3/") and ASSIGNMENT.search(data)):
        findings.add((path, "credential pattern"))


def main():
    findings = set()
    index = git("ls-files", "-z").split(b"\0")
    for raw in filter(None, index):
        path = raw.decode("utf-8", "replace")
        check(path, git("show", f":{path}"), findings)
    for entry in git("rev-list", "--objects", "--all").decode("utf-8", "replace").splitlines():
        oid, _, path = entry.partition(" ")
        if not path or git("cat-file", "-t", oid).strip() != b"blob":
            continue
        check(path, git("cat-file", "blob", oid), findings)
    for path, reason in sorted(findings):
        print(f"{reason}: {path}")
    print(f"Git safety: {'FAILED' if findings else 'passed'} ({len(index) - 1} indexed paths)")
    return bool(findings)


if __name__ == "__main__":
    sys.exit(main())
