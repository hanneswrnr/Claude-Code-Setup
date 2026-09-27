---
name: schadenmelden24-mobile-restlos-weg
description: "Mobile-App und Push-Versand bei SchadenMelden24 sind restlos entfernt, Rechtstexte und Tarife seit 24.09.2026 nachgezogen; Rest sind Hannes-Entscheidungen"
metadata:
  node_type: memory
  type: feedback
  originSessionId: dba0837b-8412-4ef4-88f6-6812801dae4e
  modified: 2026-09-24T22:39:29.724Z
---

Bei hanneswrnr/SchadenMelden24 sollen Spuren der entfernten nativen App ueberall verschwinden, nicht nur dort, wo sie schaden. Ein technisch korrektes "ist ungefaehrlich" reichte Hannes nicht.

Stand 24.09.2026, gemergt:
- #31, #42, #45, #52, #48, #64, #68, #69: App, Push-Versand, Firebase und Doku-Reste entfernt.
- #73: Datenschutz 3.4 heisst jetzt "Kamerafunktion" (input capture, Kennzeichen wird im Browser ausgelesen), die Firebase-Zeile ist weg, consent.ts nennt kein Push mehr.
  - Der AV-Vertrag nennt Push/Firebase absichtlich weiter, bis AVV_GELTENDE_VERSION auf '2026-08-18' umgestellt wird.
  - Beim Umstellen stoppt der prebuild-Waechter scripts/run-no-mobile-app-guard.ts (Meldung [avv]) den Build, bis Push und Firebase aus dem Vertrag gestrichen sind.
  - feat/ai-features stellt die AVV-Fassung schon um. Vor dessen Merge main hineinholen und 3.4 um einen Verweis auf 17.7 (KI-Kennzeichen) ergaenzen.
- #77: Migration 690 (4 inaktive Alt-Tarife "E-Mail & Push" auf "E-Mail-Benachrichtigungen"), mit Hannes' Freigabe auf Prod eingespielt.

Am 25.09.2026 hat Hannes alle Empfehlungen freigegeben, erledigt:
- #80: Mig 691 setzt die zwei Push-Eintraege im Verarbeitungsverzeichnis inaktiv. Hannes hat sie selbst im SQL-Editor eingespielt, weil der Auto-Modus-Classifier apply_migration blockiert hat.
- #80: FAQ-Satz jetzt "Benachrichtigungen auf der Plattform und per E-Mail". Vermerke: Kamera-Rechtsgrundlage bei der naechsten Anwaltsdurchsicht pruefen; AVV-Firebase-Wegfall ohne eigene Ankuendigung.
- #43 (andere Sitzung): Cookie-Kategorie "Kommunikation" entfernt.
- #88: Foto-Metadaten werden entfernt.
  - Server: lib/image/metadaten-entfernen.ts mit sharp, in 6 Routen. Ueber 70 MP mit Metadaten gibt es HTTP 400, sonst fail-open mit logger.error.
  - Browser: lib/image/bild-neu-zeichnen.ts (JPEG) fuer Chat, Feedback und Unterschrift.
  - Auf echten Geraeten und fuer sharp im Vercel-Betrieb noch nicht geprueft; Fehler erscheinen in Sentry unter [metadaten-entfernen].

**Why:** Die Entscheidung ist seine. Er will das Thema abgeschlossen sehen, nicht nur entschaerft.

**How to apply:** Auftauchende App-/Push-Spuren aktiv entfernen. Rechtstexte und Datenbank-Inhalte nie eigenmaechtig aendern, sondern vorlegen. Freigaben gelten nur fuer das genannte Stueck (z. B. "5. ja auch bereinigen" = nur die Tarife). Siehe auch [[schadenmelden24-actions-abrechnung-blockiert]] und [[schadenmelden24-ohne-klon-arbeiten]].
