import pandas as pd
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# Load data
data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"
df = pd.read_csv(data_path)
df = df.loc[df["provoked_unprovoked"] != "unknown"]

# Map integers (1–12) to month names
month_mapping = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}
df["incident_month_name"] = df["incident_month"].map(month_mapping)


# Layout for the "Monthly Information" page
def layout():
    return dbc.Container(
        [
            html.Div(
                style={"height": "calc(85vh - 120px)", "padding": "1.5%"},
                children=[
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="monthly-incident-row-chart",
                                    style={"width": "100%", "height": "100%"},
                                ),
                                width=6,
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id="monthly-site-category-stacked-bar",
                                    style={"width": "100%", "height": "100%"},
                                ),
                                width=6,
                            ),
                        ],
                        className="h-100",
                    )
                ],
            ),
        ],
        fluid=True,
    )


# Register callbacks
def register_callbacks(app):
    @app.callback(
        [
            Output("monthly-incident-row-chart", "figure"),
            Output("monthly-site-category-stacked-bar", "figure"),
        ],
        Input("url", "pathname"),
    )
    def update_monthly_graphs(pathname):
        if pathname != "/monthly":
            return {}, {}

        # Graph 1: Number of Incidents per Month as a Row Chart
        monthly_counts = (
            df["incident_month_name"]
            .value_counts()
            .reindex(
                [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ],
                fill_value=0,
            )
        )
        row_chart_fig = px.bar(
            x=monthly_counts.values,
            y=monthly_counts.index,
            orientation="h",
            labels={"x": "Number of Incidents", "y": "Month"},
            title="Number of Incidents per Month",
        )
        row_chart_fig.update_layout(
            yaxis=dict(
                categoryorder="array",
                categoryarray=list(month_mapping.values()),
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#26a69a"),
        )

        # Graph 2: Stacked Bar Chart for Incident Site Categories by Month
        site_category_counts = (
            df.groupby(["incident_month_name", "site_category_cleaned"])
            .size()
            .reset_index(name="count")
            .dropna()
        )
        stacked_bar_fig = px.bar(
            site_category_counts,
            x="incident_month_name",
            y="count",
            color="site_category_cleaned",
            labels={
                "incident_month_name": "Month",
                "count": "Number of Incidents",
                "site_category_cleaned": "Site Category",
            },
            title="Incident Site Categories by Month",
        )
        stacked_bar_fig.update_layout(
            xaxis=dict(
                categoryorder="array",
                categoryarray=list(month_mapping.values()),
            ),
            barmode="stack",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#26a69a"),
        )

        return row_chart_fig, stacked_bar_fig
