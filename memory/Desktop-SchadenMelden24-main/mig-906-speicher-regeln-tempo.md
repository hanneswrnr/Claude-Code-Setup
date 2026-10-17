---
name: mig-906-speicher-regeln-tempo
description: "Mig 906 Speicher-Regeln claim-photos/-pdfs/-signatures über speicher_ordner_*-Funktionen, LIVE seit 16.10.2026, PR #408 gemergt 16.10.2026 (6a85b44a5)"
metadata:
  node_type: memory
  type: project
  originSessionId: a3b440fb-56ee-4c2d-ab25-38fe1d9e68dd
  modified: 2026-10-16T15:09:09.820Z
---

Mig 906 (Zweig `fix/speicher-regeln-tempo`, PR #408 gegen main) ist LIVE seit 16.10.2026: neun Regeln auf storage.objects rufen fünf plpgsql-Funktionen `public.speicher_ordner_*` (SECURITY INVOKER) auf. Prüfskript live „906-TEST OK“. Nachmessung: Datei lesen ~11 ms, hochladen ~2 ms Planung (vorher 200–290 ms). Die restlichen ~11 ms stammen von Leseregeln anderer Buckets (gruppen-ticket, marktplatz, netzwerk, kalender …).

**Why:** Rechte unverändert, nur Tempo; Gleichwertigkeit im Container mit Matrix belegt. Folgt auf [[mig-905-chat-rls-tempo]].

**How to apply:** PR #408 ist gemergt (Merge-Stand: tsc grün, 22.212 Tests grün, Live-Build fertig). Nie `DROP FUNCTION speicher_ordner_* CASCADE` (löscht still die Regeln). EXECUTE für authenticated muss bleiben. Zweige der Regeln ab jetzt in den Funktionen ändern (neue Migration). Auflisten großer Buckets wird langsamer: Todo `storage-auflisten-schwelle` (Prüfdatum 16.01.2027).
