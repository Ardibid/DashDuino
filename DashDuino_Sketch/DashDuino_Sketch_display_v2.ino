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

const int button = 2;
int button_pressed_timer = 0;
bool button_down = false;

void setup() {
  display_setup();

  // the knobs
  pinMode(encoder_pin_a, INPUT_PULLUP); // internal pullup input pin 2
  pinMode(encoder_pin_b, INPUT_PULLUP); // internal pullup input pin 3

  // the push button
  pinMode(button, INPUT_PULLUP);

  // initialize serial communication at 115200 bits per second:
  Serial.begin(230400);

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
  display.setRotation(1);
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
  if (button_down) {
    display.println("S");
    display.println(" ");
    display.println("E");
    display.println(" ");
    display.println("N");
    display.println(" ");
    display.println("T");
  }
  else {

    String labels [3] = {"R", "T", "B"};
    byte knob_pins[3] = {A0, A1, A2};

    for (int i = 0 ; i < 3 ; i++) {
      int val_cut = knob_values[i];
      val_cut -= val_cut % 5;
      if (val_cut > 999) {
        val_cut = 999;
      }
      display.setTextSize(1);
      display.println(labels[i]);
      display.print("  ");
      display.println(val_cut);
    }
  }
  display.display();
}
void send_data_to_robot() {
  Serial.println("Sending something to robot");
}

void read_button_val() {
  
  int button_val = digitalRead(button);  
  
  if (button_val < 1) {
    button_pressed_timer ++;
    if (button_pressed_timer > 2) {
      button_down = true;
      button_pressed_timer = 0;
    }
  }
  else {
    button_pressed_timer = 0;
    button_down = false;
  }
}


void read_knob_values() {
  for (int i = 0; i < sizeof(knob_pins); i++) {
    knob_values[i] = analogRead(knob_pins[i]);
    doc[knob_names[i]] = knob_values[i];
  }
  read_button_val();
  
  doc["push_button"] = button_down;
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
