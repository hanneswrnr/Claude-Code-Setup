---
name: project-hartung-sektion-entfernen
description: "Checklist when removing a section in Hartung — redirects to its anchor, manifest keys, AI-badge check, parked copy"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69962245-3585-4b8c-b499-d298b527753e
  modified: 2026-09-11T10:27:41.953Z
---

Removing a homepage section in Raumgestaltung-Hartung cascades beyond the markup (learned 2026-09-11):
- `src/redirects.ts` may point legacy paths at the section's anchor (e.g. `/#ueber-uns`); a dead anchor gives no error, visitors just land at the top. Retarget, run `npm run config` (regenerates vercel.json), update `tools/routen-pruefen.mjs`.
- The build fails on manifest keys that are no longer used and (since 2026-09-11) on AI badges without AI assets or vice versa.
- Run `npm run routen` against `PORT=5199 node src/dev.ts` with `BASE=http://localhost:5199`; the single FEHL for `/impressum.html` on the dev server is expected (dev serves the file, Vercel redirects).

**Why:** The team redirects silently pointed at a removed anchor until a cleanup review caught it.

**How to apply:** Go through this list whenever the customer asks to drop a section; park the old source first ([[project-hartung-kein-git]]).
