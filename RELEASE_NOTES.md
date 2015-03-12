##
### Bei Update-Fehler
..
*AttributeError: Das Feld `eq_quantity_left` existiert nicht*

*Fehler Kontext:*
*Ansicht `eq.purchase.order.line.tree`*
*[view_id: 1661, xml_id: equitania.eq_purchase_order_line_tree_inherit, model: purchase.order.line, parent_id: 867]*

**Folgenden Datensatz löschen:**
*DELETE FROM ir_ui_view WHERE name='purchase.order.line.tree' AND mode='extension';*

## 11.03.2015
## eq_framework_agreement
### Fix
- Added small bugfix for our excel tool

## 06.03.2015
## equitania
### Erweiterung
- Button/Widget in die Produkte eingefügt, die die Preisltistenpositionen anzeigen.

## 04.03.2015
## equitania
### Erweiterung
- Wizard für das Ändern des Liferdatums im Lieferschein eingefügt. Änderungsgrund muss angegeben werden und Änderung wird als Nachricht dokumentiert.
- Suche nur nach der Bezeichnung eingefügt.
- Sortierung nach dem Feld "Produktnr." ist ab jetzt auch möglich.
- Die Kundenmaske um die Standardliefer- und rechnungsadresse erweitert. Wird im Verkauf genutzt.

### Verbesseung
- Performanceverbesserung des SQL Statements von Omprakash
