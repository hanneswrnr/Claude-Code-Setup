---
name: branding-browser-schmal-pr-315
description: "Branding geht nur als 13-Felder-Ausschnitt an den Browser (lib/branding/branding-browser.ts); PR #315 gemergt 03.10.2026 (19f126867); DB-Seite (Mitglieder lesen alle Spalten per RLS) offen"
metadata:
  node_type: memory
  type: project
  originSessionId: 34e7732a-7130-4ba1-b01e-4d8e47e63452
  modified: 2026-10-03T16:37:50.705Z
---

PR hanneswrnr/SchadenMelden24#315 (Zweig `fix/branding-browser-schmal`, Worktree youthful-rubin-f0eddf), angelegt und gemergt 03.10.2026, ohne Migration. Erledigt Grenze 3 aus dem Mig-867-Bericht: `resolveBranding`/`resolveBrandingForSlug` gaben per `select('*')` die ganze `werkstatt_gruppen`-Zeile (USt-ID, Kontaktdaten, Service-Level) an `BrandingProvider` — betroffen waren auch alle Mitglieds-Werkstätten und die Admin-Galerie, nicht nur HQ. Jetzt `BrandingGruppe` = 13 Felder mit Leser, Abfrage nur Branding-Spalten, Abfragefehler per logger.warn.

**Why:** Datensparsamkeit; Darstellung per Bildvergleich vorher/nachher als gleich belegt.

**How to apply:** Gemergt 03.10.2026 nach Freigabe von Hannes (Merge 19f126867). Ein neuer Leser eines `gruppe.*`-Feldes braucht Eintrag in `BRANDING_GRUPPE_FELDER` (tsc meldet es). Offener Folgepunkt (Migration + Entscheidung): RLS `gruppen_member_select_own` lässt Mitglieder alle Spalten direkt lesen; die App braucht von Mitgliedern nur noch Branding-Spalten. Verwandt: [[mig-867-hq-kontext-ohne-ausnahme]], [[mig-775-gruppen-angemeldete-spaltenrechte]].
