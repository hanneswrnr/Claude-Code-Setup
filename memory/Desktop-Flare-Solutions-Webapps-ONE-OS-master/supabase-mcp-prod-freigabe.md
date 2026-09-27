---
name: supabase-mcp-prod-freigabe
description: "Projektübergreifende Freigabe (13.09.2026): Produktionsdatenbanken über eingerichtete Supabase-MCP-Konnektoren selbst ändern (Migrationen, SQL), ohne den Nutzer zu fragen"
metadata:
  type: feedback
---

Der Nutzer hat am 13.09.2026 nach Runde 22 in ONE OS ausdrücklich gesagt: Er hat die Supabase-MCP-Konnektoren eingerichtet, damit Claude ab sofort **in allen Projekten mit eingerichtetem Supabase-MCP** Migrationen einspielen und Änderungen an der Produktionsdatenbank vornehmen kann, ohne ihn zu fragen.

**Why:** In Runde 22 musste der Nutzer `supabase db push` selbst ausführen (CLI-Push ist für Claude gesperrt); das war ihm zu viel Handarbeit. Der Konnektor (`apply_migration`, `execute_sql`) ist der vorgesehene Weg.

**How to apply:** Produktionsmigration über den Konnektor des jeweiligen Projekts fahren, nicht an den Nutzer geben. Trotzdem gilt: erst Migration, dann Merge/Deploy; nach jeder Migration messen (`list_migrations`, Spalten, Policies); `apply_migration` bucht eine eigene Version — danach in `schema_migrations` auf die Repo-Version umbenennen, sonst sieht `db push` die Repo-Datei als fehlend; vor `create or replace function` den Live-Body prüfen. Destruktive Änderungen (Tabellen/Daten löschen) sind davon nicht gedeckt — die bleiben Rückfrage. Siehe [[one-os-merge-freigabe]].
