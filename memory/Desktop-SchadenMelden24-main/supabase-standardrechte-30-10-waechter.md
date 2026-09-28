---
name: supabase-standardrechte-30-10-waechter
description: "Supabase nimmt neuen public-Relationen ab 30.10.2026 SELECT/INSERT/UPDATE/DELETE (auch service_role); Wächter ab Mig 783 in PR #218, gemergt am 28.09.2026 (e400210f)"
metadata:
  node_type: memory
  type: project
  originSessionId: 6d28d09c-a60d-463a-ac07-ecc587d631df
  modified: 2026-09-28T19:00:19.195Z
---

Supabase stellt am 30.10.2026 auch bestehende Projekte um: `ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public REVOKE SELECT, INSERT, UPDATE, DELETE ON TABLES` und `USAGE, SELECT ON SEQUENCES` von anon, authenticated und service_role. Live am 28.09.2026 noch nicht passiert (Prüfabfrage im Wiki liefert 18, nach der Umstellung 0).

Wächter `Web_Schadenmelden24/lib/__tests__/migration-rechte-neue-relationen.test.ts` (ab Mig 783, auch Rückwege) auf Zweig `fix/rechte-neue-relationen`, PR #218 am 28.09.2026 gemergt (e400210f), volle Testsammlung auf dem Merge-Stand grün. Kontroll-Todo `.planning/todos/pending/supabase-standardrechte-nach-30-10.md` fällig 31.10.2026.

**Why:** Ohne GRANT kommen Server-Code und Browser an neue Tabellen nicht mehr heran (42501 vor RLS). Am 28.09. legte keine offene Migration eine Relation an; 785 (Lager-Dokumente, Zweig fix/lager-dateien-anhaengen) wird es voraussichtlich tun.

**How to apply:** Bei jeder neuen Migration mit CREATE TABLE/VIEW/SEQUENCE: GRANT an service_role nach dem CREATE, passende GRANT für Policy-Rollen, nie GRANT ALL oder ON ALL TABLES. Regel und Vorlage: `wiki/05-Anti-Patterns/Supabase-Function-Grants.md`. Verwandt: [[mig-777-tabellenrechte]], [[schadenmelden24-commit-regeln]].
