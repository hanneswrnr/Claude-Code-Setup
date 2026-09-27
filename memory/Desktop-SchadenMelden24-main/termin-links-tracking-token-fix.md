---
name: termin-links-tracking-token-fix
description: "Sicherheitslücke Termin-Links geschlossen: Branch fix/termin-links-ohne-tracking (Commit 6a4c071f) gepusht am 20.09.2026, wartet auf PO-Freigabe für main"
metadata: 
  node_type: memory
  type: project
  originSessionId: 476c1c44-1c51-48e2-977f-c23ed6558865
  modified: 2026-09-20T18:53:34.253Z
---

Sicherheitsbefund vom 19.09.2026 (Tracking-Token öffnete die Kunden-Termin-API) ist behoben auf dem Branch `fix/termin-links-ohne-tracking`, Commit `6a4c071f`, gepusht am 20.09.2026. **Merge nach main wartet auf Hannes' Freigabe** — damit ist der offene Punkt aus [[nutzerfuehrung-gesamtplanung]] erledigt bis auf die Freigabe.

Inhalt: Rückfall auf `tracking_tokens` in `validateKundenToken` entfernt (wörtlich aus `47afa72a` des Termin-Zweigs, damit der Merge konfliktfrei bleibt), `app/api/tracking/search` samt Test gelöscht, verwaiste `lib/tracking/find-eigenauftrag.ts` gelöscht, totes Rate-Limit aus `middleware.ts`.

Nicht-offensichtliche Fakten für Folgearbeiten:
- `tracking_tokens` hat in Produktion 0 Zeilen (20.09.2026 geprüft) — kein Alt-Link bricht.
- `increment_tracking_token_attempts` und `tracking_tokens.access_attempts`/`locked_until` haben seitdem keinen Aufrufer mehr: toter DB-Code, Aufräum-Kandidat für Bereich 08.
- Der zweite Fix aus `47afa72a` (Mandanten-Scope für `checkIdempotency`) wurde bewusst **nicht** übernommen und kommt mit `feat/termin-vereinfachung`.
- Das Auftragssystem braucht keinen Ersatz für die gelöschte Selbstbedienungs-Suche: die Werkstatt verschickt den Link über `/api/kunde/auto-send-portal`. Siehe [[auftragssystem-konzept]].

Doku: `wiki/09-Operations/Security-Audits/2026-09-19-termin-links-tracking-token.md` und `wiki/05-Anti-Patterns/Rueckfall-Auf-Alte-Token-Arten.md`.
