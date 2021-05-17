import dash_bootstrap_components as dbc
import dash_html_components as html

navbar = dbc.NavbarSimple(

    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home")),
        dbc.NavItem(dbc.NavLink("Builds & Tests Stats", href="/builds-tests-stats")),
        dbc.NavItem(dbc.NavLink("CppCheck", href="/cpp-check")),
        dbc.NavItem(dbc.NavLink("Bazel Stats", href="/bazel-stats")),
    ],
    brand="Iw.Hub Pipeline Statistics",
    brand_href="/home",
    color="primary",
    dark=True,
)
