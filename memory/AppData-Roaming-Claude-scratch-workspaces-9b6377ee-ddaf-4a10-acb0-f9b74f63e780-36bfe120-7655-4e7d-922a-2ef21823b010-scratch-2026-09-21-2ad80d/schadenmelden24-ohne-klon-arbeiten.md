---
name: schadenmelden24-ohne-klon-arbeiten
description: Bewaehrter Weg fuer SchadenMelden24, wenn git clone abbricht - Tarball, lokales git, Git-Data-API, mit zwei Fallen
metadata:
  type: feedback
---

Auf Hannes' Rechner bricht `git clone`/`fetch` des 344-MB-Repos ab. Bewaehrt hat sich (22./23.09.2026, sechs PRs ohne einen fehlerhaften Diff):

1. `gh api repos/.../tarball/<sha>` in einen kurzen Pfad unter dem Benutzerordner entpacken, dort `git init` + ein Basis-Commit. Arbeitskopien daraus mit `git -c core.autocrlf=false clone`.
2. Aenderungen lokal committen; `npm ci`, tsc und vitest laufen dann echt.
3. Uebertragen per Git-Data-API: Blobs, Tree mit base_tree, Commit, Ref. Den Branch auf GENAU dem GitHub-Commit aufsetzen, von dem die Kopie stammt, nicht auf dem aktuellen main - GitHub merged dann dreifach und ueberschreibt keine parallelen Aenderungen.
4. Gegenprobe: Zeilenzahl +/- im GitHub-Compare muss exakt der lokalen `git diff --shortstat` entsprechen.

**Why:** Zwei Fallen: (a) systemweit ist `core.autocrlf=true` gesetzt - ein normaler Clone checkt LF-Dateien als CRLF aus, das ergibt Ganzdatei-Diffs; (b) die GitHub-Dateien sind alle LF, beim Hochladen daher auf den Zeilenende-Stand des GitHub-Blobs normalisieren. PDFs/.ai-Dateien nie normalisieren (kein NUL am Anfang, trotzdem binaer).

**How to apply:** Bei sieben parallelen Sitzungen laeuft main schnell weiter: vor jedem Merge `mergeable` pruefen; bei Konflikt frischen Tarball ziehen und neu aufsetzen, statt Konflikte blind aufzuloesen. Vercel prueft keine Typen (ignoreBuildErrors) - tsc lokal ist der einzige Typnachweis. Siehe [[schadenmelden24-mobile-restlos-weg]].
