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

radio_items = dcc.RadioItems(
    id="radio-items",
    options=[
        {"label": "All Incidents", "value": "all"},
        {"label": "Provoked", "value": "provoked"},
        {"label": "Unprovoked", "value": "unprovoked"},
    ],
    value="all",
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
                        className="grid-item radio-container",
                        children=radio_items,
                    ),  # 1fr radio
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
        Input("radio-items", "value"),
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
    incident_type,
    bar_click,
    trend_relayout,
    reset_click,
    stored_bar_click,
    stored_line_relayout,
):
    ctx_id = ctx.triggered_id
    if ctx_id == "reset-button":
        # Reset graphs to initial state based on dropdown and radio selections
        filtered_data = df[df["state_names"].isin(selected_states)]
        if incident_type != "all":
            filtered_data = filtered_data[
                filtered_data["provoked_unprovoked"] == incident_type
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
            font=dict(color="#26a69a", size=12),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            transition={"duration": 800, "easing": "sin-in-out"},
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
            font=dict(color="#26a69a", size=12),
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
    if incident_type != "all":
        filtered_data = filtered_data[
            filtered_data["provoked_unprovoked"] == incident_type
        ]

    if bar_click and "points" in bar_click:
        selected_injury = bar_click["points"][0]["x"]
        filtered_data = filtered_data[
            filtered_data["victim_injury"] == selected_injury
        ]

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
                x=aggregated_data["incident_year"],
                y=aggregated_data["count"],
                mode="lines",
                line=dict(color="#26a69a", width=2),
                name="Shark Incidents",
            )
        ]
    )
    line_fig.update_layout(
        font=dict(color="#26a69a", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        # transition={"duration": 800, "easing": "sin-in-out"},
    )
    injury_counts = filtered_data["victim_injury"].value_counts().reset_index()
    bar_fig = go.Figure(
        data=[
            go.Bar(x=injury_counts["victim_injury"], y=injury_counts["count"])
        ]
    )
    bar_fig.update_traces(marker_color="#26a69a")
    bar_fig.update_layout(
        font=dict(color="#26a69a", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        transition={"duration": 800, "easing": "sin-in-out"},
    )

    return line_fig, bar_fig, bar_click, trend_relayout


if __name__ == "__main__":
    app.run_server(debug=True)
