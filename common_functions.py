import numpy as np
import pandas as pd
import plotly.graph_objects as go


def prepare_data(path: str) -> pd.DataFrame:

    df = pd.read_csv(path)
    df = df.loc[df["provoked_unprovoked"] != "unknown"]
    df.loc[
        df["shark_common_name"] == "shark_not_known", "shark_common_name"
    ] = "unknown"
    df.loc[
        df["shark_common_name"] == "bronze whaler shark", "shark_common_name"
    ] = "bronze whaler"
    df["shark_common_name"] = df["shark_common_name"].apply(
        lambda x: x.replace(" shark", "").title()
    )

    # df["site_category_cleaned"] =
    df.loc[
        ~(
            df["site_category_cleaned"].isin(
                [
                    "coastal",
                    "island_open_ocean",
                    "estuary_harbour",
                    "river",
                    np.nan,
                ]
            )
        ),
        "site_category_cleaned",
    ] = "Others"
    # df["site_category_cleaned"] = df["site_category_cleaned"].fillna("Unknown")
    df["site_category_cleaned"] = df["site_category_cleaned"].apply(
        lambda x: x.replace("_", " ").title()
    )

    df.loc[
        ~(
            df["injury_severity"].isin(
                ["major_lacerations", "minor_lacerations", np.nan]
            )
        ),
        "injury_severity",
    ] = "Others"
    df["injury_severity"] = df["injury_severity"].replace(
        {
            "major_lacerations": "Maj.Lacerations",
            "minor_lacerations": "Min.Lacerations",
        }
    )
    df["injury_severity"] = df["injury_severity"].fillna("Unknown")

    df["injury_severity"] = df["injury_severity"].apply(
        lambda x: str(x).replace("_", " ").title()
    )

    return df


def map_months_for_graphs(df):
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
    return df[df["state_names"].isin(selected_states)]


def filter_data_single_column_single_value(
    df: pd.DataFrame, column_name: str, column_value: str
) -> pd.DataFrame:
    return df[df[column_name] == column_value]


def groupby_count(df: pd.DataFrame, column_name: str, index_name: str):
    # no sorting
    return df.groupby(column_name).size().reset_index(name=index_name)


def get_reset_value_counts(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    # sorting + faster no smol data
    return df[column_name].value_counts().reset_index()


def prepare_top_n_data(value_counts, column_name, top_n):
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
    df_first_agg,
    df_second_agg,
    xname,
    y1name,
    y2name,
    g1_name,
    g2_name,
    title,
    yaxis_title,
):
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
):
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
    combined_counts,
    xname,
    y1name,
    y2name,
    g1_name,
    g2_name,
    title,
    yaxis_title: str = None,
):
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
):
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
