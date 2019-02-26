/*
    NRF24L01 FIRMWARE RECEIVER- IC 11/08/2018
    NICHOLAS SCHARAN CYSNE - ITA
*/

#include <SPI.h>
#include <RF24.h>
#include <nRF24L01.h>
#include <RF24_config.h>

RF24 radio(7, 8); // CE, CSN

const byte address[6] = "00001";        // Address of communication, each one has one

void setup() {

  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);    // Open communication with address "address"
  radio.setPALevel(RF24_PA_MIN);        // Set Power Amplifier to Minimum
  radio.startListening();               // Set module to Receiver

}

void loop() {

  if (radio.available()) {              // Check if there's data incoming
    char text[32] = "";
    radio.read(&text, sizeof(text));    // Stores readed data into "text" string
    Serial.println(text);               // Print in Serial Monitor the message received
  }
}
