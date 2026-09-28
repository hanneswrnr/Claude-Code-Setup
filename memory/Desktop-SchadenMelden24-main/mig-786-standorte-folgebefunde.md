---
name: mig-786-standorte-folgebefunde
description: "Mig 786 (werkstatt_standorte: anon ohne INSERT/UPDATE, Admin-INSERT-Regel weg, Hauptstandort nur per RPC werkstatt_hauptstandort_setzen) gebaut auf Zweig fix/werkstatt-standorte-folgebefunde, NICHT live, wartet auf Freigabe"
metadata:
  node_type: memory
  type: project
  originSessionId: 0878a340-2aff-4e98-b2e4-ce59f7b4bdf9
  modified: 2026-09-28T21:44:02.944Z
---

Mig 786 schließt die drei Nebenbefunde aus [[mig-784-standorte-delete-nur-server]]: `anon` verliert
INSERT/UPDATE, `werkstatt_standorte_insert_policy` (Admin, Mig 653) fällt weg und `authenticated`
verliert INSERT, eindeutiger Teilindex `werkstatt_standorte_ein_hauptstandort`, SECURITY-DEFINER-RPC
`werkstatt_hauptstandort_setzen(uuid)` (FOR NO KEY UPDATE, fremd/unbekannt → PT404), Trigger
`zz_standort_hauptstandort_schutz` blockt direkte `is_primary`-Änderung durch anon/authenticated.
App: `StandortManageModal.handleSetPrimary` ruft den RPC. Stand 28.09.2026: gebaut, Container 225
PASS, Vorprüfung live READ ONLY bestanden, Sicherheit freigegeben, Korrektheit freigegeben (Doku-
Auflagen erledigt), Zweig gepusht. **Nicht eingespielt.**

**Why:** Hauptstandort-Wechsel war nicht atomar und `is_primary` frei änderbar; Admin-Direktanlage
umging den Stripe-Abgleich (ADR 0014).

**How to apply:** Ausrollen nur nach Freigabe von Hannes: erst Migration live (Skill sm24-migration
Schritt 9), dann SOFORT den PR mergen — dazwischen scheitert „Als Haupt“ in der alten Oberfläche
(ohne Datenschaden). Offene Folgeaufgaben (Chips): Wettlauf in DELETE /api/werkstatt/standorte,
Sperr-Reihenfolge in den Triggern aus Mig 768 und 774. Prüf-Agenten haben keinen DB-Zugang.
