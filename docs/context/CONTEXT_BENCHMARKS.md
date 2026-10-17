# CONTEXT_BENCHMARKS — Messwerte und was fehlt

## Ausgangswerte (gemessen, 17.10.2026)

| Messgröße | Wert | Quelle |
|---|---|---|
| Spitzen-Kontext Opus-Sitzungen, die die 400k-Grenze hatten | meist 322k–374k (19 von 24) | `tools/ctx_probe.py` |
| Spitzen-Kontext ohne wirksame Grenze | 504k, 837k, 848k, 968k, 968k (Opus); 962k (Sonnet) | dito |
| Compactions je Sitzung (lange Opus-Sitzungen) | 14 in 1.353 Antworten, 28 in 2.055 | dito |
| Wiederholte Reads in großen Sitzungen | 37 %, 27 %, 48 % (66/180, 21/78, 42/87) | dito |
| Reads über 30.000 Zeichen seit 01.10. | 594 (36 % aller Read-Zeichen) | `tools/ctx_aggregate.py` |
| Bash-Ausgaben 10.000–30.000 Zeichen seit 01.10. | 2.359 | dito |
| Agent-Typen benutzt | 14 von 293 | dito |

## Nachher-Werte

**Noch nicht vorhanden.** Die Einstellung und die Regeln wirken erst in neuen Sitzungen. Ich habe keine Nachher-Messung erfunden und keinen kontrollierten A/B-Lauf mit gleichen Aufgaben gemacht (Kosten und Zeit, keine saubere Wiederholbarkeit für reale Projektarbeit).

## So wird nachgemessen (in zwei Wochen)

```
python -I tools/ctx_aggregate.py 2026-10-18
```

Erwartung, **nicht Zusage:** weniger Reads ≥ 30.000 Zeichen, weniger wiederholte Reads, Sonnet-Sitzungen unter etwa 400k Spitze. Gegenprobe Qualität: Anzahl Korrekturen des Nutzers und neue Lernloop-Lektionen vom Typ „Fehler vermeiden“ je Woche, Test- und Prüf-Gate-Ergebnisse. Steigen diese, die Regeln lockern.

## Nicht belegt

- Dass 45 %, 55 % oder 65 % besser sind als 400k bei Opus.
- Dass die Regeln „Kontext sparen“ die Qualität unverändert lassen. Das Ziel „30–60 % weniger Messages“ ist deshalb nicht gezeigt.
- Ob `autoCompactWindow` in laufenden Sitzungen neu gelesen wird.
- Kosten: Weniger aktiver Kontext senkt nicht automatisch die Gesamtkosten (Cache, mehr Verdichtungen).

## Weitere Möglichkeiten

Agents archivieren (~20k Token), Subagenten-Modell prüfen, Statusleiste um eine Warnung bei Kontext über 300k ergänzen.
