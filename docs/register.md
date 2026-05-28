# Register

JPU-8 har 11 register:

| Namn   | Läs-address | Skriv-address | Anteckningar                                                              |
|--------|-------------|---------------|---------------------------------------------------------------------------|
| A      | 000         | 0000          | GP                                                                        |
| B      | 001         | 0001          | GP                                                                        |
| C      | 010         | 0010          | GP                                                                        |
| D      | 011         | 0011          | GP (Används ofta för temporära värden)                                    |
| XI     | X           | 0100          | ALU input 1                                                               |
| YI     | X           | 0101          | ALU input 2                                                               |
| ZO     | 100         | X             | ALU output                                                                |
| IM     | 111         | X             | Intermediate-värden                                                       |
| MEM    | 101         | 1000          | Minne (XI: address)                                                       |
| PC-LSB | X           | 0110          | Programräknare LSB                                                        |
| PC-MSB | X           | 0111          | Programräknare MSB (latchande, uppdaterar endast när PC-LSB skrivs till)  |
| PAUSE  | X           | 1110          | Stoppa klockan                                                            |
| EX-IN  | 110         | X             | Expansions-port för inputs                                                |
| LCD-D  | X           | 1100          | Skicka data till LCD-displayen                                            |
| LCD-C  | X           | 1101          | Skicka kommandon till LCD-displayen                                       |
