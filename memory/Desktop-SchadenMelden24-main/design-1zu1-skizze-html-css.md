---
name: design-1zu1-skizze-html-css
description: "PO-Regel 19.09.2026 – umgesetzte Oberflächen müssen 1:1 die Elemente der Skizze/Bausteine-Galerie sein (gleiches CSS, gleiche Struktur); Design in HTML/CSS, Logik in TypeScript; Schrift auf Akzentflächen weiß; volle Breite wie der Seitenkopf"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 10a4f912-c6fb-4fc9-863d-dda4ecf791af
  modified: 2026-09-19T19:15:27.476Z
---

Der Nutzer hat die Vercel-Vorschau des Auftragssystems am 19.09.2026 zurückgewiesen: (1) Inhalt war auf 1100 px begrenzt statt volle Breite wie der Seitenkopf (PageHero), (2) die Elemente waren nur mit Tailwind „nachgebaut" und sahen nicht 1:1 aus wie in der Skizze, (3) Schrift auf orangen Knöpfen war dunkel (Token `--role-accent-fg` = orange-950), soll aber weiß sein wie in der Galerie.

**Why:** Die Skizze wurde mit dem Nutzer Element für Element abgestimmt; jede Nachbildung weicht sichtbar ab. Der Nutzer will künftig generell: HTML/CSS für alles Sichtbare, TypeScript für alles Funktionale.

**How to apply:** Neue oder umgebaute Oberflächen nicht mit Tailwind nachbauen, sondern die Galerie-CSS (bausteine.html) bzw. die Skizzen-CSS 1:1 als echte CSS-Datei übernehmen (Präfix gegen Namenskollisionen) und dieselbe HTML-Struktur/Klassen wie in der Skizze rendern; Logik bleibt in TypeScript. Vor Abgabe Skizze und Umsetzung nebeneinander im Browser vergleichen (berechnete Stile messen). Inhalte volle Breite mit demselben Rand wie der Seitenkopf. Schrift auf Akzentflächen immer weiß. Verwandt: [[auftragssystem-konzept]].
