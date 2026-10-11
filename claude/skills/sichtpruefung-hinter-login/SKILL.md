---
name: sichtpruefung-hinter-login
description: Oberflächen hinter der Anmeldung (Dashboard, Admin, Kundenbereich) sichtbar prüfen, ohne echte Zugangsdaten oder Produktionsdaten. Vorübergehende Prüfseite, Testserver mit Platzhalter-Werten, Supabase-Attrappe, Bilder in drei Breiten hell und dunkel. Nutzen, wenn eine UI-Änderung in einem Next.js- oder Supabase-Projekt (etwa SchadenMelden24 oder Origin Labs) im Browser nachgewiesen werden soll, die Seite aber eine Anmeldung oder Datenbank braucht.
---

# Sichtprüfung hinter der Anmeldung

Ziel ist ein echter Render-Nachweis der geänderten Oberfläche, ohne dass eine echte Anmeldung, ein Produktionsschlüssel oder Kundendaten nötig sind. Es gibt keine Abkürzung über echte Konten: Keine Passwörter eingeben, keine Produktionsdatenbank ansprechen.

## Ablauf

1. **Prüfseite anlegen.** Eine vorübergehende Seite unter `app/` rendert die echten Komponenten mit Beispiel-Props und Beispieldaten, etwa `app/sichtpruefung-temp/page.tsx`. Der Ordnername darf nicht mit `_` beginnen (private Ordner sind in Next.js keine Route). Keine Logik der Komponenten nachbauen, sondern die echten Komponenten importieren.
2. **Server mit Platzhalter-Werten starten.** Den Dev-Server über ein kleines Node-Startskript starten, das nur Platzhalter-Umgebungswerte setzt. Die Startprüfung (`instrumentation.ts`) bricht sonst ab:
   - Supabase-Adresse mit `supabase.co` darin, zum Beispiel `http://127.0.0.1:<PORT>/supabase.co`.
   - Service-Schlüssel als Platzhalter mit mindestens 30 Zeichen, Resend-Schlüssel als Platzhalter mit dem Anfang `re_`.
   - Nur erkennbare Platzhalter verwenden, nie echte oder echt aussehende Schlüssel.
   - Für `next build` gilt dasselbe schon beim Bauen: `NEXT_PUBLIC`-Werte werden eingebacken. Mit einer reinen localhost-Adresse bricht `next start` danach ab, und ein neuer Build dauert lange.
3. **Warten, bis die Seite antwortet.** Vor dem ersten Browser-Aufruf per Warteschleife mit `curl` warten, bis Status 200 kommt. Die Schleife braucht immer eine Zeitgrenze und eine Abbruchbedingung. Der erste Aufruf einer Dashboard-Seite kompiliert oft 2 bis 6 Minuten. Frühe Browser-Aufrufe laufen sonst in Zeitüberschreitungen und wirken wie ein hängender Browser.
4. **Bilder erzeugen.**
   - Bevorzugt ein Playwright-Skript per `tsx`, falls das Projekt Playwright hat. `page.route` fängt Supabase-Anfragen ab und liefert Beispiel-JSON (die Attrappe).
   - Breiten 393, 768 und 1280 Pixel, jeweils hell und dunkel (`colorScheme`).
   - Der App-Browser liefert bei verstecktem Fenster nur abgeschnittene Bilder und Zeitüberschreitungen. Ihn nur nutzen, wenn das Fenster sichtbar ist.
5. **Ansehen und bewerten.** Die Bilder selbst ansehen: Zustände, Umbrüche, Kontraste, leere und lange Inhalte. Befunde beheben und die Bilder neu erzeugen.
6. **Aufräumen.**
   - Server stoppen.
   - Prüfseite, Startskript und Playwright-Skript löschen.
   - Mit `git status` kontrollieren, dass nichts davon übrig ist oder committet wird.
   - Bilder nur im Scratchpad ablegen, nicht im Repo.

## Stolperfallen

- Ohne `supabase.co` in der Adresse scheitert der Start an der Umgebungsprüfung, auch wenn der Build durchläuft.
- Warteschleifen ohne Zeitgrenze hängen stundenlang, wenn der Server abgestürzt ist.
- Beispieldaten ehrlich halten: keine erfundenen Kennzahlen oder Kundenstimmen in Screenshots, die später als Beleg dienen könnten.
- Playwright meldet einen fehlenden Browser einer bestimmten Revision: nicht nachinstallieren, sondern eine vorhandene Headless-Shell unter `%LOCALAPPDATA%\ms-playwright` per `executablePath` nutzen.
- Skripte laufen mit `tsx`: esbuild umhüllt Funktionen mit `__name`, das es im Browser nicht gibt. Als erstes `addInitScript({ content: 'window.__name = function (f) { return f };' })`, sonst brechen `page.evaluate` und Init-Skripte (etwa eine Standort-Attrappe) still ab.
- Element- oder Ganzseitenfotos, die größer als das Fenster sind, vergrößern kurz das Fenster und lösen ein `resize` aus. Bei Zeichenflächen, Karten oder anderem, das auf `resize` reagiert, nur mit `clip` im sichtbaren Fenster fotografieren; Ganzseitenfotos in einem eigenen Tab. SchadenMelden24 scrollt weich (`scroll-behavior: smooth`): vorher `scrollIntoView({ behavior: 'instant' })`.
- SchadenMelden24 im Dev-Server: Der Cookie-Hinweis liegt über der Seite und fängt Klicks ab. Nach dem Laden zuerst „Nur essenzielle“ klicken (datensparsame Wahl). Die 500-Antworten von `/api/dsgvo/consent/anonymous` kommen von den Platzhalter-Werten und sind kein Befund.
- SchadenMelden24: Das Bestätigungsfenster aus `useConfirm()` hat keine Rolle `dialog`; auf seinen Titeltext warten. Knöpfe mit exaktem Namen wählen (`exact: true`): Das Unterschriftenfeld hat einen eigenen Knopf „Löschen“, und der Bestätigen-Knopf des Fensters kann denselben Namen tragen wie der auslösende Knopf (dann `.last()`, weil das Fenster per Portal am Ende von `<body>` hängt).
- Nach jedem Klick vor dem Foto die Maus mit `page.mouse.move(0, 0)` aus der Seite nehmen. Sonst bleibt der Zeiger über dem Element, das nach dem Schließen etwa des Cookie-Hinweises darunter liegt, und dessen Hover-Zustand hängt vom Zeitpunkt ab. Bei Vorher-nachher-Vergleichen gibt das große Schein-Abweichungen.
- `page.evaluate` in einem frischen Tab ohne Seitenaufruf (etwa für einen Bildvergleich auf `about:blank`): `addInitScript` greift dort nicht. Vorher `await page.evaluate('window.__name = function (f) { return f }')` als Text aufrufen.
- Was ein Nutzer am Handy auslöst, auch nachstellen: Touch per CDP `Input.dispatchTouchEvent` mit `hasTouch`, und das Ein-/Ausfahren der Adressleiste als reine Höhenänderung (`page.setViewportSize` mit gleicher Breite).

## Bewährt

- **Darstellung bleibt gleich (Vorher-nachher):** Die Prüfseite rendert die echten Bausteine mit beiden Varianten, umschaltbar per Such-Parameter (etwa `?variante=alt|neu`). Playwright fotografiert beide Varianten je Breite und Farbschema, danach Pixelvergleich per Canvas im Browser (kein Zusatzpaket). Restabweichungen per Gegenprobe prüfen: dieselbe Variante aus zwei Läufen vergleichen. Weicht sie dort genauso ab, ist es Zeichen-Rauschen, keine Änderung. Für Datensparsamkeit zusätzlich das ausgelieferte HTML (Seiten-Datenstrom) beider Varianten nach den sensiblen Beispielwerten durchsuchen.
