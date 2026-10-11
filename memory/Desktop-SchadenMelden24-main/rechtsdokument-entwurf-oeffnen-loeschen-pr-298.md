---
name: rechtsdokument-entwurf-oeffnen-loeschen-pr-298
description: "Rechtsdokument-Entwürfe wieder öffnen und löschen (PR #298, GEMERGT 02.10.2026, 691fc1f79); keine Migration, Mig 845 erlaubt Server-Löschen von Entwürfen"
metadata:
  node_type: memory
  type: project
  originSessionId: 79e49eb5-76ab-4af7-aa02-f88cc221f9bd
  modified: 2026-10-02T21:46:13.310Z
---

PR #298 (Zweig fix/rechtsdokument-entwurf-oeffnen, Commit e9bc7d9e7, 02.10.2026): Im Reiter „Rechtsdokumente“ lassen sich Entwürfe wieder öffnen (GET ?dokument_id=, nur Sitzung) und nach Rückfrage löschen (DELETE ?dokument_id=, Sitzung prüft, Service-Client löscht mit Filter status entwurf). PATCH antwortet 404, wenn der Entwurf inzwischen gelöscht wurde. Liste in styles/rechtsdokumente.css (Präfix rd-). Keine Migration. Mit Freigabe von Hannes gemergt am 02.10.2026 (Merge-Commit 691fc1f79).

**Why:** Entscheidung Hannes 02.10.2026 (Nachtrag ADR 0032): Ein Entwurf ist noch kein Beleg; vorher ließ er sich nach Verlassen des Reiters weder fortsetzen noch entfernen.
**How to apply:** Unterschriebene Rechtsdokumente bleiben unlöschbar; neue Wege zum Löschen immer erst mit der Sitzung prüfen und mit Filter status entwurf löschen. Der live vorhandene alte Entwurf (mit BEISPIEL-Textzeile) kann nach dem Merge im Reiter gelöscht und neu erzeugt werden. Verwandt: [[rechtsdokument-pdf-schrift-pr-296]], [[mig-844-845-unterschriebenes-endgueltig]].
