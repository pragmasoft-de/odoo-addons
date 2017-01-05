## Modul eq_project_extension

#### 05.01.2017
#### Version 1.0.13
##### CHG
- Erweiterungen für Zeitenerfassung: Start- und Endzeitpunkt


#### 03.11.2016
#### Version 1.0.12
##### FIX
- Schleife eingefügt, welche jeden Datensatz durchgeht, wenn mehrere ids zurückgegeben werden. Dadurch entsteht kein Singelton Error mehr.

#### 07.06.2016
#### Version 1.0.10
##### ADD
- Unter dem Menüpunkt: "Abzurechnende Arbeitszeiten und Materialien" werden nun noch zusätzlich zwei Spalten zu dem Kunden und der dazugehörigen Kundennummer angezeigt. 

#### 02.06.2016
#### Version 1.0.9
##### FIX
- Dependency zu Modul myodoo muss nun doch vorhanden sein.

#### 02.06.2016
#### Version 1.0.8
##### FIX
- Dependency zu Modul myodoo entfernt.

#### 23.05.2016
#### Version 1.0.7
##### ADD
- In einer Aufgabe können bei "Erledigt durch" nur noch Mitarbeiter ausgewählt werden.

#### 23.05.2016
#### Version 1.0.6
##### ADD
- Eine Aufgabe, welche "Erledigt" oder "Abgebrochen" ist kann nun zwischen den Phasen verschoben werden.
- Anpassung der Projektbeschreibung

#### 20.05.2016
#### Version 1.0.5
##### ADD
- Durch das OCA-Modul "project_gtd" wurde das Schließen der Projektstufen verursacht, wenn keine Aufgaben darin enthalten sind. Dies wurde nun behoben.
- Projekte können nicht mehr abgeschlossen werden, wenn nicht alle dazugehörigen Aufgaben entweder abgeschlossen oder abgebrochen sind.
- Es ist nun nicht mehr möglich neue Aufgaben zu einem Projekt hinzuzufügen, wenn der Status des Projektes "Abgebrochen" oder "Erledigt" ist.
- Ein Projekt, welches einen Status "Abgebrochen" oder "Erledigt" hat kann nicht mehr berarbeitet werden.
- Es sind nun keine Änderungen an einer Aufgabe mehr möglich, sofern sich diese in der Phase "Erledigt" oder "Abgebrochen" befindet.
- Eine Aufgabe kann nun nur noch mit dem Projektstatus "offen" innerhalb der Phasen verschoben werden.


#### 13.05.2016
#### Version 1.0.4
##### ADD
- Klassifizierung vom Projekt wird nun als Spalte unter "Abrechnen von Aufgaben" angezeigt.


#### 20.04.2016
#### Version 1.0.3
##### Erweiterung
- Projekte können nicht mehr abgeschlossen werden, wenn nicht alle dazugehörigen Aufgaben entweder abgeschlossen oder abgebrochen sind.

#### 15.04.2016
#### Version 1.0.2
##### Erweiterung
- Attribute eines Projekts können nicht mehr bearbeitet werden, wenn das Projekt nicht den Status "offen" hat.
- Aufgaben können nur für Projekte erstellt werden, die den Status "offen" haben.

#### 15.04.2016
#### Version 1.0.1
##### Erweiterung
- Eine vollständige Übersetzung wurde hinzugefügt.
- Aufgaben können nun nach Kalendertag sortiert werden.
- Das Feld "Abrechenbar" steht nun auf "100%", wenn der Benutzer keinen anderen Wert angibt.

#### 24.03.2016
#### Version 1.0.0
##### Erweiterung
- Initiale Modul-Erstellung.
- Schlagwörter (der Aufgaben) haben eine eigene Spalte in der Account.Analytic.Line-Ansicht bekommen.
