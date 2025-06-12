#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN);

// CHANGE THESE KEYS BEFORE DEPLOYMENT!
byte voterKey[6] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF};
byte govKey[6] = {0x11, 0x22, 0x33, 0x44, 0x55, 0x66};

void setup() {
    Serial.begin(115200);
    SPI.begin();
    mfrc522.PCD_Init();
    Serial.println("READY");
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command == "PING") {
            Serial.println("ALIVE");
        } else if (command == "RESET") {
            setup();
            Serial.println("RESET_OK");
        } else if (command == "WRITE") {
            Serial.println("GOT_WRITE"); // Acknowledge to start data transfer
            
            if (Serial.available() > 0) {
                String cardData = Serial.readStringUntil('\n');
                cardData.trim();
                
                if (processCardData(cardData)) {
                    Serial.println("SUCCESS"); // Signal success
                } else {
                    Serial.println("ERROR:CARD_WRITE_FAILED");
                }
            } else {
                Serial.println("ERROR:NO_CARD_DATA");
            }
        }
    }
}


bool processCardData(String cardData) {
    String parts[5];
    int startIndex = 0;
    int partIndex = 0;
    int commaIndex;

    while (partIndex < 4 && startIndex < cardData.length()) {
        commaIndex = cardData.indexOf('|', startIndex);
        if (commaIndex == -1) {
            return false; 
        }
        parts[partIndex] = cardData.substring(startIndex, commaIndex);
        startIndex = commaIndex + 1;
        partIndex++;
    }
    parts[4] = cardData.substring(startIndex);

    // Check for a valid card
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        Serial.println("ERROR:NO_CARD");
        return false;
    }

    // Now, write the separate parts onto the RFID card
    if (!writeSector(0, voterKey, parts[0], parts[1], parts[2], parts[3], parts[4])) {
        return false;
    }
    
    return true;
}


bool writeSector(byte sector, byte* key, String name, String voterID, String age, String constituency, String fingerprintHash) {
    byte blockAddr = sector * 4;

    //Authenticate Sector
    MFRC522::StatusCode status = mfrc522.PCD_Authenticate(
        MFRC522::PICC_CMD_MF_AUTH_KEY_A, 
        blockAddr + 3,  // Sector Trailer is always in Block 3
        key, 
        &(mfrc522.uid)
    );
    if (status != MFRC522::STATUS_OK) {
        Serial.print("Authentication error: ");
        Serial.println(mfrc522.GetStatusCodeName(status));
        return false;
    }
     
   
    byte buffer[16];

    //Write the data to the blocks
    if (!writeBlock(blockAddr, name)) return false;  
    if (!writeBlock(blockAddr+1, voterID )) return false;   
    if (!writeBlock(blockAddr+2, age + "|" + constituency )) return false;   //  combining age and constituency
    if (!writeBlock(blockAddr+3, fingerprintHash)) return false;  // writing  hash to  block3
    
    Serial.println("Successfully wrote to sector. ");   // to  know if write happened
    return true;
}

bool writeBlock(byte blockAddr, String data) {
   byte buffer[16] = {0};
   byte length = min(data.length(), 16);
   data.getBytes(buffer, length);
   MFRC522::StatusCode status = mfrc522.MIFARE_Write(blockAddr, buffer, 16);
   return (status == MFRC522::STATUS_OK);
}
