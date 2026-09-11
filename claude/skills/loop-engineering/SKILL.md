---
name: loop-engineering
description: Loop Engineering statt Einzel-Prompts. Plant und startet Arbeits-Loops mit messbarem Ziel, Prüfsteinen, Budget und Abbruchbedingung (Prüf-Gate, /goal, /loop, Desktop-Routinen, dynamische Workflows). Nutzen bei substanziellen Aufgaben mit prüfbarem Endzustand (Tests grün, Build ok, Score erreicht, Backlog leer), bei wiederkehrender Arbeit (CI, Deploys, Triage) oder wenn der Nutzer Loop, Goal, "bis alles grün ist" oder "autonom" sagt.
---

# Loop Engineering

Ein Loop ist Arbeit, die sich wiederholt, bis eine Abbruchbedingung erfüllt ist. Statt jeden Schritt einzeln zu prompten, entwirfst du das System, das die Arbeit erledigt, prüft und den Stand festhält. Fertig ist, was die Prüfung grün meldet, nicht was sich fertig anfühlt.

## 1. Braucht die Aufgabe einen Loop?

- **Ja:** Das Ziel ist prüfbar und mehrere Runden sind absehbar, z. B. Migration, Feature gegen Akzeptanzkriterien, Fehler bis die Tests grün sind, Layout bis die Prüfskripte grün sind, Performance-Ziel, Backlog abarbeiten. Oder die Arbeit wiederholt sich (CI, Deploys, Triage, Pflege).
- **Nein:** kleine, klar beschriebene Änderung, reine Frage oder eine Entscheidung, die der Nutzer treffen muss. Dann normal arbeiten.

## 2. Die sechs Bausteine

1. **Ziel:** ein messbarer Endzustand plus Grenzen, z. B. "ohne Testdateien zu ändern".
2. **Prüfstein:** ein Befehl oder Messwert, der eindeutig grün oder rot liefert.
3. **Antrieb:** was die nächste Runde startet (Tabelle unten).
4. **Gedächtnis:** der Stand liegt auf der Platte, nicht nur im Kontext. Bei längeren Loops `LOOP.md` im Projekt mit Ziel, Prüfsteinen, Erledigtem, Offenem und Blockern.
5. **Budget und Abbruch:** höchstens N Runden oder Minuten, und was bei Aussichtslosigkeit passiert.
6. **Getrennte Prüfung:** Wer baut, bewertet nicht das eigene Ergebnis.

## 3. Prüfsteine finden

Suche zuerst im Projekt: `package.json`-Skripte (check, test, lint, typecheck, build, e2e, smoke, gate:*), Makefile, CI-Workflows, eigene Prüfskripte in `tools/` oder `scripts/`. Fehlt ein Prüfstein, baue zuerst einen (Test, Skript, Messung) und starte erst dann den Loop.

Bekannte Projekte des Nutzers:
- **Raumgestaltung Hartung:** `npm run check` (Typecheck und Build). `npm run routen` und `npm run ansichten` brauchen einen laufenden `npm run dev`. `npm run geraete` braucht einen statischen Server, siehe Dateikopf von `tools/geraete-pruefen.mjs`.
- **ONE OS** (Ordner `one-os`): `npm run typecheck`, `npm run lint`, `npm test`, `npm run test:e2e`, `npm run smoke`. Das Gesamt-Tor ist `npm run gate:vor-dem-merge`.

## 4. Den Antrieb wählen

| Antrieb | Wofür | So geht es |
|---|---|---|
| Prüf-Gate | Befehle entscheiden über "fertig"; der Stop-Hook führt sie nach jeder Antwort selbst aus | im Projektordner: `python C:/Users/hanne/.claude/learning/ll.py gate arm --check "npm run check" --max-rounds 8` (fragt nach Bestätigung) |
| `/goal` | Ziel, dessen Nachweis im Gespräch sichtbar wird; ein zweites Modell urteilt nach jeder Runde | `/goal npm run check endet mit Exit 0 und keine Testdatei wurde geändert, höchstens 15 Runden` |
| `/loop` | Wiederholung im Zeittakt, solange die Session offen ist | `/loop 10m prüfe den Vercel-Deploy und behebe Build-Fehler, stoppe wenn er grün ist` |
| Desktop-Routine (lokal) | wiederkehrend mit lokalen Dateien; die App muss laufen | Code-Tab, Routines, New routine, Local; Worktree-Schalter an |
| `/schedule` (Cloud) | wiederkehrend, auch wenn der Rechner aus ist | `/schedule every weekday 7:00: ...` |
| Dynamische Workflows | viele unabhängige Teilaufgaben parallel | nur wenn der Nutzer "ultracode" schreibt oder ausdrücklich einen Workflow will |

Gut kombinierbar sind Prüf-Gate plus `/goal` (das Gate prüft hart, das Goal hält die Richtung) und Routine plus `/goal` für Loops ohne Zutun.

Das Scharfschalten fragt den Nutzer nach Bestätigung und zeigt ihm die Prüfungen. `gate arm` läuft im Projekt- oder Paketordner (kein `--cwd`, nie im Benutzerordner); dort laufen später auch die Prüfungen. Erlaubt sind nur kurze, feste Formen mit Pfaden innerhalb des Projekts: `npm test` oder `npm run <skript>` (ebenso pnpm/yarn/bun, weitere Argumente nur nach `--`), `npx tsc|eslint|jest|vitest run|playwright test|prettier --check|biome check|next build|astro check|expo-doctor` mit wenigen festen Optionen, `pytest` oder `python -m pytest|unittest`, `node --test` oder ein Projektskript, `cargo test`, `go test ./...`, `gradlew test`, `dotnet test`, `mvn verify`, `git diff --exit-code`. Komplexe Schritte gehören in ein npm-Skript; dessen Inhalt samt pre- und post-Skripten und aufgerufenen Skripten wird auf Deploy-, Veröffentlichungs-, Nachlade- und Einzeiler-Befehle geprüft. Was eigene Projektdateien wie `node tools/pruefen.mjs` tun, prüft das Gate nicht; das Scharfschalten ist deshalb eine echte Freigabe. Das Gate gilt nur für die Session, die es scharf geschaltet hat, und endet spätestens nach 24 Stunden; das Zeitbudget je Runde beträgt höchstens 1500 Sekunden. Das Gate prüft nicht erneut, wenn seit der letzten roten Runde nichts geändert wurde, und endet nach zwei solchen Runden. Werden während des Gates Test- oder Prüfdateien geändert, verlangt es vor dem Abschluss eine Begründung. Weitere Befehle: `ll.py gate run --check "..."` (einmal prüfen, ohne scharf zu schalten), `ll.py gate status`, `ll.py gate off`.

## 5. Ablauf

1. Ziel, Prüfsteine, Budget und Grenzen in 3 bis 6 Zeilen festhalten, bei längeren Loops in `LOOP.md`. Vorher den Git-Stand sichern (eigener Branch oder Worktree, sauberer Arbeitsbaum): Checkpoints erfassen keine Änderungen per Bash, verlässlich zurück geht es nur über Git.
2. Ausgangsstand messen: `python C:/Users/hanne/.claude/learning/ll.py gate run --check "..."`.
3. Antrieb starten. Unbeaufsichtigte Runden brauchen Auto-Mode; das Sicherheitsnetz blockt gefährliche Befehle. Braucht ein Prüfstein einen Server, starte ihn im Hintergrund.
4. Jede Runde: kleinste sinnvolle Änderung, prüfen, die Ursache der roten Stelle beheben.
5. Vor "fertig": frischer Prüfer (Agent `devos-reviewer`, `/code-review` oder `/codex:adversarial-review`), danach den Diff lesen.
6. Dem Nutzer in einfachem Deutsch berichten: Ziel, Anzahl Runden, was grün ist, was offen bleibt. Wichtige Erkenntnisse mit dem Skill `learn` sichern.

## 6. Vorlagen

- **Website (Hartung):** Gate mit `--check "npm run check"`. Bei Layout-Arbeit zusätzlich `npm run dev` im Hintergrund starten und `--check "npm run ansichten"` ergänzen.
- **Web-App (ONE OS):** Gate mit `--check "npm run typecheck" --check "npm run lint" --check "npm test"`. Vor dem Merge: `/goal npm run gate:vor-dem-merge endet mit Exit 0, höchstens 20 Runden`.
- **Performance:** `/goal Lighthouse-Score der Startseite mindestens 90, gemessen und im Gespräch gezeigt, höchstens 5 Versuche`.
- **Mobile (Expo):** Gate mit `--check "npx tsc --noEmit" --check "npm test"`, zusätzlich `npx expo-doctor`.
- **KI-Chatbot:** ein Eval-Skript mit festen Fragen, erwarteten Antwortmerkmalen, Kostenlimit und Angriffsfällen (Prompt-Injection, Datenabfluss) als Prüfstein, z. B. `--check "npm run eval"`. Bei bewertenden Evals (etwa promptfoo `llm-rubric`) immer eine feste Schwelle setzen, sonst besteht auch ein Score von 0. Einen Teil der Fälle zurückhalten, damit der Loop nicht nur auf das bekannte Set optimiert.
- **CI oder Deploy beobachten:** `/loop 10m ...` mit klarer Stopp-Bedingung.
- **Wiederkehrende Pflege:** Desktop-Routine, z. B. wöchentlich `/reflect` oder nachts `npm run gate:vor-dem-merge` im Worktree mit Bericht.

## 7. Grenzen und Fallen

- Tests, Prüfungen oder Schwellenwerte abschwächen, überspringen oder löschen, um grün zu werden, ist verboten.
- Flackernde Prüfungen zuerst stabilisieren, sonst dreht der Loop leer.
- Nach zwei Runden ohne Fortschritt stoppen und berichten statt weiterzuprobieren.
- Screenshot-Vergleiche nur gegen Referenzbilder vom selben Betriebssystem: Windows rendert anders als Linux in der CI.
- Kein Loop ohne Budget. Verbrauch mit `/usage` und `/goal` (ohne Argument) im Blick behalten.
- Innerhalb eines Loops nie deployen, veröffentlichen, bezahlen, löschen oder Nachrichten senden ohne Freigabe des Nutzers.
- Höchstens 3 bis 5 Loops parallel, jeder im eigenen Worktree.
- Der Nutzer bleibt Ingenieur: Ergebnisse zeigen und erklären, nicht nur "grün" melden.
