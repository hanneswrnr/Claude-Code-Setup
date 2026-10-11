---
name: kalender-alle-rollen-pr-319
description: "Kalender für alle Rollen mit Google-Abgleich, Zweig feat/kalender-alle-rollen-google, PR #319; Mig 873 + 875 (Farben wie Google) LIVE seit 04.10.2026; Merge braucht Hannes; danach E2E-Klicktest im Testkonto gewünscht"
metadata:
  node_type: memory
  type: project
  originSessionId: 08a75455-f680-49af-a601-2bd875c47059
  modified: 2026-10-04T18:02:11.775Z
---

Stand 04.10.2026: Kalender für alle Rollen (Werkstatt umgebaut, Versicherung+Vermittler kostenlos, Spediteur, HQ, Admin) mit Google-Abgleich auf `feat/kalender-alle-rollen-google`, PR #319 offen. **Mig 873 und Mig 875 live seit 04.10.2026** (875: Terminfarben farbe_id/farbe_hex/farbe_ausstehend, kalender_farbe, Standortfarbe = `werkstatt_standorte.gcal_color_id` mit den 11 Google-Farben, Trigger `standort_farbe_vorbelegen`, Sicherung `mig_875_standort_farben_vorher`). Weitere Runde 04.10.: Optik (Linien auf Grau, bündige Spalten, Heute im Rollen-Verlauf, buntes Google-G per CSS), Standortfarben app-weit = Google-Palette (lib/kalender/google-farben.ts, lib/standort/farben.ts), automatischer Abgleich beim Zurückkehren in den Tab und alle 5 Min, AGB § 15 ohne „Online-Kalender“ (Stand 4. Oktober 2026), DSE 7.2 um Farben ergänzt (Freigabe Hannes für den Zusatz noch offen).

**Why:** Aufträge Hannes 03./04.10.2026 („1 zu 1 wie im Google Kalender“, buntes G — Hannes: „Entscheide du“ → buntes G trotz Markenrichtlinie, Risiko: Google verlangt Entfernung).

**Stand 04.10.2026:** Nachbesserungen fertig, drei Prüfrunden (Korrektheit + Sicherheit „annehmbar“), neu: Farbabgleich schon übertragener Google-Termine (`lib/termin/gcal/farbabgleich.ts`, pull-now `{farbabgleich:true}` mit eigener Drossel 6/60 s, Cron stündlich), main mit Mig 874 hereingeholt, gepusht mit [vorschau] (ee5cf2def). Offen nach Todo `.planning/todos/pending/kalender-pr-319-fortsetzen.md`: E2E-Klicktest (Chrome war am 04.10. zuerst nicht verbunden; Google-Anmeldung geht in der Vorschau nicht), Freigaben DSE-Zusatz + Merge, Anleitung Google-Console.

**Stand 04.10.2026 abends:** DSE-Zusatz 7.2 freigegeben. Klicktest Werkstatt/Versicherung/Vermittler/Spediteur im eingebauten Browser erledigt (Funde E1–E6 behoben, Testdaten gelöscht). main mit Mig 876–880 hereingeholt. Vorschau e1c318b00 scheiterte im Vercel-Build (Browser-Datei importierte Konstante aus Server-Modul sperre.ts) → behoben in db2a35f69 [vorschau], neuer Wächter `lib/termin/__tests__/gcal-server-module-nicht-im-browser.test.ts`. Google-Console-Anleitung als Todo `google-console-kalender-berechtigungen.md`. Danach dc786ffe8 [vorschau]: Datum 04.10. statt 05.10. (Sitzung hatte „morgen“ aus dem Todo übernommen), Wächter schneller. Spediteur-Zweig: Datumskorrektur nur lokal committed, nach Merge von #326 direkt auf main. Offen: Klicktest Verbund-Zentrale/Admin (falls Testkonten), Merge-Freigabe.

**How to apply:** Merge erst nach Hannes' Freigabe; danach Produktions-Build prüfen und den gewünschten E2E-Klicktest im Testkonto über Claude in Chrome (keine Passwörter eingeben; Testdaten danach löschen). Schalter `KALENDER_GOOGLE_AUFGABEN_ENABLED` und `KALENDER_GOOGLE_FARBEN_ENABLED` erst nach Google-Console-Freigabe der Umfänge `tasks`, `calendar.calendarlist.readonly`, `calendar.calendars.readonly`. Nicht gegen echtes Google getestet (Labels, Serien-Echo). Sicherungstabelle 875 später löschen. Rückweg 875 vor 873; App zuerst zurück. Siehe [[schadenmelden24-commit-regeln]].
