---
name: abgabe-pruefliste-knoepfe-redirects
description: "Zwei Fehler, die der Product Owner am 13./14.09.2026 selbst finden musste und die nicht wieder vorkommen sollen – Primärknöpfe in Rollenfarben (rolePrimaryButton) und keine redirect()-Aufrufe aus Layouts unter loading.tsx"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a725a692-8488-40bd-9da6-7a626b54668f
  modified: 2026-09-13T23:22:27.242Z
---

Vor jeder Abgabe in SchadenMelden24 zwei Dinge selbst prüfen, die der Product Owner nicht noch einmal melden will:

1. **Primärknöpfe:** Jeder neue Aktions-Knopf über `rolePrimaryButton(role, extra?)` aus `lib/role-theme.ts`, nie ein solides `bg-orange-600/700` oder andere feste Farben. Im Browser gegen die Rollenfarbe (Werkstatt = heller Orange-Verlauf) ansehen.
2. **Umleitungen:** Kein `redirect()` aus einem Layout auf ein Ziel unter demselben Layout, wenn ein `loading.tsx` darüber liegt (Admin- und HQ-Layout). Auth-Umleitungen gehören als echter 307 in `middleware.ts`; danach hart per `window.location` navigieren. Die Middleware sieht keine Flight-Header (RSC/Prefetch).

**Why:** Der Product Owner fand beide Fehler erst nach dem Deploy selbst (dunkle Knöpfe in Lager/Marktplatz; leere Admin-2FA-Seite bis zum Reload). Beide sind global im Lernloop gespeichert (L-20260914-68c6bf, Knopf-Lektion vom 14.09.2026) und im Wiki dokumentiert (`wiki/04-Patterns/Design-System-UI.md`, `wiki/05-Anti-Patterns/Redirect-aus-Layout-unter-Loading-Boundary.md`).

**How to apply:** Beide Punkte in die eigene Abnahme aufnehmen, bevor „fertig" gemeldet wird; der Lernloop liefert dieselben Regeln auch in anderen Projekten. Siehe [[schadenmelden24-commit-regeln]].
