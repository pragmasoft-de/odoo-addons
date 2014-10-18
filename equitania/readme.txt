Seite dem Push 87316ac verweist die Konatktperson nicht mehr auf res_users sondern auf hr_employee. 
Damit die Rechnungen, Verkaufsaufträge, Angebote, Anfragen und Bestellungen auch funktionieren, muss
man die Tabellen sale_order, purchase_order und account_invoice per SQL Statement überarbeiten.
Nachfolgend die Statements:

UPDATE sale_order
SET eq_contact_person_id = 1

UPDATE purchase_order
SET eq_contact_person_id = 1

UPDATE account_invoice
SET eq_contact_person_id = 1

Zu beachten ist hierbei, dass die Kontaktperson auf den Administrator gesetzt wird.