"""Stellt das Claude-Code-Setup aus diesem Repo auf einem Gerät wieder her.

Kopiert die Dateien nach ~/.claude und das DevOS-Paket nach ~/Documents/DevOS, prüft vorher jede Prüfsumme,
sichert alles, was überschrieben würde, und ersetzt den Benutzerordner des Export-Geräts durch den dieses Geräts.
Aufruf: python restore.py [--dry-run] [--home ORDNER]
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
TEXT = {".md", ".json", ".jsonl", ".py", ".txt", ".toml", ".yaml", ".yml", ".ps1", ".sh", ".html", ".cfg", ".ini"}


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
    home = Path(args.home)
    targets = {"claude/": home / ".claude", "extras/devos-claude-port/": home / "Documents" / "DevOS" / "devos-claude-port"}
    planned = []
    for rel, digest in sorted(manifest["files"].items()):
        src = REPO / rel
        if not src.is_file() or hashlib.sha256(src.read_bytes()).hexdigest() != digest:
            print("Abbruch, nichts geändert: %s fehlt oder passt nicht zur Prüfsumme im Manifest" % rel)
            return 1
        prefix = next((p for p in targets if rel.startswith(p)), None)
        if prefix is None:
            continue
        data = src.read_bytes()
        if src.suffix.lower() in TEXT:
            data = rewrite(data.decode("utf-8"), manifest["source_home"], home.as_posix()).encode("utf-8")
        planned.append((targets[prefix], targets[prefix] / rel[len(prefix):], data))
    changed = [(base, dest, data) for base, dest, data in planned if not dest.exists() or dest.read_bytes() != data]
    print("%d Dateien im Setup, davon %d neu oder geändert" % (len(planned), len(changed)))
    if args.dry_run:
        for _, dest, _ in changed[:60]:
            print("  " + str(dest))
        if len(changed) > 60:
            print("  … und %d weitere" % (len(changed) - 60))
        return 0
    backup_root = home / ".claude" / ("restore-backup-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
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
    if backed_up:
        print("Vorher gesichert: %d Dateien in %s" % (backed_up, backup_root))
    next_steps(home)
    return 0


if __name__ == "__main__":
    sys.exit(main())
