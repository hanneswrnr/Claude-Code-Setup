---
name: mig-882-mfa-ersatzcodes
description: "Ersatz-Codes für die zweite Anmelde-Stufe (Verbund, später Admin) – Mig 882 live, PR #335 gemergt 09.10.2026"
metadata:
  node_type: memory
  type: project
  originSessionId: 08a75455-f680-49af-a601-2bd875c47059
  modified: 2026-10-09T21:45:18.442Z
---

Mig 882 (Ersatz-Codes, HMAC-Hashes, 5 SECDEF-Funktionen nur service_role) LIVE seit 09.10.2026, verify „882-TEST OK“. App-Teil PR #335 gemergt 09.10.2026 (2214daab9); Hannes hat Erzeugen und Einlösen in der Vorschau erfolgreich getestet. Seit 882 meldet scripts/verify-873 FAIL bei der md5 von export_user_data (erwartet).

Tempo der Verbund-Zentrale PR #336 gemergt und live 09.10.2026 (a5dbd13ff).

**Why:** Ohne Ersatz-Codes sperrte ein verlorenes Handy die Zentrale aus.
**How to apply:** Admin-Zweig feat/admin-modern nutzt eine Kopie des Clients – beim Hereinholen von main gilt die main-Fassung von lib/auth/ersatzcodes/client.ts. „Mein Konto“ hat noch keine Ersatz-Code-Oberfläche. Siehe [[profilbereich-profilbild-mig-881]].
