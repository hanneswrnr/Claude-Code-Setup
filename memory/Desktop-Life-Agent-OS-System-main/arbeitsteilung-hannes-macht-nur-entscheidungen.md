---
name: arbeitsteilung-hannes-macht-nur-entscheidungen
description: "Handarbeit gehört mir (CLI, SSH, MCP) — Hannes trifft nur Entscheidungen und tut, was technisch niemand sonst tun kann"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0de720ee-866b-43c0-b026-b6cb73f6d29a
  modified: 2026-08-06T22:13:15.780Z
---

Ich führe **so viel wie möglich selbst aus** — über Bash/CLI, SSH auf den VPS (Kurzname `ssh lifeos-cc`, Adresse nur in der lokalen SSH-Konfiguration; passwortloses `sudo`) und MCP. Hannes bekommt nur, was **wirklich nur er** tun kann.

**Why:** Er kennt sich nach eigener Aussage „null aus". Jeder Schritt, den ich ihm überlasse, obwohl ich ihn ausführen könnte, kostet Zeit und erzeugt Fehler, die niemandem nützen. Er hat das am 7. August 2026 ausdrücklich gerügt, nachdem ich ihn Verzeichnisse anlegen und Dateien mit `nano` schreiben ließ, obwohl ich SSH-Zugang habe.

**Der Denkfehler, der dahinter lag:** `R18` hatte das Hinterlegen des Telegram-Tokens als „Eigentümerhandlung, keine Bauhandlung" eingestuft, und ich habe das als „von Hand durch Hannes" gelesen. Es heißt nur **„nicht Sache eines Baulaufs"**. Diese Verwechslung nicht wiederholen.

**How to apply:**
- Vor jedem „mach bitte X": erst prüfen, ob ich X per SSH/CLI/MCP selbst kann. Wenn ja, mache ich es.
- Nur diese Klassen gehen an ihn: **Entscheidungen** (`OWN-*`, Freigaben, Verfassungsfragen wie `A.4.4-R2`), Handlungen **außerhalb** meiner Reichweite (Telegram-App, Anbieterpanel, Kontoeröffnung), und das **einmalige Einfügen eines Geheimnisses**.
- Geheimnisse bleiben trotzdem aus dem Chat (`KON-704`) — aber das ist **kein Grund, ihm Arbeit zu geben**. Stattdessen ein Mechanismus: Skript auf dem Wirt, das den Wert mit `read -rs` ohne Bildschirmausgabe entgegennimmt, alles Übrige selbst erledigt und nur Erfolg/Misserfolg meldet. So gebaut am 7. August für `OWN-107`, hat funktioniert.
- Wenn ich ihm doch etwas gebe: **eine** Aktion, wörtlich vorformuliert, mit dem fertigen Befehl zum Kopieren — nicht mehrere Schritte, die er zusammensetzen muss.
- Mehrdeutigkeiten vermeiden, die für mich keine sind: „schicke dem Bot eine Nachricht" hat er ins Terminal getippt statt in die Telegram-App. Immer sagen, **in welcher Anwendung** etwas passieren soll.

Gilt zusammen mit [[a-6-3-r5-alleinlauf-sperrt-den-projektbaum]]: Läuft ein Auftrag, darf ich trotzdem nichts im Projektbaum ändern — das begrenzt *wo* ich handle, nicht *ob*.
