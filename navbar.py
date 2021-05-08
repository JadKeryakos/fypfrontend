import dash_bootstrap_components as dbc
import dash_html_components as html
PLOTLY_LOGO = "https://media-exp1.licdn.com/dms/image/C4D0BAQEcaCgbdHgkYQ/company-logo_200_200/0/1605701418054?e" \
              "=2159024400&v=beta&t=rw6rRDs5W4c281bo7vY6cBLdLZRs70aoIw-z0HgidFg "

navbar = dbc.NavbarSimple(

    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home")),
        dbc.NavItem(dbc.NavLink("CppCheck", href="/cpp-check")),
        dbc.NavItem(dbc.NavLink("Bazel Stats", href="/bazel-stats")),
        dbc.NavItem(dbc.NavLink("Tests Stats", href="/tests-stats")),
    ],
    brand="Iw.Hub Pipeline Statistics",
    brand_href="/home",
    color="primary",
    dark=True,
)