'''
    File name: DashDuino_dbc_app.py
    Author: Ardavan Bidgoli
    Date created: 06/13/2021
    Date last modified: 06/13/2021
    Python Version: 3.7.7

    License: MIT
'''

import dash
from dash_html_components.Hr import Hr
import dash_daq as daq
import dash_bootstrap_components as dbc

import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc


import serial
import json

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

serial_port = None
knob_values = {}
counter = 0


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
                                        html.H6("Control the communicatino with Arduino", className="card-subtitle"),
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

app.layout = dbc.Container([setup_row,
                            html.Hr(),
                            gauges,
                            html.Hr(),
                            controls
                            ])


@app.callback(
    Output(component_id='port_stat', component_property='children'),
    Output(component_id='port_controller', component_property='children'),
    Input(component_id='port_controller', component_property='n_clicks')
    )
def port_manager(val):
    global serial_port
    print (val)
    if val:
        if val % 2 == 1 :
            serial_port.close()
            return (["Port is closed","Open Port"])
        else:
            serial_port = serial.Serial('COM4',baudrate=115200, timeout=100)
            return (["Port is open","Close Port"])
    else:
        serial_port = serial.Serial('COM4',baudrate=115200, timeout=100)
        print (serial_port)
        return (["Port is open","Close Port"])
    # else:
    #     return [dash.no_update, dash.no_update]

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
    global serial_port
    global knob_values
    global counter
    if serial_port :
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


    return (["Still Nothing", 0, 0, 0, 0, 0,0])


if __name__ == '__main__':
    app.run_server(debug=True)