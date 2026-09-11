---
name: devos-bootstrap
description: Establish or refresh concise project instructions (CLAUDE.md) when onboarding a repository or starting a new software project.
---

# Project onboarding

Inspect existing instruction files (`CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/`, nested `CLAUDE.md` files and any `AGENTS.md` kept for other agents), git state, manifests, lockfiles, CI, key entry points, migration files and deployment configuration. Infer stack and commands from evidence; do not run package scripts before inspecting their purpose. Preserve the chosen package manager and versions. Do not expose `.env` values.

For a project that needs durable context, create or carefully merge a short repository `CLAUDE.md` containing only:

- Product purpose and important module/ownership boundaries.
- Verified install/dev/build/typecheck/test commands and required environment variable names, never values.
- Project-specific invariants and the testing evidence expected for sensitive changes.
- Deployment target/recovery prerequisites if known, with unsupported assumptions labeled.

Check instruction precedence and nested instructions before writing. Claude Code reads `CLAUDE.md`, not `AGENTS.md`: it concatenates `CLAUDE.md`/`CLAUDE.local.md` from the working directory and its ancestors at launch, and loads subdirectory files and path-scoped `.claude/rules/` on demand. If the repository already maintains `AGENTS.md` for other agents, let `CLAUDE.md` import it with a line `@AGENTS.md` and add only Claude-specific lines instead of duplicating it. Keep existing team rules; do not copy the entire global core or skill catalog. Put one non-obvious architectural decision in a small ADR only if it will save future investigation. A project without meaningful gaps needs no new files. The built-in `/init` may draft a file; trim its output to the list above.

For brand-new work, choose architecture from requirements and constraints rather than always scaffolding the same framework. Existing project-specific instructions outrank generic preferences within their scope. For substantial UX/service/mobile work route to the relevant available skill. Create/check an app before documenting its commands as working.

Run this when opening a new project only if useful; never rewrite instructions at every start. Read-back the final instructions and verify referenced paths and commands; in a new session `/context` shows which memory files actually loaded. Explain what future tasks will inherit, and which commands remain untested.

For new web projects, locate the verified `web-kit` in the DevOS source bundle recorded as `source_bundle` in `<codex-home>/.devos/state.json` (`CODEX_HOME`, otherwise `%USERPROFILE%\.codex`; port dependency: the bundle stays on the Codex side); read its README. Reuse suitable TypeScript, CSS and QA pieces after inspecting requirements. Do not copy node_modules, reports, generated output or a fixed visual theme into every app. Preserve an existing framework and package manager. Establish project-local typecheck, tests and build commands plus a CI recipe where absent; adapt paths and environment. Remote branch protection is a separate repository action and is not enabled by a local YAML file. See [web quality](references/web-quality.md) for adoption and acceptance.
