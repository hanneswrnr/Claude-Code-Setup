---
name: feedback-muster-und-zahlen-nachmessen
description: "Vor dem Setzen einer Wildcard-Regel alle wirklich getroffenen Dateien auflisten, und keine Mengenangabe schreiben, die nicht gemessen wurde"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1796cbac-bc53-494a-94a8-f5a97f78845a
  modified: 2026-09-17T22:11:24.530Z
---

Bevor eine Regel mit Platzhalter live geht (Header, Redirect, robots.txt, Glob in einer Konfiguration), erst auflisten, welche echten Dateien sie trifft, und jede einzeln ansehen. Und keine Mengenangabe (Dauer, Größe, Anzahl, Gewicht) in Text, Kommentar oder Commit schreiben, die nicht vorher gemessen wurde.

**Why:** Am 14.09.2026 habe ich im Projekt Raumgestaltung-Hartung `X-Robots-Tag: noindex` für `/assets/(.*).mp4` gesetzt, in der Annahme, das betreffe nur die dekorative Hero-Schleife. Ausgeliefert werden aber vier `.mp4`-Dateien: Die Regel hat auch Normans zwei echte Filme (Gesamtfilm 70,2 s, Badrundgang 48,0 s) aus der Google-Videosuche genommen. Das war keine Entscheidung des Auftraggebers und fiel erst vier Tage später bei einer Gegenprüfung auf. Im selben Zug hatte ich die Länge der Schleife dreimal als „sechs Sekunden" beschrieben; gemessen sind es 47,2 Sekunden. Beides war vermeidbar mit je einem Befehl.

**How to apply:** Muster auflisten statt annehmen: `ls dist/assets/*.mp4`, dann je Treffer `curl -sI <url>`. Mediendaten messen: `ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 <datei>` für die Länge, `-select_streams a -show_entries stream=codec_name` für die Tonspur. Trifft die Regel etwas, das dem Auftraggeber gehört und eine Entscheidung wäre, vorher fragen statt nachträglich dokumentieren. Verwandt: [[feedback-rote-pruefung-nicht-wegerklaeren]], [[project-hartung-livegang-stand]], [[reference-google-videobericht]].
