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
from dash_html_components.Col import Col
from dash_html_components.H4 import H4
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
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
rotary_encoder_range = [-2000, 2000]


"""
Sample of data collected from the Arduino sketch
{"knob_00":283,"knob_01":258,"knob_02":264,"knob_03":310,"knob_04":355,"knob_05":315,"rotary_knob":2310}
"""
######################################################################
######################################################################
### Dash App Begins Here
######################################################################
######################################################################
show_values_on_knobs = False

######################################################################
### Dash App setup
######################################################################
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


######################################################################
### Dash App components
######################################################################
setup_row = dbc.Card([
                    dbc.CardBody([
                            dbc.Row([html.H1("DashDuino")]),
                    dbc.Row([
                            html.P("By Ardavan Bidgoli | 2021")])
                        ])
                    ], color="light", outline=True, className="mb-2")

gauges = dbc.Card([
                        dbc.CardBody([
                        html.H4("Knobs"),
                        html.P("Use the mixer knobs to set values"),
                        html.Hr(),
                        dbc.Row([
                                dbc.Col( 
                                        daq.Gauge(
                                                id='knob_00',
                                                label="Knob 00",
                                                min= 0, 
                                                max = 1023,
                                                showCurrentValue=show_values_on_knobs,
                                                ),
                                        ),
                                dbc.Col( 
                                        daq.Gauge(
                                                id='knob_01',
                                                label="Knob 01",
                                                min= 0, 
                                                max = 1023,
                                                showCurrentValue=show_values_on_knobs,
                                                ),
                                        ),
                                dbc.Col( 
                                        daq.Gauge(
                                                id='knob_02',
                                                label="Knob 02",
                                                min= 0, 
                                                max = 1023,
                                                showCurrentValue=show_values_on_knobs,
                                                ),
                                        ),
                                dbc.Col( 
                                        daq.Gauge(
                                                id='knob_03',
                                                label="Knob 03",
                                                min= 0, 
                                                max = 1023,
                                                showCurrentValue=show_values_on_knobs,
                                                ),
                                        ),
                                dbc.Col( 
                                        daq.Gauge(
                                                id='knob_04',
                                                label="Knob 04",
                                                min= 0, 
                                                max = 1023,
                                                showCurrentValue=show_values_on_knobs,
                                                ),
                                        ),
                                dbc.Col( 
                                        daq.Gauge(
                                                id='knob_05',
                                                label="Knob 05",
                                                min= 0, 
                                                max = 1023,
                                                showCurrentValue=show_values_on_knobs,
                                                ),
                                        ),
                                ]),
                        dbc.Row([
                                dbc.Col([
                                        html.H3("No read yet", 
                                                id="rotary_status",
                                                style={'textAlign': 'center'}
                                                ),
                                                
                                        ], width=2),
                                dbc.Col([
                                        dcc.Slider(
                                                id='rotary',
                                                min= min(rotary_encoder_range), 
                                                max = max(rotary_encoder_range),
                                                )   
                                        ]),
                                ], align="center", className="mt-5"), 

                        ])
                ], color="dark" , inverse=True, className="mb-2")

rotary_encoder = dbc.Card([
                        dbc.CardBody([
                                        
                                        html.P("Use the rotary knob to adjust values"),               
                                        dbc.Row([
                                                dbc.Col([
                                                        dcc.Slider(
                                                                id='rotary_',
                                                                min= min(rotary_encoder_range), 
                                                                max = max(rotary_encoder_range),
                                                                )   
                                                        ])
                                                ], align="center", className="mt-5") #margin top 3 points
                                        ])
                        ], color="dark" , inverse=True, className="mb-2")

col_w = 3
controls = dbc.Card([
                        dbc.CardBody([
                                dbc.Row([ 
                                        dbc.Col([
                                                html.H4("Setup", className="card-title"),
                                                html.H6("Control the communicatino with Arduino", 
                                                        className="card-subtitle"),
                                                ], width=3, md=3, lg=3),

                                        dbc.Col([
                                                dbc.Button("Open port", id="port_controller"),
                                                html.P("No port", id="port_stat"),
                                                ], width=col_w, md=col_w, lg=col_w),

                                        dbc.Col([
                                                dbc.DropdownMenu(
                                                                id="port_name",
                                                                label="Port",
                                                                children=[
                                                                        dbc.DropdownMenuItem(id='COM3', children="COM3"),
                                                                        dbc.DropdownMenuItem(id='COM4', children="COM4"),
                                                                        dbc.DropdownMenuItem(id='COM5', children="COM5"),
                                                                        ],
                                                                ),
                                                html.P("", id="port_status"),
                                                ], width=col_w, md=col_w, lg=col_w),
                                        dbc.Col([
                                                html.P("Nothing!", id="serial_val"),
                                                ], width=col_w, md=col_w, lg=col_w),
                                dbc.Row([      
                                        dcc.Interval(
                                                id='interval_component',
                                                interval= 50, # in milliseconds
                                                n_intervals=0
                                                ),
                                                
                                        ])
                                ], no_gutters=True, justify="center",)
                                ])
                        ], color="dark" , inverse=True, className="mb-2")


control_panel = dbc.Card([
                        dbc.CardBody([
                                dbc.Row([
                                        dbc.Button("Options", id="show_options"),
                                        html.Hr(),
                                        ], className="mb-4"),

                                dbc.Row([
                                        dbc.Fade([controls],
                                                id="advanced_options",
                                                is_in=False,
                                                appear=False),
                                        ])
                                ])
                        ], color="dark" , inverse=True, className="mb-3")

######################################################################
### Dash App Layout
######################################################################
app.layout = dbc.Container([
                                setup_row,
                                gauges,
                                # rotary_encoder,
                                control_panel,
                            ], fluid=True,)

######################################################################
### Dash App Callbacks
######################################################################


@app.callback(
    Output("port_status", "children"),
    [Input("COM3", "n_clicks"),
    Input("COM4", "n_clicks"),
    Input("COM5", "n_clicks")]
)
def set_com_port(c3, c4, c5):
    global port

    ctx = dash.callback_context
    if not ctx.triggered:
        return "Active port: {}".format(port)
    else:
        port = ctx.triggered[0]["prop_id"].split(".")[0] 
        print (port)
        return "Active port: {}".format(port)


@app.callback(
    Output("advanced_options", "is_in"),
    [Input("show_options", "n_clicks")],
    [State("advanced_options", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in

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
    Output(component_id='rotary', component_property='value'),
    Output(component_id='rotary_status', component_property='children'),
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
                data = serial_msg.split("\r\n")
                msg = data[-2]
                knob_values = json.loads(msg)

                msg = ""

                for key, value in knob_values.items():
                    msg = msg+ "{}: {}, ".format(key[-2:], value)

                # just to clip the rotary value!
                knob_values["rotary_knob"] = max (min(rotary_encoder_range), 
                                                  min(knob_values["rotary_knob"], 
                                                      max(rotary_encoder_range)))

                return ([msg, 
                        knob_values["knob_00"],
                        knob_values["knob_01"],
                        knob_values["knob_02"],
                        knob_values["knob_03"],
                        knob_values["knob_04"],
                        knob_values["knob_05"],
                        knob_values["rotary_knob"],
                        knob_values["rotary_knob"],])
            except:
                counter += 1
                print ("had issues!",counter)
                return (9*[dash.no_update])
    # if port doesn't exist or is closed
    return (["Still Nothing", 0, 0, 0, 0, 0, 0, 0, 0])

######################################################################
### Dash App Running!
######################################################################
mode_options = {'debug':'d', 'local':'l', 'remote':'r'}
mode_selection = 'debug'
if __name__ == '__main__':
    mode = mode_options[mode_selection]
    if mode =='d':
        # for test and debug
        app.run_server(debug=True)
    elif mode=='l':
        # to run on lovel device
        app.run_server(debug=False)

    elif mode=='r':
        """
        To run and access it over network
        Access it over network on Chrome at:
              server_ip:8080
              i.e.: 192.168.86.34:8080
        """
        app.run_server(debug=False, port=8080, host='0.0.0.0')
