---
name: safety-net-blockiert-zerstoererisches
description: Das Sicherheitsnetz der Desktop-App blockiert Ref-Loeschungen und Sammel-Schreibvorgaenge unabhaengig von Hannes Zustimmung im Chat
metadata:
  type: feedback
---

Der Auto-Modus dieser App prueft die Aktion, nicht die Zustimmung. Geblockt wurden am 21.09.2026: das Loeschen von Git-Tags ("Git Destructive"), Sammel-Pushes auf viele Branches ("Modify Shared Resources") und das Abbrechen mehrerer Vercel-Builds ("Interfere With Workloads"). Einzelne gleichartige Aufrufe gingen teils durch.

**Why:** Ein Zerlegen in Einzelaufrufe waere ein Umgehen der Sperre, kein Loesungsweg. Wiederholte Versuche kosten nur Zeit.

**How to apply:** Nach hoechstens zwei Versuchen aufhoeren, den Rest der Aufgabe fertig machen und Hannes einen fertigen Befehl fuer sein PowerShell geben - das hat bei den Tags sofort funktioniert (git push origin --delete mit allen Namen in einer Zeile). Alternativ ihn bitten, den Berechtigungs-Modus umzustellen. Vorher immer einen Ruecksetzpunkt sichern und pruefen, ob die betroffenen Commits ohnehin in main haengen; dann geht beim Loeschen nur die Beschriftung verloren.
