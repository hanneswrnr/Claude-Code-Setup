---
name: project-bezahlsystem-umbau
description: "Stand des Bezahlsystem-Umbaus (Haus-Testphase, Countdown, Abo-Seiten) - PR 47 am 24.09.2026 nach main, Nacharbeiten"
metadata:
  node_type: memory
  type: project
  originSessionId: 6a790586-7093-49c2-a530-4d88f8709950
  modified: 2026-09-25T14:04:42.385Z
---

Umbau des Bezahlsystems von SchadenMelden24, begonnen 21.09.2026. **PR 47 am 24.09.2026
mit Freigabe des Product Owners nach main zusammengefuehrt** (Merge-Commit `9fe283f6`).
Arbeitsbaum `C:\Users\hanne\sm24-pay` (Zweig `fix/bezahlsystem-testphase-zahlarten`) kann
fuer Nacharbeiten weiter genutzt werden, vorher main hineinmergen.

Kern: 30-Tage-Testphase in der eigenen Software (`subscriptions.is_app_trial`, Mig 657-659
auf Prod). Vergabe beim ersten Dashboard-Aufruf fuer jedes Konto ohne je eine Abo-Zeile
(pending_checkout zaehlt nicht); Werkstaetten erst nach Admin-Freischaltung. Beim Livegang
bekamen damit 1 Werkstatt und 39 Versicherungen beim naechsten Login die Testphase plus
Willkommens-Mail (Entscheidung PO 22.09.). Countdown auf den Startseiten, Hinweis bei der
Registrierung, neue Abo-Seiten (Praefix ab-), ROI-Rechner entfernt (Entscheidung im Auftrag
des PO: Faktoren ohne Beleg). Details ADR 0025 samt Nachtraegen.

**Offene Nacharbeiten nach dem Livegang:**
1. Zahlarten: Am 25.09.2026 hat der PO im Stripe-Konto (Default-Konfiguration des
   Plattformkontos) SEPA, Apple Pay, Google Pay und Revolut Pay aktiviert; Preisseite und
   llms.txt nennen sie (Commit fd1f1af86 auf main, live). PayPal wartet auf die Stripe-
   Genehmigung - danach PayPal in beiden FAQ-Antworten (PreisePageContent.tsx) und in
   llms.txt/llms-full.txt ergaenzen.
2. `cleanup-orphaned` macht standardmaessig nur Trockenlauf. Stand 25.09.2026: Der Bericht
   des Trockenlaufs steht NUR in der HTTP-Antwort, die Route loggt ausser Fehlern nichts
   (`app/api/subscriptions/cleanup-orphaned/route.ts`, einziges console.error Z. ~379) -
   im Vercel-Protokoll ist daher nichts zu sichten. Naechster Schritt: Zusammenfassung des
   Trockenlaufs per console.info loggen (Anzahl + Abo-/Entitaets-IDs, keine PII), eine Nacht
   laufen lassen, sichten, dann genau EINEN Aufrufer scharf stellen, siehe
   [[project-externer-cron-aufrufer]].
3. AGB-Merkpunkte fuer die naechste Fassung (ADR 0025 Nachtrag 24.09.): § 9 "(Monatsende)",
   § 15/§ 18 Testphasen-Wortlaut, § 18 Abs. 1 vor Freischalten des KI-Pakets aendern.
4. Versicherungs-Abo-Seite und -Countdown nur per Tests geprueft, nicht im Browser
   (kein Test-Versicherungskonto).
5. Bekannte Luecke: Bezahlschranke nur in API-Routen, nicht in der DB (RLS).
   Siehe [[project-security-anon-rls]].

Testkonto "Testwerkstatt 888" gehoert der Loesch-Sitzung - nicht anfassen.
