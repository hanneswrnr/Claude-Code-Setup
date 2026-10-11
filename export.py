"""Exportiert das globale Claude-Code-Setup in dieses Repo.

Kopiert nur freigegebene Dateien aus ~/.claude, das automatische Gedächtnis aller Projekte, die GSD-Einstellung
und das DevOS-Paket, nie Anmeldedaten, Gesprächsverläufe oder Caches. Bricht ab, bevor etwas geschrieben wird,
wenn eine Datei oder die erzeugte Übersicht WISSEN.md nach einem Schlüssel oder Token aussieht.
Aufruf: python export.py [--behalten]
  --behalten  Gedächtnis-Dateien, die nur im Repo liegen (etwa von einem anderen Gerät), nicht löschen.
"""
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

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
    (HOME / ".gsd" / "defaults.json", "gsd/defaults.json", None),  # resolve_model_ids: GSD-Agents laufen auf Opus
]
PAYLOAD = ("claude", "extras", "memory", "gsd")
# synced: Skills, die die Desktop-App je Sitzung aus dem claude.ai-Konto hineinkopiert
NEVER = re.compile(r"(^|/)(\.credentials\.json|[^/]*\.db|state|gates|projects|synced|__pycache__|[^/]*\.pyc|[^/]*\.tmp|\.git)(/|$)",
                   re.I)
SECRET = re.compile(
    r"sk-ant-[A-Za-z0-9_-]{10,}|\bsk-[A-Za-z0-9]{32,}|\bsk-proj-[A-Za-z0-9_-]{20,}|"
    r"\bgh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|"
    r"xox[baprs]-[A-Za-z0-9-]{10,}|\bAKIA[0-9A-Z]{16}\b|\bAIza[0-9A-Za-z_-]{35}|"
    r"\b(sk|rk)_(live|test)_[A-Za-z0-9]{16,}|\bsb_secret_[A-Za-z0-9_-]{20,}|\bnpm_[A-Za-z0-9]{36}|"
    r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}|"
    r"hooks\.slack\.com/services/T[A-Za-z0-9]+/B[A-Za-z0-9]+/[A-Za-z0-9]+|"
    r"\bwhsec_[A-Za-z0-9+/=]{24,}|\bsbp_[a-f0-9]{40}\b|\bGOCSPX-[A-Za-z0-9_-]{28}\b|\b\d{8,10}:AA[A-Za-z0-9_-]{33}\b|"
    r"\bSG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}\b|\bglpat-[A-Za-z0-9_-]{20,}|\bdop_v1_[a-f0-9]{64}\b|"
    r"\bxkeysib-[a-f0-9]{64}-[A-Za-z0-9]{16}\b|\bre_[A-Za-z0-9]{8,}_[A-Za-z0-9]{16,}\b|"
    # Zugangsdaten in Adressen wie schema://nutzer:passwort@, aber keine Platzhalter wie <passwort>, ${VAR}, password
    # oder den lokalen Supabase-Standard postgres:postgres@
    r"\b[A-Za-z][A-Za-z0-9+.-]*://[^\s:/?#@\"'`]*:"
    r"(?!(?i:password|passwort|pass|secret|changeme|postgres|your[-_]?password|dein[-_]?passwort|x+|\*+)@)"
    r"[^\s/?#@\"'`<>\[\]{}]{8,}@|"
    # nur eine Kopfzeile mit folgendem Schlüsselinhalt ist ein Schlüssel; die Kopfzeile allein ist ein Suchmuster.
    # (?:\s|\\n)* erfasst auch JSON-Dateien von Google-Dienstkonten mit wörtlichem \n
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----(?:\s|\\n)*[A-Za-z0-9+/=]{40,}|"
    r"\"(access|refresh|id)_?token\"\s*:\s*\"[^\"]{16,}\"")
# Erlaubte Einzeltreffer als (Ziel im Repo, SHA-256 des Treffertexts): bekannte Lehrbeispiele in fremden
# Agent-Beschreibungen. Ein anderer Treffer in derselben Datei blockiert weiterhin.
ALLOW = {
    ("claude/agents/security-secrets-credential-engineer.md", "eb8b7d825e385b16cf41264e1bddc6d3d854b422b96d3f8b6cf6fde2b9425115"),
}
KIND_DE = {"mistake": "Fehler vermeiden", "success": "Bewährt", "preference": "Vorliebe"}  # wie in learning/llcore.py
SCRATCH = re.compile(r"scratch-workspaces-.*-scratch-(\d{4})-(\d\d)-(\d\d)-([0-9a-f]+)$")
MARKUP = re.compile(r"(`[^`]+`)|[\\`*<\[\]]|(?<![A-Za-z0-9])_|_(?![A-Za-z0-9])")


def slug(path):
    """Ordnername, den Claude Code für einen Projektpfad anlegt: C:/Users/hanne -> C--Users-hanne."""
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def short(name, home):
    """Projekt-Slug ohne den Slug des Benutzerordners, damit die Pfade im Repo kurz bleiben."""
    if name.lower() == home.lower():
        return "_home"
    return name[len(home) + 1:] if name.lower().startswith(home.lower() + "-") else name


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
    names, seen, home = {}, {}, slug(HOME.as_posix())
    for folder in sorted((CLAUDE / "projects").glob("*/memory")):  # Gedächtnis je Projekt, ohne Gesprächsverläufe
        found = {path.relative_to(folder).as_posix(): path for path in folder.rglob("*") if path.is_file()}
        found = {rel: path for rel, path in found.items() if not NEVER.search(rel)}
        if not found:
            continue
        name = folder.parent.name
        kurz = short(name, home)
        if kurz.lower() in seen:
            raise SystemExit("Abbruch, nichts exportiert: %s und %s ergeben beide memory/%s" % (seen[kurz.lower()], name, kurz))
        seen[kurz.lower()], names[kurz] = name, name
        files.update(("memory/%s/%s" % (kurz, rel), path) for rel, path in found.items())
    return files, names


def blocked(target, data):
    """True, wenn der Inhalt einen Geheimnis-Treffer enthält, der nicht in ALLOW steht."""
    text = data.decode("utf-8", "ignore")
    return any((target, hashlib.sha256(m[0].encode("utf-8")).hexdigest()) not in ALLOW for m in SECRET.finditer(text))


def md(text):
    """Einzeilig und ohne ungewollte Markdown-Formatierung; Code in Backticks bleibt Code."""
    return MARKUP.sub(lambda m: m[1] or "\\" + m[0], " ".join(str(text).split()))


def summary(data):
    """description: aus dem Frontmatter, sonst die erste Textzeile."""
    lines = data.decode("utf-8", "ignore").splitlines()
    if lines and lines[0].strip() == "---":
        end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), len(lines))
        for line in lines[1:end]:
            if line.startswith("description:"):
                value = line[len("description:"):].strip()
                try:
                    return json.loads(value) if value.startswith('"') else value.strip("'")
                except ValueError:
                    return value.strip('"')
        lines = lines[end + 1:]
    return next((line.strip("# \t") for line in lines if line.strip("# \t")), "")


def rule(lesson, why=True):
    line = "- " + md(lesson.get("rule", ""))
    if why and lesson.get("why"):
        line += " *Warum: %s*" % md(lesson["why"])
    line += " `%s`" % lesson.get("id", "")
    scope = lesson.get("scope", "global")
    return line + (" (nur %s)" % md(scope.replace("project:", "Projekt ")) if scope != "global" else "")


def grouped(lessons):
    order = list(KIND_DE)
    kinds = sorted({l.get("kind", "") for l in lessons}, key=lambda k: (order.index(k) if k in order else len(order), k))
    out = []
    for kind in kinds:
        items = sorted((l for l in lessons if l.get("kind", "") == kind), key=lambda l: l.get("id", ""))
        out += ["", "### %s (%d)" % (KIND_DE.get(kind) or md(kind), len(items)), ""] + [rule(l) for l in items]
    return out


def knowledge(contents, names):
    """Lesbare Übersicht über gelernte Regeln und das Gedächtnis je Projekt, aus den bereits gelesenen Inhalten."""
    rows = contents.get("claude/learning/lessons.jsonl", b"").decode("utf-8").splitlines()
    lessons = [json.loads(row) for row in rows if row.strip()]
    by_status = {s: [l for l in lessons if l.get("status") == s] for s in ("active", "candidate", "archived")}
    notes = {}
    for target in sorted(contents):
        if target.startswith("memory/"):
            kurz, rel = target[len("memory/"):].split("/", 1)
            notes.setdefault(kurz, []).append((rel, target))
    count = sum(1 for items in notes.values() for rel, _ in items if rel != "MEMORY.md")
    out = ["# Gesammeltes Wissen", "", "Automatisch erzeugt von export.py, nicht von Hand bearbeiten.", "",
           "- Aktive Regeln: %d" % len(by_status["active"]), "- Warten auf Freigabe: %d" % len(by_status["candidate"]),
           "- Archivierte Regeln: %d" % len(by_status["archived"]), "- Gedächtnis-Notizen: %d" % count,
           "- Projekte und Sitzungen mit Gedächtnis: %d" % len(names), "", "## Gelernte Regeln (Lernloop)"]
    out += grouped(by_status["active"]) + ["", "## Wartet auf Freigabe (/reflect)"]
    out += grouped(by_status["candidate"]) or ["", "Keine."]
    out += ["", "## Archiviert", "", "<details>", "<summary>%d archivierte Regeln anzeigen</summary>" % len(
        by_status["archived"]), ""]
    out += [rule(l, why=False) for l in sorted(by_status["archived"], key=lambda l: l.get("id", ""))]
    out += ["", "</details>", "", "## Gedächtnis je Projekt"]
    def order(kurz):  # erst Projekte nach Name, dann Sitzungen ohne Projektordner nach Datum und Kennung
        m = SCRATCH.search(kurz)
        return (1, m[1] + m[2] + m[3], m[4]) if m else (0, kurz.lower())

    for kurz in sorted(notes, key=order):
        m = SCRATCH.search(kurz)
        title = "Sitzung ohne Projektordner vom %s.%s.%s (%s)" % (m[3], m[2], m[1], m[4]) if m else md(kurz)
        items = [(rel, target) for rel, target in notes[kurz] if rel != "MEMORY.md"]
        out += ["", "### " + title, ""]
        out += ["- [%s](%s) – %s" % (md(Path(rel).stem), quote(target), md(summary(contents[target])))
                for rel, target in items] or ["Nur eine Übersicht: [MEMORY.md](%s)" % quote("memory/%s/MEMORY.md" % kurz)]
    return "\n".join(out) + "\n"


def main():
    keep = "--behalten" in sys.argv[1:]
    unknown = [a for a in sys.argv[1:] if a != "--behalten"]
    if unknown:
        print("Unbekannte Option: %s (erlaubt: --behalten)" % " ".join(unknown))
        return 2
    files, names = collect()
    contents = {target: source.read_bytes() for target, source in files.items()}  # jede Quelle genau einmal lesen
    if keep:  # Gedächtnis, das nur das Repo hat (etwa von einem anderen Gerät), nicht löschen
        old = json.loads((REPO / "setup-manifest.json").read_text(encoding="utf-8")) if (REPO / "setup-manifest.json").is_file() else {}
        for target in old.get("files", {}):
            kurz = target[len("memory/"):].split("/", 1)[0]
            if target.startswith("memory/") and target not in contents and (REPO / target).is_file():
                contents[target] = (REPO / target).read_bytes()
                if kurz not in names and kurz in old.get("memory", {}):
                    names[kurz] = old["memory"][kurz]
    wissen = knowledge(contents, names).encode("utf-8")
    hits = [target for target, data in contents.items() if blocked(target, data)]
    hits += ["WISSEN.md"] if blocked("WISSEN.md", wissen) else []
    if hits:
        print("Abbruch, nichts exportiert. Diese Dateien sehen nach Schlüsseln oder Tokens aus:")
        print("\n".join("  " + hit for hit in sorted(hits)))
        return 1
    removed = {}
    for folder in PAYLOAD:  # Spiegel: exportierte Dateien entfernen, die es in der Quelle nicht mehr gibt
        root = REPO / folder
        for path in (root.rglob("*") if root.exists() else []):
            if path.is_file() and path.relative_to(REPO).as_posix() not in contents:
                path.unlink()
                removed[folder] = removed.get(folder, 0) + 1
    manifest = {}
    for target, data in sorted(contents.items()):
        dest = REPO / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        manifest[target] = hashlib.sha256(data).hexdigest()
    meta = {"source_home": HOME.as_posix(), "exported_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "memory": dict(sorted(names.items())), "files": manifest}
    (REPO / "setup-manifest.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (REPO / "WISSEN.md").write_bytes(wissen)
    if removed:
        print("Aus dem Repo entfernt, weil in der Quelle nicht mehr vorhanden: "
              + ", ".join("%s %d" % item for item in removed.items()))
    print("Exportiert: %d Dateien nach %s, dazu WISSEN.md" % (len(contents), REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
