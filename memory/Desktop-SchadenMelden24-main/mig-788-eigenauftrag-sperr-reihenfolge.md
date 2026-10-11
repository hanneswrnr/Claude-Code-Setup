---
name: mig-788-eigenauftrag-sperr-reihenfolge
description: "Mig 788 live seit 30.09.2026 (PR #255 gemergt 30.09.2026, d9cb315e) — Terminvorschlag zum Eigenauftrag: Standort FOR KEY SHARE, Auftrag, dann Standort FOR SHARE"
metadata:
  node_type: memory
  type: project
  originSessionId: 8a293cc6-30cd-4230-8259-187e9434aa70
  modified: 2026-09-30T15:26:37.852Z
---

Mig 788 ist seit 30.09.2026 live (Freigabe Hannes „2. freigeben“, Probelauf und verify-788/787/768 OK, Ledger 788). Zweig `fix/eigenauftrag-sperr-reihenfolge`, PR #255 am 30.09.2026 gemergt (Merge-Commit d9cb315e, Freigabe „1. freigegeben“); Zweig nicht löschen, das macht der Zweig-Aufräum-Auftrag. `zz_termin_vorschlag_gleiche_werkstatt` hat einen eigenen Eigenauftrag-Zweig: Standort ungesperrt lesen, fremden Auftrag ungesperrt abweisen, Standort FOR KEY SHARE, Auftrag FOR NO KEY UPDATE, dann Standort FOR SHARE und Vergleich. Schadenfall-Pfad wie 787.

**Why:** Kreis aus Vorschlag (Standort vor Auftrag) + Umhängen per 760 bzw. Warteliste 774 (Auftrag vor Standort) + Umschaltung (Mig 786) gab 40P01. Die FOR-KEY-SHARE-Sperre kam nach der Sicherheitsprüfung dazu: ohne sie neuer 40P01 beim Löschen des Standorts, während ein Dritter den Auftrag hält.

**How to apply:** Eigenauftrag überall „Auftrag, dann Standort“ (FOR KEY SHARE auf den Standort davor ist erlaubt); Schadenfall „Standorte nach id, dann Schadenfall“. Offene Folgeaufgabe (Chip): `owner_create_abrechnung` sperrt Schadenfälle vor Aufträgen → Vier-Parteien-Kette. Keine Großbuchstaben mit Umlaut in Funktionskörpern (Wächter bricht ab). Wächter `lib/termin/__tests__/migration-788-*` hält Live- und Datei-md5 fest. Verwandt: [[mig-787-standort-sperren-reihenfolge]], [[mig-786-standorte-folgebefunde]].
