# Data integrity and migration

Read schema, migrations, queries, access policies and transaction boundaries before changing a model. Encode invariants with appropriate foreign keys, unique/check constraints, types and null semantics. Choose indexes from actual query patterns and measured plans; investigate N+1 and unbounded result sets before adding caches.

For migrations identify existing data compatibility, locking/runtime cost, rollback or forward recovery, and mixed application versions. Prefer expand/backfill/contract where necessary. Test on synthetic or explicitly authorized non-production data with the project's migration tool. Include uniqueness/race/concurrency and transaction rollback cases. Never treat a destructive migration as a normal local code edit.

For Supabase/PostgreSQL, use installed specialist documentation when available. Preserve RLS and test policies for anonymous, authenticated owner, other tenant and elevated role. Service-role credentials stay server-side and do not bypass authorization in user-facing endpoints. Consider storage policies, views/functions and realtime access as well as tables. Never disable RLS to make a test pass. Read current PostgreSQL and Supabase primary documentation for version-sensitive syntax and policy behavior.

Record migration order, operational prerequisites and what recovery was actually tested. Backups existing is not the same as a demonstrated restore.
