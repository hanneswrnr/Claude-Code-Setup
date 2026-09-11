"""Cross-session recall: SQLite FTS5 index over Claude Code transcripts in ~/.claude/projects."""
import json
import re
import sqlite3
import time
from pathlib import Path

import llcore as core

DB = core.HOME / "sessions.db"
PROJECTS = Path.home() / ".claude" / "projects"
SKIP_PREFIXES = ("<command-", "<local-command", "<system-reminder", "<learned-lessons", "<learning-review", "Caveat:")


def connect():
    core.HOME.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB, timeout=10)
    con.execute("CREATE TABLE IF NOT EXISTS files (path TEXT PRIMARY KEY, size INTEGER, mtime REAL)")
    con.execute("CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(text, session UNINDEXED, project UNINDEXED, "
                "ts UNINDEXED, role UNINDEXED, tokenize='unicode61 remove_diacritics 2')")
    return con


def extract(row):
    """Yield (role, text) for real user prompts and assistant replies; skip tool noise and injected context."""
    msg = row.get("message")
    if row.get("isMeta") or row.get("isSidechain") or not isinstance(msg, dict):
        return
    role, content = row.get("type"), msg.get("content")
    parts = [content] if isinstance(content, str) else [
        p.get("text", "") for p in content or [] if isinstance(p, dict) and p.get("type") == "text"]
    for text in parts:
        text = (text or "").strip()
        if role in ("user", "assistant") and len(text) >= 3 and not text.startswith(SKIP_PREFIXES) \
                and not (role == "user" and text.startswith("<")):
            yield role, text[:4000]


def index(max_seconds=25.0):
    started, cfg, done = time.time(), core.config(), 0
    con = connect()
    known = {path: (size, mtime) for path, size, mtime in con.execute("SELECT path, size, mtime FROM files")}
    cutoff = time.time() - cfg["index_retention_days"] * 86400
    for path in sorted(PROJECTS.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime):
        stat = path.stat()
        if stat.st_mtime < cutoff or known.get(str(path)) == (stat.st_size, stat.st_mtime):
            continue
        session, project = path.stem, path.parent.name
        con.execute("DELETE FROM docs WHERE session = ?", (session,))
        rows = []
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                for role, text in extract(row):
                    rows.append((text, session, project, row.get("timestamp", ""), role))
        con.executemany("INSERT INTO docs (text, session, project, ts, role) VALUES (?, ?, ?, ?, ?)", rows)
        con.execute("INSERT OR REPLACE INTO files VALUES (?, ?, ?)", (str(path), stat.st_size, stat.st_mtime))
        con.commit()
        done += 1
        if time.time() - started > max_seconds:
            break
    con.close()
    return done


def search(query, limit=8, project=None):
    words = [w for w in re.findall(r"[\wäöüß]{2,}", query.lower())][:12]
    if not words:
        return []
    con = connect()
    sql = ("SELECT session, project, ts, role, snippet(docs, 0, '»', '«', ' … ', 24) FROM docs WHERE docs MATCH ?"
           + (" AND lower(project) = lower(?)" if project else "") + " ORDER BY bm25(docs) LIMIT ?")
    results = []
    for joiner in (" ", " OR "):  # all words first, then any word
        match = joiner.join('"%s"' % w for w in words)
        params = [match] + ([project] if project else []) + [limit]
        results = con.execute(sql, params).fetchall()
        if results:
            break
    con.close()
    return results
