---
name: mig-866-verbund-lesen-zweite-stufe
description: "Mig 866 (Verbund-Zentrale liest nur mit aal2) LIVE seit 03.10.2026, PR #310 gemergt (3674a22f1); Ausnahme eigene Zeilen wegen HQ-Layout"
metadata:
  node_type: memory
  type: project
  originSessionId: c45a184a-541d-47f9-8903-7ccc96f00672
  modified: 2026-10-03T14:11:03.734Z
---

Mig 866 (`supabase/migrations/866_verbund_lesen_zweite_stufe.sql`) legt 24 RESTRICTIVE-Leseregeln
`hq_zweiter_faktor_select` an (16 Tabellen ganz, 7 mit Ausnahme für eigene Zeilen, Buckets
gruppen-ticket-attachments und ki-scans/gruppe). Zweig `fix/verbund-lesen-aal2`, Worktree
`C:/Users/hanne/sm24-verbund-lesen`, PR hanneswrnr/SchadenMelden24#310. **LIVE seit 03.10.2026** (Freigabe Hannes; Probelauf und
Prüfskript live „866-TEST OK“, danach 775/779-TEST OK, Ledger 866), PR gemergt (3674a22f1),
Worktree aufgeräumt, Todo nach completed/. Bericht `wiki/09-Operations/Security-Audits/2026-10-03-verbund-lesen-zweite-stufe.md`.

**Why:** Die HQ-Seiten (`resolveCurrentGruppeContext` in `app/(hq)/layout.tsx`) lesen eigenen
Admin-Eintrag und eigene Verbund-Zeile VOR der aal2-Prüfung, auch auf der 2FA-Einrichtungsseite;
deshalb bleiben diese zwei Zeilen bei aal1 lesbar (Folgeaufgabe `hq-kontext-aal1-kuerzen`).

**How to apply:** Neue Leseregeln mit HQ-Bezug (werkstatt_gruppen_admins, werkstatt_gruppen,
'werkstatt_gruppe', Helfer) nur auf den 23 Tabellen; sonst bricht die Vorprüfung bzw. der Wächter
866 an. Rückweg 763 nur nach Rückweg 866. verify-772/773/775/779 ignorieren
`hq_zweiter_faktor_select`. Folgeaufgaben `hq-kontext-aal1-kuerzen` und `gruppen-ticket-praefix-vorschlag-rechte` laufen als Mig 867 (PR #312), siehe [[mig-867-hq-kontext-ohne-ausnahme]]. Verwandt: [[mig-863-verbund-export-zweite-stufe]].
