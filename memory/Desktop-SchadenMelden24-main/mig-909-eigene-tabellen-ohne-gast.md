---
name: mig-909-eigene-tabellen-ohne-gast
description: "Mig 909 (elf Tabellen ohne anon-Rechte, 38 Regeln TO authenticated) LIVE seit 17.10.2026, PR #411 GEMERGT 17.10.2026 (b9fd9576c)"
metadata:
  node_type: memory
  type: project
  originSessionId: a9996d4a-567c-4f6e-8fa9-10d99f414f00
  modified: 2026-10-16T22:06:33.029Z
---

Mig 909 `eigene_tabellen_ohne_gast` ist LIVE seit 17.10.2026 (Freigabe Hannes), Ledger-Eintrag gesetzt, Prüfskript
gegen live „909-TEST OK“. Zweig fix/anon-rechte-to-public, PR #411 GEMERGT 17.10.2026 (b9fd9576c). Folgebefund von
[[mig-908-kalender-events-ohne-gast]]; Folgeliste weiterer Tabellen mit anon-Rechten im Bericht
`wiki/09-Operations/Security-Audits/2026-10-16-eigene-tabellen-ohne-gast.md`.

**Why:** Gast-Schutz hing nur an Regel-Ausdrücken; geringste Rechte.
**How to apply:** Rückweg 909 vor Rückwegen 748/777/778; neue Regeln auf den elf Tabellen nur TO authenticated
(Wächter `lib/werkstatt/__tests__/migration-909-…test.ts`).
