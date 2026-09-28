---
name: mig-775-gruppen-angemeldete-spaltenrechte
description: "Mig 775 (gruppen_public_select_active nur anon, Funktion oeffentliche_werkstatt_gruppen, MV nur service_role) auf Zweig fix/gruppen-angemeldete-spaltenrechte, PR #211, NICHT live; Reihenfolge Migration vor Merge"
metadata:
  node_type: memory
  type: project
  originSessionId: 55a81de6-a077-4e3e-8567-795de8be840e
  modified: 2026-09-27T23:12:07.871Z
---

Stand 28.09.2026: Mig 775 **live seit 28.09.2026** (Freigabe Hannes; Probelauf und Prüfskript live „775-TEST OK“, Ledger 775; öffentliche Schnittstelle: rpc 200 mit 4 Schlüsseln, MV 401). PR https://github.com/hanneswrnr/SchadenMelden24/pull/211 mit Freigabe zum Merge. Migrationsdatei nach dem Einspielen nicht mehr ändern. Hannes hat entschieden: offizielle Standorte bleiben für Konten außerhalb des Verbunds sichtbar → Folge-Migration (nur gelistete Verbünde, ohne werkstatt_id/status) steht im Todo.

**Why:** Jedes angemeldete Konto las alle 43 Spalten gelisteter Werkstatt-Gruppen und die ganze Sicht mv_werkstatt_mit_aktivem_branding (Folgebefund zu [[mig-772-gruppen-anon-spaltenrechte]]).

**How to apply:** Erst nach Freigabe von Hannes einspielen (Probelauf per awk-Rezept im Kopf von scripts/verify-775-…sql, Migration per execute_sql, Ledger 775, Prüfskript „775-TEST OK“), ERST DANACH PR #211 mergen — der App-Code ruft rpc('oeffentliche_werkstatt_gruppen'). Rückweg 775 muss den Stand nach Mig 777 herstellen (authenticated auf der MV nur arwd). Folgebefunde (offizielle Standorte, ist_branding_sichtbar, Hinweis bei nicht gelisteten Verbünden) im Todo `.planning/todos/pending/verbund-folgebefunde-nach-mig-775.md`. Verwandt: [[schadenmelden24-commit-regeln]].
