---
name: mig-863-verbund-export-zweite-stufe
description: "Mig 863 Datenauskunft der Verbund-Zentrale nur mit aal2 — LIVE seit 03.10.2026 (863/862/828-TEST OK), PR #307 gemergt (c146932db); Folge-Todos verbund-lesen-zweite-stufe (Leseregeln ohne aal2), admin-selbstexport-direkt"
metadata:
  node_type: memory
  type: project
  originSessionId: 82f27eff-1f3c-4c59-9d8c-cf22b24a117d
  modified: 2026-10-03T11:18:32.822Z
---

Mig 863 (`supabase/migrations/863_verbund_export_zweite_stufe.sql`) fügt in `export_user_data` genau einen Block ein: angemeldetes Konto, Rolle `werkstatt_gruppe`, `auth.jwt()->>'aal'` nicht genau `aal2` → 42501 „Zweiter Faktor erforderlich“; service_role frei. Gebaut am 03.10.2026 auf Zweig `fix/verbund-export-aal2` (Worktree `C:/Users/hanne/sm24-verbund-export-aal2`), Prüfsummen neu: Definition 66f465e2…, Länge 46313. Container 863 79/0, Vorprüfung live READ ONLY bestanden. Routen geben 403 „Bitte zuerst die zweite Anmelde-Stufe bestätigen.“ (`lib/dsgvo/export-zweite-stufe.ts`).

**Why:** Befund N4 (02.10.2026): Export enthielt alle Tickets des Verbunds, aber ohne zweiten Faktor; bei [[einstellungen-umbau-pr-299]]/Mig 862 abgetrennt.

**How to apply:** Erledigt (live und gemergt 03.10.2026). verify-828 und verify-862 kennen 863 als Nachfolger; jede neue Fassung von export_user_data braucht einen weiteren Listeneintrag dort und muss die aal2-Prüfung behalten (Wächter migration-863). CLAUDE.md-Migrationszeile erst beim Einspielen auf 863 umstellen.
