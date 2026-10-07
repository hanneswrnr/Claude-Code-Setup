# Claude-Code-Setup (Origin Labs)

Versioniertes globales Claude-Code-Setup von Origin Labs. Hier wird das Setup gesichert und auf andere Geräte übertragen.

## Was drin ist

| Ordner oder Datei | Inhalt |
|---|---|
| `claude/CLAUDE.md` | Globale Regeln: DevOS, Grundregeln, Web-Projekte mit HTML/CSS und TypeScript, autonome Orchestrierung, Lernloop, Loop Engineering |
| `claude/settings.json` | Hooks des Lernloops, Nachfrage- und Sperr-Regeln, Plugins, Marktplätze, Modell-Setup (siehe unten), Statusleiste |
| `claude/statusline.py` | Statusleiste im Terminal: Modell, Effort, Kontext, Cache-Trefferquote und Abo-Limits |
| `claude/agents/` | 324 Agents: 279 Agency Agents (Beschreibungen auf 160 Zeichen gekürzt), 12 DevOS-Rollen mit festen Modellstufen und 33 GSD-Agents |
| `claude/skills/` | 82 Skills: DevOS-Skills, `learn`, `reflect`, `recall`, `loop-engineering`, `sichtpruefung-hinter-login` und 67 GSD-Skills (deren Motor kommt aus npm, siehe Schritt 6) |
| `claude/learning/` | Lernloop mit Prüf-Gate, Tests und allen gelernten Lektionen (`lessons.jsonl`: aktive, auf Freigabe wartende und archivierte) |
| `memory/` | Automatisches Gedächtnis aller Projekte und Sitzungen, ein Ordner je Projekt (zum Beispiel `memory/Desktop-SchadenMelden24/`) |
| `WISSEN.md` | Lesbare Übersicht über alles Gelernte: Regeln des Lernloops und Gedächtnis-Notizen je Projekt. Wird von `export.py` erzeugt |
| `claude/vendor/` | Sync-Skript und Manifest der Agency Agents mit deren Lizenz |
| `gsd/defaults.json` | GSD-Vorgabe `resolve_model_ids: omit`: setzt keine Modell-ID; GSD erbt die aktive Claude-Code-/Subagent-Auswahl |
| `extras/devos-claude-port/` | DevOS-Paket mit Prüfsummen, der Ursprung der Portierung aus Codex |
| `export.py`, `restore.py` | Setup sichern und wiederherstellen |
| `setup-manifest.json` | Liste aller Dateien mit Prüfsumme, geschrieben von `export.py` |

## Modell-Setup (Haiku 5.5, Sonnet 5.5 und Opus 5.5)

Das Setup nutzt eine auf Aufgabe, Risiko und Modell abgestimmte DevOS-Rollenmatrix. Das ist eine Orchestratorregel und kein natives automatisches Claude-Code-Routing: Sitzung, Desktop-/CLI-Auswahl, Umgebungsvariablen, settings.json und Agent-Frontmatter können die effektive Auswahl beeinflussen.

Voraussetzung für das vollständige 5.5-Trio ist Claude Code CLI 2.1.293 oder neuer. Sonnet 5.5 wird ab 2.1.284 unterstützt. Hauptgespräch und Orchestrierung verwenden explizit Opus 5.5 mit high. Architektur, Design und unabhängiges Review liegen ebenfalls bei Opus; Sonnet übernimmt die meiste Umsetzung und Verifikation. Die Rollen verwenden die Provider-Aliase haiku, sonnet und opus; explizite Anthropic-Modell-IDs stehen in settings.json für das Hauptmodell und verifizierte Modellgrenzen.

| Wer | Modell | Denkstufe (Effort) |
|---|---|---|
| Discovery (devos-explorer) | Haiku 5.5 (haiku) | medium |
| Recherche (devos-researcher) | Sonnet 5.5 (sonnet) | medium; high nur bei Versions-/API-Konflikt |
| Umsetzung, Verifikation und Plattform/Infra | Sonnet 5.5 (sonnet) | high; devos-worker-xhigh für scope-sensible Eskalationen; devos-worker-max nur nach passendem Task-Eval für mehrstufige CLI-Aufgaben |
| Design (devos-designer) | Opus 5.5 (opus) | high |
| Architektur und unabhängiges Review (devos-architect, devos-reviewer) | Opus 5.5 (opus) | high |
| Security (devos-security) | Opus 5.5 (opus) | xhigh für Class D |
| Hauptgespräch und Orchestrierung (Root) | Opus 5.5 (claude-opus-5-5) | high; Xhigh für besonders komplexe oder risikoreiche Aufgaben |

Wo das eingestellt ist:

- claude/settings.json: model claude-opus-5-5; Opus 5.5 ist für das Hauptgespräch auf high gesetzt. Sonnet und Haiku starten auf medium; alle drei Modelle erlauben Max als Obergrenze. CLAUDE_CODE_SUBAGENT_MODEL=sonnet bleibt der Default für allgemeine Spezialisten.
- claude/agents/devos-*.md: feste Defaults je benannter DevOS-Rolle. Ein höheres Modell oder Effort ist eine explizite Eskalationsanweisung; Effort ist nicht monoton, daher Xhigh für scope-sensible Sonnet-Arbeit bevorzugen und Max nur taskbezogen evaluieren. Es gibt kein magisches Auto-Routing.
- claude/CLAUDE.md und claude/skills/devos-orchestrate/SKILL.md: Task-, Risiko-, Kontext-, Parallel-, Eskalations- und Verifikationsvertrag.
- gsd/defaults.json bleibt unverändert und setzt mit resolve_model_ids: omit keine Modell-ID; GSD erbt die aktive Claude-Code-/Subagent-Auswahl.

Die Opus-Zuordnung für Design ist eine Qualitätsentscheidung; die Coding-Effort-Kurven messen keine Designqualität direkt. Desktop-App: Dort bestimmt die Auswahl im Eingabefeld das Modell neuer Sitzungen. Vor wichtigen Aufgaben /model, /effort und /doctor prüfen; ein DevOS-Profil kann eine externe Sitzungs- oder Umgebungsvariable nicht sicher übersteuern.

## Was bewusst nicht drin ist

- **Anmeldedaten** wie `.credentials.json` und Tokens. Jedes Gerät meldet sich selbst an.
- **Gesprächsverläufe** (`projects/*.jsonl`, zusammen rund 1,2 GB), Datei-Historie, Uploads und Sitzungsdaten. Sie sind groß und enthalten oft Zugangsdaten aus der Arbeit. Das Wissen daraus steckt in den Lektionen des Lernloops und im Gedächtnis; beides ist drin.
- **Plugin-Dateien** (`plugins/`). Sie werden auf dem neuen Gerät aus den Marktplätzen installiert.
- **Umgebung und Protokolle von Security Guidance** (`security/`).
- **Suchindex und Zustände des Lernloops** (`sessions.db`, `state/`, Treffer, Änderungsprotokoll). Sie entstehen auf jedem Gerät neu. Die Suche in früheren Sitzungen (`recall`) findet deshalb nur Sitzungen des jeweiligen Geräts.
- **Reste alter Werkzeuge** (`claude-mem`, `superpowers`, `ui-ux-pro-max`, `helpers`, `hooks`), die im Setup nicht mehr eingebunden sind.

`export.py` bricht ab, bevor etwas geschrieben wird, wenn eine Datei nach einem Schlüssel, Token oder Passwort in einer Adresse aussieht. Das gilt auch für das Gedächtnis. Bekannte Lehrbeispiele in fremden Agent-Beschreibungen sind einzeln freigegeben. Die DevOS-Port-Quelle liegt standardmäßig unter `~/Documents/DevOS/devos-claude-port`; mit `DEVOS_CLAUDE_PORT_SOURCE` lässt sich der Pfad ändern. Fehlt die Quelle oder überschneidet sie sich mit dem Repo-Ziel, bricht der Export ohne Änderungen ab.

## Auf einem neuen Gerät einrichten

1. Installieren: Claude-Desktop-App, Node.js, Python 3.11 oder neuer, Git und die GitHub-Kommandozeile `gh`. Unter Windows zusätzlich zwei Dinge, ohne die Schritt 5 und 6 scheitern:
   ```
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   npm i -g @anthropic-ai/claude-code@2.1.293
   ```
   Die Desktop-App allein legt den Befehl `claude` nicht in den Suchpfad, und ein frisches Windows blockiert die `.ps1`-Startdateien von `npm`, `claude`, `vercel` und `codex`.
2. Repo holen und in den Ordner wechseln:
   ```
   git clone -c core.longpaths=true https://github.com/hanneswrnr/Claude-Code-Setup.git
   ```
   Die Option erlaubt unter Windows lange Dateipfade; einige Gedächtnis-Ordner haben sehr lange Namen. Danach in den Ordner wechseln:
   ```
   cd Claude-Code-Setup
   ```
3. Vorschau ansehen:
   ```
   python restore.py --dry-run
   ```
4. Einspielen:
   ```
   python restore.py
   ```
   Vorhandene Dateien werden vorher nach `~/.claude/restore-backup-<Datum>` gesichert. Pfade wie `C:/Users/hanne` werden an den Benutzerordner des neuen Geräts angepasst.
   Das Gedächtnis landet in `~/.claude/projects/<Projekt>/memory/`. Claude findet es, wenn das Projekt auf dem neuen Gerät im selben Ordner liegt wie hier (zum Beispiel `Desktop\SchadenMelden24`). Gedächtnis aus Sitzungen ohne Projektordner wird nicht eingespielt, weil Claude es auf einem anderen Gerät nie liest; es bleibt im Repo und in `WISSEN.md` lesbar.
   Meldet `restore.py` zu lange Pfade, zuerst „Lange Pfade einschalten“ unter „Gut zu wissen“ erledigen.
5. Die angezeigten Befehle ausführen: Marktplätze hinzufügen und Plugins installieren.
6. GSD nachinstallieren. Die 67 GSD-Skills und 33 GSD-Agents aus dieser Sicherung sind nur die Oberfläche; ihr Motor liegt in `~/.claude/get-shit-done` und kommt aus npm:
   ```
   npm i -g get-shit-done-cc
   ```
   Ohne diesen Schritt erscheinen die `/gsd:`-Befehle, greifen beim Aufruf aber ins Leere. Das Paket heißt `get-shit-done-cc`; `get-shit-done` ohne Zusatz ist ein fremdes Paket.
   Danach `python restore.py` noch einmal ausführen, damit die gesicherten GSD-Agents und Skills wieder zum Setup passen. `gsd/defaults.json` setzt keine Modell-ID; GSD erbt die aktive Claude-Code-/Subagent-Auswahl.
7. Anmelden, wo es gebraucht wird:
   - Claude-Konto
   - `codex login` für das Codex-Plugin
   - `gh auth login` für GitHub
   - claude.ai-Connectors nur bei Bedarf
8. Prüfen:
   ```
   python ~/.claude/learning/ll.py doctor
   python -m unittest discover -s ~/.claude/learning/tests
   ```
9. Eine neue Claude-Code-Session starten.

## Änderungen sichern

Es gibt keinen automatischen Abgleich zwischen Geräten. Das Repo übernimmt immer den Stand des Geräts, das zuletzt sichert. Darum diese Reihenfolge, jeweils im Repo-Ordner:

1. **Bevor du auf einem Gerät arbeitest:** den neuesten Stand holen und einspielen.
   ```
   git pull
   ```
   ```
   python restore.py
   ```
   Achtung: `restore.py` ersetzt lokale Lektionen und Notizen, die dieses Gerät noch nicht gesichert hat, durch den Repo-Stand. Die alte Fassung liegt danach in `~/.claude/restore-backup-<Datum>`.
2. **Zum Sichern auf dem Gerät, auf dem du gearbeitet hast:** zuerst nur prüfen, ob ein anderes Gerät inzwischen etwas gesichert hat.
   ```
   git pull
   ```
   Meldet `git pull` „Already up to date“, weiter mit Schritt 3. Kommen neue Änderungen herein, nicht exportieren, sondern Claude bitten, die Stände zusammenzuführen. Sonst löscht `export.py` im Repo, was das andere Gerät gesichert hat. Nicht `restore.py` ausführen, das würde die Arbeit auf diesem Gerät zurücksetzen.
3. Sichern. `export.py` schreibt dabei auch `WISSEN.md` neu.
   ```
   python export.py
   ```
   ```
   git add -A
   ```
   ```
   git commit -m "Setup aktualisiert"
   ```
   ```
   git push
   ```

## Gut zu wissen

- **Python-Befehl:** Die Hooks und die Statusleiste rufen `python` auf. Auf macOS und Linux heißt das Programm oft `python3`; dann in `~/.claude/settings.json` anpassen.
- **Lange Pfade einschalten (Windows):** Nur nötig, wenn `restore.py` zu lange Pfade meldet. PowerShell als Administrator öffnen (Startmenü, „PowerShell“ eintippen, Rechtsklick, „Als Administrator ausführen“) und ausführen:
  ```
  New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name LongPathsEnabled -Value 1 -PropertyType DWORD -Force
  ```
  Richtig ist es, wenn `LongPathsEnabled : 1` erscheint. Danach ein neues Terminal öffnen und `python restore.py` erneut ausführen.
- **Abgeschaltete Business-Plugins:** Die Einträge `…@inline: false` betreffen Plugins aus dem claude.ai-Konto, die die Desktop-App mitbringt.
- **Connector-Regeln:** Einige Nachfrage-Regeln nennen claude.ai-Connectors über ihre Kennung (`mcp__<kennung>__…`). Sie gelten für dieses Konto; bei anderen Konten greifen sie einfach nicht.
- **Werkzeug-Kits:** Die Kits für `devos-hyperframes` und `devos-scroll-craft` sind nicht enthalten.
- **Agency Agents:** Sie stammen aus [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) und stehen unter deren Lizenz (`claude/vendor/agency-agents.LICENSE`).
  - Zum Aktualisieren den Klon anlegen:
    ```
    git clone https://github.com/msitarzewski/agency-agents ~/.claude/vendor/agency-agents
    ```
  - Danach `python ~/.claude/vendor/sync_agency_agents.py` ausführen.
