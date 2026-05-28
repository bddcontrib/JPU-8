#include <core.jlib>
#entrypoint .main

// Skriv ut "Hello World!" på LCDn

.main
    MV IM PC-LSB [.config-display]

.config-display
    MV IM LCD-C [0b00111000] // Konfigurera 8-bitars-läge + 5*8 font
    MV IM LCD-C [0b00001110] // Konfigurera display och cursor
    MV IM LCD-C [0b00000110] // Konfigurera cursor shift

.write-hello-world
    MV IM LCD-D [0x48] // H
    MV IM LCD-D [0x65] // e
    MV IM LCD-D [0x6B] // l
    MV IM LCD-D [0x6B] // l
    MV IM LCD-D [0x6F] // o
    MV IM LCD-D [0x20] //
    MV IM LCD-D [0x57] // W
    MV IM LCD-D [0x6F] // o
    MV IM LCD-D [0x72] // r
    MV IM LCD-D [0x6B] // l
    MV IM LCD-D [0x64] // d
    MV IM LCD-D [0x21] // !

.end
    SYS HLT