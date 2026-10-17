# Claude-Code-Setup (Origin Labs)

Privates Backup des globalen Claude-Code-Setups von Origin Labs. Hier wird das Setup gesichert und auf andere Geräte übertragen.

## Was drin ist

| Ordner oder Datei | Inhalt |
|---|---|
| `claude/CLAUDE.md` | Globale Regeln: DevOS, Grundregeln, Web-Projekte mit HTML/CSS und TypeScript, autonome Orchestrierung, Lernloop, Loop Engineering |
| `claude/settings.json` | Hooks des Lernloops, Nachfrage- und Sperr-Regeln, Plugins, Marktplätze, Modell-Setup (siehe unten), Statusleiste |
| `claude/statusline.py` | Statusleiste im Terminal: Modell, Effort, Kontext, Cache-Trefferquote und Abo-Limits |
| `claude/agents-archiv/` | 235 Agents, die seit der Kontext-Prüfung vom 17.10.2026 nicht mehr geladen werden (nie benutzt); Rückweg: Dateien nach `~/.claude/agents/` schieben |
| `claude/agents/` | 58 geladene Agents (vor dem 17.10.2026: 293). Bestand: 251 Agency Agents (Beschreibungen auf 160 Zeichen gekürzt; ohne die Bereiche Wissenschaft, Geodaten, Medizin und VR/AR), 8 DevOS-Rollen mit festen Modellstufen, der Such-Agent `Explore` auf Haiku 5.5 und 33 GSD-Agents |
| `claude/skills/` | 81 Skills: DevOS-Skills, `learn`, `reflect`, `recall`, `loop-engineering`, `sichtpruefung-hinter-login` und 67 GSD-Skills (deren Motor kommt aus npm, siehe Schritt 6) |
| `claude/learning/` | Lernloop mit Prüf-Gate, Tests und allen gelernten Lektionen (`lessons.jsonl`: aktive, auf Freigabe wartende und archivierte) |
| `memory/` | Automatisches Gedächtnis aller Projekte und Sitzungen, ein Ordner je Projekt (zum Beispiel `memory/Desktop-SchadenMelden24/`) |
| `WISSEN.md` | Lesbare Übersicht über alles Gelernte: Regeln des Lernloops und Gedächtnis-Notizen je Projekt. Wird von `export.py` erzeugt |
| `claude/vendor/` | Sync-Skript und Manifest der Agency Agents mit deren Lizenz |
| `gsd/defaults.json` | Modell-Einstellung für GSD: Die GSD-Agents laufen damit auf Opus 5.5 statt auf eigenen Modellstufen |
| `extras/devos-claude-port/` | DevOS-Paket mit Prüfsummen, der Ursprung der Portierung aus Codex |
| `docs/context/` | Kontext-Prüfung vom 17.10.2026: Audit, Architektur, Änderungsliste, Messwerte |
| `tools/` | `ctx_probe.py` und `ctx_aggregate.py`: messen Kontext und Werkzeug-Ausgaben aus den Sitzungsdateien (nur lesend) |
| `export.py`, `restore.py` | Setup sichern und wiederherstellen |
| `setup-manifest.json` | Liste aller Dateien mit Prüfsumme, geschrieben von `export.py` |

## Modell-Setup (Opus 5.5, Sonnet 5.5 und Haiku 5.5)

Stand 11. Oktober 2026. Grundsatz: Die höchste Denkstufe ist nicht automatisch die beste. Jede Stufe ist nach den veröffentlichten Benchmarks gewählt (Quellen unten).

| Wer | Modell | Denkstufe (Effort) |
|---|---|---|
| Hauptgespräch und Orchestrierung | Opus 5.5 (`opus`) | high; für lange autonome Läufe bei Bedarf `/effort xhigh` |
| Unabhängige Prüfung (`devos-reviewer`) und Sicherheit (`devos-security`) | Opus 5.5 | xhigh |
| Umsetzung, Tests, Plattform und Design (`devos-worker`, `devos-verifier`, `devos-platform`, `devos-designer`) | Opus 5.5 | high |
| Gründliche Kartierung und Recherche (`devos-explorer`, `devos-researcher`) | Sonnet 5.5 (`sonnet`) | high |
| Schnelle Suche (`Explore`, ersetzt den eingebauten Such-Agenten) | Haiku 5.5 (`haiku`) | medium |
| Hintergrundaufgaben von Claude Code (etwa Sitzungstitel) | Haiku 5.5 | Standard des Modells |
| Alle anderen Agents | Opus 5.5 | wie die Sitzung (high) |

Warum so:

- **Opus 5.5:** Schon `medium` erreicht Opus 5 auf `high`. Von `medium` auf `xhigh` gibt es etwa 5 Indexpunkte für rund 2,6-fache Kosten, `max` bringt nur noch etwa 2 Punkte für das 1,7-Fache von `xhigh` (Artificial Analysis). Anthropic empfiehlt `xhigh` und `max` nur, wo ein Gewinn gemessen ist. Darum `high` als Standard und `xhigh` nur für die Prüf-Rollen, wo ein übersehener Fehler mehr kostet als die Token.
- **Sonnet 5.5:** Auf `max` schneidet es in FrontierCode schlechter ab als auf `xhigh`, weil es dann zu viel delegiert und in Zeitlimits läuft. Darum ist es auf `high` begrenzt.
- **Haiku 5.5:** etwa 40-mal günstiger als Opus je Token und deutlich schneller, in FrontierCode 46,4 % gegenüber 52,1 % bei Sonnet 5.5 auf `xhigh`, aber schwach bei langer mehrstufiger Arbeit (Terminal-Bench 39 %). Ab 100.000 Token Eingabe steigt sein Preis auf das Fünffache. Darum nur für kurze Nachschlage-Suchen; was Grundlage für Architektur-, Sicherheits- oder Löschentscheidungen ist, kartiert weiter `devos-explorer` auf Sonnet.
- **Fable 5.1** bleibt draußen: teurer als Opus 5.5 und in den Coding-Benchmarks schwächer.

Wo das eingestellt ist:

- `claude/settings.json`:
  - `"model": "opus[1m]"` für das Hauptgespräch.
  - `modelSettings` → `claude-opus-5-5` → `"effortLevel": "high"`: die Denkstufe von Opus 5.5 (gilt auch für `opus[1m]`). Wichtig: Das oberste `effortLevel` in `~/.claude/settings.json` ignoriert Opus 5.5 laut Doku; es wirkt nur noch auf ältere Modelle. Das frühere `xhigh` dort hatte deshalb keine Wirkung, Opus 5.5 lief bisher auf seinem Standard `medium`. `/effort` speichert ebenfalls unter `modelSettings`.
  - `CLAUDE_CODE_SUBAGENT_MODEL=opus` für alle Agents ohne eigene Angabe.
  - `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5` und `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-5-5` legen die Kurznamen fest; Haiku übernimmt damit auch Hintergrundaufgaben wie Sitzungstitel.
  - `modelSettings` → `maxEffortLevel` sperrt `max`: Opus höchstens `xhigh`, Sonnet und Haiku höchstens `high`.
  - `modelSettings` → `claude-opus-5-5` → `"autoCompactWindow": 400000`: Gespräche auf Opus werden bei etwa 400.000 statt beim Standard von rund 967.000 Token zusammengefasst (braucht Claude Code 2.1.288 oder neuer). Jeder Arbeitsschritt liest den ganzen Kontext neu ein; ein halb so großer Kontext halbiert diese Grundlast. Nachteil: Bei sehr langen Sitzungen wird früher zusammengefasst, Details aus dem Anfang gehen eher verloren. Für eine einzelne Sitzung mit `/autocompact` änderbar, dauerhaft in `settings.json` (höchstens 1000000).
- `claude/agents/devos-*.md` und `claude/agents/Explore.md`: feste Modell- und Effort-Werte je Rolle.
- `gsd/defaults.json`: `"resolve_model_ids": "omit"`. Die GSD-Befehle geben ihren Agents dadurch kein eigenes Modell mit, also gilt auch dort Opus 5.5.
- `claude/CLAUDE.md` (Abschnitt „Modelle“) und `claude/skills/devos-orchestrate/SKILL.md` (Abschnitt „Model routing“): die Regeln dazu.
- Der Kurzname `opus` zeigt immer auf das aktuelle Opus-Modell. `sonnet` und `haiku` sind fest eingestellt; bei einem neuen Modell die Kennungen `claude-sonnet-5-5` bzw. `claude-haiku-5-5` in `settings.json` anpassen (Umgebungsvariable und `modelSettings`).

**Desktop-App:** Dort bestimmt die Auswahl im Eingabefeld das Modell neuer Sitzungen, nicht `settings.json`. Auf jedem Gerät einmal „Opus 5.5“ und die Stufe „Hoch“ (high) auswählen.

Quellen (abgerufen am 11.10.2026): anthropic.com/news/claude-opus-5-5, anthropic.com/claude-sonnet-5-5, anthropic.com/claude-haiku-5-5, platform.claude.com/docs/en/build-with-claude/effort, code.claude.com/docs/en/model-config, code.claude.com/docs/en/sub-agents. Die Werte von Artificial Analysis stammen nur aus Suchergebnis-Auszügen, weil die Seite hier gesperrt war.

## Was bewusst nicht drin ist

- **Anmeldedaten** wie `.credentials.json` und Tokens. Jedes Gerät meldet sich selbst an.
- **Gesprächsverläufe** (`projects/*.jsonl`, zusammen rund 1,2 GB), Datei-Historie, Uploads und Sitzungsdaten. Sie sind groß und enthalten oft Zugangsdaten aus der Arbeit. Das Wissen daraus steckt in den Lektionen des Lernloops und im Gedächtnis; beides ist drin.
- **Plugin-Dateien** (`plugins/`). Sie werden auf dem neuen Gerät aus den Marktplätzen installiert.
- **Umgebung und Protokolle von Security Guidance** (`security/`).
- **Suchindex und Zustände des Lernloops** (`sessions.db`, `state/`, Treffer, Änderungsprotokoll). Sie entstehen auf jedem Gerät neu. Die Suche in früheren Sitzungen (`recall`) findet deshalb nur Sitzungen des jeweiligen Geräts.
- **Reste alter Werkzeuge** (`claude-mem`, `superpowers`, `ui-ux-pro-max`, `helpers`, `hooks`), die im Setup nicht mehr eingebunden sind.

`export.py` bricht ab, bevor etwas geschrieben wird, wenn eine Datei nach einem Schlüssel, Token oder Passwort in einer Adresse aussieht. Das gilt auch für das Gedächtnis. Bekannte Lehrbeispiele in fremden Agent-Beschreibungen sind einzeln freigegeben.

## Auf einem neuen Gerät einrichten

1. Installieren: Claude-Desktop-App, Node.js, Python 3.11 oder neuer, Git und die GitHub-Kommandozeile `gh`. Unter Windows zusätzlich zwei Dinge, ohne die Schritt 5 und 6 scheitern:
   ```
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   npm i -g @anthropic-ai/claude-code
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
   Danach `python restore.py` noch einmal ausführen. Das stellt die Modell-Einstellung für GSD wieder her, falls die Installation sie überschrieben hat.
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
   `restore.py` führt die Lektionen zusammen (jede Lektion einmal, bei doppelten die zuletzt geänderte) und behält Gedächtnis-Notizen dieses Geräts, die neuer sind. Alles andere wird durch den Repo-Stand ersetzt; die alte Fassung liegt danach in `~/.claude/restore-backup-<Datum>`.
   Wurde dabei doch etwas überschrieben (etwa mit einer älteren Fassung von `restore.py`), holt dieser Befehl Lektionen und Notizen aus der Sicherung zurück; den Ordnernamen aus der Meldung „Vorher gesichert“ einsetzen:
   ```
   python restore.py --zurueckholen C:\Users\hanne\.claude\restore-backup-20261011-144518
   ```
2. **Zum Sichern auf dem Gerät, auf dem du gearbeitet hast:** zuerst nur prüfen, ob ein anderes Gerät inzwischen etwas gesichert hat.
   ```
   git pull
   ```
   Meldet `git pull` „Already up to date“, weiter mit Schritt 3. Kommen neue Änderungen herein, nicht exportieren, sondern Claude bitten, die Stände zusammenzuführen. Sonst überschreibt `export.py` im Repo, was das andere Gerät gesichert hat. Nicht `restore.py` ausführen, das würde die Arbeit auf diesem Gerät zurücksetzen.
3. Sichern. `export.py` schreibt dabei auch `WISSEN.md` neu. `--behalten` sorgt dafür, dass Gedächtnis-Notizen, die nur das Repo hat (etwa aus Sitzungen ohne Projektordner auf dem anderen Gerät), nicht gelöscht werden.
   ```
   python export.py --behalten
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
  - Danach `python ~/.claude/vendor/sync_agency_agents.py` ausführen. Das Skript merkt sich die Auswahl in `agency-agents.selection.json` (zurzeit ohne die Bereiche `academic`, `gis`, `healthcare` und `spatial-computing`); alle wieder holen mit `--all`.
  - `restore.py` entfernt Agency Agents aus abgewählten Bereichen, aber nur, wenn sie auf dem Gerät unverändert sind; sie landen vorher im Sicherungsordner.
