import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

import plotly.graph_objects as go

import chart_studio.plotly as py
import cufflinks as cf
import seaborn as sns
import plotly.express as px

cf.go_offline()

import datapane as dp

import streamlit as st

df = pd.read_excel(
    "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/JBI100_Data_2024_2025/Australian_Shark_Incidents/Australian Shark-Incident Database Public Version.xlsx",
    sheet_name="ASID",
)

st.title("Interactive Shark Attack Data Explorer")
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

graph_choice = st.sidebar.selectbox(
    "Select a Graph to Display",
    options=[
        "Shark Attacks Over Time",
        "Attack Severity by Site Category",
        "Geographic Distribution",
        "Victim Activity and Provocation",
        "Shark Species Involved",
    ],
)

if graph_choice == "Shark Attacks Over Time":
    st.plotly_chart(fig1)
elif graph_choice == "Attack Severity by Site Category":
    st.plotly_chart(fig2)
elif graph_choice == "Geographic Distribution":
    st.plotly_chart(fig3)
elif graph_choice == "Victim Activity and Provocation":
    st.plotly_chart(fig4)
elif graph_choice == "Shark Species Involved":
    st.plotly_chart(fig5)
