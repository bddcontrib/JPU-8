// Board: Arduino Uno

uint8_t dataPins[] = {6, 7, 8, 9,  10, 11, 12, 13};
uint8_t serialClockPin = 2;
uint8_t addressSerialDataPin = 3;
uint8_t writeEnablePin = 4;
uint8_t readEnablePin = 5;

enum Mode {
  NONE,
  READ,
  WRITE,
} 
mode = NONE;

void pulsePinHigh(uint8_t pin) {
  digitalWrite(pin, HIGH);
  delayMicroseconds(50);
  digitalWrite(pin, LOW);
}

void pulsePinLow(uint8_t pin) {
  digitalWrite(pin, LOW);
  delayMicroseconds(50);
  digitalWrite(pin, HIGH);
}

void setAddress(uint16_t address) {
  for (uint8_t i = 0; i < 16; i++) {
    digitalWrite(addressSerialDataPin, (address >> i) & 1);
    pulsePinHigh(serialClockPin);
  }
}

void setData(uint8_t data) {
  for (uint8_t dI = 0; dI < 8; dI++) {
    digitalWrite(dataPins[dI], (data >> dI) & 1);
  }
}

uint8_t readData() {
  uint8_t acc = 0;

  for (uint8_t dI = 0; dI < 8; dI++) {
    acc = acc | (digitalRead(dataPins[dI]) << dI);
  }

  return acc;
}

void writeByte(uint16_t address, uint8_t data) {
  if (mode != WRITE) {
    Serial.println("May only write in write mode");
    exit(0);
  }

  setAddress(address);
  setData(data);
  delayMicroseconds(100);
  pulsePinLow(writeEnablePin);
  delayMicroseconds(10000);
}

uint8_t readByte(uint16_t address) {
  if (mode != READ) {
    Serial.println("May only read in read mode");
    exit(0);
  }

  setAddress(address);
  digitalWrite(readEnablePin, LOW);
  delayMicroseconds(500);
  uint8_t data = readData();
  digitalWrite(readEnablePin, HIGH);
  return data;
}

void readMode() {
  digitalWrite(writeEnablePin, HIGH);
  digitalWrite(readEnablePin, HIGH);

  for (uint8_t dataPin : dataPins) {
    pinMode(dataPin, INPUT);
  }

  mode = READ;
}

void writeMode() {
  digitalWrite(writeEnablePin, HIGH);
  digitalWrite(readEnablePin, HIGH);

  for (uint8_t dataPin : dataPins) {
    pinMode(dataPin, OUTPUT);
  }

  mode = WRITE;
}

void printByte(uint8_t b) {
  Serial.print(b >> 4,   HEX);
  Serial.print(b & 0xF,  HEX);
}

void setupPins() {
  pinMode(serialClockPin, OUTPUT);
  pinMode(addressSerialDataPin, OUTPUT);
  pinMode(writeEnablePin, OUTPUT);
  pinMode(readEnablePin, OUTPUT);

  digitalWrite(serialClockPin, LOW);
  digitalWrite(addressSerialDataPin, LOW);
  digitalWrite(writeEnablePin, HIGH);
  digitalWrite(readEnablePin, HIGH);

  readMode();
}

void dumpRom() {
  readMode();

  Serial.println();
  Serial.println("Dumping EEPROM...");

  delayMicroseconds(1000);

  for (uint16_t addr = 0; addr < 256; addr++) {
    if ((addr % 4) == 0) {
      Serial.println();
      Serial.print(addr);
      Serial.print(": 0x");
    }

    uint8_t data = readByte(addr);
    printByte(data);
  }

  Serial.println();
  Serial.println("done!");
}

void differentialBlobWrite(uint8_t blob[], uint16_t startingAddress) {
  int MAX_RETRIES = 10;
  Serial.println("Peforming differential write...");
  
  for (int retries = 0; retries < MAX_RETRIES; retries++) {
    Serial.print("Attempt ");
    Serial.println(retries + 1);

    readMode();
    delayMicroseconds(1000);
    uint8_t readBuffer[256];
    for (uint16_t ofst = 0; ofst < 256; ofst++) {
      readBuffer[ofst] = readByte(startingAddress + ofst);
    }

    writeMode();
    int discrepencies = 0;
    delayMicroseconds(1000);
    for (uint16_t ofst = 0; ofst < 256; ofst++) {
      if (readBuffer[ofst] != blob[ofst]) {
        discrepencies++;
        writeByte(startingAddress + ofst, blob[ofst]);
      }
    }

    if (discrepencies == 0) {
      Serial.println("No discrepencies found! Done writing.");
      mode = NONE;
      return;
    }

    Serial.print("Found ");
    Serial.print(discrepencies);
    Serial.println(" discrepencies. Retrying...");
  }

  mode = NONE;
  Serial.println("Max retry limit exceded. Write failed.");
}

void writeDummyData() {
  Serial.println();
  Serial.println("Writing dummy data... ");

  uint8_t data[256];
  for (int ddi = 0; ddi < 256; ddi++) {
    //data[ddi] = 1 << (uint8_t)(ddi % 8);
    //data[ddi] = (uint8_t)ddi;
    data[ddi] = (uint8_t)(ddi * 11);
  }


  differentialBlobWrite(data, 0);
}

void setup() {
  Serial.begin(115200);
  setupPins();

  dumpRom();
}


void loop() {

}
