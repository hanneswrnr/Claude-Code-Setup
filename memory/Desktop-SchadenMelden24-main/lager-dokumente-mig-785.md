---
name: lager-dokumente-mig-785
description: "Lager-Dokumente (PDF/Word/Excel/Fotos an Lager-Positionen), Mig 785 LIVE seit 28.09.2026, PR 221 gemergt (f7612a6c)"
metadata:
  node_type: memory
  type: project
  originSessionId: f484cb4a-7e2d-43cd-a653-160aac7f853c
  modified: 2026-09-28T20:01:26.387Z
---

Am 28.09.2026 gebaut und live: Werkstaetten koennen an Lager-Positionen Dokumente haengen (Spalte `werkstatt_lager_bestand.dokument_pfade`, max. 10; Bucket `lager-teile` 4 MB mit PDF/DOCX/XLSX/Bildern; Route `/api/werkstatt/lager/dokument`). Anlass: Kunden-Feedback Triccon 23.09.2026. Mig 785 live nach Freigabe von Hannes (Probelauf und verify-785 „785-TEST OK“, Ledger 785), hanneswrnr/SchadenMelden24#221 gemergt als f7612a6c.

**Why:** Dokumente liegen im selben Werkstatt-Ordner wie die Bilder, damit Storage-RLS und Kontoloeschung (Ordner-Scan) ohne Sonderfall greifen; sie sind getrennt von `bild_pfade`, damit nichts ins Vorschaubild oder den Marktplatz gelangt.

**How to apply:** Neue Lager-Dateiarten ueber `lib/lager/dokumente.ts` (Browser und Server gemeinsam) und den Bucket-Whitelist per neuer Migration erweitern. Bekannt offen: Standort-Loeschen laesst lager-teile-Dateien liegen (Aufgaben-Chip „Lager-Dateien beim Standort-Loeschen aufraeumen“); nicht entfernbare Objekte bleiben bis zur Kontoloeschung (N1 teilweise). Verwandt: [[schadenmelden24-commit-regeln]].
