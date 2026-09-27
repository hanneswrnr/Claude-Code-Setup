"""Stellt das Claude-Code-Setup aus diesem Repo auf einem Gerät wieder her.

Kopiert die Dateien nach ~/.claude, das Gedächtnis nach ~/.claude/projects/<projekt>/memory, die GSD-Einstellung
nach ~/.gsd und das DevOS-Paket nach ~/Documents/DevOS, prüft vorher jede Prüfsumme und Pfadlänge, sichert alles,
was überschrieben würde, und ersetzt den Benutzerordner des Export-Geräts durch den dieses Geräts.
Gedächtnis aus Sitzungen ohne Projektordner bleibt nur im Repo, weil Claude es auf anderen Geräten nicht lädt.
Aufruf: python restore.py [--dry-run] [--home ORDNER]
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
    args = ap.parse_args()
    manifest = json.loads((REPO / "setup-manifest.json").read_text(encoding="utf-8"))
    home = Path(args.home).absolute()
    targets = {"claude/": home / ".claude", "extras/devos-claude-port/": home / "Documents" / "DevOS" / "devos-claude-port",
               "gsd/": home / ".gsd"}
    memory, old, new = manifest.get("memory", {}), slug(manifest["source_home"]), slug(home.as_posix())
    bad = [rel for rel in sorted(manifest["files"]) if unsafe(rel)]
    if bad:
        print("Abbruch, nichts geändert: ungültiger Pfad im Manifest: %s" % bad[0])
        return 1
    planned, skipped = [], 0
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
    print("%d Dateien im Setup, davon %d neu oder geändert" % (len(planned), len(changed)))
    if args.dry_run:
        for _, dest, _ in changed[:60]:
            print("  " + str(dest))
        if len(changed) > 60:
            print("  … und %d weitere" % (len(changed) - 60))
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
    print("Wiederhergestellt: %d Dateien." % len(changed))
    if note:
        print(note)
    if backed_up:
        print("Vorher gesichert: %d Dateien in %s" % (backed_up, backup_root))
    next_steps(home)
    return 0


if __name__ == "__main__":
    sys.exit(main())
