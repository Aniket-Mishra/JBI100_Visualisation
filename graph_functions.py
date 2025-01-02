# This is here cuz the streamlit app got too big
# I ain't gonna be the one debugging that
# I really wish my group helped with the code
# But I hate writing reports so I guess I'm okay with it.

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
import re


# Setup functions for common plot functions
def get_top_victim_activities(df, top_index) -> pd.DataFrame:
    local_df = df.copy()
    top_activities = (
        local_df["victim_activity"].value_counts().index[:top_index]
    )
    print(top_activities)
    local_df["victim_activity"] = local_df["victim_activity"].apply(
        lambda x: x if x in top_activities else "unknown"
    )
    local_df["victim_activity_updated"] = np.nan
    local_df["victim_activity_updated"] = local_df["victim_activity"].apply(
        lambda x: (x if x in top_activities else "other_activities")
    )
    return local_df


def prepare_incident_data(df):
    """
    Prepares the incident data grouped by month and victim injury.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing shark incident data.

    Returns:
        pd.DataFrame: DataFrame grouped by month and victim injury with counts.
    """
    incidents_per_month = (
        df.groupby(["incident_month", "victim_injury"])
        .size()
        .reset_index(name="count")
    )

    months = list(range(1, 13))  # 1 to 12 for all months
    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    incidents_per_month["month_name"] = incidents_per_month[
        "incident_month"
    ].map(dict(zip(months, month_names)))

    return incidents_per_month, month_names


# Incidents - Time graphs
# Header choice 1
# other graph choices below/above(easier to code) graph
def get_incidents_over_time(df: pd.DataFrame) -> go.Figure:
    incidents_over_time = (
        df.groupby("incident_year").size().reset_index(name="attack_count")
    )

    line_graph = go.Figure()

    line_graph.add_trace(
        go.Scatter(
            x=incidents_over_time["incident_year"],
            y=incidents_over_time["attack_count"],
            mode="lines",
            line=dict(color="#00796b", width=2),
            name="Shark Incidents",
        )
    )

    line_graph.update_layout(
        title="Shark Incidents Over Time (Years)",
        xaxis_title="Year",
        yaxis_title="Number of Incidents",
        font=dict(color="#00796b", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )

    return line_graph


def get_incidents_over_time_by_injury(df: pd.DataFrame) -> go.Figure:
    shark_attacks_by_injury = (
        df.groupby(["incident_year", "victim_injury"])
        .size()
        .reset_index(name="attack_count")
    )

    line_graph = go.Figure()

    injury_colors = {
        "fatal": "#8d6e63",
        "injured": "#5c6bc0",
        "uninjured": "#26a69a",
        "unknown": "#455a64",
    }

    for injury_type, color in injury_colors.items():
        filtered_data = shark_attacks_by_injury[
            shark_attacks_by_injury["victim_injury"] == injury_type
        ]
        line_graph.add_trace(
            go.Scatter(
                x=filtered_data["incident_year"],
                y=filtered_data["attack_count"],
                mode="lines",
                line=dict(color=color, width=2),
                name=injury_type.capitalize(),
            )
        )

    line_graph.update_layout(
        title="Shark Attacks Over Time by Type of Injury",
        xaxis_title="Year",
        yaxis_title="Number of Attacks",
        font=dict(color="#00796b", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        legend_title="Type of Injury",
    )

    return line_graph


def get_incidents_over_time_by_provoked(df: pd.DataFrame) -> go.Figure:
    """
    Generate a line graph showing shark attacks over time by provoked/unprovoked status.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing shark incident data.

    Returns:
        go.Figure: A Plotly figure object representing the line graph.
    """
    shark_attacks_by_provoked = (
        df.groupby(["incident_year", "provoked_unprovoked"])
        .size()
        .reset_index(name="attack_count")
    )

    line_graph = go.Figure()

    provoked_colors = {
        "provoked": "#8d6e63",
        "unprovoked": "#5c6bc0",
        "unknown": "#26a69a",
    }

    for provoked_type, color in provoked_colors.items():
        filtered_data = shark_attacks_by_provoked[
            shark_attacks_by_provoked["provoked_unprovoked"] == provoked_type
        ]
        line_graph.add_trace(
            go.Scatter(
                x=filtered_data["incident_year"],
                y=filtered_data["attack_count"],
                mode="lines",
                line=dict(color=color, width=2),
                name=provoked_type.capitalize(),
            )
        )

    line_graph.update_layout(
        title="Shark Attacks Over Time by Provoked/Unprovoked",
        xaxis_title="Year",
        yaxis_title="Number of Attacks",
        font=dict(color="#00796b", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        legend_title="Provoked/Unprovoked",
    )

    return line_graph


# Monthly graphs - sidebar choice 2
# Other graph choices above default graph


def create_subplots_monthly_incident(
    incidents_per_month, month_names, scale_y=False
):
    """
    Creates subplots for incidents per month by injury type.

    Parameters:
        incidents_per_month (pd.DataFrame): Grouped incident data.
        month_names (list): List of month names.
        scale_y (bool): Whether to scale the y-axis to a fixed range.

    Returns:
        go.Figure: The Plotly subplots figure.
    """
    injury_types = ["fatal", "injured", "uninjured", "unknown"]
    color_map = {
        "fatal": "#ab47bc",
        "injured": "#7e57c2",
        "uninjured": "#26a69a",
        "unknown": "#8d6e63",
    }

    bar_graph = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=[
            "Fatal Incidents",
            "Injured Incidents",
            "Uninjured Incidents",
            "Unknown Incidents",
        ],
        horizontal_spacing=0.1,
        vertical_spacing=0.25,
    )

    subplot_positions = {
        "fatal": (1, 1),
        "injured": (1, 2),
        "uninjured": (2, 1),
        "unknown": (2, 2),
    }

    for injury_type in injury_types:
        filtered_data = incidents_per_month[
            incidents_per_month["victim_injury"] == injury_type
        ]
        filtered_data = (
            filtered_data.set_index("month_name")
            .reindex(month_names, fill_value=0)
            .reset_index()
        )

        row, col = subplot_positions[injury_type]
        bar_graph.add_trace(
            go.Bar(
                x=filtered_data["month_name"],
                y=filtered_data["count"],
                name=injury_type.capitalize(),
                marker_color=color_map[injury_type],
            ),
            row=row,
            col=col,
        )

    bar_graph.update_layout(
        title="Shark Incidents Per Month by Injury Type",
        font=dict(color="#00796b", size=14),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=900,
        width=1000,
    )

    if scale_y:
        bar_graph.update_yaxes(range=[0, 150])

    bar_graph.update_xaxes(title_text="Month", tickangle=-45, row=1, col=1)
    bar_graph.update_xaxes(title_text="Month", tickangle=-45, row=1, col=2)
    bar_graph.update_xaxes(title_text="Month", tickangle=-45, row=2, col=1)
    bar_graph.update_xaxes(title_text="Month", tickangle=-45, row=2, col=2)

    bar_graph.update_yaxes(title_text="Number of Incidents", row=1, col=1)
    bar_graph.update_yaxes(title_text="Number of Incidents", row=2, col=1)

    return bar_graph


def create_multi_bar_monthly_incident(incidents_per_month, month_names):
    """
    Creates a multibar chart for incidents per month by injury type.

    Parameters:
        incidents_per_month (pd.DataFrame): Grouped incident data.
        month_names (list): List of month names.

    Returns:
        go.Figure: The Plotly multibar chart figure.
    """
    monthly_injury_data = (
        incidents_per_month.groupby(["month_name", "victim_injury"])["count"]
        .sum()
        .reset_index()
    )

    multi_bar_graph = px.bar(
        monthly_injury_data,
        x="month_name",
        y="count",
        color="victim_injury",
        barmode="group",
        color_discrete_map={
            "fatal": "#ab47bc",
            "injured": "#7e57c2",
            "uninjured": "#26a69a",
            "unknown": "#8d6e63",
        },
        title="Shark Incidents Per Month by Injury Type",
        labels={
            "month_name": "Month",
            "count": "Number of Incidents",
            "victim_injury": "Injury Type",
        },
        category_orders={"month_name": month_names},
    )

    multi_bar_graph.update_layout(
        font=dict(color="#00796b", size=14),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Month",
        yaxis_title="Number of Incidents",
        legend_title="Injury Type",
        height=700,
        width=1050,
    )

    return multi_bar_graph


# Shark Graphs
def create_top_sharks_chart(df) -> px.bar:
    """
    Creates a bar chart for the top 7 shark types and combines the remaining types into 'others'.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing shark data.

    Returns:
        px.bar: The Plotly bar chart figure.
    """
    shark_counts = df["shark_common_name"].value_counts().reset_index()
    shark_counts.columns = ["shark_common_name", "count"]

    top_5_sharks = shark_counts.head(7)
    others = shark_counts.iloc[7:]
    num_others = others["shark_common_name"].nunique()
    others_count = others["count"].sum()
    others_row = pd.DataFrame(
        [
            {
                "shark_common_name": f"others: {num_others} types",
                "count": others_count,
            }
        ]
    )
    top_5_sharks = pd.concat([top_5_sharks, others_row], ignore_index=True)

    others_text = "<br>".join(
        [
            f"{row['shark_common_name']}: {row['count']} incidents"
            for _, row in others.iterrows()
        ]
    )

    top_5_sharks.loc[
        top_5_sharks["shark_common_name"] == f"others: {num_others} types",
        "hover_text",
    ] = others_text

    top_5_sharks["hover_text"] = top_5_sharks["hover_text"].fillna(
        top_5_sharks["shark_common_name"]
        + ": "
        + top_5_sharks["count"].astype(str)
        + " incidents"
    )

    colors = [
        "#ab47bc",
        "#7e57c2",
        "#2e7d32",
        "#455a64",
        "#795548",
        "#303f9f",
        "#5e35b1",
        "#4e342e",
    ]

    bar_graph = px.bar(
        top_5_sharks,
        x="shark_common_name",
        y="count",
        title="Most Dangerous Sharks",
        labels={
            "shark_common_name": "Shark Type",
            "count": "Number of Incidents",
        },
        color="shark_common_name",
        color_discrete_sequence=colors,
        text="hover_text",
    )

    bar_graph.update_traces(
        hovertemplate="%{text}",
        textposition="none",
    )

    bar_graph.update_layout(
        font=dict(color="#00796b", size=14),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Shark Type",
        yaxis_title="Number of Incidents",
        showlegend=False,
    )

    return bar_graph


def get_shark_victim_injuries(df: pd.DataFrame) -> pd.DataFrame:
    shark_victim_injury_counts = (
        df.groupby(["shark_common_name", "victim_injury"])
        .size()
        .reset_index(name="count")
    )
    shark_victim_injury_counts["total_sum"] = 0
    unique_sharks = shark_victim_injury_counts["shark_common_name"].unique()

    for shark in unique_sharks:
        dfx = shark_victim_injury_counts.loc[
            shark_victim_injury_counts["shark_common_name"] == shark
        ]
        sum_incident = dfx["count"].sum()
        shark_victim_injury_counts.loc[
            shark_victim_injury_counts["shark_common_name"] == shark,
            "total_sum",
        ] = sum_incident

    shark_victim_injury_counts = shark_victim_injury_counts.sort_values(
        "total_sum", ascending=False
    )

    shark_victim_injury_counts_top = shark_victim_injury_counts.loc[
        shark_victim_injury_counts["shark_common_name"].isin(
            shark_victim_injury_counts["shark_common_name"].unique()[:7]
        )
    ]
    shark_victim_injury_counts_others = shark_victim_injury_counts.loc[
        ~shark_victim_injury_counts["shark_common_name"].isin(
            shark_victim_injury_counts["shark_common_name"].unique()[:7]
        )
    ]

    # others_fatal_count = shark_victim_injury_counts_others.loc[
    #     shark_victim_injury_counts_others["victim_injury"] == "fatal"
    # ]["count"].sum()
    others_injured_count = shark_victim_injury_counts_others.loc[
        shark_victim_injury_counts_others["victim_injury"] == "injured"
    ]["count"].sum()
    others_uninjured_count = shark_victim_injury_counts_others.loc[
        shark_victim_injury_counts_others["victim_injury"] == "uninjured"
    ]["count"].sum()
    others_unknown_count = shark_victim_injury_counts_others.loc[
        shark_victim_injury_counts_others["victim_injury"] == "unknown"
    ]["count"].sum()
    total_sum = shark_victim_injury_counts_others["count"].sum()

    num_others = shark_victim_injury_counts_others[
        "shark_common_name"
    ].nunique()

    shark_victim_injury_counts_others = pd.DataFrame(
        {
            "shark_common_name": [
                f"others: {num_others} types",
                f"others: {num_others} types",
                f"others: {num_others} types",
            ],
            "victim_injury": ["injured", "uninjured", "unknown"],
            "count": [
                others_injured_count,
                others_uninjured_count,
                others_unknown_count,
            ],
            "total_sum": [total_sum, total_sum, total_sum],
        }
    )

    shark_victim_injury_counts = pd.concat(
        [shark_victim_injury_counts_top, shark_victim_injury_counts_others]
    ).reset_index(drop=True)

    shark_victim_injury_counts["total_sum_text"] = shark_victim_injury_counts[
        "total_sum"
    ].astype(str)

    return shark_victim_injury_counts


def create_incident_by_shark_chart(df):
    """
    Creates a bar chart showing shark incidents by type of injury, grouping less common sharks into 'others'.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing shark data.

    Returns:
        px.bar: The Plotly bar chart figure.
    """
    shark_victim_injury_counts = get_shark_victim_injuries(df)
    bar_graph = px.bar(
        shark_victim_injury_counts,
        x="shark_common_name",
        y="count",
        color="victim_injury",
        title="Shark Incidents by Type of Injury",
        labels={
            "shark_common_name": "Shark Type",
            "count": "Number of Incidents",
            "victim_injury": "Type of Injury",
        },
        barmode="group",
        color_discrete_sequence=["#ab47bc", "#7e57c2", "#26a69a", "#8d6e63"],
    )

    bar_graph.update_traces(textposition="none")
    bar_graph.update_layout(
        font=dict(color="#00796b", size=14),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Shark Type",
        yaxis_title="Number of Incidents",
        showlegend=True,
        height=750,
        width=1000,
    )

    annotations = []
    for _, row in (
        shark_victim_injury_counts.groupby("shark_common_name")
        .first()
        .iterrows()
    ):
        annotations.append(
            dict(
                x=row.name,
                y=-5,
                text=f"Total: {row['total_sum']}",
                showarrow=False,
                font=dict(color="#00796b", size=12),
                xanchor="center",
                yanchor="top",
            )
        )

    bar_graph.update_layout(annotations=annotations)

    return bar_graph


# Activities related graphs
# Victim activity graphs
def compare_victim_activity_vs_provoked(df: pd.DataFrame) -> go.Figure:
    """
    Compare shark attacks against victim activity and provoked/unprovoked status.
    Considers the top 10 victim activities, separating the bars by provoked/unprovoked.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing shark incident data.

    Returns:
        go.Figure: A Plotly figure object representing the grouped bar chart.
    """

    df["victim_activity_updated"] = np.nan
    df["victim_activity_updated"] = df["victim_activity"].apply(
        lambda x: (
            x
            if x
            in [
                "swimming",
                "boarding",
                "snorkelling",
                "spearfishing",
                "diving",
                "fishing",
                "unknown",
                "unmotorised boating",
            ]
            else "other_activities"
        )
    )

    top_activities = df["victim_activity_updated"].value_counts().index[:10]

    df_top_activities = df[df["victim_activity_updated"].isin(top_activities)]

    victim_activity_counts = (
        df_top_activities.groupby(
            ["victim_activity_updated", "provoked_unprovoked"]
        )
        .size()
        .reset_index(name="count")
    )

    victim_activity_counts["total_sum"] = victim_activity_counts.groupby(
        "victim_activity_updated"
    )["count"].transform("sum")

    victim_activity_counts = victim_activity_counts.sort_values(
        by=["total_sum", "victim_activity_updated"], ascending=[False, True]
    )

    bar_graph = px.bar(
        victim_activity_counts,
        x="victim_activity_updated",
        y="count",
        color="provoked_unprovoked",
        title="Shark Attacks by Top Victim Activities and Provoked/Unprovoked",
        labels={
            "victim_activity_updated": "Victim Activity",
            "count": "Number of Incidents",
            "provoked_unprovoked": "Provoked/Unprovoked",
        },
        barmode="group",
    )

    bar_graph.update_traces(textposition="none")
    bar_graph.update_layout(
        font=dict(color="#00796b", size=14),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Victim Activity",
        yaxis_title="Number of Incidents",
        showlegend=True,
        height=750,
        width=1000,
    )

    return bar_graph


def create_attack_severity_chart(df):
    """
    Creates a grouped bar chart for attack severity by site category.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing filtered data.

    Returns:
        go.Figure: The Plotly bar chart figure.
    """
    count_data = (
        df.groupby(["site_category_cleaned", "injury_severity"])
        .size()
        .reset_index(name="count")
    )

    bar_graph = px.bar(
        count_data,
        x="site_category_cleaned",
        y="count",
        color="injury_severity",
        barmode="group",
        title="Attack Severity by Site Category",
        labels={
            "site_category_cleaned": "Site Category",
            "count": "Number of Incidents",
            "injury_severity": "Severity",
        },
        color_discrete_sequence=px.colors.qualitative.Safe,
        width=1200,
        height=800,
    )

    bar_graph.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        title_font=dict(size=20),
        bargap=0.2,
        bargroupgap=0.1,
        legend=dict(
            font=dict(size=12),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
    )

    bar_graph.update_traces(
        width=None,
        texttemplate="%{y}",
        textposition="outside",
        textfont_size=12,
    )

    return bar_graph


def create_grouped_bar_chart(
    df, x_col, color_col, title, x_label, color_label
):
    """
    Creates a generic grouped bar chart.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing data.
        x_col (str): The column to use for the x-axis.
        color_col (str): The column to use for bar colors.
        title (str): The title of the chart.
        x_label (str): The label for the x-axis.
        color_label (str): The label for the bar colors.

    Returns:
        go.Figure: The Plotly bar chart figure.
    """
    count_data = (
        df.groupby([x_col, color_col]).size().reset_index(name="count")
    )

    bar_graph = px.bar(
        count_data,
        x=x_col,
        y="count",
        color=color_col,
        barmode="group",
        title=title,
        labels={
            x_col: x_label,
            "count": "Number of Incidents",
            color_col: color_label,
        },
        color_discrete_sequence=px.colors.qualitative.Safe,
        width=1200,
        height=800,
    )

    bar_graph.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        title_font=dict(size=20),
        bargap=0.2,
        bargroupgap=0.1,
        legend=dict(
            font=dict(size=12),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
    )

    bar_graph.update_traces(
        width=None,
        texttemplate="%{y}",
        textposition="outside",
        textfont_size=12,
    )

    return bar_graph


# create_grouped_bar_chart(
#     df=shark_data,
#     x_col="site_category_cleaned",
#     color_col="victim_injury",
#     title="Injury Type by Victim Gender",
#     x_label="Injury Type",
#     color_label="Gender"
# )

# create_grouped_bar_chart(
#     df=shark_data,
#     x_col="site_category_cleaned",
#     color_col="injury_severity",
#     title="Attack Severity by Site Category",
#     x_label="Site Category",
#     color_label="Severity"
# )
