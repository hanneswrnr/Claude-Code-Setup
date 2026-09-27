---
name: menudeck-offene-setup-korrektur
description: Zwei offene MenuDeck-Punkte aus dem Erst-Setup -- die faellige README-Korrektur und ein npm-audit-Befund fuer den P8-Security-Review
metadata: 
  node_type: memory
  type: project
  originSessionId: 4447cc85-a23c-4716-98f5-4a5845f2d0dc
  modified: 2026-08-03T22:28:23.435Z
---

Stand 2026-08-04, HEAD `08f5c85`, Tree sauber. Zwei Punkte sind **gefunden, aber noch nicht ins
Repo geschrieben** -- sie stehen nirgends in `.md`-Dateien des Projekts und gehen sonst verloren:

**(1) Die README-Korrektur ist faellig.** `docs/menudeck-naechste-schritte.md` beauftragt
ausdruecklich, wer zuerst auf einem frischen Rechner aufsetzt, moege die Anleitung pruefen und
korrigieren ("eine Anleitung, die nie von null gefahren wurde, ist eine Behauptung"). Das ist
geschehen, die Luecken stehen in [[menudeck-setup-windows]]: fehlendes WSL2, kein
Windows-Installationsweg fuer die Supabase CLI, die Zwei-Binaerdateien-Falle, das fehlende `npx
playwright install`. Dazu ein Nebenbefund: `next build` waehlt `C:\Users\hanne\package-lock.json`
als Workspace-Wurzel, weil dort eine projektfremde Lockfile liegt.

**Why:** Der Auftrag stammt aus dem Handoff-Dokument des Projekts selbst und ist die einzige
Aufgabe, die genau einmal erledigt werden kann -- beim naechsten Setup ist der Rechner nicht mehr
frisch.
**How to apply:** Als eigener Commit in `README.md`, Abschnitt "Lokale Entwicklung"; volle Suite
davor, Tree danach sauber (Arbeitsregeln des Projekts).

**(2) `npm audit` meldet 8 Schwachstellen, 4 davon hoch -- und die relevanten treffen `next@15.5.20`
genau an der Flaeche, um die es in P6/P7/P8 durchgehend ging:** *Unauthenticated disclosure of
internal Server Function endpoints*, *SSRF in Server Actions on custom servers*, *Unbounded Server
Action payload*, *Cache confusion of response bodies*. Behebbar laut npm **ohne** Breaking Change
(`npm audit fix`); die vitest/esbuild-Kette dagegen nur mit `--force` (vitest 4).

**Why:** Die gesamte Zugriffsarchitektur steht auf Server Actions mit serverseitiger Session. Eine
geprueft Zusicherung wie "alle elf Server Actions nehmen keine Mandantenkennung aus den Argumenten"
sagt nichts ueber einen Framework-Pfad, der Server-Function-Endpunkte unauthentifiziert offenlegt.
**How to apply:** Nicht nebenbei. Gehoert als benannter Schwerpunkt in den anstehenden
P8-Security-Review, mit voller Suite nach dem Update und eigenem Commit.
