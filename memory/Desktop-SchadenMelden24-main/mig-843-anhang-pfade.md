---
name: mig-843-anhang-pfade
description: "Mig 843 LIVE seit 01.10.2026 + Routen-Pfadprüfung für claim_attachments.file_path; PR #274 (Zweig fix/anhang-pfade-claim-attachments), Merge von Hannes freigegeben"
metadata:
  node_type: memory
  type: project
  originSessionId: 2f51ae01-403b-460a-a25a-6e7cb3ee1fd1
  modified: 2026-09-30T22:20:22.826Z
---

Folgepunkt 1 aus [[mig-832-835-folgepunkte-annahme-lager-verbund]]: claim_attachments.file_path war vom Client frei wählbar; Service-Routen signierten/luden ihn ungeprüft.

- App: lib/storage/anhang-pfad.ts (anhangPfadImEigenenOrdner, pfadImOrdnerDerKennung, kundenUploadPfad) in kunde/refresh, kunde/attachments DELETE, v1 photos, versicherung/dokumente (+[id]), schadensdoku, lib/ai/ai-service; FotoPflichtDialog repariert (Ordner <id>/, uploaded_by_user_id).
- Mig 843 LIVE seit 01.10.2026 00:10 (843-TEST OK, 830-TEST OK): Regel A (anon/authenticated nur `<kennung>/<name [A-Za-z0-9._-]>`), Regel B (Annahme-Foto nur mit Anhang desselben Auftrags, alle Rollen; FOR SHARE am Anhang, FOR KEY SHARE am Protokoll nur bei INSERT/Protokollwechsel). Hängt an Mig 680 (aa_vorgang_kennung_vom_server) und an UNIQUE fahrzeug_annahme_protokolle_auftrag_unique.
- Mig 844 (andere Sitzung, Annahme endgültig) kommt nach 843; Rückweg-Reihenfolge 844 → 843 → 833/832/830.
- Eigene Aufgaben vorgeschlagen (nicht gebaut): Partner-API kategorie 'photo' verstößt gegen CHECK; uploaded_by_role frei wählbar (falsche Kunden-Mail); versicherung_dokumente.file_path gleiche Lücke.

**Why:** Nächste Sitzung soll Stand kennen, ohne neu zu erheben.
**How to apply:** Neue Funktionen, die claim_attachments nennen, brauchen einen Eintrag in der Leser-Liste von verify-843 (sonst 843-TEST FAIL 3); neue Server-Routen mit file_path müssen lib/storage/anhang-pfad.ts nutzen.
