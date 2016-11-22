# NeoPixel Script Benutzerhandbuch

Dieses Dokument beschreibt NPS (NeoPixel Script), eine einfache Sprache zum steuern
einer 8x8 NeoPixel LED Matrix.

## NPS Befehle

### Kommentare

Zeilen welche mit "//" beginnen sind Kommentarzeilen die nicht vom Kompiler ausgewertet
werden:

    // das ist ein Kommentar

### pixel

Der Befehl "pixel" ermöglicht das setzen ein oder mehrerer LEDs in einer angegebenen Farbe
(siehe auch Abschnitt "Farben"). Eine LED innerhalb der Matrix kann dabei auf zwei Arten
angesrochen (adressiert) werden (siehe auch Abschnitt "Adressierung"):

  * Absolut: dabei wird die eindeutige Nummer der LED angegeben (z. B. 42)
  * Relativ: hier wird die Spalte und die Reihe der LED agegeben, getrennt mit ":" (z. B. 3:4)

Für beide Arten der Adressierung gilt, es wird mit 0 begonnen.

Um beispielsweise die LED in der linke oberen Ecke der Matrix rot zu beleuchten kann man dies
mit absoluter adressierung und folgendem Befehl tun:

    pixel 0 in rot

Das Gleiche mit ralativer adressierung:

    pixel 0:0 in rot

Und für die rechte untere Ecke:

    // absolut
    pixel 56 in rot
    // relativ
    pixel 7:7 in rot

Möchte man mehrere LEDs hintereinander in der gleichen Farbe beleuchten, so ist es möglich,
mehrere Adressen mit Komma getrennt an zu geben:

    pxiel 0, 0:1, 3:3, 3:4 in blau

Bei Verwendung von absoluten Adressen kann auch ein Bereich (von/bis) angegeben werden.
Der folgende Befehl beleuchtet die LEDs 0, 1, 2, 3, 4, 5, 6, 7 in grün:

    pixel 0..7 in gruen

Weiterhin gibt es die spezial Adresse "alle" die es ermöglicht, die komplette Matrix in
einer gegeben Farbe leuchten zu lassen:

    pixel all in lila

### schreibe

TODO

### symbol

TODO

### animiere

TODO

### feld

TODO

### helligkeit

TODO

### blenden

TODO

### warte

TODO

### szene

TODO

### wiederhole

TODO


## Farben

Liste aller bekannten Farben in NPS:

    schwarz
    blau
    braun
    zyan
    dunkelblau
    dunkelzyan
    dunkelgrau
    dunkelgruen
    dunkelmagenta
    dunkelorange
    dunkelrot
    dunkeltuerkis
    dunkelviolet
    dunkelpink
    gold
    grau
    gruen
    hellblau
    hellzyan
    hellgruen
    hellgrau
    hellpink
    hellgelb
    magenta
    orange
    pink
    lila
    rot
    silber
    tuerkis
    violet
    weiss
    gelb

## Adressierung der Matrix

Die folgenden Abschnitte zeigen die Adressen der einzelnen LEDs in absoluter und
relativer Adressierung.

### Absolut

| ID |    |    |    |    |    |    |    |
|----|----|----|----|----|----|----|----|
|  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |
| 15 | 14 | 13 | 12 | 11 | 10 |  9 |  8 |
| 23 | 22 | 21 | 20 | 19 | 18 | 17 | 16 |
| 31 | 30 | 29 | 28 | 27 | 26 | 25 | 24 |
| 39 | 38 | 37 | 36 | 35 | 34 | 33 | 32 |
| 47 | 46 | 45 | 44 | 43 | 42 | 41 | 40 |
| 55 | 54 | 53 | 52 | 51 | 50 | 49 | 48 |
| 65 | 62 | 61 | 60 | 59 | 58 | 57 | 56 |

### Relativ

|  y:x  |       |       |       |       |       |       |       |
|-------|-------|-------|-------|-------|-------|-------|-------|
|  0:0  |  0:1  |  0:2  |  0:3  |  0:4  |  0:5  |  0:6  |  0:7  |
|  1:0  |  1:1  |  1:2  |  1:3  |  1:4  |  1:5  |  1:6  |  1:7  |
|  2:0  |  2:1  |  2:2  |  2:3  |  2:4  |  2:5  |  2:6  |  2:7  |
|  3:0  |  3:1  |  3:2  |  3:3  |  3:4  |  3:5  |  3:6  |  3:7  |
|  4:0  |  4:1  |  4:2  |  4:3  |  4:4  |  4:5  |  4:6  |  4:7  |
|  5:0  |  5:1  |  5:2  |  5:3  |  5:4  |  5:5  |  5:6  |  5:7  |
|  6:0  |  6:1  |  6:2  |  6:3  |  6:4  |  6:5  |  6:6  |  6:7  |
|  7:0  |  7:1  |  7:2  |  7:3  |  7:4  |  7:5  |  7:6  |  7:7  |
