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

import datapane as dp

import streamlit as st

px.defaults.width = 875
px.defaults.height = 650

pio.templates["custom"] = go.layout.Template(layout=go.Layout(width=800, height=600))

# Set the default template to your custom template
pio.templates.default = "custom"

df = pd.read_excel(
    "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/JBI100_Data_2024_2025/Australian_Shark_Incidents/Australian Shark-Incident Database Public Version.xlsx",
    sheet_name="ASID",
)

st.set_page_config(
    page_title="Shark Incident Visualizations",
    layout="wide",
)

st.markdown(
    """
    <style>
    /* Dropdown container */
    div[data-baseweb="select"] {
        background-color: #3C3F58; /* Medium grey background */
        color: #EDF2F4; /* Light grey text */
        border-radius: 8px; /* Rounded corners */
        border: 1px solid #8D99AE; /* Grey-blue border */
    }

    /* Dropdown hover and selected options */
    div[data-baseweb="select"] > div {
        background-color: #3C3F58 !important; /* Match dropdown background */
        color: #EDF2F4 !important;
    }

    /* Dropdown list options */
    ul {
        background-color: #3C3F58 !important; /* Medium grey background for list */
        color: #8D99AE !important; /* Grey-blue text */
    }

    /* Hover effect for options */
    ul > li:hover {
        background-color: #EF233C !important; /* Vivid red highlight */
        color: #EDF2F4 !important; /* Light text */
    }

    /* Selected option styling */
    ul > li[aria-selected="true"] {
        background-color: #8D99AE !important; /* Grey-blue for selected */
        color: #EDF2F4 !important; /* White text for contrast */
    }
    .element-container {
        width: 95% !important;
        margin: auto;
    }
    div.block-container {
        max-width: 85%;
        padding: 50px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# # Page Setup
# st.set_page_config(
#     page_title="Shark Incident Visualizations",
#     layout="wide",
# )

# Sidebar Filters
st.sidebar.header("Filter Options")
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Incident.year"].min()),
    int(df["Incident.year"].max()),
    (1900, 2023),
)
filtered_data = df[
    (df["Incident.year"] >= year_range[0]) & (df["Incident.year"] <= year_range[1])
]

state_filter = st.sidebar.multiselect(
    "Select State(s)", options=df["State"].unique(), default=df["State"].unique()
)
filtered_data = filtered_data[filtered_data["State"].isin(state_filter)]

# Divide Layout into 4 Sections
col1, col2 = st.columns(2)
row1, row2 = st.columns(2)

# Section 1: Sharks (Top Left)
with col1:
    st.header("Shark-Related Data")
    # Shark Length Distribution
    fig_shark_length = px.histogram(
        filtered_data,
        x="Shark.length.m",
        nbins=15,
        title="Shark Length Distribution",
        labels={"Shark.length.m": "Shark Length (m)"},
        color_discrete_sequence=["#EF233C"],
    )
    st.plotly_chart(fig_shark_length, use_container_width=True)

    # Shark Species Bar Chart
    fig_shark_species = px.bar(
        filtered_data,
        x=filtered_data["Shark.common.name"].value_counts().index,
        y=filtered_data["Shark.common.name"].value_counts(),
        title="Most Common Shark Species Involved",
        labels={"x": "Shark Species", "y": "Incident Count"},
    )
    st.plotly_chart(fig_shark_species, use_container_width=True)

# Section 2: People (Bottom Left)
with row1:
    st.header("People-Related Data")
    # Injury Severity Bar Chart
    fig_injuries = px.bar(
        filtered_data,
        x="Injury.severity",
        color="Injury.severity",
        title="Injury Severity Distribution",
        labels={"Injury.severity": "Severity", "count": "Count"},
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    st.plotly_chart(fig_injuries, use_container_width=True)

    # Victim Activities
    fig_activities = px.bar(
        filtered_data,
        x=filtered_data["Victim.activity"].value_counts().index,
        y=filtered_data["Victim.activity"].value_counts(),
        title="Victim Activities Involved in Incidents",
        labels={"x": "Activity", "y": "Incident Count"},
    )
    st.plotly_chart(fig_activities, use_container_width=True)

# Section 3: Geography (Top Right)
with col2:
    st.header("Geographic Data")
    # Map Visualization
    fig_map = px.scatter_geo(
        filtered_data,
        lat="Latitude",
        lon="Longitude",
        color="Injury.severity",
        size="Shark.length.m",
        title="Geographic Distribution of Shark Attacks",
        labels={"Latitude": "Latitude", "Longitude": "Longitude"},
        projection="natural earth",
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Site Category by Count
    fig_site_category = px.histogram(
        filtered_data,
        x="Site.category",
        title="Incidents by Site Category",
        labels={"Site.category": "Site Category"},
        color_discrete_sequence=["#3C3F58"],
    )
    st.plotly_chart(fig_site_category, use_container_width=True)

# Section 4: Misc (Bottom Right)
with row2:
    st.header("Miscellaneous Insights")
    # Incidents Over Time
    fig_time = px.line(
        filtered_data.groupby("Incident.year").size().reset_index(name="Count"),
        x="Incident.year",
        y="Count",
        title="Shark Incidents Over Time",
        labels={"Incident.year": "Year", "Count": "Number of Incidents"},
        line_shape="spline",
        color_discrete_sequence=["#8D99AE"],
    )
    st.plotly_chart(fig_time, use_container_width=True)
