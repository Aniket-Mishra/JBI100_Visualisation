import numpy as np
import pandas as pd
import plotly.graph_objects as go
from typing import List, Tuple


def prepare_data(path: str) -> pd.DataFrame:

    df = pd.read_csv(path)
    return df


def map_months_for_graphs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map number 1-12 to months Jan-Dec

    Args:
        df (pd.DataFrame): Dataframe containing all data

    Returns:
        pd.DataFrame: Dataframe with months being converted
    """
    month_mapping = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }
    df["incident_month"] = df["incident_month"].map(month_mapping)
    return df


def filter_data_by_states(
    df: pd.DataFrame, selected_states: list
) -> pd.DataFrame:
    """
    Dataframe to get selected states

    Args:
        df (pd.DataFrame): Initial df
        selected_states (list): list of states in selected list

    Returns:
        pd.DataFrame: df with only selected states
    """
    return df[df["state_names"].isin(selected_states)]


def filter_data_single_column_single_value(
    df: pd.DataFrame, column_name: str, column_value: str
) -> pd.DataFrame:
    """_summary_

    Args:
        df (pd.DataFrame): initial df
        column_name (str): column to filter
        column_value (str): value to filter from column

    Returns:
        pd.DataFrame: df after filter
    """
    return df[df[column_name] == column_value]


def groupby_count(
    df: pd.DataFrame, column_name: str, index_name: str
) -> pd.DataFrame:
    """
    function to get groupby object from df

    Args:
        df (pd.DataFrame): initial df
        column_name (str): column to group by
        index_name (str): index to reset (Else it is a series)

    Returns:
        pd.DataFrame.groupby: groupby object df
    """
    # no sorting
    return df.groupby(column_name).size().reset_index(name=index_name)


def get_reset_value_counts(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Get value counts and convert to df

    Args:
        df (pd.DataFrame): initial df
        column_name (str): column to get value counts

    Returns:
        pd.DataFrame: value counts df
    """
    # sorting + faster no smol data
    return df[column_name].value_counts().reset_index()


def prepare_top_n_data(
    value_counts: pd.DataFrame, column_name: str, top_n: int
) -> Tuple[List, str]:
    """
    function to get the top N data from value count df

    Args:
        value_counts (pd.DataFrame): dataFrame containing value counts
        column_name (str): column name to get top n from
        top_n (int): number of top entries to include

    Returns:
        Tuple[List, str]: A tuple containing:
            - A list of the top N values from the specified column.
            - A string message summarizing the extracted top N values.
    """
    top_categories = value_counts.head(top_n)
    others = value_counts.iloc[top_n:]

    num_others = others[column_name].nunique()
    others_count = others["count"].sum()

    if num_others > 0:
        others_row = {
            column_name: f"others: {num_others} types",
            "count": others_count,
        }
        top_categories = pd.concat(
            [top_categories, pd.DataFrame([others_row])], ignore_index=True
        )

    others_text = "<br>".join(
        [
            f"{row[column_name]}: {row['count']} incidents"
            for _, row in others.iterrows()
        ]
    )

    hover_text = [
        (
            f"{row[column_name]}: {row['count']} incidents"
            if row[column_name] != f"others: {num_others} types"
            else others_text
        )
        for _, row in top_categories.iterrows()
    ]
    top_categories["hover_text"] = hover_text

    return top_categories, others_text


def get_single_line_plot(
    df: pd.DataFrame, xaxis_name: str, yaxis_name: str, title: str
) -> go.Figure:
    """
    get single line plot graph object

    Args:
        df (pd.DataFrame): initial df
        xaxis_name (str): xaxis name
        yaxis_name (str): yaxis name
        title (str): title of graph

    Returns:
        go.Figure: output figure
    """
    line_fig = go.Figure(
        data=[
            go.Scatter(
                x=df[xaxis_name],
                y=df[yaxis_name],
                mode="lines",
                line=dict(color="#26a69a"),
                name="Incidents",
            )
        ]
    )
    line_fig.update_layout(
        title=title,
        font=dict(color="#ffd600", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        yaxis_title="Number of Incidents",
    )
    return line_fig


def get_double_line_fig(
    df_first_agg: pd.DataFrame,
    df_second_agg: pd.DataFrame,
    xname: str,
    y1name: str,
    y2name: str,
    g1_name: str,
    g2_name: str,
    title: str,
    yaxis_title: str,
):
    """
    generates a dual-line plotly figure to compare two datasets.

    args:
        df_first_agg (pd.DataFrame): first dataframe with data for the first line
        df_second_agg (pd.DataFrame): second dataframe with data for the second line
        xname (str): colname of x-axis
        y1name (str): colname of y-axis of the first line
        y2name (str): colname of y-axis of the second line
        g1_name (str): legend name for the first line
        g2_name (str): legend name for the second line
        title (str): title of the graph
        yaxis_title (str): label for the y-axis

    returns:
        go.Figure: a plotly figure with two line plots
    """

    line_fig = go.Figure(
        data=[
            go.Scatter(
                x=df_first_agg[xname],
                y=df_first_agg[y1name],
                mode="lines",
                line=dict(color="#26a69a"),
                name=g1_name,
            ),
            go.Scatter(
                x=df_second_agg[xname],
                y=df_second_agg[y2name],
                mode="lines",
                line=dict(color="#ab47bc"),
                name=g2_name,
            ),
        ]
    )
    line_fig.update_layout(
        title=title,
        # title=dict(
        #     text=title,
        #     x=0.1,
        #     y=1,
        #     xanchor="left",
        #     yanchor="top",
        #     font=dict(size=16, color="#26a69a"),
        # ),
        legend=dict(
            orientation="h",
            x=0.01,
            y=1,
            xanchor="left",
            yanchor="top",
            font=dict(size=12, color="#ffd600"),
        ),
        font=dict(color="#ffd600", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        yaxis_title=yaxis_title,
        # transition={"duration": 500, "easing": "sin-in-out"},
    )
    return line_fig


def get_bar_fig(
    df: pd.DataFrame,
    xaxis_name: str,
    yaxis_name: str,
    title: str,
    yaxis_title: str = None,
) -> go.Figure:
    """
    generates a bar chart using plotly to visualize data from a dataframe.

    args:
        df (pd.DataFrame): dataframe containing the data to be plotted.
        xaxis_name (str): column name for the x-axis.
        yaxis_name (str): column name for the y-axis.
        title (str): title of the bar chart.
        yaxis_title (str): label for the y-axis (optional, defaults to None).

    returns:
        go.Figure: a plotly figure with a single bar chart.
    """
    if xaxis_name.lower().find("month") != -1:
        df = map_months_for_graphs(df)
    bar_fig = go.Figure(
        data=[
            go.Bar(x=df[xaxis_name], y=df[yaxis_name], marker_color="#26a69a")
        ]
    )
    bar_fig.update_layout(
        title=title,
        font=dict(color="#ffd600", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, automargin=True),
        yaxis=dict(showgrid=False, automargin=True),
        transition={"duration": 500, "easing": "sin-in-out"},
        yaxis_title=yaxis_title,
        barmode="group",  # Ensure consistent bar mode
    )
    return bar_fig


def get_double_bar_fig(
    combined_counts: pd.DataFrame,
    xname: str,
    y1name: str,
    y2name: str,
    g1_name: str,
    g2_name: str,
    title: str,
    yaxis_title: str = None,
) -> go.Figure:
    """
    generates a dual-bar plotly figure to compare two datasets side by side.

    args:
        combined_counts (pd.DataFrame): dataframe containing data for both bars.
        xname (str): column name for the x-axis.
        y1name (str): column name for the y-axis of the first bar group.
        y2name (str): column name for the y-axis of the second bar group.
        g1_name (str): legend name for the first bar group.
        g2_name (str): legend name for the second bar group.
        title (str): title of the bar chart.
        yaxis_title (str): label for the y-axis (optional, defaults to None).

    returns:
        go.Figure: a plotly figure with two grouped bar charts.
    """
    if xname.lower().find("month") != -1:
        combined_counts = map_months_for_graphs(combined_counts)
    bar_fig = go.Figure(
        data=[
            go.Bar(
                x=combined_counts[xname],
                y=combined_counts[y1name],
                name=g1_name,
                marker_color="#26a69a",
            ),
            go.Bar(
                x=combined_counts[xname],
                y=combined_counts[y2name],
                name=g2_name,
                marker_color="#ab47bc",
            ),
        ]
    )
    bar_fig.update_layout(
        title=title,
        legend=dict(
            orientation="h",
            x=0.5,
            y=1.15,
            xanchor="center",
            yanchor="top",
            font=dict(size=12, color="#ffd600"),
        ),
        font=dict(color="#ffd600", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, automargin=True),
        yaxis=dict(showgrid=False, automargin=True),
        transition={"duration": 500, "easing": "sin-in-out"},
        yaxis_title=yaxis_title,
        barmode="group",  # Ensure consistent bar mode
    )
    return bar_fig


def get_pie_chart(
    df: pd.DataFrame,
    labels: str,
    values: str,
    title: str,
) -> go.Figure:
    """
    generates a pie chart using plotly for visualizing proportions.

    args:
        df (pd.DataFrame): dataframe containing the data to be visualized.
        labels (str): column name for the labels of the pie chart.
        values (str): column name for the values to be represented in the pie chart.
        title (str): title of the pie chart.

    returns:
        go.Figure: a plotly figure representing the pie or donut chart.
    """
    pie_chart = go.Figure(
        data=[
            go.Pie(
                labels=df[labels],
                values=df[values],
                hole=0.3,  # For a donut chart effect; set to 0 for a full pie chart
            )
        ]
    )

    pie_chart.update_layout(
        title=title,
        font=dict(color="#ffd600", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return pie_chart
