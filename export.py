"""Exportiert das globale Claude-Code-Setup in dieses Repo.

Kopiert nur freigegebene Dateien aus ~/.claude und das DevOS-Paket, nie Anmeldedaten, Gesprächsverläufe oder
Caches. Bricht ab, bevor etwas geschrieben wird, wenn eine Datei nach einem Schlüssel oder Token aussieht.
Aufruf: python export.py
"""
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
HOME = Path.home()
CLAUDE = HOME / ".claude"
DEVOS = HOME / "Documents" / "DevOS" / "devos-claude-port"

# (Quelle, Ziel im Repo, Muster relativ zur Quelle; None = einzelne Datei)
PLAN = [
    (CLAUDE / "CLAUDE.md", "claude/CLAUDE.md", None),
    (CLAUDE / "settings.json", "claude/settings.json", None),
    (CLAUDE / "statusline.py", "claude/statusline.py", None),
    (CLAUDE / "agents", "claude/agents", ["*.md"]),
    (CLAUDE / "skills", "claude/skills", ["**/*"]),
    (CLAUDE / "learning", "claude/learning", ["ll.py", "llcore.py", "llgate.py", "llhooks.py", "llsearch.py",
                                             "lessons.jsonl", "config.json", "tests/test_learning_loop.py"]),
    (CLAUDE / "vendor", "claude/vendor", ["sync_agency_agents.py", "agency-agents.manifest.json",
                                         "agency-agents.selection.json"]),
    (CLAUDE / "vendor" / "agency-agents" / "LICENSE", "claude/vendor/agency-agents.LICENSE", None),
    (DEVOS, "extras/devos-claude-port", ["**/*"]),
]
PAYLOAD = ("claude", "extras")
NEVER = re.compile(r"(^|/)(\.credentials\.json|[^/]*\.db|state|gates|projects|__pycache__|[^/]*\.pyc|[^/]*\.tmp|\.git)(/|$)",
                   re.I)
SECRET = re.compile(
    r"sk-ant-[A-Za-z0-9_-]{10,}|\bsk-[A-Za-z0-9]{32,}|\bgh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|"
    r"xox[baprs]-[A-Za-z0-9-]{10,}|\bAKIA[0-9A-Z]{16}\b|"
    # nur eine Kopfzeile mit folgendem Schlüsselinhalt ist ein Schlüssel; die Kopfzeile allein ist ein Suchmuster
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----\s*[A-Za-z0-9+/=]{40,}|"
    r"\"(access|refresh|id)_?token\"\s*:\s*\"[^\"]{16,}\"")


def collect():
    files = {}
    for source, target, patterns in PLAN:
        if patterns is None:
            if source.is_file():
                files[target] = source
            continue
        if not source.is_dir():
            continue
        for pattern in patterns:
            for path in source.glob(pattern):
                rel = path.relative_to(source).as_posix()
                if path.is_file() and not NEVER.search(rel):
                    files["%s/%s" % (target, rel)] = path
    return files


def main():
    files = collect()
    hits = [target for target, source in files.items() if SECRET.search(source.read_bytes().decode("utf-8", "ignore"))]
    if hits:
        print("Abbruch, nichts exportiert. Diese Dateien sehen nach Schlüsseln oder Tokens aus:")
        print("\n".join("  " + hit for hit in hits))
        return 1
    for folder in PAYLOAD:  # Spiegel: exportierte Dateien entfernen, die es in der Quelle nicht mehr gibt
        root = REPO / folder
        for path in (root.rglob("*") if root.exists() else []):
            if path.is_file() and path.relative_to(REPO).as_posix() not in files:
                path.unlink()
    manifest = {}
    for target, source in sorted(files.items()):
        dest = REPO / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        manifest[target] = hashlib.sha256(dest.read_bytes()).hexdigest()
    data = {"source_home": HOME.as_posix(), "exported_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "files": manifest}
    (REPO / "setup-manifest.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("Exportiert: %d Dateien nach %s" % (len(files), REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
