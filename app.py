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


# st.title("Interactive Shark Attack Data Explorer")
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

fig1 = px.line(
    filtered_data.groupby("Incident.year").size().reset_index(name="Count"),
    x="Incident.year",
    y="Count",
    title="Shark Attacks Over Time",
    labels={"Incident.year": "Year", "Count": "Number of Incidents"},
)
# st.plotly_chart(fig1, key="fig1")


fig2 = px.histogram(
    filtered_data,
    x="Site.category",
    color="Injury.severity",
    title="Attack Severity by Site Category",
    labels={"Site.category": "Site Category", "Injury.severity": "Severity"},
)
# st.plotly_chart(fig2, key="fig2")


print(filtered_data["Shark.length.m"].isnull().sum())
print(filtered_data["Shark.length.m"].unique())

filtered_data["Shark.length.m"] = pd.to_numeric(
    filtered_data["Shark.length.m"], errors="coerce"
)

filtered_data["Shark.length.m"] = filtered_data["Shark.length.m"].fillna(1)


fig3 = px.scatter_geo(
    filtered_data,
    lat="Latitude",
    lon="Longitude",
    color="Injury.severity",
    size="Shark.length.m",
    title="Geographic Distribution of Shark Attacks",
    labels={"Latitude": "Latitude", "Longitude": "Longitude"},
    projection="natural earth",
    width=800,  # Set the width of the figure
    height=600,  # Set the height of the figure
)

# fig3.show()

fig4 = px.bar(
    filtered_data,
    x="Victim.activity",
    color="Provoked/unprovoked",
    title="Victim Activities and Provocation",
    labels={"Victim.activity": "Activity", "Provoked/unprovoked": "Provocation Type"},
)
# st.plotly_chart(fig4, key="fig4")

fig5 = px.bar(
    filtered_data,
    x="Shark.common.name",
    color="Injury.severity",
    title="Shark Species Involved in Incidents",
    labels={"Shark.common.name": "Shark Species", "Injury.severity": "Severity"},
)
# st.plotly_chart(fig5, key="fig5")

fig_severity = px.pie(
    filtered_data,
    names="Injury.severity",
    title="Severity of Shark Attacks",
    hole=0.4,  # Donut chart
    labels={"Injury.severity": "Severity"},
    color_discrete_sequence=px.colors.sequential.RdBu,  # Colorblind-friendly palette
)

fig_severity.add_annotation(
    text="Fatal cases make up 15%",
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(size=14, color="red"),
    align="center",
)

graph_choice = st.sidebar.selectbox(
    "Select a Graph to Display",
    options=[
        "Shark Attacks Over Time",
        "Attack Severity by Site Category",
        "Geographic Distribution",
        "Victim Activity and Provocation",
        "Shark Species Involved",
        "Injury Severity",
    ],
)

if graph_choice == "Shark Attacks Over Time":
    st.plotly_chart(fig1, use_container_width=True)
elif graph_choice == "Attack Severity by Site Category":
    st.plotly_chart(fig2, use_container_width=True)
elif graph_choice == "Geographic Distribution":
    st.plotly_chart(fig3, use_container_width=True)
elif graph_choice == "Victim Activity and Provocation":
    st.plotly_chart(fig4, use_container_width=True)
elif graph_choice == "Shark Species Involved":
    st.plotly_chart(fig5, use_container_width=True)
elif graph_choice == "Injury Severity":
    st.plotly_chart(fig_severity, use_container_width=True)
