---
name: feedback-no-coauthored-by
description: SchadenMelden24-Projekt — NIEMALS Co-Authored-By Trailer in Commits einfuegen (Vercel-Block)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: aa1f54a9-ecef-4758-ae12-3994b4f0aceb
---

In Commits fuer das SchadenMelden24-Projekt **niemals** `Co-Authored-By: Claude ... <noreply@anthropic.com>` Trailer einfuegen — weder in Commit-Body noch als Git-Trailer.

**Why:** Vercel Hobby Plan erlaubt keine Collaboration. Frueher hat ein Co-Authored-By Trailer dazu gefuehrt, dass `noreply@anthropic.com` als zweiter Contributor registriert wurde und das Projekt als "Team-Projekt" geflaggt wurde. Alle Deployments wurden geblockt; nur Disconnect/Reconnect des GitHub-Repos in Vercel hat es gerettet. Dokumentiert in `wiki/05-Anti-Patterns/Co-Authored-By.md`.

**How to apply:** Bei JEDEM `git commit` in diesem Projekt — den Trailer-Block weglassen. CLAUDE.md gibt zwar weiterhin den Co-Authored-By-Standard-Workflow vor, aber das Projekt-Anti-Pattern hat Vorrang. Auch User-Commits in der Historie (z.B. `e67a2b7a`) sind ohne Trailer.

Verlinkt: [[wiki-co-authored-by-anti-pattern]] — Wiki-Anti-Pattern.
