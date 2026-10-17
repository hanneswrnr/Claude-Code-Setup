# OPTIMIZATION_CHANGELOG — 17.10.2026

Sicherung der Vorher-Stände: `~/.claude/backups/ctx-opt-20261017/` (`settings.json`, `CLAUDE.md`).

## Geändert

### `~/.claude/settings.json` (im Repo: `claude/settings.json`)
- **Vorher:** `modelSettings.claude-sonnet-5-5` hatte nur `maxEffortLevel`.
- **Nachher:** zusätzlich `"autoCompactWindow": 400000`, gleicher Wert wie bei Opus.
- **Grund:** Sonnet-Sitzung vom 17.10. erreichte 962.000 Token (siehe `CONTEXT_AUDIT.md`).
- **Kompatibilität:** Schlüssel ist in 2.1.293 dokumentiert (`/autocompact` speichert ihn dort). Gilt vermutlich ab der nächsten Sitzung.
- **Zurück:** Zeile entfernen oder Datei aus der Sicherung zurückkopieren.

### `~/.claude/CLAUDE.md` (im Repo: `claude/CLAUDE.md`)
- **Vorher:** 16,1 KB, ohne Regeln zur Werkzeug-Ausgabe und ohne Abschnitt für die Verdichtung.
- **Nachher:** 18,1 KB. Neu: Abschnitt „Kontext sparen“ (gezielte Reads, Ausgabe in Dateien, Delegation mit festem Rückgabeformat, LIMIT bei Abfragen, Sitzungswechsel) und „Compact Instructions“.
- **Grund:** Read und Bash liefern etwa 70 % der Tool-Ergebnisse; Zusammenfassungen sollen Entscheidungen und Freigabegrenzen behalten.
- **Kosten:** etwa 550 Token je Sitzung dauerhaft.
- **Zurück:** Abschnitte „Kontext sparen“ und „Compact Instructions“ am Dateiende löschen oder Datei aus der Sicherung zurückkopieren.

### Neu im Repo
- `tools/ctx_probe.py` (Messung je Sitzung), `tools/ctx_aggregate.py` (Messung über viele Sitzungen: Agent-Nutzung, Größenverteilung). Nur lesend. Aufruf: `python -I tools/ctx_aggregate.py 2026-10-01`; die Skripte liegen auch in `~/.claude/vendor/`.
- `docs/context/` mit diesen vier Dokumenten.

## Bewusst nicht geändert

- Keine Agents, Skills, Hooks oder MCP-Server entfernt oder abgeschaltet.
- Keine Berechtigungen geändert.
- Keine Ausgabe-Obergrenzen per Umgebungsvariable (würden Fehlermeldungen kappen).
- Compaction-Schwelle für Opus unverändert (kein Vergleichstest vorhanden).

## Offen: braucht deine Entscheidung

1. **279 nie benutzte Agents archivieren.** Seit dem 01.10. wurden nur 14 von 293 Typen gerufen. Vorschlag: Alle außer den 14 benutzten (`devos-*`, `Explore`, `legal-compliance-checker`, `data-privacy-officer`, `technical-writer`, `legal-document-review`, `general-purpose`) nach `~/.claude/agents-archiv/` verschieben. Gewinn: etwa 20k Token je Sitzung (Angabe aus dem Auftrag, nicht nachgemessen). Rückweg: Ordner zurückschieben. Die Agents bleiben im Repo gesichert.
2. **Subagenten-Modell:** `env.CLAUDE_CODE_SUBAGENT_MODEL = opus` setzt laut Dokumentation alle Subagenten auf Opus und hat Vorrang vor der Modellangabe in den Agent-Dateien. Dann liefen `devos-explorer`, `devos-researcher` (Sonnet) und `Explore` (Haiku) ebenfalls auf Opus. **Nicht verifiziert** (meine Messung der Subagent-Modelle ergab nichts). Betrifft Kosten und Nutzungslimit, nicht den Kontext.
