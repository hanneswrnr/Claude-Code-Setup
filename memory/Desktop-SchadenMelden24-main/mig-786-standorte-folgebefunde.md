---
name: mig-786-standorte-folgebefunde
description: "Mig 786 (werkstatt_standorte: anon ohne INSERT/UPDATE, Admin-INSERT-Regel weg, Hauptstandort nur per RPC werkstatt_hauptstandort_setzen) LIVE seit 28.09.2026, App über PR #225"
metadata:
  node_type: memory
  type: project
  originSessionId: 0878a340-2aff-4e98-b2e4-ce59f7b4bdf9
  modified: 2026-09-28T22:00:19.400Z
---

Mig 786 schließt die drei Nebenbefunde aus [[mig-784-standorte-delete-nur-server]]: `anon` ohne
INSERT/UPDATE, `werkstatt_standorte_insert_policy` (Admin, Mig 653) weg und `authenticated` ohne
INSERT, eindeutiger Teilindex `werkstatt_standorte_ein_hauptstandort`, SECURITY-DEFINER-RPC
`werkstatt_hauptstandort_setzen(uuid)` (FOR NO KEY UPDATE, fremd/unbekannt → PT404), Trigger
`zz_standort_hauptstandort_schutz` blockt direkte `is_primary`-Änderung durch anon/authenticated.
**Live seit 28.09.2026** (Freigabe Hannes „3. freigegeben“; Probelauf und Prüfskript live
„786-TEST OK“, Ledger 786). App (`StandortManageModal.handleSetPrimary` → RPC) über PR #225,
gemergt am 28.09.2026 (d89e5e06).

**Why:** Hauptstandort-Wechsel war nicht atomar und `is_primary` frei änderbar; Admin-Direktanlage
umging den Stripe-Abgleich (ADR 0014).

**How to apply:** Neuer Code darf `is_primary` als Nutzer nur über den RPC ändern (Wächter
`lib/werkstatt/__tests__/migration-786-…`); Standorte anlegen nur per Service-Client/SECDEF.
Notfall: `scripts/rueckweg-786-…sql` (dann auch App zurück), Ledger 786 entfernen. Offene
Folgeaufgaben (Chips): Wettlauf in DELETE /api/werkstatt/standorte, Sperr-Reihenfolge in den
Triggern aus Mig 768 und 774. Prüf-Agenten haben keinen DB-Zugang.
