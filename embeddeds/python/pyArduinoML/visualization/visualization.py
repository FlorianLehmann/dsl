import random
from datetime import datetime
import json
import threading

import serial

import networkx as nx

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


class MockedSerial:
    def flush(self):
        pass

    def readline(self):
        return b"{\"name\": \"RedButton\", \"timestamp\": \"" + str(datetime.now()).encode() + b"\", \"StateMachine\": [{\"name\": \"day\", \"states\": [{\"name\": \"on\", \"transitions\": [{\"nextelement\": \"off\"}]}, {\"name\": \"alternate\", \"transitions\": [{\"nextelement\": \"on\"}, {\"nextelement\": \"off\"}, {\"nextelement\": \"on\"}]}, {\"name\": \"off\", \"transitions\": [{\"nextelement\": \"on\"}]}], \"transitions\": []}], \"Bricks\": [{\"type\": \"DigitalSensor\", \"name\": \"button\", \"value\": \"" + random.choice((b'HIGH', b'LOW')) + b"\", \"mode\": \"GRAPH\"}, {\"type\": \"AnalogicSensor\", \"name\": \"radio\", \"value\": " + str(random.randrange(100)).encode() + b", \"mode\": \"GRAPH\"}]}"


def initArduino(serialPort):
    try:
        print("Trying to connect on serial port " + serialPort)
        ser = serial.Serial(serialPort, dsrdtr=True, baudrate=115200)
        print("Connection successful")
        return ser
    except:
        newSerialPort = input(
            "Connection failed. Input the name of your serial port and press enter : ")
        return initArduino(newSerialPort)


class Visualizer:
    NUMBER_OF_VALUES = 100
    INTERVAL = 10

    def __init__(self, serialPort):
        self.serialPort = serialPort
        self.serial = initArduino(serialPort)
        self.serial.reset_input_buffer()
        self.lock = threading.Lock()
        self.traces = {}

    def _read_serial(self):
        try:
            if not self.lock.locked():
                self.lock.acquire()
                line = self.serial.readline()
                self.lock.release()
                return json.loads(line)
        except Exception as e:
            print(e)
        return None

    def plot_brick(self, i, fig, brick, timestamp):
        brick_type = brick['type']
        yaxis = fig['layout'][f'yaxis{i}']
        if brick_type == 'AnalogicSensor':
            yaxis = dict(
                range=[0, 10],
                showgrid=True,
                zeroline=True,
                showline=True,
                mirror='ticks',
                gridcolor='#bdbdbd',
                gridwidth=2,
                zerolinecolor='#969696',
                zerolinewidth=4,
                linecolor='#636363',
                linewidth=6
            )
        trace = go.Scatter(x=[timestamp], y=[brick['value']],
                           name=brick['name'], mode='lines+markers', yaxis=f'y{i}')
        fig.append_trace(trace, i, 1)
        return brick['name'], trace

    def plot_state_machine(self, modes):
        g = nx.DiGraph()
        for mode in modes:
            g.add_node(mode['name'])
            for transition in mode['transitions']:
                g.add_edge(mode['name'], transition['nextelement'])
            for state in mode['states']:
                g.add_node(state['name'])
                for transition in state['transitions']:
                    g.add_edge(state['name'], transition['nextelement'])
            h = g.subgraph([state['name'] for state in mode['states']])

        pos = nx.circular_layout(g)

        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
    
        X = []
        Y = []
        T = []
        for key, (x, y) in pos.items():
            X.append(x)
            Y.append(y)
            T.append(key)
        node_trace = go.Scatter(
            x=X,
            y=Y,
            text=T,
            mode='markers',
            marker=dict(
                symbol='circle',
                size=20,
                colorscale='Viridis',
                line=dict(color='rgb(50,50,50)', width=0.5)
            ),
        )

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='State Machine',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                annotations=[dict(x=pos[b][0], y=pos[b][1], xref='x', yref='y', axref='x', ayref='y', ax=pos[a][0] - pos[b][0], ay=pos[a][1] - pos[b][1], arrowhead=2, arrowsize=1) for a, b in g.edges()]
            )
        )

        return fig

    def start_app(self):
        data = None
        while data is None:
            data = self._read_serial()
        name = data['name']
        bricks = data['Bricks']
        timestamp = datetime.now()

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(name, external_stylesheets=external_stylesheets)

        fig = tools.make_subplots(
            rows=len(bricks), cols=1, subplot_titles=[brick['name'] for brick in bricks],
            shared_xaxes=True, shared_yaxes=False, vertical_spacing=0.1
        )

        self.traces = dict(self.plot_brick(i, fig, brick, timestamp)
                           for i, brick in enumerate(bricks, 1))

        state_machine = self.plot_state_machine(data['StateMachine'])

        app.layout = html.Div([
            html.H4(name),
            html.Div([dcc.Graph(figure=fig, id='bricks'), dcc.Graph(
                figure=state_machine, id='state-machine')], id='update-plot'),
            dcc.Interval(
                id='interval-component',
                interval=self.INTERVAL,  # in milliseconds
                n_intervals=0
            )
        ])

        @app.callback(Output('bricks', 'figure'), [Input('interval-component', 'n_intervals')], [State('bricks', 'figure')])
        def update_plot(n, fig):
            data = self._read_serial()
            print(data)
            timestamp = datetime.now()
            if data is None:
                for trace in fig['data']:
                    x = trace['x']
                    y = trace['y']
                    y.append(y[-1])
                    if len(y) > self.NUMBER_OF_VALUES:
                        y.pop(0)
                    x.append(timestamp)
                    if len(x) > self.NUMBER_OF_VALUES:
                        x.pop(0)
            else:
                bricks = data['Bricks']
                bricks = {brick['name']: brick for brick in bricks}
                
                for trace in fig['data']:
                    x = trace['x']
                    y = trace['y']
                    brick = bricks[trace['name']]
                    y.append(brick['value'])
                    if len(y) > self.NUMBER_OF_VALUES:
                        y.pop(0)
                    x.append(timestamp)
                    if len(x) > self.NUMBER_OF_VALUES:
                        x.pop(0)
            return fig

        app.run_server(debug=True)


def main():
    Visualizer("/dev/ttyACM0").start_app()


if __name__ == '__main__':
    main()
