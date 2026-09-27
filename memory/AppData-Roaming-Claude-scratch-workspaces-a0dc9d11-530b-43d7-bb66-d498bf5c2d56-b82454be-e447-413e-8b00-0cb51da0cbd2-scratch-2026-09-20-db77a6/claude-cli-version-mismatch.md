---
name: claude-cli-version-mismatch
description: Old npm-global claude CLI on Windows PATH breaks plugin/marketplace commands; use the desktop app's bundled newer claude.exe or update npm global.
metadata:
  type: feedback
---

Auf Hannes' Windows-Rechner lag lange eine alte, global per npm installierte Claude-CLI (2.0.76) im PATH unter `%APPDATA%\npm\claude`, waehrend die Desktop-App eine neuere Version unter `%APPDATA%\Claude\claude-code\<version>\claude.exe` mitbringt. Die alte CLI lehnt neuere Marketplace-Manifeste ab ("Invalid schema: Unrecognized key(s) ... displayName") und meldet vorhandene Plugins als "not found in marketplace".

**Why:** Am 20.09.2026 scheiterten dadurch `claude plugin marketplace add anthropics/claude-for-legal` und mehrere `claude plugin install ...@claude-plugins-official`, obwohl die Plugins im Manifest standen.

**How to apply:** Bei unerklaerlichen Plugin-/Marketplace-Fehlern zuerst `claude --version` gegen `ls %APPDATA%\Claude\claude-code` pruefen. Notfalls die gebuendelte `claude.exe` direkt aufrufen, und den globalen Stand mit `npm install -g @anthropic-ai/claude-code@latest` nachziehen (am 20.09.2026 auf 2.1.278 gebracht). Siehe auch [[powershell-no-double-ampersand]].
