---
name: feedback-rote-pruefung-nicht-wegerklaeren
description: "A failing check must be fixed or removed, never explained away in a report — the user reads the symptom, not the excuse"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 69962245-3585-4b8c-b499-d298b527753e
  modified: 2026-09-11T21:15:24.969Z
---

When a project check reports a failure, fix it (or delete the case) instead of reporting it as a known, harmless quirk. On 2026-09-11 `npm run routen` said "1 von 61 Fällen weichen ab" for `/impressum.html`. I verified production was fine, wrote "das ist nur eine Eigenheit des Entwicklungsservers" in the report, and moved on. The user came back with "Wichtig das '.html' soll bei keiner Route am Ende in der Linkzeile hängen! Das sieht unprofessionell aus!" — the explanation did not reassure, it alarmed.

**Why:** The user reads the symptom in the report, not the reasoning behind it, and a check that is known to be red gets ignored the next time it turns red for a real reason. The fix took one function in `src/dev.ts` — far less than the round trip cost.

**How to apply:** Before writing "pre-existing" or "only a dev-server quirk" into a report, ask whether the fix is small. If it is, do it in the same turn. If it genuinely does not belong to the task, still say what it would take and offer it, rather than filing it as harmless. The same applies to a check whose green result is known to be meaningless — say so in the check's own comment, not only in chat. Related: [[feedback-einfache-sprache]], [[project-hartung-kein-git]].
