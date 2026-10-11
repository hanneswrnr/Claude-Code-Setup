---
name: feedback-model-choice
description: Only current-generation models in the Claude Code setup (no Haiku 4.5; Haiku 5.5 allowed since 2026-10-11); model research only about the current generation
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b843f5d6-5de6-40ac-8cf9-a1b1443bcfbb
  modified: 2026-09-11T19:33:09.581Z
---

Do not route any setup agent, skill or default to Haiku 4.5; Sonnet 5 is the lowest tier we use. When researching model setups (X posts, guides, benchmarks), only use the current generation (as of 2026-09-11: Fable 5.1, Opus 5, Sonnet 5), not older ones such as Opus 4.8.

**Why:** On 2026-09-11 the user said Haiku 4.5 has not been improved for a long time, and rejected Opus 4.8 setups as outdated ("Aktuelle!").
**How to apply:** Check model generation and date of every source before citing it. Update 2026-10-11: the user lifted the Haiku ban because Haiku 5.5 improved strongly; Haiku 5.5 now runs quick read-only lookups (Explore) and background tasks, while devos-explorer and devos-researcher stay on Sonnet 5.5. Haiku 4.5 stays out. Pick effort levels by benchmarks; the highest level is not automatically the best.

Related: [[claude-setup-project]], [[user-profile]]
