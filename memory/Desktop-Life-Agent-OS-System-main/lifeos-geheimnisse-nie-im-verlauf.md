---
name: lifeos-geheimnisse-nie-im-verlauf
description: Im Projekt Life Agent OS darf kein Geheimniswert und auch keine Bytegröße eines Geheimnisses in Chat oder Bericht geraten
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 561d24da-981b-4394-b903-1b86f46afb8a
  modified: 2026-08-06T22:47:32.223Z
---

Kein Schlüssel, Passwort oder Token gerät in den Verlauf — **kein Wert, kein Ausschnitt und auch
keine Länge**. Das schließt `ls -l` auf einen Geheimnispfad ein: die Bytegröße ist bereits zu viel.
Größenfrei auflisten (`ls -1`, `stat -c '%a %U:%G %n'`). Zulässig sind nur abgeleitete Angaben:
Modus, Eigentümer, Prüfsumme, Vorhandensein eines Musters als Ja/Nein.

**Warum:** Was in den Verlauf gerät, liegt dauerhaft in einer `.jsonl`-Datei; das Transkript zu
löschen ist keine Schadensbegrenzung (`KON-704`). Zwischen `A.6.3-R6` (führt Bytegröße als
zulässige abgeleitete Angabe) und der Sicherheitsvorgabe des Projekts besteht ein offener
Widerspruch — es gilt die engere Fassung.

**Wie anwenden:** Braucht eine Prüfung den Wert, läuft sie **im Container** beziehungsweise in
einem Wegwerfcontainer, und ausgegeben wird **nur die Antwort, nie der Aufruf**. Diese Regel ist
in dieser Kette schon dreimal verletzt worden (`VPS-7` 14.1, Orchestrierungsebene 6.35, und
`VPS-8` einmal bei einer Einbindungsprüfung) — sie bricht nicht am Vorsatz, sondern an beiläufigen
Auflistungsbefehlen.

Siehe [[vps-8-lauf-unterbrochen]].
