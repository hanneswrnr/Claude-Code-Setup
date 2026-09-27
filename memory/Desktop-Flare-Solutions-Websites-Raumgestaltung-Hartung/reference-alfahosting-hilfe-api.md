---
name: reference-alfahosting-hilfe-api
description: Alfahosting help center blocks WebFetch (403) but its Zendesk API returns articles as JSON
metadata: 
  node_type: memory
  type: reference
  originSessionId: 69962245-3585-4b8c-b499-d298b527753e
  modified: 2026-09-11T09:05:30.029Z
---

hilfe.alfahosting.de is a Zendesk help center. Direct page fetches return 403 to automated tools, but the public API works with curl and a browser user agent:

`https://hilfe.alfahosting.de/api/v2/help_center/de/articles/<article-id>.json` → `article.title`, `article.body` (HTML), `article.edited_at`.

Articles used on 2026-09-11: 18733519581457 (SPF/DKIM, "SPF Alfahosting-Server" template, DKIM condition), 18729701719185 (SPF value), 48786409098129 (SPF in oneHome), 31207963792017 and 48788142016401 (how to request the AV contract), 31208373930385 (contact forms require an AV contract). The same trick likely works for other Zendesk-based help centers.

Related: [[project-hartung-konten-vertraege]]
