import dash
import dash_core_components as dcc
import dash_html_components as html
import time
import psutil

from collections import deque
import plotly.graph_objs as go
import random

max_length = 50
times = deque(maxlen=max_length)
cpu=deque(maxlen=max_length)
memory=deque(maxlen=max_length)
disk=deque(maxlen=max_length)
# network=deque(maxlen=max_length)

data_dict = {"CPU":cpu,
"Memory": memory,
"Disk": disk}

def update_values(times, cpu, memory,disk):
    #network

    times.append(time.time())
    if len(times) == 1:
        #starting relevant values
        # cpu.append(random.randrange(180,230))
        # memory.append(random.randrange(95,115))
        # disk.append(random.randrange(170,220))
        # network.append(random.randrange(1000,9500))
        #cpu.append(random.randrange(180,230))
        #memory.append(random.randrange(95,115))
        cpu.append(psutil.cpu_percent())
        memory.append(psutil.virtual_memory().percent)
        disk.append(psutil.disk_usage('/').percent)
        # network.append(psutil.net_if_addrs())
    else:
        for data_of_interest in [cpu, memory, disk]:
            #disk,network
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))

    return times, cpu, memory, disk
    #disk, network

times, cpu, memory, disk = update_values(times, cpu, memory, disk)
#disk, , network

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
app = dash.Dash('vehicle-data',
                external_scripts=external_js,
                external_stylesheets=external_css)

app.layout = html.Div([
    html.Div([
        html.H2('CPU Data',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='vehicle-data-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['CPU','Memory','Disk'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1000,
        n_intervals=0),

    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('vehicle-data-name', 'value'),
     dash.dependencies.Input('graph-update', 'n_intervals')],
    )
def update_graph(data_names, n):
    graphs = []
    update_values(times, cpu, memory, disk)
    #disk, network
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'

    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs

if __name__ == '__main__':
    app.run_server(debug=True)