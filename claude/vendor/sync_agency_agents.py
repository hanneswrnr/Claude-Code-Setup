#!/usr/bin/env python3
"""Sync msitarzewski/agency-agents into ~/.claude/agents as user-level Claude Code subagents.

  python sync_agency_agents.py                  git pull + install/update (respects a saved selection)
  python sync_agency_agents.py --dry-run        show what would change, write nothing
  python sync_agency_agents.py --no-pull        skip git pull
  python sync_agency_agents.py --only engineering,design,testing   install only these divisions (saved)
  python sync_agency_agents.py --exclude healthcare,gis             install all but these (saved)
  python sync_agency_agents.py --all            clear a saved selection
  python sync_agency_agents.py --force          also overwrite/remove managed agents you edited locally
  python sync_agency_agents.py --uninstall      remove every agent this script installed

Claude Code compatibility transforms (everything else is copied verbatim):
  name   slugified exactly like upstream scripts/lib.sh ("AI Engineer" -> "ai-engineer")
  color  mapped to a Claude Code color (red/blue/green/yellow/purple/orange/pink/cyan), dropped if unmappable
Only files recorded in the manifest are ever overwritten or deleted.
"""
import argparse
import colorsys
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

CLAUDE_DIR = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
VENDOR = CLAUDE_DIR / "vendor"
REPO = VENDOR / "agency-agents"
AGENTS_DIR = CLAUDE_DIR / "agents"
MANIFEST = VENDOR / "agency-agents.manifest.json"
SELECTION = VENDOR / "agency-agents.selection.json"

RESERVED = {"explore", "plan", "general-purpose", "claude", "claude-code-guide", "statusline-setup", "output-style-setup"}
CC_COLORS = {"red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"}
COLOR_ALIASES = {
    "teal": "cyan", "turquoise": "cyan", "aqua": "cyan", "sky": "cyan",
    "indigo": "blue", "navy": "blue",
    "amber": "yellow", "gold": "yellow",
    "lime": "green", "emerald": "green", "olive": "green",
    "violet": "purple", "lavender": "purple",
    "magenta": "pink", "fuchsia": "pink", "rose": "pink",
    "crimson": "red", "maroon": "red",
    "brown": "orange", "coral": "orange",
}
FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n(.*?\r?\n)---[ \t]*(\r?\n|\Z)", re.S)


def slugify(value):
    """Same as upstream lib.sh: lowercase, non [a-z0-9] -> '-', squeeze and trim dashes."""
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]", "-", value.lower())).strip("-")


def map_color(value):
    v = value.strip().strip("\"'").lower()
    if v in CC_COLORS:
        return v
    if v in COLOR_ALIASES:
        return COLOR_ALIASES[v]
    m = re.fullmatch(r"#?([0-9a-f]{6})", v)
    if not m:
        return None
    r, g, b = (int(m.group(1)[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hue, _, sat = colorsys.rgb_to_hls(r, g, b)
    if sat < 0.2:
        return None
    for limit, name in ((15, "red"), (45, "orange"), (70, "yellow"), (165, "green"), (200, "cyan"),
                        (255, "blue"), (290, "purple"), (335, "pink"), (361, "red")):
        if hue * 360 < limit:
            return name
    return None


def frontmatter_field(text, key):
    m = FRONTMATTER.match(text)
    if not m:
        return None
    found = re.search(r"^%s:[ \t]*(.*?)[ \t]*$" % re.escape(key), m.group(1), re.M)
    return found.group(1).strip("\"'") if found else None


def transform(text):
    """Return (new_text, slug), or (None, None) when the file is not an agent definition."""
    m = FRONTMATTER.match(text)
    if not m:
        return None, None
    slug, out = None, []
    for line in m.group(1).splitlines(keepends=True):
        content = line.rstrip("\r\n")
        eol = line[len(content):] or "\n"
        key, _, value = content.partition(":")
        if key == "name":
            slug = slugify(value.strip().strip("\"'"))
            out.append("name: " + slug + eol)
        elif key == "color":
            color = map_color(value)
            if color:
                out.append("color: " + color + eol)
        else:
            out.append(line)
    if not slug:
        return None, None
    return text[:m.start(1)] + "".join(out) + text[m.end(1):], slug


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.run(["git", "-c", "core.longpaths=true", "-C", str(REPO), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="show what would change, write nothing")
    ap.add_argument("--no-pull", action="store_true", help="skip git pull")
    sel = ap.add_mutually_exclusive_group()
    sel.add_argument("--only", help="comma-separated divisions to install (saved for future syncs)")
    sel.add_argument("--exclude", help="comma-separated divisions to skip (saved for future syncs)")
    sel.add_argument("--all", action="store_true", help="clear a saved --only/--exclude selection")
    ap.add_argument("--force", action="store_true", help="overwrite/remove managed agents edited locally")
    ap.add_argument("--uninstall", action="store_true", help="remove every agent this script installed")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    prefix = "[dry-run] " if args.dry_run else ""

    manifest = load_json(MANIFEST, {})
    managed = manifest.get("files", {})

    if args.uninstall:
        removed = 0
        for fname in sorted(managed):
            target = AGENTS_DIR / fname
            if target.exists():
                if not args.dry_run:
                    target.unlink()
                removed += 1
        if not args.dry_run:
            MANIFEST.unlink(missing_ok=True)
        print("%sremoved %d agency agents from %s" % (prefix, removed, AGENTS_DIR))
        return 0

    if not REPO.is_dir():
        sys.exit("agency-agents checkout not found at %s - clone it first:\n"
                 "  git clone --depth 1 https://github.com/msitarzewski/agency-agents.git \"%s\"" % (REPO, REPO))

    if not args.no_pull:
        r = git("pull", "--ff-only", "--quiet")
        print("git pull: " + ("ok" if r.returncode == 0 else
                              "FAILED, using current checkout (%s)" % (r.stderr.strip() or r.stdout.strip())))
    commit = git("log", "-1", "--format=%h %cs").stdout.strip()

    divisions = list(load_json(REPO / "divisions.json", {}).get("divisions", {}))
    if not divisions:
        sys.exit("divisions.json missing or empty in %s" % REPO)

    selection = {} if args.all else load_json(SELECTION, {})
    if args.only:
        selection = {"only": [d.strip() for d in args.only.split(",") if d.strip()]}
    if args.exclude:
        selection = {"exclude": [d.strip() for d in args.exclude.split(",") if d.strip()]}
    unknown = set(selection.get("only", []) + selection.get("exclude", [])) - set(divisions)
    if unknown:
        sys.exit("unknown division(s): %s\navailable: %s" % (", ".join(sorted(unknown)), ", ".join(divisions)))
    chosen = [d for d in divisions
              if (not selection.get("only") or d in selection["only"]) and d not in selection.get("exclude", [])]
    if not args.dry_run and (args.all or args.only or args.exclude):
        if selection:
            SELECTION.write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
        else:
            SELECTION.unlink(missing_ok=True)

    # Names of agents this script does not manage (your own agents, other sources) must never be shadowed.
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    foreign = {}
    for p in AGENTS_DIR.glob("*.md"):
        if p.name not in managed:
            name = frontmatter_field(p.read_text(encoding="utf-8", errors="replace"), "name")
            if name:
                foreign[slugify(name)] = p.name

    planned, skipped, seen = {}, [], {}
    for div in chosen:
        for src in sorted((REPO / div).rglob("*.md")):
            raw = src.read_bytes()
            if not raw.startswith(b"---"):
                continue
            rel = src.relative_to(REPO).as_posix()
            text, slug = transform(raw.decode("utf-8", errors="replace"))
            if not slug:
                skipped.append((rel, "no name in frontmatter"))
            elif slug in RESERVED:
                skipped.append((rel, "name '%s' is reserved by Claude Code" % slug))
            elif slug in seen:
                skipped.append((rel, "duplicate name '%s' (already from %s)" % (slug, seen[slug])))
            elif slug in foreign:
                skipped.append((rel, "name '%s' already used by your agent %s" % (slug, foreign[slug])))
            elif src.name in planned:
                skipped.append((rel, "duplicate filename %s" % src.name))
            else:
                seen[slug] = rel
                planned[src.name] = {"source": rel, "name": slug, "data": text.encode("utf-8"),
                                     "description": frontmatter_field(text, "description") or ""}

    added = updated = unchanged = removed = 0
    kept_modified, new_manifest = [], {}
    for fname, item in planned.items():
        target = AGENTS_DIR / fname
        entry = {"source": item["source"], "name": item["name"], "sha256": sha(item["data"])}
        if target.exists():
            if fname not in managed:
                skipped.append((item["source"], "%s exists and is not managed by this script" % fname))
                continue
            current = sha(target.read_bytes())
            if current == entry["sha256"]:
                unchanged += 1
                new_manifest[fname] = entry
                continue
            if current != managed[fname].get("sha256") and not args.force:
                kept_modified.append(fname)
                new_manifest[fname] = managed[fname]
                continue
            updated += 1
        else:
            added += 1
        if not args.dry_run:
            target.write_bytes(item["data"])
        new_manifest[fname] = entry

    for fname, entry in managed.items():
        target = AGENTS_DIR / fname
        if fname in new_manifest or not target.exists():
            continue
        if sha(target.read_bytes()) != entry.get("sha256") and not args.force:
            kept_modified.append(fname)
            new_manifest[fname] = entry
            continue
        if not args.dry_run:
            target.unlink()
        removed += 1

    if not args.dry_run:
        MANIFEST.write_text(json.dumps({
            "repo": "https://github.com/msitarzewski/agency-agents",
            "commit": commit,
            "synced_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "selection": selection,
            "files": dict(sorted(new_manifest.items())),
        }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    tokens = sum(len(i["name"]) + len(i["description"]) + 8 for i in planned.values()) // 4
    print("%sagency-agents %s | divisions: %s" % (prefix, commit, json.dumps(selection) if selection else "all"))
    print("%s%d agents in %s (added %d, updated %d, unchanged %d, removed %d)"
          % (prefix, added + updated + unchanged, AGENTS_DIR, added, updated, unchanged, removed))
    for rel, why in skipped:
        print("  skipped %s: %s" % (rel, why))
    for fname in kept_modified:
        print("  kept locally modified %s (use --force to overwrite/remove)" % fname)
    print("approx. context cost of the agent list: ~%.1fk tokens per session" % (tokens / 1000))
    return 0


if __name__ == "__main__":
    sys.exit(main())
