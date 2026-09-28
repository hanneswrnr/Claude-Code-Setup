---
name: mig-783-gruppen-hilfsfunktionen-ohne-anon
description: "Mig 783 (anon verliert EXECUTE auf _user_ist_werkstatt_der_gruppe(_read) und _werkstatt_id_von_user) LIVE seit 28.09.2026, PR #219 gemergt (a26ed518)"
metadata:
  node_type: memory
  type: project
  originSessionId: 9b80f603-172e-4ef5-a79b-614b9c4091e1
  modified: 2026-09-28T19:19:39.730Z
---

Stand 28.09.2026: Migration 783 ist **live** (Freigabe Hannes; Probelauf und Prüfskript „783-TEST OK“, „782-TEST OK“, Ledger 783) und mit Pull-Anfrage hanneswrnr/SchadenMelden24#219 nach main gemergt (Merge-Commit a26ed518, Freigabe Hannes). Rechte je Funktion jetzt `{postgres, authenticated, service_role}`; `authenticated` braucht EXECUTE (14 Regeln TO authenticated + Trigger aus 771).

**Why:** Befund aus dem Sicherheitsbericht zu Mig 782 — ohne Anmeldung ließ sich per /rest/v1/rpc die Werkstatt-Kennung zu jeder Konto-Kennung abfragen.

**How to apply:** Notfall-Rückweg: `scripts/rueckweg-783-…` als Ganzes plus Ledger-Eintrag 783 löschen. Die 782-Skripte akzeptieren beide Rechte-Stände; ein erneutes Einspielen der Datei 782 geht nur mit Rückweg 783 davor. Wer eine der drei Funktionen neu fasst oder Rechte an anon vergibt, löst den Zukunfts-Wächter `migration-783-…test.ts` aus. Offener Folgepunkt: angemeldete Konten können die Funktionen weiter mit fremden Kennungen aufrufen (siehe Bericht `wiki/09-Operations/Security-Audits/2026-09-28-gruppen-hilfsfunktionen-ohne-anon.md`). Verwandt: [[verbund-inaktiv-hq-nur-lesen-mig-779]].
