# DashDuino

![demo](/media/device.jpg)
![demo](/media/test_device.gif?raw=true)
![demo](/media/demo_v01.gif?raw=true)

A simple app to read knob values from an Arduino board to a Dash app.


### How to use

Load the DashDuino_Sketch on an Arduino Uno R3 board and wire up it based on the shcematic drawings. 
![demo](/media/board_small.png)

Once the board is up and running, make sure that Arduino serial montor is CLOSED, we want to have that port closed and ready for the dashboard to open it.
Check the port that your Arduino is connected to and update the **port** variable in DashDuino_dbc_app.py to match it. Then run the dash app:
`path\to\your\code\python  DashDuino_dbc_app.py`

![demo](/media/simulation.gif?raw=true)

## Dependencies

The code is tested to work with these versions:

* plotly: 4.14.3
* dash: 1.19.0
  * dash_core_components: 1.15.0
  * dash_html_components: 1.1.2
  * dash_bootstrap_components: 0.12.0250
  * dash_daq: 0.5.0
* numpy: 1.20.2
* re: 2.2.1
* serial: 3.5
* json: 2.0.9

---

## To do

* [x] Add port selection

* [x] Adding rotary encoder support

---

## Old Demo

![demo](/media/DashDuino_demo.gif?raw=true)

---
Code developed by [Ardavan Bidgoli](ardavan.io)