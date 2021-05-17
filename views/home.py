from dash import dash

from app import app
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

home_layout = html.Div(
    [(dbc.Jumbotron(
        [
            dbc.Row(
                html.H1("IdealWorks Pipeline Statistics", className="display-3"), justify="center"),
            dbc.Row(
                html.H1(" ", className="display-3"), justify="center"),
            dbc.Row(
                html.H1(" ", className="display-3"), justify="center"),
            dbc.Row([
                html.Img(src=app.get_asset_url('BMW.png'), height=280, alt="centered image"),
                html.Img(src=app.get_asset_url('idealworks-removebg-preview.png'), height=280, alt="centered image"),
            ],
                justify="center"),

        ]
    )),
        dbc.Row(
            html.Img(src=app.get_asset_url('idw.png'), height=580, alt="centered image"),
        )
    ],

)
