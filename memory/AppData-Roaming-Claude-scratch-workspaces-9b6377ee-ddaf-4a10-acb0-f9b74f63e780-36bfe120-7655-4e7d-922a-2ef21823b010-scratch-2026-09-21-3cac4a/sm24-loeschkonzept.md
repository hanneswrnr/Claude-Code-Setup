---
name: sm24-loeschkonzept
description: "SchadenMelden24 — geltendes Löschkonzept (Mig 662/663/680, Stand 24.09.2026) und die Rechtsgründe dahinter"
metadata:
  node_type: memory
  type: project
  originSessionId: 47f0339f-0e3c-46ed-848a-f0ec414fa721
  modified: 2026-09-24T18:45:15.194Z
---

Löschkonzept SchadenMelden24, geprüft von Datenschutz- und Steuer-Reviewern am 24.09.2026, umgesetzt in Mig 680 (in Produktion), PR #87.

- Geschäftsdaten des Kontos werden gelöscht (Art. 28 Abs. 3 lit. g); Aufbewahrungspflichten trägt das Unternehmen selbst (Export JSON/CSV vorher).
- Gemeinsame Fälle bleiben für die andere Partei; eigene Nachrichten darin mit Absender „Gelöschtes Konto (…)“, interne Notizen gehen.
- „Gutschriften“ (provisionen_abrechnungen) sind KEINE Plattform-Belege: die Werkstatt zahlt die Agentur direkt, SM24 ist nicht im Geldfluss (Betreiber Kleinunternehmer § 19 UStG). Sie gehen mit dem Agentur-Konto; nur ein Grabstein-Kopf (Summen 0) bleibt für abrechnung_id. PDF heißt „Provisionsübersicht“.
- Aufbewahrt: nur Abo-Rechnungen der Plattform (8 J. ab Jahresende, § 147 AO, § 14b UStG) und Löschnachweis dsar_requests erasure (3 J. ab Jahresende, Art. 5 Abs. 2).
- Kennung von claims/werkstatt_auftraege vergibt der Server (Trigger aa_vorgang_kennung_vom_server) — schloss Kennungs-Trick.
- PO-Entscheidung 24.09.2026: KEINE Ergänzungsmitteilung zur AGB/AVV-Änderung jetzt (Entwurf docs/legal/loeschung-agb-avv-aenderung-ENTWURF.md bleibt liegen, erst mit einer späteren AGB-Änderung mitnehmen); KEINE Info an die 3 Agenturen mit alten Gutschrift-PDFs. Browser-Löschtest mit Testwerkstatt 888 (hannes-werner+testwerkstatt@outlook.de) macht der PO später in einem anderen Chat; PO tippt Passwort und letzten Klick selbst.
- Offen: Verbund-Tickets nach 6 J. löschen, interne Notizen serverseitig schützen, Netzwerk-Gespräche für Gegenseite erhalten.

**Why:** Am 22.09. hatte ich Gutschriften ohne Prüfung des Geldflusses als Plattform-Belege eingestuft — falsch. Belegklassifizierung immer am tatsächlichen Leistungs-/Zahlungsweg prüfen.

**How to apply:** Bei Änderungen an Löschung, Export, Aufbewahrung oder Rechtstexten diesen Stand zugrunde legen; Wiki-Abschnitt „Löschkonzept“ in wiki/09-Operations/Security-Audits/2026-09-19-email-wechsel-passwortregeln.md ist die Detailquelle. Siehe [[sm24-rechtsfragen-selbst-entscheiden]].
