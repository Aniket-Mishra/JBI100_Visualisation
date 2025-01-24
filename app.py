import pandas as pd

from dash import Dash, dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from common_functions import *


def main():
    # Path to data, local
    data_path = "data/new_cleaned_updated_data.csv"

    df = prepare_data(data_path)
    df_all_columns = list(df.columns)
    # print(df_all_columns)

    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.FONT_AWESOME],
        suppress_callback_exceptions=True,
    )

    # Dropdown for state names
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

    # HTML Div for checkbox
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

    # Button component group
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

    # Header - Initially for multipage app
    header_div = html.Div(
        "Australian Shark Incidents Analysis",
        style={
            "fontSize": "32px",
            "color": "#ffd600",
            "textAlign": "center",
            "padding": "10px",
            # "background-color": "#fff",
        },
    )

    # Main layout - Initially shared layout between multiple pages
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
                        html.Div(className="grid-item", children=header_div),
                        html.Div(
                            className="grid-item", children=reset_buttons
                        ),
                        html.Div(className="grid-item"),
                    ],
                ),
                content_div,
            ],
            fluid=True,
        )

    # Graph component - Spans 90% of view (to give space for header)
    def general_content():
        return html.Div(
            style={
                "height": "calc(90vh)",
            },
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="incident-trend",
                                style={"width": "100", "height": "100"},
                            ),
                            width=6,
                            style={"height": "45vh"},
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="victim-injury-bar",
                                style={
                                    "width": "100",
                                    "height": "100",
                                },
                            ),
                            width=3,
                            style={"height": "45vh"},
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="site-category-bar",
                                style={
                                    "width": "100",
                                    "height": "100",
                                },
                            ),
                            width=3,
                            style={"height": "45vh"},
                        ),
                    ],
                    className="h-50",
                    style={"height": "50%", "width": "100%"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="monthly-incidents-bar",
                                style={"width": "100", "height": "100"},
                            ),
                            width=4,
                            style={"height": "45vh"},
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="injury-severity-bar",
                                style={"width": "100", "height": "100"},
                            ),
                            width=4,
                            style={"height": "45vh"},
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="top-sharks-bar",
                                style={"width": "100", "height": "100%"},
                            ),
                            width=4,
                            style={"height": "45vh"},
                        ),
                    ],
                    className="h-50",
                    style={"height": "50%"},
                ),
            ],
        )

    # App layout, click info and page content. Location as I wanted a multi page app initially
    app.layout = html.Div(
        [
            dcc.Store(id="stored-bar-click"),
            dcc.Store(id="stored-site-category-click"),
            dcc.Store(id="stored-injury-severity-click"),
            dcc.Store(id="stored-monthly-click"),
            dcc.Store(id="stored-top-sharks-click"),
            dcc.Store(id="stored-line-relayout"),
            dcc.Location(id="url", refresh=False),
            html.Div(id="page-content"),
        ]
    )

    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def display_page(pathname):
        return shared_layout(general_content())

    # Callback - I did it one step at a time, did not have enough time to do multiple functions for each.
    # I apologize for the huge functions.
    @app.callback(
        [
            Output("incident-trend", "figure"),
            Output("victim-injury-bar", "figure"),
            Output("site-category-bar", "figure"),
            Output("injury-severity-bar", "figure"),
            Output("monthly-incidents-bar", "figure"),
            Output("top-sharks-bar", "figure"),
            Output("stored-bar-click", "data"),
            Output("stored-monthly-click", "data"),
            Output("stored-site-category-click", "data"),
            Output("stored-injury-severity-click", "data"),
            Output("stored-top-sharks-click", "data"),
            Output("stored-line-relayout", "data"),
        ],
        [
            Input("dropdown-states", "value"),
            Input("checkbox-items", "value"),
            Input("radio-together-separate", "value"),
            Input("victim-injury-bar", "clickData"),
            Input("site-category-bar", "clickData"),
            Input("injury-severity-bar", "clickData"),
            Input("monthly-incidents-bar", "clickData"),
            Input("top-sharks-bar", "clickData"),
            Input("incident-trend", "relayoutData"),
            Input("reset-button", "n_clicks"),
            # Input("reset-filters-button", "n_clicks"),
        ],
        [
            State("stored-bar-click", "data"),
            State("stored-site-category-click", "data"),
            State("stored-injury-severity-click", "data"),
            State("stored-monthly-click", "data"),
            State("stored-top-sharks-click", "data"),
            State("stored-line-relayout", "data"),
        ],
    )
    # Funciton that runs on callback. Updates the graphs.
    def update_graphs(
        selected_states,
        checkbox_values,
        radio_value,
        bar_click,
        site_category_click,
        injury_severity_click,
        monthly_click,
        top_sharks_click,
        trend_relayout,
        reset_click,
        stored_bar_click,
        stored_site_category_click,
        stored_injury_severity_click,
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

                filtered_data = filter_data_single_column_single_value(
                    filtered_data, "provoked_unprovoked", "provoked"
                )

            elif (
                "unprovoked" in checkbox_values
                and "provoked" not in checkbox_values
            ):

                filtered_data = filter_data_single_column_single_value(
                    filtered_data, "provoked_unprovoked", "unprovoked"
                )
            elif (
                "provoked" not in checkbox_values
                and "unprovoked" not in checkbox_values
            ):

                filtered_data = pd.DataFrame(columns=df_all_columns)
            else:
                filtered_data = filter_data_by_states(df, selected_states)

            aggregated_data = groupby_count(
                filtered_data, "incident_year", "count"
            )
            line_fig = get_single_line_plot(
                aggregated_data,
                "incident_year",
                "count",
                "Incidents Over Time",
            )

            injury_counts = get_reset_value_counts(
                filtered_data, "victim_injury"
            )

            bar_fig = get_bar_fig(
                injury_counts, "victim_injury", "count", "Injury Type", None
            )

            site_category_counts = get_reset_value_counts(
                filtered_data, "site_category_cleaned"
            )

            site_category_bar_fig = get_bar_fig(
                site_category_counts,
                "site_category_cleaned",
                "count",
                "Site Category",
                None,
            )

            injury_severity_counts = get_reset_value_counts(
                filtered_data, "injury_severity"
            )
            injury_severity_bar_fig = get_bar_fig(
                injury_severity_counts,
                "injury_severity",
                "count",
                "Injury Severity",
                None,
            )
            # fn for this just swapped months around, too lz to fix
            monthly_counts = (
                filtered_data.groupby("incident_month")
                .size()
                .reset_index(name="count")
            )
            # monthly_counts = map_months_for_graphs(monthly_counts)
            monthly_bar_fig = get_bar_fig(
                monthly_counts,
                "incident_month",
                "count",
                "Monthly Incidents",
                "Number of Incidents",
            )

            # These changes are made here but could be moved to a function
            # Its different thatn regular bar graph functions
            # Because I am adding number of tupes in the end
            # Like 18 shark types in others, for example.
            # Had logic for hover text. I had an old function
            # That showed the values, got lost somewhere.
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
            hover_text = [
                (
                    f"{row['shark_common_name']}: {row['count']} incidents"
                    if row["shark_common_name"]
                    != f"others: {num_others} types"
                    else others_text
                )
                for _, row in top_7_sharks.iterrows()
            ]
            top_7_sharks.loc[
                top_7_sharks["shark_common_name"]
                == f"others: {num_others} types",
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
                legend=dict(
                    orientation="h",
                    x=0.5,
                    y=1.15,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=12, color="#ffd600"),
                ),
                font=dict(color="#ffd600", size=12),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                # xaxis_title="Shark Type",
                # yaxis_title="Number of Incidents",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False),
                showlegend=False,
                transition={"duration": 800, "easing": "sin-in-out"},
            )
            # No clicks, so None
            return (
                line_fig,
                bar_fig,
                site_category_bar_fig,
                injury_severity_bar_fig,
                monthly_bar_fig,
                top_sharks_fig,
                None,
                None,
                None,
                None,
                None,
                None,
            )
        # All code to change when click/drag action is made
        bar_click = (
            bar_click if ctx_id == "victim-injury-bar" else stored_bar_click
        )
        stored_bar_click = (
            bar_click if ctx_id == "victim-injury-bar" else stored_bar_click
        )

        site_category_click = (
            site_category_click
            if ctx_id == "site-category-bar"
            else stored_site_category_click
        )
        stored_site_category_click = (
            site_category_click
            if ctx_id == "site-category-bar"
            else stored_site_category_click
        )

        injury_severity_click = (
            injury_severity_click
            if ctx_id == "injury-severity-bar"
            else stored_injury_severity_click
        )
        stored_injury_severity_click = (
            injury_severity_click
            if ctx_id == "injury-severity-bar"
            else stored_injury_severity_click
        )

        trend_relayout = (
            trend_relayout
            if ctx_id == "incident-trend"
            else stored_line_relayout
        )
        stored_line_relayout = (
            trend_relayout
            if ctx_id == "incident-trend"
            else stored_line_relayout
        )

        monthly_click = (
            monthly_click
            if ctx_id == "monthly-incidents-bar"
            else stored_monthly_click
        )
        stored_monthly_click = (
            monthly_click
            if ctx_id == "monthly-incidents-bar"
            else stored_monthly_click
            # else None
        )

        top_sharks_click = (
            top_sharks_click
            if ctx_id == "top-sharks-bar"
            else stored_top_sharks_click
        )
        stored_top_sharks_click = (
            top_sharks_click
            if ctx_id == "top-sharks-bar"
            else stored_top_sharks_click
        )

        filtered_data = filter_data_by_states(df, selected_states)

        if (
            "provoked" in checkbox_values
            and "unprovoked" not in checkbox_values
        ):
            filtered_data = filter_data_single_column_single_value(
                filtered_data, "provoked_unprovoked", "provoked"
            )
        elif (
            "unprovoked" in checkbox_values
            and "provoked" not in checkbox_values
        ):
            filtered_data = filter_data_single_column_single_value(
                filtered_data, "provoked_unprovoked", "unprovoked"
            )
        elif (
            "provoked" not in checkbox_values
            and "unprovoked" not in checkbox_values
        ):
            filtered_data = pd.DataFrame(columns=df_all_columns)
        else:
            filtered_data = filter_data_by_states(df, selected_states)

        # All commented code below is becasue:
        # Bug - clicks caused df to become empty over time
        # Recommended by the TA (forgot his name, he was awesome)
        # To make changes at the end.
        if bar_click and "points" in bar_click:
            selected_injury = [bar_click["points"][0]["x"]]
            if selected_injury not in df["victim_injury"].unique():
                selected_injury = list(df["victim_injury"].unique())

            # filtered_data = filter_data_by_states(df, selected_states)
            # filtered_data = filter_data_single_column_single_value(
            #     filtered_data, "victim_injury", selected_injury
            # )
        else:
            selected_injury = list(df["victim_injury"].unique())
        if site_category_click and "points" in site_category_click:
            site_category = [site_category_click["points"][0]["x"]]
            if site_category not in df["site_category_cleaned"].unique():
                site_category = list(df["site_category_cleaned"].unique())
            # filtered_data = filter_data_by_states(df, selected_states)

            # filtered_data = filter_data_single_column_single_value(
            #     filtered_data, "site_category_cleaned", site_category
            # )
        else:
            site_category = list(df["site_category_cleaned"].unique())
        if injury_severity_click and "points" in injury_severity_click:
            injury_severity = [injury_severity_click["points"][0]["x"]]
            if injury_severity not in df["injury_severity"].unique():
                injury_severity = list(df["injury_severity"].unique())
            # filtered_data = filter_data_by_states(df, selected_states)

            # filtered_data = filter_data_single_column_single_value(
            #     filtered_data, "injury_severity", injury_severity
            # )
        else:
            injury_severity = list(df["injury_severity"].unique())

        # The below could also be a function.
        if monthly_click and "points" in monthly_click:
            valid_months = set(
                [str(i) for i in range(1, 13)]
                + [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ]
            )

            x_value = monthly_click["points"][0].get("x")
            month_name_to_number = {
                "Jan": 1,
                "Feb": 2,
                "Mar": 3,
                "Apr": 4,
                "May": 5,
                "Jun": 6,
                "Jul": 7,
                "Aug": 8,
                "Sep": 9,
                "Oct": 10,
                "Nov": 11,
                "Dec": 12,
            }

            if x_value in month_name_to_number:
                x_value = month_name_to_number[x_value]
            if str(x_value) in valid_months:
                monthly_incidents = [x_value]
            else:
                monthly_click = None
                monthly_incidents = list(df["incident_month"].unique())
        else:
            monthly_click = None
            monthly_incidents = list(df["incident_month"].unique())

        if top_sharks_click and "points" in top_sharks_click:
            selected_shark = [top_sharks_click["points"][0]["x"]]
            if selected_shark not in df["shark_common_name"].unique():
                selected_shark = list(df["shark_common_name"].unique())
            # filtered_data = filter_data_by_states(df, selected_states)

            # filtered_data = filter_data_single_column_single_value(
            #     filtered_data, "shark_common_name", selected_shark
            # )
        else:
            selected_shark = list(df["shark_common_name"].unique())
        if (
            trend_relayout
            and "xaxis.range[0]" in trend_relayout
            and "xaxis.range[1]" in trend_relayout
        ):
            start_year = int(float(trend_relayout["xaxis.range[0]"]))
            end_year = int(float(trend_relayout["xaxis.range[1]"]))
            if start_year not in df["incident_year"].unique():
                start_year = df["incident_year"].min()
            if end_year not in df["incident_year"].unique():
                end_year = df["incident_year"].max()
            # filtered_data = filter_data_by_states(df, selected_states)

            # filtered_data = filtered_data[
            #     (filtered_data["incident_year"] >= start_year)
            #     & (filtered_data["incident_year"] <= end_year)
            # ]
        else:
            start_year = df["incident_year"].min()
            end_year = df["incident_year"].max()

        # This is here for debugging purposes. Can comment out if needed.
        # print(f"{stored_line_relayout=}")
        # print(f"{stored_bar_click=}")
        # print(f"{stored_top_sharks_click=}")
        # print(f"{stored_monthly_click=}")
        # print(f"{stored_injury_severity_click=}")
        # print(f"{stored_site_category_click=}")
        # print(f"{trend_relayout=}")
        # print(f"{bar_click=}")
        # print(f"{top_sharks_click=}")
        # print(f"{monthly_click=}")
        # print(f"{injury_severity_click=}")
        # print(f"{site_category_click=}")

        # print(monthly_incidents)

        # Do this in graph functions
        # filtered_data = map_months_for_graphs(filtered_data)
        filtered_data = filtered_data.loc[
            (filtered_data["incident_year"] >= start_year)
            & (filtered_data["incident_year"] <= end_year)
            & (filtered_data["victim_injury"].isin(selected_injury))
            & (filtered_data["site_category_cleaned"].isin(site_category))
            & (filtered_data["shark_common_name"].isin(selected_shark))
            & (filtered_data["incident_month"].isin(monthly_incidents))
            & (filtered_data["injury_severity"].isin(injury_severity))
        ]

        print(df.shape)
        print(filtered_data.shape)
        print("\n\n")
        # filtered_data = map_months_for_graphs(filtered_data)

        aggregated_data = groupby_count(
            filtered_data, "incident_year", "count"
        )

        if radio_value == "together":
            line_fig = get_single_line_plot(
                aggregated_data,
                "incident_year",
                "count",
                "Incidents Over Time",
            )

        else:
            provoked_data = filter_data_single_column_single_value(
                filtered_data, "provoked_unprovoked", "provoked"
            )
            unprovoked_data = filter_data_single_column_single_value(
                filtered_data, "provoked_unprovoked", "unprovoked"
            )

            provoked_agg = groupby_count(
                provoked_data, "incident_year", "provoked_count"
            )

            unprovoked_agg = groupby_count(
                unprovoked_data, "incident_year", "unprovoked_count"
            )

            line_fig = get_double_line_fig(
                df_first_agg=provoked_agg,
                df_second_agg=unprovoked_agg,
                xname="incident_year",
                y1name="provoked_count",
                y2name="unprovoked_count",
                g1_name="Provoked Incidents",
                g2_name="Unprovoked Incidents",
                title="Incidents Over Time",
                yaxis_title="Number of Incidents",
            )

        injury_counts = get_reset_value_counts(filtered_data, "victim_injury")

        if radio_value == "together":
            bar_fig = get_bar_fig(
                injury_counts, "victim_injury", "count", "Injury Type", None
            )

        else:

            provoked_counts = get_reset_value_counts(
                filter_data_single_column_single_value(
                    filtered_data, "provoked_unprovoked", "provoked"
                ),
                "victim_injury",
            )
            unprovoked_counts = get_reset_value_counts(
                filter_data_single_column_single_value(
                    filtered_data, "provoked_unprovoked", "unprovoked"
                ),
                "victim_injury",
            )

            provoked_counts.columns = ["victim_injury", "provoked_count"]
            unprovoked_counts.columns = ["victim_injury", "unprovoked_count"]

            combined_counts = pd.merge(
                provoked_counts,
                unprovoked_counts,
                on="victim_injury",
                how="outer",
            ).fillna(0)

            bar_fig = get_double_bar_fig(
                combined_counts,
                xname="victim_injury",
                y1name="provoked_count",
                y2name="unprovoked_count",
                g1_name="Provoked",
                g2_name="Unprovoked",
                title="Injury Type",
                yaxis_title=None,
            )

        site_category_counts = get_reset_value_counts(
            filtered_data, "site_category_cleaned"
        )

        if radio_value == "together":
            site_category_bar_fig = get_bar_fig(
                site_category_counts,
                "site_category_cleaned",
                "count",
                "Site Category",
                None,
            )

        else:
            provoked_counts = get_reset_value_counts(
                filter_data_single_column_single_value(
                    filtered_data, "provoked_unprovoked", "provoked"
                ),
                "site_category_cleaned",
            )
            unprovoked_counts = get_reset_value_counts(
                filter_data_single_column_single_value(
                    filtered_data, "provoked_unprovoked", "unprovoked"
                ),
                "site_category_cleaned",
            )

            provoked_counts.columns = [
                "site_category_cleaned",
                "provoked_count",
            ]
            unprovoked_counts.columns = [
                "site_category_cleaned",
                "unprovoked_count",
            ]

            combined_counts = pd.merge(
                provoked_counts,
                unprovoked_counts,
                on="site_category_cleaned",
                how="outer",
            ).fillna(0)

            site_category_bar_fig = get_double_bar_fig(
                combined_counts,
                xname="site_category_cleaned",
                y1name="provoked_count",
                y2name="unprovoked_count",
                g1_name="Provoked",
                g2_name="Unprovoked",
                title="Site Category",
                yaxis_title=None,
            )

        injury_severity_counts = get_reset_value_counts(
            filtered_data, "injury_severity"
        )

        if radio_value == "together":
            injury_severity_bar_fig = get_bar_fig(
                injury_severity_counts,
                "injury_severity",
                "count",
                "Injury Severity",
                None,
            )

        else:
            provoked_counts = get_reset_value_counts(
                filter_data_single_column_single_value(
                    filtered_data, "provoked_unprovoked", "provoked"
                ),
                "injury_severity",
            )
            unprovoked_counts = get_reset_value_counts(
                filter_data_single_column_single_value(
                    filtered_data, "provoked_unprovoked", "unprovoked"
                ),
                "injury_severity",
            )

            provoked_counts.columns = ["injury_severity", "provoked_count"]
            unprovoked_counts.columns = ["injury_severity", "unprovoked_count"]

            combined_counts = pd.merge(
                provoked_counts,
                unprovoked_counts,
                on="injury_severity",
                how="outer",
            ).fillna(0)

            injury_severity_bar_fig = get_double_bar_fig(
                combined_counts,
                xname="injury_severity",
                y1name="provoked_count",
                y2name="unprovoked_count",
                g1_name="Provoked",
                g2_name="Unprovoked",
                title="Injury Severity",
                yaxis_title=None,
            )

        monthly_counts = (
            filtered_data.groupby("incident_month")
            .size()
            .reset_index(name="count")
        )
        # monthly_counts = map_months_for_graphs(monthly_counts)

        if radio_value == "together":
            # monthly_counts = map_months_for_graphs(combined_counts)
            monthly_bar_fig = get_bar_fig(
                monthly_counts,
                "incident_month",
                "count",
                "Monthly Incidents",
                "Number of Incidents",
            )
        else:
            provoked_counts = get_reset_value_counts(
                filter_data_single_column_single_value(
                    filtered_data, "provoked_unprovoked", "provoked"
                ),
                "incident_month",
            )
            unprovoked_counts = get_reset_value_counts(
                filter_data_single_column_single_value(
                    filtered_data, "provoked_unprovoked", "unprovoked"
                ),
                "incident_month",
            )

            provoked_counts.columns = ["incident_month", "provoked_count"]
            unprovoked_counts.columns = ["incident_month", "unprovoked_count"]

            combined_counts = pd.merge(
                provoked_counts,
                unprovoked_counts,
                on="incident_month",
                how="outer",
            ).fillna(0)
            # combined_counts = map_months_for_graphs(combined_counts)
            monthly_bar_fig = get_double_bar_fig(
                combined_counts,
                xname="incident_month",
                y1name="provoked_count",
                y2name="unprovoked_count",
                g1_name="Provoked",
                g2_name="Unprovoked",
                title="Monthly Incidents",
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
                legend=dict(
                    orientation="h",
                    x=0.5,
                    y=1.15,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=12, color="#ffd600"),
                ),
                font=dict(color="#ffd600", size=12),
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
                unprovoked_data["shark_common_name"]
                .value_counts()
                .reset_index()
            )
            provoked_sharks.columns = ["shark_common_name", "provoked_count"]
            unprovoked_sharks.columns = [
                "shark_common_name",
                "unprovoked_count",
            ]

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
                "provoked_count": provoked_sharks["provoked_count"]
                .iloc[7:]
                .sum(),
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
                title="Most Dangerous Sharks",
                legend=dict(
                    orientation="h",
                    x=0.5,
                    y=1.15,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=12, color="#ffd600"),
                ),
                font=dict(color="#ffd600", size=12),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                # xaxis_title="Shark Type",
                # yaxis_title="Number of Incidents",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False),
                transition={"duration": 800, "easing": "sin-in-out"},
            )

        # selected_states,
        # checkbox_values,
        # radio_value,
        # bar_click,
        # site_category_click,
        # injury_severity_click,
        # monthly_click,
        # top_sharks_click,
        # trend_relayout,
        # reset_click,
        # stored_bar_click,
        # stored_site_category_click,
        # stored_injury_severity_click,
        # stored_monthly_click,
        # stored_top_sharks_click,
        # stored_line_relayout,
        return (
            line_fig,
            bar_fig,
            site_category_bar_fig,
            injury_severity_bar_fig,
            monthly_bar_fig,
            top_sharks_fig,
            trend_relayout,
            bar_click,
            site_category_click,
            injury_severity_click,
            monthly_click,
            top_sharks_click,
        )

    # Reset callbacks
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

    app.run_server(port=8080, debug=False)


if __name__ == "__main__":
    main()
