# Claude-Code-Setup (Origin Labs)

Privates Backup des globalen Claude-Code-Setups von Origin Labs. Hier wird das Setup gesichert und auf andere Geräte übertragen.

## Was drin ist

| Ordner oder Datei | Inhalt |
|---|---|
| `claude/CLAUDE.md` | Globale Regeln: DevOS, Grundregeln, Web-Projekte mit HTML/CSS und TypeScript, autonome Orchestrierung, Lernloop, Loop Engineering |
| `claude/settings.json` | Hooks des Lernloops, Nachfrage- und Sperr-Regeln, Plugins, Marktplätze, Modellstufen (Opus 5 auf xhigh als Haupt-/Orchestrationsmodell, Fable 5.1 auf high ausschließlich für Design, Sonnet 5 statt Haiku), Statusleiste |
| `claude/statusline.py` | Statusleiste im Terminal: Modell, Effort, Kontext, Cache-Trefferquote und Abo-Limits |
| `claude/agents/` | 279 Agency Agents (Beschreibungen auf 160 Zeichen gekürzt) und 8 DevOS-Rollen mit festen Modellstufen |
| `claude/skills/` | DevOS-Skills sowie `learn`, `reflect`, `recall`, `loop-engineering` |
| `claude/learning/` | Lernloop mit Prüf-Gate, Tests und den gelernten Lektionen (`lessons.jsonl`) |
| `claude/vendor/` | Sync-Skript und Manifest der Agency Agents mit deren Lizenz |
| `extras/devos-claude-port/` | DevOS-Paket mit Prüfsummen, der Ursprung der Portierung aus Codex |
| `docs/setup-report.html` | Bericht zur Gesamtprüfung vom 11. September 2026 |
| `export.py`, `restore.py` | Setup sichern und wiederherstellen |
| `setup-manifest.json` | Liste aller Dateien mit Prüfsumme, geschrieben von `export.py` |

## Was bewusst nicht drin ist

- **Anmeldedaten** wie `.credentials.json` und Tokens. Jedes Gerät meldet sich selbst an.
- **Gesprächsverläufe** (`projects/`), Datei-Historie, Uploads und Sitzungsdaten. Sie sind privat und groß.
- **Plugin-Dateien** (`plugins/`). Sie werden auf dem neuen Gerät aus den Marktplätzen installiert.
- **Umgebung und Protokolle von Security Guidance** (`security/`).
- **Suchindex und Zustände des Lernloops** (`sessions.db`, `state/`, Treffer, Änderungsprotokoll). Sie entstehen neu.
- **Automatisches Gedächtnis** (Memory). Es hängt am jeweiligen Projektordner.

`export.py` bricht ab, bevor etwas geschrieben wird, wenn eine Datei nach einem Schlüssel oder Token aussieht.

## Auf einem neuen Gerät einrichten

1. Installieren: Claude-Desktop-App oder Claude Code, Python 3.11 oder neuer, Git. Empfohlen: Node.js und die GitHub-Kommandozeile `gh`.
2. Repo holen und in den Ordner wechseln:
   ```
   git clone https://github.com/hanneswrnr/Claude-Code-Setup.git
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
5. Die angezeigten Befehle ausführen: Marktplätze hinzufügen und Plugins installieren.
6. Anmelden, wo es gebraucht wird:
   - Claude-Konto
   - `codex login` für das Codex-Plugin
   - `gh auth login` für GitHub
   - claude.ai-Connectors nur bei Bedarf
7. Prüfen:
   ```
   python ~/.claude/learning/ll.py doctor
   python -m unittest discover -s ~/.claude/learning/tests
   ```
8. Eine neue Claude-Code-Session starten.

## Änderungen sichern

Auf dem Gerät, auf dem du am Setup gearbeitet hast:

```
python export.py
git add -A
git commit -m "Setup aktualisiert"
git push
```

Auf einem anderen Gerät danach `git pull` und `python restore.py`.

## Gut zu wissen

- **Python-Befehl:** Die Hooks und die Statusleiste rufen `python` auf. Auf macOS und Linux heißt das Programm oft `python3`; dann in `~/.claude/settings.json` anpassen.
- **Modelle:** Das Setup nutzt Opus 5 auf xhigh für Hauptgespräch, Orchestrierung, Umsetzung, Tests und unabhängige Prüfung; Fable 5.1 auf high ausschließlich für Design; Sonnet 5 für Suche und Recherche; nie Haiku. Fable ist nur im Max-Abo und bei Premium-Plätzen im Abo enthalten. Auf anderen Konten kann `"model"` in `~/.claude/settings.json` auf `"opus"` gesetzt werden; die Design-Rolle lässt sich bei Bedarf auf Opus zurückstellen.
- **Abgeschaltete Business-Plugins:** Die Einträge `…@inline: false` betreffen Plugins aus dem claude.ai-Konto, die die Desktop-App mitbringt.
- **Connector-Regeln:** Einige Nachfrage-Regeln nennen claude.ai-Connectors über ihre Kennung (`mcp__<kennung>__…`). Sie gelten für dieses Konto; bei anderen Konten greifen sie einfach nicht.
- **Werkzeug-Kits:** Die Kits für `devos-hyperframes` und `devos-scroll-craft` sind nicht enthalten.
- **Agency Agents:** Sie stammen aus [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) und stehen unter deren Lizenz (`claude/vendor/agency-agents.LICENSE`).
  - Zum Aktualisieren den Klon anlegen:
    ```
    git clone https://github.com/msitarzewski/agency-agents ~/.claude/vendor/agency-agents
    ```
  - Danach `python ~/.claude/vendor/sync_agency_agents.py` ausführen.
