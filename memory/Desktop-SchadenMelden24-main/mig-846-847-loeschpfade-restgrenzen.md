---
name: mig-846-847-loeschpfade-restgrenzen
description: "Mig 846 (Sätze vor Aufträgen beim Löschen) und 847 (Protokoll-Pause statt ALTER TABLE in anonymize_user_completely, Tabelle dsgvo_audit_pause) — LIVE seit 01.10.2026, PR #277"
metadata:
  node_type: memory
  type: project
  originSessionId: 9d21e877-92b8-4156-bf97-b25431aa7f45
  modified: 2026-10-01T04:40:25.809Z
---

Stand 01.10.2026: Folgeaufgabe aus [[mig-836-837-loeschpfade-sperr-reihenfolge]]. Beide Migrationen LIVE seit 01.10.2026 (Freigabe Hannes „1. freigegeben“), Ledger 846 `loeschen_satz_zeilen_vor_auftraegen`, 847 `anonymisierung_ohne_tabellensperre`; je Probelauf, Nachprüfung, Prüfskript OK; verify-846 nach 847 meldet sperranweisungen=7 (Nachfolger 847 erkannt). PR #277 gemergt 01.10.2026 (Merge-Commit 40032abd7, Zweig fix/loeschpfade-restgrenzen bleibt bestehen).

Gesamtreihenfolge jetzt Vermittler → Provisionssatz (vermittler_provision_configs) → Eigenauftrag → Standort → Schadenfall. 846: sechs Sperranweisungen in vier Funktionen (zz_loeschen_sperrt_auftraege_zuerst, owner_delete_vermittler, beide DSGVO-Funktionen). 847: Tabelle public.dsgvo_audit_pause (xid8-Anker, keine Rechte, RLS erzwungen, nur Regel wartende_werkstatt_sperre), audit_trigger_func mit verschachteltem Pausenblock (Schalter app.dsgvo_audit_pause → Umfang → Anker zuletzt), anonymize_user_completely ohne ALTER TABLE … TRIGGER und mit Sperrschritt im Versicherungs-Zweig; delete_user_data_hard unverändert (DISABLE TRIGGER USER bleibt). Live haben nur vier der fünf pausierten Tabellen einen Audit-Trigger (claims bewusst keinen seit 22.09.2026).

**Why:** Kreise „Satzänderung gegen Löschen“ und Agentur-/Vermittler-Anonymisierung gegen Gutschrift/Auftragsänderung (40P01) schließen.

**How to apply:** Rückweg nur in dieser Reihenfolge: erst scripts/rueckweg-847-… (Funktionen zurück, dann DROP TABLE), dann rueckweg-846-…. Neue Fassungen der DSGVO-Funktionen müssen ohne Trigger-Schalter in anonymize bleiben (Wächter 661/837/847), die Satz-Sperren behalten (Wächter 846) und als Nachfolger in die verify-Skripte 825/828/836/837/846/847 eingetragen werden. Neue Wartekante k6 (owner_reassign_vorgang gegen Agentur-Anonymisierung) bewusst akzeptiert. Offene Nebenbefunde (bypass_money_guard bis Transaktionsende, 40P01-Wiederholung in der Route, audit_log-Rechte) stehen im Bericht wiki/09-Operations/Security-Audits/2026-10-01-loeschpfade-restgrenzen.md.
