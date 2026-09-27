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

## 2026-09-11 (evening) — Claude 5 model tiers and prompt audit

The user asked for a token-efficient setup at maximum quality with a Codex-style tier system, researched on X and in Anthropic's documentation (current model generation only, no Haiku), and chose Fable 5.1 at high effort as the main model. The installed files below were changed afterwards; `port-manifest.json` and the bundle copies stay untouched.

- Model tiers: `devos-explorer` and `devos-researcher` sonnet/high; `devos-worker`, `devos-verifier` and `devos-platform` opus/high; `devos-designer` fable/high; `devos-reviewer` and `devos-security` fable/xhigh. The section "Model routing" in `devos-orchestrate` describes the tiers, generic specialists on opus, and the fallback to `model: "opus"` for the Fable roles when the weekly Fable limit is used up. The reviewer escalation through `devos-review.settings.json` is obsolete.
- `/claude-api prompt-audit`, approved findings applied: duplicated German rules and step lists removed from `CLAUDE.md` (the DEVOS block is byte-identical) and a short section „Modelle“ added; self-check rituals removed from worker and platform; reviewer and security report every issue with a confidence level; the full contract is read by relevant section instead of completely for every B–D objective; the "two rounds without progress" rule now matches `CLAUDE.md` everywhere (take an untried route while the budget allows).
- Backup before the change: `%USERPROFILE%\Documents\DevOS\backups\2026-09-11-modellstufen\`. Its `skills\devos-orchestrate\SKILL.md` is the hash-verified state `20c0f2f7…` from the table above.
- Copies after the change were kept in `local-changes/2026-09-11-modellstufen/` and moved on 2026-09-22 (superseded model tiers) to `%USERPROFILE%\Documents\DevOS\backups\2026-09-11-modellstufen-kopien-nach-aenderung\`; they also remain in the Git history of the setup repository.
- Changed in the same step outside the port: `settings.json` (model, effortLevel, env `CLAUDE_CODE_SUBAGENT_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL`, `modelSettings`, `statusLine`), `statusline.py`, `skills/loop-engineering/SKILL.md` and the agency description cap in `vendor/sync_agency_agents.py`.

| Installed file (`~/.claude/…`) | Change | SHA-256 after the change |
|---|---|---|
| `CLAUDE.md` | Prompt audit of the German sections; new section „Modelle“; after the independent review the rule that small, clearly described changes stay with the main conversation was restored | `012ab2d997551bf0120e45730ed62379bf753f40164c21f6caf8d7e79858bd70` |
| `skills/devos-orchestrate/SKILL.md` | Model routing with Claude 5 tiers and Fable-limit fallback; prompt audit (contract read by section, stop rule, brief points, completion sentence); after the review: cache claim limited to Fable 5.1, fallback wording, cheap Sonnet work only through the effort-pinned roles | `ea721fdd2674d2293b6fb30a545ffd7ddd6e99b5b19e3472693e351bc8eeba03` |
| `skills/devos-experience/SKILL.md` | Web stack by reference to CLAUDE.md; merged AI-look list; shorter SEO checklist | `f48a50037a942e216b24eeee3d08a4ed2533bd6ff799ded69f475e3b1910f451` |
| `skills/devos-verify/SKILL.md` | Step-sequence sentence removed | `979df9e70e186cd07390184c66b58ce63efe984570631c9978cf5d4a4afe4eb0` |
| `agents/devos-worker.md` | opus/high; self-check ritual removed | `af2cdff772125e68ba40ea00b6f5ffdfe63003c75897ba66c7964acb9efe5136` |
| `agents/devos-platform.md` | opus/high; self-check ritual removed | `1df3a75132da72ebddc76542abf08e3d356c07ff71c0c9c16510d8ac498169b5` |
| `agents/devos-verifier.md` | opus/high | `feab4d54d0d905db2c54c54a6b412194fd8d028d124c1e4840d33568c75358a5` |
| `agents/devos-designer.md` | fable/high; duplicates of the preloaded devos-experience rules removed | `71f71f4885dd82423e2f40e76c04a75ca3d400db53f5879aa8df3af17a5ba8ce` |
| `agents/devos-reviewer.md` | fable/xhigh; one dimension list; report every issue with confidence | `917941f8e522d9cdf44c6bbf7c5d425f7b00ec925e149d291519a750f1a0caed` |
| `agents/devos-security.md` | fable/xhigh; report every suspected issue with confidence | `8eb0bb5a46f75607a05373c71c5e5349e56713c87d4b2a91f82cf70f58f4ad92` |
| `agents/devos-explorer.md` | sonnet/high; shorter read-only rule including shell commands | `8c92a9653d6bddb4c787cfc8c341066a6c70432695a2af423101ecb5d72c7537` |
| `agents/devos-researcher.md` | sonnet/high; redundant read-only sentence removed | `91008ae91fb7ab0dcc40b0c066dff799771ec09cc3a7a723b178fb56800303c4` |

Rollback: copy `CLAUDE.md`, the agent files, the four skill files, `settings.json` and `statusline.py` from the backup folder back to `~/.claude/`, and restore the agency agent files and `sync_agency_agents.py.before` from `%USERPROFILE%\Documents\DevOS\backups\2026-09-11-agent-descriptions\`. A new Claude Code session is needed for the change to take effect.

## 2026-09-19 — Orchestrierung und Prüfung auf Opus xhigh

Auf Wunsch wurden Hauptgespräch/Orchestrierung und die Prüfpfade auf Opus mit der höchsten im Setup verwendeten Thinking-Stufe `xhigh` gestellt. Fable 5.1 auf `high` bleibt ausschließlich für Design (`devos-designer`) vorgesehen; Reviewer und Security laufen ebenfalls auf Opus `xhigh`, damit Fable nicht außerhalb des Designs eingesetzt wird. Eine neue Claude-Code-Sitzung ist nötig, damit die Einstellungen geladen werden.

| Datei | Änderung |
|---|---|
| `settings.json` | Hauptmodell `opus`, `effortLevel` `xhigh` |
| `agents/devos-verifier.md` | `opus` / `xhigh` |
| `agents/devos-reviewer.md` | `opus` / `xhigh` |
| `agents/devos-security.md` | `opus` / `xhigh` |
| `skills/devos-orchestrate/SKILL.md` | Routing-Dokumentation auf Opus-orchestriert, Design-only-Fable aktualisiert |
| `CLAUDE.md` | Modellregeln und Fable-Fallback aktualisiert |

## 2026-09-22 — Umstellung auf Opus 5.5

Auf Wunsch läuft alles außer Suche und Recherche auf Opus 5.5 (Kurzname `opus`, der bereits auf `claude-opus-5-5` zeigt; per Test-Agent geprüft). Fable wird nicht mehr eingesetzt, auch nicht für Design. Grundlage sind die Benchmark-Grafiken zur Veröffentlichung von Opus 5.5, die der Nutzer am 22.09.2026 als Bildschirmfotos geteilt hat (Werte abgelesen, nicht selbst gemessen): Opus 5.5 auf `high` liegt in Terminal-Bench 4.0, FrontierCode 1.1 und CursorBench 4.0 vor Fable 5.1 und der Vorgängergeneration auf jeder Stufe, bei geringeren Kosten; `xhigh` kostet etwa doppelt so viel wie `high` und bringt +2, 0 bzw. −3 Punkte. Sonnet 5 bleibt für Suche und Recherche. Dieser Eintrag ersetzt die Modellentscheidungen der früheren Einträge; die Kopien unter `local-changes/2026-09-11/` sind nur Archiv und dürfen nicht wieder eingespielt werden.

- Kopien nach der Änderung: `local-changes/2026-09-22-opus-5-5/`

| Datei | Änderung | SHA-256 nach der Änderung |
|---|---|---|
| `agents/devos-designer.md` | `fable` / `high` → `opus` / `high` | `cb7a25f2e18484f8c81f29a15d1ec4aaa1e3fe4fdd1de8608ef00d84e5fcc76e` |
| `agents/devos-verifier.md` | `opus` / `xhigh` → `opus` / `high` | `feab4d54d0d905db2c54c54a6b412194fd8d028d124c1e4840d33568c75358a5` |
| `agents/devos-reviewer.md` | unverändert `opus` / `xhigh` (Stand vom 19.09.2026) | `acff32cf968409aca90d1fd9759d6e27d0ef0338911aa8b8c577c44cd54d7ed9` |
| `agents/devos-security.md` | unverändert `opus` / `xhigh` (Stand vom 19.09.2026) | `725a7511fac4737d489e095f61bfd3f3a8f840bb9ff51b0837017a4923d00ccf` |
| `skills/devos-orchestrate/SKILL.md` | Abschnitt „Model routing": zwei Stufen (opus, sonnet), Fable-Limit-Regel entfernt, Hinweis gegen `max` | `690320575fa5ff82457d1417425d47c3693c06d47e251a610c9c3f35439f7e1c` |
| `CLAUDE.md` | Abschnitt „Modelle": Opus 5.5, xhigh nur für Orchestrierung, Prüfung und Sicherheit; Fable-Regel entfernt | `ec69af8424f0d99d410a32cef8f3fe4e187e8800c98c2a9edb8916e4f594ebd0` |

- Außerhalb des Ports geändert: `learning/lessons.jsonl` (Lektionen L-20260911-7c9217 und L-20260911-51c812 über `ll.py edit` auf den neuen Stand umformuliert). `settings.json` bleibt bei `model` `opus`, `effortLevel` `xhigh` und Unteragenten `opus`; der Schlüssel `skipWorkflowUsageWarning` darin stammt nicht aus dieser Änderung.
- Unverändert: `devos-worker` und `devos-platform` (`opus` / `high`), `devos-explorer` und `devos-researcher` (`sonnet` / `high`).
- Rollback: Stand vor der Änderung ist Commit `88ec724` im Setup-Repo. Wirksam wird die Änderung erst in einer neuen Claude-Code-Sitzung; in der Desktop-App zusätzlich im Eingabefeld Opus 5.5 mit „Extra hoch“ wählen.
