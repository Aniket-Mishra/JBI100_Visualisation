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


dangerous_sharks = df["Shark.common.name"].value_counts().reset_index()
dangerous_sharks.columns = ["Shark Species", "Incident Count"]
x = st.slider("Select number of top dangerous sharks to display", 5, 20, 10)
top_dangerous_sharks = dangerous_sharks.head(x)

fig_top_sharks = px.bar(
    top_dangerous_sharks,
    x="Shark Species",
    y="Incident Count",
    title=f"Top {x} Most Dangerous Sharks",
    labels={"Incident Count": "Number of Incidents", "Shark Species": "Shark Species"},
)

fig_severity = px.pie(
    df,
    names="Injury.severity",
    title="Distribution of Attack Severities",
    hole=0.4,  # Donut chart
    labels={"Injury.severity": "Severity", "count": "Count"},
)

attacks_by_year = df.groupby("Incident.year").size().reset_index(name="Count")

# Plot
fig_attacks_year = px.line(
    attacks_by_year,
    x="Incident.year",
    y="Count",
    title="Shark Attacks Over Time",
    labels={"Incident.year": "Year", "Count": "Number of Incidents"},
)


activities = df["Victim.activity"].value_counts().reset_index()
activities.columns = ["Activity", "Count"]

# Plot
fig_activities = px.bar(
    activities.head(10),  # Top 10 activities
    x="Activity",
    y="Count",
    title="Most Common Victim Activities",
    labels={"Activity": "Activity", "Count": "Number of Incidents"},
)


fatal_incidents = df[df["Injury.severity"].str.contains("fatal", na=False, case=False)]

# Plot
fig_fatal_map = px.scatter_geo(
    fatal_incidents,
    lat="Latitude",
    lon="Longitude",
    title="Geographic Distribution of Fatal Incidents",
    color="State",
    hover_name="Location",
    labels={"State": "State", "Latitude": "Latitude", "Longitude": "Longitude"},
    projection="natural earth",
)

fig_shark_length = px.histogram(
    df.dropna(subset=["Shark.length.m"]),
    x="Shark.length.m",
    nbins=20,
    title="Distribution of Shark Lengths",
    labels={"Shark.length.m": "Shark Length (m)"},
)

fig_gender = px.pie(
    df,
    names="Victim.gender",
    title="Victim Gender Distribution",
    labels={"Victim.gender": "Gender"},
    hole=0.4,
)

fig_age = px.histogram(
    df.dropna(subset=["Victim.age"]),
    x="Victim.age",
    nbins=15,
    title="Victim Age Distribution",
    labels={"Victim.age": "Age"},
)

fig_temp = px.histogram(
    df.dropna(subset=["Water.temperature.°C"]),
    x="Water.temperature.°C",
    nbins=20,
    title="Distribution of Water Temperatures During Incidents",
    labels={"Water.temperature.°C": "Temperature (°C)"},
)

fig_time = px.histogram(
    df.dropna(subset=["Time.of.incident"]),
    x="Time.of.incident",
    nbins=24,
    title="Time of Shark Incidents",
    labels={"Time.of.incident": "Time of Incident"},
)


locations = df["Location"].value_counts().reset_index()
locations.columns = ["Location", "Count"]

# Plot
fig_locations = px.bar(
    locations.head(10),  # Top 10 locations
    x="Location",
    y="Count",
    title="Top Locations for Shark Incidents",
    labels={"Location": "Location", "Count": "Number of Incidents"},
)


injury_locations = (
    filtered_data["Injury.location"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "Body Part", "Injury.location": "Count"})
)

fig_injury_location = px.bar(
    injury_locations,
    x="Body Part",
    y="Count",
    title="Most Common Injury Locations",
    labels={"Body Part": "Injury Location", "Count": "Number of Incidents"},
)

# Count by shark behavior
shark_behavior = (
    filtered_data["Shark.behaviour"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "Shark Behavior", "Shark.behaviour": "Count"})
)

fig_shark_behavior = px.bar(
    shark_behavior,
    x="Shark Behavior",
    y="Count",
    title="Shark Behavior During Incidents",
    labels={"Shark Behavior": "Behavior", "Count": "Number of Incidents"},
)

filtered_data["Depth.of.incident.m"] = pd.to_numeric(
    filtered_data["Depth.of.incident.m"], errors="coerce"
)

fig_depth = px.histogram(
    filtered_data.dropna(subset=["Depth.of.incident.m"]),
    x="Depth.of.incident.m",
    nbins=15,
    title="Shark Attacks by Depth",
    labels={"Depth.of.incident.m": "Depth of Incident (m)"},
)

filtered_data["Water.visability.m"] = pd.to_numeric(
    filtered_data["Water.visability.m"], errors="coerce"
)

fig_visibility = px.histogram(
    filtered_data.dropna(subset=["Water.visability.m"]),
    x="Water.visability.m",
    nbins=15,
    title="Shark Attacks by Water Visibility",
    labels={"Water.visability.m": "Water Visibility (m)"},
)


fatal_vs_nonfatal = (
    filtered_data["Injury.severity"]
    .apply(lambda x: "Fatal" if "fatal" in str(x).lower() else "Non-Fatal")
    .value_counts()
    .reset_index()
    .rename(columns={"index": "Outcome", "Injury.severity": "Count"})
)

fig_fatal_vs_nonfatal = px.pie(
    fatal_vs_nonfatal,
    names="Outcome",
    values="Count",
    title="Fatal vs Non-Fatal Incidents",
    hole=0.4,
)

victim_awareness = (
    filtered_data["Victim.aware.of.shark"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "Awareness", "Victim.aware.of.shark": "Count"})
)

fig_victim_awareness = px.pie(
    victim_awareness,
    names="Awareness",
    values="Count",
    title="Victim Awareness of Shark Presence",
    hole=0.4,
)


fig_time_of_day = px.histogram(
    filtered_data.dropna(subset=["Time.of.incident"]),
    x="Time.of.incident",
    nbins=24,
    title="Shark Incidents by Time of Day",
    labels={"Time.of.incident": "Time of Incident"},
)


# if graph_choice == "Shark Attacks Over Time":
#     st.plotly_chart(fig1)
# elif graph_choice == "Attack Severity by Site Category":
#     st.plotly_chart(fig2)
# elif graph_choice == "Geographic Distribution":
#     st.plotly_chart(fig3)
# elif graph_choice == "Victim Activity and Provocation":
#     st.plotly_chart(fig4)
# elif graph_choice == "Shark Species Involved":
#     st.plotly_chart(fig5)


viz_options = [
    "Shark Attacks Over Time",
    "Attack Severity by Site Category",
    "Geographic Distribution",
    "Victim Activity and Provocation",
    "Shark Species Involved",
    "Top Dangerous Sharks",
    "Attack Severity Distribution",
    "Victim Activities",
    "Fatal Incidents Map",
    "Shark Length Distribution",
    "Victim Gender Distribution",
    "Victim Age Distribution",
    "Water Temperature Distribution",
    "Top Locations",
    "Most Common Injury Locations",
    "Shark Behavior During Incidents",
    "Shark Attacks by Depth",
    "Shark Attacks by Water Visibility",
    "Fatal vs Non-Fatal Incidents",
    "Victim Awareness of Shark Presence",
    "Shark Incidents by Time of Day",
]

graph_choice = st.sidebar.selectbox(
    "Select a Graph to Display",
    options=viz_options,
)


# viz_choice = st.selectbox("Select a Visualization", options=viz_options)

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
elif graph_choice == "Top Dangerous Sharks":
    st.plotly_chart(fig_top_sharks, key="top_sharks")
elif graph_choice == "Attack Severity Distribution":
    st.plotly_chart(fig_severity, key="severity_distribution")
elif graph_choice == "Shark Attacks Over Time":
    st.plotly_chart(fig1, key="fig1")
elif graph_choice == "Victim Activities":
    st.plotly_chart(fig4, key="fig4")
elif graph_choice == "Fatal Incidents Map":
    st.plotly_chart(fig_fatal_map, key="fatal_map")
elif graph_choice == "Shark Length Distribution":
    st.plotly_chart(fig_shark_length, key="shark_length_distribution")
elif graph_choice == "Victim Gender Distribution":
    st.plotly_chart(fig_gender, key="gender_distribution")
elif graph_choice == "Victim Age Distribution":
    st.plotly_chart(fig7, key="victim_age_distribution")
elif graph_choice == "Water Temperature Distribution":
    st.plotly_chart(fig_temp, key="water_temperature_distribution")
elif graph_choice == "Top Locations":
    st.plotly_chart(fig_locations, key="top_locations")
elif graph_choice == "Most Common Injury Locations":
    st.plotly_chart(fig_injury_location, key="fig_injury_location")
elif graph_choice == "Shark Behavior During Incidents":
    st.plotly_chart(fig_shark_behavior, key="fig_shark_behavior")
elif graph_choice == "Shark Attacks by Depth":
    st.plotly_chart(fig_depth, key="fig_depth")
elif graph_choice == "Shark Attacks by Water Visibility":
    st.plotly_chart(fig_visibility, key="fig_visibility")
elif graph_choice == "Fatal vs Non-Fatal Incidents":
    st.plotly_chart(fig_fatal_vs_nonfatal, key="fig_fatal_vs_nonfatal")
elif graph_choice == "Victim Awareness of Shark Presence":
    st.plotly_chart(fig_victim_awareness, key="fig_victim_awareness")
elif graph_choice == "Shark Incidents by Time of Day":
    st.plotly_chart(fig_time_of_day, key="fig_time_of_day")
