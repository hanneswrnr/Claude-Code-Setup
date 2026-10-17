---
name: bibliothek-immer-mitpflegen
description: SM24 — bei JEDER Änderung die öffentliche Bibliothek (und Hilfe in der App) prüfen und anpassen; Anweisung Hannes 17.10.2026
metadata:
  node_type: memory
  type: feedback
  originSessionId: 222c8329-acf8-408b-97df-b43cb80ef44a
  modified: 2026-10-17T14:44:19.736Z
---

Bei JEDER Änderung an SchadenMelden24 (Funktion, Oberfläche, Texte, Abläufe, Farben, Namen von Seiten oder Knöpfen) prüfen, ob die öffentliche Bibliothek (`/bibliothek`) und die Hilfe in der App betroffen sind, und sie im selben Zweig mit anpassen. Neue Funktion → neuer Artikel. Keine Ausnahme, auch nicht bei „kleinen“ Änderungen oder in Sitzungen, die nichts mit der Bibliothek zu tun haben.

**Why:** Hannes hat am 17.10.2026 ausdrücklich verlangt: „die Bibliothek muss IMMER mit angepasst werden falls nötig! Bei JEDER Änderung!“ Die Bibliothek soll mit jeder Änderung mitwachsen (Vorbild code.claude.com/docs) und nie veraltet sein.

**How to apply:**
- Artikel liegen (ab dem Bau durch Chat 7, Zweige `feat/v4-hilfe`/`feat/v4-bibliothek` im Sammelzweig `sammel/verbesserungen`) in `content/bibliothek/<thema>.ts`; Feld `quellen` nennt die beschriebenen Programmteile, `geprueftAm` nach der Prüfung erneuern. Konzept: `.planning/features/neuigkeiten-hilfe-bibliothek/KONZEPT.md` §4.3 und Abschnitt „Pflege“.
- Gibt es `content/bibliothek/` im Zweig noch nicht: die Änderung in `feature-vault/` pflegen (Vorlage der Artikel) und im Abschlussbericht „Bibliothek: betroffen ja/nein, was“ nennen.
- Steht auch in der Projekt-CLAUDE.md unter „Nach der Arbeit aktualisieren“. Verwandt: [[version-4-0-sammelzweig]], [[design-html-css-skizzen-1zu1]].
