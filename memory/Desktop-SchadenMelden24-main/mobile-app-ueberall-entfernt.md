---
name: mobile-app-ueberall-entfernt
description: "Mobile-App (Mobile_Schadenmelden24/, V2_MOBILE.md) darf in KEINEM Branch existieren; am 19.09.2026 aus allen 46 Remote-Branches per Lösch-Commit entfernt"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 10a4f912-c6fb-4fc9-863d-dda4ecf791af
  modified: 2026-09-18T23:53:35.524Z
---

Der Nutzer will, dass die Mobile-App nirgends mehr existiert – nicht nur auf main, sondern in keinem Branch. Am 19.09.2026 wurde `Mobile_Schadenmelden24/` und `V2_MOBILE.md` aus allen 46 Remote-Branches per eigenem Commit („chore: Mobile-App endgueltig entfernt [skip ci]") entfernt; Nachprüfung: 0 Branches enthalten den Ordner.

**Why:** Der Nutzer hat es nach eigener Aussage „schon 100 mal gesagt"; alte Branches brachten den Ordner bei Merges mehrfach still zurück (siehe CLAUDE.md, ADR 0021).

**How to apply:** Nie etwas unter `Mobile_Schadenmelden24/` anlegen oder zurückmergen. Vor jedem Merge/Push prüfen: `git ls-tree -r HEAD --name-only` enthält nichts davon. Lokale Klone/Worktrees anderer Sitzungen können den alten Stand noch haben – nach `git fetch` neu aufsetzen. Die GitHub-Action „no-mobile-app" läuft wegen Abrechnungsproblem nicht; der Nutzer zahlt nichts für GitHub – das nicht vorschlagen.
