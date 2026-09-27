---
name: menudeck-migrations-ledger
description: Wie sich supabase_migrations.schema_migrations zu den Migrationsdateien verhaelt -- und warum eine nachtraegliche Korrektur in einer angewandten Migration gefahrlos ist
metadata: 
  node_type: memory
  type: project
  originSessionId: 45298565-c74a-4465-a1c8-784fe146fd81
  modified: 2026-08-06T21:08:40.865Z
---

Gemessen am 2026-08-06 an der lokalen DB (HEAD `be06b55`), weil die Frage bei jeder nachtraeglichen
Korrektur an einer bereits angewandten Migration wiederkommt:

**`supabase_migrations.schema_migrations.statements` fuehrt die SQL-Kommentare WOERTLICH mit.**
Der Ledger speichert die Datei an den Anweisungsgrenzen zerlegt (0073: 4 Anweisungen, 8037
Zeichen); fuehrende Kommentarbloecke haengen an der Anweisung, der sie vorausgehen. Probe:
`array_to_string(statements, ...) like '%SECHS BEFORE-UPDATE-Trigger%'` -> `t`.

**Trotzdem ist der Weg fuer eine Korrektur frei, und das ist gemessen, nicht angenommen:**

1. **Der Ledger folgt den Dateien.** Voller Abgleich (Whitespace normalisiert, Semikolons entfernt):
   **72 Dateien, 72 Ledger-Zeilen, 72 von 72 zeichengleich**, keine verwaiste Zeile in beide
   Richtungen. Skript-Muster: `array_to_string(statements,' ')` per base64 aus `psql` holen
   (`replace(encode(...), E'\n','')`, sonst zerfaellt die Zeile an den 76-Zeichen-Umbruechen).
2. **Der Praezedenzfall 0062 ist staerker als er aussieht.** Die Ledger-Zeile zu `0062` ENTHAELT den
   nachtraeglich eingefuegten Marker `KORRIGIERT (0063)`. Die Divergenz aus der Korrektur hat sich
   also beim naechsten Reset von selbst geschlossen.
3. **Es gibt keine DB, die kein Reset sieht.** Kein `project-ref`, kein `supabase link`, kein
   `db push` -- weder im Repo noch in der CI. Die lokale DB ist die einzige, `db:reset` ist ein
   Projekt-Skript.
4. Das Haus hat die Regel schon aufgeschrieben, `docs/menudeck-p6-regel-nachweise.md:250`: "Beim
   naechsten erreichbaren `supabase db reset` entsteht die Tabelle ohnehin neu aus den Dateien."

**How to apply:** Datei korrigieren UND `npm run db:reset` im selben Arbeitsschritt, danach den
Abgleich auf 72/72 nachfahren. Wer nur die Datei aendert, hinterlaesst 71/72 -- transient, aber
real, und genau diesen Abgleich fuehrt der Final-Review als Pruefung.

Siehe [[menudeck-p8-review-stand]].
