---
name: SchadenMelden24 Install Quirks
description: Mobile_Schadenmelden24 needs --legacy-peer-deps; project sometimes shipped without .git folder
type: project
originSessionId: 2c060bab-5db5-4554-aa09-2c7963e8e9c6
---
`Mobile_Schadenmelden24` muss mit `npm install --legacy-peer-deps` installiert werden. Sonst schlägt die Installation mit ERESOLVE fehl.

**Why:** `@capacitor-community/barcode-scanner@4.0.1` (in package.json) verlangt peer `@capacitor/core@^5.0.0`, aber das Projekt pinnt `@capacitor/core@^6.0.0`. Der eingecheckte `package-lock.json` wurde mit `--legacy-peer-deps` gebaut. Es gibt **kein** `.npmrc` und **kein** CI-Flag, das den Workaround dokumentiert.

**How to apply:** Bei jedem `npm install` in Mobile_Schadenmelden24 das Flag `--legacy-peer-deps` mitgeben. Auch bei `npm ci`. Web_Schadenmelden24 ist davon nicht betroffen — dort funktioniert `npm install` ohne Flag. Bei Vorschlag eines Fixes: `.npmrc` mit `legacy-peer-deps=true` im Mobile-Ordner anlegen wäre die saubere Lösung.

---

Außerdem: Der lokale Projektordner kommt manchmal als ZIP-Extraktion ohne `.git`-Verzeichnis. GitHub-Remote ist `https://github.com/hanneswrnr/SchadenMelden24.git` (privat, aber via cached credentials erreichbar). Bei Sync-Checks ohne `.git`: `git init` + `git remote add origin <url>` + `git fetch` + `git read-tree origin/main` + `git -c core.autocrlf=false diff origin/main` für korrekten Vergleich (ohne autocrlf=false zeigt git fälschlich riesige Diffs durch CRLF-Konvertierung).
