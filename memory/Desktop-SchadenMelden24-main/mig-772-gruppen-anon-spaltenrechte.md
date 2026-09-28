---
name: mig-772-gruppen-anon-spaltenrechte
description: Mig 772 (anon nur 5 Spalten von werkstatt_gruppen, 9 Regeln TO authenticated) LIVE seit 27.09.2026, PR #203 gemergt; Folgebefund für angemeldete Konten läuft als eigene Sitzung
metadata:
  node_type: memory
  type: project
  originSessionId: c2303351-61a6-4505-9093-6dc9dd1a5f32
  modified: 2026-09-27T22:39:55.720Z
---

Stand 27.09.2026: Mig 772 mit Freigabe von Hannes live eingespielt (Probelauf und Prüfskript live „772-TEST OK“, Ledger 772 gesetzt). PR https://github.com/hanneswrnr/SchadenMelden24/pull/203 am 27.09.2026 mit Freigabe von Hannes gemergt (Merge-Commit 6c027bad). Migrationsdatei nach dem Einspielen nicht mehr ändern.

**Why:** anon hatte Tabellen-SELECT auf werkstatt_gruppen (alle 43 Spalten gelisteter Gruppen) und drei HQ-Nebentabellen; jede anonyme Abfrage scheiterte mit 42501 an Regeln TO public → schlummerndes Leck und kaputte Verbund-Auswahl der Werkstatt-Registrierung (Schritt 3 läuft als anon). Seit 772 lädt die Auswahl wieder.

**How to apply:** Neue öffentliche Seite braucht weitere Spalten → bewusst per neuer Migration an anon freigeben (Wächter migration-772-…test.ts passt auf). Der Folgebefund (angemeldete Konten, Sicht mv_werkstatt_mit_aktivem_branding) ist Mig 775, siehe [[mig-775-gruppen-angemeldete-spaltenrechte]]. Nach 775 meldet scripts/verify-772 erwartungsgemäß FAIL 3b. Notfall: Rückwege in der Reihenfolge 775 → 772 → 763. Verwandt: [[schadenmelden24-commit-regeln]].
