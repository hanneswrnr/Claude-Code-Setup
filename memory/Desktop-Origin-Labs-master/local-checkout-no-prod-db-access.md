---
name: local-checkout-no-prod-db-access
description: "Diese lokale Arbeitskopie kann keine Migrationen gegen die Prod-DB fahren — kein Supabase-CLI, kein Link, keine Credentials"
metadata: 
  node_type: memory
  type: project
  originSessionId: 43adee3e-1d74-47a6-84f8-78ad1a2fcdec
---

Die lokale Arbeitskopie unter `c:\Users\hanne\Desktop\Origin-Labs-master` ist ein **reiner Code-Checkout ohne jeden Zugang zur Produktiv-Supabase-DB**: Supabase-CLI ist nicht installiert (nicht im PATH, nicht global, nicht in `node_modules/.bin`; `npx supabase` müsste das Paket erst herunterladen), es gibt kein `supabase/config.toml` und keinen `supabase/.temp/project-ref` (nicht gelinkt), und es existiert **keine `.env`-Datei** (`.env.local`/`.env`/`.env.production` fehlen alle) → kein Service-Role-Key, kein `DATABASE_URL`, kein DB-Passwort.

**Konsequenz:** Die zahlreichen "Operator-TODO: Migration NNN in Prod-DB applien + `migration repair`"-Punkte aus CLAUDE.md sind von dieser Session aus **nicht ausführbar**. Sie werden vom Operator (Hannes) über das Supabase-Dashboard (SQL-Editor) oder eine separat eingerichtete CLI-Umgebung angewendet, nicht aus diesem Checkout.

**Wie man Migrations-Aufgaben hier trotzdem nützlich bearbeitet:** Read-only verifizieren, welche Migrationen laut Doku/Dateistand ausstehen, die SQL auf Idempotenz + Destruktivität + Code-Abhängigkeiten prüfen (alle Projekt-Migrationen sind per `info_schema`-Guard / `IF NOT EXISTS` / `CREATE OR REPLACE` idempotent + rein additiv gebaut) und dem Operator einen geprüften Apply-Plan (Reihenfolge + SQL-Editor- bzw. `db push`-Pfad + Verifikations-Queries) liefern. Nicht versuchen, CLI zu installieren + sich Prod-Credentials geben zu lassen, ohne dass der User das explizit anstößt.

Stand 2026-06-15: 111–114 waren laut Doku ausstehend und wurden an diesem Tag vom Operator über den Supabase-SQL-Editor in Prod appliedt (alle 5 Schema-Checks `found=1` verifiziert). Offener Rest-Punkt: der `schema_migrations`-Tracker kennt 111–114 evtl. noch nicht (SQL-Editor schreibt ihn nicht) → bei künftigem `supabase db push` aus einer gelinkten Umgebung `migration repair --status applied 111..114` nachziehen; unkritisch, weil alle vier idempotent sind und ein Re-Push ein No-Op wäre. Siehe [[payments-bank-transfer-only]] für weiteren Prod-Betriebs-Kontext.
