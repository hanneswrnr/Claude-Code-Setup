---
name: mig-836-837-loeschpfade-sperr-reihenfolge
description: "Mig 836/837 (Löschkaskaden und DSGVO-Löschung sperren Eigenaufträge vor Schadenfällen) — LIVE seit 30.09.2026, PR #271 gemergt; Rückweg 825/828 nur nach Rückweg 836/837"
metadata:
  node_type: memory
  type: project
  originSessionId: 9d21e877-92b8-4156-bf97-b25431aa7f45
  modified: 2026-09-30T21:44:54.502Z
---

Stand 30.09.2026: Mig 836 (BEFORE-DELETE-Trigger auf werkstatt_standorte, vermittler, versicherungen, Funktion zz_loeschen_sperrt_auftraege_zuerst(); bei der Agentur erst Vermittler-Zeilen FOR UPDATE, dann Eigenaufträge) und Mig 837 (anonymize_user_completely nur Vermittler-Zweig, delete_user_data_hard Versicherungs- und Vermittler-Zweig; Körper wörtlich aus 828 plus drei Blöcke) sind LIVE seit 30.09.2026 gegen 23:30/23:40 Uhr, nach Freigabe von Hannes. Ledger 836/837, Prüfskripte 836, 837 und 781 gegen Live „TEST OK“. Zweig fix/loeschpfade-sperr-reihenfolge, PR #271 gemergt 30.09.2026 (251ba290d). Container 836 182/0, 837 205/0.

**Why:** Folgeaufgabe aus [[mig-825-abrechnung-sperr-reihenfolge]]; nach 825 liefen Löschkaskaden gegen die Gutschrift (40P01 möglich).

**How to apply:** Neue Fassungen von anonymize_user_completely/delete_user_data_hard müssen die Sperrschritte aus 837 behalten (Wächter migration-837 prüft). Kein Sperrschritt im Versicherungs-Zweig von anonymize_user_completely (dort ALTER TABLE … DISABLE TRIGGER → neuer Kreis). Rückweg 825/828 nur nach Rückweg 836/837. Offene Folgeaufgaben: Satz-Zeilen beim Vermittler-Löschen früher sperren; DSGVO-Funktionen Trigger per Transaktions-Schalter statt ALTER TABLE abschalten. GitGuardian-Fehlalarm aus Test 837 (Vorfall 37760391) am 01.10.2026 als „Test credential“ ignoriert. Folgeaufgaben laufen als Mig 846/847 (Zweig fix/loeschpfade-restgrenzen).
