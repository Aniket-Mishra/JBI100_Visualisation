import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from graph_functions import *


def main():

    # Load data
    data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"
    df = pd.read_csv(data_path)

    # Create Dash app
    app = dash.Dash(__name__)
    app.title = "Shark Incidents Dashboard"

    # Generate initial figures
    incidents_over_time_fig = get_incidents_over_time(df)
    categorical_col = "victim_injury"
    victim_injury_counts_fig = create_bar_chart(df, categorical_col)

    # Define layout
    app.layout = html.Div(
        [
            html.H1(
                "Shark Incidents Dashboard", style={"textAlign": "center"}
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="incidents-over-time",
                        figure=incidents_over_time_fig,
                        className="six columns",
                    ),
                    dcc.Graph(
                        id="victim-injury-counts",
                        figure=victim_injury_counts_fig,
                        className="six columns",
                    ),
                ],
            ),
            # html.Div(
            #     [
            #         dcc.Graph(
            #             id="victim-injury-counts",
            #             figure=victim_injury_counts_fig,
            #             className="four columns",
            #         )
            #     ],
            #     style={"margin": "20px 0"},
            # ),
        ]
    )

    # Callbacks for interactivity
    @app.callback(
        Output("victim-injury-counts", "figure"),
        Input("incidents-over-time", "selectedData"),
    )
    def update_bar_chart(selected_data):
        if selected_data and "points" in selected_data:
            selected_years = [point["x"] for point in selected_data["points"]]
            filtered_df = df[df["incident_year"].isin(selected_years)]
        else:
            filtered_df = df

        return create_bar_chart(filtered_df, categorical_col)

    @app.callback(
        Output("incidents-over-time", "figure"),
        Input("victim-injury-counts", "clickData"),
    )
    def update_line_chart(click_data):
        if click_data and "points" in click_data:
            selected_category = click_data["points"][0]["x"]
            filtered_df = df[df[categorical_col] == selected_category]
        else:
            filtered_df = df

        return get_incidents_over_time(filtered_df)

    # Run app
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
