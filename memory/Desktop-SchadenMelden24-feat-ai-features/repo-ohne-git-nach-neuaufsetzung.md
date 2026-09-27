---
name: repo-ohne-git-nach-neuaufsetzung
description: Der Ordner Desktop/SchadenMelden24-feat-ai-features ist seit 13.09.2026 eine Zip-Kopie von feat/ai-features (e944ee06, 26.08.2026) ohne .git und ohne node_modules; PC wurde am 09.09.2026 neu aufgesetzt
metadata:
  type: project
---

Stand 13.09.2026: Der Arbeitsordner `C:\Users\hanne\Desktop\SchadenMelden24-feat-ai-features` hat **kein `.git`** und keine `node_modules`. Alle Dateien tragen den Zeitstempel 13.09.2026 20:11 — eine heruntergeladene Kopie des Branch-Stands `feat/ai-features` (Commit e944ee06 vom 26.08.2026). Der frühere Worktree `C:\Users\hanne\sm24-ai-features` existiert nicht mehr (PC-Neuaufsetzung 09.09.2026, siehe Remote-Branch `backup/wip-sm24-ai-features-20260909`, der nur 15 Marketing-Video-Dateien über e944ee06 hinaus enthält).

**Why:** Ohne Git können Änderungen weder committet noch mit `main` (61 Commits voraus, Stand 04.09.2026) abgeglichen werden; `gh` ist als hanneswrnr angemeldet.

**How to apply:** Vor Code-Arbeit das Repo frisch klonen (kurzer Pfad, z. B. `C:\Users\hanne\sm24`), `feat/ai-features` auschecken und die Zip-Kopie nur als Referenz nutzen. Siehe [[ki-launch-frist-avv]].
