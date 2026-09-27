---
name: menudeck-instrumentenfallen
description: "Drei gemessene Faelle, in denen das Messgeraet und nicht die Anwendung geantwortet hat -- und woran es jedes Mal aufgefallen ist"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4447cc85-a23c-4716-98f5-4a5845f2d0dc
  modified: 2026-08-06T22:54:25.641Z
---

Im P8-Security-Review sind drei Messungen zunaechst falsch ausgefallen, **alle drei so, dass das
Ergebnis wie ein bestandener Test aussah**. Gefunden hat sie jedes Mal die Positivkontrolle, nie
die eigentliche Zusicherung.

1. **Playwrights `APIRequestContext` sendet ein `secure`-Cookie ueber http NICHT mit.** Chrome haelt
   `http://127.0.0.1` fuer einen sicheren Kontext, undici nicht. Die Methodenmessung lieferte sechs
   `307` — das haette sich als „die Methoden sind dicht" gelesen. Aufgefallen allein daran, dass die
   POST-Kontrolle MIT Sitzung ebenfalls 307 lieferte. **Loesung: in-page `fetch` per
   `page.evaluate`.**
2. **`signOutAction` steckt unter den Server-Action-IDs.** Sie lief als erste durch, meldete ab und
   liess die folgenden 15 Proben auf `/login` laufen — ein Bild, das exakt wie „die Sperre greift"
   aussieht. **Loesung: je ID eine frische Anmeldung.**
3. **`fetch(..., { redirect: 'manual' })` liefert bei Umleitungen eine OPAQUE Antwort** — `status`
   ist 0, Kopfzeilen leer. Das Messgeraet konnte 405 und 204 lesen und JEDE Umleitung nicht
   (gemessen: 303 -> 0, 307 -> 0, 204 -> 204). **Loesung: den Status aus
   `page.waitForResponse` lesen, also aus der Netzwerkschicht vor der fetch-Semantik.**

**Die gemeinsame Lehre, und sie ist aelter als P8:** schon der erste Regel-1-Detektor des Projekts
meldete fuer BEIDE Rollen 0, weil er nach `from public.orders` suchte, waehrend PostgREST
`FROM "public"."delivery_list"` schreibt. **Ohne Positivkontrolle misst eine Null das Instrument,
nicht die Anwendung.**

Praktische Folge fuer den Aufbau einer Probe: **die Positivkontrolle gehoert an den ANFANG**, nicht
ans Ende. Steht sie vorn, scheitert der Test am Messgeraet und sagt das auch; steht sie hinten,
laufen die Zusicherungen davor gruen durch und die Meldung zeigt auf die falsche Ebene.

Siehe [[menudeck-p8-review-stand]].
