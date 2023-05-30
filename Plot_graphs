import time
from smbus import SMBus
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

bus = SMBus(1)  # 1 indicates /dev/i2c-1

# PCF8591 and MAX30102 addresses
PCF8591_ADDR = 0x48
MAX30102_ADDR = 0x57  # This is a guess; check the actual address

# Initialize global data store
data = {
    'channel_{}'.format(i): []
    for i in range(6)
}

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1*1000,
    ),
])

@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    # Read from the PCF8591
    for i in range(4):
        bus.write_byte(PCF8591_ADDR, i)
        value = bus.read_byte(PCF8591_ADDR)
        data['channel_{}'.format(i)].append(value)

    # Read from the MAX30102
    for i in range(2):
        # You'll need to replace this with the actual code to read from the MAX30102
        value = bus.read_byte_data(MAX30102_ADDR, i)
        data['channel_{}'.format(i+4)].append(value)

    # Create new figure
    fig = go.Figure()

    # Add traces
    for i in range(6):
        fig.add_trace(go.Scatter(
            x=list(range(len(data['channel_{}'.format(i)]))),
            y=data['channel_{}'.format(i)],
            name='Channel {}'.format(i),
            mode='lines+markers'
        ))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
