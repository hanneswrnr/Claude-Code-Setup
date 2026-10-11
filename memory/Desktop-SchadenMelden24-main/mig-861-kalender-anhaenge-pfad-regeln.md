---
name: mig-861-kalender-anhaenge-pfad-regeln
description: "Mig 861 LIVE seit 02.10.2026 (PR #293): kalender-anhaenge nur Leseregel im eigenen Ordner, 536 nie eingespielt und entfernt, Rückweg entfernt nur die neue Regel"
metadata:
  node_type: memory
  type: project
  originSessionId: 69147cd5-0c98-4ed1-8914-742dc6922023
  modified: 2026-10-02T16:30:10.743Z
---

Mig 861 `kalender_anhaenge_pfad_regeln` ist LIVE seit 02.10.2026 (Ledger 861, Prüfskript live „861-TEST OK“), Zweig `fix/kalender-anhaenge-pfad-policies`, PR #293 gemergt am 02.10.2026 (8794eae1e). Ersetzt die drei Speicher-Regeln von Mig 357 (prüften `foldername(w.name)` = Werkstatt-Name, mit selbst gesetztem Namen Zugriff auf alle Dateien) durch nur `kalender_anhaenge_eigene_lesen` (SELECT, authenticated, Pfad `<werkstatt_id>/<event_id>/<datei>`). Hochladen/Löschen für Nutzer gibt es nicht mehr (App lädt seit 19.09.2026 nichts hoch).

**Why:** Die Korrektur 536 lag seit Juni im Repo, war aber nie eingespielt; Wiki/Runbook behaupteten „live, ledger-los“. Hannes hat am 02.10.2026 Einspielen und Merge ausdrücklich freigegeben („alle Sachen sind sofort freigegeben … Auch Merge!“).

**How to apply:**
- Rückweg `scripts/rueckweg-861-…` entfernt NUR die Leseregel (bewusste Abweichung von „byte-genau“; die 357-Regeln gaben nur die Lücke). 861 lässt sich danach erneut einspielen (Vorprüfung akzeptiert „keine Regel für den Bucket“).
- Folgepunkt offen: Aufräum-Trigger aus Mig 361 (`queue_kalender_anhaenge_cleanup_for_event`) übernimmt storagePath aus der frei beschreibbaren `attachments`-Spalte ohne Ordnerprüfung – vor einer Rückkehr des Hochladens auf den eigenen Ordner begrenzen. Der Wächter `lib/kalender/__tests__/migration-861-…` schlägt an, wenn App-Code wieder in den Bucket hochlädt.
- Live hat seit 861 keine Speicher-Regel mehr den Alias-Fehler (Abfrage in `wiki/05-Anti-Patterns/Storage-Policy-Aliasing.md`).
- Verwandt: [[schadenmelden24-commit-regeln]], [[supabase-standardrechte-30-10-waechter]].
