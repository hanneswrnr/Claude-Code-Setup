---
name: provision-nur-server-mig-630
description: "Stand 20.09.2026 — Migration 630 live in Prod (Pruefskript bestanden), Frontend auf main (b01d2f71); Migration 635 (Restpunkte) gepusht auf fix/provision-restpunkte und wartet auf PO-Freigabe; Provisionsbetrag kommt nur noch aus der DB"
metadata: 
  node_type: memory
  type: project
  originSessionId: e8004b9b-eeb4-4f6b-8264-01c3762771de
  modified: 2026-09-19T19:36:16.205Z
---

Vorgezogener Auftrag aus Konzept 02 (Provisionen/Vertreter, §8 Nr. 14), siehe [[nutzerfuehrung-gesamtplanung]]. Erledigt am 19.09.2026.

- **Live:** Migration `630_provision_nur_server` in Prod (schema_migrations 20260919192156, über apply_migration). Frontend auf main (Merge b01d2f71, Branch `fix/provision-nur-server`). Prüfskript `scripts/verify-provision-nur-server-630.sql` gegen Prod bestanden, alle Teile mit Daten, keine Reste.
- Browser schreibt `provision_amount` nicht mehr; Anzeige nur über `lib/provision/betrag.ts::provisionsBetrag`. DB rechnet beim Wechsel in Fertig-Status neu; bezahlte/abgerechnete Posten nie; `provision_neu_berechnen()` für bewusstes Nachrechnen (noch ohne Knopf); Agentur liest `werkstatt_provision_configs` nur noch.
- **PO-Entscheidungen 19.09.2026:** Verbund ohne Pflicht-Satz = 0 € (PO ließ mich entscheiden; beide Verbund-Mitglieder in Prod sind Testkonten); 13 Aufträge mit alten Startwerten 50/20 € bleiben; 2 bezahlte Aufträge mit 0 € bleiben; keine Nachberechnung der 12 Null-Beträge.
- **Restpunkte (PO 19.09.2026 abends: "alle offenen Aufgaben"):** Branch `fix/provision-restpunkte` gepusht am 20.09.2026 (Commits 1c70f951 Code+Migration, 56f246f2 Doku), Migration `635_provision_restpunkte.sql` (Nummer 632 gehoert der Sitzung E-Mail-Wechsel): Trigger `aac_werkstatt_felder_schuetzen` (Schadensart + Bestaetigung + Bezahlt-Stand nur Werkstatt bzw. SECURITY-DEFINER), Flotten-Prozent-Paid-Guard, stiller Alt-Recalc der Tabelle standort_provision_configs entfernt, neue Funktion `provision_mit_mwst(p_versicherung_id)`. Befund: Mig 533 war NIE in Prod (live lief noch 014 mit v2, ueberschrieb auch bezahlte Posten). Probelauf 635 auf Prod mit Rueckrollen bestanden (ohne 635 gelingen alle sechs Angriffe, mit 635 keiner), NICHT eingespielt. UI: Verbund-Mitglieder werden auf Einstellungen -> Provisionen geleitet, MwSt der Abrechnung kommt im Verbund aus der Zentrale (`lib/provision/verbund.ts`); toter Rueckweg in lib/vermittler/aggregation.ts entfernt. Nachweis 20.09.2026: type-check 0 Fehler, 3244 Tests gruen, Build gruen (lokal nur mit Platzhalter-Env, weil keine .env.local existiert). Wartet auf PO-Freigabe (Migration einspielen + Merge nach main).

- Weiter offen (gehört zum großen Konzept 02): Zahlung als eigenes Ding (Stufe 1, payment_status setzt heute die Werkstatt); feste Startwerte 10/50/20/20 € für Aufträge ohne Satz (Stufe 3); Reiter und Liste zählen Eigenaufträge über verschiedene Filter.

**Why:** Geld- und Sicherheitsbefund, vom PO vorgezogen.
**How to apply:** Neue Provisions-Arbeit baut darauf auf; nie wieder `provision_amount` aus dem Browser schreiben (Test `betrag.test.ts` schlägt an). Prod-Zugriff über den claude.ai-Supabase-Konnektor (UUID-Werkzeuge); Vercel-Konnektor hat keinen Zugriff auf Deployments, Status über `gh api .../commits/<sha>/status`. Siehe auch [[prod-db-drift-feat-ai-features]], [[werkstatt-freischaltung-mig-620]].
