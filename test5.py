import pandas as pd

from dash import Dash, dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"
df = pd.read_csv(data_path)
df = df.loc[df["provoked_unprovoked"] != "unknown"]

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,  # Allow dynamically generated components
)

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

reset_buttons = dbc.ButtonGroup(
    [
        dbc.Button(
            "Reset Graphs",
            id="reset-button",
            color="primary",
        ),
        dbc.Button(
            "Reset Filters",
            id="reset-filters-button",
            color="primary",
        ),
    ]
)

page_buttons = dbc.ButtonGroup(
    [
        dbc.Button("General Information", color="primary"),
        dbc.Button("Monthly Information", color="primary"),
        dbc.Button("Shark Information", color="primary"),
        dbc.Button("Victim Information", color="primary"),
    ]
)


# Define the shared layout structure
def shared_layout(content_div):
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
                className="grid-container",  # Apply CSS grid layout
                children=[
                    html.Div(className="grid-item"),  # 1fr empty space
                    html.Div(
                        className="grid-item dropdown-container",
                        children=dropdown_states,
                    ),  # 2fr dropdown
                    html.Div(
                        className="grid-item checkbox-container",
                        children=checkbox_radio_group,
                    ),  # 1fr checklist and radio
                    html.Div(
                        className="grid-item", children=page_buttons
                    ),  # 6fr page links
                    html.Div(
                        className="grid-item", children=reset_buttons
                    ),  # 3fr reset
                    html.Div(className="grid-item"),  # 1fr empty space
                ],
            ),
            content_div,
        ],
        fluid=True,
    )


# Define the content for the General Information page (2 rectangles)
def general_content():
    return html.Div(
        style={
            "height": "calc(85vh - 120px)",
            "padding": "1.5%",
        },
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="incident-trend",
                            style={"width": "100%", "height": "100%"},
                        ),
                        width=8,
                        style={"height": "98%"},
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(
                                id="victim-injury-bar",
                                style={"width": "100%", "height": "100%"},
                            ),
                        ],
                        width=4,
                        style={"height": "98%"},
                    ),
                ],
                className="h-100",
                style={"height": "100%"},
            )
        ],
    )


# App layout with routing
app.layout = html.Div(
    [
        dcc.Store(id="stored-bar-click"),
        dcc.Store(id="stored-line-relayout"),
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
    ]
)


# Callback to handle navigation
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    return shared_layout(general_content())


# Define callbacks for the graph in General Content
@app.callback(
    [
        Output("incident-trend", "figure"),
        Output("victim-injury-bar", "figure"),
        Output("stored-bar-click", "data"),
        Output("stored-line-relayout", "data"),
    ],
    [
        Input("dropdown-states", "value"),
        Input("checkbox-items", "value"),
        Input("radio-together-separate", "value"),
        Input("victim-injury-bar", "clickData"),
        Input("incident-trend", "relayoutData"),
        Input("reset-button", "n_clicks"),
    ],
    [
        State("stored-bar-click", "data"),
        State("stored-line-relayout", "data"),
    ],
)
def update_graphs(
    selected_states,
    checkbox_values,
    radio_value,
    bar_click,
    trend_relayout,
    reset_click,
    stored_bar_click,
    stored_line_relayout,
):
    ctx_id = ctx.triggered_id
    if ctx_id == "reset-button":
        # Reset graphs to initial state based on dropdown and checklist selections
        filtered_data = df[df["state_names"].isin(selected_states)]
        if (
            "provoked" in checkbox_values
            and "unprovoked" not in checkbox_values
        ):
            filtered_data = filtered_data[
                filtered_data["provoked_unprovoked"] == "provoked"
            ]
        elif (
            "unprovoked" in checkbox_values
            and "provoked" not in checkbox_values
        ):
            filtered_data = filtered_data[
                filtered_data["provoked_unprovoked"] == "unprovoked"
            ]

        # Create initial graphs
        aggregated_data = (
            filtered_data.groupby("incident_year")
            .size()
            .reset_index(name="count")
        )
        line_fig = go.Figure(
            data=[
                go.Scatter(
                    x=aggregated_data["incident_year"],
                    y=aggregated_data["count"],
                    mode="lines",
                    line=dict(color="#26a69a"),
                    name="Incidents",
                )
            ]
        )
        line_fig.update_layout(
            font=dict(color="#26a69a", size=18),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            # transition={"duration": 800, "easing": "sin-in-out"},
        )
        injury_counts = (
            filtered_data["victim_injury"].value_counts().reset_index()
        )
        bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=injury_counts["victim_injury"], y=injury_counts["count"]
                )
            ]
        )
        bar_fig.update_traces(marker_color="#26a69a")
        bar_fig.update_layout(
            font=dict(color="#26a69a", size=18),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            transition={"duration": 800, "easing": "sin-in-out"},
        )

        return line_fig, bar_fig, None, None

    # Retain or update stored values
    bar_click = (
        bar_click if ctx_id == "victim-injury-bar" else stored_bar_click
    )
    trend_relayout = (
        trend_relayout if ctx_id == "incident-trend" else stored_line_relayout
    )

    filtered_data = df[df["state_names"].isin(selected_states)]

    # Filter by provoked/unprovoked
    if "provoked" in checkbox_values and "unprovoked" not in checkbox_values:
        filtered_data = filtered_data[
            filtered_data["provoked_unprovoked"] == "provoked"
        ]
    elif "unprovoked" in checkbox_values and "provoked" not in checkbox_values:
        filtered_data = filtered_data[
            filtered_data["provoked_unprovoked"] == "unprovoked"
        ]

    # Handle bar click event
    if bar_click and "points" in bar_click:
        selected_injury = bar_click["points"][0]["x"]
        filtered_data = filtered_data[
            filtered_data["victim_injury"] == selected_injury
        ]

    # Handle line chart relayout (zooming or selection)
    if (
        trend_relayout
        and "xaxis.range[0]" in trend_relayout
        and "xaxis.range[1]" in trend_relayout
    ):
        start_year = int(float(trend_relayout["xaxis.range[0]"]))
        end_year = int(float(trend_relayout["xaxis.range[1]"]))
        filtered_data = filtered_data[
            (filtered_data["incident_year"] >= start_year)
            & (filtered_data["incident_year"] <= end_year)
        ]

    # Create graphs
    aggregated_data = (
        filtered_data.groupby("incident_year").size().reset_index(name="count")
    )

    if radio_value == "together":
        line_fig = go.Figure(
            data=[
                go.Scatter(
                    x=aggregated_data["incident_year"],
                    y=aggregated_data["count"],
                    mode="lines",
                    line=dict(color="#26a69a"),
                    name="All Incidents",
                )
            ]
        )
        line_fig.update_layout(
            font=dict(color="#26a69a", size=18),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            # transition={"duration": 800, "easing": "sin-in-out"},
        )
    else:  # separate
        provoked_data = filtered_data[
            filtered_data["provoked_unprovoked"] == "provoked"
        ]
        unprovoked_data = filtered_data[
            filtered_data["provoked_unprovoked"] == "unprovoked"
        ]

        provoked_agg = (
            provoked_data.groupby("incident_year")
            .size()
            .reset_index(name="provoked_count")
        )
        unprovoked_agg = (
            unprovoked_data.groupby("incident_year")
            .size()
            .reset_index(name="unprovoked_count")
        )

        line_fig = go.Figure(
            data=[
                go.Scatter(
                    x=provoked_agg["incident_year"],
                    y=provoked_agg["provoked_count"],
                    mode="lines",
                    line=dict(color="#26a69a"),
                    name="Provoked Incidents",
                ),
                go.Scatter(
                    x=unprovoked_agg["incident_year"],
                    y=unprovoked_agg["unprovoked_count"],
                    mode="lines",
                    line=dict(color="#ab47bc"),
                    name="Unprovoked Incidents",
                ),
            ]
        )
        line_fig.update_layout(
            legend=dict(
                orientation="h",
                x=0.5,
                y=-0.1,
                xanchor="center",
                yanchor="top",
                font=dict(size=12, color="#26a69a"),
            ),
            font=dict(color="#26a69a", size=18),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            # transition={"duration": 800, "easing": "sin-in-out"},
        )

    injury_counts = filtered_data["victim_injury"].value_counts().reset_index()

    if radio_value == "together":
        bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=injury_counts["victim_injury"], y=injury_counts["count"]
                )
            ]
        )
        bar_fig.update_traces(marker_color="#26a69a")
        bar_fig.update_layout(
            font=dict(color="#26a69a", size=18),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            transition={"duration": 800, "easing": "sin-in-out"},
        )
    else:
        provoked_counts = (
            filtered_data[filtered_data["provoked_unprovoked"] == "provoked"][
                "victim_injury"
            ]
            .value_counts()
            .reset_index()
        )
        unprovoked_counts = (
            filtered_data[
                filtered_data["provoked_unprovoked"] == "unprovoked"
            ]["victim_injury"]
            .value_counts()
            .reset_index()
        )
        provoked_counts.columns = ["victim_injury", "provoked_count"]
        unprovoked_counts.columns = ["victim_injury", "unprovoked_count"]

        combined_counts = pd.merge(
            provoked_counts, unprovoked_counts, on="victim_injury", how="outer"
        ).fillna(0)

        bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=combined_counts["victim_injury"],
                    y=combined_counts["provoked_count"],
                    name="Provoked",
                    marker_color="#26a69a",
                ),
                go.Bar(
                    x=combined_counts["victim_injury"],
                    y=combined_counts["unprovoked_count"],
                    name="Unprovoked",
                    marker_color="#ab47bc",
                ),
            ]
        )
        bar_fig.update_layout(
            legend=dict(
                orientation="h",
                x=0.5,
                y=-0.1,
                xanchor="center",
                yanchor="top",
                font=dict(size=12, color="#26a69a"),
            ),
            font=dict(color="#26a69a", size=18),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            margin=dict(t=20, b=100),
            transition={"duration": 800, "easing": "sin-in-out"},
        )

    return line_fig, bar_fig, bar_click, trend_relayout


@app.callback(
    [
        Output("dropdown-states", "value"),
        Output("checkbox-items", "value"),
        Output("radio-together-separate", "value"),
    ],
    Input("reset-filters-button", "n_clicks"),
)
def reset_app(n_clicks):
    if n_clicks:
        return (
            df["state_names"].unique().tolist(),
            ["provoked", "unprovoked"],
            "together",
        )
    raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
