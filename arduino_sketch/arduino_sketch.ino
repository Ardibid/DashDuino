#include <ArduinoJson.h>
DynamicJsonDocument doc(64);


void setup() {
  // initialize serial communication at 57600 bits per second:
  Serial.begin(57600);
}

// the loop routine runs over and over again forever:
void loop() {
  int knob00 = analogRead(A0);
  int knob01 = analogRead(A1);
//  write2Serial(knob00, knob01);
  doc["knob_00"] = knob00;
  doc["knob_01"] = knob01;
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
