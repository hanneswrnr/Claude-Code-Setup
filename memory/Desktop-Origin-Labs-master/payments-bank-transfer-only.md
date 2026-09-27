---
name: payments-bank-transfer-only
description: Operator wickelt alle Zahlungen per Banküberweisung ab — kein SEPA-Lastschrift/Stripe gewünscht
metadata:
  type: project
---

Hannes (Inhaber Origin Labs) wickelt **alle Kundenzahlungen per Banküberweisung** ab.

**Why:** Beim Vorschlag eines SEPA-/Stripe-Auto-Abbuchungs-Moduls als Nachfolger des Sorglos-Recurring-Billing (§17) klar abgelehnt — Zahlungen laufen ausschließlich über Überweisung. Das Mahnwesen (§14) fängt überfällige Rechnungen ab; eine Auto-Abbuchung ist nicht gewünscht.

**How to apply:** Keine SEPA-Mandat-/Stripe-Abo-/Auto-Abbuchungs-Features vorschlagen oder bauen. Die wiederkehrende-Rechnung-Engine (Sorglos, [[..]]) bleibt das Abrechnungs-Modell: Rechnung wird erstellt, Kunde überweist, Mahnwesen eskaliert bei Verzug. Echte Auto-Abbuchung ist dauerhaft out-of-scope.
