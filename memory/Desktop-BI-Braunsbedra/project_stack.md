---
name: Next.js + Supabase (static export)
description: Reiner Next.js+Supabase-Stack. Static Export nach out/, die frühere PHP/MySQL-API in public/api/ und public/send-mail.php wurde entfernt.
type: project
originSessionId: d293811f-30e2-4e96-92c7-9fb78202c407
---
Projekt BI-Braunsbedra: Next.js 16 App Router mit `output: 'export'` (static export), Backend komplett auf Supabase (Auth, Postgres, Storage). Deployment liefert nur die statischen Assets aus `out/`; die Seite spricht zur Laufzeit ausschließlich mit Supabase.

Die früher vorhandene PHP/MySQL-Hostinger-API (`public/api/{auth,config,csrf,index,settings,upload}.php` + `public/send-mail.php` + `public/api/migrations/`) wurde komplett entfernt, inklusive CSRF-Token-Flow. Das Kontaktformular nutzt jetzt die Tabelle `contact_messages` (Migration `supabase/migrations/005_contact_messages.sql`) mit RLS: anon darf INSERT, authenticated darf SELECT/UPDATE, DELETE bewusst nicht policy'd.

**Why:** Architektur-Entscheidung im April 2026 — weg von Hostinger/PHP, alles auf Supabase. Es gibt aktuell keinen Mail-Versand mehr für neue Kontaktnachrichten, die landen nur in der DB.

**How to apply:** Bei Arbeit am Kontakt-Flow daran denken, dass Mail-Versand als nächstes ergänzt werden muss (z.B. Supabase Database Webhook → Edge Function → Resend/SendGrid). Beim Security-Audit reicht jetzt ein Blick auf Next + Supabase — keine Parallel-Stacks mehr. Bei Hosting-Wechsel: `.htaccess` ist Apache/LiteSpeed-spezifisch und wird auf Vercel/Netlify/etc. ignoriert; Security-Headers dort in der jeweiligen Hoster-Config neu setzen.
