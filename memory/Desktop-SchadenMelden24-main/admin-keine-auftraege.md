---
name: admin-keine-auftraege
description: "Produktregel — der Plattform-Admin darf keine Aufträge (claims) sehen; UI entfernt am 16.09.2026, RLS-Lücke noch offen"
metadata: 
  node_type: memory
  type: project
  originSessionId: 10a4f912-c6fb-4fc9-863d-dda4ecf791af
  modified: 2026-09-16T16:05:54.471Z
---

Der Plattform-Admin darf keine Aufträge sehen (ADR-0014 Admin-Eindampfung, Mai 2026; vom Nutzer am 16.09.2026 bekräftigt). Am 16.09.2026 wurde auf dem Branch `feat/admin-auftraege-entfernen` (Commits aca3939d + 034c017c auf Basis von main 86f49e04, gepusht, noch nicht gemergt; Vercel-Preview vom Nutzer gewünscht) der tote Code unter `app/(dashboard)/admin/auftraege/` gelöscht, die Claims-Suche des Admins in `components/shared/CommandPalette.tsx` abgeschaltet und die letzten Links entfernt. Die Middleware-Sperrliste `BLOCKED_ADMIN_UI_PREFIXES` in `lib/admin/routes.ts` bleibt.

**Why:** Schadenakten enthalten Endkundendaten; der Admin braucht sie nicht. Die Vault-Seite stand fälschlich auf „aktiv“ und führte zu Arbeit an totem Code.

**How to apply:** Admin-Seiten nie um Auftragsdaten erweitern. Abgeschlossen am 16.09.2026: Branch per Fast-Forward nach main gemergt (main 069e7877, gepusht), Migration `604_admin_kein_auftragszugriff` per Supabase-MCP in Prod eingespielt (inkl. Teil B: Nebentabellen, audit_log, Storage-Buckets, Realtime-Kanal, alte Admin-RPCs ohne authenticated-EXECUTE). Der Functions-Eintrag `admin_account_auftrags_stats` in `database.types.ts` wurde manuell ergänzt; bei der nächsten Typgenerierung abgleichen. Admin-Papierkorb und `AssignClaimModal` sind gelöscht. Siehe [[schaden-melden-formular-bleibt]].
