---
name: mig-910-914-gast-rechte-folgeliste
description: "Mig 910–914 (Folgeliste von 909, anon/PUBLIC ohne Rechte, Regeln TO authenticated) LIVE und gemergt 17.10.2026; Rückwege 744/748/777/866 erst nach 91x"
metadata:
  node_type: memory
  type: project
  originSessionId: 957a086a-61db-432c-8c1a-9bd3b5a30204
  modified: 2026-10-17T14:34:14.269Z
---

Mig 910 (Kunden/Rechnungen), 911 (KI), 912 (Versicherung), 913 (Benachrichtigungen), 914 (Server-Tabellen, feedback,
stripe_webhook_events, gcal) sind seit 17.10.2026 live und gemergt: #421, #417, #418, #419, #420.
Ausgenommen bleiben bewusst consent_records, reserved_slugs, werkstaetten, werkstatt_standorte.

**Why:** Folgeliste aus [[mig-909-eigene-tabellen-ohne-gast]]; Gäste hatten Tabellenrechte, nur RLS-Ausdrücke hielten sie draußen.

**How to apply:** Ältere Rückwege 744, 748, 777 und 866 im Notfall erst nach dem passenden Rückweg 91x laufen lassen
(Reihenfolge steht je als „(Mig 91x)“-Absatz im Kopf). Offen: pen-test-hq.test.ts mit Testzugängen; Nebenbefunde
(wirkungslose auth.role()='service_role'-Regeln, refresh_token_encrypted lesbar, unnötige I/U/D für authenticated)
laufen als eigene Folgeaufgabe.
