---
name: startseiten-video-kino-buehne
description: "Startseiten-Video „So funktioniert“ als Kino-Bühne mit 30-s-Showreel; LIVE seit 28.09.2026 (PR #222, Merge d85b8902); 9:16-Fassung auf Zweig video/showreel-30s-9x16 in Arbeit"
metadata:
  node_type: memory
  type: project
  originSessionId: b7790e34-cafe-48c3-9ada-ba38af10d979
  modified: 2026-09-28T20:21:29.082Z
---

LIVE seit 28.09.2026: PR #222 gemergt (d85b8902), Vercel-Produktion READY. `components/shared/VideoShowcase.tsx` + `styles/video-showcase.css` (Präfix `vs-`), Video `public/videos/showreel-30s.mp4` (12 MB, `.gitignore`-Ausnahme). Zweig `feat/homepage-showreel-video` liegt noch auf GitHub (Löschen per Safety Net gesperrt, harmlos).

PO-Vorgaben: Selbststart + Endlosschleife mit „Auf Null“-Animation; Ton nie dauerhaft (gilt einen Durchlauf); moderne Kino-Bühne statt Box. Zeitleiste/Lautstärkeregler bewusst entfernt; 12 MB Selbstladen (Option: Handy-Fassung).

Instagram 9:16 FERTIG 28.09.2026: `C:\Users\hanne\Videos\SchadenMelden24-Showreel-30s-9x16.mp4` (1080×1920, 60 fps, 30 s, gleicher Ton), Commit 1ae2afce auf Zweig `video/showreel-30s-9x16` gepusht (kein Merge nach main nötig). Quellprojekt `marketing/showreel-30s` auf Zweig `video/showreel-30s` (Film-Hash = Startseiten-Quelle). Hochformat per `?format=hoch` (`html[data-format="hoch"]`, Bühne 1080×1920, CSS in `hoch/*.css`), Worktree `C:\Users\hanne\sm24-reel916`, Zweig `video/showreel-30s-9x16`. Aufnahme mit `SM24_CHROMIUM` = installierte headless_shell (Playwright-Version passt sonst nicht). Referenz-Standbilder der Querfassung: `C:\Users\hanne\sm24-ref-quer`.

**Why:** Weiterarbeit braucht den Stand und die festgelegten Wünsche.
**How to apply:** Querformat darf sich durch das Hochformat nicht ändern (Standbilder gegen Referenz vergleichen). Siehe [[design-html-css-skizzen-1zu1]].
