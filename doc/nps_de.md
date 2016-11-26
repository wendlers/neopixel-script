# NeoPixel Script Benutzerhandbuch

Dieses Dokument beschreibt NPS (NeoPixel Script), eine einfache Sprache zum Steuern
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
  * Relativ: hier wird die Spalte und die Zeile der LED agegeben, getrennt durch ":" (z. B. 3:4)

Für beide Arten der Adressierung gilt, es wird immer bei 0 begonnen.

Um beispielsweise die LED in der rechten oberen Ecke der Matrix rot zu beleuchten kann man dies
mit absoluter Adressierung und folgendem Befehl tun:

    pixel 0 in rot

Das Gleiche mit ralativer Adressierung:

    pixel 0:7 in rot

Und für die rechte untere Ecke:

    // absolut
    pixel 63 in rot
    // relativ
    pixel 7:7 in rot

Möchte man mehrere LEDs hintereinander in der gleichen Farbe beleuchten, so ist es möglich,
Adressen durch Komma getrennt an zu geben:

    pxiel 0, 0:1, 3:3, 3:4 in blau

Bei Verwendung von absoluten Adressen kann auch ein Bereich (von/bis) angegeben werden.
Der folgende Befehl beleuchtet die LEDs 0, 1, 2, 3, 4, 5, 6, 7 in grün:

    pixel 0..7 in gruen

Weiterhin gibt es die spezial Adresse "alle" welche es ermöglicht, die komplette Matrix in
einer gegeben Farbe leuchten zu lassen:

    pixel alle in lila

### schreibe

Mit dem Befehl "schreibe" kann ein Text in einer angegebenen Farbe von rechts
nach links über die Matrix gerollt werden:

    schreibe "NeoPixel Script ist einfach!" in gelb

Wichtig dabei ist, dass der Text in Anführungszeichen ("") steht.    

### symbol

Der Befehl "symbol" stellt ein einzelnes Zeichen in einer angegebenen Farbe auf
der Matrix dar:

    symbol "X" in blau

Für den Befehl "symbol" gilt, dass innerhalbt der Anführungszeichen genau ein
Zeichen stehen darf.

### animiere

Mit "animiere" werden die agegebenen Zeichen nacheinander in der definierten Farbe
dargestellt:

    animiere "Hallo!" in magenta

### feld

Ein "feld" enhält für jede LED genau einen Wert - 0 oder 1. 0 bedeutet LED schwarz/aus,
1 bedeutet, dass die LED in der gegebene Farbe beleuchtet wird:

    // ein X über die komplette Matrix
    feld
      1 0 0 0 0 0 0 1
      0 1 0 0 0 0 1 0
      0 0 1 0 0 1 0 0
      0 0 0 1 1 0 0 0
      0 0 0 1 1 0 0 0
      0 0 1 0 0 1 0 0
      0 1 0 0 0 0 1 0
      1 0 0 0 0 0 0 1
    in tuerkis

### helligkeit

Der Befehl "helligkeit" gibt an wie stark die LEDs beleuchtet werden sollen.
Die Helligkeit kann nur für alle LEDs gesetzt werden (und nicht pro LED).
Der Wert für die Helligkeit muss zwischen 0 und 255 liegen:

    // nicht besonders hell
    helligkeit 10

    // sehr hell
    helligkeit 200

### blenden

Mit dem Befehl "blenden" wird die Helligkeit innerhalb des gegebenen Wertebereiches
schrittweise erhöht (Einblenden) bzw. erniedrigt (Ausblenden).

Zum Einblenden wählt man den Wertebereich so, dass der Startwert kleiner als der
Endwert ist:

    blenden 0..50

Und zum Ausblenden wird der Endwert kleiner als der Startwert gewählt:

    blenden 50..0

### warte

Wertet die angegebene Zeit in Sekunden (sek) oder Millisekunden (msek):

    warte 1 sek
    warte 500 msek

### szene / spiele

Eine "szene" erlaubt die Gruppierung beliebiger anderer Anweisungen (außer "szene").
Über den vergebenen Namen und den Befehle "spiele" kann eine Szene später an beliebiger
Stelle aufgerufen werden:

    szene hallo
      schreibe "Hallo " in gruen
    ende

    szene welt
      schreibe "Welt!" in blau
    ende

    szene hallo_welt
      spiele hallo
      spiele welt
    ende

    helligkeit 10
    spiele hallo_welt
    helligkeit 50
    spiele hallo_welt

### schiebe

Mit dem Befehl "schiebe" können "neue" Pixel in einer gegebenen Farbe vom linken
oder rechten Ende der Matrix eingeschoben werden. Bestehende Pixel werden dabei
weiter geschoben:

    wiederhole 64 mal
      schiebe 1 rechts in blau
      warte 100 msek
    ende

    wiederhole 64 mal
      schiebe 1 links in gruen
      warte 100 msek
    ende

### wiederhole

Mit "wiederhole" können einfache Schleifen mit und ohne Zählervariable erstellt werden.
Eine Schleife dient dabei der N-fachen Wiederholung beliebig Anweisungen (außer "szene").

Um beispielsweise eine Pixel-Schlange durch die gesamte Matrix zu schieben kann folgende
Schleife verwendet werden:

    pixel alle schwarz
    wiederhole 64 mal
      schiebe 1 rechts in rot
      warte 100 msek
    ende

Zusätzlich kann eine Zählervariable angegeben werden. Diese kann dann zur Adressierung
von LEDs verwendet werden. Wichtig ist hierbei, dass Variablen immer ein "$" vorangestellt
bekommen:

    // lässt ein Pixel diagonal durch die Matrix wandern
    wiederhole 8 mal mit $i
      pixel $i:$i in rot
      warte 100 msek
      pixel $i:$i in schwarz
    ende

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
|  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 |
| 23 | 22 | 21 | 20 | 19 | 18 | 17 | 16 |
| 31 | 30 | 29 | 28 | 27 | 26 | 25 | 24 |
| 39 | 38 | 37 | 36 | 35 | 34 | 33 | 32 |
| 40 | 41 | 42 | 43 | 45 | 45 | 46 | 47 |
| 55 | 54 | 53 | 52 | 51 | 50 | 49 | 48 |
| 56 | 57 | 58 | 59 | 60 | 61 | 62 | 63 |

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
