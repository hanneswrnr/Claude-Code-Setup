---
name: werkstatt-freischaltung-mig-620
description: "Migration 620 (DB-Sperre für nicht freigeschaltete Werkstatt-Konten) liegt auf Branch fix/werkstatt-freischaltung-rls, Stand 19.09.2026 NICHT auf Prod und nicht gemerged; Freigabe des PO offen"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5fa7573b-b818-42e1-acac-ed571a64a66b
  modified: 2026-09-19T13:58:03.123Z
---

Stand 2026-09-19: Branch `fix/werkstatt-freischaltung-rls` (gepusht, 1 Commit) enthält Migration `620_wartende_werkstatt_db_sperre.sql`, API-Gate in vier `subscriptions/*`-Routen, NULL-Fix in LoginForm/DashboardContext, Tests (`supabase/tests/620/run.sh` mit Docker: 46 PASS; vitest) und Wiki (`wiki/05-Anti-Patterns/Freischaltung-nur-in-der-Oberflaeche.md`, Audit `wiki/09-Operations/Security-Audits/2026-09-19-…`). Migration ist **nicht** auf Prod eingespielt, Merge nach main offen — beides braucht die ausdrückliche Freigabe von Hannes.

**Why:** `is_verified` wurde nur in der Oberfläche geprüft; wartende Werkstatt-Konten konnten per JWT u. a. alle `versicherungen` inkl. IBAN lesen. Kein Vorfall (0 wartende Konten).

**How to apply:** Nach Merge von 620 muss jede Migration mit neuer RLS-Tabelle `SELECT public.wartende_werkstatt_sperre_anwenden();` aufrufen (vitest-Wächter prüft alle Nummern > 604). `get_user_werkstatt_id()` hat ab 620 einen neuen Body — nicht mit altem Stand überschreiben. `ist_wartende_werkstatt()` nie `authenticated` entziehen (steckt in jeder Policy). Einspielen in verkehrsarmer Zeit (lock_timeout 3 s, bricht sonst sauber ab). Offene Rest-Risiken stehen im Audit (validate_discount_code, Inline-SECDEF-RPCs, google-places). Im Worktree `distracted-gates-9eba7c` ist `Web_Schadenmelden24/node_modules` eine Junction auf den Hauptordner (npm ci scheitert an Lockfile-Drift @emnapi) — vor `git worktree remove` die Junction entfernen. Siehe [[prod-db-drift-feat-ai-features]], [[nutzerfuehrung-gesamtplanung]].

**Korrektur 20.09.2026 (lesend in der Prod-DB geprüft):** Migration 620 ist LIVE. Die Funktion
`public.wartende_werkstatt_sperre_anwenden()` existiert auf der Produktionsdatenbank (ihr eigener
Kommentar nennt Migration 620), und 194 `wartende_werkstatt_sperre`-Policies sind aktiv. Die
frühere Notiz „620 NICHT auf Prod" gilt nicht mehr. Folge: Jede neue Migration, die eine Tabelle
mit RLS anlegt, MUSS am Ende `SELECT public.wartende_werkstatt_sperre_anwenden();` aufrufen —
sonst fehlt die Sperre auf der neuen Tabelle. Nicht erneut einspielen.
