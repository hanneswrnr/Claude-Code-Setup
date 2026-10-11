---
name: mig-859-versicherung-kennung-vom-server
description: "Mig 859 LIVE seit 02.10.2026 — versicherungen.id nur vom Server (Rechte entzogen + Trigger aa_versicherung_kennung_vom_server), PR #289 gemergt (48beadd3e); Werkstätten/Standorte als eigene Aufgabe"
metadata:
  node_type: memory
  type: project
  originSessionId: 449a8023-0cd2-4f40-bd50-aaaa8a41a4bb
  modified: 2026-10-02T16:27:07.288Z
---

Mig 859 ist seit 02.10.2026 live (Probelauf und Prüfskript „859-TEST OK“ mit konto_geprueft=t, Ledger 859). Sie entzieht anon/authenticated INSERT auf versicherungen, anon DELETE, authenticated UPDATE (id, user_id) und hängt den BEFORE-Trigger aa_versicherung_kennung_vom_server an (Funktion versicherung_kennung_vom_server, SECURITY INVOKER, md5 726f017ba9ba8fc313aed1d0e859e675). Zweig fix/versicherung-kennung-vom-server, PR #289 (Hannes hat am 02.10.2026 Einspielen und Merge freigegeben).

**Why:** Die Kennung trägt Rechte ohne Fremdschlüssel (ki-scans/versicherung/<id>/, insurance-documents/<id>/, Realtime-Topic vs:<id>); eine frei gewordene Kennung ließ sich übernehmen. Folgepunkt 2 aus Mig 848.

**How to apply:** Neue Browser-Schreibwege auf versicherungen dürfen nie id/user_id setzen und nichts anlegen; anlegen nur über register_versicherung_complete. Bewusst gelassen: insert_policy (wirkungslos), DELETE von authenticated, SELECT von anon. Werkstätten (werkstaetten.id/user_id) und Standorte (werkstatt_standorte.id) haben dieselbe Lücke — eigene Sitzung „Kennung von Werkstätten und Standorten absichern“. Rückweg erst nach Abhängigen. Verwandt: [[mig-843-anhang-pfade]], [[supabase-standardrechte-30-10-waechter]].
