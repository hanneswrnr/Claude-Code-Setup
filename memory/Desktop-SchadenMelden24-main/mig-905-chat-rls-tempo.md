---
name: mig-905-chat-rls-tempo
description: "Mig 905 (Chat-RLS schneller über SECDEF-Hilfsfunktionen) LIVE seit 12.10.2026; PR #400 in release/4.0 gemergt; Speicher-Regeln aller Buckets laufen seit 16.10.2026 in eigener Sitzung"
metadata:
  node_type: memory
  type: project
  originSessionId: 507c6ba5-6347-4268-a695-4af6a8992a1e
  modified: 2026-10-16T11:28:42.299Z
---

Mig 905 `chat_rls_tempo`, Zweig `fix/v4-chat-rls-tempo` (Arbeitsordner `C:/Users/hanne/sm24-v4-chat-rls-tempo`), PR #400 gegen release/4.0, oberster Commit d8e3bfdcc mit `[vorschau]`. **LIVE seit 12.10.2026** (Freigabe Hannes, Selbstprüfung, Ledger 905, Nachprüfung, „905-TEST OK“). PR #400 nach Freigabe am 12.10.2026 in release/4.0 gemergt (3a4938e05, Baum identisch mit geprüftem Stand); Arbeitsordner und lokaler Zweig entfernt, Zweig auf GitHub bleibt.

- Sieben plpgsql-SECDEF-Hilfsfunktionen, sechs Regeln per ALTER POLICY; Rumpf von `ist_wartende_werkstatt()` als NOT EXISTS kopiert, Partei-Bedingungen vor der Sicht.
- Live nachgemessen: Chat-Tabellen unter 1 ms Planung (Anhang 1.695–2.363 → 0,57 ms). Speicher-Wege nur 203–287 ms (Hochladen) bzw. 201–277 ms (Lesen), weil die 60 Regeln auf storage.objects aller Buckets mitgeplant werden → Todo `2026-10-12-storage-regeln-tempo.md`.
- Nie Probelauf mit Sperren gegen live (sperrt storage.objects exklusiv, hat am 11./12.10. Auth/Realtime gestört).
- 12.10.2026 ab ~14:33 UTC: Vercel baute normal (Dashboard „Ready“), meldete aber weder Commit-Status noch Deployment an GitHub. Fehlt der GitHub-Status, im Vercel-Dashboard per Claude in Chrome nachsehen (vercel.com/hanneswrnrs-projects/schaden-melden24/deployments), nicht Hannes fragen.
- Speicher-Regeln aller Buckets: als eigene Sitzung angeboten (Chip „Speicher-Regeln aller Buckets schneller machen“), 44 Regeln mit Unterabfrage.
- Folgepunkte: `.planning/todos/pending/2026-10-12-chat-rls-tempo-folgepunkte.md` (Kopien bei RLS-Änderungen nachziehen, ungefilterte Zugriffe beobachten).

Verwandt: [[version-4-0-sammelzweig]]
