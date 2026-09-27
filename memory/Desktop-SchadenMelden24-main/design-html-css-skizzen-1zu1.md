---
name: design-html-css-skizzen-1zu1
description: "PO-Entscheidung 19.09.2026 — Design nur HTML/CSS, Funktion TypeScript, Skizzen 1:1; steht in CLAUDE.md + ADR 0024 + wiki/04-Patterns/Skizze-1zu1-Einbau.md; Präfixe der Nutzerführungs-Bereiche re- … os-"
metadata: 
  node_type: memory
  type: project
  originSessionId: efa8ef76-a78e-4f52-aa81-bafef39f305c
  modified: 2026-09-19T19:24:20.376Z
---

Am 19.09.2026 hat der Product Owner entschieden: In SchadenMelden24 wird ab sofort alles Design in HTML/CSS gebaut, TypeScript nur für Funktion, abgenommene Skizzen werden 1:1 eingebaut. Die Regel steht seit Commit 83408854 (origin/main) in der Projekt-CLAUDE.md, in ADR `wiki/07-Decisions/0024-Design-in-HTML-CSS.md` und in der Anleitung `wiki/04-Patterns/Skizze-1zu1-Einbau.md` (Präfix-Tabelle, drei Umbenennungen `.x`→`.bs-x`, `--x`→`--bs-x`, `sk-x`→`<präfix>-x`, Nachweis). Eingetragen hat sie der Termin-Chat; das Fundament (`styles/bausteine.css` + Skripte) baut der Auftrags-Chat.

**Why:** Der PO hatte gesehen, dass eine Skizze nicht 1:1 umgesetzt wurde. Mit demselben HTML/CSS in Skizze und App entfällt das Übersetzen.

**How to apply:** Skizzen müssen baureif sein (nur Galerie-Tokens, keine Inline-Stile für Gestaltung; Werte aus Daten nur als CSS-Variable). Die Nutzerführungs-Bereiche haben diese Präfixe angemeldet: `re-` 01, `pv-` 02, `ek-` 03, `mh-` 04, `bn-` 05, `ue-` 06, `kf-` 07; reserviert `kp-` 08, `vw-` 09, `ww-` 10, `sd-` 11, `vb-` 12, `ad-` 13, `os-` 14. Ausnahme E-Mails: inhaltlich 1:1, Gestaltung über den Mail-Rahmen. Bezug: [[nutzerfuehrung-gesamtplanung]].
