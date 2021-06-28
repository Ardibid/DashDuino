/*
  A simple code to read the analog signals from a series of
  potentiometers connected to the Analogue pins. The values will
  be sent over serial port in JSON format, i.e.:
    {"knob_00":542,
      "knob_01":0,
      "knob_02":336,
      "knob_03":0,
      "rotary_knob":0}

  The circuit:
    Each 3-legged potentiometer should be connected to 5v, ground,
    and the middle leg should go to Analogue pin.
    Values will be between 0 and 1023, if you have less than 6 potentiometers,
    connect them to A0, A1, .... The value of last potentiometer will
    be automatically copied to the rest of the dictionary (idk why!)
    For the display, i uses Adafruit_GFX.h & Adafruit_SSD1306.h,
    VCC -> 5V, GND -> GND, SCL -> A5, SDA -> A4

  Author: Ardavan Bidgoli
  https://github.com/Ardibid/DashDuino

  The rotary encoder code is based on code by jumejume1
  https://github.com/jumejume1/Arduino/blob/master/ROTARY_ENCODER/ROTARY_ENCODER.ino

  Date created: 06/13/2021
  Date last modified: 06/28/2021
  License: MIT
*/

#include <ArduinoJson.h>

// For screen
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);

DynamicJsonDocument doc(128);


int knob_values[4] = {0, 0, 0, 0};
byte knob_pins[4] = {A0, A1, A2, A3};
String knob_names[sizeof(knob_pins)];

int encoder_pin_a = 2;
int encoder_pin_b = 3;
volatile int temp = 0;
volatile int counter = 0 ;


void setup() {
  display_setup();

  // the knobs
  pinMode(encoder_pin_a, INPUT_PULLUP); // internal pullup input pin 2
  pinMode(encoder_pin_b, INPUT_PULLUP); // internal pullup input pin 3

  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);

  // initialize the dictionary
  for (int i = 0; i < sizeof(knob_pins); i++) {
    knob_names[i] = "knob_0" + String(i);
  }

  attachInterrupt(0, ai0, RISING);
  attachInterrupt(1, ai1, RISING);

}

void display_setup() {
  //display code
  // connect AREF to 3.3V and use that as VCC, less noisy!
  //analogReference(EXTERNAL);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.display();
  delay(250);

  // Clear the buffer.
  display.clearDisplay();
  display.setRotation(3);
}

void loop() {
  read_knob_values();
  write_knob_values_to_serial();
  show_values_on_display();
}

void show_values_on_display() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  
  String labels [4]= {"    L","    T","    B","    R"};
  byte knob_pins[4] = {A0, A1, A2, A3};

  for (int i = 0 ; i < 4 ; i++) {
    display.setTextSize(1);
    display.println("    ");
    display.println(labels[i]);
    display.setTextSize(2);
    display.println(knob_values[i]/10);
  }
  display.display();
}

void read_knob_values() {
  for (int i = 0; i < sizeof(knob_pins); i++) {
    knob_values[i] = analogRead(knob_pins[i]);
    doc[knob_names[i]] = knob_values[i];
  }
  doc["rotary_knob"] = counter;
}

void write_knob_values_to_serial() {
  serializeJson(doc, Serial);
  // this line helps to read the data in Python
  Serial.println("");
}


// These two are just the rotary knob,
// If not using it, just delete these!
void ai0() {
  // ai0 is activated if DigitalPin nr 2 is going from LOW to HIGH
  // Check pin 3 to determine the direction
  if (digitalRead(3) == LOW) {
    counter--;
  } else {
    counter++;
  }
}

void ai1() {
  // ai0 is activated if DigitalPin nr 3 is going from LOW to HIGH
  // Check with pin 2 to determine the direction
  if (digitalRead(2) == LOW) {
    counter++;
  } else {
    counter--;
  }
}
