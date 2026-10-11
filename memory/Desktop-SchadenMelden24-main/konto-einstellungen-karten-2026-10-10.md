---
name: konto-einstellungen-karten-2026-10-10
description: "Stand 10.10.2026 – Admin modern, Einstellungen/Abo, Konto in Einstellungen + ein Bild, Mig 890/891/896 live, Google Maps LIVE (PR #371), Info-Boxen der Karten in Arbeit"
metadata:
  node_type: memory
  type: project
  originSessionId: 08a75455-f680-49af-a601-2bd875c47059
  modified: 2026-10-11T00:20:23.653Z
---

Live seit 10.10.2026: Admin-Bereich modern (PR #344), Abo-Box farbig + weicher Bereichswechsel (PR #345), „Mein Konto“ → Gruppe „Ihr Zugang“ in den Einstellungen aller Rollen, ein Bild je Rolle (PR #358). Mig 890, 891 und 896 LIVE (896 = Löschfrist externe_karten 2 Jahre ab greatest(created_at, granted_at) für alle Cookie-Arten, Verzeichnis ohne CARTO; PR #375 gemergt).

Google Maps LIVE seit 10.10.2026 (PR #371, Merge 964cb3198): Karte immer sichtbar (Entscheidung Hannes) – ohne Einwilligung sofort OpenStreetMap mit Link „Google-Karte anzeigen“, kein Platzhalter mehr; Browser-Einwilligung gilt 24 Monate (Feld kartenSeit). Karten-ADR heißt 0040 (0039 = Rechtsentscheidungen auf main). AV-Vertrag nennt CARTO bis zur angekündigten Fassung 16.11.2026 (ADR 0039 C2/C3), nicht vorher ändern.

Info-Fenster der Karten LIVE seit 11.10.2026 (PR #380, Merge 9448418c2): gemeinsame KartenInfo (Präfix ki-), „Aufträge ansehen“ → Liste mit ?standort=&ansicht=alle (alle Status inkl. Archiv, wie die Box zählt), sichtbarer Filter-Hinweis StandortFilterHinweis (components/shared). Worktrees kinfo, gmaps, mig895, ersatz, einst, konto, vlogo, alogo am 11.10. entfernt; stehen gelassen: sm24-admin (nur Zeilenenden-Änderung, ohne node_modules), sm24-karten (package-lock geändert), sm24-dsgvotest und sm24-seiten (Rest-Ordner ohne Worktree-Eintrag, evtl. andere Sitzung). Erledigt 11.10.: anonymize_user_completely braucht KEINE Migration für versicherung_branding (Kaskade auth.users → profiles → versicherungen → branding), Doku korrigiert per PR #381. Claude-App-Projekt „SchadenMelden24“: zurückgestellt bis Projekte für Claude Code ausgerollt sind (Dateien liegen in C:\Users\hanne\sm24-claude-projekt; die Claude-App darf ich nicht selbst bedienen). 11.10.: Mig 899 (Trigger zz_consent_records_zeitstempel_schutz, Zeitstempel der Zustimmungen setzt die DB) und Mig 900 (Datenauskunft der Agentur mit versicherung_branding) LIVE, PR #382/#383 gemergt, DSE Stand 11. Oktober 2026. Folgeaufgaben aus 899: R1 consent_version/ip/user_agent noch vom Client setzbar (Route per Service-Zugang schreiben lassen), R2 Regel consent_insert_anon offen und ungenutzt. Erledigt: consent_update_own erlaubt Konten, eigene Zeitstempel zu ändern (Nebenbefund 896).

**Why:** Hannes will alles modern und Karten wie Google, immer sichtbar, rechtssauber.
**How to apply:** Nach Info-Box-Merge die Worktrees sm24-gmaps, sm24-mig895, sm24-kinfo aufräumen (Junction zuerst lösen). Siehe [[mig-882-mfa-ersatzcodes]].
