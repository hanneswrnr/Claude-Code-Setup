---
name: terminsystem-vereinfachung-konzept
description: Konzept v2 zur Vereinfachung des Werkstatt-Terminsystems (Google-artige Termin-Maske) liegt seit 16.09.2026 in .planning; Google-Push-Sync in Prod vermutlich tot (falscher Spaltenname); 11 PO-Entscheidungen offen
metadata: 
  node_type: memory
  type: project
  originSessionId: bb0d2f4d-2dd6-470d-a213-32389480b147
  modified: 2026-09-16T13:47:52.716Z
---

Am 16.09.2026 entstand nach Werkstatt-Feedback (Triccon: „unübersichtlich, schwer zu bedienen“, arbeitet hauptsächlich in Google Calendar) das Konzept `.planning/features/terminbuchung/VEREINFACHUNG-KONZEPT.md` (v2) plus Skizze `VEREINFACHUNG-SKIZZE.html` (v2, fünf Zustände, Klick-Karte, „Wir haben zu“, Leiste nach dem Ziehen). Leitidee „Ein Termin, eine Maske, eine Wahrheit“; die Entscheidung „Und der Kunde?“ (fest / sucht Zeit aus / ohne Nachricht) steht direkt unter der Zeit.

**Wichtiger Befund (gegen Prod-DB `ownxhgvhciwknzonmsbs` geprüft, nur lesend):** `lib/termin/gcal/sync.ts` liest an claims/werkstatt_auftraege die Spalte `ganztaegig`, die dort nicht existiert (heißt `scheduled_ganztaegig`); Fehler wird verschluckt. 6 Google-Verbindungen, 0 terminierte Aufträge der letzten 60 Tage mit gcal_event_id. Push nach Google läuft vermutlich seit dem Refactoring ins Leere. Reparatur = Stufe 0 im Konzept. Keine der 6 Werkstätten steht noch auf Kapazität 1/1.

**Why:** Kalender-Bereich 11.800 Zeilen, 13 Fenster, 4 Eingabemasken, 5 Einstiege; Mechaniker-Walkthrough und Paritätsprüfung (16.09.) haben die v1-Lücken benannt (Gegenvorschlag, Ändern-Frage, Kunde ohne E-Mail, Leerzustand, Sperren).

**How to apply:** Vor Umsetzung die 11 Entscheidungen in §8 des Konzepts einholen („Empfehlungen übernehmen“ reicht). Reihenfolge: Stufe 0 Sync-Fix → Stufe 1 Maske an fünf Einstiegen (alte Masken hinter Schalter bis Triccon-Test) → Google-Punkte → Kalender entschlacken → Einstellungen → Kalender-Wahl/Push-Kanal. Versicherungs-Kalender teilt Komponenten, mitdenken. Siehe [[schaden-melden-formular-bleibt]].
