/*
  A simple code to read the analog signals from a series of 
  potentiometers connected to the Analogue pins. The values will
  be sent over serial port in JSON format, i.e.:
    {"knob_00":300,
     "knob_01":737,
     "knob_02":732,
     "knob_03":723,
     "knob_04":721,
     "knob_05":705}

  The circuit:
    Each 3-legged potentiometer should be connected to 5v, ground,
    and the middle leg should go to Analogue pin.
    Values will be between 0 and 1023, if you have less than 6 potentiometers, 
    connect them to A0, A1, .... The value of last potentiometer will
    be automatically copied to the rest of the dictionary (idk why!)

  Author: Ardavan Bidgoli
  https://github.com/Ardibid/DashDuino

  Date created: 06/13/2021
  Date last modified: 06/13/2021
  License: MIT
*/

#include <ArduinoJson.h>
DynamicJsonDocument doc(128);
int knob_values[6] = {0,0,0,0,0,0};
byte knob_pins[6] = {A0, A1, A2, A3, A4, A5}; 
String knob_names[sizeof(knob_pins)];

void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);

  // initialize the dictionary 
  for (int i = 0; i < sizeof(knob_pins); i++) {
    knob_names[i] = "knob_0"+String(i);
  }
}


void loop() {
  // reading/sending to serial port in each loop
  read_knob_values();
  write_knob_values_to_serial();
}

void read_knob_values(){
  for (int i = 0; i < sizeof(knob_pins); i++) {
    knob_values[i] = analogRead(knob_pins[i]);
    doc[knob_names[i]] = knob_values[i];
  }
 
}

void write_knob_values_to_serial(){
  serializeJson(doc, Serial);
  // this line helps to read the data in Python
  Serial.println("");
}
