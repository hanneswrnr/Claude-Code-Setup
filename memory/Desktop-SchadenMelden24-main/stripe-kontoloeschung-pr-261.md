---
name: stripe-kontoloeschung-pr-261
description: "Kontolöschung kündigt nur eigene Stripe-Abos, löscht Kunden nur ohne fremde Objekte — PR #261 gemergt 30.09.2026 (ff628011), Datenschutzerklärung angepasst"
metadata:
  node_type: memory
  type: project
  originSessionId: db7bfe8b-6197-4ff6-b2db-6ad077a40739
  modified: 2026-09-30T18:07:41.172Z
---

PR #261 (Zweig `fix/stripe-kontoloeschung-eigene-abos`, Worktree `C:/Users/hanne/sm24-stripe-loeschen`) am 30.09.2026 mit Freigabe von Hannes gemergt, Merge-Commit ff628011. Keine Migration.

Kern: `lib/subscriptions/stripe-kontoloeschung.ts`; eigene Abos einzeln kündigen, `customers.del` erst nach der Lösch-RPC und nur ohne fremde Objekte, sonst nur eigene Metadaten leeren. Datenschutzerklärung sagt seit 30.09.2026: Stripe-Kundendatensatz wird gelöscht, „soweit Sie ihn nicht auch für ein anderes Angebot nutzen“ (Entscheidung Hannes).

**Why:** Stripe-Konto ist mit Origin Labs geteilt; `customers.del` kündigt alle Abos des Kunden. Verwandt: [[schadenmelden24-commit-regeln]].

**How to apply:** Offene Folgeaufgabe als Todo `.planning/todos/pending/stripe-kundenpfade-geteilte-kunden.md` (Kundenportal, Stammdaten-Updates in create-checkout und stripe-customer-sync, Checkout-Wettlauf bei Löschung, force-sync prüfen); `verify` ist mit PR #260 erledigt.
