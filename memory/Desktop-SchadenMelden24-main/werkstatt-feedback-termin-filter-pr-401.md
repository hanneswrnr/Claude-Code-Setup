---
name: werkstatt-feedback-termin-filter-pr-401
description: "Hotfix 13.10.2026 aus Werkstatt-Feedback (mehrtägige Termine mit Uhrzeit, Auftragsliste behält Filter) – PR #401 und Restpunkte PR #402 direkt auf main"
metadata:
  node_type: memory
  type: project
  originSessionId: 709c4bfe-301b-4861-9e4c-fa259c292072
  modified: 2026-10-16T13:19:19.306Z
---

Zwei Pull Requests vom 13.10.2026, beide ohne Migration und beide direkt auf main. Freigabe von Hannes: „sofort auf main“ bzw. „gleich mit auf main“.

**PR #401** (gemergt, 0f7f39373), Zweig fix/werkstatt-feedback-termin-filter:
- „Mehrere Tage…“ geht wieder mit Uhrzeit.
- Die Auftragsliste behält Standort-Filter und Scroll-Stelle.
- Mails und Kundenportal nennen bei mehrtägigen Terminen beide Tage.

**PR #402** (Restpunkte), Zweig fix/termin-mehrtaegig-restgrenzen:
- Im Vorschlagsweg hat jede angebotene Zeit ein eigenes Ende. Die Funktion dafür ist `endeDerZeile`.
- Betreffzeilen und Erinnerungen nennen beide Tage. Der Cron nutzt dafür `lib/email/termin-erinnerung-zeit.ts`.
- Ein abgeleitetes 'express' wird bei ganztägigen oder mehrtägigen Terminen zu 'tages'. Das regelt `lib/termin/express-regel.ts` in allen Schreibwegen, auch bei der Übernahme aus Google (`lib/termin/gcal/pull.ts`).

**Why:** Eine Werkstatt (Standort Weißenfels) hatte beides als Rückschritt gemeldet.

**Restpunkte 16.10.2026** (PR #405, gemergt fa35c20a8, Freigabe Hannes 16.10.):
- Cron `termin-followup-check` steht NICHT in vercel.json und bleibt aus: Hannes 29.09.2026, am 16.10.2026 von Claude bestätigt (übertragen, PR #407). No-Show-Fall deckt `abschluss-vergessen-check` (Glocke, ab letztem Tag) ab. Nicht wieder zum Einschalten vorschlagen.
- No-Show-Mail nennt beide Tage und kommt erst nach dem letzten Tag (`letzterBelegterTag`, `noShowZeitangabe`).
- Alle Termin-Mails schreiben „5. Oktober“ ohne führende Null.
- Wechsel weg von „Mehrere Tage…“ behält die eigenen Enden der weiteren Zeiten.
- Alte mehrtägige Express-Termine: live nur einer, abgeschlossen (16.–17.09.), bewusst nicht geändert.

**How to apply:** Folgende Grenzen sind weiterhin offen:
- Der No-Show-Cron prüft nur `claims`, nicht `werkstatt_auftraege`.
- Das Kundenportal (`lib/kunde/termin-anzeige.ts`) schreibt weiter „01.“.
- Die Kopfzeile in `KundeTerminCard` zeigt bei 22:00–00:00 zwei Tage.
- `berechneScheduledFelder` setzt bei einem Ende um 00:00 den Folgetag als Enddatum.

Neue Schreibwege für Termine müssen `buchungsTypFuerZeitraum` nutzen.

Siehe [[version-4-0-sammelzweig]] (Live-Fehler sofort auf main).
