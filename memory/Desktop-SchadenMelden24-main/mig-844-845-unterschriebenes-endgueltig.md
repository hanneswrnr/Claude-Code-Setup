---
name: mig-844-845-unterschriebenes-endgueltig
description: "ADR 0032 (30.09.2026, von Hannes an Claude delegiert): Annahmeprotokoll nach Abschluss endgültig, Rechtsdokumente nur vom Server; Mig 844/845 LIVE seit 01.10.2026, PR #275 gemergt (49f22eef), Doku-PR #276 gemergt"
metadata:
  node_type: memory
  type: project
  originSessionId: 67a02df8-5536-4b42-aa9b-c58835a2f55f
  modified: 2026-09-30T22:56:43.238Z
---

Stand 01.10.2026: Hannes hat die zwei offenen Produktfragen an Claude delegiert („Entscheide du beide Produktfragen“). Entscheidung ADR 0032 (`wiki/07-Decisions/0032-Unterschriebenes-bleibt-unveraendert.md`):
- Annahmeprotokoll: Unterschrift und Abschluss sind ein Schritt; Abschluss ohne Unterschrift nur mit `ohne_unterschrift: true` nach Rückfrage; danach unveränderlich auch für service_role; Löschen nur mit dem Auftrag; Pfadregel P5 (Unterschrift/PDF genau eine Datei im Auftragsordner).
- Rechtsdokumente: Browser nur lesen; Text, Hinweis (Spalte `hinweis`) und PDF nur vom Server; PNG-Unterschrift komplett geprüft und neu gepackt (Entpack-Bomben); unterschrieben endgültig.

LIVE seit 01.10.2026 (Freigabe Hannes): Spalte hinweis, PR #275 gemergt (49f22eef, Live-Build ok), Mig 844 und 845 eingespielt, „844-TEST OK“, „845-TEST OK“, danach „830-TEST OK“ und 843-Kernprüfungen OK. Doku-PR #276 gemergt (ce607dbf, Live-Build richtig übersprungen). Container 844: 260/0, 845: 165/0; vitest 15 353 grün; drei Prüfrunden ohne offene Befunde. Nebenbei behoben: Unterschreiben im Annahmeprotokoll scheiterte an der CSP (fetch auf data:), Kundenportal löschte Datei vor Zeile.

**Why:** Belege, die sich nach der Unterschrift ändern lassen, beweisen nichts; live gab es beim Entscheiden nur ein leeres Entwurfsprotokoll und kein Rechtsdokument.

**How to apply:** Rückweg: erst DB (rueckweg-845, rueckweg-844), dann App; 844 vor 843 zurücknehmen. Nicht wieder „Wiederöffnen“ abgeschlossener Protokolle einbauen; Rechtsdokumente nur über Server-Routen schreiben; nie `fetch(dataUrl)` im Browser (CSP connect-src ohne data:, Helfer `lib/upload/data-url.ts`). Verwandt: [[mig-832-835-folgepunkte-annahme-lager-verbund]], [[schadenmelden24-commit-regeln]].
