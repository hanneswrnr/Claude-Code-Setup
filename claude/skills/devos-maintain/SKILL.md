---
name: devos-maintain
description: Audit and maintain the installed DevOS Claude Code port (user CLAUDE.md block, devos-* agents and skills, toolkit adapters) for drift, compatibility, skill/agent overlap and reversible updates.
---

# Maintain without blind upgrades

Use on a setup audit/update request, not automatically on ordinary coding tasks. Locate the actual Claude config directory (`CLAUDE_CONFIG_DIR` if set, otherwise `~/.claude`), the installed DevOS files (the `CLAUDE.md` block between the `DEVOS (CLAUDE CODE PORT)` markers, `agents/devos-*.md`, `skills/devos-*`) and the port bundle they were copied from (recommended location `%USERPROFILE%\Documents\DevOS\devos-claude-port`, containing `port-manifest.json`). Read the bundle manifest and, if present, `LOCAL-CHANGES.md` next to it: the files listed there were intentionally changed or added by the user after the port (added files have no manifest entry) — merge them, never overwrite them with bundle copies or a re-port. If the bundle is missing, audit installed files and reconstruct a reviewable update; never download and execute an uninspected replacement.

Inspect `claude --version`, `claude --help`, `/doctor`, `/context` (loaded memory files), the subagent types and skills the session actually lists, and actual model availability (`/model`). Prefer current Anthropic primary docs (code.claude.com/docs) and installed CLI behavior over old tutorials. Re-check agent/skill paths and frontmatter keys; preserve provider/auth/MCP/plugin/permission settings. Never read or log credentials (`.credentials.json`, tokens in settings `env`) just to inventory integrations.

Compare installed file hashes (for example `Get-FileHash -Algorithm SHA256`) with the bundle manifest. Treat user edits as drift to merge, not damage to overwrite. Compare upstream changes by pinned commit, inspect full changed skills/scripts/references, check license and network behavior, and assess overlap/context cost, including installed generic agent libraries (agency-agents) and plugins with their own skills, agents or hooks. A popular X post is a lead, not a trusted installer.

The Codex DevOS remains the origin of this port. When the current SHA-256 of a Codex source file (`source` in `port-manifest.json`, relative to `<codex-home>`) differs from its recorded `source_sha256`, the Codex side changed: re-port only the affected files with the same adaptation rules. The receipts `hyperframes.json` and `scroll-craft.json` stay authoritative for the toolkits.

Stage changes, explain their concrete benefit, back up only affected non-secret files to a timestamped folder outside the live config, and test on a copy first (for example a throwaway `CLAUDE_CONFIG_DIR`): discovery, idempotent re-copy, merge of user edits, drift detection and rollback. Apply reversible improvements within the user's update request; do not install new external services or expand permissions merely to remove a warning.

After installing, verify hashes, settings loading, new-session instruction discovery (`/context`), precise skill triggers and representative behavior (for example: a class A edit stays with root; a class C task delegates to `devos-explorer`, `devos-worker` and `devos-reviewer`). Report any required new session/restart and untested behavior. Never promise that a currently running session has reloaded startup guidance.

For rollback, restore the backed-up files in reverse order of application. Refuse to clobber later user edits; reconcile them first. No scheduled changes, background services, telemetry or new MCP are needed for this workflow.

Port note: the Codex bundle's `scripts/health.py`, `scripts/install.py`, transaction journal and `evals/setup` target `CODEX_HOME` and are not portable; do not run them against the Claude config. The port has no installer: installation is a reviewed file copy, and evidence comes from hashes plus a fresh-session check.
