---
name: project-externer-cron-aufrufer
description: Zwei Jobs bei cron-job.org rufen SchadenMelden24-Routen per POST mit dem CRON_SECRET auf; Abschalt-Reihenfolge und Stand
metadata:
  node_type: memory
  type: project
  originSessionId: 94b1cc47-6789-4a56-9ec9-0ddbb7c844e2
  modified: 2026-09-22T20:55:22.345Z
---

Stand 22.09.2026: Im cron-job.org-Konto des Product Owners laufen zwei Jobs, die
Routen von SchadenMelden24 per **POST** mit dem gültigen `CRON_SECRET` aufrufen.
Angelegt, als das Projekt noch kein bezahltes Vercel-Abo hatte. Sie waren bis dahin
die **eigentlichen** Auslöser, weil die gleichnamigen Vercel-Crons per GET einen
Zweig trafen, der nur zählte:

| Job bei cron-job.org | Takt | Route | Vercel-Cron tat |
|---|---|---|---|
| SchadenMelden24 Notifications | alle 5 Min | `/api/notifications/process` | nichts (GET zählte) |
| Cleanup Orphaned Subscriptions | täglich 03:00 | `/api/subscriptions/cleanup-orphaned` | nichts (GET zählte) |

Der Product Owner kann bei cron-job.org selbst klicken; Claude ist dort nicht
angemeldet und gibt keine Passwörter ein.

**Stand 22.09.2026 abends:** Fix ist live (PR #50, Merge `fd3ab546`, Deployment
`dpl_ABUDBEovqJW412dWh8MKSxo2ruYd`). Der Product Owner hat den Job „SchadenMelden24
Notifications" bei cron-job.org **gelöscht**; seitdem ist der Vercel-Cron der einzige
Auslöser. Offen: erster Versand einer echten Benachrichtigung über den Vercel-Cron
(Beleg: `sent_at` nicht mehr auf 5-Minuten-Raster, Verzögerung unter 60 s).
„Cleanup Orphaned Subscriptions" bleibt bis PR #47 live ist. Den `CRON_SECRET`-Tausch
hat der Product Owner für **ganz am Ende** freigegeben — nach Löschen des zweiten
Jobs; Claude macht ihn selbst (Vercel-Umgebungsvariable + Redeploy) und zieht dann
die Wiki-Seite `05-Anti-Patterns/Vercel-Cron-ruft-GET.md` (Abschnitt Reihenfolge) nach.

**Why:** Ohne diese Jobs stünde der gesamte Benachrichtigungs-Versand (E-Mail,
Push, Glocke) und das nächtliche Abo-Aufräumen still — ohne Alarm, der Vercel-Cron
meldet ja 200.

**How to apply:** Abschalten nur in dieser Reihenfolge:
1. Notifications-Job erst nach dem Deploy des Fixes (GET und POST auf denselben
   Handler, atomares Beanspruchen) und erst, wenn ein Versand außerhalb des
   5-Minuten-Rasters belegt ist; zuerst pausieren, dann löschen.
2. Cleanup-Job erst, wenn Pull Request 47 ([[project-bezahlsystem-umbau]]) live ist —
   dort liegt die Reparatur von `cleanup-orphaned`. ACHTUNG: Mit PR 47 macht die
   Route standardmaessig nur einen TROCKENLAUF und kuendigt erst mit `?scharf=1`
   (bewusst, der Job lief nie gesichtet). Nach dem Livegang von PR 47 raeumen also
   weder der Vercel-Cron noch cron-job.org mehr scharf auf. Reihenfolge dann: einen
   Trockenlauf sichten, danach den Pfad in `vercel.json` auf `?scharf=1` umstellen
   (Code-Aenderung, eigener PR) und erst dann den cron-job.org-Job loeschen - nie
   beide scharf, sonst laeuft die Kuendigung doppelt. Solange es kein zahlendes
   Stripe-Abo gibt (Stand 22.09.2026: keines), eilt das nicht.
3. Danach `CRON_SECRET` tauschen (lag bei einem Drittanbieter), nicht vorher.
Siehe `wiki/05-Anti-Patterns/Vercel-Cron-ruft-GET.md`.
