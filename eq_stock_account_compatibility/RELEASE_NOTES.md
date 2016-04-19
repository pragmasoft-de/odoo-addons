## Modul eq_stock_account_compatibility

#### 17.12.2015
#### Version 1.0.0
##### Veröffentlichung
- Kompatibilitätsmodul für das equitania und stock_account Modul, wodurch die Berechnung des Lagerwertes (Durchschnitt) funktioniert.
- Aktuelle Bestandsbewertung des Lagers überarbeitet, sodass nicht stock.moves für die id genutzt werden, sondern die stock.quants. Somit fehlen keine Einträge, wenn in einem stock.move unterscheidliche stock.quants hinterlegt sind.