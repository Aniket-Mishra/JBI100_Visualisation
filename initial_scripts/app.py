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
    "/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/data/Australian Shark-Incident Database Public Version.xlsx",
    sheet_name="ASID",
)

st.set_page_config(
    page_title="Shark Incident Visualizations",
    page_icon="/Users/paniket/TU_Eindhoven/2_Study/Q2_JBI100_Visualisation_4/4_Code/JBI100_Visualisation/images/shark_smile.png",
    layout="wide",
)

# st.markdown(
#     """
#     <style>
#     /* Dropdown container */
#     div[data-baseweb="select"] {
#         background-color: #3C3F58; /* Medium grey background */
#         color: #EDF2F4; /* Light grey text */
#         border-radius: 8px; /* Rounded corners */
#         border: 1px solid #8D99AE; /* Grey-blue border */
#     }

#     /* Dropdown hover and selected options */
#     div[data-baseweb="select"] > div {
#         background-color: #3C3F58 !important; /* Match dropdown background */
#         color: #EDF2F4 !important;
#     }

#     /* Dropdown list options */
#     ul {
#         background-color: #3C3F58 !important; /* Medium grey background for list */
#         color: #8D99AE !important; /* Grey-blue text */
#     }

#     /* Hover effect for options */
#     ul > li:hover {
#         background-color: #EF233C !important; /* Vivid red highlight */
#         color: #EDF2F4 !important; /* Light text */
#     }

#     /* Selected option styling */
#     ul > li[aria-selected="true"] {
#         background-color: #8D99AE !important; /* Grey-blue for selected */
#         color: #EDF2F4 !important; /* White text for contrast */
#     }
#     .element-container {
#         width: 95% !important;
#         margin: auto;
#     }
#     div.block-container {
#         max-width: 85%;
#         padding: 50px;
#         margin: auto;
#     }

#     # [data-testid="stSidebar"] .stSelectbox {
#     #     color: white; /* Text color */
#     #     background-color: #121212; /* Background color */
#     #     # border: 1px solid #ccc; /* Border color */
#     # }
#     # [data-testid="stSidebar"] .stSelectbox:hover {
#     #     background-color: #232323; /* Background color on hover */
#     # }

#     /* Target the multiselect widget in the sidebar */
#     # [data-testid="stSidebar"] .stMultiSelect {
#     #     background-color: #121212; /* Background color */
#     #     color: #EDF2F4; /* Text color */
#     #     border: 1px solid #ccc; /* Border color */
#     #     border-radius: 5px; /* Rounded corners */
#     # }
#     # [data-testid="stSidebar"] .stMultiSelect:hover {
#     #     background-color: #454545; /* Hover effect */
#     # }
#     # [data-testid="stSidebar"] .stMultiSelect .css-1d391kg {
#     #     color: #EDF2F4; /* Text inside multiselect */
#     # }

#     # [data-testid="stSidebar"] .stMultiSelect .css-1nwa0ja {
#     #     background-color: #121212; /* Background color of the dropdown items */
#     #     color: #EDF2F4; /* Text color of the dropdown items */
#     #     border-radius: 5px; /* Optional: Rounded corners for dropdown items */
#     # }
#     # [data-testid="stSidebar"] .stMultiSelect .css-1nwa0ja:hover {
#     #     background-color: #121212; /* Background color on hover */
#     #     color: #EDF2F4; /* Text color on hover */
#     # }

#     # [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] {
#     #     background-color: #4CAF50 !important; /* Change background color of selected items */
#     #     color: white !important; /* Change text color of selected items */
#     #     border-radius: 10px; /* Optional: Rounded corners for a modern look */
#     #     padding: 5px; /* Add padding for better readability */
#     # }
#     # [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"]:hover {
#     #     background-color: #45a049 !important; /* Change background color on hover */
#     # }

#     # .stMultiSelect div[data-baseweb="tag"] {
#     #     background-color: #4CAF50 !important; /* New background color for selected items */
#     #     color: white !important; /* Text color for selected items */
#     #     border-radius: 10px; /* Rounded corners for a sleek look */
#     #     padding: 5px; /* Optional: Add padding for readability */
#     # }
#     # .stMultiSelect div[data-baseweb="tag"] svg {
#     #     fill: white !important; /* Change the color of the close (X) icon */
#     # }
#     # .stMultiSelect div[data-baseweb="tag"]:hover {
#     #     background-color: #45a049 !important; /* Background color on hover */
#     # }
#     [data-testid="stSidebar"] {
#         font-size: 32px; /* Adjust font size here */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


st.title("Interactive Shark Attack Data Explorer")
st.sidebar.header("Filter Options")

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
# st.plotly_chart(fig1, key="fig1")


# fig2 = px.histogram(
#     filtered_data,
#     x="Site.category",
#     color="Injury.severity",
#     title="Attack Severity by Site Category",
#     labels={"Site.category": "Site Category", "Injury.severity": "Severity"},
# )
# # st.plotly_chart(fig2, key="fig2")

count_data = (
    filtered_data.groupby(["Site.category", "Injury.severity"])
    .size()
    .reset_index(name="count")
)
fig2 = px.bar(
    count_data,
    x="Site.category",
    y="count",
    color="Injury.severity",
    barmode="group",  # Grouped bar chart
    title="Attack Severity by Site Category",
    labels={
        "Site.category": "Site Category",
        "count": "Number of Incidents",
        "Injury.severity": "Severity",
    },
    color_discrete_sequence=px.colors.qualitative.Safe,
    width=1200,
    height=800,
)

# Adjust layout
fig2.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
    plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot area
    font_color="white",  # High contrast text
    title_font=dict(size=20),
    bargap=0.2,  # Adjust the gap between groups (increase for more space)
    bargroupgap=0.1,  # Adjust the gap between bars in the same group
    legend=dict(
        font=dict(size=12),
        bgcolor="rgba(0,0,0,0)",  # No background for legend
        borderwidth=0,  # No border
    ),
)

# Adjust bar thickness and add data labels
fig2.update_traces(
    width=None,  # Automatically adjusts width to fit group spacing
    texttemplate="%{y}",  # Display values above bars
    textposition="outside",
    textfont_size=12,
)


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
    width=1200,  # Set the width of the figure
    height=900,  # Set the height of the figure
)

# fig3.show()

fig4 = px.bar(
    filtered_data,
    x="Victim.activity",
    color="Provoked/unprovoked",
    title="Victim Activities and Provocation",
    labels={
        "Victim.activity": "Activity",
        "Provoked/unprovoked": "Provocation Type",
    },
)
# st.plotly_chart(fig4, key="fig4")

# fig5 = px.bar(
#     filtered_data,
#     x="Shark.common.name",
#     color="Injury.severity",
#     title="Shark Species Involved in Incidents",
#     labels={"Shark.common.name": "Shark Species", "Injury.severity": "Severity"},
# )
# st.plotly_chart(fig5, key="fig5")

# shark_data = (
#     filtered_data.groupby(["Shark.common.name", "Injury.severity"])
#     .size()
#     .reset_index(name="count")
# )

# # Create the grouped bar chart
# fig5 = px.bar(
#     shark_data,
#     x="Shark.common.name",
#     y="count",
#     color="Injury.severity",
#     barmode="group",  # Grouped bar chart for better comparison
#     title="Shark Species Involved in Incidents",
#     labels={
#         "Shark.common.name": "Shark Species",
#         "count": "Number of Incidents",
#         "Injury.severity": "Severity",
#     },
#     color_discrete_sequence=px.colors.qualitative.Safe,  # Colorblind-friendly palette
# )

# # Adjust layout for improved spacing and readability
# fig5.update_layout(
#     paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
#     plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot area
#     font_color="white",  # High contrast text
#     title_font=dict(size=20),
#     bargap=0.2,  # Space between groups
#     bargroupgap=0.1,  # Space between bars within a group
#     legend=dict(
#         font=dict(size=12),
#         bgcolor="rgba(0,0,0,0)",  # No background for legend
#         borderwidth=0,  # No border
#     ),
# )

# # Add data labels and automatic bar width adjustment
# fig5.update_traces(
#     width=None,  # Automatically adjust bar width
#     texttemplate="%{y}",  # Display values on bars
#     textposition="outside",
#     textfont_size=12,
# )

shark_data = (
    filtered_data.groupby(["Shark.common.name", "Injury.severity"])
    .size()
    .reset_index(name="count")
)

# Sort species by total count
shark_data_sorted = (
    shark_data.groupby("Shark.common.name")["count"]
    .sum()
    .reset_index()
    .sort_values(by="count", ascending=False)
)
shark_data = shark_data.merge(
    shark_data_sorted, on="Shark.common.name", suffixes=("", "_total")
)
shark_data = shark_data.sort_values(by="count_total", ascending=False)
top_species = shark_data_sorted.head(5)["Shark.common.name"]

# Filter the data for only top species
top_shark_data = shark_data[shark_data["Shark.common.name"].isin(top_species)]

# Create a grouped bar chart for top species
fig5 = px.bar(
    top_shark_data,
    x="Shark.common.name",
    y="count",
    color="Injury.severity",
    barmode="group",
    title="Top 5 Shark Species Involved in Incidents",
    labels={
        "Shark.common.name": "Shark Species",
        "count": "Number of Incidents",
        "Injury.severity": "Severity",
    },
    color_discrete_sequence=px.colors.qualitative.Safe,  # Colorblind-friendly palette
)

# Adjust layout
fig5.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    title_font=dict(size=20),
    bargap=0.2,
    legend=dict(
        font=dict(size=12),
        bgcolor="rgba(0,0,0,0)",
        borderwidth=0,
    ),
)

fig5.update_traces(
    width=None,  # Automatically adjusts width to fit group spacing
    texttemplate="%{y}",  # Display values above bars
    textposition="outside",
    textfont_size=12,
)


fig_severity = px.pie(
    filtered_data,
    names="Injury.severity",
    title="Severity of Shark Attacks",
    hole=0.5,  # Donut chart
    labels={"Injury.severity": "Severity"},
    color_discrete_sequence=px.colors.sequential.Viridis,  # Similar to line chart
)

# Add central text for context
fig_severity.update_layout(
    annotations=[
        dict(
            text="Fatal Cases<br><b>15%</b>",  # Clean central label
            x=0.5,
            y=0.5,
            font_size=16,
            showarrow=False,
            font=dict(color="white"),
            align="center",
        )
    ],
    paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
    plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot area
    font_color="white",  # White text for contrast
    title_font=dict(size=20),  # Readable title
    legend=dict(
        font=dict(size=12),
        bgcolor="rgba(0,0,0,0)",  # Transparent legend background
    ),
)

# Ensure font sizes and labels are consistent
fig_severity.update_traces(
    textinfo="percent+label",  # Show percentage and label on slices
    textfont_size=14,  # Adjust label font size
)

graph_choice = st.sidebar.selectbox(
    "Select a Graph to Display",
    options=[
        "Shark Attacks Over Time",
        "Attack Severity by Site Category",
        "Geographic Distribution",
        "Victim Activity and Provocation",
        "Top 5 Shark Species Involved",
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
elif graph_choice == "Top 5 Shark Species Involved":
    st.plotly_chart(fig5, use_container_width=True)
elif graph_choice == "Injury Severity":
    st.plotly_chart(fig_severity, use_container_width=True)
