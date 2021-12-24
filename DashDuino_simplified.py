'''
    File name: DashDuino_dbc_app.py
    Author: Ardavan Bidgoli
    Date created: 06/13/2021
    Date last modified: 12/14/2021
    Python Version: 3.7.7

    License: MIT
'''

######################################################################
### Imports
######################################################################
import dash
from dash import dcc
from dash import html
# from dash_html_components.Col import Col
# from dash_html_components.H4 import H4
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash_extensions import WebSocket

# import dash_html_components as html

from dash.dependencies import Input, Output, State
# from dash_html_components.Hr import Hr

import serial
import json
import argparse

import socket
import time

from src.machinaRobot import MachinaRobot  
######################################################################
### Arguments
######################################################################
parser = argparse.ArgumentParser(prog='DashDuino',
                                description="A Dash app to communicate with Arduino board")
parser.add_argument('mode', 
                        help="Run the App in \"debug\", \"local\", or \"remote\" mode (str)", 
                        default= "debug",
                        nargs='?',
                        type=str)

parser.add_argument('comPort', 
                        help="Select the COM port to use, defulat is \"COM4\" (str)", 
                        default='COM4',
                        nargs='?',
                        type=str)

parser.add_argument('baudRate', 
                        help="Defeins the baudrate for the port, defulat is 230400 (int)", 
                        default=230400,
                        nargs='?',
                        type=int)

args = parser.parse_args()

port = args.comPort
mode_selection = args.mode
baudrate_val = args.baudRate
default_port = port


######################################################################
### Variables
######################################################################
serial_port = None
knob_values = {}
counter = 0
timeout_val = 1000
rotary_encoder_range = [-2000, 2000]

machina = None
client = None
abb_ip = '127.0.0.1'
abb_port = 7000
buffer_size = 1024


min_height = -20
max_height = -min_height

min_zone = 0
max_zone = 20

min_speed = 0
max_speed = 1000

"""
Sample of data collected from the Arduino sketch
{"knob_00":283,"knob_01":258,"knob_02":264,"knob_03":310,"knob_04":355,"knob_05":315,"rotary_knob":2310}
"""
######################################################################
######################################################################
### Dash App Begins Here
######################################################################
######################################################################
# styling variables
show_values_on_knobs = False
col_w = 3

######################################################################
### Dash App setup
######################################################################
external_stylesheets = [dbc.themes.CYBORG]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


######################################################################
### Dash App components
######################################################################
# the title row
title_row = dbc.Card([
                    dbc.CardBody([
                            dbc.Row([html.H1("DashDuino")]),
                    dbc.Row([
                            html.P("by Ardavan Bidgoli | 2021")])
                        ])
                    ], color="light", outline=True, className="mb-2")

gauge_color= "#2186f4"
# the main card to contain all the readings from knobs
gauges = dbc.Card([
                        dbc.CardBody([
                        html.H4("Knobs", id="Knobs_title"),
                        html.P("Use the mixer knobs to set values", id="Knobs_p"),
                        html.Hr(),
                        dbc.Row([
                                dbc.Col([
                                        html.Div(
                                                [   
                                                dbc.Button("Send to Robot", 
                                                            id= "send_data_button",
                                                            className="me-lg-2",
                                                            color='dark')
                                                ],
                                                className="d-grid gap-2 d-md-flex justify-content-md-center",),
                                        html.P(id="send_data_button_status"),
                                        html.Hr(),
                                        html.Div(
                                                [
                                                    dbc.Input(id="score_input", 
                                                              placeholder="Type score here", 
                                                              type="text",
                                                              size="lg", 
                                                              ),
                                                    html.Br(),
                                                    html.P("Score here...",
                                                           id="score_input_status"),
                                                    
                                                    dbc.Button("Initiate Robot", 
                                                                id= "init_robot",
                                                                className="me-lg-2",
                                                                color='dark'),
                                                    html.P("",
                                                           id="init_robot_status"),
                                                ],
                                                className="d-grid  justify-content-md-center",)
                                        ],
    
                                        width=4, align="center"),
                                
                                dbc.Col([
                                        dbc.Row([
                                            dbc.Col(
                                                daq.Gauge(
                                                        id='knob_01',
                                                        label="Zone",
                                                        min= min_zone, 
                                                        max = max_zone,
                                                        color=gauge_color,
                                                        showCurrentValue=True,
                                                        #showCurrentValue=show_values_on_knobs,
                                                        ),)
                                                ], align="center"),
                                        dbc.Row([
                                            dbc.Col(
                                                daq.Gauge(
                                                        id='knob_02',
                                                        label="Speed",
                                                        min= min_speed, 
                                                        max= max_speed,
                                                        # scale={'start': min_speed, 'interval': 100, 'labelInterval': 1},
                                                        color=gauge_color,
                                                        showCurrentValue=True,
                                                        #showCurrentValue=show_values_on_knobs,
                                                        ),)
                                                ], align="center"),
                                        ], width=4),
                               
                                dbc.Col( 
                                        [daq.Gauge(
                                                id='knob_00',
                                                label="Main",
                                                min= min_height, 
                                                max = max_height,
                                                size= 300,
                                                color= gauge_color,
                                                showCurrentValue=True,
                                                # showCurrentValue=show_values_on_knobs,
                                                
                                                ),
                                        ], width=4),
                                ], align="center"),
                        # dbc.Row([
                        #         dbc.Col([
                        #                 html.H3("No read yet", 
                        #                         id="rotary_status",
                        #                         style={'textAlign': 'center'}
                        #                         ),
                                                
                        #                 ], width=2),
                        #         dbc.Col([
                        #                 dcc.Slider(
                        #                         id='rotary',
                        #                         min= min(rotary_encoder_range), 
                        #                         max = max(rotary_encoder_range),
                        #                         )   
                        #                 ]),
                        #         ], align="center", className="mt-5"), 

                        ])
                ], color="light" , inverse=True, className="mb-2")

# Dedicated card for the rotary knob, 
# Not used in final code, kept here for a reference 
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
                        ], color="light" , inverse=True, className="mb-2")

# the main card to contain setup and monitor tools
# it will be hold inside a dcc.Fade object
controls = dbc.Card([
                        dbc.CardBody([
                                dbc.Row([ 
                                        dbc.Col([
                                                html.H4("Setup", className="card-title"),
                                                html.H6("Control the communicatino with Arduino", 
                                                        className="card-subtitle"),
                                                ], width=4, md=3, lg=3),

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
                                                                        dbc.DropdownMenuItem(id='COM6', children="COM6"),
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
                                                interval= 250, # in milliseconds
                                                n_intervals= 0
                                                ),
                                        WebSocket(url="ws://127.0.0.1:6999/Bridge", id="ws")
                                             
                                        ])
                                ], no_gutters=True, justify="center",)
                                ])
                        ], color="light" , inverse=True, className="mb-2", id="control_card")

# the card to organize the flip switch for controls
# as well as the control card
control_panel = dbc.Card([
                        dbc.CardBody([
                                dbc.Row([
                                        dbc.Col([html.H6("Control Display", 
                                                className="card-subtitle")
                                                ], width=2),
                                        dbc.Col([daq.BooleanSwitch(
                                                                id='text_switch',
                                                                on=True,
                                                                label="Show Knob Lable",
                                                                labelPosition="top"
                                                                ),
                                                ], width=2),
                                        dbc.Col([daq.BooleanSwitch(
                                                                id='setup_switch',
                                                                on=False,
                                                                label="Show Advanced",
                                                                labelPosition="top"
                                                                ),
                                                ], width=2),   
                                        ], className="mb-2"),                                     
                                dbc.Row([
                                        controls
                                        ], className="mb-2")
                                ])
                        ], color="light" , inverse=True, className="mb-3")

######################################################################
### Dash App Layout
######################################################################
app.layout = dbc.Container([
                                title_row,
                                gauges,
                                control_panel,
                                dcc.Store(id='port_name_shared_data'),
                                dcc.Store(id='knob_shared_data'),
                                ],
                           #fluid=True,
                           )

######################################################################
### Dash App Callbacks
######################################################################
cmd_qeue = []
@app.callback(
    #Output("send_data_button_status", "children"), 
    Output("init_robot_status", "children"),
    [Input("init_robot", "n_clicks")]
)
def init_robot_connection(n):
    global cmd_qeue 
    if n:
        if len(cmd_qeue) == 0:
            cmd_qeue.append('MoveTo(360, 0, 600);')
        return dash.no_update
    else:
        return dash.no_update
"""    
def contact_robot(cmd):
    global client
    try :
        client.connect((abb_ip,abb_port))
    except:
        print(client)
    try: 
        msg = client.recv(buffer_size)
        print (msg)     
    except:
        print("Hah?") 
        
    time.sleep(1)
     
    cmd = "@1 4 100;"
    
    try:
        client.send(bytes(cmd, "ascii"))
        time.sleep(1)
        msg = client.recv(buffer_size)
        print(msg)
    except:
        msg = "Oooops!"
        print (msg)
        
    #client.close()   
    return msg

@app.callback(
    #Output("init_robot_status", "children"), 
    Output("ws", "send"),
    [Input("send_data_button", "n_clicks"),
     Input('knob_shared_data', 'data')]
)
def send_data_to_robot(n, knob_values):
    
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return dash.no_update 
    else:
        data = ctx.triggered[0]
        if data['prop_id'] == 'send_data_button.n_clicks' or knob_values['push_button']:
            print("OK, what is up?")
            cmd = "@1 4 {}".format(knob_values["knob_02"])
            msg = contact_robot(cmd)
            return "Just sent something: {}".format(msg)

"""  
@app.callback(
    #Output("send_data_button_status", "children"), 
    Output("ws", "send"),
    [Input("send_data_button", "n_clicks"),
     Input('knob_shared_data', 'data')]
)
def send_data_to_robot(n, knob_values):
    global cmd_qeue 
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return dash.no_update 
    else:
        data = ctx.triggered[0]
        if data['prop_id'] == 'send_data_button.n_clicks' or knob_values['push_button']:
            precision_msg = "PrecisionTo({});".format(float(knob_values["knob_01"]))
            speed_msg = "SpeedTo({});".format(knob_values["knob_02"])
            z_adjust_msg = "Move({},{},{});".format(0.0, 0.0, float(knob_values["knob_00"]))

            cmd_qeue.append(precision_msg)
            cmd_qeue.append(speed_msg)
            cmd_qeue.append(z_adjust_msg)
        
    while len(cmd_qeue) > 0:
        cmd = cmd_qeue.pop(0)
        print(cmd)
        return cmd 
    return dash.no_update


@app.callback(
    Output("send_data_button_status", "children"), 
    [Input("ws", "message")])
def message(e):
    if e:
        msg = json.loads(e['data'])
        return msg["last"]
    else:
        return dash.no_update
  
@app.callback(Output("score_input_status", "children"), 
              [Input("score_input", "value")])
def output_text(value):
    return value

  
####################
# style callbacks
####################
@app.callback(
    Output('control_card', 'style'),
    [Input('setup_switch', 'on')])
def update_output(on):
        if on:
                return {'display': 'block'}
        else:
                return {'display': 'none'}

####################
# Setup callbacks
####################
@app.callback(
        Output("port_status", "children"),
        Output('port_name_shared_data', 'data'),
        [Input("COM3", "n_clicks"),
        Input("COM4", "n_clicks"),
        Input("COM5", "n_clicks"),
        Input("COM6", "n_clicks")]
        )
def set_com_port(c3, c4, c5, c6):
        """
        Reads the name of COM port from the drop down menu
        updates the port varaibale accordingly.
        It is triggered by clic on any of the dropdown items 

        Args:
                c3, c4, c5 (int): the number of clicks on the port_controller button
        """
        # here we get the context of the call back
        # then we extract the information that we need
        ctx = dash.callback_context
        if not ctx.triggered:
                return "Active port: {}".format(default_port), dash.no_update
        else:
                port = ctx.triggered[0]["prop_id"].split(".")[0] 
                print (port)
                return "Active port: {}".format(port), port


        
@app.callback(
        Output(component_id='port_stat', component_property='children'),
        Output(component_id='port_controller', component_property='children'),
        Input(component_id='port_controller', component_property='n_clicks'),
        Input('port_name_shared_data', 'data'),
        )
def port_manager(val, port_name):
        """
        Manages the serial port
        At the begining, opens the port automatically
        Upon further clicks, closes or opens the port and updates the notes

        Args:
                val (int): the number of clicks on the port_controller button
        """
        global serial_port 
        global machina
        global client
        
        if port_name is None:
            port_name = port
            
        # if client is None:
        #     client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        #     print(client)
            
                
        # flip the port open and close on click
        timeout_val = 1000
        
        if val:
                if val % 2 == 1 :
                        serial_port.close()
                        return (["Port is closed","Open Port"])
                else:
                        serial_port = serial.Serial(port_name, baudrate=baudrate_val, timeout=timeout_val)
                        return (["Port is open","Close Port"])
        # opening the port on page load
        else:
                serial_port = serial.Serial(port_name, baudrate=baudrate_val, timeout=timeout_val)
                
                
                # opening bridge communication 
                machina = MachinaRobot()
                return (["Port is open","Close Port"])


@app.callback(
        Output(component_id='serial_val', component_property='children'),
        Output(component_id='knob_00', component_property='value'),
        Output(component_id='knob_01', component_property='value'),
        Output(component_id='knob_02', component_property='value'),
        Output('knob_shared_data', 'data'),
        Input(component_id="interval_component", component_property="n_intervals"),
        )
def update_serial(interavl):
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
        knob_values = None

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
                            # knob_values["rotary_knob"] = max (min(rotary_encoder_range), 
                            #                                 min(knob_values["rotary_knob"], 
                            #                                 max(rotary_encoder_range)))
                                
                            
                            
                            # adjusting the values to fit the z and v steps of RAPID
                            knob_values["knob_00"] = round((((knob_values["knob_00"]/1000)*(max_height-min_height)) + min_height),1)
                            knob_values["knob_01"] = int(((knob_values["knob_01"]/1000)*(max_zone-min_zone)) + min_zone)
                            knob_values["knob_02"] = (int((((knob_values["knob_02"]+80)/1000)*(max_speed-min_speed)) + min_speed)//100)*100
                            
                            
                            if knob_values["knob_01"] > 5:
                                knob_values["knob_01"] = int((knob_values["knob_01"]//5)*5)
                            
                                
                            # returining the data
                            return ([msg, 
                                    knob_values["knob_00"],
                                    knob_values["knob_01"],
                                    knob_values["knob_02"],
                                    #knob_values["knob_03"],
                                    knob_values,
                                    ])
                        except:
                            print("Error: {}".format(knob_values))
                            return (5*[dash.no_update])
        # if port doesn't exist or is closed
        return (["Still Nothing",  0, 0, 0, None])





######################################################################
### Dash App Running!
######################################################################
mode_options = {'debug':'d', 'local':'l', 'remote':'r'}
#mode_selection = 'debug'

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
