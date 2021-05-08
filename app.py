import flask
import dash
import dash_bootstrap_components as dbc

app = dash.Dash('app', external_stylesheets=[dbc.themes.FLATLY])

app.config['suppress_callback_exceptions'] = True
