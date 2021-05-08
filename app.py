import flask
import dash
import dash_bootstrap_components as dbc

server = flask.Flask('app')
app = dash.Dash('app', external_stylesheets=[dbc.themes.FLATLY], server=server)

app.config['suppress_callback_exceptions'] = True
