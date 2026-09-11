# Local changes to the installed DevOS Claude Code port

`port-manifest.json` records the state copied from the Codex DevOS on 2026-09-11 (morning). The installed files listed below were **intentionally changed afterwards at the user's request**. `devos-maintain` reads this note: treat every listed file as a user edit to merge — never overwrite it with the bundle copy or a re-port, and keep listed new files that have no manifest entry.

## 2026-09-11 — autonomous orchestration contract

The user supplied `AUTONOMOUS_SOFTWARE_ENGINEERING.md` ("Das soll auch alles mit ins Setup"). It is installed verbatim as a reference of `devos-orchestrate`, with a short Claude Code mapping on top, and its core rules are woven into the files that act on them. An independent review (coverage, consistency with the existing rules, technical validity; every finding re-checked by a skeptic) led to a second round the same afternoon: complete list of questions to the user (security posture, outward-facing actions), stop rule aligned with Loop Engineering budgets, delegation limited to substantive objectives and to the main session, explicit Workflow opt-in, section 20 (SEO/marketing, no fabricated claims), dependency policy and "no test hacks" in the always-loaded layer, worker rules for `devos-platform`, reviewer without render evidence, and `devos-maintain` reading this note.

- Backup of every affected file before the change, plus the original upload: `%USERPROFILE%\Documents\DevOS\backups\2026-09-11-autonomes-orchestrieren\` (`CLAUDE.md.vor-runde2-mit-web-abschnitt` is the state before round two)
- Copies of the changed files after the change: `local-changes/2026-09-11/` next to this note

| Installed file (`~/.claude/…`) | Change | SHA-256 after the change |
|---|---|---|
| `CLAUDE.md` | Sections „Grundregeln" (new: „Neue Pakete sparsam", „Nichts erfinden"; „Prüfbar arbeiten" without test hacks; real questions defined), „Autonome Orchestrierung" (new), „Loop Engineering" (done = green and confirmed in behavior; Workflow opt-in) | `1fa94536ce8355cd09fa61661fff2c906bddf8958069104bec8b4d8337f46b78` |
| `skills/devos-orchestrate/SKILL.md` | Description; section „Autonomous engineering loop — user contract since 2026-09-11"; board fields; worker rules for generic specialists; Workflow opt-in and loop budget in the stop rule | `20c0f2f7f887c2cede2c4b653a003340ff40203ffe8a03d7dbc0135047d0109a` |
| `skills/devos-orchestrate/references/autonomous-software-engineering.md` | **New.** User contract verbatim, mapping to Claude Code at the top | `44020f2f730a0578155926225df8f8096e806c47b3c33dc723165c8ec1c86f9d` |
| `skills/devos-experience/SKILL.md` | No generic AI look; separate design review loop (13–14); SEO, analytics and marketing without fabricated claims (20) | `0a200d8ac120387a9ee0f782df0d4502a98792c52dc7da67ac9c95fe12d9ae75` |
| `skills/devos-verify/SKILL.md` | Debugging sequence, competing read-only hypotheses, no test hacks (16–17) | `e6fe36e06923af8b316c971480290e0984ce4659432ef74ee6898b41e742b33d` |
| `skills/devos-services/SKILL.md` | Dependency policy (23); security checklist inline (15) | `0bd9ac01a65b0b3cf3ca69b026300b5c0695471c5ebd14e1a756aee4e45d2c4a` |
| `skills/devos-maintain/SKILL.md` | Reads this note next to the manifest; listed files are merged, never overwritten | `b4f8b120dd2352c54c9f905de106b62d902be960598071f030f80899f7a73f6e` |
| `agents/devos-worker.md` | Working changes not advice, self-check, no test hacks, fuller report, fix returned findings in the same context | `7f0502f6db17524c6056621cb13fc25302eaa333c246cd67bcc2ac9f80b907bf` |
| `agents/devos-reviewer.md` | Quality-gate dimensions; UX/design only with render evidence; recommendation accept / revise / cross-review / redesign | `586a065ac3c23edba07f5e580cb92a0255778e6d50c8a02180e4210be509a524` |
| `agents/devos-verifier.md` | Typecheck and incomplete tests are no proof; UI states, widths, keyboard, reduced motion | `01d35ccf5cedcd6e45170c7e337a3c97bfe15594b941f6630ce44ebcfd877bed` |
| `agents/devos-designer.md` | Working UI in owned files; no generic AI look; review loop findings go to root | `a1ade1693863ce7b28137359d775bf1f9d2173ca961f67dc5e0377e2c96fb139` |
| `agents/devos-security.md` | Default security checklist; never weaken security for tests | `b828cac16e6d4c86336448331f85083a03980d87f699ed8fe8d937f7d91c7c24` |
| `agents/devos-platform.md` | Worker rules for implementation briefs (working changes, no test hacks, fuller report, fix findings in context) | `d9d66bbd16850cc2c0422c869f929f4c89ee37aa346f08321df8f31124f41b4d` |

Notes:
- The installed `CLAUDE.md` already differed from the bundle before this change — the bundle holds only the marked DEVOS block; the installed file adds the user's own sections below it.
- The section „# Web-Projekte: HTML, CSS und TypeScript" in `CLAUDE.md` was added the same day at 13:45 outside this change (by the user or another session). It is part of the recorded hash above but not part of this contract integration.

## Rollback

Copy the files from the backup folder back to `~/.claude/` and delete `skills/devos-orchestrate/references/autonomous-software-engineering.md`. For `CLAUDE.md`: the backup `CLAUDE.md` is the state before the integration and does not contain the later Web section; `CLAUDE.md.vor-runde2-mit-web-abschnitt` contains the Web section but also round one of this change. To undo the integration and keep the Web section, restore `CLAUDE.md` and re-insert the section „# Web-Projekte: HTML, CSS und TypeScript" from the other file. A new Claude Code session is needed for any change to take effect.
