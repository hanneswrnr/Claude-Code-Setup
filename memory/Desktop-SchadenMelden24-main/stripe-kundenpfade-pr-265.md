---
name: stripe-kundenpfade-pr-265
description: "PR #265 Stripe-Kundenpfade (Portal, Checkout, E-Mail-Abgleich nur bei eigenem Kunden; Abo ohne Firma kündigen) — GEMERGT 30.09.2026 (e5ca606dd), keine Migration; Werkstatt-Kündigen-Knopf auf Zweig feat/werkstatt-kuendigen-knopf"
metadata:
  node_type: memory
  type: project
  originSessionId: 1880efdf-b626-4ab1-89c6-31e3636e5536
  modified: 2026-09-30T21:48:07.829Z
---

Zweig `fix/stripe-kundenpfade-geteilte-kunden` (Worktree C:\Users\hanne\sm24-stripe-kunden), PR hanneswrnr/SchadenMelden24#265, gepusht am 30.09.2026 mit [vorschau] im obersten Commit (Merge von main). Nicht gemergt — Merge braucht Freigabe von Hannes. Keine Migration.

Kern: `pruefeEigenenKunden` in lib/subscriptions/stripe-kunde-eigen.ts (Metadaten nur diese Firma inkl. Altbestand user_id des Inhabers/enterprise_angebot_id, alle Abos/Rechnungen/Checkouts/Zahlungen eigen). Portal nur bei eigenem Kunden (409/503), kein Rückfall aufs Standard-Portal ohne STRIPE_BILLING_PORTAL_CONFIG_ID. Webhook kündigt Abo zu gelöschter Firma (lib/subscriptions/abo-ohne-firma.ts). Einzelrechnungen gelten bewusst als fremd (subscription_invoices live leer).

**Why:** Stripe-Konto ist mit Origin Labs geteilt; Stripe kann das Portal nicht pro Produkt beschränken.

Am 30.09.2026 nach Freigabe gemergt (main danach baumgleich mit dem geprüften Stand). Werkstatt-Kündigen-Knopf („Vertrag kündigen“ ruft /api/subscriptions/cancel) als PR #268 am 30.09.2026 gemergt (7a7db8184), Sichtprüfung 393/768/1280 hell/dunkel bestanden. Entscheidung (an Claude delegiert): keine App-Kündigung bei past_due/unpaid/paused — Begründung im Wiki Stripe-Konto-Mehrere-Produkte.

Offener Punkt geklärt und live (PR #272, gemergt 30.09.2026, b37d1d6f1): Checkout verknüpft den Zahlungsvorgang erst nach Erfolg mit der Rechnung; abgebrochene/abgelehnte Versuche (PaymentIntent ohne Geldfluss) zählen in pruefeEigenenKunden nicht mehr. Kontolöschung bleibt bewusst streng.

**How to apply:** Bei neuen Prüfungen „gehört diese Zahlung uns?“ nur PaymentIntents mit Geldfluss (succeeded/processing/requires_capture) einer Rechnung zuordnen. Verwandt: [[stripe-kontoloeschung-pr-261]], [[stripe-verify-abgleich-pr-260]].
