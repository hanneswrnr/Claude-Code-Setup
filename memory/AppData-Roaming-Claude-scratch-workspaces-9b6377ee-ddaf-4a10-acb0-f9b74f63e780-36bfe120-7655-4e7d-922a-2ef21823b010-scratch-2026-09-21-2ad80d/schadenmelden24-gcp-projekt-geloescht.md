---
name: schadenmelden24-gcp-projekt-geloescht
description: Hannes hat am 24.09.2026 das Google-Cloud-Projekt 533361161972 (ehemals Firebase) geloescht; der Google-Kalender-Abgleich ist seitdem kaputt
metadata:
  node_type: memory
  type: project
  originSessionId: dba0837b-8412-4ef4-88f6-6812801dae4e
  modified: 2026-09-24T22:39:36.485Z
---

Am 24.09.2026 hat Hannes das ganze Firebase-/Google-Cloud-Projekt geloescht (Projektnummer 533361161972). Darin lagen auch die OAuth-Zugangsdaten fuer den Google-Kalender (Vercel-Variablen GOOGLE_CALENDAR_CLIENT_ID/SECRET) und vermutlich der GOOGLE_PLACES_API_KEY (Adressvervollstaendigung, laut Datenschutz nur im Admin-Bereich).

Folge: /api/cron/gcal-pull scheitert alle 5 Minuten mit "GCal listEvents 403 ... Project #533361161972 has been deleted" (werkstatt_gcal_connections.last_pull_error, eine aktive Verbindung seit 24.07.2026). Wiederherstellen geht 30 Tage lang, also bis etwa 24.10.2026, unter console.cloud.google.com/cloud-resource-manager?pendingDeletion=true (ggf. Abrechnungskonto neu verknuepfen). Hannes hat das Projekt am 24.09.2026 gegen 16:40 Uhr wiederhergestellt. Der Abgleich um 16:45 Uhr lief ohne Fehler (last_pull_error = null). Hannes hat danach die Schluessel des Dienstkontos firebase-adminsdk geloescht; der Kalender lief um 16:50 Uhr weiter fehlerfrei.

**Why:** Der Rat "Firebase-Projekt loeschen" (PR #68) war falsch, weil das Projekt mehr als Firebase enthielt. PR #69 hat den Rat korrigiert, geloescht war das Projekt da aber schon.

**How to apply:**
- Nach der Wiederherstellung pruefen, ob last_pull_error leer wird.
- Danach nur den Schluessel des firebase-adminsdk-Dienstkontos widerrufen, nicht das Projekt loeschen.
- Nie empfehlen, ein Google-Projekt zu loeschen, ohne vorher alle darin liegenden APIs und Zugangsdaten geprueft zu haben.
