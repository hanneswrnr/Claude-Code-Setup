---
name: powershell-no-double-ampersand
description: Hannes' shell is Windows PowerShell 5.1 — `&&` is a parser error; chain with `;` or separate commands.
metadata:
  type: user
---

Hannes arbeitet lokal in Windows PowerShell 5.1. Dort ist `&&` kein gueltiges Trennzeichen ("Das Token '&&' ist in dieser Version kein gueltiges Anweisungstrennzeichen").

**Why:** Am 20.09.2026 scheiterten zwei lange Befehlsketten mit `&&` komplett, es wurde kein einziger Befehl ausgefuehrt.

**How to apply:** Befehle fuer Hannes immer einzeln in eigene Codebloecke schreiben, nie mit `&&` verketten. Fuer "nur wenn erfolgreich": `A; if ($?) { B }`. Siehe auch [[claude-cli-version-mismatch]].
