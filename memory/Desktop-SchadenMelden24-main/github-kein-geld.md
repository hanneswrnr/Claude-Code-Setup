---
name: github-kein-geld
description: Hannes gibt für GitHub kein Geld aus; GitHub-Actions-Prüfung no-mobile-app startet wegen Abrechnung nicht
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a927aacf-dd52-44d1-b49d-540b0f37218d
  modified: 2026-09-18T23:46:47.620Z
---

Hannes gibt für GitHub kein Geld aus (ausdrückliche Ansage 19.09.2026). Nie vorschlagen, bei GitHub zu zahlen, ein Ausgabenlimit zu erhöhen oder einen kostenpflichtigen Plan zu buchen.

**Why:** Die GitHub-Actions-Prüfung „no-mobile-app“ (`.github/workflows/no-mobile-app.yml`) startet seit mindestens 18.09.2026 nicht mehr, auch auf `main`. GitHub nennt als Grund ein Abrechnungsproblem des Kontos. Ich hatte Hannes das als Aufgabe gegeben; er lehnt das ab.

**How to apply:** Ein rotes Kreuz bei „no-mobile-app“ ist kein Code-Fehler. Vor einem Merge nach `main` den Schutz von Hand nachstellen: `git ls-tree -r HEAD --name-only` darf nichts unter `Mobile_Schadenmelden24/` und keine `V2_MOBILE.md` enthalten. Seit 19.09.2026 läuft derselbe Schutz kostenlos als `prebuild` vor `npm run build` (`Web_Schadenmelden24/scripts/no-mobile-app-guard.ts`, auf Vercel nachgewiesen) und zusätzlich als Git-Hook unter `.githooks`; maßgeblich ist der Vercel-Build, nicht das rote GitHub-Kreuz. Siehe auch [[schadenmelden24-commit-regeln]].
