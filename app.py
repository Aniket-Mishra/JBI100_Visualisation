import pandas as pd
from dateutil.relativedelta import relativedelta

import plotly.express as px
import plotly.graph_objects as go

import cufflinks as cf
import plotly.io as pio

cf.go_offline()

import streamlit as st

from graph_functions import *

px.defaults.width = 875
px.defaults.height = 650

pio.templates["custom"] = go.layout.Template(
    layout=go.Layout(width=800, height=600)
)

pio.templates.default = "custom"

data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"
df = pd.read_csv(data_path)
df["month_year"] = pd.to_datetime(df["month_year"])

# Set page configuration
st.set_page_config(
    page_title="Shark Incident Visualizations",
    page_icon="/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/images/shark_smile.png",
    layout="wide",
)

st.title("Interactive Shark Attack Data Explorer")
st.sidebar.title("Filter Options")

min_year = int(df["incident_year"].min())
max_year = int(df["incident_year"].max())

start_year, end_year = st.sidebar.slider(
    "Select Date Range",
    min_value=min_year,
    max_value=max_year,
    value=(1900, 2000),
)

filtered_data = df[
    (df["incident_year"] >= start_year) & (df["incident_year"] <= end_year)
]

state_filter = st.sidebar.multiselect(
    "Select State(s)",
    options=df["state_names"].unique(),
    default=df["state_names"].unique(),
)
filtered_data = filtered_data[filtered_data["state_names"].isin(state_filter)]


graph_choice = st.sidebar.selectbox(
    "Select a Graph to Display",
    options=[
        "Trends Over Time",
        "Monthly Trends",
        # "Most Dangerous Sharks",
        # "Shark Incidents by Injury Type",
        # "Victim Activities and Shark Attacks",
        "Shark Related Information",
        "Attack Severity by Site",
        "Custom Grouped Bar Charts",
    ],
)

if graph_choice == "Trends Over Time":
    st.sidebar.subheader("Trends Over Time Options")
    trend_option = st.sidebar.radio(
        "Select an option:",
        options=["All incidents over time", "Custom Filters"],
        index=0,
    )

    if trend_option == "All incidents over time":
        fig = get_incidents_over_time(filtered_data)
    else:
        category_col = st.sidebar.selectbox(
            "Select Category to Separate By:",
            options=[
                "provoked_unprovoked",
                "victim_injury",
                "site_category_cleaned",
                "victim_gender",
                "victim_activity",
            ],
        )

        custom_data = (
            filtered_data.groupby(["incident_year", category_col])
            .size()
            .reset_index(name="attack_count")
        )

        line_graph = go.Figure()
        unique_categories = custom_data[category_col].unique()
        color_map = px.colors.qualitative.Safe[: len(unique_categories)]

        for category, color in zip(unique_categories, color_map):
            filtered_category_data = custom_data[
                custom_data[category_col] == category
            ]
            line_graph.add_trace(
                go.Scatter(
                    x=filtered_category_data["incident_year"],
                    y=filtered_category_data["attack_count"],
                    mode="lines",
                    line=dict(color=color, width=2),
                    name=str(category).capitalize(),
                )
            )

        line_graph.update_layout(
            title=f"Shark Incidents Over Time by {category_col.replace('_', ' ').capitalize()}",
            xaxis_title="Year",
            yaxis_title="Number of Incidents",
            font=dict(color="#00796b", size=12),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            legend_title=category_col.replace("_", " ").capitalize(),
        )

        fig = line_graph

    st.plotly_chart(fig, use_container_width=True)


elif graph_choice == "Monthly Trends":
    separate_graphs = st.sidebar.radio(
        "Separate Graphs:", options=["True", "False"], index=1
    )

    if separate_graphs == "True":
        scale_y = st.sidebar.checkbox("Scale Y Axis", value=False)
        monthly_data, month_names = prepare_incident_data(filtered_data)
        fig = create_subplots_monthly_incident(
            monthly_data, month_names, scale_y=scale_y
        )
    else:
        monthly_data, month_names = prepare_incident_data(filtered_data)
        fig = create_multi_bar_monthly_incident(monthly_data, month_names)

    st.plotly_chart(fig, use_container_width=True)

elif graph_choice == "Shark Related Information":
    st.sidebar.subheader("Shark Related Options")
    shark_option = st.sidebar.radio(
        "Select an option:",
        options=[
            "Most Dangerous Sharks",
            "Shark Incidents by Injury Type",
            "Victim Activities and Shark Attacks",
        ],
        index=0,
    )

    if shark_option == "Most Dangerous Sharks":
        fig = create_top_sharks_chart(filtered_data)
    elif shark_option == "Shark Incidents by Injury Type":
        fig = create_incident_by_shark_chart(filtered_data)
    elif shark_option == "Victim Activities and Shark Attacks":
        fig = compare_victim_activity_vs_provoked(filtered_data)

    st.plotly_chart(fig, use_container_width=True)
elif graph_choice == "Attack Severity by Site":
    fig = create_attack_severity_chart(filtered_data)
    st.plotly_chart(fig, use_container_width=True)
elif graph_choice == "Custom Grouped Bar Charts":
    x_col = st.sidebar.selectbox(
        "Select X-Axis Column:",
        options=[
            "shark_common_name",
            "site_category_cleaned",
            "victim_activity",
        ],
    )
    y_col = st.sidebar.selectbox(
        "Select Y-Axis Column:", options=["count"], index=0
    )
    color_col = st.sidebar.selectbox(
        "Select Color Grouping Column:",
        options=["victim_injury", "provoked_unprovoked", "injury_severity"],
    )
    title = st.sidebar.text_input("Chart Title:", "Custom Grouped Bar Chart")
    x_label = st.sidebar.text_input("X-Axis Label:", "X-Axis")
    y_label = st.sidebar.text_input("Y-Axis Label:", "Y-Axis")

    bar_chart_data = (
        filtered_data.groupby([x_col, color_col])
        .size()
        .reset_index(name="count")
    )

    fig = px.bar(
        bar_chart_data,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        labels={x_col: x_label, y_col: y_label, color_col: "Category"},
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )

    fig.update_layout(
        font=dict(color="#00796b", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )

    st.plotly_chart(fig, use_container_width=True)
