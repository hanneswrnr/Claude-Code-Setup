---
name: mig-832-835-folgepunkte-annahme-lager-verbund
description: "Mig 832–835 (Annahme-FKs, Storage-Dateischutz, Lager-Abo-Tor, Verbund-Einladung R5a) LIVE seit 30.09.2026, PR #263 gemergt (08d57253)"
metadata:
  node_type: memory
  type: project
  originSessionId: 67a02df8-5536-4b42-aa9b-c58835a2f55f
  modified: 2026-09-30T18:56:13.413Z
---

Stand 30.09.2026: Mig 832 (FKs Foto→Protokoll→Auftrag gleiche Werkstatt, eindeutige Indizes statt UNIQUE-Constraint), 833 (RESTRICTIVE DELETE-Regel auf storage.objects für Bilder abgeschlossener Annahmeprotokolle, Hilfsfunktion annahme_foto_datei_gesperrt), 834 (lager_bewegung_buchen mit `werkstatt_abo_gueltig_wie_app(...) IS NOT TRUE` → SUBSCRIPTION_REQUIRED) und 835 (verbund_einladung_beantworten: eingelöste Einladung nur vom registrierten Konto) sind LIVE (Probelauf und Prüfskripte OK, Ledger 832–835 vorhanden). PR #263 gemergt am 30.09.2026 (Merge-Commit 08d57253).

Zusätzlich App: `lib/annahme/pfad.ts` — Service-Routen signieren/löschen nur Pfade im Auftragsordner; lehnt `%`, `?`, `#`, `\`, Steuerzeichen und `.`/`..` ab (storage-js setzt Pfade unkodiert in die URL, fetch deutet `%2e%2e` als `..`).

**Why:** Folgepunkte aus den Berichten zu Mig 829–831 und 828; Bericht wiki/09-Operations/Security-Audits/2026-09-30-folgepunkte-annahme-lager-verbund.md.

**How to apply:** Rückwege der Vorgänger (829/759 nach 834, 780 nach 835, 830 nach 833/832) brechen ab, bis die neuen zurückgenommen sind; Notfall zuerst `scripts/rueckweg-83x-*.sql` in umgekehrter Reihenfolge. Die Migrationsdateien nicht mehr ändern. Offener Folgepunkt (eigene Sitzung läuft): `claim_attachments.file_path` ist frei wählbar, weitere Service-Routen signieren ungeprüft. Produktentscheidungen (Endgültigkeit abgeschlossener Annahmeprotokolle, Rechtsdokumente vom Client) laufen in anderen Chats. Verwandt: [[schadenmelden24-commit-regeln]], [[supabase-standardrechte-30-10-waechter]].
