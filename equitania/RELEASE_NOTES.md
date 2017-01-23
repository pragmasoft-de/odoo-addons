## Modul equitania

### Unterstützung OpenSans Font

Dazu muss der Zeichensatz installiert werden.

Vorgehensweise unter Debian:

`wget https://release.myodoo.de/fonts/opensans.zip`

`unzip opensans.zip`

`mv opensans /usr/share/fonts/truetype/`

`rm opensans.zip`

`fc-cache -f -v`

#### 23.01.2017
### Version 1.1.132
#### CHG
- Das Feld eq_firstname ist ab jetzt auf der Detailansicht von res_partner immer eingeblendet

#### 19.01.2017
### Version 1.1.131
#### IMP
- Im Auftrag werden nun unter "Rechnungen anzeigen" auch Gutschriften aufgelistet.
#### FIX
- Report: Der Vor- und Nachname im Lieferscheint wird nur angedruckt, wenn es sich um kein Unternehmen handelt

#### 10.01.2017
### Version 1.1.130
#### CHG
- Reports Lieferschein: Captions für "Lieferadrese" wurden entfernt

#### 10.01.2017
### Version 1.1.129
#### ADD
- Reports: Es ist nun möglich ein Seitenumbruch vor dem Fußtext zu erzwingen

#### 04.01.2017
### Version 1.1.128
#### FIX    
- Korrektur für Textersetzung in Rechnungsreports


#### 03.01.2017
### Version 1.1.127
#### CHG    
- Anpassung für Einkaufspreise der Lieferanten: Dezimalstelleneinstellung über "Product Price Purchase"


#### 30.12.2016
### Version 1.1.126
#### FIX    
- Auskommentierung von "o.payment_term" wieder herausgenommen, da keine Zahlungskondition mehr angezeigt wurde 
- Auskommentierung von eq_ref_number Zeile 39 ff. rausgenommen (fehlt noch Logik)

#### 30.12.2016
### Version 1.1.125
#### FIX
- Abhängigkeit zum CK Editor 4 eingebaut (Fix für Kopf- und Fußtexte in Aufträgen) 


#### 28.12.2016
### Version 1.1.124
#### FIX
- Select Statements in der Funktion "_set_group_for_users" angepasst. Zusatz zu Version 1.1.120: uid wurde bisher zufällig gesetzt. Es wurde
ein Zusatz in das SQL Statement eingefügt, welches uid und gid gemäß des Sub-Selects korrekt setzt.

#### 13.12.2016
### Version 1.1.123
#### IMP
- Erweiterung um bessere Kontrolle von Context, damit man kein Fehler beim Aufruf der Importfunktion bekommt

#### 13.12.2016
### Version 1.1.122
#### CHG
- Steuerfreie Positionen werden jetzt auch in dem Rechnungsreport angezeigt (Ticket #3454).

#### 13.12.2016
### Version 1.1.121
#### FIX
- Bugfix der Funktion write(..), damit man beim Speichern eine Änderung unter Einstellungen kein Fehler mit KeyError 'lang' mehr bekommt.
 Ab jetzt wird kontrolliert ob dieser Wert überhaupt im Kontext vorhanden ist

#### 12.12.2016
### Version 1.1.120
#### FIX
- Select Statements in der Funktion "_set_group_for_users" angepasst. Jetzt wird die uid korrekt gesetzt (vorher wurde aufgrund der Reihenfolge 
fälschlicherweise die gid als uid verwendet).

#### 09.12.2016
### Version 1.1.119
#### FIX
- Korrektur der Lokalisierung für das Feld name, damit wir kein Problem mehr mit dem Modul web_translate haben

#### 08.12.2016
### Version 1.1.118
#### CHG
- Produkt-Einkaufspreis und Einkaufspreishistorie berücksichtigt nun den Dezimalstellen-Formatierer "Product Price Purchase"
- Abstand zwischen Einkaufspreis und dem Button "Preishistorie anzeigen" vergrößert


#### 28.11.2016
### Version 1.1.117
#### FIX
- Fehlerhafte Filterung nach Rahmenaufträgen unter "Auftragspositionen" entfernt.

#### 24.11.2016
### Version 1.1.116
#### FIX
- Attributstring wurde um neue Zeile erweitert, damit der Text wegen dem Standard "line.name.splitlines()[1:]" im Kern, korrekt angezeigt wird

#### 23.11.2016
### Version 1.1.115
#### IMP
- Erweiterung der Dokumentation bei der Funktion generate_line_text_with_attributes

#### 22.11.2016
### Version 1.1.114
#### IMP
- Erweiterung um neue Funktion generate_line_text_with_attributes() damit man im Text einer Bestellposition auch die Attribute der Varianten ausgeben kann

#### 15.11.2016
### Version 1.1.113
#### FIX
- eq_mail.py entfernt
- Abfrage der eq_mail.py in eq_mail_extension eingefügt (siehe ReleaseNotes).
- Grund: Durch Übernahme dieser Abfrage wird nun wieder gewährleistet, dass bei installiertem eq_mail_extension Modul auch die dazugehörige send Methode ausgeführt wird (vorher wurde die def send Methode vom Equitania Modul ausgeführt, diese ist nun aber nicht mehr vorhanden, da Übernahme der Logik in die def send des eq_mail_extension Moduls).

#### 11.11.2016
### Version 1.1.112
#### IMP
- Erweiterung der Tabelle res_country und Pflegemaske um neues Feld eq_active

#### 08.11.2016
### Version 1.1.111
#### CHG
- Anpassungen für überschriebene write-Methode für Produkte

#### 02.11.2016
### Version 1.1.110
#### FIX
- Unicode-Fehler bei Wareneingang buchen beseitigt. Außerdem einen Import für die Warning-Ausgabe hinzugefügt.

#### 02.11.2016
### Version 1.1.109
#### FIX
- Abfrage beim Einblenden der Attribute unter der product.product Tree View korrigiert, welcher bei der erstmaligen Initialisierung aufgetreten ist.

#### 26.10.2016
### Version 1.1.108
#### ADD
-  Die Spalte Attribute unter der product.product tree view lässt sich nun durch ein Flag in den Einstellungen ein- bzw. ausblenden.

#### 26.10.2016
### Version 1.1.107
#### CHG
- Der Reportzusatz "Angebot gültig bis" wird nichtmehr über ein Template manipuliert, welches für das Modul website_quote das Feld verschiebt 

#### 20.10.2016
### Version 1.1.106
#### CHG
- in der Produkt Template Tree View wurde der Status entfernt und hinter den tatsächlichen Bestand die Mengeneinheit gesetzt.
- In der Product Product Tree View wurde die Spalte "Attribute" entfernt.

#### 19.10.2016
### Version 1.1.105
#### CHG
- Feld für Anrede wird für Unternehmen nicht mehr ausgeblendet

#### 14.10.2016
### Version 1.1.104
#### ADD
- Unter dem Menüunterpunkt "Adressen" wird nun angezeigt, ob die Adresse ein Lieferant, Kunde, Interessent oder Chance ist.

#### 13.10.2016
### Version 1.1.103
#### FIX
- Das Feld "eq_house_no" wird nun auch bei der Umwandlung eines Interessenten zu einer Chance bei der Erstellung eines neuen Kunden mit übernommen.

#### 11.10.2016
### Version 1.1.102
#### CHG
- Zwei Hilfskommentare in den Templates der RechnungsReports hinzugefügt

#### 04.10.2016
### Version 1.1.101
#### FIX
- Beim Umwandeln einer Chance werden nun die gesetzten Felder wie Vorname, Nachname, Geburtstag etc. mit übernommen.

#### 30.09.2016
### Version 1.1.100
#### FIX
- Beim Anlegen eines Interessenten wurde nach der Auswahl eines Kunden die Hausnummer nicht mehr in das entsprechende Feld mit übernommen. Dies wurde nun durch die Hinzunahme des Feldes eq_house_no behoben.

#### 30.09.2016
### Version 1.1.99
#### ADD
- Unter der Rubrik "Chancen" einen SmartButton hinzugefügt, welcher direkt auf die Angebote des Ansprechspartners verweist.

#### 27.09.2016
### Version 1.1.98
#### FIX
- In der stock.py wurde eine Abfrage auf den Typ der Rechnung (Eingangs- oder Ausgangsrechnung) hinzugefügt, sodass die richitge Steuer gezogen werden kann.

#### 06.09.2016
### Version 1.1.97
#### Änderung
- Anpassung für Bestellreport


#### 06.09.2016
### Version 1.1.96
#### Änderung
- Neues Feld eq_name3 für Partner hinzugefügt


#### 01.09.2016
### Version 1.1.95
#### Änderung
- Erweiterung für Adresssuche (Ticket 1700)


#### 30.08.2016
### Version 1.1.94
#### FIX
- Lieferschein: Korrektur der Position der Anrede, bei kürzeren Company Adressen sowie eine IF-Abfrage für die c/o


#### 26.08.2016

### Version 1.1.93
#### FIX
- Anpassung für Modul equitania: weitere Felder werden nicht mehr ausgeblendet

### Version 1.1.92
#### FIX
- Verbesserung für Ausblenden von Elementen: Tab Warnings wird nicht mehr ausgeblendet


#### 25.08.2016
### Version 1.1.91
#### FIX
- Verbesserung für Ausblenden von Elementen für interne Nutzer wegen Fehler im Formular für Kontaktpersonen


#### 25.08.2016
### Version 1.1.90
#### FIX
- BugFix bei der name_search Methode, wleche alle product_template_id's eines Lieferanten lädt. Bei der Suche werden nun die product_template_id's verwendet (vorher product_id).

#### 23.08.2016
### Version 1.1.89
#### FIX
- Verbesserung für Ausblenden von Elementen für interne Nutzer (Reiter Maps und Geolocation)


#### 23.08.2016
### Version 1.1.88
#### FIX
- Verbesserung für Ausblenden von Elementen für interne Nutzer (Reiter Profiling)


#### 23.08.2016
### Version 1.1.87
#### FIX
- Reiter Finanzen wurde für Benutzer nicht angezeigt, welche nicht der Rechtegruppe Finanzen angehörten. Dadruch entstand nun der Fehler, dass der Reiter Finanzen für diese Benutzer nicht ausgeblendet werden konnte. Dies wurde nun behoben. 

#### 22.08.2016
### Version 1.1.86
#### CHG
- Ausblenden weiterer Felder und Tabs in Partnermaske für Benutzer


#### 22.08.2016
### Version 1.1.85
#### FIX
- Fehler für Auftragsmaske behoben


#### 19.08.2016
### Version 1.1.84
#### CHG
- Anpassungen der Partnermaske für interne Benutzer


#### 12.08.2016
### Version 1.1.83
#### CHG
- Setzen des Zugriffs für Menueinträge Personal und Berichtswesen über neue Gruppen



#### 01.08.2016
### Version 1.1.82
#### CHG
- Lieferschein-Anschrift: Wechsel der Positionen von Partner und Kunde in der Anschrift, wenn eine abweichende Lieferanschrift gewählt wurden.

#### 28.07.2016
### Version 1.1.81
#### CHG
- Ticket 1700: Defaultfilter für Adresssuche entfernt


#### 28.07.2016
### Version 1.1.80
#### CHG
- Übersetzung ergänzt (expiry date)

#### 19.07.2016
### Version 1.1.79
#### IMP
- der Klasse .returnaddress grundsätzlich Schriftgröße 7pt (von 5.5)gegeben. War sehr schwer zu lesen.(Adressfeld für eigene Adresse im Sichtfenster im Briefumschlag)

#### 01.07.2016
### Version 1.1.78
#### IMP
- Erweiterung der Logik für eq_head_text auf der Rechnung. Ab jetzt kann man mit dem "eq_use_text_from_order" steuern ob man den Default- oder Equitaniatext verwenden will

#### 01.07.2016
### Version 1.1.76
#### FIX
- Änderung für Ermittlung der Sprache

#### 30.06.2016
### Version 1.1.75
#### IMP
- Angebot & Rechnungen: Die Steuersätze welche in den Auftragspositionen ohne Wert sind (also mit 0,00 €) werden in der Zusammenrechnungen / Footer vom Report nicht mehr angezeigt

#### 30.06.2016
### Version 1.1.74
#### ADD
- Funktion in Auftragszeilenposition: Es ist nun möglich eine Auftragszeile (in Angebote oder Rechnungen) zu erstellen, ohne ein Produkt auszuwählen. Hierdurch können Beschreibungstexte trotzdem hinzugefügt werden, z.B. um ein Angebotstext auf der Folgeseite weiterführen zu können oder Ergänzungen hinzufügen zu können.

#### 28.06.2016
### Version 1.1.73
#### FIX
- Korrektur für Parameter default_get für sale.order.line

#### 28.06.2016
### Version 1.1.71
#### FIX
- Dekorator abgeändert

#### 24.06.2016
### Version 1.1.70
#### FIX
- Fehler, welcher beim Erstellen eines neuen Angebots auftrat, wurde behoben (local variable "currency_symbol" referenced before assignment). Die Variable "currency_symbol" musste initialisiert werden, falls keine Preisliste für das Produkt vorhanden ist.

#### 22.06.2016
### Version 1.1.69
#### Änderung
- Ticket 1700: Anpassungen für Adresssuche über Telefonnummer

### Version 1.1.68
#### Bugfix
- Optionale Positionen werden bei der Steuerberechnung des Reports beachtet. Werden nicht in die Summe einberechnet.

### Version 1.1.67
#### Bugfix
- Fehler des letzten Bugfixes aus der Version 1.1.66 trat auch beim Erstellen eines Angebotes auf. Selbe Lösung verwendet.



#### 21.06.2016
### Version 1.1.66
#### Bugfix
- Validation Period wurde als String 0.0 definiert und anschließend in ein Integer gecastet. Dies verursachte den Fehler "invalid literal for int() with base 10: '0.0'"
Lösung: Typecast nun in ein Float.


#### 16.06.2016
### Version 1.1.65
#### Änderung
- Erweiterungen für Adresssuche (Suche nach Schlagwörtern)


#### 09.06.2016
### Version 1.1.64
#### Bugfix
- Die Lieferantennummer im Menü "von Bestellpositionen" (Model: purchase.order.line) wird nicht in der Datenbank gespeichert.
Sollte ein Lieferant durch einen Benutzer verändert werden, der keinen Zugriff auf die purchase.order.line hat,
so kommt es zu einem Fehler, wenn die Lieferantennumemr geändert wird.


#### 07.06.2016
### Version 1.1.63
#### ADD
- Reports: Lieferschein, Angebote, Rechnung... enthalten in den Kopfdaten nun die Kunden Ust.ID.Nr, wenn dieser in der Steuerzuordnung als "Kunde Ausland mit UST-ID" gekennzeichnet wurde.

### Version 1.1.62
#### FIX
- Warning table "stock move" wurde durch einen erzeugten Index beim Feld 'name' verursacht (select=True). Wurde dementsprechend geändert, dass nun für das Feld "name" kein Index erstellt wird. 

#### 06.06.2016
### Version 1.1.61
#### Änderung
- Bei der offenen Menge des Smart Buttons "Verkäufe" im Produkt werden nun auch die noch offenen Lieferungen von abgeschlossenen Verkaufsaufträgen beachtet.


#### 03.06.2016
### Version 1.1.60
#### Änderung
- Das Feld "Lieferdatum" in den Auftragspositionen im Verkauf in "Lieferavis" umbenannt.


#### 01.06.2016
#### Version 1.1.59
##### ADD
- Bei den Email-Templates wird nun der ursprüngliche Editor durch ein anderes Widget verwendet. Dieses zeigt nur die "Source View".

### Version 1.1.58
#### Änderung
- Alle Benutzer haben nur die Leserechte für die Einträge in dem Menü "Auftragspositionen"

### Version 1.1.57
#### Bugfix
- Fehlenden Import eingefügt


#### 31.05.2016
#### Version 1.1.56
##### ADD
- Deutsche Übersetzung zur "Version Number" eingefügt.


#### 31.05.2016
#### Version 1.1.55
##### ADD
- Bei den Email Templates ein zusätzlichen Integer-Feld mit der Versionsnummer eingefügt.


#### 30.05.2016
#### Version 1.1.54
##### CHG
- Rechnungen und Angebote/Aufträge werden absteigend nach dem Datum sortiert dargestellt

#### Version 1.1.53
##### CHG
- Bei den Email Templates: Sales Order - Send by Email und Sales Order - Send by Email (Portal) zusätzlich noch ein noupdate="1" hinzugefügt. Somit werden diese Templates nach dem diese bearbeitet wurden nicht mehr durch ein Update überspielt.


#### 30.05.2016
#### Version 1.1.52
##### CHG
- Bei den Email Templates: Sales Order - Send by Email und Sales Order - Send by Email (Portal) ein forcecreate="False" hinzugefügt. Somit werden diese Templates nach dem diese gelöscht wurden bei einem Update nicht wieder erzeugt.

#### Version 1.1.51
##### FIX
- Fehlermeldung bei dem Druck von Ausgangsrechnungen tritt nun nicht mehr auf. Die Bedingung für das Ersetzen des Wertes und des Datums wird nun nur ausgeführt, wenn ein Wert in "Date" (Zahlungsfrist: Platzhalter für das Datum) und "Value" (Zahlungsfrist: Platzhalter für den entsprechenden Wert) vorhanden ist.


#### 25.05.2016
#### Version 1.1.50
##### Änderung
- Feldname angepasst.

#### Version 1.1.49
##### Bugfix
- Aktionen für die Smartbuttons überarbeitet.

#### Version 1.1.48
##### Bugfix
- Methode auf neue API umgeschrieben.

#### Version 1.1.47
##### Bugfix
- Fehlerhaftes Feld.

#### Version 1.1.46
##### Bugfix
- Fehlendes Feld eingefügt.

#### Version 1.1.45
##### Erweiterung
- Smartbuttons für Angebote und Aufträge in den Kunden eingefügt.

#### Version 1.1.44
##### Erweiterung
- Das Feld "Gültig bis" wird bei Aufträgen ausgeblendet.
- Es kann ein Zeitraum für die Gültigkeit eines Produktes definiert werden. Das Feld "Gültig bis" im Angebot wird entsprechend gesetzt.

#### Version 1.1.43
##### Erweiterung
- Beim "Anlegen" eines Kunden wird die Briefanrede direkt gesetzt. Wenn die Sprache eines Kunden auf Englisch gesetzt wird, so wechselt die Briefanrede auf "Dear ".


#### 25.05.2016
#### Version 1.1.42
##### Erweiterung
- Referenzbeleg wird in der Formansicht der Angebotsanfrage/Bestellung immer angezeigt.


#### 24.05.2016
#### Version 1.1.41
##### Erweiterung
- Attributwerte einer Produktvariante werden nun mit in den Positionstext (Beschreibung) eingefügt.

#### Version 1.1.40
##### Erweiterung
- Unterscheidung zwischen Rechnugnskorrektur und Gutschrift eingebaut.

#### Version 1.1.39
##### Bugfix
- Im Angebot/Auftrag werden die Kontakte auch über "Weitere Anzeigen" des DropDown des Partners angezeigt.


#### 23.05.2016
#### Version 1.1.37
##### Verbesserung
- Den Graph View für Lagerdetailbestände(stock.quants) abgeändert, sodass er bei großen Datenmengen noch zu öffnen ist.


#### 09.05.2016
#### Version 1.1.36
##### Änderung
- Formatierung eines Sql Queries angepasst


#### 04.05.2016
#### Version 1.1.35
##### Änderung
- Reports: Kundenreferenz und Auftragsnummer in der Rechnungsposition überarbeitet


#### 28.04.2016
#### Version 1.1.34
##### Neu
- Reports: Angebote und Rechnungen enthalten nun auf Auftragszeilenposition auch den tatsächlich errechneten Rabattwert in Klammern angezeigt


#### 28.04.2016
#### Version 1.1.33
##### Verbesserung
- Reports: Beschreibungstexte zu Artikeln sind auf den Angeboten und Rechnungen nun über mehrere Spalten breit.


#### 27.04.2016
#### Version 1.1.32
##### Verbesserung
- Reports: Anpassungen der Abstände von Grundelementen, nach der Anpassung für die neue StandardSchrift OpenSans


#### 27.04.2016
#### Version 1.1.31
##### Erweiterung
- Anzeige der Rabattwerte für sale_order und account_invoice


#### 27.04.2016
#### Version 1.1.30
##### FIX
- Schriftarten in den StandardReportsStyling auf "Open Sans" gestellt (diese Schriftart muss natürlich noch auf dem Server installiert sein)


#### 25.04.2016
#### Version 1.1.29
##### FIX
- Angebots-Report: Umbruch für das Lieferdatum wird nun auch bei langen Zeichnungsnummern korrekt gesetzt 


#### 25.04.2016
#### Version 1.1.28
##### Änderung
- Adresssuche: Verbesserungen für Rechteverwaltung und Ermittlung der Daten 


#### 25.04.2016
#### Version 1.1.27
##### Änderung
- Rechteverwaltung für Adresssuche 


#### 22.04.2016
#### Version 1.1.26
##### Änderung
- Erweiterungen für Adresssuche (Filter und Gruppierung)


#### 22.04.2016
#### Version 1.1.25
##### Änderung
- Anpassungen für Lieferscheinreport (Kopf- und Fußtexte)


#### Version 1.1.24
##### Erweiteurng
- Lieferscheinpositionen werden im Report nach den Sektionen aus dem Verkaufsauftrag gruppiert.


#### 22.04.2016
#### Version 1.1.23
##### Änderung
- Verkäufer und Sachbearbeiter werden bei einer Rechnungskorrektur übernommen.


#### 21.04.2016
#### Version 1.1.22
##### Änderung
- Anpassung für Kopf- und Fußtexte in den Einstellungen, damit diese über das neue Modul für die Dokumentenvorlagen angesprochen werden können


#### 21.04.2016
#### Version 1.1.21
##### FIX
- Lieferschein/Kommisionierungsauftrag wird übersetzt.


#### 21.04.2016
#### Version 1.1.20
##### ADD
- MwSt. Spalte auf Positionebene in Rechnungs- und Angebots-Reports, sobald 2 oder mehr unterschiedliche Steuern berechnet werden


#### 20.04.2016
#### Version 1.1.19
##### FIX
- Korrektur für Umwandlung eines Kunden in eine Chance


#### 20.04.2016
#### Version 1.1.18
##### FIX
- Lieferschein-Report: Wenn die Lieferadresse ein Kontakt war, wurde dessen Firma nicht angedruckt. Dies wurde behoben.


#### 20.04.2016
#### Version 1.1.17
##### Änderung
- Das Feld Pos für die Position eines Lagervorgangs sind bearbeitbar


#### 20.04.2016
#### Version 1.1.16
##### Erweiterung
- Übersetzung für den Report "Kommissionierungsschein" implementiert.


#### 19.04.2016
#### Version 1.1.15
##### Änderung
- Das Feld Kontakt-Name wird im Interessenten und der Chance angezeigt.
- Lieferscheinreport: Die Abstände zwischen PLZ und Ort, sowie zwischen Straße und Hausnummer wurde korrigiert.


#### 19.04.2016
#### Version 1.1.14
##### FIX
- Fehler durch nicht-definierte Ansicht behoben.


#### 18.04.2016
#### Version 1.1.13
##### Erweiterung
- Änderungen bezügl. Attributwerte auskommentiert.
- Unter Preislisten eine weitere Unterkategorie "Preislistenversionspositionen" hinzugefügt, welche alle Preislistenversionspositionen anzeigt.
- Hier nun auch Gruppierung nach Preislistenversion, Produkte, Regelbezeichnung, Produkt-Vorlage und Produktkategorie


#### 14.04.2016
#### Version 1.1.12
##### Erweiterung
- Attributwerte der Produktvariante werden nun unter der Produktvariante angezeigt und wurden beschreibbar gemacht (im Kern war dies schon vorhanden aber nur readonly, außerdem wurden die Attributwerte durch das Equitania-Paket ausgeblendet).
- Sequenz bei den Attributen eingefügt, Logik von eq_website_customerportal ins Equitania-Modul verschoben, um ein doppeltes Feld zu vermeiden.


##### Änderung
- Das Feld "Vermittelt durch" im Interessenten/Chance umbenannt, sodass die Bezeichnung nun eindeutig ist.


#### 12.04.2016
#### Version 1.1.11
##### Erweiterung
- Ticket 1700: Erweiterung für Suche über alle Adresstabellen und Korrektur für Query für Ermittlung der Daten 


#### Version 1.1.10
##### Fix
- Übersetzung für "Vermittelt durch" angepasst.


#### 12.04.2016
#### Version 1.1.9
##### Fix
- Übersetzung angepasst.


#### 11.04.2016
#### Version 1.1.8
##### Erweiterung
- Ticket 1700: Begonnen mit Erweiterung der Suchfunktion für Adressen


#### Version 1.1.7
##### Erweiterung
- Kundenreferenz und Auftrags-Nr wird in der Position dargestellt. Für den Rechnungsreport.


#### Version 1.1.6
##### Fix Übersetzung


#### 08.04.2016
#### Version 1.1.5
##### Erweiterung
- Ticket 2513: Button "Anlegen" für Positionsansicht wurde entfernt (führte zur Anlage von Positionen ohne Auftragskopf
- Ticket 2534: Neues Feld für Anzeige des Produkttemplates (für automatische Erzeugung des Templates über die Varianten)


#### Version 1.1.4
##### Änderung
- Rechnungs-Report enthält nun bei dem Summenblock die Möglichkeit für die Anzeige mehrerer Steuersätze (z.B. 19% + 7% usw.)


#### Version 1.1.4
##### Änderung
- Bestellung-Report enthält nun bei dem Summenblock die Möglichkeit für die Anzeige mehrerer Steuersätze (z.B. 19% + 7% usw.)


#### Version 1.1.3
##### FIX
- Steuern werden richtig berechnet und angezeigt.


#### Version 1.1.2
##### Änderung & FIX
- FIX: Abstände in den Adressanschriften für Hausnummer und PLZ wurden korrigiert
- Änderung: Angebots-Report enthält nun bei dem Summenblock die Möglichkeit für die Anzeige mehrerer Steuersätze (z.B. 19% + 7% usw.)


#### 03.04.2016
#### Version 1.1.1
##### Fix
- Die Lieferanschrift in der Rechnung und dem Angebot/Auftrag angepasst.


#### 03.04.2016
#### Version 1.1.0
##### FIX Übersetzungen


#### 01.04.2016
#### Version 1.0.180
##### FIX
- Nummerngenerator bei Produkten: Fehler abgefangen (def eq_product_number_update), wenn Trennzeichen nicht gesetzt. Außerdem ist der aneinandergekettete String nun Leerzeichen frei (Separator kann kein Leerzeichen sein).


#### 31.03.2016
#### Version 1.0.179
##### Erweiterung
- Erweiterung um "Seitenumbruch nach Kopftext" --> Einkaufsbelege


#### 30.03.2016
#### Version 1.0.178
##### Änderung
- Textänderung -> den Text "[equitania]" zeigen wir bei der Erweiterung "Seitenumbruch nach Kopftext" icht mehr an


#### 30.03.2016
#### Version 1.0.177
##### Erweiterung
- Erweiterung um "Seitenumbruch nach Kopftext" --> Verkaufsbelege (Angebot, AB und Rechnung)


#### 29.03.2016
#### Version 1.0.176
##### Änderung
- Einkaufsreport auf die neuen Templates umgestellt


#### Version 1.0.175
##### Erweiterung
- Methode create(...) der Klasse "stock_picking_extension" erweitert. Ab jetzt ist Verlinkung auf sale_order im Feld eq_sale_order gespeichert


#### 29.03.2016
#### Version 1.0.174
##### Fix
- In der res_partner.py bei der Funktion _address_fields: append() mit extend() ersetzt, da mehrere Argumente einer Liste hinzugefügt werden sollen.


#### 26.03.2016
#### Version 1.0.173
##### Änderung
- Abhängigkeit zu account_cancel ergänzt, da dies immer gebraucht wird


#### 24.03.2016
#### Version 1.0.172
##### Änderung
- Produktvorlage wird in der Formansicht de Produktvariante angezeigt
- Lieferschein-Report um eine ID erweitert und einen fixen Abstand ersetzt


#### Version 1.0.171
##### Änderung
- Anpassung für Rechnungen


#### Version 1.0.170
##### Fix
- Korrektur für Übersetzungen


#### 23.03.2016
#### Version 1.0.169
##### Änderung
- Verschieben von Rechnungspositionen
- Suche für Chancen angepasst


##### Änderung
- Stadtteil wird übernommen, wenn der Haken bei "Unternehmensanschrift verwenden" gesetzt wird.
- Stadtteil und Hausnummer werden für bestehende Kontakte übernommen.

#### Version 1.0.169
##### Änderung
- Hausnummer wird übernommen, wenn der Haken bei "Unternehmensanschrift verwenden" gesetzt wird.


#### 23.03.2016
#### Version 1.0.168
##### Änderung
- Übersetzung angepasst
- Lieferschein-Report wurde um eine CSS Klasse erweitert


#### 22.03.2016
#### Version 1.0.167
##### Erweiterung
- Konfigurationsmöglichkeit für manuelles Setzen der Positionsnummer


#### 21.03.2016
#### Version 1.0.166
##### Änderung
- Telefon, Fax und Mail aus der Formansicht der Benutzer entfernt.
- Produktbeschreibung wird in der Position geändert, sobald das Produkt geändert wird.


#### 18.03.2016
#### Version 1.0.165
##### Änderung
- Verbesserung für Übersetzung


#### 18.03.2016
#### Version 1.0.164
##### Änderung
- Anpassungen der Ansicht für Angebotserstellung


#### 18.03.2016
#### Version 1.0.163
##### Fix
- Korrektur für Reportnamen


#### 18.03.2016
#### Version 1.0.162
##### Fix
- Korrektur für __openerp__.py


#### 17.03.2016
#### Version 1.0.161
##### Änderung
- Reports für Renner-/Pennerliste


#### 16.03.2016
#### Version 1.0.160
##### Fix
- Rechnung-Reports: Übersetzungskorrekt für das Lieferdatum


#### 15.03.2016
#### Version 1.0.159
##### Fix
- Hausnummer der Firma wird im Partnerdatensatz gespeichert, genau wie der Rest der Adresse.
- Reports: Die Absendeadresse greift nun direkt auf die Firmendaten, und nichtmehr auf den Partner darunter


#### 09.03.2016
#### Version 1.0.158
##### Änderung
- Erweitern der Lieferscheine um eine ID


#### 07.03.2016
#### Version 1.0.157
##### Bugfix
- Fehler im SQL-Statement in der Funktion _eq_sale_count(...) behoben. Jetzt kann man neue Produkte speichern


#### 07.03.2016
#### Version 1.0.156
##### Bugfix
- Fehler in der Funktion calculate_sum(..) beseitigt. Bei der Rechnungsposition gibt es das Feld eq_optional und product_uom_qty nicht


#### 04.03.2016
#### Version 1.0.155
##### Erweiterung
- Erweiterung der Basisklassen für Sale-Reports um 2 neue Funktion (GetUserInfo und GetUserSignature). Die Funktionen sind im ReportHelper


#### 03.03.2016
#### Version 1.0.154
##### Änderung
- Übersetzung angepasst.


#### Version 1.0.153
##### Änderung
- Incoterm wird zu Incoterm übersetzt.



#### 02.03.2016
#### Version 1.0.152
##### Fix
- Offene Menge der Verkäufe im Produkt wird richtig berechnet.


#### Version 1.0.151
##### Fix
- Offene Menge bei der Verkaufspositionen wird richtig berechnet.


#### Version 1.0.150
##### Fix
- Die Methode product_id_change kann ohne context aufgerufen werden.


#### 01.03.2016
#### Version 1.0.149
##### Fix
- Im Lieferschein wird die Produktbeschreibung als Text gespeichert, wodurch die Formatierung nicht verloren geht.


#### Version 1.0.148
##### Fix
CRM/Lead/Interessent
- "Unternehmensanschrift verwenden" wird nun standard gesetzt 


#### Version 1.0.147
##### Fix + Erweiterung
CRM/Lead/Interessent
- Übersetzungen nachgepflegt (auch Placeholder)
- Feldvergrösserung
- Hausnummer
- PLZ, Stadt, Stadtteil untereinander
- Feld Stadtteil hinzugefuegt
- Neue Felder bei Wandlung zum Kunden berücksichtigt
- Disctrict in District umbenannt


#### Version 1.0.146
##### Fix
- Dateinamen geändert, sodass die ungenaue Suche funktioniert.

#### 29.02.2016
#### Version 1.0.145
##### Erweiterung
- Selectionen für den Report können übersetzt werden. Menüeintrag umbenannt in "Report Sektionen".


#### Version 1.0.144
##### Erweiterung
- Ungenaue Suche für die standard und erweiterte Suche eingebaut.
- Beschreibung:
- Um alle Kunden zu finden, die sich im PLZ Bereich 75XXX befinden, müssen man bei der Suche "|75%" eingeben.
- Das Zeichen "|" (Pipe) gibt an, dass die Zeichen "%" und '_' anders interpretiert werden. Das Prozentzeichen "%" steht für eine unbestimmte Anzahl beliebiger Zeichen
- und der -Unterstrich "_" für genau ein beliebiges Zeichen.


#### Version 1.0.143
##### Änderung
- Vor- und Zuname der Chance aus dem eq_bms Modul umgezogen.


#### 25.02.2016
#### Version 1.0.142
##### Änderung
- Anpassung für Zusammensetzen des Beschreibungstextes der Produkte in Angeboten
##### Bugfix
- Fehler auf der Rechnung mit Sektionen korrigiert


#### 24.02.2016
#### Version 1.0.141
##### Erweiterung
- Die Maske "User -> Einstellungen ->" um neue Image Feld für Unterschrift erweitert 


#### 24.02.2016
#### Version 1.0.140
##### Fix
- Die Benutzergruppe "Reiter Beschaffung in den Produkten anzeigen" hat bei manchen Systemen nicht funktioniert.


#### 16.02.2016
#### Version 1.0.139
##### Erweiterung
- Richtige Übersetzung für das Feld "Bundesland" des Interessenten eingefügt.
- SaleOrderReport: Kleine Anpassung für die Kopfzeile bei Rabatten


#### 15.02.2016
#### Version 1.0.138
##### Erweiterung
- Report Sale Order: Erweitern von zwei CSS Klassen für weitere Änderungen an Reports


#### 12.02.2016
#### Version 1.0.137
##### Fix
- Richtigen Helptext für die Benutzergruppe Lieferanten einblenden eingefügt.


#### 10.02.2016
#### Version 1.0.136
##### Erweiterung
- Erweiterung der Funktionalität für Rechnung (Kopf- und Fußtext) für den Fall "Rechnung direkt unter Ausgangsrechnungen erstellen"


#### 10.02.2016
#### Version 1.0.135
##### Erweiterung
- Erweiterung der Funktionalität für Rechnung (Kopf- und Fußtext) für den Fall "Rechnung auf Basis Auslieferung" 


#### 10.02.2016
#### Version 1.0.134
##### Erweiterung
- Erweiterung der Funktionalität für Zahlungsbedingungen (Wildcards)
- Erweiterung der Funktionalität für Rechnung (Kopf- und Fußtext)


#### 09.02.2016
#### Version 1.0.133
##### Änderung
- Rück-Lieferschein auf die neue Variante umgebaut


#### 04.02.2016
#### Version 1.0.132
##### Änderung
- Report Papierformat geändert: Die Maße für den Kopfbereich der Papierformate wurde aktualisiert, Neu:
> Kopfrand (headerspacing) = 49
> Kopfzeilenabstand (margin_top) = 49


#### Version 1.0.131
##### Änderung
- Die Felder für Telefon, Mobil und Fax werden direkt im Benutzer angezeigt.


#### 03.02.2016
#### Version 1.0.130
##### Änderung
- Verkauf/Einkauf/Rechnung: Kopf- und Fußtext in separate Reiter eingefügt. Kontaktperson zu Sachbearbeiter umbenannt.
- Verkauf/Rechnung Einkäufer unter den Sachbearbeiter gefügt.


#### Version 1.0.129
##### Änderung
- Reports Verkauf/Rechnung: Statt dem Sachbearbeiter, den Verkäufer in den Kontaktinformationen drucken


#### 02.02.2016
#### Version 1.0.128
##### Fix
- Lieferschein Reports:
> Abschluss vom Standard-Umbau
> FIX vom ReportHeader für Lieferscheine
> FIX von der Übersetzung für Lieferscheine


#### 29.01.2016
#### Version 1.0.127
##### Fix
- Rechnungs-Report: Zeigt nun auch korrekt die abweichende Lieferanschrift im unteren Report-Bereich für Kontakte
##### Änderung
- Verkaufs-Report: wurde erweitert für die neue Briefpapier-Variante
- Umstellung der Lieferschein-Reports auf die neue Variante, damit es später für Briefpapiere auch verwendet werden kann


#### 28.01.2016
#### Version 1.0.126
##### Fix
- Nicht übermittelten Code eingefügt.


#### Version 1.0.125
##### Fix
- Titel + Name wird für Endkunden in der Suche angezeigt.


##### Erweiterung
- Lieferscheine Reports: Erweitern um die Logik ob die Rechnungsadresse ein Kontakt ist oder nicht, entsprechend auch Name und Titel abbilden.


#### 21.01.2016
#### Version 1.0.124
##### Fix
- Übersetzungsfehler (ID für Templates) korrigiert


#### 20.01.2016
#### Version 1.0.123
##### Erweiterung
- Der Menüpunkt "Lieferanten" ist nur für die neu erstellte Gruppe "Bereich 'Lieferanten' in Finanzen anzeigen" sichtbar. Standardmäßig für alle Benutzer aktiviert.


#### Version 1.0.122
##### Änderung
- Änderung der Lokalisierung von Lieferschein


#### 19.01.2016
#### Version 1.0.121
##### Änderung
- Die Beschränkung der Liefer- und Rechnnugsadresse ins equitania_limit_address_sale Modul ausgelagert und über die Einstellungen installierbar gemacht.


#### 19.01.2016
#### Version 1.0.120
##### Erweiterung
- Suche nach "Vermittelt durch" in die Interessenten und Chancen eingefügt..


#### 18.01.2016
#### Version 1.0.121
##### Erweiterung
- Vorbereitung für neue Report-Header (invoice und saleorder umgestellt)


#### 18.01.2016
#### Version 1.0.120
##### Fix
- Zugriffsrechte für die Preishistorie hinzugefügt.


#### 15.01.2016
#### Version 1.0.119
##### Erweiterung
- Anpassung des Mailversandes: gültige E-Mailadresse für Return-Path
- Report Headers um eine CSS Klasse erweitert für bessere Änderungen im Headerbereich


#### 14.01.2016
#### Version 1.0.118
##### Erweiterung
- Preishistorie für den Anschaffungspreis eingefügt.


#### 11.01.2016
#### Version 1.0.117
##### Verbesserung
- Lokalisierung für "Delivery note" erweitert


#### 7.01.2016
#### Version 1.0.116
##### Änderung
- Die Gruppe "Lagerort" auf der Lasche "Bestand" wurde für Produkte und Varianten ausgeblendet


#### 4.01.2016
#### Version 1.0.115
##### Änderung
- Fehlende Datei eq_sale_order_action_data.xml hinzugefügt


#### 23.12.2015
#### Version 1.0.114
##### Änderung
- Anzeige des Lieferdatums für Positionen in Auftragsformular


#### 22.12.2015
#### Version 1.0.113
##### Änderung
- Änderung der Email-Vorlagen


#### 22.12.2015
#### Version 1.0.112
##### Änderung
-  Email-Vorlage für unsere englische Version von "Send by Email (Online Quote)" hinzugefügt - auch mit funktionierendem Feld eq_house_no


#### 22.12.2015
#### Version 1.0.111
##### Änderung
- Anrede für Firmen geändert


#### 22.12.2015
#### Version 1.0.110
##### Änderung
- Anrede "Hello" auf "Dear" geändert


#### 22.12.2015
#### Version 1.0.109
##### Erweiterung
- Anrede wird ab jetzt in beiden Sprachen mit dieser Logik gesetzt:
1. res_partner is company => Sehr geehrte Damen & Herren,
2. res_partner is not company => oder Sehr geehrte(r)


#### 22.12.2015
#### Version 1.0.108
##### Erweiterung
-  Email-Vorlage für unsere englische Version von "Sale Order Portal" hinzugefügt - endlich auch mit funktionierendem Feld eq_house_no

! Wichtig ! Damit es korrekt funktioniert, muss man diese Schritte ausführen:
1. Das Modul portal_sale deinstallieren und gleich nochmal installieren
2. Update mit -u equitania ausführen
3. Jetzt sind alle Änderungen da


#### 22.12.2015
#### Version 1.0.107
##### Erweiterung
- Email-Vorlage für unsere englische Version von "Sale Order Portal" hinzugefügt. Im Moment aber wegen einem Fehler in der Vererbung deaktviert 


#### 21.12.2015
#### Version 1.0.106
##### Bugfix
- Benutzergruppe "Reiter 'Beschaffung' im Produkt anzeigen" wird beim Update oder der Installation für alle Benutzer gesetzt.


#### 17.12.2015
#### Version 1.0.106
##### Erweiterung
- Email-Template für Bestellbestätigung (Portal) verbessert


#### Version 1.0.102
##### Verbesserung
- Texte aus Auftrag und Bestellung in Rechnung übernehmen


#### 17.12.2015
#### Erweiterung, 1.0.105
- Der Reiter "Beschaffung" kann über die Gruppen ausgeblendet werden.


#### Bugfix, 1.0.104
- Fehlende Datei hinzugefügt.


##### Bugfix, 1.0.103
- Fehlerhafte compute function überarbeitet.


##### Bugfix, 1.0.102
- Durchschnittspreis im "Berichtswesen/Einkauf/Statistik Einkauf" wird wie folgt berechnet (Gesamtpreis/Menge).


#### 15.12.2015
#### Version 1.0.101
##### Bugfix
- Lieferant wird in der Ausgangsrechnung richtig dargestellt.


#### 10.12.2015
#### Version 1.0.100
##### Bugfix
- context wird in der Methode "_get_items_from_po" erwartet.


#### Version 1.0.99
##### Änderung
- Werte für die stock_transfer_details_items werden in einer separaten Methode erstellt, damit es in der Vererbung verändert werden kann.


#### Version 1.0.98
##### Bugfix
- Deutsche Übersetzung für "Only show Products of selected supplier [equitania]" eingefügt.


#### 04.12.2015
#### Version 1.0.97
##### Erweiterung
- Produkt- und Lieferantenfilterung, anhand der Lieferanten in den Produkten, in die Anfragen und Bestellungen eingefügt. Lässt sich über die Einstellungen aktivieren. Funktioniert nur für Anfragen und Bestellungen, die nach der Aktivierung erstellt wurden.


#### 04.10.2015
#### Version 1.0.96
##### Erweiterung
- Lieferschein: Ab jetzt zeigen wird bei der Adresse diese Felder: Anrede, Vorname und Nachname


#### 30.11.2015
#### Version 1.0.95
##### Erweiterung
- Footer: Die feste Bezeichnung "Geschäftsführer" ist nun entfernt, stattdessen heißen Zusatzfeld 1-4: nun Bezeichnung (z.b. Geschäftsführer) und 1. - 3. Person für den Report
INFO: Ggf. muss man im Backend eine "Übersetzung laden" für die deutsche Sprache um die neuen Bezeichnungen zu erhalten.


#### 12.11.2015
#### Version 1.0.94
##### Erweiterung
- Deutsche Übersetzung für den Menüpunkt "Bestellpositionen" hinzugefügt.


#### 05.11.2015
#### Version 1.0.93
##### Fix
- Deutsche Übersetzung für die Kundennummer im Angebot/Auftrag hinzugefügt.


#### 05.11.2015
#### Version 1.0.92
##### Verbesserung
- Reports: Referenzeinträge des Kunden können nun nur noch 2 Zeilen in der Länge betragen (inkl. Umbruch im Report). Alles was zu viel ist, wird abgeschnitten, damit der Report korrekt angezeigt bleibt und die Anschrift nicht abgeschnitten wird.


#### 29.10.2015
#### Version 1.0.91
##### Erweiterung
- Kennzeichnung der Felder, die nur für die Variante gelten, eingefügt.


#### Version 1.0.90
##### Erweiterung
- Kundennummer über den Kunden im Verkaufsauftrag eingefügt.


#### 28.10.2015
#### Version 1.0.89
##### Bugfix
- Beim Ändern des Kunden im Angebot/Verkaufsauftrag kann False nicht mehr als context übergeben werden.


#### 26.10.2015
#### Version 1.0.88
##### Erweiterung
- Listen- und Formansicht für das Feld "Vermittelt durch", welches sich im Kunden und Chance/Interessent befindet, eingefügt.


##### Bugfix
- Option "Suche nur nach Firmen in den Angeboten und Verkaufsaufträgen [equitania]" im Einkauf


#### 19.10.2015
#### Version 1.0.87
##### Änderung
- Abhängigkeiten korrigiert.


#### 19.10.2015
#### Version 1.0.86
##### Änderung
- Abhängigkeiten zum 'website', 'website_report', 'website_quote', 'eq_quotation_enhancement' Modul hinzugefügt.

#### 16.10.2015
#### Version 1.0.85
##### Bugfix
- Reports mit Positionen ohne Steuer konnten nicht generiert werden.


#### 14.10.2015
#### Version 1.0.84
##### Bugfix
- Alle Benutzer, die Zugriff auf die Produkte haben, können die Produktnummerfolge generieren.


#### 12.10.2015
#### Version 1.0.83
##### Erweiterung
- Defaultwerte der Maske "Pricelist items" werden ab jetzt gesetzt
- Änderung der Funktion "product_id_change". Ab jetzt wird der Produkttext nur einmal gesetzt und wird nach der Änderung der Menge nicht mehr ersetzt


#### 09.10.2015
#### Version 1.0.82
##### Erweiterung
- Ab jetzt kann man auf der Maske "Benutzer" den zugehörigen Partner auswählen. Es ist nicht mehr readonly
- Der Preis "price_surcharge" wird ab jetzt auch in der Tabelle "Pricelist Items" in neuer Spalte "Preis" angezeigt


#### 02.10.2015
#### Version 1.0.81
##### Erweiterung
- Die Tabelle product.product um neues Feld eq_sale_min_qty erweitert
- Die Maske "Variante - Productdetail" um das Feld eq_sale_min_qty erweitert


#### 02.10.2015
#### Version 1.0.80
##### Erweiterung
- Methode zum Löschen unnötiger Einträge überarbeitet.


#### 01.10.2015
#### Version 1.0.79
##### Erweiterung
- Methode zum Löschen unnötiger Einträge in der ir_model_data Tabelle erweitert, sodass nun auch nicht installierte Module aus der ir_module_module Tabelle entfernt werden.


#### 01.10.2015
#### Version 1.0.78
##### Erweiterung
- Methode eingefügt, die unnötige Einträge in der ir_model_data Tabelle entfernt.


#### 01.10.2015
#### Version 1.0.77
##### Bugfix
- Gruppeneinschränkung für den Menüeintrag "Einstellungen/Projekte" entfernt, da die Installation des Modules "Projekte" keine Voraussetzung für dieses Modul ist.


#### 30.09.2015
#### Version 1.0.76
##### Bugfix
- Fehlende PLZ in der Infozeile bei der Rechnungsadresse auf der Masken (Angebotsanfrage und Auftrag) korrigiert


#### 30.09.2015
#### Version 1.0.75
##### Erweiterung
- Wichtige Kontrolle für Auswertung des Feldes eq_house_no hinzugefügt
- Strasse, Hausnummer, PLZ, Ort und Land wird ab jetzt auch auf diesen Masken angezeigt (Angebotsanfrage, Bestellung, Eingangsrechnung, Ausgangsrechnung, Auftrag)
- Default Widget wurde deaktiviert


#### 29.09.2015
#### Version 1.0.74
##### Bugfix
- Bugfix im Report "eq_report_sale_order" in der Berechnung für optionale Positionen


##### Erweiterung
- Hausnummer auf der Maske SaleOrder (Angebot, Vertrag) etc. wird jetzt bei der Lieferadresse und Rechnungsadresse angezeigt


#### 18.09.2015
#### Version 1.0.73
##### Bugfix
- Bei der Funktion "Lieferung stornieren" wurden für die Rücklieferung andere Quants genommen. Nicht die der Lieferung.


#### 18.09.2015
#### Version 1.0.72
##### Bugfix
- Die action_button_conifrm Methode im Verkaufsauftrag wird richtig aufgerufen.


#### 15.09.2015
#### Version 1.0.71
##### Erweiterung
- Erweiterung der Reportlogik für alle Belege im Verkauf (optionale Positionen und Bruttopreis)


#### 14.09.2015
#### Version 1.0.70
##### Bugfix
- Fußtext wird in der Formansicht der Ein-/Ausgangsrechnung richtig dargestellt.


#### 11.09.2015
#### Version 1.0.69
##### Bugfix
- Änderung an einer XML Datei auskommentiert, welche das knowledge Modul benötigt.


##### Erweiterung
- Erweiterung in Darstellung von "Nachname, Vorname" für Kunden mit dem Flag "is_company=False" im Treeview und Kanban


#### 10.09.2015
#### Version 1.0.68
##### Erweiterung
- Deutsche Übersetzung für den UVP eingefügt.


#### 09.09.2015
#### Version 1.0.67
##### Erweiterung
- Den UVP(RRP) in die Produktvarianten eingefügt.


#### 08.09.2015
#### Version 1.0.66
##### Erweiterung
- Wichtige Änderung in der eq_res_users. Ab jetzt wird keine Funktion copy(...) mehr ausgeführt. Es hat nur zu einem Problem mit SignUp geführt.
- Wichtige Änderung in der eq_res_users_new_api. Neue Version funktioniert nach dem Refactoring von eq_res_users korrekt im Webshop und auch in der Anpassung für Illingen


#### 02.09.2015
#### Version 1.0.65
##### Bugfix
- Kreditoren- und Debitorennummer wird in der Kanban Ansicht und den Feldern für Partner richtig dargestellt.
##### Änderung
- Fußtext in der Formansicht für Ein-/Ausgangsrechnungen auf die gesamte Breite erweitert.


#### 31.08.2015
#### Version 1.0.64
##### Erweiterung
- Ab jetzt kann man auf der Maske "Verkauf - Kunden" auch nach eq_name2 suchen
- Bei Anlage eines Benutzers wird ab jetzt immer geprüft ob es bereits Kunden mit der E-Mail Adresse gibt. Falls ja, wird gleich die Verlinkung zwischen dem Benutzer und Kunden gesetzt.


#### 21.08.2015
##### Bugfix, 1.0.63
- Benutzer können wieder kopiert werden.


#### 19.08.2015
##### Erweiterung, 1.0.62
- Optionale Positionen in die Auftragspositionen eingefügt.
-- In der Listenansicht im Angebot werden die optionalen Positionen blau dargestellt.
-- In dem gedruckten Angebot werden die Zwischensummen der optionalen Positionen in Klammern dargestellt.


#### 17.08.2015
##### Änderung, 1.0.61
- Reports: Die Positionen und Schriftgröße der Reports wurde angepasst um potentielle Fehler vorzubeugen


#### 13.08.2015
##### Bugfix, 1.0.60
- Die Felder "Belegnr. des Kunden" und "Referenz / Beschreibung" werden bei allen Abrechnungstypen richtig erfasst.


#### 11.08.2015
##### Bugfix, 1.0.59
- Neues Addon: Snom-Telefonunterstützung. Es können direkt Telefonate aus dem Kundenstamm gestartet werden.


#### 10.08.2015
##### Bugfix, 1.0.58
- Überlieferung wird auch zusammengefasst, wenn ein Produkt nur teilweise verfügbar ist.


#### 06.08.2015
##### Erweiterung, 1.0.57
- Das Feld "Vermittelt durch" ist ab jetzt auch bei Kunden, deren Kontakten und bei Interessenten
- Alle Klassen in der Datei eq_lead_referred.py wurden auf neue API umgestellt
- Die DE.PO Datei wurde um neuen Eintrag erweitert. Diesmal habe ich es wirklich manuell gemacht


#### 03.08.2015
##### Änderung, 1.0.56
- Abstände von Zahlungskonditionen, Lieferbedingungen, Rechnungsanschrift und Lieferanschrift am Fuß von Rechnungen, Angeboten und Einkäufen verbessert.

#### 29.07.2015
##### Änderung, 1.0.55
- Lieferscheinnummer wird in der Rechnung unter jeder Position angezeigt.


#### 29.07.2015
##### Erweiterung, 1.0.54
- id für ein td Element eingefügt


##### BUGFIX, 1.0.53
- Fehlerhafte Abfrage überarbeitet, wodurch vorher keine Lieferung durchgeführt werden konnte, wenn Überlieferungen in einer Position angezeigt werden sollten.
- Verkaufseinheit in der Verkaufsposition wird beim Ändern der Menge abgeändert.

##### Erweiterung
- Fußtext (Notiz/Geschäftsbedingung) im Verkauf/Einkauf von der Darstellung in der Form und den Report überarbeitet.
-- Report: Direkt unter die Positionen und ohne der Information "Notiz".
-- Form: Feld wird auf der ganzen Breite angezeigt.


##### BUGFIX, 1.0.52
- Übersetzungsfehler in Reports behoben.


#### 23.07.2015
##### BUGFIX, 1.0.51
- Fehler behoben, der Auftritt wenn bereits erstellte Lieferungen geliefert werden.


#### 23.07.2015
##### Änderung, 1.0.49
- Ansicht der Partner angepasst.
- Schlagworte auf volle Breite.
- Briefanrede nach dem Geburtstag
- Übersetzung angepasst.


##### Änderung, 1.0.50
- Startwert der Sequenz der Debitoren-/Kreditorennummer um 1 erhöht.


#### 22.07.2015
#### Version 1.0.48
##### Änderung
- Den Fix für die Leerzeichen in die Reports direkt eingefügt.
- Briefanrede zu den Kontakten hinzugefügt.


#### 21.07.2015
#### Version 1.0.47
##### Erweiterung
- Positionen beim Liefern haben einen direkten Bezug zu den Lieferscheinpositionen.


#### 17.07.2015
#### Version 1.0.46
##### Bugfix
- Hausnummer des Unternehmens in die Reports eingefügt.


#### 10.07.2015
#### Version 1.0.45
##### Bugfix
- Die offene Menge der Verkäufe bei den Produkten und Produktvarianten zeigt nun den richtigen Wert.


#### 07.07.2015
#### Version 1.0.44
##### Bugfix
- Feld eq_qty_left als float erfasst.
#####Erweiterung
- Kopf- und Fußtext auf html umgestellt.


#### 07.07.2015
#### Version 1.0.43
##### Bugfix
- Der Text zum einfügen eines Snippets wird im report nicht angezeigt.


##### Erweiterung
- Kopftext auf html umgestellt.
- Geschäftsbedingungen auf html umgestellt.


#### 29.06.2015
##### Bugfix, 1.0.42
- Übersetzung für Webseiten und Reports überarbeitet. Manche Begriffe wurden nicht übersetzt.


#### 23.06.2015
##### Bugfix, 1.0.41
- Eins zu Eins Beziehung zwischen Mitarbeiter und Benutzer wird wieder richtig hergestellt.
- Mitarbeiter ließ sich nicht mit einem Benutzer erstellen.

#### 23.06.2015
##### Erweiterung, 1.0.40
- Papierformate werden bei Neuinstallation und update angelegt und Reports werden automatisch zugeteilt.


##### FIX, 1.0.39
- Überlieferung war nicht möglich.


##### FIX, 1.0.38
- Vereinzelte Lieferscheine ließen sich nicht abschließen.


#### 23.06.2015, 1.0.37
##### Erweiterung
- Die Reports werden bei der Installation den Papierformaten zugeordnet.


#### 22.06.2015, 1.0.36
##### Änderung
- Papierformate für die neuen Reports angepasst. Werden bei einer Neuinstallation neu gesetzt.


##### FIX
- Bei einer Unterlieferung wird die Verkaufsmenge richtig gesetzt, wodurch dir Rechnung mit der korrekten Menge erstellt wird.
- Bei erzwungenen Teillieferungen (nicht auf Lager) wird die Lieferung von davor nicht addiert.


#### 19.06.2015, 1.0.35
##### Änderung
- Rechnung- und Lieferadresse bekommen auch den Zusatz Straße und Stadt, wenn die Option in den Verkaufseinstellungen aktiviert ist.


#### 18.06.2015, 1.0.34
##### Änderung
- Die Änderungen am partner_id Feld zusammengefasst. Nur die nötigen Attribute werden geändert.
- Die Optionen für die Adresserweiterungen werden nun immer angezeigt.
- Beim "Verkäufe" Button im Produkt wird die Menge aus Angeboten nicht mehr berücksichtigt.


##### Erweiterung
- Hausnummer in die Unternehmensdaten eingefügt.

#### 12.06.2015, 1.0.33
##### Änderung
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


#### 9.06.2015, 1.0.32
##### Bugfix
- Zeilenumbrüche werden auf den Reports wieder richtig angezeigt.


#### 9.06.2015, 1.0.31
##### Bugfix
- Fehlenden Context eingefügt.


#### 29.05.2015, 1.0.30
##### Verbesserung
- Auswahl bei Standardliefer- und Rechnungsadresse auf die eigenen Partner-Kontakte beschränkt
- Kundenreferenznr. wird beim Duplizieren übertragen


#### 28.05.2015, 1.0.28
##### Bugfix
- Benutzer mit eingetragenem Mitarbeiter lässt sich wieder erstellen.
- Logik für die 1zu1 Verbindung zwischen Mitarbeiter und Benutzer funktioniert wieder.


#### 28.05.2015, 1.0.27
##### Verbesserung
- Deutsche Übersetzung für Ein-/Ausgangsrechnung angepasst.


#### 27.05.2015, 1.0.26
##### Bugfix
- In der Lieferansicht, welche man über den Button "Lieferungen" im Produkt öffnet, wird nach dem richtigen Produkt gefiltert.


#### 27.05.2015, 1.0.25
##### Bugfix
- Button in der Produktübersicht für die Ein-/Ausgangsrechnungen zeigt nun alle Rechnungen an.


#### 27.05.2015, 1.0.25
##### Verbesserung
- Button, welcher die Verkäufe im Produkt anzeigt, zeigt nun die offene Menge und die Gesamtmenge an.


#### 27.05.2015, 1.0.24
##### Erweiterung
- Anzeigeart (Kalenderwoche/Datum) des Lieferdatums auf Kundenebene einstellbar.


#### 27.05.2015, 1.0.23
##### Erweiterung
- Filter "Ein- und Ausgang" für die Lagerbuchungen eingefügt. Lieferungen von und zu Kunden und Lieferanten.
- Der Button "Lieferungen" in den Produkten und Produktvarianten benutzt den Filter Ein- und "Ausgang"


#### 19.05.2015, 1.0.22
##### Erweiterung
- Boolean Feld in die Lieferdetails eingefügt, wodurch die zu Liefernde Position abgeschlossen wird und im neuen Lieferschein nicht mehr aufgeführt ist.


#### 19.05.2015, 1.0.21
##### Erweiterung
- Button zum Öffnen der Ein-/Ausgangsrechnung in die Form Ansicht der Produkte und Produktvarianten eingefügt.
- Anzeige der Rechnung


#### 12.05.2015, 1.0.20
##### Bugfix
- Fehlendes Hochkomma im Report "Angebotsanfrage" hinzugefügt.


#### 05.05.2015, 1.0.19
##### Erweiterung
- Beim Ein- und Verkaufsaufträgen wird als Beschreibung der Position ein Leerzeichen eingefügt, wenn für das Produkt keine Beschreibung hinterlegt ist. Dieses Leerzeichen wird auf den Reports nicht angezeigt.


#### 05.05.2015, 1.0.18
##### Bugfix
- Fehler behoben, bei dem man den Verkaufsauftrag aus dem Webshop nicht erstellen konnte.


#### 05.05.2015, 1.0.17
##### Erweiterung
- Einstellung in den Verkauf hinzugefügt, wodurch der Verkaufstext einer Position aus der internen Beschreibung des Produktes genommen wird.


#### 05.05.2015, 1.0.16
##### Bugfix
- Fehlerhafte Anzeige des Produktnummern Generators in den Einstellungen behoben.


#### 04.05.2015, 1.0.15
##### Bugfix
- Rechnungs- und Lieferadresse im Angebot/Auftrag werden nicht mehr überschrieben, sondern abgeändert.


#### 30.04.2015, 1.0.14
##### Bugfix
- Fehler behoben, bei dem die neu eingefügten Felder auf den Report nicht angezeigt wurde.


#### 30.04.2015, 1.0.13
##### Änderung
- Icon für den Button "Preislistenpos." in der Form View des Produktes abgeändert.


##### Verbesserung
- Reports: Adressfelder für den Stadtteil und die Hausnummer eingefügt.
- Reports: Zweites Namensfeld eingefügt.
- Reports: Telefax(geschäftlich) in das Mitarbeiterobjekt eingefügt.


#### 29.04.2015, 1.0.12
##### Verbesserung
- Adressfelder für den Stadtteil und die Hausnummer zum Partnerobjekt hinzugefügt und die Formanischt überarbeitet. Zweites Namensfeld hinzugefügt.
- Feld Telefax(geschäftlich) in das Mitarbeiterobjekt eingefügt.


#### 24.04.2015, 1.0.11
##### Verbesserung
- Produktnummern können in der Listenansicht der Produkt über den Button "Mehr/Produktnummer generieren" für die ausgewählten Produkte generiert werden.


#### 24.04.2015, 1.0.10
##### Verbesserung
- Produktnummergenerierung kann in der Lagereinstellungen eingestellt werden.
- Wenn bei der Produktnummergenerierung nur eindeutige Produktnummern erstellt werden können (min/max Prefixlänge = 0), dann wird die EAN13 des Produktes automatisch generiert.


#### 20.04.2015, 1.0.9
##### Bugfix
- Für zusätzliche Produkte, die nur im Lieferschein erfasst werden, wird nun die richtige Beschreibung benutzt.


##### Erweiterung
- Produkte werden standardmäßig nach der Produktnummer sortiert.


#### 07.04.2015, 1.0.8
##### Verbesserung
- In allen Reports haben nun die Spalten für Artikelnummer, Preis pro Einheit und Netto-Preis eine Mindestbreite.

#### 01.04.2015, 1.0.7
##### Bugfix
- Seriennummermodul funktionsfähig gemacht.


#### 01.04.2015, 1.0.6
##### Bugfix
- Neu erstellte Lieferscheine, die über den Button "Lieferschein abbrechen" erstellt wurden, werden mit dem Rechnungsstatus abzurechnen erstellt.


#### 26.03.2015, 1.0.5
##### Bugfix
- Fehlerhafte id abgeändert.


#### 26.03.2015, 1.0.4
##### Verbesserung
- Erweiterung der Tabelle res.partner um neues Feld eq_foreign_ref
- Erweiterung der Maske, damit man das Feld in der Detailansicht der Adresse pflegen kann
- Wenn ein Kundenauftrag oder eine Bestellung angelegt wird, ist der Inhalt des Feldes res.partner.eq_foreign_ref automatisch aus der Adresse übernommen und im Feld purchase.order."partner_ref" / sale.order."client_order_ref" gespeichert


#### 25.03.2015, 1.0.3
##### Änderung
- Die Zeichnungsnnummer aus den Reports Angebot/Auftrag, Lieferschein, Rücklieferschein und Rechnung entfernt und durch Platzhalter mit der id "eq_drawing_number" ersetzt.


#### 24.03.2015, 1.0.2
##### Verbesserung
- Ids an die Elemente der Lieferanschrift in der Rechnung vergeben.


#### 23.03.2015, 1.0.1
##### Änderung
- Das Feld eq_supplier_order_ref entfernt
- Vor dem Update muss das dazugehöre View gelöscht werden. Hierzu folgenden SQL Query benutzen:
- delete from ir_ui_view where arch like '%eq_supplier_order_ref%'


##### Bugfix
- Die Übersetzung des Textes "Leave Requests to Approve" im HR Modul wurde in unserer de.po Datei gespeichert, damit unsere Lokalisierung den Text selber setzen kann -> "Urlaubsanträge"


#### 20.03.2015
##### Verbesserung
- Unnötige Zugriffsrechte entfernt
- Finale Version unserer Lokalisierung hinzugefügt


##### Bugfix
- Steuer wird bei den Rechnungspositionen automatisch gesetzt, wenn eine Rechnung von einem Lieferauftrag erstellt wird, welcher keinen Bezug zu einem Verkaufs-/Einkaufsauftrag hat.
- Testeinträge in der de.po Datei gelöscht


#### 19.03.2015
##### Erweiterung
- Erweiterung der Lokalisierung für Texte, die in der DB bereits vorhanden sind. Man kann also ab jetzt immer ein UPDATE der Übersetzungen durchführen


#### 17.03.2015
##### Bugfix
- Fehler bei den Unterlieferungen (Eingang) behoben. (Mengeneinheit * stimmt mit Mengeneinheit * nicht überein)
- Feld für den Rahmenauftrag einer Auftragsposition entfernt.


#### 13.03.2015
##### Erweiterung
- Open purchase order lines um neue Gruppierung nach Rahmenauftrag erweitert
- Feld für die Preislistenversion in die Preislistenposition eingefügt.

##### Bugfix
- Fehler bei den Unterlieferungen behoben. (Mengeneinheit Stück stimmt mit Mengeneinheit Stück nicht überein)


##### Änderung
- Änderung in der Lokalisierung für open purchase order lines -> der text "von Bestellpositionen" wird nicht mehr angezeigt


##### Bugfix
- Bugfix im Aufruf der Gruppierung nach Rahmenauftragsnummer für open sale order lines


#### 12.03.2015
##### Erweiterung
- Erweiterung der Lokalisierung für open purchase order lines


#### Bei Update-Fehler
..
*AttributeError: Das Feld `eq_quantity_left` existiert nicht*

*Fehler Kontext:*
*Ansicht `eq.purchase.order.line.tree`*
*[view_id: 1661, xml_id: equitania.eq_purchase_order_line_tree_inherit, model: purchase.order.line, parent_id: 867]*

**Folgenden Datensatz löschen:**
*DELETE FROM ir_ui_view WHERE name='purchase.order.line.tree' AND mode='extension';*


#### 06.03.2015
##### Erweiterung
- Button/Widget in die Produkte eingefügt, die die Preislistenpositionen anzeigen.


#### 04.03.2015
##### Erweiterung
- Wizard für das Ändern des Lieferdatums im Lieferschein eingefügt. Änderungsgrund muss angegeben werden und Änderung wird als Nachricht dokumentiert.
- Suche nur nach der Bezeichnung eingefügt.
- Sortierung nach dem Feld "Produktnr." ist ab jetzt auch möglich.
- Die Kundenmaske um die Standardliefer- und Rechnungsadresse erweitert. Wird im Verkauf genutzt.


##### Verbesserung
- Performance-Verbesserung des SQL Statements von Omprakash


#### Modul Equitania

- Optimierung der Masken für Adressen, Produkte, Verkauf, Einkauf, Fertigung uvm.
- Die Anzeige in der Partnersuche des Verkaufsauftrag um den Adresstypen erweitert. Straße, Ort einstellbar
- In den Einstellungen wird der Reiter "Installierte Module" als erster Eintrag angezeigt und beim Öffnen aufgerufen
- Die Unternehmensmaske um 4 Felder, die in der Fußzeile der Reports angezeigt werden, und das Firmenlogo, welches auf dem Report aufgedruckt wird
- Die Debitoren- und Kreditorennummer mit Sequenzgenerator im Kunden/Lieferanten hinzugefügt
- Eigene Übersetzungslogik der Reports und Masken
- Internes und externes Papierformat wird gesetzt
- Das Feld "Vermittelt durch" in die Leads eingefügt. Enthält eine Beschreibung.
- Alle Auftragspositionen für Einkauf und Verkauf werden noch einmal in einer separaten Maske(Liste, Form) angezeigt
- Lieferbedingungen in den Verkaufsauftrag eingefügt
- Die Suche nach einzelnen Positionen in Preisliste - Löschen über die Detailansicht - Widget in der Produktmaske
- Sachbearbeiter in den Verkaufsauftrag eingefügt, Verkäufer wird automatisch eingetragen (einstellbar)
- Eigene Logik für Tausender Separatoren und Nachkommastellen für die Reports eingefügt (einstellbar)
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

##### Kontakt überarbeitet:

- Feld Vorname eingefügt
- Feld Geburtsdatum eingefügt
- Addresstyp um die Postfachaddresse erweitert
- Standard Liefer- und Rechnungsadresse kann festgelegt werden
- Ersteller des Datensatzes wird als Verkäufer eingetragen (einstellbar)


##### Reports überarbeitet:

- Angebot
- Verkaufsauftrag
- Anfrage
- Bestellung
- Lieferschein
- Rechnung
- Neu:  Auftragspositionen
- Neu: Rücklieferschein
- Das "sale_layout" Modul integriert, wodurch sich Positionen gruppieren lassen
