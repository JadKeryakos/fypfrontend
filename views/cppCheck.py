import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import requests
from app import app
from dash.dependencies import Input, Output
import pandas as pd

labels = ["error", "performance", "portability", "style", "warning"]


# base_url = "http://localhost:8081/cppcheck/"


# Generate request based on request_type, custom endpoint path, and a request body using a base_url
def request_generator(request_type, url, request_body):
    if request_type == "post":
        response = requests.post(url, json=request_body)
    else:
        response = requests.get(url)

    return response.json()


# API call to get the last 10 builds names
def fetch_latest_build(size):
    build_names_json = request_generator("get", "http://localhost:8081/builds/{}".format(size), None)
    build_names_list = []
    for build in reversed(build_names_json):
        build_names_list.insert(0, build['buildName'])

    data = pd.DataFrame(build_names_list, columns=['name']).name.unique()
    return data


# Create a dictionary representing the data for the bar graph
def parse_data_for_comparison(value):
    # To avoid returning a dic of null
    if value is None or len(value) == 0:
        return {}
    # API call to get build stats for specific build names fetched from the dropdown
    comparison_data = request_generator("post", "http://localhost:8081/builds-name/cppChecks", {"buildNames": value})

    res = dict()
    for select_value in value:
        res[select_value] = dict()
    # fetch stats and fill the res dictionary with relevant info
    for data in comparison_data:
        for type_of_data in data:
            if type_of_data != 'build' and type_of_data != 'id':
                res[data["build"]["build_name"]][type_of_data] = data[type_of_data]
    # return the data to visualize on the graph
    return px.bar(pd.DataFrame.from_dict(res), barmode="group", template="presentation")


def parse_data(json_data):
    res = dict()
    for key in json_data.keys():
        res[key] = dict()
    for key in json_data.keys():
        for obj in json_data[key]:
            if obj != "build-name":
                res[key][obj] = json_data[key][obj]
    return res


def parse_response(payload):
    res = dict()
    res["Builds"] = list()
    for key in labels:
        res[key] = list()
    for elt in payload:
        for key in elt:
            if key in labels:
                res[key].append(elt[key])
            elif key == "build":
                res["Builds"].append(elt[key]["build_name"])
    return res


cpp_check_layout = [html.Div([html.H3("Statistics on the latest cppChecks"),
                              dcc.Input(id="input", type="number", placeholder="Enter Limit"),
                              html.Div(id="number-out"),
                              dcc.Graph(
                                  figure={},
                                  id='graph'
                              ),
                              html.H3("Aggregation of the last N cppChecks"),
                              dcc.Input(id="bar-input", value=2, type="number", placeholder="Enter Aggregation Size"),
                              html.Div(id="bar-number-out"),
                              dcc.Graph(
                                  id='Aggregation-Graph',
                                  figure={}
                              ),
                              html.H3("Comparison of selected builds"),
                              html.Div(
                                  id='my-dropdown-parent',
                                  children=[dcc.Store(id='data-store'),
                                            dcc.Interval(interval=120 * 1000, id='interval'),
                                            dcc.Dropdown(
                                                id='my-dropdown',
                                                options=[],
                                                value=fetch_latest_build(2),
                                                multi=True
                                            )
                                            ]
                              ),
                              html.Div(id='my-container'),
                              dcc.Graph(
                                  id='ComparatorGraph',
                                  figure={}
                              ),
                              ])]


@app.callback(
    Output("Aggregation-Graph", "figure"),
    Input("bar-input", "value")
)
def bar_render(number):
    if number is None:
        number = 2
    aggregation_size = int(number)
    aggregation_type = [
        "sum", "avg", "max", "min"
    ]
    body = {
        "aggregationSize": int(aggregation_size),
        "aggregations": aggregation_type
    }
    fig1 = px.bar(pd.DataFrame.from_dict(
        parse_data(request_generator("post", "http://localhost:8081/builds/cppCheck-agg", body))),
                  barmode="group", template="presentation")
    return fig1


@app.callback(
    Output("graph", "figure"),
    Input("input", "value"),
)
def graph_render(number):
    if number:
        request_url = "http://localhost:8081/cppChecks/last/" + str(number)
    else:
        request_url = "http://localhost:8081/cppChecks"
    df = parse_response(request_generator("get", request_url, None))
    fig = px.line(df, x="Builds", y=labels, height=800, title="CppCheck Data", template="presentation")
    fig.update_traces(mode='markers+lines')
    return fig


@app.callback(
    Output('data-store', 'data'),
    Input('interval', 'n_intervals'))
def update_time(n_intervals):
    return fetch_latest_build(10)


@app.callback(
    Output('my-dropdown', 'options'),
    [Input('data-store', 'data'),
     Input('my-dropdown-parent', 'n_clicks')])
def update_comp_graph(data, n_clicks):
    if data:
        return [{'label': i, 'value': i} for i in data]


@app.callback(
    Output('ComparatorGraph', 'figure'),
    Input('my-dropdown', 'value')
)
def update_graph(value):
    return parse_data_for_comparison(value)
