---
name: loeschfristen-kundendaten-mig-865
description: "Löschfristen Werkstatt-Kundendaten (Mig 865, Zweig feat/loeschfristen-kundendaten) — Entscheidungen Hannes 03.10.2026; Stand Bau/Einspielen"
metadata:
  node_type: memory
  type: project
  originSessionId: b1d5046e-a8f0-4e32-b180-94be9d785858
  modified: 2026-10-03T11:44:42.802Z
---

Löschfristen für Werkstatt-Kundendaten, Migration 865 (863/864 waren von anderen Sitzungen belegt), Zweig `feat/loeschfristen-kundendaten`, Bauvertrag `.planning/features/loeschfristen/KONZEPT.md`. Stand 03.10.2026: Mig 865 LIVE (Probelauf und Prüfskript live 865-TEST OK, Ledger 865), PR #309 GEMERGT (c85c4f30a). 31 verwaiste Altdateien per scripts/einmalig-865-verwaiste-auftragsdateien.sql vorgemerkt (Freigabe Hannes). Erste echte Löschungen frühestens 2029.

Entscheidungen Hannes 03.10.2026 (alle je Empfehlung):
1. Automatisch löschen (nächtlicher Cron), Vorschau 90 Tage in Einstellungen → Datenschutz.
2. Löschsperre je Kunde mit Pflicht-Grund und Enddatum ≤ heute + 3 Jahre.
3. Unterschriebene Rechtsdokumente 6 Jahre ab Ende Unterschriftsjahr, `abtretungserklaerung` 8 Jahre (nicht anwaltlich geprüft).
4. Kundenkartei Vorgabe 3 Jahre nach letztem Auftrag, 1–10 je Werkstatt, sofort für alle aktiv; Hinweis in die nächste AV-Vertrag-Änderung (AGB-Runde 09.11. schon mitgeteilt; Todo loeschfristen-folgeaufgaben).

**Why:** Mustervorlage „Datenschutzhinweise“ (PR #303) verspricht „Anschließend löschen wir sie“; vorher löschte nichts automatisch, unterschriebene Dokumente gar nicht (ADR 0032, Mig 845), und Dateien gelöschter Eigenaufträge blieben im Speicher (live 31 Dateien in 17 Ordnern verwaist; 6 weitere PDFs dort sind Gutschriften von Versicherungen).

**How to apply:** Migrationsdatei 865 nicht mehr ändern; Änderungen nur per neuer Migration. Folge-Todo `.planning/todos/pending/loeschfristen-folgeaufgaben.md` (AV-Klausel, 31 verwaiste Dateien, Anonymisierung leert Sperre nicht, Kalender).  Löschen unterschriebener Dokumente nur über SECDEF `loeschfristen_anwenden()` nach Fristende (Eigentümerweg), Trigger 844/845 bleiben unverändert. Einspielen: erst Migration 865 (Freigabe Hannes), dann App-Merge. Einmaliges Aufräumen der verwaisten Dateien = eigene Freigabe. Verwandt: [[mig-844-845-unterschriebenes-endgueltig]], [[rechtsdokument-mustervorlagen-pr-303]].
