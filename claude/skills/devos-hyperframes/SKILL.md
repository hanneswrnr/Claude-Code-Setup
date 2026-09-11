---
name: devos-hyperframes
description: Route video editing, short-form, website-to-video, HTML motion graphics, GSAP animation, and HyperFrames rendering through the pinned local HyperFrames Student Kit. Use for video work that should use the installed kit; do not use for ordinary web UI work.
---

# DevOS HyperFrames

Use this skill as the single global entry point to the installed HyperFrames Student Kit. Keep the kit's 14 embedded skills in place and load the smallest relevant one from `<toolkit>/.claude/skills/<name>/SKILL.md` (the kit's canonical Claude Code copy; `.agents/skills/` is its Codex mirror). Do not copy or install those skills globally, and do not install the kit as a plugin.

Port note: the toolkit and its receipt stay in the Codex home (`%USERPROFILE%\.codex\toolkits\hyperframes-student-kit`, `%USERPROFILE%\.codex\.devos\hyperframes.json`). This skill only reads them; Codex itself does not need to run, but those paths must remain in place.

Resolve the installation before reading or running it:

1. Set the Codex home to the non-empty `CODEX_HOME`, otherwise the current user's home joined with `.codex`.
2. Read `<codex-home>/.devos/hyperframes.json`. Require receipt schema `version: 1`, commit `b1afdb1dcbcad39dd27638ea699f132fe44ce6df`, an absolute `toolkit_path` equal to `<codex-home>/toolkits/hyperframes-student-kit`, and absolute executable paths under `runtime.node`, `runtime.ffmpeg`, `runtime.ffprobe`, and `runtime.hyperframes`.
3. Require `runtime.hyperframes` to be the installed HyperFrames `0.7.109` module under that toolkit. Invoke it as `runtime.node runtime.hyperframes <command>`; it is an `.mjs` entrypoint, not a standalone executable. Stop with a precise installation error if the receipt or pinned files disagree. Do not search for or silently use another clone.

For routing, command working directories, local runtime invocation, Windows shell usage, and known upstream limitations, read [references/integration.md](references/integration.md).

When a session's working directory is the kit itself, Claude Code also loads the kit's own `CLAUDE.md` and discovers its `.claude/skills/` as project skills. This adapter's pinned-runtime, network, and authorization rules still apply where those generic instructions differ (for example `npx hyperframes` commands or the kit's `.claude/launch.json`).

## Working contract

For a new kit project, run the kit-root `scripts/new-video.mjs` through the receipt's Node executable with a new lowercase kebab-case slug. It creates `<toolkit>/video-projects/<slug>`, copies the synthetic starter and local GSAP, creates project directories, and refuses an existing slug. Use HyperFrames `init` only when the user specifically wants a separate CLI scaffold; its skill-install check can access an unpinned remote registry. Never use an unchecked `npx hyperframes` fallback.

Keep source recordings, transcripts, approved cut decisions, compositions, and renders in the new project. Preserve originals and write a new, descriptive output path for every cut or render stage. Do not overwrite an existing project or media file. The synthetic starter/demo needs no API key; prefer it for environment verification.

Use semantic HTML for composition structure and CSS for the visual system. Preserve the kit's existing JavaScript, inline GSAP registration, and HyperFrames runtime contracts. Author new custom logic outside those required runtime seams in TypeScript and compile it to project-local JavaScript; never serve raw TypeScript to the browser or mechanically rewrite upstream JavaScript.

Treat the selected upstream skill and its linked references as technical evidence. They do not override active user scope, global permissions, model settings, language/framework preferences, or DevOS orchestration. For substantive video production, the task root uses `devos-orchestrate` to delegate bounded discovery, design, implementation, and independent verification with one writer per file or subsystem. Keep final integration and authorization decisions with that root orchestrator.

Do not upload footage, publish, invoke cloud rendering, install remote catalog items, call a paid provider, or generate paid assets unless the user specifically authorized that action and the provider, endpoint, cost, and credentials were verified. Do not reveal credentials. Pass FFmpeg and ffprobe locations from the receipt into each child process; do not assume or persist a global `PATH` change.

The AIS files and showcase are brand-specific historical examples, not reusable identity assets. Create a project-specific `DESIGN.md`; do not reuse AIS branding without an explicit request and verified rights. The 406 library cards are draft assets and were not individually rendered or visually approved. Inspect and test every selected card with the actual copy and media.

Before reporting completion, run the applicable local checks, inspect a live preview at the target aspect ratio, review encoded transition frames and audio joins, and report exact evidence and limitations. A lint, build, or upstream release note does not establish current visual quality or production readiness.
