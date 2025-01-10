from dash import Dash, dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import general_info
import monthly_info

# Initialize app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.SUPERHERO],
)

# Updated button group with spacing and size
page_buttons = dbc.ButtonGroup(
    [
        dbc.Button(
            "General Information",
            id="general-info-btn",
            color="info",
            className="px-4 py-2",
        ),
        dbc.Button(
            "Monthly Information",
            id="monthly-info-btn",
            color="info",
            className="px-4 py-2",
        ),
        dbc.Button(
            "Shark Information",
            id="shark-info-btn",
            color="info",
            className="px-4 py-2",
        ),
        dbc.Button(
            "Victim Information",
            id="victim-info-btn",
            color="info",
            className="px-4 py-2",
        ),
    ],
    className="mb-4 d-flex justify-content-center",
)

# App layout
app.layout = html.Div(
    [
        html.H1(
            "Australian Shark Incident Data Analysis",
            className="text-center mb-4",
            style={
                "color": "#26a69a",
                "font-size": "2.5rem",
                "paddingTop": "25px",
            },
        ),
        dcc.Location(id="url", refresh=False),
        html.Div(page_buttons),
        html.Div(id="page-content"),
    ]
)


# Callback for button-based navigation
@app.callback(
    Output("url", "pathname"),
    [
        Input("general-info-btn", "n_clicks"),
        Input("monthly-info-btn", "n_clicks"),
        Input("shark-info-btn", "n_clicks"),
        Input("victim-info-btn", "n_clicks"),
    ],
)
def navigate_page(general_clicks, monthly_clicks, shark_clicks, victim_clicks):
    ctx = (
        callback_context.triggered[0]["prop_id"].split(".")[0]
        if callback_context.triggered
        else None
    )
    if ctx == "general-info-btn":
        return "/"
    elif ctx == "monthly-info-btn":
        return "/monthly"
    elif ctx == "shark-info-btn":
        return "/shark"
    elif ctx == "victim-info-btn":
        return "/victim"
    return "/"


# Routing callback
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return general_info.layout()
    elif pathname == "/monthly":
        return monthly_info.layout()
    elif pathname == "/shark":
        return html.Div(
            html.H3(
                "Shark Information Page Placeholder",
                style={"color": "#26a69a"},
            )
        )
    elif pathname == "/victim":
        return html.Div(
            html.H3(
                "Victim Information Page Placeholder",
                style={"color": "#26a69a"},
            )
        )
    return html.Div(
        "404: Page not found", style={"color": "red", "text-align": "center"}
    )


# Register callbacks for general_info
general_info.register_callbacks(app)
monthly_info.register_callbacks(app)
if __name__ == "__main__":
    app.run_server(debug=True)
