### 26.03.2015, 1.0.5
### equitania
#### Bugfix
- Fehlerhafte id abgeändert.

### 26.03.2015, 1.0.4
### equitania
#### Verbesserung
- Erweiterung der Tabelle res.partner um neues Feld eq_foreign_ref
- Erweiterung der Maske, damit man das Feld in der Detailansicht der Adresse plfegen kann
- Wenn ein Kundenauftrag oder eine Bestellung angelegt wird, ist der Inhalt des Feldes res.partner.eq_foreign_ref automatisch aus der Adresse übernommen und im Feld purchase.order."partner_ref" / sale.order."client_order_ref" gespeichert


### 25.03.2015, 1.0.3
### equitania
#### Änderung
- Die Zeichnungsnnummer aus den Reports Angebot/Auftrag, Lieferschein, Rückliefertschein und Rechnung entfernt und durch Platzhalter mit der id "eq_drawing_number" ersetzt.

### 24.03.2015, 1.0.2
### equitania
#### Verbesserung
- Ids an die Elemente der Lieferanschrift in der Rechnung vergeben.

### 23.03.2015, 1.0.1
### equitania
#### Änderung
- Das Feld eq_supplier_order_ref entfernt
* Vor dem Update muss das dazugehöre View gelöscht werden. Hierzu folgenden SQL Query benutzen:
* delete from ir_ui_view where arch like '%eq_supplier_order_ref%'

#### Bugfix
- Die Übersetzung des Textes "Leave Requests to Approve" im HR Modul wurde in unserer de.po Datei gespeichert, damit unsere Lokalisierung den Text selber setzen kann -> "Urlaubsanträge"


### 20.03.2015
### equitania
#### Verbesserung
- Unnötige Zugriffsrechte entfernt
- Finale Version unserer Lokalisierung hinzugefügt
#### Bugfix
- Steuer wird bei den Rechnungspositionen automatisch gesetzt, wenn eine Rechnung von einem Liferauftrag erstellt wird, welcher keinen Bezug zu einem Verkaufs-/Einkaufsauftrag hat.
- Testeinträge in der de.po Datei gelöscht

### 19.03.2015
### equitania
#### Erweiterung
- Erweiterung der Lokalisierung für Texte, die in der DB bereits vorhanden sind. Man kann also ab jetzt immer ein UPDATE der Übersetzungen durchführen

### 17.03.2015
### equitania
#### Bugfix
- Fehler bei den Unterlieferungen (Eingang) behoben. (Mengeneinheit * stimmt mit Mengeneinheit * nicht überein)
- Feld für den Rahmenauftrag einer Auftragsposition entfernt.
 
### 13.03.2015
### equitania
#### Erweiterung
- Open purchase order lines um neue Gruppierung nach Rahmenauftrag erweitert
- Feld für die Preislistenversion in die Preislistenposition eingefügt.
#### Bugfix
- Fehler bei den Unterlieferungen behoben. (Mengeneinheit Stück stimmt mit Mengeneinheit Stück nicht überein)
 
#### Änderung
- Änderung in der Lokalisierung für open purchase order lines -> der text "von Bestellpositionen" wird nicht mehr angezeigt

#### Bugfix
- Bugfix im Aufruf der Gruppierung nach Rahmenauftragsnummer für open sale order lines

### 12.03.2015
### equitania
#### Erweiterung
- Erweiterung der Lokalisierung für open purchase order lines

### Bei Update-Fehler
..
*AttributeError: Das Feld `eq_quantity_left` existiert nicht*

*Fehler Kontext:*
*Ansicht `eq.purchase.order.line.tree`*
*[view_id: 1661, xml_id: equitania.eq_purchase_order_line_tree_inherit, model: purchase.order.line, parent_id: 867]*

**Folgenden Datensatz löschen:**
*DELETE FROM ir_ui_view WHERE name='purchase.order.line.tree' AND mode='extension';*

### 11.03.2015
### eq_framework_agreement
#### Bugfix
- Added small bugfix for our excel tool

### 06.03.2015
### equitania
#### Erweiterung
- Button/Widget in die Produkte eingefügt, die die Preisltistenpositionen anzeigen.

### 04.03.2015
### equitania
#### Erweiterung
- Wizard für das Ändern des Liferdatums im Lieferschein eingefügt. Änderungsgrund muss angegeben werden und Änderung wird als Nachricht dokumentiert.
- Suche nur nach der Bezeichnung eingefügt.
- Sortierung nach dem Feld "Produktnr." ist ab jetzt auch möglich.
- Die Kundenmaske um die Standardliefer- und rechnungsadresse erweitert. Wird im Verkauf genutzt.

#### Verbesseung
- Performanceverbesserung des SQL Statements von Omprakash
