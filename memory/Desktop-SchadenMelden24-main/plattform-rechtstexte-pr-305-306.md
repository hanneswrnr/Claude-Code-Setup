---
name: plattform-rechtstexte-pr-305-306
description: Plattform-Rechtstexte 03.10.2026: #305/#311 Datenschutzerklärung live, Mig 864 + 870 live, #306 AV § 8 im Zweig von #270 (ab 28.10.), Bewertungsbitte mit Einwilligung neu gebaut (#314); nächste AV-Fassung als Entwurf; AGB § 22 nächste Runde
metadata:
  type: project
  modified: 2026-10-03T16:47:05.553Z
---

Folgeaufgabe 2 aus PR #303 (Mustervorlagen), alles mit Freigabe von Hannes am 03.10.2026.

- PR #305 gemergt (35c3be809), live: Datenschutzerklärung ohne Google Places und ohne alte 7a.2, Absatz Sperrliste. Begründung `docs/legal/plattform-rechtstexte-2026-10-ENTWURF.md`.
- Mig 864 live (Ledger 864): Verarbeitungsverzeichnis `data_processing_activities` Places inaktiv, Sentry Frankfurt. Rückweg `scripts/rueckweg-864-verarbeitungsverzeichnis.sql`.
- PR #306 in den Zweig von #270 gemergt (364f0a904): AV § 8 ohne Places, Sentry Frankfurt, § 8 Abs. 4 Kopie der SCC, Vermerk unter dem Stand. Wird mit #270 am/nach 28.10. wirksam.
- PR #308 gemergt (e013a69b): alter Cron `feedback-funnel` abgeschaltet (lief ohne Einwilligung).
- Bewertungsbitte NEU mit Einwilligung (Entscheidung Hannes): Mig 870 LIVE seit 03.10.2026 (Ledger 870, 870-TEST OK), PR #314 gemergt (04993258e). Tabelle `kunde_einwilligungen` („erteilt“ nur per Trigger beim Unterschreiben der Mustervorlage), Schalter `notify_kunde_bewertungsbitte` Standard aus, `interne_feedback` für Browser nur lesen ohne token, Cron wieder in vercel.json, DSE 7a.2 neu. Bericht `wiki/09-Operations/Security-Audits/2026-10-03-bewertungsbitte-einwilligung.md`, Rückweg `scripts/rueckweg-870-...sql`.
- PR #311 gemergt (573fcc62e): DSE Abschnitt 11 ohne „Geräte für Push-Benachrichtigungen“.
- Nächste AV-Fassung (Bewertungsbitte § 2/§ 3, Papierkorb, OSM/CARTO, Sentry-Zweck, Löschklausel): Entwurf `docs/legal/avv-naechste-fassung-ENTWURF.md`, Todo `avv-naechste-fassung.md` (fällig 28.10.2026, erst nach Vollzug #270).
- AGB § 22 Mustervorlagen: Todo `agb-nachtrag-kennzahlen-audit.md` Punkt 5; aktive Zustimmung empfohlen.

**Why:** Rechtstexte sind Hannes' Entscheidung; Datenbank vor App-Code (Cron liest neue Tabelle).
**How to apply:** Offen: Einwilligungen in `export_user_data` und `export_user_data_for_kunde_token` aufnehmen (eigene Migration, Todo `plattform-rechtstexte-folgepunkte.md`). Löschfristen-Mig 868 löscht Kunden/Rechtsdokumente, CASCADE räumt Einwilligungen ab. Siehe [[rechtsdokument-mustervorlagen-pr-303]].
