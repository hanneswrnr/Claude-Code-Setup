---
name: project-security-anon-rls
description: SchadenMelden24 — kein anon-Direktzugriff auf Customer-Portal-Tabellen erlauben (Token-Enumeration-Vektor)
metadata: 
  node_type: memory
  type: project
  originSessionId: 68291127-dd49-4ba7-aca2-2f4e8463e433
---

Auf den Kundenportal-Tabellen (`kunde_tokens`, `tracking_tokens`, `claims`, `claim_messages`, `claim_attachments`, `werkstatt_auftraege`, `fahrzeuge`, `kunden`) darf NIEMALS wieder eine RLS-Policy `TO anon` mit `USING (...EXISTS (token aktiv...))` erstellt werden.

**Why:** Pen-Test 2026-05-12 hat aufgedeckt: Solche Policies erlauben dem public `NEXT_PUBLIC_SUPABASE_ANON_KEY` (= aus jedem Browser-Bundle extrahierbar) direkten REST-Zugriff auf alle Zeilen mit aktivem Token — inklusive der Token-Werte selbst (`kunde_tokens.token`, `tracking_tokens.token`). Damit kann sich ein Angreifer via `https://<proj>.supabase.co/rest/v1/kunde_tokens` alle aktiven Tokens listen lassen und jedes Kundenportal übernehmen. Migration 229 hat alle diese Policies entfernt.

**How to apply:** Kundenportal-/Tracking-Daten laufen ausschließlich über API-Routes (`/api/kunde/[token]/*`, `/api/tracking/[token]`) mit `SUPABASE_SERVICE_ROLE_KEY` nach Token-Validierung. Realtime-Push-Updates für anon sind nicht möglich — Polling übernimmt (`useKundePolling` ~5s, tracking-page 10s setInterval). Wenn neue Customer-Portal-Features Realtime brauchen, Broadcast-Channel mit token-spezifischem Channelname statt postgres_changes verwenden — niemals zurück zu anon-RLS auf Datentabellen.

Bezug: [[project-security-ip-trust]]
