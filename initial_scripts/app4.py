import os, sys
import shutil
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

import plotly.graph_objects as go

import chart_studio.plotly as py
import cufflinks as cf
import seaborn as sns
import plotly.express as px
import plotly.io as pio

cf.go_offline()

import streamlit as st

px.defaults.width = 875
px.defaults.height = 650

pio.templates["custom"] = go.layout.Template(
    layout=go.Layout(width=800, height=600)
)

pio.templates.default = "custom"


df = pd.read_excel(
    "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/JBI100_Data_2024_2025/Australian_Shark_Incidents/Australian Shark-Incident Database Public Version.xlsx",
    sheet_name="ASID",
)

st.set_page_config(
    page_title="Shark Incident Visualizations",
    page_icon="/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/images/shark_smile.png",
    layout="wide",
)


st.title("Interactive Shark Attack Data Explorer")
st.sidebar.title("Filter Options")

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Incident.year"].min()),
    int(df["Incident.year"].max()),
    (1900, 2000),
)

filtered_data = df[
    (df["Incident.year"] >= year_range[0])
    & (df["Incident.year"] <= year_range[1])
]

state_filter = st.sidebar.multiselect(
    "Select State(s)",
    options=df["State"].unique(),
    default=df["State"].unique(),
)
filtered_data = filtered_data[filtered_data["State"].isin(state_filter)]

fig1 = px.line(
    filtered_data.groupby("Incident.year").size().reset_index(name="Count"),
    x="Incident.year",
    y="Count",
    title="Shark Attacks Over Time",
    labels={"Incident.year": "Year", "Count": "Number of Incidents"},
)

fig1.update_traces(line_color="#00796b")

# Remove grid lines and background
fig1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
)


graph_choice = st.sidebar.selectbox(
    "Select a Graph to Display",
    options=[
        "Shark Attacks Over Time",
    ],
)

if graph_choice == "Shark Attacks Over Time":
    # line_color_choice = st.selectbox(
    #     "Change Line Colour:",
    #     options=["Default (Teal)", "Blue", "Green"],
    #     index=0,
    # )

    # color_mapping = {
    #     "Default (Teal)": "#00796b",
    #     "Blue": "#0000FF",
    #     "Green": "#008000",
    # }

    # selected_color = color_mapping[line_color_choice]
    # fig1.update_traces(line_color=selected_color)
    st.plotly_chart(fig1, use_container_width=True)
