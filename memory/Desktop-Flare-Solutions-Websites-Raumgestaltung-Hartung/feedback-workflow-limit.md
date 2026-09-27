---
name: feedback-workflow-limit
description: Big multi-agent workflows hit the weekly usage limit and left half-finished edits; check changed files and build after any abort
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 69962245-3585-4b8c-b499-d298b527753e
  modified: 2026-09-11T09:05:24.124Z
---

On 2026-09-10 three background workflows (design fan-out of ~11 agents with ~2.3M subagent tokens, research, legal-page implementation) were cut off by the weekly usage limit. The implementer had already added a manifest key (`originLabsLogo`) but not the markup using it, so `npm run build` failed ("Assets im Manifest, aber nirgends verwendet").

**Why:** Aborted agents leave partial file changes behind, and this repo's build is strict about unused assets and vercel.json parity.

**How to apply:** Keep fan-outs small; do mechanical or well-understood steps inline. After any aborted agent/workflow, first list files changed since it started (LastWriteTime, backups), diff them, and run `npm run typecheck` and `npm run build` before continuing. Related: [[feedback-edit-statt-skript]].
