#!/usr/bin/env python3
"""Lernloop für Claude Code (Hermes-artig): Hooks, Lektionen, Session-Suche.

  python C:/Users/hanne/.claude/learning/ll.py hook <Event>        wird von ~/.claude/settings.json aufgerufen
  python C:/Users/hanne/.claude/learning/ll.py add --kind mistake|success|preference --rule "..." [--why "..."]
         [--scope global|project] [--keywords a,b] [--tools Bash,PowerShell] [--errors "text"] [--source user-correction] [--note "..."]
  python C:/Users/hanne/.claude/learning/ll.py list [--status active] [--kind mistake] [--search wort]
  python C:/Users/hanne/.claude/learning/ll.py show|unpin|archive|restore|approve <id> [<id> ...]
  python C:/Users/hanne/.claude/learning/ll.py pin <id> [--block-regex REGEX]      nur mit Zustimmung des Nutzers
  python C:/Users/hanne/.claude/learning/ll.py edit <id> [--rule "..."] [--why "..."] [--keywords a,b] [--tools Bash] [--errors "text"]
  python C:/Users/hanne/.claude/learning/ll.py quarantine [list [--all]] | quarantine release <qid> ... | quarantine drop <qid> ...
  python C:/Users/hanne/.claude/learning/ll.py search "frage" [--here] [--limit N]    Volltextsuche über frühere Sessions
  python C:/Users/hanne/.claude/learning/ll.py gate arm --check "npm run check" [--check ...] [--max-rounds N] [--timeout S] [--note "..."]
  python C:/Users/hanne/.claude/learning/ll.py gate status|off [--cwd ORDNER] | gate run [--check "..."] [--timeout S] [--cwd ORDNER]
  python C:/Users/hanne/.claude/learning/ll.py index | curate [--apply] | stats | doctor
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

if len(sys.argv) >= 3 and sys.argv[1] == "hook":  # fast path, keeps hook latency low
    import llhooks
    sys.exit(llhooks.run(sys.argv[2], sys.stdin.buffer.read()))

import argparse
import json
import os
import re
import shutil

import llcore as core

STATUS_DE = {"active": "aktiv", "stale": "ruhend", "archived": "archiviert", "candidate": "wartet"}


def split(value):
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def short(lesson, width=110):
    rule = lesson["rule"] if len(lesson["rule"]) <= width else lesson["rule"][:width - 1] + "…"
    return "%s  %-10s %-16s %-7s %.2f  %s" % (lesson["id"], STATUS_DE.get(lesson["status"], lesson["status"]),
                                              core.KIND_DE.get(lesson["kind"], lesson["kind"]),
                                              "global" if lesson["scope"] == "global" else "projekt",
                                              lesson.get("confidence", 0), rule)


def cmd_add(args):
    project, root = core.project_key(args.cwd)
    status, payload = core.add_lesson(
        args.kind, args.rule, args.why, "global" if args.scope == "global" else project,
        {"keywords": split(args.keywords), "tools": split(args.tools), "errors": split(args.errors)},
        source=args.source, note=args.note, session=os.environ.get("CLAUDE_CODE_SESSION_ID", ""), project_path=root)
    if status in ("added", "merged"):
        print("%s: %s" % ("Neu gespeichert" if status == "added" else "Mit bestehender Lektion zusammengeführt", short(payload)))
    elif status == "candidate":
        reasons = [core.RISK_DE.get(r, r) for r in payload.get("risk", [])] or ["Freigabemodus ist eingeschaltet"]
        print("Als wartende Lektion gespeichert (Freigabe über /reflect nötig): " + ", ".join(reasons))
        print("  " + short(payload))
    elif status == "quarantined":
        print("Nicht gespeichert, in Quarantäne (Prüfung durch den Nutzer nötig): " + ", ".join(payload))
    else:
        print("Fehler: " + payload)
        return 1
    return 0


def cmd_list(args):
    lessons = core.load_lessons()
    for lesson in lessons:
        if args.status and lesson["status"] != args.status or args.kind and lesson["kind"] != args.kind:
            continue
        if args.search and args.search.lower() not in json.dumps(lesson, ensure_ascii=False).lower():
            continue
        print(short(lesson))
    return 0


def update(lesson_ids, action, change):
    with core.Lock():
        lessons = core.load_lessons()
        found = 0
        for lesson in lessons:
            if lesson["id"] in lesson_ids:
                before = dict(lesson)
                change(lesson)
                lesson["updated"] = core.now()
                core.ledger(action, "user", lesson["id"], before=before, after=lesson)
                found += 1
                print("%s: %s" % (action, short(lesson)))
        core.save_lessons(lessons)
    if not found:
        print("Keine Lektion mit dieser ID gefunden.")
    return 0 if found else 1


def cmd_simple(args):
    if args.cmd == "show":
        for lesson in core.load_lessons():
            if lesson["id"] in args.ids:
                print(json.dumps(lesson, ensure_ascii=False, indent=1))
        return 0
    if args.cmd == "pin" and args.block_regex:
        why = core.block_regex_problem(args.block_regex)
        if why:
            print("Sperre abgelehnt: %s" % why)
            return 1
    changes = {
        "pin": lambda l: l.update(pinned=True, block_regex=args.block_regex or l.get("block_regex", "")),
        "unpin": lambda l: l.update(pinned=False, block_regex=""),
        "archive": lambda l: l.update(status="archived"),
        "restore": lambda l: l.update(status="active"),
        "approve": lambda l: l.update(status="active"),
    }
    result = update(set(args.ids), args.cmd, changes[args.cmd])
    if args.cmd in ("approve", "restore"):
        for lesson in core.load_lessons():
            if lesson["id"] in args.ids and core.scan(*core.lesson_texts(lesson)):
                print("Hinweis: %s wird nicht eingeblendet, solange der Sicherheits-Scanner anschlägt. "
                      "Mit ll.py edit ohne diesen Teil umformulieren." % lesson["id"])
    return result


def cmd_edit(args):
    given = {k: getattr(args, k) for k in ("rule", "why", "keywords", "tools", "errors") if getattr(args, k) is not None}
    if not given:
        print("Nichts zu ändern: --rule, --why, --keywords, --tools oder --errors angeben.")
        return 1
    rule = " ".join(given["rule"].split()) if "rule" in given else None
    why = " ".join(given["why"].split()) if "why" in given else None
    if rule is not None and not 8 <= len(rule) <= 400:
        print("Fehler: Die Regel muss 8 bis 400 Zeichen lang sein.")
        return 1
    if why is not None and len(why) > 600:
        print("Fehler: Das Warum darf höchstens 600 Zeichen lang sein.")
        return 1
    trig = {k: core.clean_list(split(given[k])) for k in ("keywords", "tools", "errors") if k in given}
    hits = core.scan(rule or "", why or "", " ".join(sum(trig.values(), [])))
    if hits:
        print("Nicht geändert: Der Sicherheits-Scanner schlägt beim neuen Text an (%s)." % ", ".join(hits))
        return 1

    def change(lesson):
        if rule is not None:
            lesson["rule"] = rule
        if why is not None:
            lesson["why"] = why
        for key, values in trig.items():
            lesson.setdefault("triggers", {})[key] = values

    return update({args.id}, "edit", change)


def cmd_quarantine(args):
    action = args.action or "list"
    if action == "list":
        show_all = getattr(args, "all", False)
        rows = core.load_quarantine()
        shown = [row for row in rows if show_all or row["status"] == "open"]
        for row in shown:
            status = "  %-8s" % row["status"] if show_all else ""
            print("%s  %s%s  %s  %s" % (row["id"], str(row.get("ts", ""))[:16], status, ",".join(row.get("reasons", [])),
                                        str(row.get("rule", ""))[:100]))
        if not shown:
            print("Keine Quarantäne-Einträge." if show_all else "Keine offenen Quarantäne-Einträge.")
        return 0
    done = 0
    with core.Lock():
        rows, lessons = core.load_quarantine(), core.load_lessons()
        for row in rows:
            if row["id"] not in args.ids or row["status"] != "open":
                continue
            if action == "drop":
                row["status"] = "dropped"
                core.ledger("quarantine-drop", "user", None, note=row["id"])
                print("Verworfen: %s" % row["id"])
            else:
                trig = row.get("triggers") if isinstance(row.get("triggers"), dict) else {}
                trig = {k: core.clean_list(trig.get(k)) for k in ("keywords", "tools", "errors")}
                rule = " ".join(str(row.get("rule", "")).split())
                if row.get("kind") not in core.KINDS or len(rule) < 8:
                    print("Übersprungen (unvollständiger Eintrag): %s" % row["id"])
                    continue
                evidence = row.get("evidence") if isinstance(row.get("evidence"), dict) else {}
                why = " ".join(str(row.get("why", "")).split())
                labels = list(dict.fromkeys(["quarantine:" + r for r in row.get("reasons", [])]
                                            + core.risk(rule, why, " ".join(sum(trig.values(), [])))))
                lesson = core.make_lesson(lessons, row["kind"], rule, why, row.get("scope") or "global", trig,
                                          evidence.get("source", "manual"), [evidence] if evidence else [], "candidate", labels)
                lessons.append(lesson)
                row["status"], row["lesson"] = "released", lesson["id"]
                core.ledger("quarantine-release", "user", lesson["id"], after=lesson, note=row["id"])
                print("Als wartende Lektion übernommen (Freigabe mit ll.py approve %s): %s" % (lesson["id"], row["id"]))
            done += 1
        if done:
            if action == "release":
                core.save_lessons(lessons)
            core.save_quarantine(rows)
    if not done:
        print("Kein offener Quarantäne-Eintrag mit dieser ID gefunden.")
    return 0 if done else 1


def cmd_search(args):
    import llsearch
    llsearch.index(max_seconds=10)
    project = None
    if args.here:
        project = re.sub(r"[^A-Za-z0-9]", "-", str(Path.cwd()))
    rows = llsearch.search(args.query, limit=args.limit, project=project)
    if not rows:
        print("Nichts gefunden.")
    for session, proj, ts, role, snippet in rows:
        print("%s  %s  [%s, %s]\n    %s" % (ts[:10], proj[-45:], role, session[:8], " ".join(snippet.split())))
    return 0


def cmd_curate(args):
    cfg, hits = core.config(), core.hits_map()
    lessons = core.load_lessons()
    plan = []
    for lesson in lessons:
        if lesson["status"] not in ("active", "stale") or lesson.get("pinned"):
            continue
        idle = core.idle_days(lesson, hits)
        if idle >= cfg["archive_days"]:
            plan.append((lesson["id"], "archive", "%d Tage ungenutzt" % idle))
        elif idle >= cfg["stale_days"] and lesson["status"] == "active":
            plan.append((lesson["id"], "stale", "%d Tage ungenutzt" % idle))
        elif lesson["status"] == "stale":
            used = core.newest(hits.get(lesson["id"], (0, "", ""))[1], lesson.get("last_hit"))
            if used and core.days_since(used.isoformat()) < cfg["stale_days"]:
                plan.append((lesson["id"], "reactivate", "wieder genutzt"))
    active = [l for l in lessons if l["status"] == "active"]
    merged = set()
    for i, first in enumerate(active):
        for second in active[i + 1:]:
            if second["id"] not in merged and first["kind"] == second["kind"] and first["scope"] == second["scope"] \
                    and core.is_duplicate(first, second["rule"], second.get("triggers", {})):
                plan.append((second["id"], "merge:" + first["id"], "fast gleich wie " + first["id"]))
                merged.add(second["id"])
    for scope_type, cap in (("global", cfg["max_active_global"]), ("project", cfg["max_active_project"])):
        pool = [l for l in active if (l["scope"] == "global") == (scope_type == "global") and not l.get("pinned")]
        for lesson in sorted(pool, key=lambda l: core.score(l, hits))[:max(0, len(pool) - cap)]:
            plan.append((lesson["id"], "archive", "Limit %d für %s erreicht" % (cap, scope_type)))
    for lesson_id, action, why in plan:
        print("%-22s %-28s %s" % (lesson_id, action, why))
    if not plan:
        print("Nichts zu tun.")
    if not args.apply:
        print("(Vorschau. Mit --apply ausführen.)")
        return 0
    backups = core.HOME / "backups"
    backups.mkdir(parents=True, exist_ok=True)
    if core.LESSONS.exists():
        shutil.copy2(core.LESSONS, backups / ("lessons-%s.jsonl" % core.now()[:19].replace(":", "")))
    for old in sorted(backups.glob("lessons-*.jsonl"))[:-10]:
        old.unlink()
    with core.Lock():
        lessons = core.load_lessons()
        by_id = {l["id"]: l for l in lessons}
        for lesson_id, action, why in plan:
            lesson = by_id.get(lesson_id)
            if not lesson:
                continue
            before = dict(lesson)
            if action.startswith("merge:") and action[6:] in by_id:
                keep = by_id[action[6:]]
                keep["evidence"] = (keep.get("evidence", []) + lesson.get("evidence", []))[-10:]
                best = max(keep.get("confidence", 0.5), lesson.get("confidence", 0.5))
                keep["confidence"] = round(max(keep.get("confidence", 0.5), min(0.9, best + 0.05)), 2)
                lesson["status"] = "archived"
            elif action == "reactivate":
                lesson["status"] = "active"
            else:
                lesson["status"] = "archived" if action == "archive" else "stale"
            lesson["updated"] = core.now()
            core.ledger("curate-" + action.split(":")[0], "curator", lesson_id, before=before, after=lesson, note=why)
        folded = core.take_hits()
        for lesson in lessons:
            count, last_use, last_seen = folded.get(lesson["id"], (0, "", ""))
            if count:
                lesson["hits"] = lesson.get("hits", 0) + count
            if last_use:
                lesson["last_hit"] = max(lesson.get("last_hit") or "", last_use)
            if last_seen:
                lesson["last_seen"] = max(lesson.get("last_seen") or "", last_seen)
        core.save_lessons(lessons)
    for state in core.STATE_DIR.glob("*.json"):
        if core.days_since(core.read_json(state, {}).get("updated", "")) > 14:
            state.unlink()
    core.write_json(core.META, dict(core.read_json(core.META, {}), last_curation=core.now()))
    print("Pflege abgeschlossen. Sicherung in %s" % backups)
    return 0


def cmd_stats(args):
    lessons = core.load_lessons()
    count = lambda key: {v: sum(1 for l in lessons if l[key] == v) for v in sorted({l[key] for l in lessons})}
    print("Lektionen gesamt: %d" % len(lessons))
    print("nach Status: %s" % count("status"))
    print("nach Art: %s" % count("kind"))
    hits = core.hits_map()
    uses = lambda l: l.get("hits", 0) + hits.get(l["id"], (0, "", ""))[0]
    print("am häufigsten genutzt:")
    for lesson in sorted(lessons, key=lambda l: -uses(l))[:5]:
        print("  %3d× %s" % (uses(lesson), lesson["rule"][:90]))
    signatures = {}
    for state in core.STATE_DIR.glob("*.json"):
        for failure in core.read_json(state, {}).get("failures", []):
            sig = re.sub(r"[a-z]:[\\/][^\s'\"]+|/[^\s'\"]+|\d+", "#", failure.get("error", "").lower())[:80]
            signatures.setdefault((failure.get("tool"), sig), set()).add(state.stem)
    repeated = {k: v for k, v in signatures.items() if len(v) >= 2}
    print("Fehler, die in mehreren Sessions wiederkehren (Ziel: 0): %d" % len(repeated))
    for (tool, sig), sessions in sorted(repeated.items(), key=lambda kv: -len(kv[1]))[:5]:
        print("  %d Sessions · %s · %s" % (len(sessions), tool, sig))
    print("in Quarantäne (offen): %d" % sum(1 for row in core.load_quarantine() if row["status"] == "open"))
    return 0


def cmd_doctor(args):
    import sqlite3
    import llgate
    ok = True

    def check(label, passed, hint=""):
        nonlocal ok
        ok &= bool(passed)
        print("%s %s%s" % ("OK  " if passed else "WARN", label, "" if passed else " -> " + hint))

    check("Python >= 3.9", sys.version_info >= (3, 9), "Python aktualisieren")
    try:
        sqlite3.connect(":memory:").execute("CREATE VIRTUAL TABLE t USING fts5(x)")
        check("SQLite FTS5 verfügbar", True)
    except sqlite3.Error:
        check("SQLite FTS5 verfügbar", False, "Session-Suche nicht möglich")
    core.HOME.mkdir(parents=True, exist_ok=True)
    check("Speicherordner beschreibbar: %s" % core.HOME, os.access(core.HOME, os.W_OK), "Rechte prüfen")
    settings = core.read_json(Path.home() / ".claude" / "settings.json", {})
    wired = json.dumps(settings.get("hooks", {}) if isinstance(settings, dict) else {})
    for event in ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUseFailure", "Stop", "PreCompact", "SessionEnd"):
        check("Hook %s eingetragen" % event, "ll.py hook %s" % event in wired, "settings.json prüfen")
    skills = Path.home() / ".claude" / "skills"
    for skill in ("learn", "reflect", "recall"):
        check("Skill %s vorhanden" % skill, (skills / skill / "SKILL.md").exists(), "Skill-Datei fehlt")
    errors = core.read_jsonl(core.HOME / "errors.jsonl")
    check("keine Hook-Fehler protokolliert (%d)" % len(errors), not errors, "siehe errors.jsonl")
    lessons = core.load_lessons()
    print("Lektionen: %d · wartend: %d · Quarantäne offen: %d · Prüf-Gates aktiv: %d" % (
        len(lessons), sum(1 for l in lessons if l["status"] == "candidate"),
        sum(1 for row in core.load_quarantine() if row["status"] == "open"), len(list(llgate.GATES.glob("*.json")))))
    return 0 if ok else 1


def cmd_gate(args):
    import llgate
    if args.action == "arm":
        if not args.check:
            print('Mindestens eine Prüfung angeben, z. B. --check "npm run check"')
            return 1
        state, bad = llgate.arm(args.check, args.max_rounds, args.timeout, args.note)
        for check, why in bad:
            print("Abgelehnt: %s" % ("%s -> %s" % (check, why) if check else why))
        if bad:
            return 1
        print("Prüf-Gate aktiv für %s" % state["cwd"])
        print("  Prüfungen: %s" % " | ".join(state["checks"]))
        print("  höchstens %d Runden, Zeitbudget je Runde %d s, endet spätestens nach 24 Stunden" % (state["max_rounds"], state["timeout"]))
        print("  %s" % ("gebunden an diese Session" if state["session"] else
                        "an keine Session gebunden: die nächste Session in diesem Ordner übernimmt es, wenn sie innerhalb von 2 Stunden endet"))
        print("Ab jetzt prüft der Stop-Hook nach jeder Antwort. Beenden: python C:/Users/hanne/.claude/learning/ll.py gate off")
        return 0
    if args.action in ("status", "off"):
        state = llgate.find(args.cwd)
        if args.action == "status":
            print(json.dumps(llgate.public(state), ensure_ascii=False, indent=1) if state else "Kein Prüf-Gate aktiv.")
        elif state:
            llgate.disarm(state, "manual-off")
            print("Prüf-Gate beendet.")
        else:
            print("Kein Prüf-Gate aktiv.")
        return 0
    cwd = os.path.abspath(args.cwd or os.getcwd())
    state = None if args.check else llgate.find(cwd)
    checks = args.check or (state["checks"] if state else [])
    if state:
        cwd = state.get("cwd") or state["root"]
    bad = [(check, llgate.problem(check) or llgate.script_problem(check, cwd)) for check in checks]
    bad = [(check, why) for check, why in bad if why]
    for check, why in bad:
        print("Abgelehnt: %s -> %s" % (check, why))
    if not checks:
        print("Keine Prüfung angegeben und kein Prüf-Gate aktiv.")
    if not checks or bad:
        return 1
    for result in llgate.run_checks({"checks": checks, "cwd": cwd, "root": cwd, "timeout": llgate.clamp(args.timeout, 30, 1500, 900)}):
        print("%s  %s  (Exit %s, %s s)" % ("grün" if result["code"] == 0 else "ROT ", result["check"], result["code"], result["seconds"]))
        if result["code"] != 0:
            print("    " + result["tail"][-600:].replace("\n", "\n    "))
    return 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="ll.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
                                 allow_abbrev=False)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def parser(group, name, **kwargs):  # no abbreviated options anywhere: permission rules match exact words
        return group.add_parser(name, allow_abbrev=False, **kwargs)

    add = parser(sub, "add")
    add.add_argument("--kind", required=True, choices=sorted(core.KINDS))
    add.add_argument("--rule", required=True)
    add.add_argument("--why", default="")
    add.add_argument("--scope", default="global", choices=["global", "project"])
    add.add_argument("--keywords", default="")
    add.add_argument("--tools", default="")
    add.add_argument("--errors", default="")
    add.add_argument("--source", default="manual", choices=sorted(core.SOURCE_CONFIDENCE))
    add.add_argument("--note", default="")
    add.add_argument("--cwd", default=None)
    lst = parser(sub, "list")
    lst.add_argument("--status")
    lst.add_argument("--kind")
    lst.add_argument("--search")
    for name in ("show", "pin", "unpin", "archive", "restore", "approve"):
        p = parser(sub, name)
        p.add_argument("ids", nargs="+")
        if name == "pin":
            p.add_argument("--block-regex", default="")
    edit = parser(sub, "edit", help="Lektion umformulieren (nur mit Zustimmung des Nutzers)")
    edit.add_argument("id")
    for flag in ("--rule", "--why", "--keywords", "--tools", "--errors"):
        edit.add_argument(flag, default=None)
    quar = parser(sub, "quarantine", help="Quarantäne: list [--all] | release <qid> | drop <qid>")
    quars = quar.add_subparsers(dest="action")
    parser(quars, "list").add_argument("--all", action="store_true", help="auch übernommene und verworfene Einträge zeigen")
    for name in ("release", "drop"):
        parser(quars, name).add_argument("ids", nargs="+")
    srch = parser(sub, "search")
    srch.add_argument("query")
    srch.add_argument("--limit", type=int, default=8)
    srch.add_argument("--here", action="store_true", help="nur Sessions aus dem aktuellen Ordner")
    cur = parser(sub, "curate")
    cur.add_argument("--apply", action="store_true")
    gate = parser(sub, "gate", help="Prüf-Gate: arm | status | off | run")
    gates = gate.add_subparsers(dest="action", required=True)
    g_arm = parser(gates, "arm", help="im Projektordner ausführen")
    g_arm.add_argument("--check", action="append", default=[], help="Prüfbefehl, mehrfach möglich")
    g_arm.add_argument("--max-rounds", type=int, default=8)
    g_arm.add_argument("--timeout", type=int, default=900, help="Sekunden für alle Prüfungen einer Runde (30 bis 1500)")
    g_arm.add_argument("--note", default="")
    for name in ("status", "off"):
        parser(gates, name).add_argument("--cwd", default=None)
    g_run = parser(gates, "run", help="einmal prüfen, ohne scharf zu schalten")
    g_run.add_argument("--check", action="append", default=[], help="Prüfbefehl, mehrfach möglich")
    g_run.add_argument("--timeout", type=int, default=900)
    g_run.add_argument("--cwd", default=None)
    for name in ("index", "stats", "doctor"):
        parser(sub, name)
    args = ap.parse_args()
    if args.cmd == "add":
        return cmd_add(args)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd in ("show", "pin", "unpin", "archive", "restore", "approve"):
        return cmd_simple(args)
    if args.cmd == "edit":
        return cmd_edit(args)
    if args.cmd == "quarantine":
        return cmd_quarantine(args)
    if args.cmd == "search":
        return cmd_search(args)
    if args.cmd == "index":
        import llsearch
        print("Neu indexierte Sessions: %d" % llsearch.index())
        return 0
    if args.cmd == "curate":
        return cmd_curate(args)
    if args.cmd == "stats":
        return cmd_stats(args)
    if args.cmd == "gate":
        return cmd_gate(args)
    return cmd_doctor(args)


if __name__ == "__main__":
    sys.exit(main())
