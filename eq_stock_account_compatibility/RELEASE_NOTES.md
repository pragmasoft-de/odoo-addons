## Modul eq_stock_account_compatibility

#### 15.12.2016
#### Version 1.0.3
##### CHG
- Sprachdatei ersetzt, Beschreibung ergänzt

#### 14.12.2016
#### Version 1.0.2
##### ADD
- Sprachdatei angelegt damit keine Warnings mehr in der Konsole angezeigt werden

#### 17.12.2015
#### Version 1.0.0
##### Veröffentlichung
- Kompatibilitätsmodul für das equitania und stock_account Modul, wodurch die Berechnung des Lagerwertes (Durchschnitt) funktioniert.
- Aktuelle Bestandsbewertung des Lagers überarbeitet, sodass nicht stock.moves für die id genutzt werden, sondern die stock.quants. Somit fehlen keine Einträge, wenn in einem stock.move unterscheidliche stock.quants hinterlegt sind.