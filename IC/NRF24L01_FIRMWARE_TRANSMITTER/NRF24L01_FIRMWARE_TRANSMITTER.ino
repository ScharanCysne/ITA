/*
    NRF24L01 FIRMWARE TRANSMITTER- IC 11/08/2018
    NICHOLAS SCHARAN CYSNE - ITA
*/

#include <SPI.h>
#include <RF24.h>
#include <nRF24L01.h>
#include <RF24_config.h>

RF24 radio(7, 8); // CE, CSN

const byte address[6] = "00001";        // Address of communication, each one has one

void setup() {
  
  radio.begin();
  radio.openWritingPipe(address);       // Open communication with address "address"
  radio.setPALevel(RF24_PA_MIN);        // Set Power Amplifier to Minimum
  radio.stopListening();                // Set module to Transmitter
  Serial.begin(9600);
  
}

void loop() {
  
  const char text[] = "Hello World";    // Message to be Sent 
  radio.write(&text, sizeof(text));     // Sends message from address &text with the size "text"
  Serial.println("Peekaboo!");
  delay(1000);
  
}
