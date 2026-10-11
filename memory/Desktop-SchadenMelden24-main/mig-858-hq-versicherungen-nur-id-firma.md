---
name: mig-858-hq-versicherungen-nur-id-firma
description: "Mig 858 LIVE seit 02.10.2026, PR #290 gemergt (834b4ba34) – HQ liest versicherungen nur als id+firma über hq_provision_versicherungen (aal2), get_agentur_vermittler nur Berechtigte, HQ-Provision nur mit Zusammenarbeit; PR #290"
metadata:
  node_type: memory
  type: project
  originSessionId: d028da4f-a655-4974-af8b-8642246e8c56
  modified: 2026-10-02T16:37:50.796Z
---

Mig 858 (`hq_versicherungen_nur_id_firma`) ist seit 02.10.2026 live (Ledger, „858-TEST OK“), App-Teil in PR #290, gemergt 02.10.2026 als 834b4ba34 (Zweig `fix/hq-versicherungen-nur-id-firma`, Worktree nach dem Merge entfernt; Live-Bau 834b4ba34 fertig). Baut auf Mig 856 auf ([[mig-856-werkstatt-liest-nur-partner-versicherungen]]).

- HQ-Zweig der Leseregel `versicherungen_select_policy` entfernt (griff live nie, weil `profiles_select_policy` nur das eigene Profil zeigt – schlummernde Lücke).
- HQ bekommt Namen nur über `hq_provision_versicherungen()` (SECDEF, id+firma, nur eigene Vorgaben, verifiziert + aktiv + aal2).
- `get_agentur_vermittler`: nur Werkstatt mit Zusammenarbeit, Admin, Inhaber der eigenen Agentur, Server ohne Nutzer. Vermittler bekommen 0 Zeilen.
- Produktentscheidung Hannes 01.10.2026: HQ-Provision mit registrierter Versicherung nur, wenn eine Werkstatt des Verbunds zusammenarbeitet (`gruppe_hat_zusammenarbeit`, nur service_role; Trigger `zz_gruppen_provision_nur_partner` → 23514).

**Why:** Folgepunkte M1/2 aus der 856-Sicherheitsprüfung; keine Werkstatt/kein Verbund soll fremde Versicherer sehen.
**How to apply:** Neue HQ-Leser von Versicherungsdaten nur über SECDEF-Funktionen mit aal2-Tor; der 856-Wächter erlaubt `ALTER POLICY versicherungen_select_policy` nur in der Datei 858 – spätere Änderungen brauchen eine Freigabeliste-Anpassung dort. `scripts/verify-856-…` endet nach 858 erwartungsgemäß mit „856-TEST FAIL 5“.
