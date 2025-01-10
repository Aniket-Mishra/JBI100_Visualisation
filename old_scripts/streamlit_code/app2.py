import pandas as pd
from dateutil.relativedelta import relativedelta

import plotly.express as px
import plotly.graph_objects as go

import cufflinks as cf
import plotly.io as pio

cf.go_offline()

import streamlit as st
from streamlit_plotly_events import plotly_events
from graph_functions import *

px.defaults.width = 875
px.defaults.height = 650

pio.templates["custom"] = go.layout.Template(
    layout=go.Layout(width=800, height=600)
)

pio.templates.default = "custom"


# @st.cache_data
# def load_data():
#     data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"
#     return pd.read_csv(data_path)
# df = load_data()


data_path = "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/filtered_cleaned_shark_data.csv"
df = pd.read_csv(data_path)
df["month_year"] = pd.to_datetime(df["month_year"])

# Set page configuration
st.set_page_config(
    page_title="Shark Incident Visualizations",
    page_icon="/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/images/shark_smile.png",
    layout="wide",
)

if "selected_years" not in st.session_state:
    st.session_state["selected_years"] = None
if "selected_injury" not in st.session_state:
    st.session_state["selected_injury"] = None


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
        "Trends Over Time and Injury",
        "Test",
        "Monthly Trends",
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

elif graph_choice == "Test":
    st.sidebar.subheader("Test")
    fig = go.Figure(
        data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3], mode="markers")]
    )

    # Display the figure and capture click events
    selected_points = plotly_events(fig, click_event=True)

    # Update the chart based on the selected points
    if selected_points:
        # Get the x and y coordinates of the selected point
        current_x = selected_points[0]["x"]
        current_y = selected_points[0]["y"]

        # Update the chart to highlight the selected point
        fig.update_layout(
            annotations=[
                dict(
                    x=current_x,
                    y=current_y,
                    xref="x",
                    yref="y",
                    text="Selected point",
                    showarrow=True,
                    arrowhead=7,
                    ax=0,
                    ay=-20,
                )
            ]
        )

        # Display the updated chart
        st.plotly_chart(fig, use_container_width=True)

elif graph_choice == "Trends Over Time and Injury":
    st.sidebar.subheader("Trends Over Time and Injury Options")

    line_data = (
        filtered_data.groupby("incident_year").size().reset_index(name="count")
    )
    bar_data = filtered_data["victim_injury"].value_counts().reset_index()
    bar_data.columns = ["victim_injury", "count"]

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Incidents by Year", "Victim Injury Distribution"),
        shared_yaxes=True,
    )

    # Add line chart
    line_trace = go.Scatter(
        x=line_data["incident_year"],
        y=line_data["count"],
        mode="lines",
        name="Incidents",
    )
    fig.add_trace(line_trace, row=1, col=1)

    # Add bar chart
    bar_trace = go.Bar(
        x=bar_data["victim_injury"], y=bar_data["count"], name="Injuries"
    )
    fig.add_trace(bar_trace, row=1, col=2)

    # Update layout
    fig.update_layout(
        height=600,
        width=1000,
        title_text="Shark Incident Analysis",
        dragmode="select",
    )
    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_xaxes(title_text="Victim Injury", row=1, col=2)
    fig.update_yaxes(title_text="Number of Incidents", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)

    # Add range slider to line chart
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(
                        count=10, label="10y", step="year", stepmode="backward"
                    ),
                    dict(
                        count=50, label="50y", step="year", stepmode="backward"
                    ),
                    dict(
                        count=100,
                        label="100y",
                        step="year",
                        stepmode="backward",
                    ),
                    dict(step="all"),
                ]
            )
        ),
        row=1,
        col=1,
    )

    # Create a Streamlit container for the chart
    chart_container = st.empty()

    # Function to update bar chart based on selected range in line chart
    def update_bar_chart(trace, points, selector):
        if len(points.xs) == 2:
            start_year, end_year = points.xs
            filtered_df = df[
                (df["incident_year"] >= start_year)
                & (df["incident_year"] <= end_year)
            ]
            updated_bar_data = (
                filtered_df["victim_injury"].value_counts().reset_index()
            )
            updated_bar_data.columns = ["victim_injury", "count"]
            with fig.batch_update():
                fig.data[1].x = updated_bar_data["victim_injury"]
                fig.data[1].y = updated_bar_data["count"]
        chart_container.plotly_chart(fig, use_container_width=True)

    # Function to update line chart based on clicked bar in bar chart
    def update_line_chart(trace, points, selector):
        if points.point_inds:
            selected_injury = bar_data.iloc[points.point_inds[0]][
                "victim_injury"
            ]
            filtered_df = df[df["victim_injury"] == selected_injury]
            updated_line_data = (
                filtered_df.groupby("incident_year")
                .size()
                .reset_index(name="count")
            )
            with fig.batch_update():
                fig.data[0].x = updated_line_data["incident_year"]
                fig.data[0].y = updated_line_data["count"]
        chart_container.plotly_chart(fig, use_container_width=True)

    # Set up callbacks
    fig.data[0].on_selection(update_bar_chart)
    fig.data[1].on_click(update_line_chart)

    # Display the initial chart
    chart_container.plotly_chart(fig, use_container_width=True)

    # Add instructions for user interaction
    st.write(
        "Select a range on the line chart to update the bar chart. Click on a bar to update the line chart."
    )
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
