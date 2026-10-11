---
name: mig-825-abrechnung-sperr-reihenfolge
description: "Mig 825 (Eigenaufträge vor Schadenfällen sperren in 4 Funktionen) LIVE seit 30.09.2026 ~19:05, PR #259 gemergt (e566d45b); Folge Mig 836/837 für Löschpfade"
metadata:
  node_type: memory
  type: project
  originSessionId: 0a7cfba0-5f8a-4bb7-9bb1-af35bd723b5d
  modified: 2026-09-30T17:16:54.016Z
---

Migration 825 stellt `owner_create_abrechnung` (Schritt 4b), `provision_neu_berechnen`,
`recalculate_vermittler_provisions_on_config_change` und `owner_delete_vermittler` (erst
Vermittler-Zeile, dann Aufträge) auf „Eigenauftrag vor Schadenfall“ um. **Live seit 30.09.2026**
(Freigabe Hannes; Probelauf und Prüfskript „825-TEST OK“, Ledger 825, verify-802 Teil 1–2 OK),
PR hanneswrnr/SchadenMelden24#259 gemergt als e566d45b.

**Why:** Nur die Gutschrift umzudrehen hätte mit den drei anderen Funktionen neue Zweier-Kreise
erzeugt. Restgrenze: FK-Kaskaden beim Löschen eines Standorts oder Vermittler-Kontos (live
claims vor werkstatt_auftraege) und DSGVO-Vermittler-Zweig laufen jetzt gegen die Gutschrift;
Folgeaufgabe als Mig 836/837 in eigener Sitzung (Zweig fix/loeschpfade-sperr-reihenfolge), deren
Vorprüfung verlangt Ledger 825 und den Text „Mig 825: Sperrreihenfolge“ in allen vier Körpern.

**How to apply:** Neue Stellen, die claims und werkstatt_auftraege gemeinsam sperren oder ändern,
sperren die Aufträge zuerst (Gesamtreihenfolge in wiki werkstatt_standorte.md). Rückweg 825 nur
nach Rückweg 836/837. verify-802 Teil 3 wird live bewusst nicht ausgeführt.
