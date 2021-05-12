import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
from app import app


# Generate request based on request_type, custom endpoint path, and a request body using a base_url
def request_generator(request_type, url, request_body):
    if request_type == "post":
        response = requests.post(url, json=request_body)
    else:
        response = requests.get(url)

    return response.json()


# API call to get the last 10 builds names
def fetch_results_build(type):
    build_names_json = request_generator("get", "https://fypbackendstr.herokuapp.com/builds", None)
    success_counter = 0
    failure_counter = 0

    if type == "Test Status":
        for build in build_names_json:
            if build["buildStatus"] == "failure":
                failure_counter += 1
            else:
                success_counter += 1
    else:
        for build in build_names_json:
            if build["testsStatus"] == "failure":
                failure_counter += 1
            else:
                success_counter += 1
    res = {"status": ["failure", "success"], "value": [failure_counter, success_counter]}
    return res


builds_layout = [html.Div([

    html.P("Types:"),
    dcc.Dropdown(
        id='names',
        value='Test Status',
        options=[{'value': x, 'label': x}
                 for x in ['Build Status', 'Test Status']],
        clearable=False
    ),

    dcc.Graph(
        id="pie-chart",
        figure=px.pie(values=fetch_results_build("Test Status")["value"],
                      names=fetch_results_build("Test Status")["status"],
                      color=["lightcyan", "darkblue"],
                      color_discrete_sequence=["lightcyan", "darkblue"],
                      color_discrete_map={'success': 'lightcyan', 'failure': 'darkblue'})
    ),
])]


# print(px.data.iris().to_dict())

@app.callback(
    Output("pie-chart", "figure"),
    Input("names", "value")
)
def generate_chart(names):
    fig = px.pie(values=fetch_results_build(names)["value"], names={'success': 'success',
                                                                    'failure': 'failure'},
                 color=["lightcyan", "darkblue"],
                 color_discrete_sequence=["lightcyan", "darkblue"],
                 color_discrete_map={'success': 'lightcyan', 'failure': 'darkblue'})
    print(fetch_results_build(names)["value"], fetch_results_build(names)["status"])
    return fig
