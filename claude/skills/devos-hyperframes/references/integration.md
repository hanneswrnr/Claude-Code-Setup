# HyperFrames integration

Read this reference after resolving the pinned toolkit and before running its skills or commands.

## Route to the embedded skills

Build each skill path by joining the receipt's absolute `toolkit_path` with `.claude/skills/<skill>/SKILL.md`. Resolve every relative link and script path from the embedded skill's own directory unless it explicitly names the kit root or project directory.

Port note: the kit ships two mirrors of the same 14 skills, `.claude/skills/` (canonical, used by Claude Code) and `.agents/skills/` (Codex copy); the receipt pins both. They are hash-identical except the `SKILL.md` of `cut-mistakes`, `cut-silences` and `short-form-edit`, which have assistant-specific variants: use the `.claude` variant. Helper scripts are identical in both mirrors. Outside the kit directory these embedded skills are not registered as `/` commands; read their `SKILL.md` directly.

| Request | Embedded skill |
| --- | --- |
| Full recording edit and stage coordination | `edit-video` |
| Reels, Shorts, and new short advertisements | `short-form-edit` |
| Maintenance of the legacy May Shorts examples | `short-form-video` |
| Silence removal and transcript retiming | `cut-silences` |
| Reviewed stutter, repeat, false-start, and retake cuts | `cut-mistakes` |
| New motion-graphics video from a brief | `make-a-video` |
| Website capture followed by a video | `website-to-hyperframes` |
| Narrative arc, spatial world, and callbacks | `video-storytelling` |
| Transcript-anchored overlay beats and cards | `hyperframes-video-beats` |
| Local draft card styles and scene templates | `style-library` |
| Composition HTML, timing, captions, and media | `hyperframes` |
| Local CLI, preview, diagnostics, and render | `hyperframes-cli` |
| GSAP timelines and animation technique | `gsap` |
| Remote HyperFrames registry discovery or installation | `hyperframes-registry` |

Prefer `short-form-edit` for new reels. `short-form-video` refers to a missing `seedance-loop-prompt` skill and private historical memories; those are not installed capabilities. Do not fabricate them or treat their absence as permission to call another generator.

Load `edit-video` first for a complete edit, then only the stage skills needed for the requested outcome. Load `MOTION_PHILOSOPHY.md` and the project's `DESIGN.md` before a creative build. The project brief controls pacing and visual identity.

## Paths and processes

The receipt contract is:

```json
{
  "version": 1,
  "commit": "b1afdb1dcbcad39dd27638ea699f132fe44ce6df",
  "toolkit_path": "/absolute/path/to/.codex/toolkits/hyperframes-student-kit",
  "runtime": {
    "node": "/absolute/path/to/node",
    "ffmpeg": "/absolute/path/to/ffmpeg",
    "ffprobe": "/absolute/path/to/ffprobe",
    "hyperframes": "/absolute/path/to/hyperframes/cli.mjs"
  }
}
```

Use the actual platform paths from the receipt. Validate file existence and resolve canonical absolute paths before invocation. When a kit script shells out to `ffmpeg` or `ffprobe`, construct the child environment from the current environment plus the parent directories of `runtime.ffmpeg` and `runtime.ffprobe` prepended to that child process's `PATH`. Restore the caller environment afterward; never edit machine or user `PATH`.

Windows shell note (Claude Code): prefer the PowerShell tool and keep each invocation self-contained. Quote every receipt path, use the call operator, set the working directory with `Push-Location`/`Pop-Location`, and prepend the FFmpeg directory for the child inside the same call, for example `Push-Location "<toolkit>"; $env:PATH = "<ffmpeg-dir>;" + $env:PATH; try { & "<runtime.node>" "<toolkit>\scripts\preflight.mjs" "<project>" } finally { Pop-Location }`. Environment changes in one tool call do not persist to later calls; never use `setx` or change user/machine variables. In the Bash tool (Git Bash) use POSIX paths with a command-scoped assignment such as `PATH="/c/<ffmpeg-dir>:$PATH" "<node>" ...`.

Run kit utilities with the kit as the working directory and absolute project arguments:

```text
<runtime.node> <toolkit>/scripts/new-video.mjs <slug>
<runtime.node> <toolkit>/scripts/preflight.mjs <project>
<runtime.node> <toolkit>/scripts/validate-beat-sync.mjs <project>
<runtime.node> <toolkit>/.claude/skills/cut-silences/scripts/cut-silences.mjs ...
<runtime.node> <toolkit>/.claude/skills/cut-mistakes/scripts/find-cut-candidates.mjs ...
<runtime.node> <toolkit>/.claude/skills/cut-mistakes/scripts/apply-cuts.mjs ...
```

The last three commands preserve the embedded skills' argument order and project-relative output conventions. Read their `--help` or source before composing a command. Never mix timestamps from the original recording with footage already retimed by a prior cut.

Run HyperFrames from the video project directory through the pinned module:

```text
<runtime.node> <runtime.hyperframes> <command> [options] [project-directory]
```

Before using a CLI command or flag copied from an upstream skill, inspect `<runtime.node> <runtime.hyperframes> <command> --help`; the installed `0.7.109` grammar is authoritative. The verified local forms include:

```text
<node> <hyperframes> lint <project>
<node> <hyperframes> validate <project>
<node> <hyperframes> inspect <project> --at-transitions
<node> <hyperframes> check <project> --at-transitions
<node> <hyperframes> snapshot <project> --frames 5 --describe false --output <new-directory>
<node> <hyperframes> preview <project> --no-open
<node> <hyperframes> render <project> --quality draft --workers 1 --output <new-file>
```

`validate` and `inspect` remain available but the installed CLI marks them deprecated in favor of the combined `check` command. Use `lint` plus `check` for the normal gate, and use `inspect` or `snapshot` when their focused artifacts aid review. Always pass `--describe false` unless the user explicitly chose Gemini vision; `snapshot` otherwise uses Gemini automatically when a key is present. Rendering uses `--workers 1` for this kit's video-layer stability. A preview server is a local process: start it as a background command (`run_in_background`), inspect the printed local URL with the session's browser surface (desktop Browser pane `navigate` plus `resize_window` at the delivery aspect ratio, or Playwright MCP), and stop the background task when the review is done. Do not use the kit's `.claude/launch.json`: it starts `npx hyperframes preview` for one fixed example project. If a Browser-pane launch configuration is useful, set `runtimeExecutable` to `runtime.node` and `runtimeArgs` to `runtime.hyperframes`, `preview`, the project directory and explicit `--no-open`/`--port` values.

The kit initializer and the CLI initializer solve different problems. `scripts/new-video.mjs <slug>` is the default: its slug must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`, it creates a project below the pinned toolkit, and it refuses replacement. `hyperframes init [NAME]` creates a standalone CLI scaffold and currently checks AI skills against GitHub unless `HYPERFRAMES_SKIP_SKILLS=1` is set; `--skip-skills` is documented as temporarily ignored. Do not use that remote check during ordinary kit work. Invoke the receipt's module directly rather than `npx`: outside a package with the pinned dependency, `npx` may fetch an unchecked current package.

## Provider and network boundaries

Local TTS in HyperFrames `0.7.109` uses Kokoro. HyperFrames transcription uses a local ASR engine when available. The separate kit script `scripts/transcribe-elevenlabs.mjs` uploads audio and consumes the user's ElevenLabs access; run it only when that provider and upload were explicitly chosen. Kie.ai is optional and paid. Do not fall back from a missing local tool to ElevenLabs, OpenAI, Kie.ai, Gemini, a registry download, or any other paid or remote API.

For website capture, the supplied URL authorizes reading that site for the requested task, subject to the user's scope. Pass `--skip-vision` unless the user explicitly chose Gemini image descriptions. Keep downloaded source provenance and do not expose authenticated screens or credentials.

`hyperframes-registry` points at an unpinned GitHub `main` registry. Inspect the requested item manifest, code, transitive registry dependencies, license, and resolved commit before proposing installation. Do not auto-download it. Likewise, library templates that use public CDNs need dependency review and localization before a final offline artifact.

Do not run `publish`, `cloud`, `lambda`, `cloudrun`, `auth`, or other external mutations without matching user authorization. Keep telemetry disabled according to the installed environment rather than changing account or project settings from this adapter.

## Known upstream gaps

- `.claude/skills/hyperframes/scripts/animation-map.mjs` (identical in `.agents/skills/`) imports the absent `@hyperframes/producer` package through an invalid local path. Do not claim or use it until a separately reviewed repair supplies the pinned dependency and correct import. Use local `check`, `inspect`, and `snapshot` evidence instead.
- `video-storytelling` names project-specific `scripts/qa-*.mjs`, `scripts/integrate.mjs`, and `qa/v4/flicker/qa-flicker.mjs` that are not shipped. Do not invent or report those gates as passed. Use the installed CLI checks plus explicit contiguous-frame, seam, audio, and visual review; state which specialized checks remain unavailable.
- The 406 style-library cards passed distribution-level path and manifest checks in the upstream release, but they were not all rendered. Treat each selected card as a draft and verify its actual DOM, dependencies, copy fit, motion, and encoded frames.

## Review evidence

For every changed project, keep evidence under the project rather than altering the toolkit distribution. At minimum:

1. Run the kit preflight and HyperFrames `lint`.
2. Run `validate-beat-sync` only when the project uses anchored sub-compositions and a compatible transcript; otherwise record why it does not apply.
3. Run HyperFrames `check --at-transitions`, then capture focused snapshots with remote description disabled.
4. Inspect the live preview at the delivery aspect ratio and relevant frame sizes.
5. Render to a new draft filename, inspect hero frames and contiguous transition strips, watch the encoded motion, and listen across every edit and audio join.
6. Record exact commands, exit codes, artifact paths and hashes, inspected timestamps, revisions, unavailable modalities, and remaining risks. Never promote upstream release evidence or an empty tool result to a pass for the current project.

Publishing or uploading the finished artifact is a separate external action and requires explicit authorization.
