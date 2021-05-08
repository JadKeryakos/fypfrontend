import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import requests
from app import app
from dash.dependencies import Input, Output
import pandas as pd

tests_labels = ["testFailed", "testPassed", "Average"]


def request_generator(request_type, url, request_body):
    if request_type == "post":
        response = requests.post(url, json=request_body)
    else:
        response = requests.get(url)

    return response.json()


def fetch_latest_build_test(size):
    build_names_json = request_generator("get", "http://localhost:8081/builds/{}".format(size), None)
    build_names_list = []
    for build in reversed(build_names_json):
        build_names_list.insert(0, build['buildName'])

    data = pd.DataFrame(build_names_list, columns=['name']).name.unique()
    return data


tests_stats_layout = [html.Div([html.H3("Statistics on the latest tests"),
                                dcc.Input(id="tests_input", type="number", placeholder="Enter Limit"),
                                dcc.Graph(
                                    figure={},
                                    id='test_graph'
                                ),
                                html.H3("Aggregation of the last N tests"),
                                dcc.Input(id="test-bar-input", value=2, type="number", placeholder="Enter Aggregation "
                                                                                                   "Size"),
                                dcc.Graph(
                                    id='Test-Aggregation-Graph',
                                    figure={}
                                ),
                                html.H3("Comparison of selected builds"),
                                html.Div(
                                    id='my-dropdown-parent-test',
                                    children=[dcc.Store(id='data-store-test'),
                                              dcc.Interval(interval=120 * 1000, id='interval-test'),
                                              dcc.Dropdown(
                                                  id='my-dropdown-test',
                                                  options=[],
                                                  value=fetch_latest_build_test(2),
                                                  multi=True
                                              )
                                              ]
                                ),
                                html.Div(id='my-container'),
                                dcc.Graph(
                                    id='ComparatorGraph-test',
                                    figure={}
                                )
                                ])]


def parse_response_test(payload):
    res = dict()
    res["Builds"] = list()
    res["Average"] = list()
    for key in tests_labels:
        res[key] = list()
    for elt in payload:
        for key in elt:
            if key in tests_labels:
                res[key].append(elt[key])
            elif key == "build":
                res["Builds"].append(elt[key]["build_name"])
    for elt in range(len(res["testFailed"])):
        res["Average"].append(((res["testPassed"][elt] / (res["testPassed"][elt] + res["testFailed"][elt])) / 2) * 100)
    return res


def parse_test_data(json_data):
    res = dict()
    for key in json_data.keys():
        res[key] = dict()
    for key in json_data.keys():
        for obj in json_data[key]:
            if obj != "build-name":
                res[key][obj] = json_data[key][obj]
    return res


# Create a dictionary representing the data for the bar graph
def parse_test_data_for_comparison(value):
    # To avoid returning a dic of null
    if value is None or len(value) == 0:
        return {}
    # API call to get build stats for specific build names fetched from the dropdown
    comparison_data = request_generator("post", "http://localhost:8081/build/tests/names/", {"names": value})
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


@app.callback(
    Output("test_graph", "figure"),
    Input("tests_input", "value"),
)
def graph_render(number):
    if number:
        request_url = "http://localhost:8081/build/tests/last/" + str(number)
    else:
        request_url = "http://localhost:8081/tests"
    df = parse_response_test(request_generator("get", request_url, None))
    fig = px.line(df, x="Builds", y=tests_labels, height=800, title="Tests Data", template="presentation")
    fig.update_traces(mode='markers+lines')
    return fig


@app.callback(
    Output("Test-Aggregation-Graph", "figure"),
    Input("test-bar-input", "value")
)
def test_bar_render(number):
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
        parse_test_data(request_generator("post", "http://localhost:8081/builds/test/agg", body))),
        barmode="group", template="presentation")
    return fig1


@app.callback(
    Output('data-store-test', 'data'),
    Input('interval-test', 'n_intervals'))
def update_time(n_intervals):
    return fetch_latest_build_test(10)


@app.callback(
    Output('my-dropdown-test', 'options'),
    [Input('data-store-test', 'data'),
     Input('my-dropdown-parent-test', 'n_clicks')])
def update_comp_graph(data, n_clicks):
    if data:
        return [{'label': i, 'value': i} for i in data]


@app.callback(
    Output('ComparatorGraph-test', 'figure'),
    Input('my-dropdown-test', 'value')
)
def update_graph(value):
    return parse_test_data_for_comparison(value)
