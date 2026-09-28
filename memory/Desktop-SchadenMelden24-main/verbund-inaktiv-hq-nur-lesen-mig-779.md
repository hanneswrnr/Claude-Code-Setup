---
name: verbund-inaktiv-hq-nur-lesen-mig-779
description: "Verbund nie löschen, nur deaktivieren (PR 208); deaktiviert ⇒ HQ nur lesen (PR 213, Mig 779 live) und Ticketsystem ruht auch für Mitglieder (PR 217 gemergt, Mig 782 live seit 28.09.2026)"
metadata:
  node_type: memory
  type: project
  originSessionId: afbd755b-7ec9-45d9-bb00-6af78cc040e1
  modified: 2026-09-28T16:23:19.235Z
---

Stand 28.09.2026, abgeschlossen: Hannes hat entschieden, dass ein Verbund (werkstatt_gruppen) nie gelöscht, nur deaktiviert wird (Admin-Schalter PATCH /api/admin/werkstatt-gruppen/[id], PR #208), und dass das HQ-Team eines deaktivierten Verbunds nur noch lesen darf. PR https://github.com/hanneswrnr/SchadenMelden24/pull/213 gemergt (Merge-Commit 2c8cbea3, Produktion ausgerollt). Mig 779 live seit 28.09.2026 (Freigabe Hannes; Probelauf und Prüfskript „779-TEST OK“, Ledger 779): Funktion ist_hq_konto_mit_inaktivem_verbund() + 21 RESTRICTIVE-Regeln hq_verbund_inaktiv_* auf 6 Ticket-Tabellen und storage.objects (gruppen_ticket_saved_views bewusst offen).

**Why:** Alle HQ-Schreibwege laufen mit Dienstschlüssel — die verbindliche Sperre sitzt in requireHqAdmin (allowedRoles ohne viewer = schreibend, 403 VERBUND_INAKTIV) und requireTicketSchreibContext/hqNurLesenAntwort; 779 schließt die direkten PostgREST-Wege.

**How to apply:** Neue HQ-Schreibrouten müssen requireHqAdmin ohne viewer nutzen (Wächter hq-schreibrouten-waechter.test.ts). Neue direkte HQ-Schreibtabellen brauchen hq_zweiter_faktor_* UND hq_verbund_inaktiv_*. Der Zukunfts-Wächter von Mig 775 führt die 779-Funktion in GEPRUEFTE_SPAETERE_BEFUNDE. Die frühere Produktfolge (Mitglieder schicken Tickets an ein gesperrtes HQ, Eskalations-Mails laufen weiter) ist mit dem Nachtrag unten erledigt. Verwandt: [[gruppen-tickets-spaltenschutz-mig-771]].

**Nachtrag 28.09.2026:** Hannes: Mitglieder dürfen einem deaktivierten Verbund keine Tickets schicken („darf natürlich nicht passieren“). Umgesetzt: Ticketsystem ruht für den ganzen Verbund (Werkstatt-Schreibsperre in loadTicketContext/werkstattSchreibSperrAntwort, 403 VERBUND_INAKTIV; Hinweis WerkstattTicketSperrHinweis; Mig 782 ändert _user_ist_werkstatt_der_gruppe() und Sicht tickets_eskalation_candidates). Zweig feat/verbund-inaktiv-tickets-ruhen, PR https://github.com/hanneswrnr/SchadenMelden24/pull/217. **Mig 782 live seit 28.09.2026** (Freigabe Hannes, Probelauf und Prüfskript „782-TEST OK“, Ledger 782); PR 217 gemergt (031d264c), Produktion ausgerollt. Neue Werkstatt-Ticket-Schreibrouten brauchen werkstattSchreibSperrAntwort (Wächter gruppen-tickets-schreibschutz-waechter). Folge-Aufgabe angelegt: anon-EXECUTE auf _user_ist_werkstatt_der_gruppe(_read) und _werkstatt_id_von_user entziehen.
