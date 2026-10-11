---
name: rechtsdokument-mustervorlagen-pr-303
description: "Sieben geprüfte Mustervorlagen ersetzen die BEISPIEL-Rechtsdokumente (PR #303, ADR 0033), GEMERGT 03.10.2026 (8e4b0b6ce); Prüfung ohne Anwalt, Anwalt aus Kostengründen zurückgestellt"
metadata:
  node_type: memory
  type: project
  originSessionId: 79e49eb5-76ab-4af7-aa02-f88cc221f9bd
  modified: 2026-10-03T00:22:52.345Z
---

PR #303 (Zweig feat/rechtsdokument-vorlagen-geprueft) am 03.10.2026 nach Freigabe gemergt, Merge-Commit 8e4b0b6ce. Sieben Mustervorlagen (Fassung MUSTER_STAND 10/2026) in lib/rechtsdokumente/muster/ ersetzen die sechs BEISPIEL-Vorlagen: Reparaturauftrag, KV-Freigabe, Zahlungsanweisung (statt Abtretung), Leihvertrag Ersatzfahrzeug, Probefahrtvereinbarung, Datenschutzhinweise, Einwilligung Erinnerungen/Angebote. Eingabemaske (MusterEingaben.tsx), Feldart bestaetigung, PDF-Kopf mit Werkstattname. Keine Migration. ADR 0033, Prüfbericht wiki/09-Operations/Rechtsdokument-Mustervorlagen-Pruefung.md.

**Why:** Hannes hat keinen Anwalt und hat Prüfung und Freigabe an Claude übertragen („musst du alle prüfen und absegnen“). Seine Entscheidungen: Hinweis nur für Werkstatt, Zahlungsanweisung, Eingabemaske, Datenschutzhinweise plus Einwilligung. Eine anwaltliche Durchsicht befürwortet er, stellt sie aber aus Kostengründen zurück (03.10.2026). Nicht erneut drängen; erst wieder vorschlagen, wenn Budget da ist oder die Texte rechtlich kippen.

**How to apply:**
- Textänderungen nur per PR, mit MUSTER_STAND-Erhöhung und Nachtrag im Prüfbericht.
- Nie wieder „(BEISPIEL)“ für Muster.
- Folgeaufgaben stehen im Todo .planning/todos/pending/rechtsdokumente-folgeaufgaben.md, fällig 04.10.2026: Löschfristen (zuerst), Plattform-Rechtstexte, aria an Select/DatePicker/TimePicker.

Verwandt: [[rechtsdokument-entwurf-oeffnen-loeschen-pr-298]].
