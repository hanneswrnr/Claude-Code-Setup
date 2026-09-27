---
name: stale-local-checkout-mobile-risk
description: "Der 4K+-Zaehler in VS Code kam von einem 2128 Commits alten HEAD, nicht von echter Arbeit — am 2026-08-08 bereinigt; Diagnose-Rezept fuer den Wiederholungsfall"
metadata: 
  node_type: memory
  type: project
  originSessionId: f39e72ac-b8d9-42c4-af68-421a729918a9
  modified: 2026-08-08T20:18:08.478Z
---

**Erledigt am 2026-08-08.** Der Checkout unter `C:\Users\hanne\Desktop\SchadenMelden24-main`
zeigte in VS Code **4K+ Aenderungen**. Ursache war **nicht** lokale Arbeit, sondern ein
HEAD, der **2128 Commits** hinter `origin/main` stand (`e6dc1270` statt `e28fe132`).
Die Dateien auf der Platte waren bereits **byte-identisch** mit `origin/main` — VS Code
verglich nur gegen den alten Zeiger.

Behoben mit `git reset --mixed origin/main` (schreibt keine einzige Datei), danach
`git clean -f` fuer 22 Altlasten und `git branch --set-upstream-to=origin/main main`.
Endstand: sauberer Baum, 0/0 gegen den Remote. Backup der 22 Dateien lag im
Session-Scratchpad; dauerhaft wiederherstellbar bleiben sie ueber
`git checkout e6dc12704aa53ee64213d52f2dcf8894230fc8aa -- <pfad>`.

**Warum das gefaehrlich war:** Der alte HEAD trackte `Mobile_Schadenmelden24/` noch,
`origin/main` hatte den Ordner entfernt. Ein Merge/Push von lokal `main` haette die 237
Dateien wieder eingeschleppt — der Fehler, der laut `CLAUDE.md` schon **viermal**
passiert ist. Auch die 22 Altlasten enthielten `ios-build.yml`/`android-build.yml`; ein
`git add -A` haette sie zurueckgebracht.

**Diagnose-Rezept, falls der Zaehler wieder hochgeht** — erst messen, nie raten:
```bash
git fetch origin main
git rev-list --left-right --count origin/main...HEAD   # links gross = Checkout veraltet
# echte Abweichung Platte vs. Remote, ohne irgendetwas anzufassen:
GIT_INDEX_FILE=/tmp/probe.idx git read-tree origin/main
GIT_INDEX_FILE=/tmp/probe.idx git update-index --refresh -q
GIT_INDEX_FILE=/tmp/probe.idx git diff-index --name-status origin/main   # 0 Zeilen = nur der Zeiger
GIT_INDEX_FILE=/tmp/probe.idx git ls-files --others --exclude-standard   # Reste
```

Nebenbefund: `git worktree add` scheitert in diesem Repo am Windows-Pfadlaengen-Limit
(`.planning/features/werkstatt-gruppen/branding/.../Flag`). Fuer Einzeldatei-Commits auf
einen fremden Stand stattdessen `hash-object` + `read-tree` + `commit-tree` + `push
<sha>:main` nutzen. Die Git-Identitaet war nur global ungesetzt und musste lokal auf
`hanneswrnr <hannes-werner@outlook.de>` gesetzt werden.

Siehe auch [[keine-co-authored-by]] und [[project_install_quirks]].
