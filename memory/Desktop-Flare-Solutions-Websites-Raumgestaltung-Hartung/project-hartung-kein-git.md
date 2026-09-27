---
name: project-hartung-kein-git
description: Raumgestaltung-Hartung now has git + GitHub (since 2026-09-11); everything goes straight to main, Vercel deploys from it
metadata:
  node_type: memory
  type: project
  originSessionId: 69962245-3585-4b8c-b499-d298b527753e
  modified: 2026-09-11T20:13:47.508Z
---

The project is a git repository since 2026-09-11, pushed to https://github.com/hanneswrnr/Raumgestaltung-Hartung.git. The user's rule: "Alles soll direkt zu main" — no feature branches, no PRs. Vercel is Git-connected and deploys every push to main automatically (build took ~55 s on 2026-09-11).

**Why:** Until 2026-09-11 there was no repo, so deletions were unrecoverable and source had to be parked as `.txt` in `prototypes/`. That no longer applies — history recovers it. The parked files from before still exist and stay as they are.

**How to apply:** Commit normally. Git has **no configured identity** (neither local nor global), so every commit needs it inline: `git -c user.name=hanneswrnr -c user.email=hannes-werner@outlook.de commit …`. Write the message via a Bash heredoc (`git commit -F -`), never a PowerShell-written file — those pick up a UTF-8 BOM and land in the message. Since Vercel auto-deploys, a push to main is a production change: get approval first. Related: [[project-hartung-konten-vertraege]], [[feedback-edit-statt-skript]].
