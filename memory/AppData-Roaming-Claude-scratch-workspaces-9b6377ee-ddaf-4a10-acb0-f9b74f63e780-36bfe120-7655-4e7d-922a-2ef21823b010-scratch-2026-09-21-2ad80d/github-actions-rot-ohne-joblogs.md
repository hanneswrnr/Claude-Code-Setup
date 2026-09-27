---
name: github-actions-rot-ohne-joblogs
description: "Roter GitHub-Workflow ohne Job-Logs heisst meist, dass der Job nie startete - Check-Annotationen lesen statt die Pruefung zu verdaechtigen"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dba0837b-8412-4ef4-88f6-6812801dae4e
  modified: 2026-09-21T16:26:05.809Z
---

Ist ein GitHub-Workflow rot und `gh run view --log-failed` meldet "log not found", erst die Check-Annotationen lesen: `gh api repos/<owner>/<repo>/actions/runs/<run>/jobs --jq '.jobs[0].id'`, dann `gh api repos/<owner>/<repo>/check-runs/<jobid>/annotations`. Zeigt der Job `steps: []` und eine Laufzeit von wenigen Sekunden, ist er gar nicht gestartet (Abrechnung, Runner-Kontingent, Berechtigungen) - die Pruefung selbst ist dann unschuldig.

**Why:** Am 21.09.2026 lautete die Aufgabe, geloeschte Mobile-Dateien erneut von `main` zu entfernen, weil der Waechter-Workflow rot war. Tatsaechlich war `main` sauber; seit dem 04.09.2026 startete jeder Job wegen eines Abrechnungsproblems des GitHub-Kontos nicht. Ohne die Annotationen haette ich einen leeren Bereinigungs-PR gebaut und die echte Ursache verfehlt.

**How to apply:** Bei rotem CI zuerst pruefen, ob der Job ueberhaupt lief, bevor der Inhalt der Pruefung verdaechtigt wird. Vorgetragene Fehlerursachen - auch von einer anderen Claude-Sitzung - gegen die API-Rohdaten pruefen, bevor Dateien geaendert werden. Siehe auch [[branch-mobile-dateien-kein-merge-risiko]].
