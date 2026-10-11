---
name: rechtsdokument-pdf-schrift-pr-296
description: "Rechtsdokument-PDF Fließtext fett behoben (PR #296 gemergt 02.10.2026); doppelter BEISPIEL-Hinweis entfernt (PR #297 gemergt 02.10.2026)"
metadata:
  node_type: memory
  type: project
  originSessionId: c9d51413-a6cb-45e0-be2d-58eb0a344762
  modified: 2026-10-02T21:41:56.250Z
---

PR #296 GEMERGT am 02.10.2026 (1ad3b0359): `lib/pdf/rechtsdokument-pdf.ts` setzt Schrift und Größe selbst vor jedem Abschnitt (Hinweis fett 8,5 pt, Fließtext normal 10 pt). Keine Migration.

PR #297 (Zweig fix/rechtsdokument-beispiel-hinweis-einmal, 02.10.2026): Hannes hat die Entscheidung übertragen; Textzeile „BEISPIEL — rechtlich nicht geprüft …“ aus den sechs Vorlagen in `lib/rechtsdokumente/beispiel-vorlagen.ts` gestrichen, Kasten (Spalte `hinweis`) bleibt; im Reiter steht der Kasten nach dem Erzeugen oben in der Vorschau-Karte. GEMERGT am 02.10.2026 (a4f0376c1). Live: 1 alter Entwurf behält die Zeile.

**Why:** Seit Mig 845 ist der Kasten serverseitig fest; die Textzeile war redundant und wirkte unsauber.
**How to apply:** Nie wieder den Hinweis in Vorlagentexte schreiben; der Test `lib/rechtsdokumente/__tests__/beispiel-vorlagen.test.ts` verbietet es. Nebenbefund (Entwürfe weder öffnen noch löschen) behoben in PR #298, siehe [[rechtsdokument-entwurf-oeffnen-loeschen-pr-298]]. Verwandt: [[mig-844-845-unterschriebenes-endgueltig]].
