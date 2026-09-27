---
name: ki-launch-frist-avv
description: KI-Launch von feat/ai-features hängt an der Vierwochenfrist der AVV-Mitteilung (ab 18.08.2026), gemessen am 13.09.2026 fehlen 26 Kenntnisnahmen
metadata:
  type: project
---

Der Merge von `feat/ai-features` nach `main` darf erst erfolgen, wenn für jeden Auftraggeber vier Wochen seit seiner frühesten Kenntnisnahme der AVV-Mitteilung (`agb_zustimmungen`, dokument='av-vertrag', version>='2026-08-18') vergangen sind. Gemessen 13.09.2026: 19 Kenntnisnahmen (früheste Frist endet 16.09., späteste 07.10.2026), 26 Konten ohne Kenntnisnahme (22 Versicherung, 2 Werkstatt, 2 Verbund). Alle Branch-Migrationen 586–598 sind auf Produktion eingespielt. Reihenfolge danach: Runbook `wiki/09-Operations/Runbooks/KI-Scharfschaltung.md`.

**Why:** § 12 Abs. 4 des eigenen AV-Vertrags; ein früherer Merge wäre eine Vertragsänderung ohne Ankündigung.

**How to apply:** Vor jedem Merge-Vorschlag die SQL aus `wiki/09-Operations/DSGVO/Ankuendigung-Unterauftragsverarbeiter-OpenAI.md` gegen Prod laufen lassen; Nachzügler anschreiben ist Aufgabe des Betreibers. Siehe [[repo-ohne-git-nach-neuaufsetzung]].
