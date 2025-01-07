import pandas as pd
from dateutil.relativedelta import relativedelta

import plotly.express as px
import plotly.graph_objects as go

import plotly.io as pio


import streamlit as st

from streamlit_plotly_events import plotly_events
from graph_functions import *

px.defaults.width = 875
px.defaults.height = 650

pio.templates["custom"] = go.layout.Template(
    layout=go.Layout(width=800, height=600)
)

pio.templates.default = "custom"


@st.cache_data
def load_data():
    data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"
    return pd.read_csv(data_path)


def render_preview_ui(df: pd.DataFrame):
    with st.expander("Preview"):
        st.dataframe(df)


def render_plotly_ui(df: pd.DataFrame):
    incidents_over_time_fig = get_incidents_over_time(df)

    categorical_col = "victim_injury"
    victim_injur_counts_fig = create_bar_chart(df, categorical_col)
    # victim_injur_counts_fig.update_layout(
    #     margin=dict(l=25, r=25, t=25, b=25),
    #     # width=500,
    #     # height=500,
    # )

    categorical_col = "provoked_unprovoked"
    provoked_unprovoked_counts_fig = create_bar_chart(df, categorical_col)
    # provoked_unprovoked_counts_fig.update_layout(
    #     margin=dict(l=25, r=25, t=25, b=25),
    #     # width=600,
    #     # height=400,
    # )
    c1, c2 = st.columns([2, 1])
    with c1:
        incidents_over_time_fig_selected = plotly_events(
            incidents_over_time_fig, select_event=True
        )
        # st.plotly_chart(incidents_over_time_fig)
    with c2:
        # victim_injur_counts_fig_clicked = plotly_events(
        #     victim_injur_counts_fig, click_event=True
        # )
        # st.plotly_chart(victim_injur_counts_fig)
        # st.plotly_chart(provoked_unprovoked_counts_fig)
        provoked_unprovoked_counts_fig_clicked = plotly_events(
            provoked_unprovoked_counts_fig, click_event=True
        )
    # st.write(incidents_over_time_fig_selected)
    # st.write(victim_injur_counts_fig_clicked)


def main():

    st.set_page_config(
        page_title="Shark Incident Visualizations",
        page_icon="/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/images/shark_smile.png",
        layout="wide",
    )
    df = load_data()
    st.title("Interactive Shark Attack Data Explorer")
    render_preview_ui(df)
    render_plotly_ui(df)
    # injury_over_time_counts = plot_injury_type_counts(df)
    # st.plotly_chart(injury_over_time_counts)

    # categorical_col = "provoked_unprovoked"
    # time_col = "incident_year"
    # provoked_unprovoked_over_time_fig = line_chart_on_category(
    #     df, categorical_col, time_col
    # )

    # attack_severity_fig = create_attack_severity_chart(df)
    # st.plotly_chart(attack_severity_fig)
    # # st.sidebar.header("Filter Options")

    # monthly_data, month_names = prepare_incident_data(df)
    # multi_monthly_injury_type = create_multi_bar_monthly_incident(
    #     monthly_data, month_names
    # )
    # st.plotly_chart(multi_monthly_injury_type)
    # year_range = st.sidebar.slider(
    #     "Select Year Range",
    #     int(df["incident_year"].min()),
    #     int(df["incident_year"].max()),
    #     (1900, 2000),
    # )
    # filtered_data = df[
    #     (df["incident_year"] >= year_range[0])
    #     & (df["incident_year"] <= year_range[1])
    # ]

    # with st.expander("Preview"):
    #     st.dataframe(filtered_data)


if __name__ == "__main__":
    main()
