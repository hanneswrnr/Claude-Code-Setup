---
name: einstellungen-umbau-pr-299
description: "Einstellungen aller Rollen nach Skizze 03 + Mein Konto + API-Zugang entfernt (PR #299, live); Bewertungen bereinigt (PR #300); Mig 862 Vertreter-Export live seit 03.10.2026, App-Teil PR #302"
metadata:
  node_type: memory
  type: project
  originSessionId: 3f856479-fba4-4da8-94e4-20cd09696bec
  modified: 2026-10-02T23:56:52.745Z
---

Umbau der Einstellungen aller Rollen (Nutzerführung 03), PR #299 GEMERGT und LIVE seit 03.10.2026 (45baee501). Bewertungsseite bereinigt, PR #300 GEMERGT 03.10.2026 (cd1c32fcf).

Mig 862 (Vertreter-Datenexport ohne Gutschrift-Köpfe der Agentur) LIVE seit 03.10.2026 nach Freigabe: Probelauf, Ledger 862, Nachprüfung, verify-862 und verify-828 OK. App-Teil (Export-Knopf für Vertreter wieder an, 403 in POST /api/dsgvo/export weg, Formprüfung im Download `lib/dsgvo/vertreter-export-pruefung.ts`) in PR #302 GEMERGT 03.10.2026 (469b32f2c); Worktree und lokaler Zweig aufgeräumt.

- PO-Entscheidung 02.10.2026: „API-Zugang“ in allen Rollen ersatzlos weg (auch nicht als „Anbindung anderer Software“).
- Rahmen `components/einstellungen/EinstellungenRahmen.tsx`, Bereiche `bereiche.ts`; Mein Konto `components/konto/MeinKonto*.tsx`; `roleKontoPath` in `lib/roles.ts`.
- Abmelden: lokal (nur dieses Gerät), Admin global; eigener Knopf „Auf allen Geräten abmelden“.
- Firma-Formulare schreiben `profiles.display_name` nicht mehr.
- Verbund-Einstellungen nur per `?bereich=` (2FA-Ausnahmepfad hat Präfix-Wirkung).
- Offen: Todo `.planning/todos/pending/verbund-export-zweite-stufe.md` (zweite Anmelde-Stufe für den Export der Verbund-Zentrale, eigene Migration, Freigabe nötig). Produktfrage nur gemeldet: `attribuierte_claims` zeigt Vertretern Provision und Reparaturkosten (laut RLS ohnehin erlaubt).
- Design-Abgleich aller Seiten: `.planning/ui-modernisierung/DESIGN-ABGLEICH-2026-10-02.md` (115 von 143 Seiten noch alter Stil; 8 Pakete).

**Why:** Nächste Sitzungen sollen Stand, Entscheidungen und Folgeaufgaben kennen, ohne den Verlauf zu lesen.
**How to apply:** Neue Fassungen von `export_user_data` müssen den Vertreter-Zweig gekürzt lassen (Wächter migration-862, verify-828 kennt 862 als Nachfolger). Folgepakete aus dem Design-Abgleich nur nach Bestätigung der jeweiligen Skizze.
