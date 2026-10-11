---
name: mig-860-standort-kennung-fest
description: "Mig 860 (Standort-Kennung fest + werkstaetten-Schreibrechte für anon/INSERT authenticated entzogen) LIVE seit 02.10.2026, Zweig fix/werkstatt-standorte-id-fest"
metadata:
  node_type: memory
  type: project
  originSessionId: 7013c43c-568a-4f83-940b-11d0711cc9e3
  modified: 2026-10-02T16:17:39.519Z
---

Mig 860 `860_werkstatt_standorte_id_fest.sql` LIVE seit 02.10.2026 („860-TEST OK“), Zweig `fix/werkstatt-standorte-id-fest`. Hannes hat am 02.10.2026 alles freigegeben (Einspielen und Merge).

- Trigger `zz_werkstatt_standorte_id_fest` (Muster Mig 733), md5 Körper 8449…2a6f; werkstaetten jetzt anon=r, authenticated=rwd (kein INSERT mehr, Registrierung nur per register_werkstatt_complete).
- Befund-Korrektur: `werkstaetten.id` war schon seit Mig 733 fest; `user_id` durch Regel + unique_werkstatt_user geschützt.
- `scripts/verify-770-…` angepasst: Anlegen als authenticated endet seit 860 am Tabellenrecht (`fehler=42501_recht` zählt als Erfolg).
- Live-Falle: anon darf werkstaetten nicht einmal lesen (Leseregel nutzt werkstatt_gruppen_admins ohne anon-Recht, Mig 772) — Rechte-Proben als anon nur ohne Spaltenbezug.
- Offen (Randnotiz Sicherheitsprüfung): authenticated braucht auch DELETE auf werkstaetten nicht. Nebenbefund Kalender-Anhänge → eigene Sitzung, Mig 861.

**Why:** Kennungen tragen Rechte ohne Fremdschlüssel; gleiches Muster wie Mig 733 und 859 (versicherungen).
**How to apply:** Neue Code-Wege, die als Browser Werkstätten anlegen wollen, scheitern mit 42501 — über Server/RPC gehen. Neue Tabellen mit UPDATE für authenticated: id-Schutz prüfen.
