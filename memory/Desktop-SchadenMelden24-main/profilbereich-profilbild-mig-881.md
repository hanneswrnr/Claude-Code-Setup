---
name: profilbereich-profilbild-mig-881
description: "Profilbereich der Seitenleiste moderner + eigenes Profilbild, PR #327 (Worktree C:\\Users\\hanne\\sm24-profil), Mig 881 LIVE seit 04.10.2026; Merge wartet auf Hannes; Google-/Apple-Anmeldung erst später"
metadata:
  node_type: memory
  type: project
  originSessionId: 08a75455-f680-49af-a601-2bd875c47059
  modified: 2026-10-04T18:00:01.026Z
---

Auftrag Hannes 04.10.2026: Profilkasten unten in der Seitenleiste in allen Rollen deutlich moderner, eigenes Profilbild hochladen und dort anzeigen. Anmeldung mit Google/Apple (dann Google-Profilbild) ausdrücklich „erst irgendwann in der Zukunft, nicht jetzt“.

Skizze `.planning/features/profilbereich/SKIZZE.html` (Präfix pf-) nach drei Runden freigegeben: v2 musste aus der Design-Bibliothek (= Bausteine-Galerie) gebaut werden, v3 mit deutlich smootheren Ein-/Ausklapp-Animationen. Entscheidungen: Klick auf Karte öffnet Konto-Menü; Verbund-Zentrale Variante A (eigenes Bild groß, Verbund-Logo als Abzeichen); Bild sieht nur man selbst; bis 10 MB, im Browser auf 256×256 WebP.

Stand 04.10.2026: Mig 881 LIVE (`profiles.avatar_pfad` mit CHECK `<id>/avatar-<ms>.webp`, privater Bucket `profilbilder` 512 KB webp, Policies nur eigener Ordner, Kontolöschung/Anonymisierung ziehen mit; verify „881-TEST OK“, Container-Test 226 PASS). Datei nie mehr ändern. App-Teil auf Zweig `feat/profilbereich-profilbild`, PR #327, Vorschau 4abcc5c34 (Datumskorrektur). Satz zum Profilbild in der Datenschutzerklärung 3.3 von Hannes freigegeben. Merge braucht Hannes; erst nach PR #319 mergen, dann main hereinholen (Konflikt erwartet in DashboardSidebar; der „Stand“ der Datenschutzerklärung ist in beiden Zweigen 4. Oktober 2026). Offen: echter Test am iPhone (Safari) beim Hochladen.

**Why:** Hannes wollte bei der Skizze „noch moderner, schau in die Design Bibliothek“ — zurückhaltende Entwürfe ohne Galerie-Elemente gefallen ihm nicht.
**How to apply:** Neue Oberflächen-Skizzen direkt aus Galerie-Bausteinen (Verlauf, Glow, Profil-Menü) bauen und Bewegungen flüssig planen. Siehe [[design-1zu1-skizze-html-css]], [[kalender-alle-rollen-pr-319]].
