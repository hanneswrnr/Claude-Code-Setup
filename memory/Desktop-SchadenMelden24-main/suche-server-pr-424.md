---
name: suche-server-pr-424
description: "Globale Suche (Lupe/Strg+K) über GET /api/suche mit RLS, PR #424 in sammel/verbesserungen GEMERGT 17.10.2026 (21f65d8f8); offen Werkstätten für Agentur (Migration 920–924 mit Freigabe)"
metadata:
  node_type: memory
  type: project
  originSessionId: 83f41a1d-c3c4-4afc-9804-39df1cb308a9
  modified: 2026-10-17T13:54:00.486Z
---

Chat 6 „Suche“ der Welle 2 (17.10.2026): Zweig `feat/v4-suche`, PR #424 in `sammel/verbesserungen` GEMERGT 17.10.2026 (21f65d8f8, nie main). Server-Suche `GET /api/suche?q=` mit dem Konto des Nutzers (RLS), keine Migration, Drossel 60/60 s je Konto. Doku: `wiki/03-Features/Suche.md`, `wiki/06-Reference/API-Routes/suche.md`, `feature-vault/08-Querschnitt/Schnellsuche.md`.

**Why:** Suche fand vorher nur Teile und lief im Browser; die Verbund-Zentrale lud bis 500 Mitglieder vorab.

**How to apply:**
- Agentur/Vertreter finden keine Werkstätten: `werkstaetten_select_policy` (Mig 151) gibt Agenturen per RLS nichts. Lösung nur per SECURITY-DEFINER-Funktion = Migration im Bereich 920–924, braucht Hannes' Freigabe.
- Sentry: `lib/sentry/scrub.ts` schwärzt `q`, `or`/`and` und Such-Operator-Werte (`ilike.` …) in Adressen, `query_string`, `http.query`/`url.query`; neue Suchquellen mit `.or(oderIlike(...))` sind damit gedeckt. Nie `dataCollection` in Sentry setzen (schaltet sonst alles Sammeln ein).
- `DashboardHeader.tsx` gehört Chat 7.
- Verwandt: [[version-4-0-sammelzweig]]
