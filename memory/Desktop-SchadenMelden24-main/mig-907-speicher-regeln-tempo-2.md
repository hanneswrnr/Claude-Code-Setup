---
name: mig-907-speicher-regeln-tempo-2
description: "Mig 907 (Speicher-Regeln Stufe 2) live seit 16.10.2026, PR #409 gemergt; Planung 11,6 → 2,8 ms; Folgesession anon-Rechte Kalender"
metadata:
  node_type: memory
  type: project
  originSessionId: 997081cf-4cf5-4d66-8a92-53d01723d65d
  modified: 2026-10-16T19:39:44.761Z
---

Mig 907 ist seit 16.10.2026 live, nach Freigabe von Hannes. Die Regeln `kalender_anhaenge_eigene_lesen` und „Werkstatt reads own invoice PDFs“ rufen jetzt die INVOKER-Funktionen `speicher_kalender_anhang_eigen` und `speicher_werkstatt_eigen` auf. 907-, 861- und 906-TEST sind OK. Die Planung beim Lesen in storage.objects liegt live bei rund 2,8 ms statt vorher 11,6 ms.

PR #409 (Zweig fix/speicher-regeln-tempo-2) wurde am 16.10.2026 nach Freigabe von Hannes gemergt (d97acadf7). Folgepunkt: Gäste (anon) haben Rechte auf werkstatt_kalender_events. Daran arbeitet eine eigene Sitzung.

**Why:** Die Sitzung, die 907 vorbereitet hat, ist beendet. Wer später an die Speicher-Regeln geht, muss wissen, dass 907 schon live ist und dass der Rückweg von 861 erst nach dem Rückweg von 907 laufen darf.

**How to apply:** Niemals `DROP FUNCTION … CASCADE` auf diese Funktionen ausführen, das löscht still die Regeln. Wer den Körper ändert, muss die md5 an zwei Stellen nachziehen: in verify-907 und in verify-861. Siehe [[mig-906-speicher-regeln-tempo]].
