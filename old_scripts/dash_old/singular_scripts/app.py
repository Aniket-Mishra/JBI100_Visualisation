import dash
from dash import dcc, html, Input, Output, Patch, clientside_callback, callback
import pandas as pd
from graph_functions import *
import dash_bootstrap_components as dbc
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template


def main():
    data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"
    df = pd.read_csv(data_path)

    # app = dash.Dash()
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.GRID, dbc.icons.FONT_AWESOME],
    )

    app.title = "Shark Incidents Dashboard"

    incidents_over_time_fig = get_incidents_over_time(df)
    incidents_over_time_fig.update_layout(
        xaxis={"rangeslider": {"visible": True}, "title": "Year"},
        yaxis={"title": "Number of Incidents"},
    )

    categorical_col = "victim_injury"
    victim_injury_counts_fig = create_bar_chart(df, categorical_col)

    # Create top sharks chart
    top_sharks_fig = create_top_sharks_chart(df)

    app.css.config.serve_locally = True
    # Define layout
    app.layout = html.Div(
        style={
            # "position": "fixed",
            "backgroundColor": "#121212",
            "margin": 0,
            "padding": 0,
            "minHeight": "100vh",  # Make it cover the viewport height
            "width": "100%",
            "z-index": 1000,
            "text": "#f5f5f5",
            "color": "#f5f5f5",
        },
        children=[
            dbc.Container(
                html.Div(
                    [
                        html.H1(
                            "Shark Incidents Dashboard",
                            style={
                                "textAlign": "center",
                                "marginBottom": "25px",
                                "marginTop": 0,
                                "marginRight": 0,
                                "marginLeft": 0,
                                "paddingTop": "20px",
                                "paddingLeft": "5px",
                                "paddingRight": "5px",
                                "paddingBottom": "5px",
                                "color": "#f5f5f5",
                            },
                        ),
                        dcc.Graph(
                            id="incidents-over-time",
                            figure=incidents_over_time_fig,
                        ),
                    ],
                    style={
                        "width": "92%",
                        "height": "30%",
                    },
                ),
                html.Div(
                    [
                        # html.Div(
                        #     [
                        #         dcc.Graph(
                        #             id="victim-injury-counts",
                        #             figure=victim_injury_counts_fig,
                        #         )
                        #     ],
                        #     style={
                        #         "width": "30%",
                        #         "display": "inline-block",
                        #         "height": "30%",
                        #     },
                        # ),
                        # html.Div(
                        #     [
                        dcc.Graph(id="top-sharks-chart", figure=top_sharks_fig)
                        #     ],
                        #     style={
                        #         "width": "68%",
                        #         "display": "inline-block",
                        #         "height": "30%",
                        #     },
                        # ),
                    ],
                    style={
                        "width": "92%",
                        "height": "30%",
                        # "padding": "5%",
                        # "margin": "2%",
                    },
                ),
            ),
        ],
    )

    # Run app
    app.run_server(debug=False)


if __name__ == "__main__":
    main()
