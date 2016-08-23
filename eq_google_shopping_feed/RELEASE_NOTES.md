## Modul eq_google_shopping


#### 23.08.2016
#### Version 1.0.19
##### FIX
- Attribut "google_identifier_exists" auf "identifier_exists" abgeändert

#### 23.08.2016
#### Version 1.0.18
##### ADD
- Attribut "google_identifier_exists" hinzugefügt

#### 09.08.2016
#### Version 1.0.17
##### ADD
- Leerzeichen jeweils zwischen Zahl und Einheit bei Unit Pricing Measure und Unit Pricing Base Measure entfernt.
- Produktbild wird nun korrekt angezeigt und der Image-Link wird korrekt gebildet, wenn keine Varianten gesetzt worden sind.
- MPN nun die Artikelnummer (default_code)

#### 09.08.2016
#### Version 1.0.16
##### ADD
- Nun werden nur Produkte im Google Shopping Feed angezeigt, wenn das Flag "Im Google Shopping Feed anzeigen" beim Artikel gesetzt und der Artikel im Shop veröffentlicht ist (vorher hat es ausgereicht wenn der Artikel nur veröffentlicht war).

#### 25.07.2016
#### Version 1.0.14
##### FIX
-Abfrage hinzugefuegt, welche verhindert, dass ein Image-Link gleich NoneType gesetzt werden kann. Dadurch trat ein Fehler auf, welcher es verhindert hat, dass der Shopping Feed ausgegeben werden konnte.

#### 13.07.2016
#### Version 1.0.13
##### FIX
-Modulbeschreibung Ü in Ö geändert

#### 13.07.2016
#### Version 1.0.12
##### CHG
-Modulbeschreibung Google Shopping Feed um den Kurzlink zum Wiki ergänzt

#### 27.06.2016
#### Version 1.0.11
##### FIX
- Zeichen "&,%,>,<" haben die sofortige Anzeige des entsprechenden XML-Feeds verhindert. Diese Zeichen werden nun durch den entsprechenden XML-fähigen Code ersetzt. Dadurch wird eine sofortige Ausgabe des Google-Shopping-Feeds gewährleistet.
- "Weitere suchen"-Funktion funktioniert nun bei der Eingabe eines Begriffs in das Feld von Google Produkt Category.

#### 24.06.2016
#### Version 1.0.10
##### CHG
- Modulbeschreibung und Icon angepasst

#### 23.06.2016
#### Version 1.0.9
##### FIX
- Fehler behoben, welcher durch das Speichern einer nicht gesetzten Google Produkt Kategorie verursacht wurde.

#### 23.06.2016
#### Version 1.0.8
##### CHG
- Aufruf der XML-Feeds nun unter Root-Url + /google_shopping_feed/data + _at.xml/_de.xml/_en.xml/_gb.xml/_ch.xml

#### 23.06.2016
#### Version 1.0.7
##### ADD
- Benötigte Felder im XML-FEED-Header (Titel, url und Erstellungsdatum) werden nun dynamisch gesetzt.

#### 23.06.2016
#### Version 1.0.6
##### ADD
- Produktattribute werden nun korrekt im XML-Feed eingetragen. Print-Statements entfernt. Ansicht zum Setzen der "Google-Attribute" erstellt.

#### 22.06.2016
#### Version 1.0.5
##### ADD
- Alle notwendigen Felder eines Produkt werden nun ausgelesen und anschließend wird der Google-Shopping-Feed erstellt.
(Diese Version enthält noch print-Statements zur Ausgabe der Produktattribute. Diese print-Statements werden für die noch zu erledigende Formatierung der Produktattribute im XML-Feed benötigt.)

#### 16.06.2016
#### Version 1.0.4
##### CHG
- Grundgerüst für XML-Feed erstellt (vorher .txt File)
- In der product_template Form-Ansicht neuen Reiter für "Google Shopping Feed" erstellt, welcher alle noch nicht vorhandenen aber notwendigen Felder für einen Feed enthält.
- Übersetzung angepasst

#### 19.02.2016
#### Version 1.0.3
##### Fix
- Indexfehler  products[0].ids korrigiert