"""Statusleiste für Claude Code: zeigt Modell, Effort, Kontext-Auslastung, Cache-Trefferquote und Abo-Limits.

Claude Code ruft das Skript bei jeder Aktualisierung auf und schickt den Sessionzustand als JSON auf stdin
(siehe code.claude.com/docs/en/statusline). Die Ausgabe ist genau eine Zeile. Fehler werden nie gemeldet,
damit die Leiste die Session nicht stört.
"""
import json
import sys


def pick(data, path, default=None):
    for key in path.split("."):
        if not isinstance(data, dict) or key not in data:
            return default
        data = data[key]
    return data


def percent(value):
    try:
        return "%d%%" % round(float(value))
    except (TypeError, ValueError):
        return None


def main():
    try:
        # Claude Code schickt UTF-8; unter Windows wäre stdin sonst cp1252, eine BOM wird toleriert.
        data = json.loads(sys.stdin.buffer.read().decode("utf-8-sig", errors="replace") or "{}")
    except ValueError:
        data = {}
    if not isinstance(data, dict):
        data = {}
    parts = []

    model = pick(data, "model.display_name") or pick(data, "model.id") or "Modell?"
    if pick(data, "fast_mode"):
        model += " fast"
    parts.append(model)

    effort = pick(data, "effort.level")
    if effort:
        parts.append("Effort " + str(effort))

    used = percent(pick(data, "context_window.used_percentage"))
    if used:
        size = pick(data, "context_window.context_window_size")
        window = "1M" if isinstance(size, (int, float)) and size >= 1000000 else "200k"
        parts.append("Kontext %s von %s" % (used, window))

    ratio = pick(data, "prompt_cache.hit_ratio")
    if isinstance(ratio, (int, float)):
        share = percent(ratio * 100 if ratio <= 1 else ratio)
        if share:
            parts.append("Cache %s%s" % (share, "" if pick(data, "prompt_cache.warm", True) else " kalt"))

    for label, key in (("5h", "rate_limits.five_hour"), ("Woche", "rate_limits.seven_day")):
        limit = pick(data, key)
        value = None
        if isinstance(limit, dict):
            for field in ("used_percentage", "utilization", "percent_used", "used_pct"):
                value = percent(limit.get(field))
                if value:
                    break
        elif isinstance(limit, (int, float)):
            value = percent(limit)
        if value:
            parts.append("%s %s" % (label, value))

    # Claude Code liest UTF-8; die Windows-Standardausgabe wäre sonst cp1252 und zerlegt das Trennzeichen.
    sys.stdout.buffer.write(" · ".join(str(p) for p in parts if p).encode("utf-8"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # eine kaputte Statusleiste darf die Session nie stören
        sys.exit(0)
