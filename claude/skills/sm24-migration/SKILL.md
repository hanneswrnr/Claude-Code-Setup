---
name: sm24-migration
description: Datenbank-Migration für SchadenMelden24 bauen, im Container prüfen, prüfen lassen und nach Freigabe live einspielen und zusammenführen. Nutzen bei jeder neuen oder geänderten Supabase-Migration in SchadenMelden24 (Trigger, RLS-Regel, SECURITY-DEFINER-Funktion, Rechte) und beim Einspielen oder Mergen einer schon gebauten Migration.
---

# SchadenMelden24: Migration bauen, prüfen, einspielen

Bewährter Ablauf aus Mig 745, 751–753, 757 und 759–762. Muster auf main: Migration 760
(`supabase/migrations/760_auftrag_standort_gleiche_werkstatt.sql`), Prüfskript und Rückweg unter
`scripts/…-760-…sql`, Container-Test `supabase/tests/760/`, Wächter
`Web_Schadenmelden24/lib/kunde/__tests__/migration-760-auftrag-standort-gleiche-werkstatt.test.ts`,
Bericht `wiki/09-Operations/Security-Audits/2026-09-27-auftrag-standort-gleiche-werkstatt.md`.
Vor dem Bauen diese Dateien auf `origin/main` lesen und nachbauen, nicht aus dem Gedächtnis.

Grundsätze:
- Produktion (Projekt `ownxhgvhciwknzonmsbs`) wird bis Schritt 9 nur gelesen. Verhalten wird im
  Wegwerf-Container belegt, nie mit Testdaten in Produktion.
- Andere Sitzungen arbeiten gleichzeitig im selben Repo und spielen laufend eigene Migrationen ein.
  Live-Stand und Nummern darum immer frisch prüfen, nie aus einem älteren Lauf übernehmen.
- Hannes ist Product Owner, kein Entwickler. Status in einfachem Deutsch, Fachbegriffe kurz erklären.

## 1. Arbeitsordner anlegen

Eigener Worktree (zweiter Arbeitsordner desselben Repos) je Thema, nie im Hauptordner arbeiten.

```bash
git -C C:/Users/hanne/Desktop/SchadenMelden24-main fetch --all --prune
git -C C:/Users/hanne/Desktop/SchadenMelden24-main worktree add --no-track -b fix/<thema> C:/Users/hanne/sm24-<thema> origin/main
```

- Start-Stand merken: `git -C C:/Users/hanne/sm24-<thema> rev-parse HEAD` (braucht Schritt 7).
- Fehlen `scripts/` oder `docs/` (Teil-Checkout): `git sparse-checkout add scripts docs`.
- `node_modules` als Junction (Verknüpfung) statt Neuinstallation, in PowerShell:
  `New-Item -ItemType Junction -Path C:\Users\hanne\sm24-<thema>\Web_Schadenmelden24\node_modules -Target C:\Users\hanne\Desktop\SchadenMelden24-main\Web_Schadenmelden24\node_modules`
- Pushen immer mit Ziel: `git push -u origin HEAD:refs/heads/fix/<thema>`. Nie nacktes `git push`.
- Aufräumen nach dem Merge: erst die Junction lösen
  `[System.IO.Directory]::Delete('C:\Users\hanne\sm24-<thema>\Web_Schadenmelden24\node_modules', $false)`,
  dann `git worktree remove C:/Users/hanne/sm24-<thema>` (ohne `--force`), dann `git branch -d fix/<thema>`.
  Nie `Remove-Item -Recurse` auf einen Ordner mit Junction (löscht sonst das echte node_modules).

Geklappt, wenn: `git worktree list` den Ordner mit dem neuen Zweig zeigt und `npx vitest --version`
im App-Ordner antwortet.

## 2. Nummer prüfen und reservieren

Die lokale Liste `ls supabase/migrations` ist für die Nummernvergabe wertlos. Einmal je Quelle prüfen:

1. `git fetch --all --prune`, dann alle Zweige in einem Lauf:
   `git log --all --name-only --diff-filter=A --format= -- 'supabase/migrations/76*' | sort -u`
   (Beispiel für Nummern ab 760; schneller als `git ls-tree` je Zweig; Worktrees teilen die
   Zweige, also nur einmal je Repo).
2. Unversionierte Dateien in allen Arbeitsbäumen aus `git worktree list --porcelain` sowie in
   weiteren eigenen Klonen unter `C:/Users/hanne/sm24*` per `ls <ordner>/supabase/migrations`.
3. Live-Ledger (Liste der eingespielten Migrationen) per Konnektor:
   `SELECT version, name FROM supabase_migrations.schema_migrations WHERE version ~ '^\d{1,4}$' ORDER BY length(version) DESC, version DESC LIMIT 10;`
   Nie `version::int` (Zeitstempel-Versionen brechen den Cast).
4. Nächste freie Nummer über allem nehmen, sofort Platzhalter-Datei
   `supabase/migrations/NNN_<thema>.sql` committen und pushen. Die Prüfung vor dem Push ist eine
   harte Bedingung (bei Treffer abbrechen, nicht nur ausgeben).
5. Ein bis zwei Minuten später erneut holen und prüfen. Bei Doppelbelegung gilt: wer zuerst
   committet und gepusht hat, behält die Nummer; der andere nummeriert sofort um. Die betroffene
   Sitzung per SendMessage informieren.

Geklappt, wenn: die Nummer in allen Zweigen, Arbeitsbäumen, Klonen und im Ledger genau einmal vorkommt.

## 3. Live-Stand nur lesend erheben

- Nur Supabase-Konnektor `execute_sql` mit SELECT. Nie `apply_migration` (vergibt
  Zeitstempel-Versionen), nie `supabase db query --linked` (legt in Produktion eine Anmelderolle an).
  Prüf-Agenten dieselbe Grenze in den Auftrag schreiben.
- Nur Zählwerte und Prüfsummen ausgeben, keine Personendaten, keine Kennungen.
- Signaturen nie raten: `to_regprocedure('public.f(text)')` oder vorher `pg_proc` lesen.
  `pg_get_functiondef` nur über `pg_proc` mit `prokind = 'f'`.
- Katalogspalten vom Typ `char` (`tgenabled`, `relkind`, `contype`, `polcmd`) und `regclass` vor
  `||` nach `text` casten, sonst Fehler 42725.
- Jede Funktion, die die Migration ändert: Live-Körper per `pg_get_functiondef` holen, als Datei
  sichern und belegen: `md5(pg_get_functiondef(oid))`, `md5(prosrc)` und `length(prosrc)` live
  gegen die lokale Datei (mit LF, `tr -d '\r'`). Nie den Stand der höchsten Repo-Migration nehmen.
- Offene Zweige nach Migrationen durchsuchen, die dieselben Funktionen ändern; dort nur Namen oder
  `md5(prosrc)` vorprüfen, sonst bricht die Vorprüfung je nach Reihenfolge grundlos ab.
- Alle Schreiber finden: Funktionen (`pg_get_functiondef … ILIKE`), Trigger, pg_cron-Aufträge und
  App-Code per `git grep` (nicht per Grep über den ganzen App-Ordner).

Geklappt, wenn: für jede berührte Funktion eine Datei mit belegter Prüfsumme vorliegt und die
Schreiber-Liste steht.

## 4. Migration bauen

- `BEGIN;` … `COMMIT;` je genau einmal in eigener Zeile, `SET LOCAL lock_timeout = '3s'`,
  `SET LOCAL search_path = public, pg_temp`. Tabellen gleich am Anfang per `LOCK TABLE` sperren,
  Eltern vor Kindern.
- Vorprüfung (Schritt 0, bricht ohne Änderung ab): Stand wie live (Tabellen, Spalten,
  Fremdschlüssel im Wortlaut), 0 Verstöße als Zählwerte, md5 der bekannten Schreiber, Suche nach
  unbekannten Schreibern. Soll-Werte per `set_config` statt Temp-Tabellen, dann läuft der Block
  auch in `BEGIN READ ONLY … ROLLBACK` gegen live.
- Trigger nach Muster 751/760: AFTER, Name mit `zz_` (feuert nach den anderen), Zeilensperre
  passend wählen (`FOR SHARE`, wenn eine Nicht-Schlüsselspalte geschützt wird; vor einem späteren
  UPDATE derselben Zeile `FOR NO KEY UPDATE`). Gegenrichtung (Elternzeile wird umgehängt) nur unter
  READ COMMITTED, sonst Fehler 40001. Verstöße mit Fehler 23514 und „(Mig NNN).“ am Ende.
- SECURITY DEFINER: `SET search_path = public, pg_temp` (pg_temp zuletzt), Eigentümer `postgres`,
  `REVOKE ALL ON FUNCTION … FROM PUBLIC, anon, authenticated;`, dann nur nötige GRANTs. Seit Mig 552
  sind neue Funktionen nicht mehr automatisch für anon ausführbar; der REVOKE bleibt trotzdem Pflicht.
- Vor einem Rechteentzug: RLS-Regeln, die die Funktion aufrufen, und alle `rpc`-Aufrufe im Code prüfen.
- Funktionen immer ganz per `CREATE OR REPLACE` aus dem belegten Live-Körper, nie dynamisch patchen.
  Keine Großbuchstaben mit Umlaut in Funktionskörpern (lower() rechnet live anders als im Container).
- Neue Tabelle mit RLS: Sperre aus Mig 620 aufrufen (`wartende_werkstatt_sperre_anwenden`).
- md5-Werte nie in dieselbe Zeile wie Namen mit token, secret, key, auth, credential oder api
  (Regel `wiki/04-Patterns/Pruefsummen-ohne-GitGuardian-Fehlalarm.md`).
- Selbstprüfung am Ende (Trigger, md5, Rechte, genau eine Fassung je Funktion); bei Fehler rollt alles zurück.
- Kopf: Befund, Regeln, Schreiber-Liste, was die Migration tut, bewusst nicht Geändertes, Sperren
  und Nebenläufigkeit, bekannte Grenzen, Hinweis auf Einspielen, Prüfskript und Rückweg.
- Nach dem Einspielen die Datei nie mehr ändern, auch nicht Kommentare.

Geklappt, wenn: die Vorprüfung live in `BEGIN READ ONLY … ROLLBACK` besteht (Datei nach dem
Prüfblock abschneiden, vorher per grep sichern, dass kein DROP, ALTER, GRANT oder EXECUTE drin ist).

## 5. Begleitdateien

- **Rückweg** `scripts/rueckweg-NNN-<thema>.sql`: stellt geänderte Funktionen byte-genau auf den
  Live-Stand davor zurück (md5 im Kopf), entfernt neue Trigger und Funktionen, Wächter gegen
  falschen Ausgangsstand, wiederholbar, Hinweis auf LF und auf den Ledger-Eintrag.
- **Prüfskript** `scripts/verify-NNN-<thema>.sql`: endet immer mit Abbruch; Erfolg ist die
  Meldung „NNN-TEST OK“, Fehlschlag „NNN-TEST FAIL n: …“, übersprungene Teile „NNN-HINWEIS“. Jede
  Prüfung in eigenem Block, keine Personendaten, `statement_timeout`, `lock_timeout`,
  `idle_in_transaction_session_timeout`. Im Kopf die awk-Anleitung für den Probelauf (Muster 760).
  Ohne die Migration muss es mit FAIL enden (Nachweis der Lücke).
- **Container-Test** `supabase/tests/NNN/` mit `run.sh` und `README.md` nach Muster 760:
  postgres:17.6, `timeout` um jeden docker- und psql-Aufruf, SQL per stdin (`docker exec -i … psql`),
  `trap` räumt den Container weg, Nachbau-Treue (md5 wie live), Gegenprobe ohne Migration,
  Negativfall als Rolle `authenticated` mit nachgebauter RLS-Regel, Varianten der Migration per
  `sed` (Vor- und Selbstprüfung müssen abbrechen), Prüfskript ohne/mit Migration und als
  Probelauf, doppeltes Einspielen, Rückweg-Zyklus. CHECK-Regeln der Tabellen mit nachbauen.
- **Wächter** `Web_Schadenmelden24/lib/<bereich>/__tests__/migration-NNN-<thema>.test.ts`:
  CRLF-fest, jede Datei einmal lesen, schnelle Vorfilter vor teuren Regex, Muster mit beliebigem
  Leerraum; prüft Aufbau, gleiche md5 in Migration, Prüfskript und Rückweg, und dass spätere
  Migrationen nichts entfernen, abschalten oder freigeben.

Geklappt, wenn: `run.sh` alle Fälle grün meldet und
`npx vitest run lib/<bereich>/__tests__/migration-NNN lib/__tests__/migration-pruefsummen-gitguardian`
im App-Ordner grün ist.

## 6. Docker

- Vor jedem Test `docker info`. Fehlt die Pipe `dockerDesktopLinuxEngine`, läuft Docker Desktop
  nicht. Starten in PowerShell losgelöst (nicht mit Start-Process, das stirbt mit dem Befehl):
  `Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = '"C:\Program Files\Docker\Docker\Docker Desktop.exe"' }`
  Danach `docker desktop status` mit Zeitgrenze abwarten.
- Stürzt das Backend mit einem Fehler an `sailor-ingest.sock` ab: Docker Desktop beenden, den
  Ordner `%LOCALAPPDATA%\Docker\run` umbenennen (etwa in `run-alt-20260927`), leeren Ordner `run`
  anlegen, einmal per CIM neu starten.
- Lange Läufe (bis über 30 Minuten) im Hintergrund starten. Wettläufe über `pg_stat_activity`
  belegen, nicht über Laufzeiten.

## 7. Unabhängig prüfen lassen

- devos-security und devos-reviewer mit festem Bereich `git diff <start-sha>..HEAD`, Live-Zugriff
  nur lesend über den Konnektor.
- Befunde an denselben Umsetzer zurück (SendMessage), danach Gegenprüfung durch denselben Prüfer.

Geklappt, wenn: beide Prüfer ohne kritischen, hohen oder mittleren Befund freigeben.

## 8. Doku

- Sicherheitsbericht `wiki/09-Operations/Security-Audits/JJJJ-MM-TT-<thema>.md` (Aufbau wie 760:
  Befund, Fix, Prüfung, Einspielen, Rückweg) und Eintrag oben im `README.md` daneben.
- Betroffene Seiten unter `wiki/06-Reference/DB-Schema/` und `wiki/06-Reference/API-Routes/`,
  dazu `feature-vault` in einfacher Sprache.
- `verified_at` auf heute, echte Umlaute, Aussagen wie „kein Aufrufer“ vorher per `git grep` belegen.

## 9. Einspielen (nur nach Freigabe)

Nur nach ausdrücklicher Freigabe von Hannes mit Aktion und Ziel, etwa „Migration 763 in Produktion
einspielen“. Sperrt die automatische Prüfung trotzdem, nicht auf ein anderes Werkzeug ausweichen:
Stand melden, Hannes um erneute Freigabe genau dieses Schritts bitten, dann einmal wiederholen.

1. **Vorprüfung erneut, nur lesend:** Prüfsummen der Schreiber, Nummer (Schritt 2), Sperren und
   lange Transaktionen auf den Tabellen (`pg_locks`, `pg_stat_activity`). Zählwerte und Prüfsummen
   der berührten Tabellen notieren.
2. **Probelauf:** Prüfskript mit Migrationskörper nach der awk-Anleitung im Kopf des Prüfskripts
   bauen (nur Kommentarzeilen in Spalte 0 dürfen weg, nie solche in Funktionskörpern), per
   `execute_sql` wörtlich senden. „NNN-TEST OK“ kommt als Fehlermeldung P0001 zurück: das ist Erfolg.
3. **Nachsehen, dass nichts zurückblieb:** keine neuen Funktionen oder Trigger, Prüfsummen und
   Zählwerte wie vorher, Sperren zählen mit `WHERE pid <> pg_backend_pid()` (die eigene Sitzung
   ausnehmen). Abweichungen erst fremden Quellen (Cron, andere Sitzung) zuordnen.
4. **Einspielen:** Migrationsdatei mit LF als Ganzes (BEGIN … COMMIT) über `execute_sql`.
5. **Ledger-Eintrag:**
   `INSERT INTO supabase_migrations.schema_migrations (version, name, statements) VALUES ('NNN', '<thema>', ARRAY['-- siehe supabase/migrations/NNN_<thema>.sql']) ON CONFLICT DO NOTHING RETURNING version;`
6. **Nachprüfung, nur lesend:** Trigger aktiv (`tgenabled::text`), md5 wie in der Migration,
   SECURITY DEFINER, Eigentümer, `proconfig`, kein EXECUTE für anon/authenticated
   (`has_function_privilege`), genau eine Fassung je Funktion.
7. **Prüfskript erneut** gegen den eingespielten Stand: „NNN-TEST OK“, danach keine Sperren.
8. Doku und Code-Kommentare auf „live“ mit Datum umstellen, committen, pushen.

Geklappt, wenn: Ledger-Eintrag zurückkommt, Nachprüfung passt und das Prüfskript OK meldet.

## 10. Zusammenführen (nach Freigabe)

- `origin/main` hereinholen. Konflikte meist im Security-Audits-`README.md`: alle Einträge behalten,
  neuester oben. Läuft main während des Merges weiter: Merge festschreiben, dann erneut mergen
  (nicht `merge --abort`).
- Vor dem Merge im selben Befehl vergleichen, dass `origin/main` dem getesteten Stand entspricht.
  Zieht main ständig weiter: nur das Delta seit dem letzten Volltest auf kritische Pfade prüfen
  (eigene Dateien, `supabase/migrations/`, betroffene App-Bereiche, `migration-*.test.ts`) und nur
  bei Treffern abbrechen und neu testen:
  `d=$(git diff --name-only <getestet>..origin/main | grep -E '^supabase/migrations/|migration-.*\.test\.ts$|<bereich>'); [ -z "$d" ] && gh pr merge <nr> --merge --match-head-commit <kopf-sha>`
- Danach den Merge-Stand komplett testen: im App-Ordner `npx vitest run` und `npx tsc --noEmit`.
- Vercel-Status des Merge-Commits abwarten: `gh api repos/{owner}/{repo}/commits/<sha>/status --jq .state`.
  Startet kein Produktions-Build, das melden bzw. per Vercel-Konnektor anstoßen.

## 11. Stolperfallen

- Kein `Co-Authored-By` in Commits und PR-Texten (hat früher Vercel-Deployments gesperrt).
- Commit-Nachrichten per Datei und `git commit -F <datei>`, keine Here-Strings im Bash-Werkzeug.
- `git add` nur mit Pfadliste, nie mit `git commit` per Semikolon verketten; danach `git show --stat HEAD`.
- Grep nie über den ganzen App-Ordner (folgt der node_modules-Junction), sondern gezielt `lib`, `app` …
- Pfade mit eckigen Klammern (`app/api/kunde/[token]`) in git-Pfadangaben mit `:(literal)` davor.
- Bash-Pipes nicht am Exit-Code bewerten, wenn `tail` am Ende steht (`set -o pipefail` oder Ausgabe lesen).
- CRLF aus dem Windows-Checkout verfälscht md5 im Container: Migration und Skripte mit `tr -d '\r'` einspielen.
- In PL/pgSQL Aliase und Variablen nie wie Spalten der abgefragten Tabelle nennen.
