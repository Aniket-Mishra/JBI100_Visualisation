import pandas as pd

from dash import Dash, dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

# Load Data
data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"
df = pd.read_csv(data_path)
df = df.loc[df["provoked_unprovoked"] != "unknown"]

# Initialize App
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
)

# Dropdown for States
dropdown_states = dcc.Dropdown(
    id="dropdown-states",
    options=[
        {"label": state, "value": state}
        for state in df["state_names"].unique()
    ],
    value=df["state_names"].unique().tolist(),
    multi=True,
    className="dropdown-container",
)

# Checklist and Radio Items
checkbox_radio_group = html.Div(
    style={"display": "flex", "alignItems": "center", "gap": "10px"},
    children=[
        dcc.Checklist(
            id="checkbox-items",
            options=[
                {"label": "Provoked", "value": "provoked"},
                {"label": "Unprovoked", "value": "unprovoked"},
            ],
            value=["provoked", "unprovoked"],
            className="checkbox-container",
            inline=True,
            inputStyle={"margin-right": "5px"},
        ),
        dcc.RadioItems(
            id="radio-together-separate",
            options=[
                {"label": "Together", "value": "together"},
                {"label": "Separate", "value": "separate"},
            ],
            value="together",
            className="radio-container",
            inputStyle={"margin-right": "5px"},
        ),
    ],
)

# Reset Buttons
reset_buttons = dbc.ButtonGroup(
    [
        dbc.Button("Reset Graphs", id="reset-button", color="primary"),
        dbc.Button(
            "Reset Filters", id="reset-filters-button", color="primary"
        ),
    ]
)

# Page Buttons
page_buttons = dbc.ButtonGroup(
    [
        dbc.Button(
            "General Information", id="general-info-button", color="primary"
        ),
        dbc.Button(
            "Monthly Information", id="monthly-info-button", color="primary"
        ),
    ]
)


# Shared Layout
def shared_layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H1(
                        "Australian Shark Incident Data Analysis",
                        className="text-center mb-4",
                        style={"paddingTop": "10px", "color": "#26a69a"},
                    )
                )
            ),
            html.Div(
                className="grid-container",
                children=[
                    html.Div(className="grid-item"),
                    html.Div(
                        className="grid-item dropdown-container",
                        children=dropdown_states,
                    ),
                    html.Div(
                        className="grid-item checkbox-container",
                        children=checkbox_radio_group,
                    ),
                    html.Div(className="grid-item", children=page_buttons),
                    html.Div(className="grid-item", children=reset_buttons),
                    html.Div(className="grid-item"),
                ],
            ),
            html.Div(
                style={"height": "calc(85vh - 120px)", "padding": "1.5%"},
                children=[
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="main-graph-1",
                                    style={"width": "100%", "height": "100%"},
                                ),
                                width=8,
                                style={"height": "98%"},
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id="main-graph-2",
                                    style={"width": "100%", "height": "100%"},
                                ),
                                width=4,
                                style={"height": "98%"},
                            ),
                        ],
                        className="h-100",
                        style={"height": "100%"},
                    )
                ],
            ),
        ],
        fluid=True,
    )


# App Layout
app.layout = html.Div(
    [
        dcc.Store(id="view-mode", data="general"),  # Store for view mode
        dcc.Store(id="stored-bar-click"),  # Store for bar click info
        dcc.Store(
            id="stored-line-relayout"
        ),  # Store for line chart range info
        html.Div(id="page-content"),
    ]
)


# Callback to Render Layout
@app.callback(
    Output("page-content", "children"),
    Input("view-mode", "data"),
)
def render_layout(view_mode):
    return shared_layout()


# Callback to Update Graphs
@app.callback(
    [
        Output("main-graph-1", "figure"),
        Output("main-graph-2", "figure"),
    ],
    [
        Input("dropdown-states", "value"),
        Input("checkbox-items", "value"),
        Input("radio-together-separate", "value"),
        Input("view-mode", "data"),
        Input("stored-bar-click", "data"),
        Input("stored-line-relayout", "data"),
    ],
)
def update_graphs(
    selected_states,
    checkbox_values,
    radio_value,
    view_mode,
    bar_click,
    trend_relayout,
):
    # Data Filtering
    filtered_data = df[df["state_names"].isin(selected_states)]
    if "provoked" in checkbox_values and "unprovoked" not in checkbox_values:
        filtered_data = filtered_data[
            filtered_data["provoked_unprovoked"] == "provoked"
        ]
    elif "unprovoked" in checkbox_values and "provoked" not in checkbox_values:
        filtered_data = filtered_data[
            filtered_data["provoked_unprovoked"] == "unprovoked"
        ]

    # General View
    if view_mode == "general":
        # Incident Trend Line Graph
        aggregated_data = (
            filtered_data.groupby("incident_year")
            .size()
            .reset_index(name="count")
        )
        fig1 = go.Figure(
            data=[
                go.Scatter(
                    x=aggregated_data["incident_year"],
                    y=aggregated_data["count"],
                )
            ]
        )
        fig2 = go.Figure(
            data=[
                go.Bar(
                    x=aggregated_data["incident_year"],
                    y=aggregated_data["count"],
                )
            ]
        )

        return fig1, fig2


# Run Server
if __name__ == "__main__":
    app.run_server(debug=True)
