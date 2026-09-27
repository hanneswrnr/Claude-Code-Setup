---
name: schadenmelden24-actions-abrechnung-blockiert
description: GitHub Actions startet bei Hannes keine Jobs mehr, weil das kostenlose Monatskontingent aufgebraucht ist - Hauptverbraucher ist ONE-OS, nicht SchadenMelden24
metadata:
  type: project
---

Seit dem 04.09.2026 startet in hanneswrnr/SchadenMelden24 kein GitHub-Actions-Job mehr. Jeder Lauf endet nach Sekunden mit 0 Schritten und der Annotation, dass Zahlungen fehlgeschlagen seien oder das Ausgabenlimit erhoeht werden muesse.

Die Abrechnungsseite vom 21.09.2026 zeigt: keine kostenpflichtigen Abos (GitHub Free und Copilot Free, je 0 Dollar), nichts faellig. Der gemessene Verbrauch von 16,34 Dollar wird vollstaendig vom enthaltenen Gratiskontingent gedeckt - das heisst, es ist aufgebraucht. Verteilung: ONE-OS 16,14, BI-Braunsbedra 0,17, SchadenMelden24 0,02. Der eigentliche Verbraucher ist also ONE-OS.

Es gibt somit kein Zahlungsproblem zu loesen. Das Kontingent setzt sich zum naechsten Abrechnungsmonat zurueck; danach laufen die Workflows wieder, bis es erneut aufgebraucht ist.

Folge: Fuer jeden seit dem 04.09.2026 gemergten PR hat nie eine Workflow-Pruefung stattgefunden. Gruene Haken an diesen PRs stammen von Vercel.

**Why:** Ohne diese Zahlen wirkt die Meldung wie eine fehlgeschlagene Zahlung, und man raet faelschlicherweise zu einer kostenpflichtigen Loesung, die Hannes ablehnt.

**How to apply:** Rote Actions-Laeufe in diesem Zeitraum nicht inhaltlich deuten und Aenderungen nicht mit "CI gruen" begruenden. Als kostenlosen Ersatz die lokalen Hooks nutzen; Hannes hat core.hooksPath am 21.09.2026 auf .githooks gesetzt. Wer das Kontingent entlasten will, muss bei ONE-OS ansetzen. Siehe auch [[github-nicht-bezahlen]] und [[github-actions-rot-ohne-joblogs]].
