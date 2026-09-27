---
name: menudeck-p8-review-stand
description: "Stand von P8 -- Final-Review und Security-Review gefahren, alle Befunde behoben; offen ist nur die unabhaengige Bestaetigung"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4447cc85-a23c-4716-98f5-4a5845f2d0dc
  modified: 2026-08-06T22:54:05.680Z
---

**HIER GEHT ES WEITER** (Stand 2026-08-07, `origin/main` = **`a353adf`**, Tree sauber, Supabase
gestoppt, Docker aus).

**Final-Gesamt-Review P8** (fuenf unabhaengige Pruflinien + adversarische Gegenpruefung):
CHANGES REQUESTED, 7 Befunde bestaetigt, 2 widerlegt — **alle sieben behoben** (`cb70232`,
`0bd07d9` = Migration `0073`, `12032d1`). Vier der sieben betrafen die PRUEFMITTEL, nicht den Code.

**P8-Security-Review** (eigenes Fenster, inzwischen geschlossen): **CHANGES REQUESTED, zwei
Befunde, beide ohne DB-Bezug — es gibt KEINE Migration `0074`.** Der Review hat sein Verdikt
ausdruecklich an eine Bedingung geknuepft: *„Nach S1 und S2 ist APPROVED erreichbar, ohne dass eine
weitere Messung noetig waere."*
- **S1** — die 405-Zusage hatte keinen Anker. **Behoben in `a353adf`** mit ZWEI Ebenen:
  Modulform (`test/lieferung-route.test.ts`, Mutant -> allein rot) und HTTP
  (`e2e/methodenweiche.spec.ts`, 3 Specs; unter dem Mutanten fallen 2 an ihrer eigenen Zusage).
- **S2** — `next@15.5.20` lag hinter der Backport-Linie. **Behoben: `15.5.23`.** Die acht EIGENEN
  next-Advisories sind weg (darunter `GHSA-955p-x3mx-jcvp`); was bleibt, ist transitiv
  (postcss, sharp) und nur per MAJOR zu schliessen. **Achtung: `npm audit` meldet vorher wie
  nachher „8 vulnerabilities" — die Kennzahl verdeckt die Verbesserung.**

**DAS EINZIGE, WAS OFFEN IST: die unabhaengige Bestaetigung von S1 und S2.** Ein Workflow mit zwei
Pruefern ohne Vorkontext lief und wurde beim Feierabend abgebrochen (beide waren noch nicht fertig;
der Arbeitsbaum blieb sauber). **Wer morgen weitermacht: diesen Workflow erneut fahren** —
Skript liegt unter
`.claude/projects/.../workflows/scripts/p8-security-bestaetigung-wf_f4a384bf-62a.js`.
Wichtig dabei: S1 braucht Datenbank und Port 3100 EXKLUSIV, S2 darf beides nicht anfassen.

Danach: **Verdikt APPROVED in die Doku schreiben** (Abschnitt 2 von
`docs/menudeck-naechste-schritte.md` beschreibt den Security-Review noch als anstehend — bewusst
nicht vorweggenommen), dann die vertagte **Entscheidung PA vor P9**.

**Gemessener Stand:** 72 Migrationen `0001`–`0073` · Vitest 99 Dateien / 1400 · Playwright 81 Specs
· typecheck 0 · `next build` gruen (Next.js 15.5.23) · gruene Wiese per `db:reset` durch `0073`
· Regel 1 unabhaengig belegt (`authenticated` 0 von 33 Basistabellen-Statements, `service_role`
37 von 39 als Positivkontrolle).

Drei Instrumentenfallen dieses Reviews, alle nur durch Positivkontrollen gefunden — siehe
[[menudeck-instrumentenfallen]]. Weiter: [[menudeck-ci-rot]], [[menudeck-migrations-ledger]].
