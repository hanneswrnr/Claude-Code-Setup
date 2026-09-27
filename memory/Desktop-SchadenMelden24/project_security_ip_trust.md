---
name: project-security-ip-trust
description: SchadenMelden24 — Client-IP nur über lib/api/get-client-ip.ts (spoof-sicher)
metadata: 
  node_type: memory
  type: project
  originSessionId: 68291127-dd49-4ba7-aca2-2f4e8463e433
---

Für Rate-Limiting, Audit-Logs, IP-Whitelists und Brute-Force-Sperren ausschließlich `getClientIp()` aus `Web_Schadenmelden24/lib/api/get-client-ip.ts` nutzen.

**Why:** `request.headers.get('x-forwarded-for').split(',')[0]` ist auf Vercel UNSICHER — das erste Element ist der vom Client setzbare Wert. Vercel hängt seine Edge-IP nur an, überschreibt nicht. Ein Angreifer rotiert `X-Forwarded-For: 1.2.3.4` und umgeht jedes IP-basierte Rate-Limit. Pen-Test 2026-05-12 hat das als High-Severity-Bypass identifiziert.

**How to apply:** Der Helper liest die Quellen in dieser Reihenfolge: `x-vercel-forwarded-for` → `x-real-ip` → *letztes* Element von `x-forwarded-for`. Nur diese Werte sind plattform-gesetzt und vertrauenswürdig. Niemals neue inline-IP-Parsing-Funktionen in API-Routes schreiben — immer importieren. Bei neuen Routen mit Rate-Limit/Audit-Bezug zuerst sicherstellen, dass der Helper genutzt wird.

Bezug: [[project-security-anon-rls]]
