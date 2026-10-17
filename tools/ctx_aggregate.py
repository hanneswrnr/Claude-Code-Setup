"""Aggregiert ueber alle Sitzungen seit Datum: Agent-Aufrufe je Typ, Groessenverteilung der Tool-Ergebnisse."""
import json, sys, glob, os, collections, time
since = time.mktime(time.strptime(sys.argv[1], "%Y-%m-%d"))
agents = collections.Counter(); buckets = collections.defaultdict(lambda: collections.Counter())
n_files = 0
for p in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")) + glob.glob(os.path.expanduser("~/.claude/projects/*/*/subagents/*.jsonl")):
    p = "\\\\?\\" + os.path.abspath(p)
    try:
        if os.path.getmtime(p) < since: continue
    except OSError: continue
    n_files += 1
    id2 = {}
    with open(p, encoding="utf-8", errors="replace") as f:
        for line in f:
            try: r = json.loads(line)
            except Exception: continue
            m = r.get("message") or {}
            c = m.get("content") if isinstance(m, dict) else None
            if not isinstance(c, list): continue
            for b in c:
                if b.get("type") == "tool_use":
                    id2[b["id"]] = b.get("name")
                    if b.get("name") == "Agent":
                        agents[(b.get("input") or {}).get("subagent_type") or "general-purpose"] += 1
                elif b.get("type") == "tool_result":
                    body = b.get("content")
                    n = len(body) if isinstance(body, str) else sum(len(x.get("text", "")) for x in body if isinstance(x, dict))
                    nm = id2.get(b.get("tool_use_id"), "?")
                    if nm.startswith("mcp__"): nm = "mcp"
                    k = "<2k" if n < 2000 else "2-10k" if n < 10000 else "10-30k" if n < 30000 else ">=30k"
                    buckets[nm][k + "_n"] += 1; buckets[nm][k + "_c"] += n
print("Dateien", n_files)
print("Agent-Typen:", agents.most_common(40))
print("verschiedene Typen genutzt:", len(agents))
for nm in ("Bash", "PowerShell", "Read", "Grep", "mcp", "Agent"):
    b = buckets[nm]; tot = sum(v for k, v in b.items() if k.endswith("_c")) or 1
    print(nm, {k: b[k] for k in sorted(b)}, "Anteil>=10k: %d%%" % ((b["10-30k_c"] + b[">=30k_c"]) * 100 // tot))
