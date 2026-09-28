---
name: mig-784-standorte-delete-nur-server
description: "Mig 784 (DELETE-Regel und DELETE-Recht auf werkstatt_standorte für anon/authenticated weg) LIVE seit 28.09.2026, PR #220 gemergt"
metadata:
  node_type: memory
  type: project
  originSessionId: eb502487-d9e3-4bbe-8a07-1bf14fa011d0
  modified: 2026-09-28T19:57:03.684Z
---

Mig 784 entfernt `werkstatt_standorte_delete_policy` und entzieht anon/authenticated DELETE auf
`werkstatt_standorte` (Umweg an `DELETE /api/werkstatt/standorte` vorbei). **Live seit 28.09.2026**
(Freigabe von Hannes; Probelauf und Prüfskript live „784-TEST OK“, Ledger 784), PR #220 gemergt
(a8271663), Vercel-Produktionsbuild grün. Direktes Löschen als Nutzer scheitert jetzt mit 42501.

**Why:** Löschen nur über die Route, damit Hauptstandort-Regel und Stripe-Abgleich greifen.

**How to apply:** Neuer App-Code darf Standorte nur mit Service-Client in `app/api` löschen (Wächter
`lib/werkstatt/__tests__/migration-784-…`). Notfall: `scripts/rueckweg-784-…sql`, danach Ledger
784 entfernen. Offene Nebenbefunde (anon INSERT/UPDATE, Hauptstandort-Wechsel nicht atomar,
Admin-INSERT-Regel) als Folgeaufgabe vorgeschlagen. Verwandt: [[nebenbefunde-768-mig-776-777]].
