---
name: geraet-merken-pr-301
description: "Neue-Gerät-Mail kam bei jeder Anmeldung (Cookie geht verloren); PR #301 erkennt Gerät auch über gleiches /24-Netz + Browser-Art (30 Tage, nur Vercel/IPv4) und schickt Admin-Login-Mail an info@ nur noch bei neuem Gerät; Merge freigegeben 03.10.2026"
metadata:
  node_type: memory
  type: project
  originSessionId: acd0f306-beda-4676-b672-521f5834eca0
  modified: 2026-10-02T23:42:21.432Z
---

03.10.2026: Hannes bekam die Mail „Anmeldung auf einem neuen Gerät“ bei fast jeder Anmeldung. Ursache (Live-Daten): Der Browser verliert das Cookie `sm24_geraet` (dreimal in 30 h neue Kennung am selben Rechner); Abmelden ist NICHT schuld, Vorschau-Adressen auch nicht (Supabase-Edge-Logs: alle Logins von www).

PR #301, Zweig `fix/geraet-merken-netz-browser` (Commits bc1ac8ba3 + 0ba96c914):
- `app/api/auth/security-event/route.ts` `gleichesNetzUndBrowser`: gleiches /24 + gleiche `browserArt()` (UA ohne Zahlen) einer Anmeldung desselben Kontos in 30 Tagen → bekannt, `metadata.erkannt='netz_browser'`. Nur VERCEL_ENV production/preview, nicht IPv6.
- `app/api/admin/auth/login-notification/route.ts`: info@-Mail nur, wenn `anmeldeEinstufungDerSitzung()` nicht 'bekannt' liefert (session_id bleibt bei aal1→aal2 gleich, Beleg Supabase `updateMFASessionAndClaims`); audit_log bekommt jede Admin-Anmeldung.
- devos-security: zweimal „annehmen“ nach Nachbesserungen. Merge von Hannes freigegeben (03.10.2026, nach eigener Prüfung durch Claude).

**Why:** Warn-Mail bei jeder Anmeldung wird ignoriert; Restrisiko (gleiches Netz/Sammeladressen) bewusst akzeptiert, dokumentiert in wiki/06-Reference/API-Routes/auth.md und admin.md.

**How to apply:** Der eingebaute Claude-Browser hat eine eigene Browser-Art (UA enthält „Claude/…“), seine erste Anmeldung löst die Mail zu Recht aus. Wirksamkeit live prüfen: `auth_security_events.metadata->>'erkannt' = 'netz_browser'`; viele audit_log-Einträge `admin_login_notifications` mit `geraet: 'nicht_zugeordnet'` hießen, dass die Sitzungs-Zuordnung nicht greift. Option (nicht umgesetzt): info@-Mail nur bei Cookie-Erkennung unterdrücken, nicht beim Netzweg.
