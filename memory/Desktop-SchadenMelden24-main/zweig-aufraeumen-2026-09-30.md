---
name: zweig-aufraeumen-2026-09-30
description: "Zweig-Aufräumen 30.09.2026 — Sicherung (voll.bundle + refs/sicherung), PRs #249–#258 gemergt, Mig 828–831 LIVE seit 30.09.2026"
metadata:
  node_type: memory
  type: project
  originSessionId: 5e664e83-2c80-42f0-8ec1-28a3cc8524ed
  modified: 2026-09-30T17:53:52.864Z
---

Am 30.09.2026 wurden 244 gemergte Remote-Zweige gelöscht (dazu 17 weitere per Befehl durch Hannes) und die übrigen 33 einzeln mit Hannes entschieden (Ergebnis in `.planning/aufraeumen/BRANCHES.md`, Abschnitt „Ergebnis 30.09.2026“).

- **Sicherung:** `C:\Users\hanne\Desktop\zweige-sicherung-2026-09-30-voll.bundle` (277 Zweige, volle Geschichte, im leeren Repo getestet). Zusätzlich lokale Refs `refs/sicherung/2026-09-30/<zweig>` im Hauptordner — nicht löschen, sie halten die Objekte fest. Das Repo war vorher ein flacher Klon und ist seitdem vollständig (`fetch --unshallow`).
- **Übernahmen, alle gemergt am 30.09.2026 (Freigabe Hannes „alles freigegeben“):** #249 Planung Nutzerführung, #250 Mig 014 Replay, #251 Mig 591/592 nachgetragen, #252 Stripe-Mandantentrennung, #253 KI-SEC-01/07, #254 Stripe-Kleinkorrekturen, #256 Mig 829–831, #257 Mig 828, #258 Doku.
- **Live seit 30.09.2026:** Mig 829, 830, 831 (Lager nur anhängen/Menge nur per Buchung, Annahme nur vollständig abschließbar inkl. Anhang-Sperre, Rechtsdok-Freigabe nur Plattform) und Mig 828 (DSGVO-Auskunft/Löschung neuere Tabellen). Entscheidung Hannes 30.09.: Absender-Adresse der Rundschreiben (Mig 279) und Marktplatz-Kaskade (Mig 539) bleiben unverändert.
- **claude/awesome-ramanujan-kn06oo** (Cloud-Aufräum-Chat): fertig (alle PRs bis #239 gemergt, voll in main, in Sicherung); Hannes hat die Entscheidung delegiert → Löschung beschlossen 30.09.2026.
- **Behalten:** recht/agb-2026-11-* (bis 09.11.), video/showreel-* (Marketing), feat/ai-features + backup/wip-sm24-ai-features-20260909 (KI; einzige Quelle der live laufenden Migrationen aus 586–598; beim Übernehmen 587 als 587 behalten, 586_s0 vor 592).
- **Folgepunkte** stehen in den Sicherheitsberichten 2026-09-30-lager-annahme-rechtsdok.md und 2026-09-30-dsgvo-auskunft-loeschung-neue-tabellen.md (fremde Annahme-Fotoplätze, Storage-Löschen Mig 528, Buchungs-RPC ohne Abo-Prüfung, Mig 780 registriert_am); eine Sitzung dazu wurde am 30.09. gestartet (Zweig fix/folgepunkte-annahme-lager-verbund).

**Why:** Die Sicherung und die Entscheidungen sind nur hier gebündelt; Remote-Löschungen macht wegen des Safety Net nur Hannes selbst.

**How to apply:** Die `refs/sicherung`-Refs nicht per `git gc --prune`/Update-Ref entfernen; bei „wo ist Zweig X hin“ zuerst im voll.bundle nachsehen. Siehe [[mobile-app-ueberall-entfernt]], [[prod-db-drift-feat-ai-features]].
