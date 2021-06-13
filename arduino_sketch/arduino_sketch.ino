#include <ArduinoJson.h>
DynamicJsonDocument doc(128);
int knob_values[] = {0,0,0,0,0,0};
byte knob_pins[] = {A0, A1, A2, A3, A4, A5}; 

void setup() {
  // initialize serial communication at 57600 bits per second:
  Serial.begin(57600);
}

// the loop routine runs over and over again forever:
void loop() {
  read_knob_values();
  write_knob_values_to_serial();
}

void read_knob_values(){
  int knob00 = analogRead(A0);
  int knob01 = analogRead(A1);
  //  write2Serial(knob00, knob01);
  doc["knob_00"] = knob00;
  doc["knob_01"] = knob01;
}

void write_knob_values_to_serial(){
  serializeJson(doc, Serial);
  Serial.println("");
}

void write2Serial(float val00, float val01){
  String msg = "";
  msg.concat(String(val00, 2));
  msg.concat(" | ");
  msg.concat(String(val01, 2));
  Serial.println(msg);
}
