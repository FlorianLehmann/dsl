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
    NUMBER_OF_VALUES = 20
    INTERVAL = 50

    def __init__(self, serialPort):
        self.serialPort = serialPort
        self.serial = initArduino(serialPort)
        self.serial.reset_input_buffer()
        self.lock = threading.Lock()
        self.traces = {}
        self.data = None

    def _read_serial(self):
        try:
            if not self.lock.locked():
                self.lock.acquire()
                line = self.serial.readline()
                self.lock.release()
                data = json.loads(line)
                self.data = data
        except Exception as e:
            pass
        return self.data

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

    def plot_state_machine(self, data):
        modes = data['StateMachine']

        g = nx.DiGraph()
        for mode in modes:
            for state in mode['states']:
                g.add_node(state['name'])
                for transition in state['transitions']:
                    g.add_edge(state['name'], transition['nextelement'])

        pos = nx.circular_layout(g)
    
        X = []
        Y = []
        T = []
        C = []
        for key, (x, y) in pos.items():
            X.append(x)
            Y.append(y)
            T.append(key)
            if key == data['current_state']:
                C.append('rgb(50,200,250)')
            else:
                C.append('rgb(50,50,50)')
        node_trace = go.Scatter(
            x=X,
            y=Y,
            text=T,
            mode='markers+text',
            textposition='top center',
            marker=dict(
                symbol='circle',
                size=20,
                color=C,
                line=dict(color='rgb(50,50,50)', width=0.5)
            ),
        )

        fig = go.Figure(
            data=[node_trace],
            layout=go.Layout(
                title=data['current_mode'],
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                annotations=[dict(x=pos[b][0], y=pos[b][1], xref='x', yref='y', axref='x', ayref='y', ax=pos[a][0], ay=pos[a][1], arrowhead=2, arrowsize=1) for a, b in g.edges()]
            )
        )

        return fig

    def start_app(self):
        while self.data is None:
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

        state_machine = self.plot_state_machine(data)

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
            timestamp = datetime.now()
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

        @app.callback(Output('state-machine', 'figure'), [Input('interval-component', 'n_intervals')], [State('state-machine', 'figure')])
        def update_plot(n, fig):
            data = self._read_serial()
            return fig

        app.run_server(debug=True)


def main():
    Visualizer("/dev/ttyACM0").start_app()


if __name__ == '__main__':
    main()
