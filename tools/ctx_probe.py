"""Misst pro Sitzung: Kontextspitze, Compactions, Tool-Ausgaben nach Werkzeug, wiederholte Reads.
Nur lesend. Tokenzahlen stammen aus den usage-Feldern der Assistant-Nachrichten (exakt);
Tool-Ausgaben sind Zeichenzahlen (Proxy, keine Tokens)."""
import json, sys, glob, os, collections

def analyse(path):
    peak = 0; last = 0; compacts = 0; turns = 0
    tool_chars = collections.Counter(); tool_n = collections.Counter()
    reads = collections.Counter(); id2name = {}
    out_tok = 0; model = None; big = []
    drops = 0
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try: r = json.loads(line)
            except Exception: continue
            t = r.get("type")
            if r.get("isCompactSummary") or (t == "system" and "compact" in str(r.get("subtype", ""))):
                compacts += 1
            m = r.get("message") or {}
            if t == "assistant" and isinstance(m, dict):
                u = m.get("usage") or {}
                ctx = (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                       + u.get("cache_creation_input_tokens", 0))
                if ctx:
                    turns += 1
                    if last and ctx < last * 0.6: drops += 1
                    last = ctx; peak = max(peak, ctx)
                out_tok += u.get("output_tokens", 0)
                model = m.get("model") or model
                c = m.get("content")
                if isinstance(c, list):
                    for b in c:
                        if b.get("type") == "tool_use":
                            id2name[b["id"]] = b.get("name")
                            if b.get("name") == "Read":
                                reads[(b.get("input") or {}).get("file_path")] += 1
            elif t == "user" and isinstance(m, dict):
                c = m.get("content")
                if isinstance(c, list):
                    for b in c:
                        if b.get("type") == "tool_result":
                            body = b.get("content")
                            n = len(body) if isinstance(body, str) else sum(len(x.get("text", "")) for x in body if isinstance(x, dict))
                            nm = id2name.get(b.get("tool_use_id"), "?")
                            tool_chars[nm] += n; tool_n[nm] += 1
                            big.append((n, nm))
    rep = sum(v - 1 for v in reads.values() if v > 1)
    big.sort(reverse=True)
    return dict(path=path, model=model, peak=peak, last=last, turns=turns, compacts=compacts, drops=drops,
                out=out_tok, tool_chars=tool_chars, tool_n=tool_n, rereads=rep, reads=sum(reads.values()),
                top5=big[:5])

if __name__ == "__main__":
    for p in sys.argv[1:]:
        a = analyse(p)
        print(os.path.basename(p)[:12], os.path.getsize(p)//1024, "KB", a["model"], "peak", a["peak"], "turns", a["turns"],
              "compacts", a["compacts"], "drops", a["drops"], "reads", a["reads"], "rereads", a["rereads"])
        tot = sum(a["tool_chars"].values()) or 1
        for k, v in a["tool_chars"].most_common(6):
            print("   %-14s %9d Zeichen (%2d%%) in %d Aufrufen" % (k, v, v * 100 // tot, a["tool_n"][k]))
