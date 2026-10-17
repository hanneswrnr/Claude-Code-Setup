# OPTIMIZATION_CHANGELOG — 17.10.2026

Sicherung der Vorher-Stände: `~/.claude/backups/ctx-opt-20261017/` (`settings.json`, `CLAUDE.md`).

## Stand nach der Rücknahme (auf Wunsch, 17.10.2026)

Zurückgenommen: `settings.json` und `CLAUDE.md` sind wieder exakt der Vorher-Stand (keine Sonnet-Grenze, keine Abschnitte „Kontext sparen“, „Compact Instructions“ und keine Design-Regel). Die zwölf Design-/Frontend-/Barrierefreiheits-Agents haben wieder ihren Originalinhalt ohne `model`/`effort` und liegen im Archiv. **Die Modellauswahl ist damit wie vor dieser Prüfung.**

Bleibt bestehen: Die 235 nie benutzten Agents liegen im Archiv (46 Agents geladen: 8 DevOS-Rollen, `Explore`, 4 benutzte Fachagents, 33 GSD-Agents, die GSD-Befehle aufrufen). Die Messwerkzeuge und diese Dokumente bleiben als Nachschlagewerk; die Einträge unten beschreiben den Zwischenstand vor der Rücknahme. Ganz zurück: `mv ~/.claude/agents-archiv/*.md ~/.claude/agents/`.

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

### Agents archiviert (mit deiner Freigabe)
- **Vorher:** 293 Agent-Dateien in `~/.claude/agents/`, alle mit ihrer Beschreibung in jeder Sitzung geladen.
- **Nachher:** 58 geladen, 235 in `~/.claude/agents-archiv/` (wird von Claude Code nicht gelesen). Geladen bleiben: die 8 DevOS-Rollen, `Explore`, `technical-writer`, `legal-document-review`, `legal-compliance-checker`, `data-privacy-officer`, alle 33 GSD-Agents (die GSD-Befehle rufen sie auf; sie wurden nur nicht „direkt“ gezählt) und die 12 Design-Agents.
- **Abweichung vom Vorschlag:** statt 279 wurden 235 archiviert (GSD-Agents und Design-Agents bleiben).
- **Design auf Opus (Anweisung vom 17.10.2026):** `ui-designer`, `ux-architect`, `ux-researcher`, `brand-guardian`, `ui-finish-gate-reviewer`, `persona-walkthrough-specialist`, `visual-storyteller`, `whimsy-injector`, `image-prompt-engineer`, `inclusive-visuals-specialist`, `frontend-developer`, `accessibility-auditor` haben jetzt `model: opus` und `effort: high` in der Datei (vorher ohne Angabe); `devos-designer` hatte es schon. In `CLAUDE.md` steht die Regel unter „Modelle“.
- **Prüfung:** Alle 58 Dateien haben gültigen Kopfteil (`name`, `description`); alle 13 benutzten Namen sind vorhanden (`general-purpose` ist eingebaut). Ob die laufende Claude-Code-Sitzung die Agents neu einliest, ist nicht prüfbar: Es zeigt erst eine neue Sitzung. `claude agents --json` listet keine Agent-Definitionen und taugt dafür nicht.
- **Zurück:** `mv ~/.claude/agents-archiv/*.md ~/.claude/agents/` (die zwölf Design-Agents behalten dabei `model: opus`). Das Repo sichert beide Ordner (`claude/agents`, `claude/agents-archiv`); `export.py` kennt den Archivordner jetzt.
- **Erwarteter Gewinn:** etwa 15–20k Token je Sitzung (Schätzung aus dem Auftrag, nicht gemessen; erst der Wert „Custom agents“ in einer neuen Sitzung belegt es).

## Bewusst nicht geändert

- Keine Skills, Hooks oder MCP-Server entfernt oder abgeschaltet.
- Keine Berechtigungen geändert.
- Keine Ausgabe-Obergrenzen per Umgebungsvariable (würden Fehlermeldungen kappen).
- Compaction-Schwelle für Opus unverändert (kein Vergleichstest vorhanden).

## Geprüft, kein Handlungsbedarf (17.10.2026)

**Subagenten-Modell:** Verdacht war, dass `env.CLAUDE_CODE_SUBAGENT_MODEL = opus` die Modellangaben in den Agent-Dateien überstimmt. Test mit je einem Agenten, der nur sein Modell aus dem Systemprompt nannte: `devos-explorer` meldete Sonnet 5.5, `Explore` Haiku 5.5, `devos-designer` Opus 5.5. Die Dateiangaben gelten also, die Variable bleibt unverändert (sie greift nur für Agents ohne eigene Angabe). Gilt für die Desktop-App in dieser Sitzung; im reinen Terminal nicht getestet.

## Offen

- Nachher-Messung der Kontextwerte (siehe `CONTEXT_BENCHMARKS.md`), frühestens in zwei Wochen.
