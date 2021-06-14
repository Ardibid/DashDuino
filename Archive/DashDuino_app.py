import dash
import dash_core_components as dcc

import dash_daq as daq
import dash_html_components as html
import serial
from dash.dependencies import Input, Output

import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

serial_port = None
knob_values = {}
counter = 0

app.layout = html.Div([
    daq.Gauge(
        id='knob_00',
        label="Knob 00",
        min= 0, 
        max = 1023,
        showCurrentValue=True,
    ),
    daq.Gauge(
        id='knob_01',
        label="Knob 01",
        min= 0, 
        max = 1023,
        showCurrentValue=True,
    ),
    daq.Gauge(
        id='knob_02',
        label="Knob 02",
        min= 0, 
        max = 1023,
        showCurrentValue=True,
    ),
    daq.Gauge(
        id='knob_03',
        label="Knob 03",
        min= 0, 
        max = 1023,
        showCurrentValue=True,
    ),
    daq.Gauge(
        id='knob_04',
        label="Knob 04",
        min= 0, 
        max = 1023,
        showCurrentValue=True,
    ),
    daq.Gauge(
        id='knob_05',
        label="Knob 05",
        min= 0, 
        max = 1023,
        showCurrentValue=True,
    ),
    html.Div(id='knob-output', ),
    html.Hr(),
    html.Button("Open port", id="port_controller"),
    html.P("No port", id="port_stat"),
    html.Hr(),
    html.Button("Read Serial", id="serial_read"),
    html.P("Nothing!", id="serial_val"),
    dcc.Interval(
            id='interval_component',
            interval= 50, # in milliseconds
            n_intervals=0
        )
])


@app.callback(
    Output(component_id='port_stat', component_property='children'),
    Output(component_id='port_controller', component_property='children'),
    Input(component_id='port_controller', component_property='n_clicks')
    )
def port_manager(val):
    global serial_port
    if val:
        if val % 2 == 0 :
            serial_port.close()
            return (["port is closed","close Port"])
        else:
            serial_port = serial.Serial('COM4',baudrate=115200, timeout=100)
            print (serial_port)
            return (["port is open","close Port"])
    else:
        return [dash.no_update, dash.no_update]

@app.callback(
    Output(component_id='serial_val', component_property='children'),
    Output(component_id='knob_00', component_property='value'),
    Output(component_id='knob_01', component_property='value'),
    Output(component_id='knob_02', component_property='value'),
    Output(component_id='knob_03', component_property='value'),
    Output(component_id='knob_04', component_property='value'),
    Output(component_id='knob_05', component_property='value'),
    Input(component_id='serial_read', component_property='n_clicks'),
    Input(component_id="interval_component", component_property="n_intervals"),
    )
def update_serila(value, interavl):
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
            return (dash.no_update*7)
    return (["Still Nothing", 0, 0, 0, 0, 0,0])

if __name__ == '__main__':
    app.run_server(debug=True)