---
name: reference-google-videobericht
description: "Google-Quellen zum Search-Console-Videobericht — dekorative Videos bleiben dort dauerhaft gemeldet, und ein noindex auf der Videodatei räumt den Eintrag nicht"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1796cbac-bc53-494a-94a8-f5a97f78845a
  modified: 2026-09-17T22:11:39.532Z
---

Der Bericht „Videoseiten" der Search Console zählt genau die Videos, die **nicht** indexiert sind. Ein Eintrag verschwindet deshalb nicht dadurch, dass man das Nicht-Indexieren bestätigt. Belegt und am 17./18.09.2026 selbst nachgelesen:

- https://developers.google.com/search/blog/2023/12/video-is-the-main-content — Google hat im Dezember 2023 bewusst umgestellt: „Videos that aren't the main content of the page will appear as 'No video indexed' in Search Console." Ein dekoratives Hintergrundvideo gehört damit per Produktentscheidung in diesen Bericht. Die Beispiele für nicht-primäre Videos stehen dort ausdrücklich.
- https://support.google.com/webmasters/answer/9495631 — Gründeliste, dazu: „Nur Videos auf einer Wiedergabeseite können indexiert werden", „Google indexiert nur ein Video pro Seite", und zur Frage, ob man überhaupt etwas tun muss: „Es liegt in Ihrem eigenen Ermessen, ob Sie sich um ein bestimmtes Problem kümmern oder nicht."
- https://support.google.com/webmasters/answer/7440203 — Überprüfung: „If you missed a fix, validation will stop when Google finds a single remaining instance of that issue." Ein absichtlich bestehendes Video lässt die Überprüfung also immer scheitern.
- https://developers.google.com/search/docs/appearance/video — die dokumentierten Wege, ein Video herauszunehmen, setzen alle an der **Seite** an: 404, `noindex` im Seitenkopf, Ablaufdatum. Zur Videodatei selbst steht dort nur die Warnung „Don't block the URL of the actual video bytes with the noindex rule or robots.txt file", und die richtet sich an alle, die Videofunktionen wollen.
- https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag — `X-Robots-Tag` ist der Weg für Nicht-HTML-Dateien; er wirkt nur, wenn die Datei crawlbar bleibt, eine robots.txt-Sperre macht ihn unlesbar.
- https://developers.google.com/search/docs/crawling-indexing/http-network-errors — Adressen mit 4xx fallen aus dem Index. Deshalb verschwinden alte Videoeinträge von selbst, sobald die alte Adresse 403 oder 404 liefert.

Praktische Folge für dekorative Hero-Videos: rot lassen, Überprüfung nicht erneut starten, im Projekt dokumentieren warum. Verwandt: [[project-hartung-livegang-stand]], [[feedback-muster-und-zahlen-nachmessen]].
