# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
from app import app
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

import navbar as nv
from views.bazelStats import bazel_stats_layout
from views.testsStats import tests_stats_layout
from views.cppCheck import cpp_check_layout
from views.home import home_layout

server = app.server
app.title = "FYP-Frontend"

app.layout = html.Div([
    dcc.Location(id='location', refresh=False),
    nv.navbar,
    html.Div(id='page-content')
])

not_found_layout = [html.H3("404"), html.H5("Page not found")]
layout_dict = {
    '/': home_layout,
    '/home': home_layout,
    '/builds-tests-stats': tests_stats_layout,
    '/bazel-stats': bazel_stats_layout,
    '/cpp-check': cpp_check_layout,
}


@app.callback(Output('page-content', 'children'), [Input('location', 'pathname')])
def page_content_update(pathname):
    if layout_dict.get(pathname):
        return layout_dict[pathname]
    else:
        return not_found_layout


if __name__ == '__main__':
    # Runs on the following port: http://127.0.0.1:8050/
    app.run_server(debug=True)
