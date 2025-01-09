import pandas as pd

from dash import Dash, dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"
df = pd.read_csv(data_path)

# Initialize the app with a Bootstrap theme
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

checkbox_items = dcc.Checklist(
    id="checkbox-items",
    options=[
        {"label": "Provoked", "value": "provoked"},
        {"label": "Unprovoked", "value": "unprovoked"},
    ],
    value=["provoked", "unprovoked"],
    className="checkbox-container",
    inline=True,
)

radio_together_separate = dcc.RadioItems(
    id="radio-together-separate",
    options=[
        {"label": "Together", "value": "together"},
        {"label": "Separate", "value": "separate"},
    ],
    value="together",
    className="radio-container",
)

reset_button = dbc.Button(
    "Reset Selection", id="reset-button", color="secondary", className="mt-3"
)

page_buttons = dbc.ButtonGroup(
    [
        dbc.Button("General Information", href="/", color="primary"),
        dbc.Button("Monthly Information", href="/monthly", color="primary"),
    ]
)

sparkyshark_box = html.Div("SparkyShark", className="text-box")


# Define the shared layout structure
def shared_layout(content_div):
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H1(
                        "Australian Shark Incident Data Analysis - Center of Page",
                        className="text-center text-light mb-4",
                        style={"paddingTop": "10px"},
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
                        children=[checkbox_items, radio_together_separate],
                    ),  # 1fr checklist and radio
                    html.Div(
                        className="grid-item", children=page_buttons
                    ),  # 6fr page links
                    html.Div(
                        className="grid-item", children=sparkyshark_box
                    ),  # 3fr SparkyShark
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
                        dcc.Graph(id="incident-trend"),
                        width=8,
                        style={"height": "110%"},
                    ),
                    dbc.Col(
                        [dcc.Graph(id="victim-injury-bar"), reset_button],
                        width=4,
                        style={"height": "110%"},
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
    line_fig = go.Figure(
        data=[
            go.Scatter(
                x=aggregated_data["incident_year"], y=aggregated_data["count"]
            )
        ]
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
    else:  # separate
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
                    marker_color="#42a5f5",
                ),
            ]
        )

    return line_fig, bar_fig, bar_click, trend_relayout


if __name__ == "__main__":
    app.run_server(debug=True)
