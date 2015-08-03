### 03.08.2015
### equitania
#### Änderung, 1.0.56
- Abstände von Zahlungskonditionen, Lieferbedingungen, Rechnungsanschrift und Lieferanschrift am Fuß von Rechnungen, Angeboten und Einkäufen verbessert.

### 29.07.2015
### equitania
#### Änderung, 1.0.55
- Lieferscheinnummer wird in der Rechnung unter jeder Position angezeigt.

### 29.07.2015
### equitania
#### Erweiterung, 1.0.54
- id für ein td Element eingefügt
#### BUGFIX, 1.0.53
- Fehlerhafte Abfrage überarbeitet, wodurch vorher keine Lieferung durchgeführt werden konnte, wenn Überleiferungen in einer Position angezeigt werden sollten.
- Verkaufseinheit in der Verkaufsposition wird beim Ändern der Menge abgeändert.
#### Erweiterung
- Fußtext (Notiz/Geschäftsbedingung) im Verkauf/Einkauf von der Darstellung in der Form und den Report überarbeitet.
-- Report: Direkt unter die Positionen und ohne der Information "Notiz".
-- Form: Feld wird auf der ganzen Breite angezeigt.
#### BUGFIX, 1.0.52
- Übersetzungsfehler in Reports behoben.

### 23.07.2015
### equitania
#### BUGFIX, 1.0.51
- Fehler behoben, der Auftritt wenn bereits erstellte Lieferungen geliefert werden.

### 23.07.2015
### equitania
#### Änderung, 1.0.49
- Anischt der Partner angepasst.
-- Schlagwörte auf volle Breite.
-- Briefanrede nach dem Geburtstag
-Übersetzung angepasst.
#### Änderung, 1.0.50
- Startwert der Sequenz der Debitoren-/Kreditorennummer um 1 erhöht.

### 22.07.2015
### equitania, 1.0.48
#### Änderung
- Den Fix für die Leerzeichen in die Reports direkt eingefügt.
- Breifeanrede zu den Kontakten hinzugefügt.

### 21.07.2015
### equitania, 1.0.47
#### Erweiterung
- Positionen beim Liefern haben einen direkten Bezug zu den Lieferscheinpositionen.

### 17.07.2015
### equitania, 1.0.46
#### Bugfix
- Hausnummer des Unternehmens in die Reports eingefügt.

### 10.07.2015
### equitania, 1.0.45
#### Bugfix
- Die offene Menge der Verkäufe bei den Produkten und Produktvarianten zeigt nun den richtigen Wert.

### 07.07.2015
### equitania, 1.0.44
#### Bugfix
- Feld eq_qty_left als float erfasst.
####Erweiterung
- Kopf- und Fußtext auf html umgestellt.

### 07.07.2015
### equitania, 1.0.43
#### Bugfix
- Der Text zum einfügen eines Snippets wird im report nicht angezeigt.
#### Erweiterung
- Kopftext auf html umgestellt.
- Geschäftsbedingungen auf html umgestellt.

### 29.06.2015
### equitania
#### Bugfix, 1.0.42
- Übersetzung für Webseiten und Reports überarbeitet. Manche Begriffe wurden nicht übersetzt.

### 23.06.2015
### equitania
#### Bugfix, 1.0.41
- Eins zu Eins Beziehung zwischen Mitarbeiter und Benutzer wird wieder richtig hergestellt.
- Mitarbeiter ließ sich nicht mit einem Benutzer erstellen.

### 23.06.2015
### equitania
#### Erweiterung, 1.0.40
- Papierformate werden bei neuinstallation und update angelegt und Reports werden automatisch zugeteilt.
#### FIX, 1.0.39
- Überleiferung war nicht möglich.
#### FIX, 1.0.38
- Vereinzelte Lieferscheine ließen sich nicht abschließen.

### 23.06.2015, 1.0.37
### equitania
#### Erweiterung
- Die Reports werden bei der Installation den Papierformaten zugeordnet.

### 22.06.2015, 1.0.36
### equitania
#### Änderung
- Papierformate für die neuen Reports angepasst. Werden bei einer Neuinstallation neu gesetzt.
#### FIX
- Bei einer Unterlieferung wird die Verkaufsmenge richtig gesetzt, wodurch dir Rechnung mit der korrekten Menge erstellt wird.
- Bei erzwungenenen Teillieferungen (nicht auf Lager) wird die Lieferung von davor nicht addiert. 

### 19.06.2015, 1.0.35
### equitania
#### Änderung
- Rechnung- und Lieferadresse bekommen auch den Zusatzt Starße und Stadt, wenn die Option in den Verkaufseinstellungen aktiviert ist.

### 18.06.2015, 1.0.34
### equitania
#### Änderung
- Die Änderungen am partner_id Feld zusammengefasst. Nur die nötigen Attribute werden geändert.
- Die Optionen für die Ädresserweiterungen werden nun immer angezeigt.
- Beim "Verkäufe" Button im Produkt wird die Menge aus Angeboten nicht mehr berücksichtigt.
#### Erweiterung
- Hausnummer in die Unternehmendsdaten eingefügt.

### 12.06.2015, 1.0.33
### equitania
#### Änderung
- Reports und Header überarbeitet. Informationsblock wird auf allen Seiten gedruckt.

##### Vor dem Update folgende SQL Script ausführen

- delete from ir_ui_view where inherit_id = (select id from ir_ui_view where name = 'eq_saleorder_extension');
- delete from ir_ui_view where name = 'eq_saleorder_extension';

- delete from ir_ui_view where inherit_id = (select id from ir_ui_view where name = 'eq_purchasequotation_extension');
- delete from ir_ui_view where name = 'eq_purchasequotation_extension';

- delete from ir_ui_view where inherit_id = (select id from ir_ui_view where name = 'eq_purchaseorder_extension');
- delete from ir_ui_view where name = 'eq_purchaseorder_extension';

- delete from ir_ui_view where inherit_id = (select id from ir_ui_view where name = 'eq_invoice_extension');
- delete from ir_ui_view where name = 'eq_invoice_extension';

- delete from ir_ui_view where inherit_id = (select id from ir_ui_view where name = 'eq_report_picking_extension');
- delete from ir_ui_view where name = 'eq_report_picking_extension';

- update report_paperformat
- set header_spacing = 55, margin_top = 60
- where id = 1;

### 9.06.2015, 1.0.32
### equitania
#### Bugfix
- Zeilenumbrüche werden auf den Reports wieder richtig angezeigt.

### 9.06.2015, 1.0.31
### equitania
#### Bugfix
- Fehlenden Context eingefügt.

### 29.05.2015, 1.0.30
### equitania
#### Verbesserung
- Auswahl bei Standardliefer- und rechnungsadresse auf die eigenen Partner-Kontakte beschränkt
- Kundenreferenznr. wird beim Duplizieren übertragen

### 28.05.2015, 1.0.28
### equitania
#### Bugfix
- Benutzer mit eingetragenem Mitarbeiter lässt sich wieder erstellen.
- Logik für die 1zu1 Verbindung zwischen Mitarbeiter und Benutzer funktioniert wieder.

### 28.05.2015, 1.0.27
### equitania
#### Verbesserung
- Deutsche Übersetzung für Ein-/Ausgangsrechnung angepasst.

### 27.05.2015, 1.0.26
### equitania
#### Bugfix
- In der Lieferansicht, welche man über den Button "Lieferungen" im Produkt öffnet, wird nach dem richtigen Produkt gefiltert.

### 27.05.2015, 1.0.25
### equitania
#### Bugfix
- Button in der Produktübersicht für die Ein-/Ausgangsrechnungen zeigt nun alle Rechnungen an.

### 27.05.2015, 1.0.25
### equitania
#### Verbesserung
- Button, welcher die Vekäufe im Produkt anzeigt, zeigt nun die offene Menge und die Gesamtmenge an.

### 27.05.2015, 1.0.24
### equitania
#### Erweiterung
- Anzeigeart (Kalenderwoche/Datum) des Lieferdatums auf Kundenebene einstellbar.

### 27.05.2015, 1.0.23
### equitania
#### Erweiterung
- Filter "Ein- und Ausgang" für die Lagerbuchungen eingefügt. Lieferungen von und zu Kunden und Lieferanten.
- Der Button "Lieferungen" in den Produkten und Produktvarianten benutzt den Filter Ein- und "Ausgang"

### 19.05.2015, 1.0.22
### equitania
#### Erweiterung
- Boolean Feld in die Lieferdetails eingefügt, wodurch die zu Liefernde Position abgeschlossen wird und im neuen Lieferschein nicht mehr aufgeführt ist.

### 19.05.2015, 1.0.21
### equitania
#### Erweiterung
- Button zum Öffnen der Ein-/Ausgangsrechnung in die Form Anischt der Produkte und Produktvarianten eingefügt.
- Anzeige der Rechnung

### 12.05.2015, 1.0.1
### eq_info_for_product_product
#### Bugfix
- Lieferanten für Produktvarianten lassen sich nun auch anlegen, wenn die id der Variante nicht als id für die Templates benutzt wird.

### 12.05.2015, 1.0.20
### equitania
#### Bugfix
- Fehlendes Hochkomma im Report "Angebotsanfrage" hinzugefügt.

### 05.05.2015, 1.0.19
### equitania
#### Erweiterung
- Beim Ein- und Verkaufsaufträgen wird als Beschreibung der Position ein Leerzeichen eingefügt, wenn für das Produkt keine Beschreibung hinterlegt ist. Dieses Leerzeichen wird auf den Reports nicht angezeigt.

### 05.05.2015, 1.0.18
### equitania
#### Bugfix
- Fehler behoben, bei dem man den Verkaufsauftrag aus dem Webshop nicht erstellen konnte.

### 05.05.2015, 1.0.17
### equitania
#### Erweiterung
- Einstellung in den Verkauf hinzugefügt, wordurch der Verkaufstext einer Position aus der internen Beschreibung des Produktes genommen wird.

### 05.05.2015, 1.0.16
### equitania
#### Bugfix
- Fehlerhafte Anzeige des Produktnummern Generators in den Einstellungen behoben.

### 04.05.2015, 1.0.15
### equitania
#### Bugfix
- Rechnungs und Lieferadresse im Angebot/Auftrag werden nicht mehr überschrieben, sondern abgeändert.

### 30.04.2015, 1.0.14
### equitania
#### Bugfix
- Fehler behoben, bei dem die neu eingefügten Felder auf den Report nicht angezeigt wurde.

### 30.04.2015, 1.0.13
### equitania
#### Änderung
- Icon für den Button "Preislistenpos." in der Form View des Produktes abgeändert.
#### Verbesserung
- Reports: Adressfelder für den Stadtteil und die Hausnummer eingefügt.
- Reports: Zweites Namensfeld eingefügt.
- Reports: Telefax(geschäftlich) in das Mitarbeiterobjekt eingefügt.

### 29.04.2015, 1.0.12
### equitania
#### Verbesserung
- Adressfelder für den Stadtteil und die Hausnummer zum Partnerobjekt hinzugefügt und die Formanischt überarbeitet. Zweites Namensfeld hinzugefügt.
- Feld Telefax(geschäftlich) in das Mitarbeiterobjekt eingefügt. 

### 24.04.2015, 1.0.11
### equitania
#### Verbesserung
- Produktnummern können in der Listenansicht der Produkt über den Button "Mehr/Produktnummer generieren" für die ausgewählten Produkte generiert werden.

### 24.04.2015, 1.0.10
### equitania
#### Verbesserung
- Produktnummerngenerierung kann in der Lagereinstellungen eignestellt werden.
- Wenn bei der Produktnummerngenerierung nur eindeutige Produktnummern erstellt werden können (min/max Prefixlänge = 0), dann wird die EAN13 des Produktes automatisch generiert.

### 20.04.2015, 1.0.9
### equitania
#### Bugfix
- Für zusätzliche Produkte, die nur im Lieferschein erfasst werden, wird nun die richtige Beschreibung benutzt.

#### Erweiterung
- Produkte werden standardmäßig nach der Produktnummer sortiert.

### 07.04.2015, 1.0.8
### equitania
#### Verbesserung
- In allen Reports haben nun die Spalten für Artikelnummer, Preis pro Einheit und Netto-Preis eine Mindestbreite.

### 01.04.2015, 1.0.7
### equitania
#### Bugfix
- Seriennummernmodul funktionsfähig gemacht.

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
- Optimiertung der Masken für Adressen, Produkte, Verkauf, Einkauf, Fertigung uvm.
- Die Anzeige in der Partnersuche des Verkaufsauftrag um den Adresstypen erweitert. Straße, Ort einstellbar
- In den Einstellungen wird der Reiter "Installierte Module" als erster Eintrag angezeigt und beim Öffnen aufgerufen
- Die Unternehmensmaske um 4 Felder, die in der Fußzeile der Reports angezeigt werden, und das Firmenlogo, welches auf dem Report aufgedruckt wird
- Die Debitoren- und Kreditorennummer mit Sequenzgenerator im Kunden/Lieferanten hinzugefügt
- Eigene Übersetzungslogik der Reports und Masken
- Internes und externes Papierformat wird gesetzt
- Das Feld "Vermittelt durch" in die Leads eingefügt. Enthält eine Beschreibung.
- Alle Auftragspositionen für Einkauf und Verkauf werden noch einmal in einer seperaten Maske(Liste, Form) angezeigt
- Lieferbedingungen in den Verkaufsauftrag eingefügt
- Die Suche nach einzelnen Positionen in Preisliste - Löschen über die Detailansicht - Widget in der Produktmaske
- Sachbearbeiter in den Verkaufsauftrag eingefügt, Verkäufer wird automatisch eingetragen (einstellbar)
- Eigene Logik für Tausender Serperatoren und Nachkommastellen für die Reports eingefügt (einstellbar)
- Dezimalstellen für Mengen, Gewichte und Preise für Einkauf, Verkauf und Fertigung separat einstellbar
- Liefertermin für Ein/Verkauf eingefügt. Wird auf Reports gedruckt (einstellbar KW/Datum)
- Kopftext für die Reports eingefügt
- Verbindung zwischen Verkaufsauftrag, Lieferschein und Rechnung hergestellt
- Leistungsdatum in Rechnung vom Lieferschein abgeleitet
- Produktbeschreibung wird für den Verkauf/Einkauf optimiert
- Positionsnummer eingefügt. Wird vom Verkaufsauftrag and den Lieferschein und die Rechnung übergeben
- Die Produktsuche erweitert, sodass nach der Referenz gesucht werden kann und diese auch angezeigt wird
- Kundenreferenz in die Listenansicht des Verkaufsauftrag und Suche nach der Kundenreferenz hinzugefügt
- 1:1 Verbindung zwischen Mitarbeitern und Benutzern hergestellt
- Überlieferungen werden in einer Position zusammengefasst (einstellbar)
- Stornieren von Lieferscheinen ohne Rechnung - neuer Lieferschein wird erstellt
- Wizard für das Ändern des Lieferdatums im Lieferschein eingefügt. Änderungsgrund muss angegeben werden und Änderung wird als Nachricht dokumentiert
- Button/Widget in die Produkte eingefügt, die die Preislistenpositionen anzeigen
- Feld für die Preislistenversion in die Preislistenposition eingefügt
- Steuer wird bei den Rechnungspositionen automatisch gesetzt, wenn eine Rechnung von einem Lieferauftrag erstellt wird, welcher keinen Bezug zu einem Verkaufs-/Einkaufsauftrag hat
- Fremdnr. bei Kontakt pflegbar - wird automatisch im Kundenauftrag in Referenznr. eingefügt

####Kontakt überarbeitet:

- Feld Vorname eingefügt
- Feld Geburtsdatum eingefügt
- Addresstyp um die Postfachaddresse erweitert
- Standard Liefer- und Rechnungsadresse kann festgelegt werden
- Ersteller des Datensatzes wird als Verkäufer eingetragen (einstellbar)


####Reports überarbeitet:

- Angebot
- Verkaufsauftrag
- Anfrage
- Bestellung
- Lieferschein
- Rechnung
- Neu:  Auftragspositionen
- Neu: Rücklieferschein
- Das "sale_layout" Modul intigriert, wodurch sich Positionen gruppieren lassen
