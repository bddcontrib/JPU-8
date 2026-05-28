# Jscript 
### (.jscript)


## Datatyper

| Namn  | Användning        | Anteckningar                                     |
|-------|-------------------|--------------------------------------------------|
| int   | Heltal            | Skikas med värde                                 |
| int*  | Heltal (Pekare)   | Pekare                                           |
| long  | Heltal            | Pekare till LSB. MSB finns vid address + 1       |
| str   | Text (Pekare)     | Pekare till första elementet. Avslutas med 0x00. |
| any[] | Lista             | Pekare till första objekt                        |
| bool  | Booleanska värden | Lagras som en int, 0 = False, 1-255 = True       |
| byte  | Binär data        | Lagras som en int                                |

## Funktioner

``
func namn() {

}


``

## Komentarer
``
[kod] // kommentar
``