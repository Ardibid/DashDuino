'''
    File name: DashDuino_dbc_app.py
    Author: Ardavan Bidgoli
    Date created: 06/13/2021
    Date last modified: 06/13/2021
    Python Version: 3.7.7

    License: MIT
'''

######################################################################
### Imports
######################################################################
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from dash_html_components.Hr import Hr

import serial
import json

######################################################################
### Variables
######################################################################
serial_port = None
knob_values = {}
counter = 0
timeout_val = 100
baudrate_val=115200
port = 'COM4'


######################################################################
######################################################################
### Dash App Begins Here
######################################################################
######################################################################


######################################################################
### Dash App setup
######################################################################
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


######################################################################
### Dash App components
######################################################################
setup_row = dbc.Row([
                    dbc.Col(html.H1("Arduino Dashboard")),
                    ])
gauges = html.Div([
                    dbc.Row([
                            dbc.Col( 
                                    daq.Gauge(
                                            id='knob_00',
                                            label="Knob 00",
                                            min= 0, 
                                            max = 1023,
                                            showCurrentValue=True,
                                            ),
                                    ),
                            dbc.Col( 
                                    daq.Gauge(
                                            id='knob_01',
                                            label="Knob 01",
                                            min= 0, 
                                            max = 1023,
                                            showCurrentValue=True,
                                            ),
                                    ),
                            dbc.Col( 
                                    daq.Gauge(
                                            id='knob_02',
                                            label="Knob 02",
                                            min= 0, 
                                            max = 1023,
                                            showCurrentValue=True,
                                            ),
                                    ),
                            html.Hr(),
                            ]),

                    dbc.Row([
                            dbc.Col( 
                                    daq.Gauge(
                                            id='knob_03',
                                            label="Knob 03",
                                            min= 0, 
                                            max = 1023,
                                            showCurrentValue=True,
                                            ),
                                    ),
                            dbc.Col( 
                                    daq.Gauge(
                                            id='knob_04',
                                            label="Knob 04",
                                            min= 0, 
                                            max = 1023,
                                            showCurrentValue=True,
                                            ),
                                    ),
                            dbc.Col( 
                                    daq.Gauge(
                                            id='knob_05',
                                            label="Knob 05",
                                            min= 0, 
                                            max = 1023,
                                            showCurrentValue=True,
                                            ),
                                    ),
                            html.Hr(),
                            ])
])

controls = dbc.Row([
                    dbc.Card([
                         dbc.CardBody([
                                        html.H4("Setup", className="card-title"),
                                        html.H6("Control the communicatino with Arduino", 
                                                className="card-subtitle"),
                                        html.Hr(),
                                        dbc.Button("Open port", id="port_controller"),
                                        html.P("No port", id="port_stat"),
                                        html.Hr(),
                                        html.P("Nothing!", id="serial_val"),
                                        dcc.Interval(
                                                id='interval_component',
                                                interval= 50, # in milliseconds
                                                n_intervals=0
                                            )
                                    ])
                            ])
                    ],className="mb-3",)

######################################################################
### Dash App Layout
######################################################################
app.layout = dbc.Container([setup_row,
                            html.Hr(),
                            gauges,
                            html.Hr(),
                            controls
                            ])

######################################################################
### Dash App Callbacks
######################################################################
@app.callback(
    Output(component_id='port_stat', component_property='children'),
    Output(component_id='port_controller', component_property='children'),
    Input(component_id='port_controller', component_property='n_clicks')
    )
def port_manager(val):
    """
    Manages the serial port
    At the begining, opens the port automatically
    Upon further clicks, closes or opens the port and updates the notes
    """
    global serial_port
    global timeout_val  
    global baudrate_val 
    global port  

    # flip the port open and close on click
    if val:
        if val % 2 == 1 :
            serial_port.close()
            return (["Port is closed","Open Port"])
        else:
            serial_port = serial.Serial(port,baudrate=baudrate_val, timeout=timeout_val)
            return (["Port is open","Close Port"])
    # opening the port on page load
    else:
        serial_port = serial.Serial(port, baudrate=baudrate_val, timeout=timeout_val)
        return (["Port is open","Close Port"])


@app.callback(
    Output(component_id='serial_val', component_property='children'),
    Output(component_id='knob_00', component_property='value'),
    Output(component_id='knob_01', component_property='value'),
    Output(component_id='knob_02', component_property='value'),
    Output(component_id='knob_03', component_property='value'),
    Output(component_id='knob_04', component_property='value'),
    Output(component_id='knob_05', component_property='value'),
    Input(component_id="interval_component", component_property="n_intervals"),
    )
def update_serila(interavl):
    """
    Reads the serial port data in given time intervals
    The time interval is defined by the interval val in:
                                dcc.Interval(
                                            id='interval_component',
                                            interval= 50)
    Args:
        interval: number of interval passed since the load, coming from
                     dcc.Interval and its n_intervals value
    """
    global serial_port
    global knob_values
    global counter

    # checks if the serial port exists
    if serial_port:
        # checks if the serial port is open
        if serial_port.isOpen():
            try:
                data_to_read = serial_port.inWaiting()
                serial_msg = serial_port.read(data_to_read).decode('ascii')
                msg = serial_msg.split("\r\n")[-2]
                knob_values = json.loads(msg)

                msg = ""
                for key, value in knob_values.items():
                    msg = msg+ "{}: {}, ".format(key[-2:], value)

                return ([msg, 
                        knob_values["knob_00"],
                        knob_values["knob_01"],
                        knob_values["knob_02"],
                        knob_values["knob_03"],
                        knob_values["knob_04"],
                        knob_values["knob_05"],])
            except:
                counter += 1
                print ("had issues!",counter)
                return (7*[dash.no_update])
    # if port doesn't exist or is closed
    return (["Still Nothing", 0, 0, 0, 0, 0, 0])

######################################################################
### Dash App Running!
######################################################################
if __name__ == '__main__':
    app.run_server(debug=True)