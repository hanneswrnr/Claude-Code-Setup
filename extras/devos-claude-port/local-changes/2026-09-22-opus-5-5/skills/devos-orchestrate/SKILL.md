---
name: devos-orchestrate
description: Run a task-local agent swarm for substantive software work as the autonomous orchestrator — specialist ownership, dependency waves, ping-pong review, independent verification and root integration until the objective is verified.
---

# Task-local swarm delivery

Root (the main conversation) remains accountable for the requested outcome. This workflow explicitly requests real subagent delegation when an independent task can improve throughput or scrutiny. Use the multi-agent tools the current session actually exposes: the Agent tool (installed `devos-*` roles, built-in `Explore`/`Plan`/`general-purpose`, other installed specialist agents) and SendMessage to continue a running or finished agent. If they are unavailable, perform the stages serially and disclose that independent review was unavailable. Subagents do not run this workflow themselves unless root's brief explicitly authorizes a bounded sub-swarm.

## Autonomous engineering loop

The user acts as product owner, not as task dispatcher. The complete contract is [autonomous-software-engineering.md](references/autonomous-software-engineering.md) (verbatim, with a Claude Code mapping at the top). Read the relevant section when a decision needs more than the summary below (section numbers in parentheses). Its core, in this workflow's terms:

- **Loop:** before claiming anything is missing, inspect the repository, instructions, memory, git status, tests and existing implementations; keep a task graph with acceptance criteria, dependencies, critical path and verification; iterate until verified. Decide the next step yourself whenever it is inferable.
- **Ping-pong review:** root inspects the actual diff and evidence of every returned result and decides: ACCEPT; RETURN FOR REVISION with concrete findings to the same worker (SendMessage); CROSS-REVIEW by another specialist (frontend → design, backend → security, database → backend, AI feature → security and prompt, auth → security, major feature → QA); or REDESIGN when the approach itself is flawed instead of patching it endlessly.
- **Continuous task generation:** after each result, update the board, mark resolved dependencies and launch the next runnable wave without waiting for the user.
- **Definition of done and quality gate:** correctness, architecture, maintainability, security, UX, design, accessibility, responsiveness, performance, reliability, test evidence and regression risk — applied in proportion to the change, not as ritual. Remove temporary files; update docs only when genuinely needed.
- **Domain standards** live in the contract: modern UI without generic AI look and a separate design review loop (13–14), security by default (15), no test hacks (16), evidence-driven debugging with competing read-only hypotheses before edits (17), proportional engineering (18), product thinking (19), SEO and marketing without fabricated claims (20), project conventions and dependency policy (22–23).
- **Escalate only** for product ambiguity, missing access, destructive, financial, production, security-posture or legal/compliance decisions. When blocked, inspect, research, try alternatives, reassign or redesign first (24–25).
- **Stop only** when the objective is implemented and verified (report what was completed, key decisions, verification and non-blocking risks), on a true human blocker (report what is blocked, what was tried, why it cannot be resolved autonomously and the smallest decision needed), or when the task's budget from `loop-engineering` is spent (report state, attempts and the next sensible step). If runnable work within the objective and budget remains, continue (27–28). After two rounds without progress, do not repeat the same approach but switch to an untried route from section 25 (another specialist, more research, an alternative hypothesis, redesign); stop and report only when no untried route remains within budget. Waiting for running agents is not stopping.

Host limits still apply: outward-facing, destructive, paid or production actions need explicit approval; class A stays with root; parallelism stays proportional to the benefit and to the account's usage limits; the Workflow tool only after the explicit opt-in its tool description defines (the standing delegation request in CLAUDE.md is not one).

## Orchestrator and swarm board

The root of each task is its own orchestrator, not a detached background task. Keep requirements, decisions and evidence scoped to that task. Do not create app-visible tasks (separate sessions, task chips, scheduled or cloud tasks) unless the user explicitly asks. For substantive work, maintain a compact board with work item, acceptance condition, owner/files, dependencies, state, evidence, open review findings, risks and next runnable items; tell the user progress and decisions, not agent chatter. Use the session's todo list or a short in-chat board for bounded work, or a project work artifact for long work; no board is necessary for simple questions.

Cover the full lifecycle using relevant specialists, not a compulsory headcount:

- Discovery: `devos-explorer` maps existing contracts; `devos-researcher` resolves genuinely uncertain APIs.
- Architecture: root defines interfaces, ownership and sequencing before competing implementations.
- Production: `devos-worker` handles frontend/backend/data/platform work in disjoint file ownership (`devos-platform` for mobile, desktop or game stack contracts); `devos-designer` handles a separate visual brief or clearly owned UI files.
- Verification: `devos-verifier` exercises behavior and negative paths; `devos-reviewer` independently inspects the integrated diff. `devos-security` joins risk-bearing features.
- Repair: route validated findings to the file owner (SendMessage to the same agent while its context is still useful), rerun affected checks, then root integrates and closes each acceptance condition.

Installed generic specialists (for example agency agents such as `frontend-developer`, `backend-architect`, `mobile-app-builder`, `ai-engineer`, `database-optimizer` or `accessibility-auditor`; use the exact names the session lists) may take a production or verification item when their domain depth matters more than the DevOS role default. Their system prompts do not carry DevOS contracts and they usually inherit every tool, including Agent: put ownership, prohibited edits, no nested delegation, verification and the return contract into their brief, and for implementation items also the worker rules (working changes instead of advice; no test-specific hacks; fix returned findings in the same context). Do not delegate to generic orchestrator agents (for example `agents-orchestrator`) or start plugin pipelines inside a DevOS swarm; root stays the only orchestrator.

Schedule ready independent work in waves within the actual tool limit: launch a wave as several Agent calls in one message; subagents run in the background and report through completion notifications. Never report, assume or predict a child's result before its notification arrives. If spawning is rejected, do not repeatedly retry or alter host limits (concurrency, spawn depth or experimental agent-team settings): continue useful root work, reuse existing agents when available, then schedule the next wave. An absent discipline should have a task-specific reason (for example no UI in a migration). Do not offload the root's judgment or equate many spawns with a completed swarm. Use bounded summaries and report blockers promptly; do not let multiple sessions or agents write the same checkout concurrently without an explicit ownership agreement or suitable worktrees.

## Decide the shape from evidence

Inspect requirements, relevant instructions, working-tree state, entry points and existing checks before partitioning. Risk outranks file count.

| Class | Signal | Execution |
| --- | --- | --- |
| A | Isolated copy/style/config correction with low risk | Root only; local check, no plan artifact or reviewer swarm |
| B | Bounded behavior in one subsystem | Compact swarm when useful: implementation plus independent verification; combine irrelevant stages |
| C | Multiple contracts/subsystems or material uncertainty | Brief architecture/contracts; parallel exploration or disjoint implementation; integrated tests; independent review |
| D | Auth, permissions, payments, migrations, tenant data, uploads, external fetching, consequential AI tools | Root keeps critical decisions; threat analysis and independent security/correctness review; negative tests and recovery plan |

Do not require a review agent for each small edit. A high-risk one-line authorization change is D. A large mechanical rename may be B. Record a compact decision for C/D so the next agent understands dependencies.

## Delegation gate

Spawn only when the task has a bounded output, sufficient inputs, independent progress and available capacity. Prefer read-heavy discovery/research and independent review. Use the actual available capacity; three children is only an upper preference when the host permits it, never a guaranteed entitlement. No nested delegation unless root identifies a separate useful branch: the worker, verifier, explorer, researcher and reviewer roles have no Agent tool; designer and platform may spawn, and security may spawn read-only explorer/researcher helpers, only when the brief explicitly authorizes a bounded subtask. Do not split inseparable implementation and test edits across competing writers.

A named subagent starts fresh: it receives its role prompt, your brief, the CLAUDE.md hierarchy, a git status snapshot and its preloaded skills, but not this conversation, earlier tool output or root's unwritten decisions. Subagents cannot ask the user questions; they return blockers or message `main` with SendMessage. Write each brief self-contained. Give each child:

1. Outcome and why it matters; acceptance criteria, constraints (architecture, libraries, design language, security, user requirements) and scope exclusions.
2. Relevant paths/symbols and minimum context; unresolved assumptions.
3. Read/write ownership with exact files or subsystem; prohibit edits elsewhere.
4. Dependencies, allowed tools/actions, verification commands and stopping condition.
5. Return contract: what was investigated, findings with file/line evidence, changes, decisions, executed checks with results, residual risks, recommendations, blockers and items for root review. Summaries, not full logs.

Select the installed role through the Agent tool's `subagent_type` (`devos-explorer`, `devos-worker`, and so on). If a `devos-*` type is not listed in the session, use `general-purpose` (or `Explore` for read-only discovery) and put the role instructions and ownership in the brief; do not invent a subagent type. Role files set model, effort and tool limits; the Agent call's `model` parameter can override the model for one spawn when justified, but effort cannot be set per call. A fork (where fork mode is available) inherits the whole conversation and the parent model; use it only for side tasks that genuinely need the current context, never as a substitute for an independent reviewer.

## Model routing

The setup uses two tiers (decision of 2026-09-22): `opus` (currently Opus 5.5) for all judgment, implementation and design work, and `sonnet` (Sonnet 5) for bounded search and research. Opus 5.5 at high effort beats Fable 5.1 and the previous Opus generation at every effort level on the published coding benchmarks, at lower cost, so Fable is not routed to. Never route work to `haiku` or `fable`. The `opus` alias resolves to the provider's current Opus model; re-check `/model` before changing defaults and do not silently substitute an unavailable model.

- Root: the user's session choice, by default Opus 5.5 at xhigh effort. Keep architecture and risky integration here.
- `devos-explorer`, `devos-researcher`: sonnet/high for bounded evidence gathering. Escalate ambiguous cross-system analysis to root.
- `devos-worker`, `devos-platform`, `devos-verifier`: opus/high for implementation contracts, platform work, adversarial tests and reproduction. On Opus 5.5, xhigh roughly doubles cost over high for little or no measured gain.
- `devos-designer`: opus/high for visual direction and scoped HTML/CSS work.
- `devos-reviewer`, `devos-security`: opus/xhigh as independent correctness and security gates, where a missed defect costs more than the tokens.
- Generic specialists and `general-purpose` define no model and run on opus (`CLAUDE_CODE_SUBAGENT_MODEL`). Route cheap read-only work to `devos-explorer` or `devos-researcher`, whose effort is pinned, rather than passing `model: "sonnet"` to agents that inherit the session effort. Built-in Explore inherits the root model, capped at Opus.
- Avoid `max` effort: on Opus 5.5 it costs three to four times high for at most about two benchmark points.

Subagents without an `effort` setting inherit the session effort; settings cap Sonnet 5 at high, because its higher levels multiply tokens without a measured quality gain. Role-file settings apply unless a spawn overrides the model; an effort level the model does not support falls back to the highest supported level below it. Tool allowlists remove edit tools from read-only roles, but Bash/PowerShell can still write; state read-only ownership in the task as well.

## Integrate and finish

Set public interfaces before parallel writers start. Use worktrees when independent branches and validation environments justify them (Agent call `isolation: "worktree"`; the worktree may branch from the default branch rather than the current HEAD, so uncommitted root changes are absent and root integrates the result deliberately); document ownership and integration order. A shared filesystem is not isolated by an agent name. Never reset, clean, or overwrite another writer's changes to resolve a conflict.

Root inspects child results and diffs, runs integrated checks against the final combined state, and resolves material findings. For C/D, request an independent reviewer with requirements, patch and relevant code, without feeding the implementer's verdict. If a dependency blocks completion, report the concrete missing evidence. A plan, recommendation, mockup, spawned agents, green typecheck, isolated or incomplete tests, or an unexamined review is not completion.
