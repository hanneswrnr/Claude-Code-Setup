---
name: standort-loeschen-hauptstandort-atomar-pr-227
description: "PR 227 (fix/standort-loeschen-hauptstandort-atomar) macht die Hauptstandort-Regel in DELETE /api/werkstatt/standorte atomar; ohne Migration, gemergt 29.09.2026 (be4ab9d5), LIVE seit 22:54 mit Redeploy von 5145e59f ohne Build-Cache"
metadata:
  node_type: memory
  type: project
  originSessionId: 192c9f59-8577-421f-83f2-98b191ee4527
  modified: 2026-09-29T20:58:05.076Z
---

Am 29.09.2026 gebaut und gepusht: PR #227 (Zweig fix/standort-loeschen-hauptstandort-atomar, Commit fb4a1996) schließt den Wettlauf zwischen Hauptstandort umschalten (RPC werkstatt_hauptstandort_setzen, Mig 786) und Standort löschen. Keine Migration, nur App-Code, Tests und Doku. Unabhängig geprüft (angenommen).

**Why:** Folgebefund aus den Prüfungen zu Mig 786 ([[nebenbefunde-768-mig-776-777]], [[mig-786-standorte-folgebefunde]]).

**How to apply:** Mit Freigabe von Hannes am 29.09.2026 gemergt (be4ab9d5; Vorschau-Bau war im Vercel-Dashboard abgebrochen worden, geprüft per lokalem Produktions-Build und voller Testsuite). Offene Grenzen, die nur per Datenbankfunktion lösbar wären: einziger Standort gelöscht, während POST einen zweiten anlegt; Rückroll-DELETE im POST ohne Bedingung; das Fenster lädt die Liste bei 409 nicht neu.
