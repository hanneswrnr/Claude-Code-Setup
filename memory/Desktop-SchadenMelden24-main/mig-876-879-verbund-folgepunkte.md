---
name: mig-876-879-verbund-folgepunkte
description: "Mig 876–880 LIVE seit 04.10.2026 (PR #321–#325 gemergt): Verbund-Folgepunkte nach 775/872 erledigt"
metadata:
  node_type: memory
  type: project
  originSessionId: 923fa7dd-4738-46a9-8312-a86297b91496
  modified: 2026-10-04T12:03:03.257Z
---

**Stand 04.10.2026: 876, 877, 878, 879 LIVE** (Freigabe Hannes: „Migration 876, 877, 878 und 879 einspielen und PR #321, #322, #323 und #324 mergen“). Ledger 876–879, Prüfskripte live je „NNN-TEST OK“. Merges: #321 b3144cb22, #322 51cd6dafa, #323 9a8c2ae37, #324 c6387495f (879 vor dem App-Teil eingespielt).

| Mig | Inhalt |
|---|---|
| 876 | `_user_ist_gruppen_mitglied(uuid)` gelöscht; rueckweg-872 legt sie bei Bedarf selbst an (md5 06eca71b…) |
| 877 | Regel `offizielle_standorte_public_select` weg, `oeffentliche_offizielle_standorte()` (10 Spalten, nur aktive+gelistete) |
| 878 | `ist_branding_sichtbar` echte Antwort nur eigene Werkstatt, HQ mit aal2, Server (auch über Sitzungsrolle); Rückweg 767 erst nach Rückweg 878 |
| 879 | `gewuenschte_gruppe_eigene_anfrage()` + App `ladeGewuenschteGruppe`; Rückweg: erst App, dann rueckweg-879 |

**Mig 880 (Zweig fix/offizielle-standorte-mitglieder-weg, Worktree C:\Users\hanne\sm24-standorte-mitglieder):** streicht `offizielle_standorte_werkstatt_select_own_group` (Entscheidung an Claude delegiert, Muster 872). LIVE seit 04.10.2026 (Freigabe „Migration 880 einspielen und PR #325 mergen“), verify-880/877/775 live OK, PR #325 gemergt (e192ba10b). Live bleiben 4 Regeln auf werkstatt_gruppen_offizielle_standorte (HQ, Plattform-Admin, 2 RESTRICTIVE).

**Entscheidungen Hannes 04.10.2026:** Versicherungen dürfen sehen, zu welchem Verbund eine Werkstatt gehört (bleibt so). Todo `verbund-folgebefunde-nach-mig-775.md` → completed; neues Todo `verbund-folgepunkte-nach-mig-876-879.md` (Texte, Suchpfad-Härtung, verify-877 bei echten Standorten).

**How to apply:** Gestapelte PRs gegen main in Reihenfolge mergen, vor jedem Merge main in den nächsten Zweig holen; Prüf-Agenten haben keinen Live-Zugang, Live-Punkte prüft root. Verwandt: [[mig-871-872-mein-verbund]], [[mig-775-gruppen-angemeldete-spaltenrechte]].

**Nachtrag 09.10.2026:** Todo-Punkte 3, 4, 5, 9 (Texte) mit PR #332 gemergt; Punkte 7, 8 mit Mig 883 (Suchpfad von 113 SECURITY-DEFINER-Funktionen ohne pg_catalog, Wächter ab 884) live seit 09.10.2026, PR #334. Offen: Punkt 6 (verify-877, sobald echte offizielle Standorte existieren) und Punkt 10 (24 SECURITY-INVOKER-Funktionen mit demselben Muster). Lehre: Subagenten nehmen eine weitergereichte Freigabe für Prod-Schreiben nicht an — Einspielen macht root selbst; Monitor-Aufgaben von Subagenten bleiben sonst als „läuft“ stehen.
