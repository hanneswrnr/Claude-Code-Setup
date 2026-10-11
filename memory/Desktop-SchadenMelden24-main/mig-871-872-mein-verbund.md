---
name: mig-871-872-mein-verbund
description: "Mig 871/872 LIVE seit 03.10.2026 — Mitglieds-Werkstätten lesen ihren Verbund nur über mein_verbund() (24 Spalten); PR #317 und Doku-PR #318 gemergt"
metadata:
  node_type: memory
  type: project
  originSessionId: a3a5576d-fd13-4338-b4ec-c233fb287de9
  modified: 2026-10-03T22:06:10.863Z
---

Hannes hat am 03.10.2026 für die Datenbank-Seite des Befunds „Mitglieder lesen ihre Verbund-Zeile mit allen 43 Spalten“ die **schmale Funktion** gewählt (nicht Tabellen-Aufteilung, nicht Server-only, nicht „so lassen“). Eine erste Antwort „Tabelle aufteilen“ kam an, ohne dass er die Frage gesehen hatte — verworfen und neu gefragt.

**Stand: LIVE seit 03.10.2026** (Freigabe „Alle 3 freigegeben“): Mig 871 `mein_verbund()` eingespielt (871-TEST OK) → PR #317 gemergt (Merge 7e4a09bed, Live-Build ok) → Mig 872 eingespielt (872-TEST OK, verify-867 und verify-775 OK). Ledger 871 und 872. Doku-PR #318 (`docs/mein-verbund-live`, nur Wiki/CLAUDE.md/Todo) mit Freigabe am 04.10.2026 gemergt (d69babd78). Bericht `wiki/09-Operations/Security-Audits/2026-10-03-verbund-mitglieder-lesen-schmal.md`.

**Why:** Verwaltungsdaten (USt-ID, Kontakt der Zentrale, Service-Level) sollen Mitglieder nicht sehen; App brauchte sie seit PR #315 schon nicht mehr.

**How to apply:** Neue Mitglieder-Leser nur über `leseMeinVerbund` (`lib/werkstatt-gruppe/mein-verbund.ts`); direkte Abfragen/Einbettungen von `werkstatt_gruppen` liefern Mitgliedern `null` (Wächter `mitglieder-verbund-lesen.test.ts`). Weitere Felder nur per Migration in die Funktion; neue RESTRICTIVE-Regeln auf werkstatt_gruppen auch in `mein_verbund()` nachbilden (Wächter migration-871 meldet sie). Rückweg: rueckweg-872 → App zurück → rueckweg-871. Nebenbefunde (Todo-Punkte 4/5) mit Mig 874 erledigt, live seit 04.10.2026 (PR #320): anon ohne EXECUTE an `_user_ist_gruppen_mitglied` und ohne Rechte an tickets_eskalation_candidates/v_werkstatt_gruppen_service_level_compliance; Suchpfad der Funktion bewusst unverändert (Prüfsumme in verify-872/rueckweg-872). Verwandt: [[mig-867-hq-kontext-ohne-ausnahme]], [[branding-browser-schmal-pr-315]], [[mig-775-gruppen-angemeldete-spaltenrechte]].
