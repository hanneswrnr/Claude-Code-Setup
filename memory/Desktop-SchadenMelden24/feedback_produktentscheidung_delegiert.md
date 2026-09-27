---
name: feedback-produktentscheidung-delegiert
description: "Wenn Hannes eine Produktfrage mit \"entscheide du\" zurückgibt, entscheidet Claude selbst – vorsichtig, begründet, dokumentiert"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 392d2b61-39f3-4db1-a724-3c38c80ab10c
  modified: 2026-09-25T11:43:16.704Z
---

Gibt Hannes eine Produkt- oder Fachentscheidung mit „entscheide du, ich habe keine Ahnung“ zurück, entscheidet Claude selbst statt erneut nachzufragen (so am 25.09.2026 bei den Service-Erinnerungen in SchadenMelden24).

**Why:** Hannes ist kein Entwickler und kann solche Fragen oft nicht beurteilen; eine zweite Rückfrage blockiert nur.

**How to apply:** Die umkehrbare, vorsichtige Variante wählen – nichts einschalten, was Mails an Dritte (Endkunden) verschickt oder rechtlich ungeprüft ist; stattdessen das Produkt ehrlich machen (keine Versprechen für Funktionen, die nicht laufen). Entscheidung mit Gründen und Weg zum Umkehren in feature-vault/wiki festhalten („vom Product Owner an Claude übertragen“), per Wächter-Test absichern, als eigenen PR ohne Merge vorlegen. Aktionen mit Außenwirkung (Versand, Deploy-Schalter) bleiben trotzdem freigabepflichtig. Siehe [[project_bezahlsystem_umbau]] für den Produktkontext.
