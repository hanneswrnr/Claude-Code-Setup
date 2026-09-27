---
name: project-hartung-konten-vertraege
description: "Account/contract/mailbox structure for the Hartung site (Vercel in Origin Labs Pro account, Alfahosting on Norman, second mailbox formular@ as sender) as decided by the user on 2026-09-10"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69962245-3585-4b8c-b499-d298b527753e
  modified: 2026-09-10T11:49:28.625Z
---

Facts and decisions from the user on 2026-09-10 (the repo docs said otherwise before and must be corrected):

- The Vercel project runs in Hannes's **Origin Labs Vercel account, plan Pro**. Vercel's customer is Origin Labs; for the GDPR structure Norman (controller) needs an AVV with Origin Labs (processor), Vercel is sub-processor.
- The **Alfahosting contract is in Norman's name**. Domain and e-mail stay at Alfahosting; hosting/deployment via Vercel.
- **`web144p1` is the login for the whole Alfahosting online portal**, not the mailbox name (docs/KONTAKTFORMULAR.md and src/versand.ts claimed it was the mailbox).
- Contact form mailbox — **decision changed the same day**: first "info@ sends to itself", then (final) **a second mailbox is created in the Alfahosting portal** so Norman's info@ password is not needed. The assistant chose the name: sender **formular@raumgestaltung-hartung.de** (own mailbox, forwarding to info@ recommended), recipient stays **info@raumgestaltung-hartung.de**. Hannes creates the mailbox himself and sets its password only in Vercel. Created the same day in Confixx: POP3 mailbox **`web144p2`** (comment "Kontaktformular") → this is `SMTP_USER`; address formular@ assigned to web144p2 (+ forwarding to info@ recommended). The pNN naming suggests web144p1 is the existing info@ mailbox after all — verify before writing docs.
- Wanted on both legal pages (/impressum, /datenschutz): an "Umsetzung der Website" credit block with the Origin Labs logo and address (see [[user-hannes-origin-labs]]).
- Privacy-policy "Stand": the assistant chose "September 2026" (month, because contract placeholders get filled this month).

**Why:** These facts decide who signs which data-processing contract, which env values the form needs, and what the privacy policy may truthfully say.

**How to apply:** Word legal texts, docs and env instructions accordingly (ANFRAGE_ABSENDER = formular@, ANFRAGE_EMPFAENGER = info@; do NOT make the recipient fall back to the sender). Never remove a `[[…]]` contract placeholder until the user confirms the contract is actually concluded/signed.
