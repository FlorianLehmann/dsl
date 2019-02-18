import random
from datetime import datetime
import json

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
        return b"{\"StateMachine\": \"<dotfile>\", \"timestamp\": \"" + str(datetime.now()).encode() + b"\", \"name\": \"RedButton\", \"Bricks\": [{\"type\": \"DigitalSensor\", \"name\": \"button\", \"value\": \"" + random.choice((b'HIGH', b'LOW')) + b"\", \"mode\": \"GRAPH\"}, {\"type\": \"AnalogicSensor\", \"name\": \"radio\", \"value\": " + str(random.randrange(100)).encode() + b", \"mode\": \"GRAPH\"}]}"


def initArduino(serialPort):
    try:
        print("Trying to connect on serial port " + serialPort)
        ser = serial.Serial(serialPort)
        print("Connection successful")
        return ser
    except:
        newSerialPort = input(
            "Connection failed. Input the name of your serial port and press enter : ")
        return initArduino(newSerialPort)


class Visualizer:
    NUMBER_OF_VALUES = 100
    INTERVAL = 1000

    def __init__(self, serialPort):
        self.serialPort = serialPort
        self.serial = MockedSerial()
        self.serial.flush()
        self.traces = {}

    def _read_serial(self):
        line = self.serial.readline().decode()
        data = json.loads(line)
        return data

    def plot_brick(self, i, fig, brick, timestamp):
        brick_type = brick['type']
        yaxis = fig['layout'][f'yaxis{i}']
        if brick_type == 'DigitalSensor':
            yaxis.update(categoryorder='array', categoryarray=[
                         'LOW', 'HIGH'], type='category')
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

    def plot_state_machine(self, state_machine):
        return create_graph()

    def start_app(self):
        data = self._read_serial()
        name = data['name']
        bricks = data['Bricks']
        timestamp = data['timestamp']

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
            name = data['name']
            bricks = data['Bricks']
            bricks = {brick['name']: brick for brick in bricks}
            timestamp = data['timestamp']

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


def create_graph():
    G = nx.random_geometric_graph(200, 0.125)
    pos = nx.get_node_attributes(G, 'pos')
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x-0.5)**2+(y-0.5)**2
        if d < dmin:
            ncenter = n
            dmin = d
    p = nx.single_source_shortest_path_length(G, ncenter)
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([len(adjacencies[1])])
        node_info = '# of connections: '+str(len(adjacencies[1]))
        node_trace['text'] += tuple([node_info])

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
        title='<br>Network graph made with Python',
        titlefont=dict(size=16),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    return fig


def main():
    Visualizer("/dev/ttyASM0").start_app()


if __name__ == '__main__':
    main()
