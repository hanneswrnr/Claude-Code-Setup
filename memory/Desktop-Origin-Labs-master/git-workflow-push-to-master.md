---
name: git-workflow-push-to-master
description: "Arbeit wird direkt auf master committet und gepusht — keine Feature-Branches, keine PRs"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b820f2a0-993b-4101-bb34-e8699d23a8f5
  modified: 2026-08-06T19:54:21.467Z
---

Änderungen gehen direkt auf `master` und werden am Ende der Session dorthin gepusht — **keine** Feature-Branches, kein PR-Umweg. Ausdrücklich so angewiesen am 2026-08-05 („Am Ende bitte alles gleich zu master pushen und nicht auf eine feat branche!").

**Why:** Ein-Personen-Betrieb ohne Review-Partner; ein Branch-plus-PR-Zyklus erzeugt hier nur Overhead ohne Gegenwert.

**How to apply:** Auf `master` bleiben, in fachlich getrennten atomaren Commits arbeiten (die Nachvollziehbarkeit trägt die Commit-Granularität, nicht der Branch), am Ende `git push origin master`. Vor dem Push tsc + eslint + die volle Vitest-Suite grün haben — es gibt keine CI-Gate-Stufe davor. Fremde, nicht zum Auftrag gehörende Änderungen im Working Tree (z. B. `marketing/`) unangetastet lassen. Siehe auch [[local-checkout-no-prod-db-access]].
