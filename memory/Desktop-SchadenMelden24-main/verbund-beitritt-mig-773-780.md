---
name: verbund-beitritt-mig-773-780
description: "Verbund-Beitritt per Anfrage und Einladung (Mig 773) und Folgepunkte mit Einladungs-Mail (Mig 780) – beide live, PR #206 und #215 gemergt; Entscheidungen des PO"
metadata:
  node_type: memory
  type: project
  originSessionId: 43cd8618-5304-4ee7-9f5f-9bb8b921c950
  modified: 2026-09-28T15:53:48.185Z
---

Verbund-Beitritt ist seit 28.09.2026 komplett live: Mig 773 (27.09.2026, PR #206) und Mig 780 (28.09.2026, PR #215), jeweils Prüfskript live „TEST OK“.

Funktionen (alle SECURITY DEFINER, nur service_role): F1 verbund_anfrage_stellen, F2 _zurueckziehen, F3 _entscheiden, F4 verbund_einladung_beantworten, F5 verbund_einladung_mail_reservieren, F6 _freigeben. Ab 780 ist scripts/verify-780-… maßgeblich (verify-773 meldet danach erwartungsgemäß FAIL 1).

Entscheidungen des PO (Hannes hat sie an die Umsetzung übertragen, 28.09.2026):
- Mailversand beim CSV-Upload standardmäßig AUS; HQ muss einschalten und Einwilligung bestätigen (Protokoll). Keine Rechtsprüfung zu § 7 UWG erfolgt.
- Grenzen: 200 Mails je Verbund und Tag, 24 h Abstand, 3 je Einladung, 3 je Adresse in 90 Tagen, 90 Tage keine Mail nach Ablehnung; Anfragen: 30 Tage nach Ablehnung, 3 in 7 Tagen.
- Registrierung über Verbund-Link darf Anfragen auch an nicht gelistete Verbünde anlegen (Werbeweg, HQ entscheidet).
- Resend: Open/Click-Tracking für schadenmelden24.com aus (geprüft).

**Why:** Hält fest, was bewusst so entschieden wurde, damit spätere Sitzungen es nicht als Lücke „reparieren“.
**How to apply:** Änderungen an F1–F6 nur per neuer Migration aus dem Live-Körper; Wächter-Freigabelisten von 770 enthalten 773 und 780. Offen: Support setzt gruppe_id direkt → Einladungen bleiben offen; Einladungstabelle scrollt bei 768 px in der Karte. Siehe [[mig-775-gruppen-angemeldete-spaltenrechte]], [[verbund-inaktiv-hq-nur-lesen-mig-779]].
