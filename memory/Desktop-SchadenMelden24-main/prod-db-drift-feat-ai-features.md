---
name: prod-db-drift-feat-ai-features
description: "Prod-Supabase (ownxhgvhciwknzonmsbs) enthält Migrationen 591-598 aus dem Branch feat/ai-features, die in main fehlen; Funktions-Bodies vor CREATE OR REPLACE immer live per pg_get_functiondef abgleichen"
metadata: 
  node_type: memory
  type: project
  originSessionId: a725a692-8488-40bd-9da6-7a626b54668f
  modified: 2026-09-13T20:21:49.380Z
---

Stand 2026-09-13: Die Produktions-Datenbank (Supabase-Projekt `ownxhgvhciwknzonmsbs`, MCP-Server-ID 24849822…) hat Migration 598 (`benachrichtigungs_schalter_greifen`, Branch `feat/ai-features`, lokal auch unter `Desktop/SchadenMelden24-feat-ai-features`) bereits angewendet, obwohl `main` bei 590 endet. `supabase_migrations.schema_migrations` listet nur bis 564 — Migrationen werden per SQL-Editor/MCP eingespielt, die Tabelle ist keine verlässliche Quelle.

**Why:** Ein `CREATE OR REPLACE FUNCTION queue_notification` auf Basis der höchsten main-Migration (562) hätte die drei 598-Zweige (`kunde_message_portal`, `kunde_attachment_portal`, `fahrzeug_abholbereit`) still gelöscht. Nummern 591–598 sind in `feat/ai-features` belegt; eigene Migrationen wurden deshalb 599/600 nummeriert.

**How to apply:** Vor jeder Funktions-Neudefinition `SELECT pg_get_functiondef(...)` live ausführen und den Body als Basis nehmen; neue Migrationsnummern gegen alle Remote-Branches prüfen (`git ls-tree origin/<branch> supabase/migrations/`). Siehe [[schadenmelden24-commit-regeln]].
