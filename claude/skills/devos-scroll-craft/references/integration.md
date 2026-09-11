# ScrollCraft integration

Read this reference after resolving the receipt and upstream skill.

## Paths and working directories

The receipt contract is:

```json
{
  "version": 1,
  "commit": "0b816225945e45380397d6a0487efa3c98916858",
  "toolkit_path": "/absolute/path/to/.codex/toolkits/scroll-craft",
  "skill_path": "plugins/nateherk-design/skills/scroll-craft",
  "runtime": {
    "node": "/absolute/path/to/node",
    "ffmpeg": "/absolute/path/to/ffmpeg",
    "ffprobe": "/absolute/path/to/ffprobe",
    "chrome": "/absolute/path/to/chrome",
    "playwright": "/absolute/path/to/toolkit/node_modules/playwright-core"
  }
}
```

Join `toolkit_path` and the relative `skill_path` only after validating both. Resolve the resulting canonical path inside the toolkit. Use the receipt's Node executable for every `.mjs` script and its FFmpeg, ffprobe, and Chrome paths for child processes. Set `SCROLLCRAFT_FFMPEG` and `SCROLLCRAFT_CHROME` only in the invoked process environment; do not edit persistent `PATH` or global configuration.

Windows shell note (Claude Code): the `cwd=<...> VAR=<...> <node> ...` lines below are notation. With the PowerShell tool, keep each invocation self-contained, for example `Push-Location "<toolkit>"; $env:SCROLLCRAFT_HOME = "<workspace>"; $env:SCROLLCRAFT_FFMPEG = "<ffmpeg>"; $env:SCROLLCRAFT_CHROME = "<chrome>"; try { & "<node>" "<skill>\scripts\doctor.mjs" } finally { Pop-Location }`. Environment changes in one tool call do not persist to later calls; never use `setx` or change user/machine variables.

Select a task-owned absolute workspace, create no output in the toolkit, and set `SCROLLCRAFT_HOME=<workspace>` before every command. Run workspace initialization from the toolkit root so ancestor configuration is bypassed:

```text
cwd=<toolkit> SCROLLCRAFT_HOME=<workspace> <node> <skill>/scripts/workspace.mjs --ensure --json
cwd=<toolkit> SCROLLCRAFT_HOME=<workspace> SCROLLCRAFT_FFMPEG=<ffmpeg> SCROLLCRAFT_CHROME=<chrome> <node> <skill>/scripts/doctor.mjs
```

Do not pass `doctor.mjs --probe` during ordinary setup: it spends a Kie API request when a key is present. Verify that `workspace.mjs --ensure` reports exactly the chosen workspace before creating a build. The toolkit root contains the pinned Playwright dependency; do not follow the upstream `npm i playwright-core` instruction in each build and do not replace the lockfile.

Keep each build under `<workspace>/builds/<name>` and review evidence under `<workspace>/lab/<name>-...`. Copy these files into a new build without editing their source or copied contents:

```text
<skill>/engine/scrollcraft.js
<skill>/engine/scrollcraft.css
```

Add project-owned semantic HTML, design CSS, and compiled `app.ts` output beside them. Use the existing project compiler when present. If the output is a new standalone site, establish the smallest project-local TypeScript build that emits ES2022 modules and pins any new tooling in its lockfile; do not change TypeScript versions or module settings in an existing project without repository evidence.

## Local preview and verification

Use the installed `serve.mjs` adaptation only after confirming it binds `127.0.0.1`, restricts requests to canonical files beneath the supplied root, serves an allowlist of web asset types, accepts only `GET` and `HEAD`, and implements real byte ranges with `206` and `416` responses. Start it with an absolute build root and an available loopback port as a background command (`run_in_background`), then stop that background task after review:

```text
cwd=<toolkit> SCROLLCRAFT_HOME=<workspace> <node> <skill>/scripts/serve.mjs --root <absolute-build> --port <port>
```

Run the screenshot harness from the toolkit root so `createRequire(process.cwd()/package.json)` resolves the pinned `playwright-core` `1.63.0`. Always provide explicit loopback URL and absolute output directories:

```text
cwd=<toolkit> SCROLLCRAFT_HOME=<workspace> SCROLLCRAFT_CHROME=<chrome> SCROLLCRAFT_FFMPEG=<ffmpeg> <node> <skill>/scripts/shoot.mjs --url http://127.0.0.1:<port> --out <workspace>/lab/<name>-desktop
cwd=<toolkit> SCROLLCRAFT_HOME=<workspace> SCROLLCRAFT_CHROME=<chrome> SCROLLCRAFT_FFMPEG=<ffmpeg> <node> <skill>/scripts/shoot.mjs --url http://127.0.0.1:<port> --out <workspace>/lab/<name>-mobile --width 390 --height 844
cwd=<toolkit> SCROLLCRAFT_HOME=<workspace> SCROLLCRAFT_CHROME=<chrome> SCROLLCRAFT_FFMPEG=<ffmpeg> <node> <skill>/scripts/shoot.mjs --url http://127.0.0.1:<port> --out <workspace>/lab/<name>-reduced --reduced-motion
```

The installed `shoot.mjs` disables `requestPointerLock`, `setPointerCapture`, `releasePointerCapture`, and `exitPointerLock` before navigation. Preserve those guards. Inspect its screenshots (image files can be opened with Read), contact sheet, `report.json`, console errors, request failures, and non-settling media; a zero exit code alone is incomplete evidence.

For a worldflight build, run `worldflight-assert.mjs` only if the installed copy has the same four pointer guards before navigation in both desktop and reduced-motion contexts. Run it from the toolkit root with the same explicit runtime environment and loopback URL. The assertions cover worldflight mechanics; still perform visual, interaction, accessibility, responsive, and reduced-motion review.

Use a real browser (the desktop Browser pane, Playwright MCP or Chrome DevTools MCP, whichever the session has) for at least the opening, every transition/device family, the engineered peak, the ending, phone composition, and reduced motion. Test keyboard order, visible focus, controls, meaningful links, and form behavior with non-production endpoints or safe mocks. Inspect slow-loading and missing-media states. Compare actual pixels rather than DOM claims.

## Encoding without replacement

The upstream `encode.sh` uses `ffmpeg -y` and will overwrite its destination. Before invoking it, canonicalize the input and output, require that they differ, require that the output does not exist, and create a new versioned filename. On POSIX, set `SCROLLCRAFT_FFMPEG` to the receipt path and prepend the receipt ffprobe directory to that child process only.

On Windows, invoke the receipt's native FFmpeg executable directly with the PowerShell tool rather than routing `encode.sh` through Bash (Claude Code's Bash tool is Git Bash). Preserve the script's dense-GOP behavior while using `-n` to refuse overwrite; in PowerShell, quote the `-vf` filter value:

```text
<ffmpeg> -n -hide_banner -loglevel error -i <input> -an -vf scale=-2:1080:flags=lanczos,format=yuv420p -c:v libx264 -profile:v high -preset slow -crf 20 -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart <fresh-desktop-output>
<ffmpeg> -n -hide_banner -loglevel error -i <input> -an -vf scale=-2:720:flags=lanczos,format=yuv420p -c:v libx264 -profile:v high -preset slow -crf 24 -g 4 -keyint_min 4 -sc_threshold 0 -movflags +faststart <fresh-mobile-output>
```

Use `runtime.ffprobe` to verify codec, dimensions, frame rate, duration, GOP behavior, audio absence, and a decodable first/middle/last frame. The supplied `encode.sh` has no portrait mode; design and verify portrait assets explicitly rather than treating the 720px-height mobile preset as portrait cropping.

## External assets

Prefer supplied or locally created assets. Record source path or URL, license/rights, checksum, transformations, and selected output. Inspect full-resolution source and encoded media; CSS filters do not repair unsuitable source lighting, framing, or clipping.

Do not run `<skill>/scripts/kie.mjs`, including `probe`, based only on a discovered key or an upstream suggestion. If the user specifically selects Kie.ai:

1. Verify current official endpoints, model IDs, request fields, upload behavior, pricing, balance, and the exact assets that would leave the machine.
2. Obtain or confirm authorization for the concrete paid calls and uploads. Never print or copy the key.
3. Adapt the workflow so the create response's task ID, model, prompt, input hashes, endpoint, timestamp, cost estimate, and intended output path are atomically persisted under the build before polling.
4. Resume polling with that task ID after interruption or transient errors. Bound retries and never create a replacement job automatically.
5. Download into a fresh temporary output, validate content type and media integrity, then move it to a new final asset path. Inspect the result before use.

No missing photo, failed generation, or absent key authorizes a fallback paid service. Do not publish, deploy, upload the site, or connect real form endpoints as part of local production.

## Completion evidence

Report the selected grammar, journey, feeling curve and peak, signature move, four-or-more device-family check where applicable, final output path, compiler/build results, tested viewports, reduced-motion behavior, verified interactions, server Range checks, screenshot/contact-sheet observations, console and request failures, media probe results, and remaining gaps. Keep evidence with the task workspace. A contact sheet, automated assertion, or successful build is one kind of evidence and does not by itself prove the final experience is polished or accessible.
