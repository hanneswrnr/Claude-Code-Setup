---
name: reference-test-vermittler
description: Test-Vermittlerkonto fuer Browser-Tests der Vermittler-Rolle (seit 25.09.2026) und wie man es nutzt
metadata:
  node_type: memory
  type: reference
  originSessionId: 2d1ba5fd-606f-40b9-a7b5-8bd67970e110
  modified: 2026-09-24T22:23:03.006Z
---

Seit 25.09.2026 gibt es ein Test-Vermittlerkonto in der Test-Agentur des Nutzers: E-Mail `hannes-werner+test888@outlook.de` (Name „Test Vermittler“), eingeladen ueber Team → „Team-Mitglied einladen“. Passwort kennt nur der Nutzer — er meldet sich selbst an; Claude darf keine Passwoerter eingeben oder Konten anlegen.

Stand 25.09.2026: das Konto hat noch keinen eigenen Auftrag (Startseite/Liste zeigen 0). Ein Positivtest braeuchte einen Auftrag mit seiner vermittler_id — eine Schadensmeldung geht an eine echte Werkstatt, also vorher fragen.

**How to apply:** Fuer Klicktests der Rolle vermittler in Claude in Chrome den Nutzer bitten, sich damit anzumelden und Chrome neben die Claude-App zu stellen (verdeckte Tabs werden gedrosselt). Netzwerk-Anfragen (read_network_requests) zeigen, ob auf `vermittler_id=eq.` gefiltert wird. Siehe [[project_security_anon_rls]].
