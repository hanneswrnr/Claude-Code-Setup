---
name: vps-8-lauf-unterbrochen
description: "Stand des VPS-8-Baulaufs (lifeos-egress, lifeos-backup Stufe 1, AT-OBS-066) beim Schnitt am 6. August 2026, und was zur Wiederaufnahme fehlt"
metadata: 
  node_type: memory
  type: project
  originSessionId: 561d24da-981b-4394-b903-1b86f46afb8a
  modified: 2026-08-07T19:38:12.798Z
---

Der Baulauf `VPS-8` wurde am 6. August 2026 gegen 22:45 UTC auf Wunsch des Eigentümers
unterbrochen und wird fortgesetzt. **Der vollständige offene Stand steht in `TODO.md` im
Projektwurzelverzeichnis** — dort zuerst nachsehen. Die Quellen der beiden gebauten Container
liegen in `vps8-artefakte/`. Beides ist am 7. August nach `hanneswrnr/Life-Agent-OS-System`
(privat) gepusht; der Projektordner ist seitdem ein echter Klon von `main`.

**Gebaut und belegt:** `lifeos-egress` (TZ-EGRESS, 3 Netze, 0 Volumes, Fähigkeitsmenge gemessen
leer, Positivliste als Umgebungswert, Bindung nur auf net-egress) und `lifeos-backup` Stufe 1
(4 lesende Einbindungen, `*.key`-Gegenprobe 0 Treffer, kein Geheimnis in einer
Umgebungsvariablen). `AT-OBS-066` für **CRITICAL** bestanden (Alarm bei der ersten Auswertung,
Telegram `ok=True`). Positivliste vollständig geprüft, einschließlich Regel 3 und Regel 4.

**Offen, in dieser Reihenfolge:** `AT-OBS-066` für **MEDIUM** (dreifache Entprellung, ~45 min
Wanduhr — das ist das Abnahmekriterium des Laufs); Bestätigung des Eigentümers, was wann in
Telegram ankam; Ablösung von `lifeos-cert-exporter` (zurzeit **zwei** Erzeuger derselben Metrik);
`AT-OBS-072`; Rest von Aufgabe 6; Bericht nach `spec-parts/VPS-EINRICHTUNG-8.md`.

**Blockade:** Die Rückabfrage aus dem Beobachtungs-Backend wird vom Berechtigungsfilter der
Werkzeugumgebung abgewiesen, weil sie das Wurzelmerkmal aus
`/var/lib/lifeos/secrets/observability/root.env` liest. Sie trägt zwei Berichtspunkte und die
Löschung der Prüfzeitreihe. Braucht eine Bash-Freigabe für `/tmp/vps8-build/obs-abfrage.sh`.
Nicht umgehen — eine base64-Verpackung wäre möglich, sieht aber wie Verschleierung aus.

Siehe [[lifeos-geheimnisse-nie-im-verlauf]].
