#include <ArduinoJson.h>
DynamicJsonDocument doc(128);
int knob_values[6] = {0,0,0,0,0,0};
byte knob_pins[6] = {A0, A1, A2, A3, A4, A5}; 
String knob_names[sizeof(knob_pins)];

void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);
  for (int i = 0; i < sizeof(knob_pins); i++) {
    knob_names[i] = "knob_0"+String(i);
  }
}


void loop() {
  read_knob_values();
  write_knob_values_to_serial();
}

void read_knob_values(){
  for (int i = 0; i < sizeof(knob_pins); i++) {
    knob_values[i] = analogRead(knob_pins[i]);
    doc[knob_names[i]] = knob_values[i];
    // Serial.println(String(i)+ ":" + String(knob_values[i]));
  }
 
}

void write_knob_values_to_serial(){
  serializeJson(doc, Serial);
  Serial.println("");
}

//
//void write2Serial(float val00, float val01){
//  String msg = "";
//  msg.concat(String(val00, 2));
//  msg.concat(" | ");
//  msg.concat(String(val01, 2));
//  Serial.println(msg);
//}
