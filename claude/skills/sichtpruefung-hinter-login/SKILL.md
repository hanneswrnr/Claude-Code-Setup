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
