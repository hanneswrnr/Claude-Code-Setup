# CONTEXT_ARCHITECTURE — Wie Kontext hier geführt wird

Nur dokumentierte Mittel von Claude Code 2.1.293: `modelSettings.<Modell>.autoCompactWindow`, ein Abschnitt „Compact Instructions“ in `CLAUDE.md`, manuelles `/compact`, Subagenten, Hooks. Nicht benutzt, weil nicht nötig oder nicht belegt: `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, eigene Hooks, die Kontext einspeisen.

## Vier Schichten

| Schicht | Wo sie liegt | Regel |
|---|---|---|
| Aktiver Kontext (Auftrag, Dateien in Arbeit, Blocker, Teststand) | Gespräch und Aufgabenliste | Bleibt, solange er gilt; wird beim Verdichten durch „Compact Instructions“ geschützt |
| Dauerhaftes Wissen | `CLAUDE.md` (global), Projekt-`CLAUDE.md`, Gedächtnis je Projekt, Lernloop | Eine Quelle je Tatsache, keine Kopien in Agents oder Skills |
| Vorläufiges (Logs, Zwischenhypothesen) | Scratchpad-Dateien | Nicht im Gespräch halten; bei Bedarf gezielt nachlesen |
| Wegwerfbares (Erfolgslogs, doppelte Ausgaben) | nirgends | Gar nicht erst ins Gespräch holen |

## Verdichtung

- **Schwelle:** 400.000 Token für Opus 5.5 und Sonnet 5.5 (`autoCompactWindow`). Gründe: Messung zeigt, dass Opus damit bei etwa 366.000 bleibt; die Sitzungen dort liefen ohne erkennbare Qualitätsklagen im Lernloop. **Nicht getestet:** 45 %, 55 % und 65 % gegeneinander. Ein sauberer Vergleich bräuchte gleiche Aufgaben mit Testergebnissen; er wurde nicht gemacht, deshalb wurde die bestehende Grenze nicht verschoben.
- **Inhalt der Zusammenfassung:** steuert der Abschnitt „Compact Instructions“ in `claude/CLAUDE.md` (Auftrag, Entscheidungen, verworfene Wege, geänderte Dateien, Teststand, Blocker, Freigabegrenzen; weglassen: Erfolgslogs, ganze Dateien, überholte Pläne).
- **Aufgabenbewusste Verdichtung:** Claude Code kann nicht von selbst „an Meilensteinen“ verdichten. Der manuelle Weg steht in `CLAUDE.md`: nach Meilenstein oder Themenwechsel `/compact` oder neue Sitzung mit kurzer Übergabe.
- **Vor der Verdichtung:** Der `PreCompact`-Hook des Lernloops sichert dessen Stand. Ein eigener Zwischenstand-Hook wurde bewusst nicht gebaut: Die Aufgabenliste, `git status` und `git diff` sind schon die verlässlichen Wahrheiten, und ein zusätzlicher Zustandsspeicher wäre ein konkurrierendes Gedächtnis.
- **Nach der Verdichtung:** Stand aus `git status`, `git diff` und Aufgabenliste prüfen, nicht aus der Zusammenfassung allein.

## Werkzeug-Ausgabe

Read mit `offset`/`limit` nach Grep; lange Build-, Test- und Migrationsausgaben in Dateien, mit Exit-Code und bei Fehlern voller Meldung; SQL mit `LIMIT`. Kein pauschales Abschneiden per Einstellung (`BASH_MAX_OUTPUT_LENGTH`, `MAX_MCP_OUTPUT_TOKENS`), weil es auch Fehlermeldungen kappt.

## Delegation

Nur wenn Isolation etwas bringt: breite Erkundung, Log-Analyse, unabhängige Prüfung, Sicherheit. Rückgabeformat: Ergebnis, Belege mit Datei:Zeile, Risiken, offene Fragen, nächster Schritt. Die 8 DevOS-Rollen sind genau diese Rollen und machen 98 % der Aufrufe aus. Für breite, parallele Läufe mit ausdrücklicher Freigabe gilt das Muster aus deiner Vorlage (Bild): Das Workflow-Skript hält den Plan und filtert die Agenten-Ausgaben, der Orchestrator sieht nur geprüfte Endergebnisse.

## Sitzungswechsel

Alte Sitzung nicht weiterziehen, wenn sie vor einer Einstellungsänderung gestartet wurde oder mehrere Verdichtungen hinter sich hat. Neue Sitzung mit kurzer Übergabe: Auftrag, Stand, geänderte Dateien, offene Punkte, nächster Schritt. Die Übergabe ersetzt weder Quelltext-Lesen noch Tests.
