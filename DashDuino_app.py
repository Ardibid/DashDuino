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
    html.Div(id='knob-output', ),
    html.Hr(),
    html.Button("Open port", id="port_controller"),
    html.P("No port", id="port_stat"),
    html.Hr(),
    html.Button("Read Serial", id="serial_read"),
    html.P("Nothing!", id="serial_val"),
    dcc.Interval(
            id='interval_component',
            interval=1*200, # in milliseconds
            n_intervals=0
        )
])


########################################
## add multiple inputs for the app
########################################
@app.callback(
    Output(component_id='port_stat', component_property='children'),
    Output(component_id='port_controller', component_property='children'),
    Input(component_id='port_controller', component_property='n_clicks'))
def port_manager(val):
    global serial_port
    if val:
        if val % 2 == 0 :
            serial_port.close()
            return (["port is closed","close Port"])
        else:
            serial_port = serial.Serial('COM4',baudrate=9600, timeout=10)
            print (serial_port)
            return (["port is open","close Port"])
    else:
        return [dash.no_update,dash.no_update]

@app.callback(
    Output(component_id='serial_val', component_property='children'),
    Output(component_id='knob_00', component_property='value'),
    Output(component_id='knob_01', component_property='value'),
    Input(component_id='serial_read', component_property='n_clicks'))
def update_serila(value):
    if value:
        global serial_port
        global knob_values
        #serial_msg = serial_port.readline().decode('ascii')
        data_to_read = serial_port.inWaiting()
        serial_msg = serial_port.read(data_to_read).decode('ascii')
        msg = serial_msg.split("\r\n")[-2]
        knob_values = json.loads(msg)
        print (type(knob_values), knob_values)
        return ([msg, knob_values["knob_00"],knob_values["knob_01"]])
    return (["Still Nothing", 0, 0])

# @app.callback(
#     Output('knob-output', 'children'),
#     [Input('my-knob', 'value')])
# def update_output(value):
#     return 'The knob value is {}.'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)