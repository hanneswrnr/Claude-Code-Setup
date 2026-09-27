---
name: menudeck-ci-rot
description: "Die MenuDeck-CI war nie gruen, und seit dem 2026-08-02 loest kein Push mehr einen Lauf aus"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4447cc85-a23c-4716-98f5-4a5845f2d0dc
  modified: 2026-08-06T19:58:26.295Z
---

**Die GitHub-Actions-CI dieses Repos war nie gruen.** Die gesamte Laufhistorie kennt genau ZWEI
Laeufe, beide am 2026-08-02, beide nach gut einer Minute gescheitert. Alle Zahlen in `README.md`
und `docs/menudeck-naechste-schritte.md` stammen aus **lokalen** Laeufen.

**Der Defekt ist gefunden und behoben** (Commit `2a0f850`, 2026-08-05): `next build` lief VOR
`supabase start`, und der Workflow legte `apps/dashboard/.env.local` nie an. Beim Prerendern wirft
`publicSupabaseEnv()` -- absichtlich so gebaut (P6). Lokal reproduziert: dieselbe Datei
beiseitelegen, `npm run build` -> exit 1 mit derselben Meldung.

**ZWEI DINGE BLEIBEN OFFEN und muessen von einem Menschen im Browser geklaert werden:**

1. **Seit dem 2026-08-02 loest KEIN Push mehr einen Lauf aus.** Gemessen an zwei aufeinander
   folgenden Pushes (`12032d1`, `2a0f850`): 0 Runs, waehrend der Workflow `state=active` meldet und
   Actions repoweit `enabled` ist. Naechstliegender Verdacht bei einem privaten Repo: aufgebrauchtes
   Actions-Minutenkontingent oder ein Ausgabenlimit -- steht unter **Settings -> Billing** und ist
   ueber die API nur mit dem `user`-Scope sichtbar, den der vorhandene Token nicht hat.
2. **Der Fix ist damit begruendet, aber nicht bewiesen.** Solange kein Lauf entsteht, ist "die CI ist
   jetzt gruen" genau die Sorte unbelegter Zusage, die dieses Projekt sonst nicht durchgehen laesst.

**Nebenbei offen:** die CI faehrt `npm run test:e2e` gar nicht. Die 78 Playwright-Specs sind
ausschliesslich lokal belegt.

Siehe [[menudeck-p8-review-stand]].
