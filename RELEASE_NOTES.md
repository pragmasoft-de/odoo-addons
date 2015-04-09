### 01.04.2015, 1.0.6
### equitania
#### Bugfix
- Neu erstellte Lieferscheine, die über den Button "Lieferschein abbrechen" erstellt wurden, werden mit dem Rechnungsstatus abzurechnen erstellt.

### 26.03.2015, 1.0.5
### equitania
#### Bugfix
- Fehlerhafte id abgeändert.

### 26.03.2015, 1.0.4
### equitania
#### Verbesserung
- Erweiterung der Tabelle res.partner um neues Feld eq_foreign_ref
- Erweiterung der Maske, damit man das Feld in der Detailansicht der Adresse pflegen kann
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
- Steuer wird bei den Rechnungspositionen automatisch gesetzt, wenn eine Rechnung von einem Lieferauftrag erstellt wird, welcher keinen Bezug zu einem Verkaufs-/Einkaufsauftrag hat.
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
- Button/Widget in die Produkte eingefügt, die die Preislistenpositionen anzeigen.

### 04.03.2015
### equitania
#### Erweiterung
- Wizard für das Ändern des Lieferdatums im Lieferschein eingefügt. Änderungsgrund muss angegeben werden und Änderung wird als Nachricht dokumentiert.
- Suche nur nach der Bezeichnung eingefügt.
- Sortierung nach dem Feld "Produktnr." ist ab jetzt auch möglich.
- Die Kundenmaske um die Standardliefer- und rechnungsadresse erweitert. Wird im Verkauf genutzt.

#### Verbesseung
- Performanceverbesserung des SQL Statements von Omprakash



### Modul Equitania
Optimiertung der Masken für Adressen, Produkte, Verkauf, Einkauf, Fertigung uvm.
Die Anzeige in der Partnersuche des Verkaufsauftrag um den Adresstypen erweitert. Straße, Ort einstellbar
In den Einstellungen wird der Reiter "Installierte Module" als erster Eintrag angezeigt und beim Öffnen aufgerufen
Die Unternehmensmaske um 4 Felder, die in der Fußzeile der Reports angezeigt werden, und das Firmenlogo, welches auf dem Report aufgedruckt wird
Die Debitoren- und Kreditorennummer mit Sequenzgenerator im Kunden/Lieferanten hinzugefügt
Eigene Übersetzungslogik der Reports und Masken
Internes und externes Papierformat wird gesetzt
Das Feld "Vermittelt durch" in die Leads eingefügt. Enthält eine Beschreibung.
Alle Auftragspositionen für Einkauf und Verkauf werden noch einmal in einer seperaten Maske(Liste, Form) angezeigt
Lieferbedingungen in den Verkaufsauftrag eingefügt
Die Suche nach einzelnen Positionen in Preisliste - Löschen über die Detailansicht - Widget in der Produktmaske
Sachbearbeiter in den Verkaufsauftrag eingefügt, Verkäufer wird automatisch eingetragen (einstellbar)
Eigene Logik für Tausender Serperatoren und Nachkommastellen für die Reports eingefügt (einstellbar)
Dezimalstellen für Mengen, Gewichte und Preise für Einkauf, Verkauf und Fertigung separat einstellbar
Liefertermin für Ein/Verkauf eingefügt. Wird auf Reports gedruckt (einstellbar KW/Datum)
Kopftext für die Reports eingefügt
Verbindung zwischen Verkaufsauftrag, Lieferschein und Rechnung hergestellt
Leistungsdatum in Rechnung vom Lieferschein abgeleitet
Produktbeschreibung wird für den Verkauf/Einkauf optimiert
Positionsnummer eingefügt. Wird vom Verkaufsauftrag and den Lieferschein und die Rechnung übergeben
Die Produktsuche erweitert, sodass nach der Referenz gesucht werden kann und diese auch angezeigt wird
Kundenreferenz in die Listenansicht des Verkaufsauftrag und Suche nach der Kundenreferenz hinzugefügt
1:1 Verbindung zwischen Mitarbeitern und Benutzern hergestellt
Überlieferungen werden in einer Position zusammengefasst (einstellbar)
Stornieren von Lieferscheinen ohne Rechnung - neuer Lieferschein wird erstellt
Wizard für das Ändern des Lieferdatums im Lieferschein eingefügt. Änderungsgrund muss angegeben werden und Änderung wird als Nachricht dokumentiert
Button/Widget in die Produkte eingefügt, die die Preislistenpositionen anzeigen
Feld für die Preislistenversion in die Preislistenposition eingefügt
Steuer wird bei den Rechnungspositionen automatisch gesetzt, wenn eine Rechnung von einem Lieferauftrag erstellt wird, welcher keinen Bezug zu einem Verkaufs-/Einkaufsauftrag hat
Fremdnr. bei Kontakt pflegbar - wird automatisch im Kundenauftrag in Referenznr. eingefügt
Kontakt überarbeitet:

Feld Vorname eingefügt
Feld Geburtsdatum eingefügt
Addresstyp um die Postfachaddresse erweitert
Standard Liefer- und Rechnungsadresse kann festgelegt werden
Ersteller des Datensatzes wird als Verkäufer eingetragen (einstellbar)

Reports überarbeitet:

Angebot
Verkaufsauftrag
Anfrage
Bestellung
Lieferschein
Rechnung
Neu:  Auftragspositionen
Neu: Rücklieferschein
Das "sale_layout" Modul intigriert, wodurch sich Positionen gruppieren lassen
