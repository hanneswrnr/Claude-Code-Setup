---
name: mig-867-hq-kontext-ohne-ausnahme
description: "Mig 867 LIVE seit 03.10.2026 (App-Teil PR #312 gemergt 2da548923, dann 867); Doku-PR #313 gemergt (0ea3f8bb5); App-Rollback nur nach Rückweg 867"
metadata:
  node_type: memory
  type: project
  originSessionId: c45a184a-541d-47f9-8903-7ccc96f00672
  modified: 2026-10-03T15:30:14.402Z
---

Zweig `fix/hq-kontext-aal1`, Worktree `C:/Users/hanne/sm24-hq-kontext`, PR hanneswrnr/SchadenMelden24#312 gemergt 03.10.2026 (2da548923), Live-Build fertig, danach **Mig 867 LIVE seit 03.10.2026** (Probelauf + verify-867/866 live OK, Ledger 867). Todos in completed/, Doku-PR #313 gemergt 03.10.2026 (0ea3f8bb5), Worktree aufgeräumt.

- App: `resolveCurrentGruppeContext` ohne aal2 nur auf `/werkstatt-gruppe/einstellungen` per Dienstschlüssel (4 Spalten, feste Filter); unterscheidbare Form über `zweiteStufe`; Browser nur `HqBrowserKontext`; HQ-Seiten nutzen `resolveHqSeitenKontext()` (leitet ohne aal2 zur Einrichtung, ohne Login zu /login).
- Mig 867: zwei Regeln `hq_zweiter_faktor_select` pauschal, REVOKE EXECUTE `gruppen_ticket_praefix_vorschlag(uuid)`. Live nur lesend: Vorprüfung OK.
- Container 867 116/0, 866 144/0, vitest 17 092/0, beide Prüfer freigegeben.

**Why:** Ohne App-Stand käme eine Zentrale nach 867 nicht mehr zur Code-Eingabe (Umleitung /login).

**How to apply:** App-Rollback auf Stand vor #312 nur NACH Rückweg 867. Nach Änderungen an den zwei Regeln immer verify-867 UND verify-866 laufen lassen. Neue HQ-Seiten unter `app/(hq)/werkstatt-gruppe` müssen `resolveHqSeitenKontext` nutzen (Wächter). Verwandt: [[mig-866-verbund-lesen-zweite-stufe]].
