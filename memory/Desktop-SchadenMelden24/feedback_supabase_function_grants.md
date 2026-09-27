---
name: feedback-supabase-function-grants
description: "SECURITY DEFINER Functions in public müssen REVOKE EXECUTE … FROM anon explizit setzen — REVOKE FROM PUBLIC reicht nicht, weil Supabase via ALTER DEFAULT PRIVILEGES jedes neue Function-Create automatisch anon/authenticated/service_role grantet"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9f024ee0-9f95-4b48-a8bd-fbba66c68cf9
---

SECURITY DEFINER Functions in `public` brauchen IMMER **beide** Revoke-Schichten: `REVOKE EXECUTE ... FROM PUBLIC, anon`. Eine Schicht allein reicht nie — anon hat sowohl direkten Default-Grant als auch PUBLIC-Vererbung. Verify nach Deploy via `has_function_privilege('anon', oid, 'execute')` (returns false = sauber).

**Why — der Doppel-Fail (beide am 2026-05-22 beobachtet):**
- **Mig 325** hatte nur `REVOKE FROM PUBLIC`. Verify zeigte anon=EXECUTE, weil Supabase per `ALTER DEFAULT PRIVILEGES` für `public` jedem neuen Function-Create einen expliziten anon-Grant verpasst — REVOKE FROM PUBLIC entfernt nur die Vererbung, nicht den expliziten Grant. `proacl = {postgres=X/postgres,anon=X/postgres,authenticated=X/postgres,service_role=X/postgres}`.
- **Mig 326 erster Anlauf** hatte nur `REVOKE FROM anon` für 6 cleanup_*/anonymize_*-Functions. Validation FAIL, weil PUBLIC bei denen noch EXECUTE hatte → anon erbte weiter via PUBLIC. Bei den 2 notify_*-Functions, wo Mig 315 PUBLIC bereits revoked hatte, ging es durch. Erst `REVOKE FROM PUBLIC, anon` schloss beide Wege.

**How to apply:**
- Neue SECDEF-Function-Mig immer mit:
  ```sql
  REVOKE EXECUTE ON FUNCTION public.my_func(...) FROM PUBLIC, anon;
  GRANT  EXECUTE ON FUNCTION public.my_func(...) TO authenticated, service_role;
  ```
  `FROM PUBLIC, anon` in einer Zeile = beide Schichten in einem Statement.
- Verify-Query nach Deploy: `SELECT has_function_privilege('anon', oid, 'execute') FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public' AND p.proname='X';` — Erwartung false.
- `information_schema.routine_privileges` allein reicht NICHT zum Verify — PUBLIC zeigt es nicht; via `has_function_privilege('anon', ...)` testen.
- Wiki-Doku mit Sweep-Query für Bestand: `wiki/05-Anti-Patterns/Supabase-Function-Grants.md`.
- Triggers (`AFTER INSERT/UPDATE EXECUTE FUNCTION foo()`) brauchen keinen EXECUTE-Grant — sie laufen im Trigger-Kontext. Cron via `serviceClient.rpc(...)` nutzt service_role-Grant. Beide nicht von anon-Revoke betroffen.
- Bei Hinweis auf "Supabase RPC", "SECURITY DEFINER", "anon-Grant", "PostgREST-Privileg" → diese Regel checken.

Verwandt: [[project-security-anon-rls]] (Anon-RLS-Verbot auf Portal-Tabellen — analoger Schutz auf Tabellen-Ebene).
