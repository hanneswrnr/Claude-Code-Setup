---
name: terminsystem-umsetzung-branch
description: "Umsetzung Terminsystem-Vereinfachung läuft seit 18.09.2026 im Worktree C:\\Users\\hanne\\sm24-termin auf Branch feat/termin-vereinfachung; nie nach main, nur Branch pushen für Vercel-Preview"
metadata: 
  node_type: memory
  type: project
  originSessionId: bb0d2f4d-2dd6-470d-a213-32389480b147
  modified: 2026-09-19T19:33:38.092Z
---

Die Umsetzung des vereinfachten Terminsystems (Konzept siehe [[terminsystem-vereinfachung-konzept]]) läuft im eigenen Git-Worktree `C:\Users\hanne\sm24-termin` auf Branch `feat/termin-vereinfachung` (node_modules als Junction aus dem Hauptordner). Alle 11 PO-Entscheidungen gelten laut /goal vom 18.09.2026 als nach Empfehlung beschlossen.

**Why:** Der Nutzer hat am 18.09.2026 ausdrücklich verlangt, dass am Ende nichts auf main landet, sondern auf einem eigenen Branch, damit er per Vercel-Preview vorher schauen kann. Parallel arbeiten andere Sitzungen (Auftragssystem im Klon `C:\Users\hanne\sm24-auftrag`, Branch feat/auftragssystem-vereinfachung; Nutzerführung nur in .planning).

**How to apply:** Nur den Feature-Branch pushen, nie main, kein Merge ohne ausdrückliche Freigabe. Vercel-Preview nutzt vermutlich die Prod-DB: Migrationen nur additiv schreiben und vor dem Einspielen fragen. Migrationsnummern 610–619 sind für Termine reserviert (belegt sind 610–614) (605–609 Auftragssystem). Dateiaufteilung: lib/termin/**, lib/kalender/**, app/api/werkstatt/termin*/**, components/termin/**, components/shared/detail/Termin*.tsx, Date/Time-Picker, beide Kalender-Seiten, Termin-Einstellungen gehören dieser Sitzung; Select.tsx, Auftrags-Detailansichten und Auftragslisten dem Auftragssystem-Chat. Stand 19.09.2026 abends: Funktion vom Korrektheits- und Sicherheitsprüfer für die Vorschau freigegeben; danach Umbau der Termin-Oberflächen 1:1 aus VEREINFACHUNG-SKIZZE.html (Bilder 1–4) auf HTML/CSS nach der neuen Regel (ADR-0024, Präfix `tm-`, `styles/termin.css` per `scripts/skizze-css.ts`, Fundament `styles/bausteine.css` kommt per cherry-pick vom Auftragssystem-Chat). Eigene gemeinsame Bausteine: DatePicker, DateTimePicker, TimePicker, MonthPicker, Callout, PopoverPortal, Switch. Das Vorschau- und Messwerkzeug liegt jetzt unter `.planning/features/terminbuchung/vorschau-werkzeug/` (README erklärt das Zurückkopieren); es darf nie innerhalb von `Web_Schadenmelden24/` gepusht werden. Nummer 620 gehört der Sitzung „Werkstatt-Freischaltung" (Branch fix/werkstatt-freischaltung-rls): Werden 611–613 (legen RLS-Tabellen an) NACH 620 eingespielt, muss jede am Ende `SELECT public.wartende_werkstatt_sperre_anwenden();` aufrufen; vor 620 ist nichts zu tun. `get_user_werkstatt_id()` nie per CREATE OR REPLACE überschreiben (610–614 tun das nicht, geprüft 19.09.2026). Vor worktree remove die node_modules-Junction per PowerShell löschen.

**Stand 20.09.2026 (Abend):** Branch `feat/termin-vereinfachung` liegt mit 29 Commits auf GitHub (4012 Tests gruen, tsc und eslint sauber, unabhaengige Pruefung durch). Die gemeinsamen Bausteine Button/SegmentedControl/Select/TabNav kommen wortgleich vom Auftragssystem-Branch (c530928a), zusammen mit `components/auftrag-styles.ts`, `styles/auftrag.css` und `auftrag-app.css` - ohne die beiden CSS-Dateien fehlen die Korrekturen der Bausteine selbst. Wichtig: `auftrag-app.css` setzt `.bs-detail-aside{top:80px}` ohne eigene Klasse und trifft damit auch die Termin-Maske; Gegenregel `.tm-sheet .bs-detail-aside{top:16px}` steht in `termin-app.css`. Gesperrte Segment-Optionen tragen `aria-disabled` statt `disabled`.

Messvergleich Skizze/App (1280 + 393 px hell, 768 px dunkel): deckungsgleich. Zwei Messfallen, die mich Zeit gekostet haben: eine laufende Einfahr-Animation skaliert alles auf 0,96 (527/549 = 49/51 = 68/71), und ein gemessenes `rgb(15,23,42)` ist die Dunkelmodus-Farbe, nicht ein dunkles Feld im hellen Modus. Bekannte Abweichung mit Grund: Die Skizze schaltet Zustaende mit `display: revert !important` und verliert dabei `display:flex` (Hinweiskasten 118 statt 84 px) - die App ist richtig.

Offen: Kalender-Oberflaechen und Termin-Block im Auftrag im Browser gegenpruefen (bisher nur dunkel bei 1280 px); PO-Frage, ob der Knopf "Dritte Zeit anbieten" orange (Skizze) oder neutral (Galerie) sein soll; Abschlussbericht. Befunde, die den gemeinsamen Bausteinen gehoeren (Tippflaeche der Reiter, bs-h-btn, min-w am Select im Buehnen-Planer, searchable), stehen im Auftragssystem-Prompt in `.planning/features/terminbuchung/LAPTOP-PROMPTS-2026-09-20.md` - dort liegen auch die Notebook-Prompts fuer alle sieben SchadenMelden24-Sitzungen.

**20.09.2026, Freigabe erteilt:** Migrationen 610-614 sind auf der Produktionsdatenbank eingespielt
(per Supabase-Konnektor, apply_migration). Nachkontrolle bestanden: werkstatt_kapazitaet_ausnahmen,
werkstatt_gcal_standort_kalender, werkstatt_gcal_kalender_sync, werkstatt_gcal_watch_channels
existieren, RLS an, `wartende_werkstatt_sperre` auf jeder, anon/PUBLIC ohne Rechte, die Spalten
kapazitaet_bestaetigt_at, pull_gestartet_at, gcal_event_id, gcal_calendar_id sind da.
`lib/supabase/database.types.ts` kennt die neuen Tabellen noch NICHT - bewusst nicht neu erzeugt,
weil die Datei allen Branches gehoert; `npm run db:types` erst nach dem Merge auf main.
Datenschutz-Abschnitt 7.2 wurde auf den neuen Google-Datenumfang umgeschrieben (Scopes, beide
Richtungen, Titel fremder Termine 120 Zeichen, Push-Kanaele) - vom Nutzer delegiert, kein Anwalt
geprueft.
