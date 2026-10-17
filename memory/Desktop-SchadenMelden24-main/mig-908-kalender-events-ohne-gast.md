---
name: mig-908-kalender-events-ohne-gast
description: "Mig 908 (werkstatt_kalender_events ohne anon, Regeln TO authenticated) live seit 16.10.2026; PR #410 GEMERGT 16.10.2026 (ca53687d4)"
metadata:
  node_type: memory
  type: project
  originSessionId: bd184268-7cb1-4700-b7db-ed814f09318d
  modified: 2026-10-16T20:33:04.587Z
---

Mig 908 `kalender_events_ohne_gast` ist LIVE seit 16.10.2026 (Freigabe Hannes, Prüfskript live „908-TEST OK“).
Zweig `fix/kalender-events-anon-rechte`, PR #410 gemergt 16.10.2026 (ca53687d4), Live-Build grün.
Rückweg 908 vor den Rückwegen 748 und 777. Neue Regeln auf `werkstatt_kalender_events` nur `TO authenticated`
(Wächter `lib/kalender/__tests__/migration-908-…test.ts`).

**Why:** Nebenbefund aus [[mig-907-speicher-regeln-tempo-2]]: anon hatte CRUD, Schutz hing allein an RLS-Ausdruck.
**How to apply:** Offen sind `scripts/pen-test-hq.test.ts` (braucht Test-Zugänge) und gleichartige Tabellen mit Regeln
`TO public` (notification_queue, werkstatt_reminders, werkstatt_tagesnotizen, versicherung_kalender_events).
