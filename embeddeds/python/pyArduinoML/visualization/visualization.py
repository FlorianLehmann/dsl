import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import random
from datetime import datetime

import networkx as nx


NUMBER_OF_VALUES = 10
INTERVAL = 1000


class _Application:
    def __init__(self, name, graph, bricks):
        self.name = name
        self.graph = graph
        self.bricks = bricks


class _Brick:
    def __init__(self, name):
        self.name = name
        self.values = []
        self.timestamps = []


def plot_brick(i, brick):
    return go.Scatter(
        x=brick.timestamps,
        y=brick.values,
        name=brick.name,
        mode='lines+markers',
        yaxis=f'y{i}'
    )


def plot_bricks(bricks):
    pass


def create_graph():
    G=nx.random_geometric_graph(200,0.125)
    pos=nx.get_node_attributes(G,'pos')
    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d
    p=nx.single_source_shortest_path_length(G,ncenter)
    edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
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
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
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
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
        node_info = '# of connections: '+str(len(adjacencies[1]))
        node_trace['text']+=tuple([node_info])

    fig = go.Figure(data=[edge_trace, node_trace],
            layout=go.Layout(
            title='<br>Network graph made with Python',
            titlefont=dict(size=16),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002 ) ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    return fig

def debug(application):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(application.name,
                    external_stylesheets=external_stylesheets)
    traces = [plot_brick(i, brick) for i, brick in enumerate(application.bricks, 1)]

    fig = tools.make_subplots(
        rows=len(traces), cols=1, subplot_titles=[brick.name for brick in application.bricks],
        shared_xaxes=True, shared_yaxes=False, vertical_spacing=0.1,
    )

    for i in range(1, len(traces)+1):
        fig['layout'][f'yaxis{i}'].update(categoryorder='array', categoryarray=['LOW', 'HIGH'], type='category')
    
    for i, trace in enumerate(traces, 1):
        fig.append_trace(trace, i, 1)
    
    graph = create_graph()

    app.layout = html.Div([
        html.H4(application.name),
        html.Div([dcc.Graph(figure=fig, id='bricks'), dcc.Graph(figure=graph, id='graph')], id='update-plot'),
        dcc.Interval(
            id='interval-component',
            interval=INTERVAL,  # in milliseconds
            n_intervals=0
        )
    ])

    @app.callback(Output('bricks', 'figure'), [Input('interval-component', 'n_intervals')], [State('bricks', 'figure')])
    def update_plot(n, fig):
        traces = fig['data']
        now = datetime.now()
        for trace in traces:
            x = trace['x']
            y = trace['y']
            y.append(random.choice(('LOW', 'HIGH')))
            if len(y) > NUMBER_OF_VALUES:
                y.pop(0)
            x.append(now)
            if len(x) > NUMBER_OF_VALUES:
                x.pop(0)
        return fig

    app.run_server(debug=True)


def main():
    timestamps = list(range(20))
    button = _Brick("Button")
    led = _Brick("Led")
    bricks = [button, led]
    application = _Application("RedButton", None, bricks)
    debug(application)


if __name__ == '__main__':
    main()
