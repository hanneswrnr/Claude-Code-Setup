---
name: feedback-edit-statt-skript
description: "Script-based rewrites of project source files get blocked by the auto-mode classifier — use the Edit tool, sequentially per file"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 69962245-3585-4b8c-b499-d298b527753e
  modified: 2026-09-11T09:05:17.304Z
---

On 2026-09-11 a Bash command that ran a Node script to cut the old mail code out of `src/anfrage.ts` (plus `cp` backups in the same call) was denied by the auto-mode classifier. The whole command was rejected, so the backups were not made either.

**Why:** Programmatic rewrites of source files look risky to the classifier; the Edit tool is the sanctioned path. There is also no git repo in this project, so a lost backup means no easy revert.

**How to apply:** Change project files with Edit (large removals in a few exact chunks). Never send two Edits to the same file in one parallel batch — do them one after another. Make backups with a separate, harmless command before editing, not bundled with the rewrite. See [[feedback-workflow-limit]].
