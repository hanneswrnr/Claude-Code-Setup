---
name: reference-aufnahme-exitcode
description: "tools/aufnahme.mjs often ends with exit code 255 although the screenshot was written — check the \"geschrieben:\" line"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 69962245-3585-4b8c-b499-d298b527753e
  modified: 2026-09-11T10:04:38.577Z
---

`node tools/aufnahme.mjs <breite> <seite> <scroll> <vh> <port> [--bewegt]` in Raumgestaltung-Hartung frequently returns exit code 255 when run from PowerShell, even though the PNG was written (seen 2026-09-11, several runs). Cause is the headless Chrome child being killed at the end, not a failed capture.

How to apply: judge success by the `geschrieben: <datei>` line and the file on disk, not by the exit code. Set `AUFNAHME_BASIS` to the running static server (e.g. http://127.0.0.1:5317), and move the PNGs into the scratchpad afterwards. Related: [[project-hartung-kein-git]].
