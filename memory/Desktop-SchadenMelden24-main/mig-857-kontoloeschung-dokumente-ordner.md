---
name: mig-857-kontoloeschung-dokumente-ordner
description: Mig 857 LIVE seit 02.10.2026 — get_user_storage_paths nimmt insurance-documents nur über den Ordner <versicherung_id>/; Folgepunkt Feedback-Screenshots offen
metadata:
  node_type: memory
  type: project
  originSessionId: ae9f58a6-bfca-4a43-bcfc-2ab21c22a34e
  modified: 2026-10-02T15:51:15.898Z
---

Mig 857 (`kontoloeschung_dokumente_nur_ordner`) ist seit 02.10.2026 live (Probelauf, Einspielen, Ledger, „857-TEST OK“ und „848-TEST OK“), Zweig `fix/kontoloeschung-dokumente-ordner`, Freigabe von Hannes für Einspielen und Merge am 02.10.2026. `get_user_storage_paths(uuid)` streicht den Zweig über `versicherung_dokumente.file_path`; die Funktion nennt die Tabelle nicht mehr. Live-Körper vor 857 war Mig 730 + Laufzeit-Patch 741 + Suchpfad 747 (nicht „zuletzt 730“).

**Why:** Folgepunkt 1 aus dem Bericht zu Mig 848 ([[mig-844-845-unterschriebenes-endgueltig]] gleiche Serie der Löschpfade, [[mig-846-847-loeschpfade-restgrenzen]]).

**How to apply:** Neue Änderungen an get_user_storage_paths vom Live-Körper (md5 `84e3…385c` nach 857) aus bauen; Wächter `lib/auth/konto/__tests__/migration-857-…test.ts` verlangt die Markierung `-- 857-REGEL GEÄNDERT:` für Pfadspalten-Zweige. Offener Folgepunkt (niedrig): Feedback-Screenshots über `feedback.screenshot_url` (Browser setzbar) in derselben Funktion. Rückweg 741 nur nach Rückweg 857.
