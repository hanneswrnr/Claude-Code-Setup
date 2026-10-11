---
name: mig-884-889-offene-todos-10-10
description: "Mig 884–889 live seit 10.10.2026 (Admin-Auskunft, Feedback-Ordner, audit_log-Schwärzung, INVOKER-Suchpfad, anon-Rechte, Schutzspalten); Reihenfolge, Entscheidungen, offene Doku-PRs"
metadata:
  node_type: memory
  type: project
  originSessionId: 923fa7dd-4738-46a9-8312-a86297b91496
  modified: 2026-10-10T14:16:42.980Z
---

Alle sechs Migrationen sind live (10.10.2026), Reihenfolge 887 → 886 → 889 → 884, dann 888 und 885, die beiden letzten jeweils erst nach ihrem App-Merge.
- **887:** Pull-Anfrage #346.
- **886:** #348. Sicherungstabelle `mig_886_audit_log_vorher` am 10.10.2026 nach Bestätigung von Hannes gelöscht (verify-886 OK); Rückweg der Altzeilen nicht mehr möglich.
- **884 und 889:** #347. 884 wurde per replace-Block in den Live-Körper eingesetzt; die Selbstprüfung hat per md5 belegt, dass das Ergebnis byte-gleich mit der Datei ist.
- **888:** App #342.
- **885:** App #343. Die 38 verwaisten Feedback-Bilder sind über `pending_storage_cleanups` zum Löschen eingereiht (reason `feedback_waise_885`).

Weitere gemergte Pull-Anfragen ohne Migration: #338 (Admin-DSGVO über eine Route, CSP), #339 (`lib/supabase/database-helpers.ts`), #340, #341, #349.

Decisions delegated by Hannes on 10.10.2026:
- The storno reason `grund` stays readable in the audit log, because it is the revision proof.
- The orphaned feedback screenshots are deleted.

Follow-up PRs #350 (Dsgvo.test.tsx red on main after #338 met another session's admin test), #351, #352, #354 merged on 10.10.2026.

**Why:** Später fragen Sitzungen nach Stand, Reihenfolge und Rückwegen. Die Rückwege laufen in umgekehrter Reihenfolge: 884 → 889 → 886 → 887; 888 vor der App; 885 vor der App.
**How to apply:** Wer `verify-887` neu lesen muss: Das Skript kennt die Nachfolger 886, 888 und 889. Wer `export_user_data` oder `protect_privileged_profile_columns` ändert: Live-md5 55ade397… bzw. 19a5f469… pinnen. Siehe [[mig-876-879-verbund-folgepunkte]] und [[supabase-standardrechte-30-10-waechter]].
