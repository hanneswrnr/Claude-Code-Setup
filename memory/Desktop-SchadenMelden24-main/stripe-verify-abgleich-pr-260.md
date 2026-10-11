---
name: stripe-verify-abgleich-pr-260
description: "PR #260 gemergt 30.09.2026 (37c2733f1) — verify nur eigenes Stripe-Abo, Rechnung ohne Zeile, Standort-Hinweis; Worktree entfernt"
metadata:
  node_type: memory
  type: project
  originSessionId: c329c92c-d6ca-4ad7-8098-2cebeaa541f6
  modified: 2026-09-30T17:33:41.662Z
---

Stand 30.09.2026: PR #260 mit Freigabe von Hannes gemergt (Merge-Commit 37c2733f1, Baum = getesteter Stand). Keine Migration. Live-Build war beim Merge in der Vercel-Warteschlange.
Inhalt: verify übernimmt nur Stripe-Abos mit eigenen Checkout-Metadaten, passender subscription_id und Tarif-Preis (lib/subscriptions/eigener-tarif.ts, von Webhook und verify geteilt); invoice.payment_succeeded ohne Zeile → 500 nur für die erste Rechnung (billing_reason subscription_create), wenn die Zeile noch entstehen kann, sonst error-Log + 200; Standort-Löschen mit quantitySync 'failed' → Hinweis mit Knopf im StandortManageModal; syncWerkstattQuantity wirft bei Lesefehlern.

**Why:** Bewusst KEIN nächtlicher Abgleich Standortzahl → Stripe: Werkstätten können auf der Abo-Seite Standorte im Voraus bezahlen (Reserve), der Abgleich würde sie jede Nacht löschen.

**How to apply:** Offene Folgepunkte: invoice.payment_failed ohne Zeile still; Preisänderung mit offenem Checkout → Abo ohne Zeile (Anleitung in wiki/02-Domain/Pricing.md); Kontolöschung löscht ganzen Stripe-Kunden (als eigene Folgeaufgabe vorgeschlagen).
