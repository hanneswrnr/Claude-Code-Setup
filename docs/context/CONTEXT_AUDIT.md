# CONTEXT_AUDIT — Wo der Kontext hingeht (Stand 17.10.2026)

Claude Code 2.1.293, Windows 11. Alle Zahlen stammen aus `tools/ctx_probe.py` und `tools/ctx_aggregate.py` (nur lesend). **Tokenzahlen** sind die `usage`-Felder der Assistant-Nachrichten und damit exakt. **Zeichenzahlen** der Tool-Ergebnisse sind nur ein Maß für die Größe, keine Tokens. Die Werte der Kategorien aus dem Kontext-Bildschirm (System tools 21,5k, Custom agents 21,1k, MCP 16k, Skills 9,9k, Memory 7k) sind die Angaben aus dem Auftrag, nicht von mir nachgemessen.

## Hauptbefund

Messages sind nicht „Gespräch“, sondern Werkzeug-Ausgabe. In 518 Sitzungsdateien seit dem 01.10.2026 (Haupt- und Subagent-Sitzungen) entfielen die Tool-Ergebnisse so:

| Werkzeug | Aufrufe | Zeichen | Anteil an Ergebnissen ≥ 10.000 Zeichen |
|---|---:|---:|---:|
| Bash | 39.714 | 108 Mio. | 33 % |
| Read | 7.829 | 65 Mio. | 76 % |
| PowerShell | 2.646 | 5 Mio. | 36 % |
| MCP (alle) | 5.856 | 7,6 Mio. | 18 % |
| Grep | 4.246 | 6,7 Mio. | 14 % |
| Agent (Rückgabe an das Hauptgespräch) | 708 | 0,8 Mio. | 1 % |

- **Read ist der größte Hebel:** 594 Reads lieferten je über 30.000 Zeichen (23 Mio. Zeichen, 36 % aller Read-Zeichen). In den großen Sitzungen wurden 27–48 % der Reads wiederholt (zum Beispiel 66 von 180, 42 von 87).
- **Bash:** 2.359 Aufrufe mit 10.000–30.000 Zeichen Ausgabe (Build, Test, Migration, Log).
- **Subagenten sind kein Problem für das Hauptgespräch:** Ihre Rückgaben sind klein (im Schnitt gut 1.000 Zeichen). Ihre eigenen Transkripte sind groß (bis 46 MB), zählen aber nicht in den Kontext des Hauptgesprächs.

## Verdichtung (Compaction)

- `modelSettings.claude-opus-5-5.autoCompactWindow = 400000` steht schon in der Einstellung. Wirkung gemessen: Von 24 Opus-Sitzungen über 1 MB, die seit dem 11.10.2026 geändert wurden, bleiben 19 bei höchstens 374.000 Token Spitze (meist um 366.000); die übrigen 5 siehe „Lücke 2“. Compactions: 0 bis 28 je Sitzung, bei den langen etwa eine je 70–100 Antworten.
- **Lücke 1: Sonnet 5.5 hatte keine Grenze.** Die Sitzung vom 17.10.2026 (Flare AI Trading, Sonnet) erreichte 962.000 Token Spitze bei nur 2 Compactions. Behoben (siehe Changelog).
- **Lücke 2: Sitzungen, die vor der Einstellung gestartet und später fortgesetzt wurden**, laufen weiter bis nahe 1 Mio. (Beispiele: 08a75455 968k, 923fa7dd 968k, 82bcdd3b 848k mit 0 Compactions am 12.10.). Die Einstellung wird vermutlich beim Sitzungsstart gelesen; das ist **nicht verifiziert**. Praktische Folge: Alte Sitzungen nicht weiterziehen, sondern mit Übergabe neu starten.
- Vorhanden und nicht verändert: `PreCompact`-Hook des Lernloops (sichert den Stand des Lernloops, schreibt nichts in den Kontext), Statusleiste mit Kontextanzeige.

## Immer geladener Kontext

- 293 Agents. **Seit dem 01.10.2026 wurden nur 14 Typen benutzt**, davon die 7 DevOS-Rollen in 698 von 708 Aufrufen. 279 Agents wurden nie gerufen, laden aber ihre Beschreibung in jede Sitzung (laut Auftrag etwa 21k Token). Das ist der größte Einzelposten, den man ohne Qualitätsverlust verkleinern könnte. **Braucht deine Freigabe** (siehe Changelog, Abschnitt „Offen“).
- MCP: 1.110 Werkzeuge sind bereits verzögert geladen (nur Namen), kein weiterer Hebel ohne Funktionsverlust.
- `CLAUDE.md` (global): vorher 16,1 KB, jetzt 18,1 KB. Der neue Abschnitt „Kontext sparen“ kostet etwa 550 Token je Sitzung und soll die Read-/Bash-Ausgaben senken. Ob er sich lohnt, zeigt erst der Vergleich in `CONTEXT_BENCHMARKS.md`.

## Was schon gut ist

Subagent-Rückgaben klein, MCP verzögert geladen, Compaction-Grenze für Opus, Statusleiste, Lernloop-Hooks kurz (Timeouts 10–30 s), Skills nur als Beschreibung geladen.

## Risiken der Vorschläge

| Maßnahme | Risiko | Umkehrbar |
|---|---|---|
| Sonnet-Grenze 400.000 | Etwas mehr Compactions bei langen Sonnet-Läufen | ja, eine Zeile |
| Regeln „Kontext sparen“ | Zu knappe Reads können Zusammenhang verpassen; deshalb steht „ganze Datei, wenn wirklich nötig“ drin | ja |
| Compact Instructions | Zusammenfassung wird länger | ja |
| 279 Agents archivieren | Ein selten gebrauchter Spezialist fehlt bis zur Rückholung | ja, Ordner zurückschieben |
