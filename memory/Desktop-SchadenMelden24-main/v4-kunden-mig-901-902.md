---
name: v4-kunden-mig-901-902
description: Version 4.0 Kunden automatisch + Dubletten (Chat 3): Mig 901 live seit 11.10.2026 (Trigger aus), 902 erst mit Merge release/4.0 nach main; PR #392 gegen release/4.0
metadata:
  type: project
  modified: 2026-10-12T00:38:13.026Z
---

Zweig `feat/v4-kunden` (Worktree `.claude/worktrees/adoring-cannon-bcd6d4`), PR #392 gegen `release/4.0`.
Mig 901 (Struktur: `kunden.firma`, `kunden_vermittelte_auftraege`, `kunden_dubletten_hinweise`, Funktionen nur service_role) ist live seit 11.10.2026, Ledger 901, verify-901 OK; Trigger `zz_claim_kunde_zuordnen` auf `claims` bewusst abgeschaltet (tgenabled D).
Mig 902 (Altbestand nachziehen, ca. 172 Karten, Trigger an) erst zusammen mit dem Merge von release/4.0 nach main; Todo `.planning/todos/pending/mig-902-kunden-aus-auftraegen-mit-version-4-0.md` (fällig 18.10.2026). Vorprüfung von 902 verlangt 901 unverändert.

Klick-Durchgang 11.10.2026 (Vorschau, Testversicherung + Testwerkstatt „Musterwerkstatt“): mit Freigabe `kunde_aus_auftrag_zuordnen` von Hand für GS-2026-0690/0691 ausgeführt → 2 Zeilen in `kunden_vermittelte_auftraege` (Testwerkstatt). **Die Vorprüfung von 902 bricht ab, solange dort Zeilen mit kunde_id stehen** („Zuordnungen oder Hinweise existieren schon“): die 2 Testzeilen wurden am 11.10.2026 mit Freigabe gelöscht (Tabellen wieder leer, Trigger D); Testkarten bleiben. Bei weiteren Handtests danach wieder aufräumen.

12.10.2026: „Firma“-Markierung überall einheitlich blau über `components/shared/FirmaPille` (Auftragslisten Werkstatt + Versicherung/Vermittler, Kopf der KundeKarte), PR #397 in release/4.0 gemergt (d745ffe71). Hannes will Firma/Privat-Markierungen in allen Rollen gleich; neue Stellen nur mit `FirmaPille`.

**Why:** Hannes-Entscheidung 11.10.2026 (`.planning/version-4-0/kunden/ENTSCHEIDUNGEN.md`): heutige Live-App soll keine Karten ohne neue Oberfläche zeigen.
**How to apply:** Vor jeder Migration, die `claims`-Trigger, `loeschfristen_termine`, `export_user_data` oder `mask_audit_pii_jsonb` ändert, Prüfsummen aus 901 beachten. Große SQL-Dateien im SQL-Editor: Datei per Set-Clipboard, in Hannes' Chrome per Claude in Chrome einfügen, monaco setEOL(0), SHA-256 prüfen, dann Run (CRLF bricht die Selbstprüfung). Siehe [[welle-10-10-pr-359-370]], [[version-4-0-sammelzweig]].
