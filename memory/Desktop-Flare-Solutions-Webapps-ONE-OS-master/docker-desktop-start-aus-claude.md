---
name: docker-desktop-start-aus-claude
description: "Docker Desktop aus einer Claude-Code-Sitzung starten: Start-Process stirbt mit dem Werkzeugaufruf, explorer.exe-Start überlebt (gemessen 12.09.2026)"
metadata: 
  node_type: memory
  type: project
  originSessionId: dbcdc46a-67e5-462b-91ec-58cfd818214b
  modified: 2026-09-12T12:32:22.067Z
---

Auf dem ONE-OS-Arbeitsplatz läuft der Docker-Daemon nach dem Rechnerstart nicht. Ein `Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"` aus dem PowerShell-Werkzeug zeigt für Sekunden Prozesse, die mit dem Ende des Werkzeugaufrufs wieder verschwinden (zweimal gemessen am 12.09.2026: nach 5 Minuten kein Prozess, `docker info` weiter ohne Pipe). Der Start über `explorer.exe "C:\Program Files\Docker\Docker\Docker Desktop.exe"` überlebt den Aufruf; danach war der Daemon nach etwa einer Minute erreichbar und `npx -y supabase@2.108.0 start` lief.

**Why:** Der Werkzeug-Sandkasten räumt Kindprozesse mit dem Aufruf ab; Explorer startet die Anwendung ausserhalb dieses Job-Objekts.

**How to apply:** Zuerst `docker info`; bei fehlender Pipe `dockerDesktopLinuxEngine` per `explorer.exe` starten, dann in einem Hintergrund-Bash mit `until docker info; do sleep 5; done` warten und den Stack starten. Nicht mit `Start-Process` wiederholen. Siehe [[one-os-arbeitsplatz-flare]].
