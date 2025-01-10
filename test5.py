import pandas as pd

from dash import Dash, dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"


def prepare_data(path: str) -> pd.DataFrame:

    df = pd.read_csv(data_path)
    df = df.loc[df["provoked_unprovoked"] != "unknown"]
    df.loc[
        df["shark_common_name"] == "shark_not_known", "shark_common_name"
    ] = "unknown"
    df.loc[
        df["shark_common_name"] == "bronze whaler shark", "shark_common_name"
    ] = "bronze whaler"
    df["shark_common_name"] = df["shark_common_name"].apply(
        lambda x: x.replace(" shark", "").title()
    )

    month_mapping = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }
    df["incident_month"] = df["incident_month"].map(month_mapping)
    return df


df = prepare_data(data_path)


def filter_data_by_states(
    df: pd.DataFrame, selected_states: list
) -> pd.DataFrame:
    return df[df["state_names"].isin(selected_states)]


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
            inputStyle={"margin-right": "5px", "padding": "2px"},
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

header_div = html.Div(
    "Australian Shark Incidents Analysis",
    style={
        "fontSize": "32px",
        "color": "#26a69a",
        "textAlign": "center",
        "padding": "10px",
        # "background-color": "#fff",
    },
)


# Define the shared layout structure
def shared_layout(content_div):
    return dbc.Container(
        [
            # dbc.Row(
            #     dbc.Col(
            #         html.H1(
            #             "Australian Shark Incident Data Analysis",
            #             className="text-center mb-4",
            #             style={"paddingTop": "10px", "color": "#26a69a"},
            #         )
            #     )
            # ),
            html.Div(
                style={"paddingTop": "15px"},
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
                        className="grid-item", children=header_div
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
            "height": "calc(90vh)",  # Increased container height
            # "padding": "-11%",
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
                        style={
                            "height": "45vh"
                        },  # Increased height for each graph
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id="victim-injury-bar",
                            style={"width": "100%", "height": "100%"},
                        ),
                        width=4,
                        style={
                            "height": "45vh"
                        },  # Increased height for each graph
                    ),
                ],
                className="h-50",
                style={"height": "50%"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="monthly-incidents-bar",
                            style={"width": "100%", "height": "100%"},
                        ),
                        width=6,
                        style={
                            "height": "45vh"
                        },  # Increased height for each graph
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id="top-sharks-bar",
                            style={"width": "100%", "height": "100%"},
                        ),
                        width=6,
                        style={"height": "45vh"},
                    ),
                ],
                className="h-50",
                style={"height": "50%"},
            ),
        ],
    )


# App layout with routing
app.layout = html.Div(
    [
        dcc.Store(id="stored-bar-click"),
        dcc.Store(id="stored-monthly-click"),
        dcc.Store(id="stored-top-sharks-click"),
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
        Output("monthly-incidents-bar", "figure"),
        Output("top-sharks-bar", "figure"),
        Output("stored-bar-click", "data"),
        Output("stored-monthly-click", "data"),
        Output("stored-top-sharks-click", "data"),
        Output("stored-line-relayout", "data"),
    ],
    [
        Input("dropdown-states", "value"),
        Input("checkbox-items", "value"),
        Input("radio-together-separate", "value"),
        Input("victim-injury-bar", "clickData"),
        Input("monthly-incidents-bar", "clickData"),
        Input("top-sharks-bar", "clickData"),
        Input("incident-trend", "relayoutData"),
        Input("reset-button", "n_clicks"),
        # Input("reset-filters-button", "n_clicks"),
    ],
    [
        State("stored-bar-click", "data"),
        State("stored-monthly-click", "data"),
        State("stored-top-sharks-click", "data"),
        State("stored-line-relayout", "data"),
    ],
)
def update_graphs(
    selected_states,
    checkbox_values,
    radio_value,
    bar_click,
    monthly_click,
    top_sharks_click,
    trend_relayout,
    reset_click,
    stored_bar_click,
    stored_monthly_click,
    stored_top_sharks_click,
    stored_line_relayout,
):
    ctx_id = ctx.triggered_id
    if ctx_id == "reset-button":
        filtered_data = filter_data_by_states(df, selected_states)

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
            title="Incidents Over Time",
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            yaxis_title="Number of Incidents",
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
            title="Injury Type",
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
        )

        monthly_counts = (
            filtered_data.groupby("incident_month")
            .size()
            .reset_index(name="count")
        )

        monthly_bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=monthly_counts["incident_month"],
                    y=monthly_counts["count"],
                    marker_color="#26a69a",
                )
            ]
        )

        monthly_bar_fig.update_layout(
            title="Monthly Incidents",
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            yaxis_title="Number of Incidents",
        )

        shark_counts = (
            filtered_data["shark_common_name"].value_counts().reset_index()
        )
        shark_counts.columns = ["shark_common_name", "count"]

        top_7_sharks = shark_counts.head(7)
        others = shark_counts.iloc[7:]
        num_others = others["shark_common_name"].nunique()
        others_count = others["count"].sum()
        others_row = {
            "shark_common_name": f"others: {num_others} types",
            "count": others_count,
        }
        top_7_sharks = pd.concat(
            [top_7_sharks, pd.DataFrame([others_row])], ignore_index=True
        )
        others_text = "<br>".join(
            [
                f"{row['shark_common_name']}: {row['count']} incidents"
                for _, row in others.iterrows()
            ]
        )
        # hover_text = [
        #     (
        #         f"{row['shark_common_name']}: {row['count']} incidents"
        #         if row["shark_common_name"] != f"others: {num_others} types"
        #         else others_text
        #     )
        #     for _, row in top_7_sharks.iterrows()
        # ]
        top_7_sharks.loc[
            top_7_sharks["shark_common_name"] == f"others: {num_others} types",
            "hover_text",
        ] = others_text

        top_7_sharks["hover_text"] = top_7_sharks["hover_text"].fillna(
            top_7_sharks["shark_common_name"]
            + ": "
            + top_7_sharks["count"].astype(str)
            + " incidents"
        )

        top_sharks_fig = go.Figure()

        top_sharks_fig.add_trace(
            go.Bar(
                x=top_7_sharks["shark_common_name"],
                y=top_7_sharks["count"],
                marker=dict(color="#26a69a"),
            )
        )

        top_sharks_fig.update_layout(
            title="Most Dangerous Sharks",
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            # xaxis_title="Shark Type",
            # yaxis_title="Number of Incidents",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            showlegend=False,
            transition={"duration": 800, "easing": "sin-in-out"},
        )
        # Ensure six return values
        return (
            line_fig,
            bar_fig,
            monthly_bar_fig,
            top_sharks_fig,
            None,
            None,
            None,
            None,
        )

    # Handle other inputs and retain stored states
    bar_click = (
        bar_click if ctx_id == "victim-injury-bar" else stored_bar_click
    )
    trend_relayout = (
        trend_relayout if ctx_id == "incident-trend" else stored_line_relayout
    )
    monthly_click = (
        monthly_click
        if ctx_id == "monthly-incidents-bar"
        else stored_monthly_click
    )
    top_sharks_click = (
        top_sharks_click
        if ctx_id == "top-sharks-bar"
        else stored_top_sharks_click
    )

    filtered_data = filter_data_by_states(df, selected_states)

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
    if monthly_click and "points" in monthly_click:
        selected_injury = monthly_click["points"][0]["x"]
        filtered_data = filtered_data[
            filtered_data["incident_month"] == selected_injury
        ]
    if top_sharks_click and "points" in top_sharks_click:
        selected_shark = top_sharks_click["points"][0]["x"]
        filtered_data = filtered_data[
            filtered_data["shark_common_name"] == selected_shark
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
            title="Incidents Over Time",
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            yaxis_title="Number of Incidents",
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
            title="Incidents Over Time",
            legend=dict(
                orientation="h",
                x=0.5,
                y=-0.1,
                xanchor="center",
                yanchor="top",
                font=dict(size=12, color="#26a69a"),
            ),
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            yaxis_title="Number of Incidents",
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
            title="Injury Type",
            font=dict(color="#26a69a", size=13),
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
            title="Injury Type",
            legend=dict(
                orientation="h",
                x=0.5,
                y=-0.1,
                xanchor="center",
                yanchor="top",
                font=dict(size=12, color="#26a69a"),
            ),
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            margin=dict(t=20, b=100),
            transition={"duration": 800, "easing": "sin-in-out"},
        )

    monthly_counts = (
        filtered_data.groupby("incident_month")
        .size()
        .reset_index(name="count")
    )

    if radio_value == "together":
        monthly_bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=monthly_counts["incident_month"],
                    y=monthly_counts["count"],
                    marker_color="#42a5f5",
                )
            ]
        )
        monthly_bar_fig.update_traces(marker_color="#26a69a")
        monthly_bar_fig.update_layout(
            title="Monthly Incidents",
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            yaxis_title="Number of Incidents",
            transition={"duration": 800, "easing": "sin-in-out"},
        )
    else:
        provoked_counts = (
            filtered_data[filtered_data["provoked_unprovoked"] == "provoked"][
                "incident_month"
            ]
            .value_counts()
            .reset_index()
        )
        unprovoked_counts = (
            filtered_data[
                filtered_data["provoked_unprovoked"] == "unprovoked"
            ]["incident_month"]
            .value_counts()
            .reset_index()
        )
        provoked_counts.columns = ["incident_month", "provoked_count"]
        unprovoked_counts.columns = ["incident_month", "unprovoked_count"]

        combined_counts = pd.merge(
            provoked_counts,
            unprovoked_counts,
            on="incident_month",
            how="outer",
        ).fillna(0)

        monthly_bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=combined_counts["incident_month"],
                    y=combined_counts["provoked_count"],
                    name="Provoked",
                    marker_color="#26a69a",
                ),
                go.Bar(
                    x=combined_counts["incident_month"],
                    y=combined_counts["unprovoked_count"],
                    name="Unprovoked",
                    marker_color="#ab47bc",
                ),
            ]
        )
        monthly_bar_fig.update_layout(
            title="Monthly Incidents",
            legend=dict(
                orientation="h",
                x=0.5,
                y=-0.1,
                xanchor="center",
                yanchor="top",
                font=dict(size=12, color="#26a69a"),
            ),
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            # margin=dict(t=20, b=100),
            yaxis_title="Number of Incidents",
            transition={"duration": 800, "easing": "sin-in-out"},
        )

    shark_counts = (
        filtered_data["shark_common_name"].value_counts().reset_index()
    )
    shark_counts.columns = ["shark_common_name", "count"]

    top_7_sharks = shark_counts.head(7)
    others = shark_counts.iloc[7:]
    num_others = others["shark_common_name"].nunique()
    others_count = others["count"].sum()
    others_row = {
        "shark_common_name": f"others: {num_others} types",
        "count": others_count,
    }
    top_7_sharks = pd.concat(
        [top_7_sharks, pd.DataFrame([others_row])], ignore_index=True
    )
    others_text = "<br>".join(
        [
            f"{row['shark_common_name']}: {row['count']} incidents"
            for _, row in others.iterrows()
        ]
    )
    # hover_text = [
    #     (
    #         f"{row['shark_common_name']}: {row['count']} incidents"
    #         if row["shark_common_name"] != f"others: {num_others} types"
    #         else others_text
    #     )
    #     for _, row in top_7_sharks.iterrows()
    # ]
    top_7_sharks.loc[
        top_7_sharks["shark_common_name"] == f"others: {num_others} types",
        "hover_text",
    ] = others_text

    top_7_sharks["hover_text"] = top_7_sharks["hover_text"].fillna(
        top_7_sharks["shark_common_name"]
        + ": "
        + top_7_sharks["count"].astype(str)
        + " incidents"
    )
    if radio_value == "together":

        top_sharks_fig = go.Figure()

        top_sharks_fig.add_trace(
            go.Bar(
                x=top_7_sharks["shark_common_name"],
                y=top_7_sharks["count"],
                marker=dict(color="#26a69a"),
            )
        )

        top_sharks_fig.update_layout(
            title="Most Dangerous Sharks",
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            # xaxis_title="Shark Type",
            # yaxis_title="Number of Incidents",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            showlegend=False,
            transition={"duration": 800, "easing": "sin-in-out"},
        )
    else:
        provoked_sharks = (
            provoked_data["shark_common_name"].value_counts().reset_index()
        )
        unprovoked_sharks = (
            unprovoked_data["shark_common_name"].value_counts().reset_index()
        )
        provoked_sharks.columns = ["shark_common_name", "provoked_count"]
        unprovoked_sharks.columns = ["shark_common_name", "unprovoked_count"]

        combined_sharks = pd.merge(
            provoked_sharks,
            unprovoked_sharks,
            on="shark_common_name",
            how="outer",
        ).fillna(0)

        combined_sharks = combined_sharks.sort_values(
            by=["provoked_count", "unprovoked_count"], ascending=False
        ).head(7)

        combined_sharks.loc[len(combined_sharks)] = {
            "shark_common_name": "Others",
            "provoked_count": provoked_sharks["provoked_count"].iloc[7:].sum(),
            "unprovoked_count": unprovoked_sharks["unprovoked_count"]
            .iloc[7:]
            .sum(),
        }

        top_sharks_fig = go.Figure(
            data=[
                go.Bar(
                    x=combined_sharks["shark_common_name"],
                    y=combined_sharks["provoked_count"],
                    name="Provoked",
                    marker_color="#26a69a",
                ),
                go.Bar(
                    x=combined_sharks["shark_common_name"],
                    y=combined_sharks["unprovoked_count"],
                    name="Unprovoked",
                    marker_color="#ab47bc",
                ),
            ]
        )

        top_sharks_fig.update_layout(
            # barmode="stack",
            title="Most Dangerous Sharks by Incident Type",
            font=dict(color="#26a69a", size=13),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            # xaxis_title="Shark Type",
            # yaxis_title="Number of Incidents",
            legend=dict(
                orientation="h",
                x=0.5,
                y=-0.1,
                xanchor="center",
                yanchor="top",
                font=dict(size=12),
            ),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            transition={"duration": 800, "easing": "sin-in-out"},
        )

    return (
        line_fig,
        bar_fig,
        monthly_bar_fig,
        top_sharks_fig,
        bar_click,
        monthly_click,
        top_sharks_click,
        trend_relayout,
    )


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
