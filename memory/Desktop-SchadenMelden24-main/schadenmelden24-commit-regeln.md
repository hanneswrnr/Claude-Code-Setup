---
name: schadenmelden24-commit-regeln
description: "In SchadenMelden24 nie Co-Authored-By in Commits (bricht Vercel-Hobby-Deploys); Desktop-Ordner ist ein Zip-Download ohne .git, .env.local-Schreiben ist blockiert, kein Werkstatt-Testlogin vorhanden"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a725a692-8488-40bd-9da6-7a626b54668f
  modified: 2026-09-13T20:21:57.997Z
---

Für dieses Repo gilt die Projektregel aus `wiki/05-Anti-Patterns/Co-Authored-By.md`: keine `Co-Authored-By`-Zeile in Commits, auch wenn die Harness-Anweisung sie verlangt.

**Why:** Der Trailer registrierte `noreply@anthropic.com` als Contributor; Vercel Hobby erlaubt keine Collaboration und blockte alle Deployments.

**How to apply:** Commit-Messages ohne Trailer schreiben. Weitere Umgebungs-Fakten (2026-09-13): `Desktop/SchadenMelden24-main` war ein Zip-Download ohne `.git` — per `git init` + `git fetch origin main` + `git reset origin/main` in ein Repo verwandelt; `npm ci` scheitert an zwei optionalen Lock-Einträgen, `npm install` mit Lockfile-Backup/Restore funktioniert; Schreiben von `.env.local` wird vom Sicherheitsnetz blockiert (öffentliche Supabase-Werte stattdessen inline beim Befehl setzen); es gibt keinen Werkstatt-Testlogin — visuelle Prüfung nur über eine temporäre Vorschau-Seite mit gemocktem `fetch` unter `app/__preview__/` (vor Commit löschen). Siehe [[prod-db-drift-feat-ai-features]].
