---
name: loeschfristen-folgeaufgaben-mig-868
description: "Löschfristen-Folgeaufgaben: Mig 868 LIVE seit 03.10.2026, PR #316 GEMERGT (3eda046bb), 12 Altpfad-Dateien gelöscht; 869 entfällt"
metadata:
  node_type: memory
  type: project
  originSessionId: b1d5046e-a8f0-4e32-b180-94be9d785858
  modified: 2026-10-03T17:13:46.022Z
---

Folgeaufgaben 1–6 der Löschfristen (Auftrag Hannes 03.10.2026 „alle gleich“), Bauvertrag `.planning/features/loeschfristen/FOLGEAUFGABEN.md`, Todo in `.planning/todos/completed/`. Stand 03.10.2026, alles mit Freigabe von Hannes: **Mig 868 LIVE** (Probelauf und Prüfskript „868-TEST OK“, Ledger 868), **PR #316 gemergt** (3eda046bb), Einmal-Skript `scripts/einmalig-868-verwaiste-altpfade.sql` ausgeführt (12 Dateien vorgemerkt und gelöscht).

- 868: Kalendereinträge gehen mit dem Auftrag (FK CASCADE); Trigger `zz_kalender_event_bezuege_gleiche_werkstatt`/`zz_auftrag_werkstatt_wechsel_kalender` (Kalender-Verweise nur in derselben Werkstatt — sonst blockiert ein fremder Eintrag per Kaskade Papierkorb/Kontolöschung); neue Arten kalender/rechnung/ablage/kassenbuch/kassenabschluss; Halt eines Auftrags durch Kalendereinträge höchstens 3 Jahre nach deren Anlegen. Rechnungen/Ablage/Kassenbuch ohne Oberfläche → Fristen nur in der DB, sichtbare Texte nennen sie nicht.
- 869 entfällt: anonymize_user_completely löscht am Ende auth.users, Kunden gehen per Kaskade samt Löschsperre mit. Künftige Neufassung von anonymize braucht die Härtung von app.bypass_money_guard (Wächter geldschutz-schalter-loeschfunktionen).
- AV-Vertrag schreibt die Sitzung „Plattform-Rechtstexte“ (Entwurf docs/legal/avv-naechste-fassung-ENTWURF.md, Ankündigung ab 28.10.2026, Kalender-Teile freigeschaltet).

**Why:** Lücken aus Mig 865 (Kalendertermine gelöschter Aufträge, ungenutzte Rechnungstabellen ohne Frist, unsichtbare Dokumente gelöschter Aufträge).

**How to apply:** Datei 868 nie mehr ändern. Wer Rechnungen/Ablage/Kassenbuch eine Oberfläche gibt: Dateien vormerken (Trigger), Kartei soll Rechnungen als Bezug zählen, Texte in Einstellungen/DSGVO-Report/Datenschutzerklärung/AV ergänzen (ADR 0034 Nachtrag). Offener Folgepunkt aus 861: Anhang-Trigger (Mig 361) merkt Pfade ohne Ordner-/Längenprüfung vor. Verwandt: [[loeschfristen-kundendaten-mig-865]].
