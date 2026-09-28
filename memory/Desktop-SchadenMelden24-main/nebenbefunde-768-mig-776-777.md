---
name: nebenbefunde-768-mig-776-777
description: "Mig 776 (tote Funktion) + 777 (TRUNCATE/TRIGGER/REFERENCES/MAINTAIN für anon/authenticated) LIVE seit 28.09.2026, PR #210 gemergt; Mig 781 (Standort mit Termin-Verlauf löschbar) LIVE seit 28.09.2026, PR #216 gemergt"
metadata:
  node_type: memory
  type: project
  originSessionId: a10855be-d529-4a2d-a39f-2b15546e7bd7
  modified: 2026-09-28T16:17:37.454Z
---

Stand 28.09.2026: Mig 776 und 777 mit Freigabe von Hannes live eingespielt (Probeläufe und Prüfskripte live „776-TEST OK“/„777-TEST OK“, Ledger 776/777). PR https://github.com/hanneswrnr/SchadenMelden24/pull/210 gemergt (Merge 425440d6, Vercel-Build erfolgreich). Bericht: `wiki/09-Operations/Security-Audits/2026-09-27-nebenbefunde-768.md`. Migrationsdateien nicht mehr ändern.

Produktfrage „Standort mit Terminvorschlägen löschbar?“ hat Hannes an Claude übertragen (ADR-0029). Entscheidung: löschbar, sobald keine OFFENEN Vorschläge und keine künftigen/laufenden Termine (greatest(scheduled_date, scheduled_end_date) ab heute; archivierte zählen, Werkstatt-Papierkorb nicht; nur solange die Werkstatt besteht) daran hängen; erledigter Verlauf wird mitgelöscht (FK → CASCADE + BEFORE-DELETE-Trigger `zz_standort_loeschen_offene_termin_vorschlaege`, 23503 „(Mig 781)“). Mig 781 LIVE seit 28.09.2026 ~18:05 (Freigabe von Hannes; Probelauf und Prüfskript live „781-TEST OK“, Ledger 781, Funktions-md5 171d6275…). PR https://github.com/hanneswrnr/SchadenMelden24/pull/216 gemergt (Merge 028237c4, Vercel success); Worktree und lokaler Zweig aufgeräumt. Rückweg `scripts/rueckweg-781-…` bringt gelöschten Verlauf nicht zurück; nach 781 bricht ein erneutes Einspielen von 768 an dessen FK-Vorprüfung ab.

**Why:** Jeder Standort kostet 38 €/Monat; mit RESTRICT war ein Standort mit irgendeinem (auch altem) Vorschlag nie löschbar (live 4 von 9).

**How to apply:** Notfall-Rückwege in umgekehrter Reihenfolge, zuerst Rückweg 777 (763/773/774 brechen sonst ab, 767/772 öffnen Rechte wieder). Ab 30.10.2026 (Supabase) braucht jede neue Tabelle ausdrückliche GRANTs, auch für service_role; verify-777 meldet danach den geänderten Standard (dann Skript anpassen). Nach 781 bricht ein erneutes Einspielen von 768 an dessen FK-Vorprüfung ab. Verwandt: [[mig-772-gruppen-anon-spaltenrechte]], [[schadenmelden24-commit-regeln]].
