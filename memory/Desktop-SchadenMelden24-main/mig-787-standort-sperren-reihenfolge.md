---
name: mig-787-standort-sperren-reihenfolge
description: "Mig 787 live seit 29.09.2026 (PR #229) — Trigger 768/774 sperren Standorte sortiert, Schadenfall danach; Eigenauftrag-Kreis mit Mig 788 behoben"
metadata:
  node_type: memory
  type: project
  originSessionId: 073a0f0e-f97f-471f-90f6-8a1b3e724209
  modified: 2026-09-29T21:14:33.634Z
---

Mig 787 ist seit 29.09.2026 live (Freigabe Hannes, Probelauf und verify-787/768/774 OK, Ledger 787, PR #229). `zz_termin_vorschlag_gleiche_werkstatt` und `zz_warteliste_auftrag_gleiche_werkstatt` sperren ihre zwei Standorte in einer Anweisung `ORDER BY s.id FOR SHARE`, auf dem Schadenfall-Pfad vor dem Schadenfall; Eigenauftrag-Pfad von 774 bewusst wie vorher (Auftrag vor Standort, wie Trigger aus Mig 760).

**Why:** Mit `werkstatt_hauptstandort_setzen` (Mig 786, sortiert NO KEY UPDATE) gab es 40P01; im Container zusätzlich ein Kreis zu dritt (Warteliste sperrte Schadenfall vor Standorten, Vorschlag danach).

**How to apply:** Neue Stellen, die mehrere Standortzeilen sperren: eine Anweisung, nach id, beim Schadenfall vor dem Schadenfall. Folgepunkt Eigenauftrag erledigt mit [[mig-788-eigenauftrag-sperr-reihenfolge]] (live 30.09.2026). Wächter `lib/termin/__tests__/migration-787-*` hält Live-md5 und Datei-md5 fest. Verwandt: [[mig-786-standorte-folgebefunde]], [[nebenbefunde-768-mig-776-777]].
