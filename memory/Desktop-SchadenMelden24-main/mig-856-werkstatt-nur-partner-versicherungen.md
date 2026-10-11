---
name: mig-856-werkstatt-nur-partner-versicherungen
description: "Mig 856 LIVE seit 02.10.2026, PR #288 gemergt (d6b2fe3ae) — Werkstatt sieht nur Versicherungen mit Zusammenarbeit, „Alle entdecken“ entfernt, Sperr-Trigger gegen Selbst-Freischaltung"
metadata:
  node_type: memory
  type: project
  originSessionId: 0a5407aa-ed6e-4fb0-9377-5bbd1d6aef84
  modified: 2026-10-02T16:00:55.203Z
---

PO-Entscheidung 01.10.2026: Werkstatt sieht nur Vermittler/Versicherungen mit Zusammenarbeit (Schadenfall an eigenem Standort oder eigener Auftrag mit versicherung_id); Tab „Alle entdecken“ entfernt. Auch Auswahllisten (Registrierter Vertreter, Zugewiesene Agentur, Provisionssätze) zeigen nur Partner — allein per RLS.

Stand 02.10.2026: Mig 856 LIVE („856-TEST OK“ gegen Live-Stand, Ledger 856), PR #288 gemergt (Merge d6b2fe3ae). Enthält Hilfsfunktion werkstatt_hat_zusammenarbeit(uuid), engere versicherungen_select_policy, get_agentur_vermittler für Werkstatt nur Partner, Sperr-Trigger zzz_versicherung_nur_mit_zusammenarbeit (BEFORE, alphabetisch letzter) auf werkstatt_auftraege und kunden_versicherung. Wächter erlaubt spätere ALTER POLICY nur in 858_hq_versicherungen_nur_id_firma.sql (andere Sitzung, entfernt HQ-Zweig).

**Why:** Vorher las jede Werkstatt alle 40 Versicherungen samt IBAN; ohne Sperr-Trigger hätte sie sich per fremder versicherung_id selbst freischalten können.
**How to apply:** Neue BEFORE-Trigger auf den zwei Tabellen dürfen nicht hinter zzz_ sortieren; neue Leseregeln auf versicherungen brauchen die Hilfsfunktion und einen Eintrag in der Wächter-Freigabeliste. Rückweg erst nach 858. Siehe [[supabase-standardrechte-30-10-waechter]].
