---
name: gruppen-tickets-spaltenschutz-mig-771
description: "Mig 771 (Spaltenschutz gruppen_tickets/-messages, N1–N4 aus Mig-766-Prüfung) live seit 27.09.2026, PR 201 gemergt (0bd791ff)"
metadata:
  node_type: memory
  type: project
  originSessionId: 0e767399-b47f-4803-9217-3b81537fb08d
  modified: 2026-09-27T20:51:20.826Z
---

Stand 27.09.2026: Migration 771 `gruppen_tickets_spaltenschutz` ist live (Freigabe Hannes; Probelauf und Prüfskript live „771-TEST OK“, Ledger-Eintrag 771). BEFORE-Trigger `aa_gruppen_tickets_spaltenschutz` und `aa_gruppen_ticket_messages_spaltenschutz`, WITH CHECK der Werkstatt-Regel verschärft, `gruppen_ticket_messages_update` entfernt. App-Teil (M-45-Fehlermeldungen, read/PATCH-Route) mit PR hanneswrnr/SchadenMelden24#201 am 27.09.2026 in main gemergt (Merge-Commit 0bd791ff).

**Why:** Datenbank erzwingt jetzt Spalten je Rolle und die Statuswechsel der App; Nachrichten sind nicht mehr bearbeitbar.

**How to apply:** Neue Spalte in gruppen_tickets, die ein Client ändern soll, muss in die Spaltenliste der Trigger-Funktion (neue Migration, CREATE OR REPLACE aus dem Live-Körper, md5 22b06afb…). Nachrichten-Bearbeiten wieder einführen nur mit eigener BEFORE-UPDATE-Prüfung (nie absender_rolle system). Rückweg: scripts/rueckweg-771-gruppen-tickets-spaltenschutz.sql. Muster wie [[werkstatt-freischaltung-mig-620]].
