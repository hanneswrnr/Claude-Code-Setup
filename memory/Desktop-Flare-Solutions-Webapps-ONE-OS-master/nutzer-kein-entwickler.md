---
name: nutzer-kein-entwickler
description: "Hannes ist kein Softwareentwickler: Claude erledigt alles technisch Mögliche selbst und gibt ihm nur unvermeidbare, kleinstmögliche Aufgaben mit Beispielwerten (Anweisung 12.09.2026)"
metadata:
  type: user
---

Hannes ist Product Owner und kein Softwareentwickler. Er will so wenig Aufgaben wie möglich bekommen: Claude macht alles selbst, was per Befehl, Skript, SSH (`lifeos-cc`), Konnektor oder PR geht, und gibt nur ab, was technisch nicht anders geht (Passwörter/Schlüssel, Browser-OAuth, Dashboard-Klicks ohne Konnektor, Käufe, echte Entscheidungen).

**Why:** Ausdrückliche Anweisung am 12.09.2026 nach dem Supabase-Umzug; beim Umzug gingen Aufgaben an ihn schief, weil Platzhalter wörtlich übernommen und Befehle im falschen Fenster ausgeführt wurden.

**How to apply:** Vor jeder Aufgabe an ihn den eigenen Weg suchen. Anleitungen: ein Befehl pro Block, Fenster benennen, Beispielwerte statt `<Platzhalter>`, erwartete Ausgabe nennen, Fehleingaben prüfen und nur den nächsten Schritt geben. Steht auch global in `~/.claude/CLAUDE.md` („Arbeitsteilung mit dem Nutzer"). Siehe [[one-os-orchestrator-arbeitsweise]].
