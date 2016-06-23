## Modul eq_google_shopping

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