---
name: feedback-model-choice
description: No Haiku 4.5 anywhere in the Claude Code setup; model research only about the current generation (Claude 5 family as of 2026-09)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b843f5d6-5de6-40ac-8cf9-a1b1443bcfbb
  modified: 2026-09-11T19:33:09.581Z
---

Do not route any setup agent, skill or default to Haiku 4.5; Sonnet 5 is the lowest tier we use. When researching model setups (X posts, guides, benchmarks), only use the current generation (as of 2026-09-11: Fable 5.1, Opus 5, Sonnet 5), not older ones such as Opus 4.8.

**Why:** On 2026-09-11 the user said Haiku 4.5 has not been improved for a long time, and rejected Opus 4.8 setups as outdated ("Aktuelle!").
**How to apply:** Pin cheap roles (explorer, researcher) to sonnet, never haiku; override the model when spawning roles whose file still says haiku; check model generation and date of every source before citing it.

Related: [[claude-setup-project]], [[user-profile]]
