---
name: menudeck-setup-windows
description: "Wie der MenuDeck-Arbeitsrechner (Windows 11 Home) aufgesetzt ist -- vier Schritte, die die README nicht nennt"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4447cc85-a23c-4716-98f5-4a5845f2d0dc
  modified: 2026-08-03T22:28:04.198Z
---

MenuDeck laeuft auf einem Windows-11-**Home**-Rechner. Vier Setup-Schritte waren noetig, die
`README.md` (Abschnitt "Lokale Entwicklung") nicht nennt; am 2026-08-04 erstmals von null
durchgefahren:

1. **WSL2 musste nachinstalliert werden** (`wsl --install --no-distribution`, erhoeht). Auf Home
   gibt es kein Hyper-V-Backend fuer Docker Desktop -- ohne WSL2 startet die Engine nie, und die
   Anwendung meldet das nicht, sie hat einfach keinen Daemon.
2. **Docker Desktop** ueber `winget install -e --id Docker.DockerDesktop`. Kein Neustart noetig,
   obwohl das CBS-Reboot-Flag gesetzt wurde.
3. **Supabase CLI 2.107.0** (die von `.github/workflows/ci.yml` gepinnte Version) liegt unter
   `C:\Users\hanne\bin\`, im User-PATH. Es gibt auf Windows **keinen** winget-Weg, kein Scoop
   vorausgesetzt, und globales `npm i -g supabase` unterstuetzt Supabase nicht mehr -- installiert
   aus dem Release-Archiv von `supabase/cli`. **Die CLI besteht aus ZWEI Binaerdateien**
   (`supabase.exe` + `supabase-go.exe`), die im selben Verzeichnis liegen muessen. `supabase
   --version` antwortet auch ohne den Go-Teil und taugt deshalb NICHT als Installationspruefung --
   `supabase projects --help` schon.
4. **`npx playwright install chromium`.** `npm ci` laedt die Browser nicht nach. Fehlen sie oder
   passt die Build-Nummer nicht, faellt **jeder** der 78 E2E-Specs nach ~4 ms beim Browserstart --
   ein Bild, das wie ein kaputtes Projekt aussieht und keines ist.

**Node ist v24.11.1, die CI baut auf 22** (`package.json` verlangt nur `>=20`). Gemessen kein
Problem: `npm ci`, `next build`, `typecheck` und die volle Vitest-Suite (96 Dateien / 1368 Tests)
laufen darauf gruen.

Siehe [[menudeck-offene-setup-korrektur]].
