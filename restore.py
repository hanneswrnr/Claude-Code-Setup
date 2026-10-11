"""Stellt das Claude-Code-Setup aus diesem Repo auf einem Gerät wieder her.

Kopiert die Dateien nach ~/.claude, das Gedächtnis nach ~/.claude/projects/<projekt>/memory, die GSD-Einstellung
nach ~/.gsd und das DevOS-Paket nach ~/Documents/DevOS, prüft vorher jede Prüfsumme und Pfadlänge, sichert alles,
was überschrieben würde, und ersetzt den Benutzerordner des Export-Geräts durch den dieses Geräts.
Agency Agents aus abgewählten Bereichen werden entfernt, wenn sie auf dem Gerät unverändert sind (mit Sicherung).
Gedächtnis aus Sitzungen ohne Projektordner bleibt nur im Repo, weil Claude es auf anderen Geräten nicht lädt.
Lektionen werden zusammengeführt statt ersetzt, neuere Gedächtnis-Notizen dieses Geräts bleiben erhalten.
--zurueckholen ORDNER holt Lektionen und Gedächtnis aus einer älteren Sicherung (restore-backup-…) zurück.
Aufruf: python restore.py [--dry-run] [--home ORDNER] [--zurueckholen ORDNER]
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path, PureWindowsPath

REPO = Path(__file__).resolve().parent
TEXT = {".md", ".json", ".jsonl", ".py", ".txt", ".toml", ".yaml", ".yml", ".ps1", ".sh", ".html", ".cfg", ".ini"}
SCRATCH = re.compile(r"scratch-workspaces-.*-scratch-\d{4}-\d\d-\d\d-[0-9a-f]+$")  # Sitzungen ohne Projektordner


def unsafe(rel):
    """Manifest-Pfad, der aus dem Zielordner herausführen könnte: absolut, leere Teile, . oder .., Laufwerksangaben"""
    parts = rel.replace("\\", "/").split("/")
    return (bool(PureWindowsPath(rel).drive) or rel[:1] in ("", "/", "\\")
            or any(p in ("", ".", "..") or ":" in p for p in parts))


def long_paths_enabled():
    """Unter Windows: ist LongPathsEnabled in der Registry auf 1 gesetzt? Lesefehler gelten als aus."""
    if os.name != "nt":
        return True
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\FileSystem") as key:
            return winreg.QueryValueEx(key, "LongPathsEnabled")[0] == 1
    except OSError:
        return False


def slug(path):
    """Ordnername, den Claude Code für einen Projektpfad anlegt: C:/Users/hanne -> C--Users-hanne."""
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def project(name, old, new):
    """Projekt-Slug des Export-Geräts auf den Benutzerordner dieses Geräts umstellen."""
    if name.lower() == old.lower() or name.lower().startswith(old.lower() + "-"):
        return new + name[len(old):]
    return name


def rewrite(text, old, new):
    old_p, new_p = old.replace("\\", "/"), new.replace("\\", "/")
    old_w = old_p.replace("/", "\\")
    new_w = new_p.replace("/", "\\") if os.name == "nt" else new_p
    json_new = new_w.replace("\\", "\\\\")
    for before, after in ((old_w.replace("\\", "\\\\"), json_new), (old_w, new_w), (old_p, new_p)):
        text = text.replace(before, after)
    return text


def retired_agents(home, manifest):
    """Agency Agents aus Bereichen, die die Auswahl im Repo ausschließt, die dieses Gerät aber noch unverändert hat.

    Grundlage ist das Agency-Manifest des Geräts vor dem Einspielen: Entfernt werden nur Dateien, die das Sync-Skript
    dort selbst installiert hat, die seitdem nicht verändert wurden und deren Bereich die Auswahl im Repo-Manifest
    abwählt (--exclude oder nicht in --only). Eigene Agents und neuere Agents aus noch gewählten Bereichen bleiben.
    """
    def load(path):
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            return {}
        return data if isinstance(data, dict) else {}

    old = load(home / ".claude" / "vendor" / "agency-agents.manifest.json").get("files")
    repo = load(REPO / "claude" / "vendor" / "agency-agents.manifest.json")
    new, selection = repo.get("files"), repo.get("selection")
    if not isinstance(old, dict) or not isinstance(new, dict) or not isinstance(selection, dict):
        return [], []
    only, exclude = selection.get("only") or [], selection.get("exclude") or []
    retire, kept = [], []
    for fname, entry in sorted(old.items()):
        if not isinstance(entry, dict) or not isinstance(entry.get("source"), str):
            continue
        division = entry["source"].split("/")[0]
        if not (division in exclude or (only and division not in only)):
            continue
        target = home / ".claude" / "agents" / fname
        if fname in new or "claude/agents/" + fname in manifest["files"] or unsafe(fname) or not target.is_file():
            continue
        if hashlib.sha256(target.read_bytes()).hexdigest() == entry.get("sha256"):
            retire.append(target)
        else:
            kept.append(target)
    return retire, kept


def lesson_rows(data):
    """(Kennung, Zeile) je Lektion; None, wenn eine Zeile kein gültiges JSON mit Kennung ist."""
    rows = []
    for line in data.decode("utf-8-sig", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            rows.append((str(entry["id"]), line, str(entry.get("updated") or entry.get("created") or "")))
        except (ValueError, KeyError, TypeError):
            return None
    return rows


def merge_lessons(local, repo):
    """Lektionen beider Stände: jede Kennung einmal, bei doppelten die zuletzt geänderte Fassung (bei Gleichstand
    die des Repos); Lektionen, die nur lokal existieren, bleiben am Ende erhalten. Unlesbares lokal: Repo-Stand."""
    mine, theirs = lesson_rows(local), lesson_rows(repo)
    if mine is None or theirs is None:
        return repo
    newline = "\r\n" if b"\r\n" in repo else "\n"
    by_id = {lid: (line, stamp) for lid, line, stamp in mine}
    out, seen = [], set()
    for lid, line, stamp in theirs:
        other = by_id.get(lid)
        out.append(other[0] if other and other[1] > stamp else line)
        seen.add(lid)
    out += [line for lid, line, _ in mine if lid not in seen]
    return (newline.join(out) + newline).encode("utf-8")


def modified(data):
    """modified: aus dem Frontmatter einer Gedächtnis-Notiz, sonst leer."""
    text = data.decode("utf-8", errors="replace")
    if not text.lstrip("\ufeff").startswith("---"):
        return ""
    head = text.split("---", 2)[1] if text.count("---") >= 2 else ""
    m = re.search(r"^\s*modified:\s*(\S+)", head, re.M)
    return m.group(1) if m else ""


def merge_memory(name, local, repo):
    """Gedächtnis-Datei beider Stände -> (Ergebnis, Konflikt). MEMORY.md: Repo-Zeilen plus lokale Einträge mit
    anderem Ziel. Notizen: die nach modified neuere; ohne Zeitstempel die Fassung, die die andere vollständig enthält.
    Sonst gilt das Repo und der Konflikt wird gemeldet."""
    if local == repo:
        return repo, False
    lines = lambda data: [l.rstrip("\r") for l in data.decode("utf-8", errors="replace").split("\n")]
    if name == "MEMORY.md":
        key = lambda line: (re.search(r"\]\(([^)]+)\)", line) or [None, line.strip()])[1]
        ours = lines(repo)
        keys = {key(l) for l in ours if l.strip()}
        extra = [l for l in lines(local) if l.strip() and key(l) not in keys]
        if not extra:
            return repo, False
        newline = "\r\n" if b"\r\n" in repo else "\n"
        while ours and not ours[-1].strip():
            ours.pop()
        return (newline.join(ours + extra) + newline).encode("utf-8"), False
    mine, theirs = modified(local), modified(repo)
    if mine and theirs:
        return (local if mine > theirs else repo), False
    a, b = set(lines(local)), set(lines(repo))
    if a >= b:
        return local, False
    if b >= a:
        return repo, False
    return repo, True


def recover(home, folder, dry_run):
    """Holt Lektionen und Gedächtnis aus einem restore-backup-Ordner zurück, ohne den aktuellen Stand zu verlieren."""
    src_root = folder / ".claude"
    if not src_root.is_dir():
        print("Abbruch, nichts geändert: %s enthält keinen Ordner .claude" % folder)
        return 1
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    safety = home / ".claude" / ("restore-backup-" + stamp + "-vor-zurueckholen")
    conflicts = home / ".claude" / ("restore-konflikte-" + stamp)
    writes, conflict_files, untouched, removed_agents = [], [], [], 0
    for path in sorted(p for p in src_root.rglob("*") if p.is_file()):
        rel = path.relative_to(src_root)
        dest = home / ".claude" / rel
        old = path.read_bytes()
        now = dest.read_bytes() if dest.is_file() else None
        parts = rel.parts
        if rel.as_posix() == "learning/lessons.jsonl":
            merged = merge_lessons(old, now) if now is not None else old
            conflict = False
        elif len(parts) >= 4 and parts[0] == "projects" and parts[2] == "memory":
            merged, conflict = merge_memory(rel.name, old, now) if now is not None else (old, False)
        elif parts[0] == "agents" and now is None:
            removed_agents += 1  # bewusst entfernte Agency Agents bleiben entfernt
            continue
        else:
            if now != old:
                untouched.append(rel.as_posix())
            continue
        if conflict:
            conflict_files.append((rel, old))
        if merged != now:
            writes.append((rel, dest, now, merged))
    lessons = [w for w in writes if w[0].as_posix() == "learning/lessons.jsonl"]
    if lessons:
        before = len(lesson_rows(lessons[0][2]) or []) if lessons[0][2] is not None else 0
        print("Lektionen: %d vorher, %d nach dem Zusammenführen" % (before, len(lesson_rows(lessons[0][3]) or [])))
    print("%d Gedächtnis-Dateien werden aus der Sicherung zurückgeholt oder ergänzt"
          % sum(1 for w in writes if w[0].parts[0] == "projects"))
    for rel, _, _, _ in writes:
        print("  " + rel.as_posix())
    if conflict_files:
        print("%d Notizen unterscheiden sich ohne erkennbar neuere Fassung; der aktuelle Stand bleibt, die alte Fassung"
              " liegt danach in %s:" % (len(conflict_files), conflicts))
        for rel, _ in conflict_files:
            print("  " + rel.as_posix())
    if untouched:
        print("%d weitere Dateien der Sicherung weichen ab und wurden bewusst nicht zurückgeholt:" % len(untouched))
        for rel in untouched:
            print("  " + rel)
    if removed_agents:
        print("%d entfernte Agency Agents bleiben entfernt." % removed_agents)
    if dry_run:
        return 0
    for rel, dest, now, merged in writes:
        if now is not None:
            target = safety / ".claude" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(now)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(merged)
    for rel, old in conflict_files:
        target = conflicts / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(old)
    print("Zurückgeholt: %d Dateien.%s" % (len(writes), " Der Stand davor liegt in %s" % safety if writes else ""))
    return 0


def next_steps(home):
    settings = json.loads((home / ".claude" / "settings.json").read_text(encoding="utf-8-sig"))
    print("\nNächste Schritte:")
    for name, spec in settings.get("extraKnownMarketplaces", {}).items():
        print("  claude plugin marketplace add %s" % spec.get("source", {}).get("repo", name))
    for plugin, enabled in settings.get("enabledPlugins", {}).items():
        if enabled and not plugin.endswith("@inline"):
            print("  claude plugin install %s" % plugin)
    print("  python %s doctor" % (home / ".claude" / "learning" / "ll.py").as_posix())
    print("  Danach eine neue Claude-Code-Session starten.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, allow_abbrev=False, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="nur anzeigen, was sich ändern würde")
    ap.add_argument("--home", default=str(Path.home()), help="Benutzerordner des Zielgeräts (Standard: der aktuelle)")
    ap.add_argument("--zurueckholen", metavar="ORDNER",
                    help="Lektionen und Gedächtnis aus einem restore-backup-Ordner mit dem aktuellen Stand zusammenführen")
    args = ap.parse_args()
    home = Path(args.home).absolute()
    if args.zurueckholen:
        return recover(home, Path(args.zurueckholen).absolute(), args.dry_run)
    manifest = json.loads((REPO / "setup-manifest.json").read_text(encoding="utf-8"))
    targets = {"claude/": home / ".claude", "extras/devos-claude-port/": home / "Documents" / "DevOS" / "devos-claude-port",
               "gsd/": home / ".gsd"}
    memory, old, new = manifest.get("memory", {}), slug(manifest["source_home"]), slug(home.as_posix())
    bad = [rel for rel in sorted(manifest["files"]) if unsafe(rel)]
    if bad:
        print("Abbruch, nichts geändert: ungültiger Pfad im Manifest: %s" % bad[0])
        return 1
    planned, skipped, conflicts = [], 0, []
    for rel, digest in sorted(manifest["files"].items()):
        src = REPO / rel
        if not src.is_file() or hashlib.sha256(src.read_bytes()).hexdigest() != digest:
            print("Abbruch, nichts geändert: %s fehlt oder passt nicht zur Prüfsumme im Manifest" % rel)
            return 1
        if rel.startswith("memory/"):  # memory/<kurz>/<datei> -> ~/.claude/projects/<slug>/memory/<datei>
            kurz, _, rest = rel[len("memory/"):].partition("/")
            if not rest or not re.fullmatch(r"[A-Za-z0-9-]+", memory.get(kurz, "")):
                print("Abbruch, nichts geändert: memory/%s fehlt im Manifest unter \"memory\" oder ist ungültig" % kurz)
                return 1
            if SCRATCH.search(memory[kurz]):  # Claude lädt diese Ordner auf keinem anderen Gerät
                skipped += 1
                continue
            base, dest = home / ".claude", home / ".claude" / "projects" / project(memory[kurz], old, new) / "memory" / rest
        else:
            prefix = next((p for p in targets if rel.startswith(p)), None)
            if prefix is None:
                continue
            base, dest = targets[prefix], targets[prefix] / rel[len(prefix):]
        data = src.read_bytes()
        if src.suffix.lower() in TEXT:
            data = rewrite(data.decode("utf-8"), manifest["source_home"], home.as_posix()).encode("utf-8")
        if dest.is_file() and rel == "claude/learning/lessons.jsonl":  # Lektionen dieses Geräts nie verwerfen
            data = merge_lessons(dest.read_bytes(), data)
        elif dest.is_file() and rel.startswith("memory/"):  # neuere Notizen dieses Geräts behalten
            data, conflict = merge_memory(dest.name, dest.read_bytes(), data)
            if conflict:
                conflicts.append(dest)
        planned.append((base, dest, data))
    changed = [(base, dest, data) for base, dest, data in planned if not dest.exists() or dest.read_bytes() != data]
    backup_root = home / ".claude" / ("restore-backup-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
    touched = [dest for _, dest, _ in changed] + [backup_root / base.name / dest.relative_to(base)
                                                  for base, dest, _ in changed if dest.exists()]
    too_long = [p for p in touched if len(str(p)) >= 260 or len(str(p.parent)) >= 248]  # Windows-Grenzen ohne lange Pfade
    if too_long and not long_paths_enabled():
        longest = max(too_long, key=lambda p: len(str(p)))
        print("Abbruch, nichts geändert: %d Pfade sind für Windows ohne lange Pfade zu lang (Datei ab 260, Ordner ab 248 "
              "Zeichen). Der längste hat %d Zeichen:\n  %s\nBitte zuerst den Schritt „Lange Pfade einschalten“ aus "
              "README.md ausführen oder mit --home einen kürzeren Benutzerordner wählen."
              % (len(too_long), len(str(longest)), longest))
        return 1
    note = ("%d Gedächtnis-Dateien aus Sitzungen ohne Projektordner übersprungen (bleiben im Repo und in WISSEN.md)"
            % skipped if skipped else "")
    retire, kept = retired_agents(home, manifest)  # vor dem Schreiben lesen: danach liegt schon das neue Manifest da
    print("%d Dateien im Setup, davon %d neu oder geändert" % (len(planned), len(changed)))
    if conflicts:
        print("%d Gedächtnis-Notizen dieses Geräts weichen ohne erkennbar neuere Fassung ab; es gilt der Repo-Stand, die"
              " Fassung dieses Geräts landet in der Sicherung: %s" % (len(conflicts), ", ".join(p.name for p in conflicts)))
    if retire:
        print("%d Agency Agents aus abgewählten Bereichen werden entfernt (vorher gesichert)" % len(retire))
    if kept:
        print("%d Agency Agents aus abgewählten Bereichen bleiben, weil sie auf diesem Gerät verändert wurden: %s"
              % (len(kept), ", ".join(p.name for p in kept)))
    if args.dry_run:
        for _, dest, _ in changed[:60]:
            print("  " + str(dest))
        if len(changed) > 60:
            print("  … und %d weitere" % (len(changed) - 60))
        for path in retire:
            print("  entfernen: " + str(path))
        if note:
            print(note)
        return 0
    backed_up = 0
    for base, dest, data in changed:
        if dest.exists():
            backup = backup_root / base.name / dest.relative_to(base)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dest, backup)
            backed_up += 1
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    for path in retire:
        backup = backup_root / ".claude" / path.relative_to(home / ".claude")
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
        path.unlink()
        backed_up += 1
    print("Wiederhergestellt: %d Dateien." % len(changed))
    if retire:
        print("Entfernt: %d Agency Agents aus abgewählten Bereichen." % len(retire))
    if note:
        print(note)
    if backed_up:
        print("Vorher gesichert: %d Dateien in %s" % (backed_up, backup_root))
    next_steps(home)
    return 0


if __name__ == "__main__":
    sys.exit(main())
