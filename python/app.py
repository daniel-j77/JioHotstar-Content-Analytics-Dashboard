import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="JioHotstar Content Analytics",
    page_icon="📺",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/disney_plus_titles.csv")
    return df

df = load_data()

# ---------------- BACKGROUND ----------------

with open("images/jiohotstar_background.png", "rb") as f:
    bg = f.read()
CARD_BG = "rgba(8,20,66,0.95)"
import base64

bg_base64 = base64.b64encode(bg).decode()

st.markdown(
    f"""
    <style>

    .stApp {{
        background-image:url("data:image/png;base64,{bg_base64}");
        background-size:cover;
        background-attachment:fixed;
    }}

    section[data-testid="stSidebar"] {{
        background:#08113a;
    }}

    .kpi {{
        background:#08113a;
        border:1px solid #2847ff;
        border-radius:14px;
        padding:18px;
    }}

    .kpi-label {{
        color:#BFC7E5;
        font-size:14px;
    }}

    .kpi-value {{
        color:white;
        font-size:36px;
        font-weight:700;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOGO + TITLE ----------------

logo = Image.open("images/logo.png")

c1, c2 = st.columns([1, 8])

with c1:
    st.image(logo, width=170)

with c2:
    st.markdown(
        """
        <h1 style='color:white;margin-top:15px'>
        JioHotstar Content Analytics Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

# ---------------- SIDEBAR ----------------

st.sidebar.title("Filters")

type_filter = st.sidebar.multiselect(
    "Type",
    sorted(df["type"].dropna().unique())
)

country_filter = st.sidebar.multiselect(
    "Country",
    sorted(df["country"].dropna().unique())
)

genre_filter = st.sidebar.multiselect(
    "Genre",
    sorted(df["listed_in"].dropna().unique())
)

rating_filter = st.sidebar.multiselect(
    "Rating",
    sorted(df["rating"].dropna().unique())
)

# ---------------- FILTER LOGIC ----------------

filtered = df.copy()

if type_filter:
    filtered = filtered[filtered["type"].isin(type_filter)]

if country_filter:
    filtered = filtered[filtered["country"].isin(country_filter)]

if genre_filter:
    filtered = filtered[filtered["listed_in"].isin(genre_filter)]

if rating_filter:
    filtered = filtered[filtered["rating"].isin(rating_filter)]


# ---------------- KPI CARDS ----------------

total_titles = len(filtered)
movies = len(filtered[filtered["type"] == "Movie"])
tvshows = len(filtered[filtered["type"] == "TV Show"])
countries = filtered["country"].nunique()
genres = filtered["listed_in"].nunique()

avg_duration = 0

if "duration_num" in filtered.columns:
    avg_duration = round(filtered["duration_num"].mean(), 1)

cols = st.columns([1,1,1,1,1,1])
st.markdown(
    """
    <style>
    .kpi-value{
        font-size:42px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
kpis = [
    ("Total Titles", total_titles),
    ("Movies", movies),
    ("TV Shows", tvshows),
    ("Countries", countries),
    ("Genres", genres),
    ("Avg Duration", avg_duration)
]

for col, (label, value) in zip(cols, kpis):
    with col:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- ROW 1 ----------------

left, right = st.columns(2)

# Donut

with left:

    donut = filtered["type"].value_counts()

    fig = px.pie(
        values=donut.values,
        names=donut.index,
        hole=0.65
    )

    fig.update_traces(
        marker=dict(
            colors=["#11C5FF", "#A855F7"]
        ),

        texttemplate="%{value} (%{percent})",

        textposition="outside",

        textfont=dict(
            color="white",
            size=16
        ),

        hovertemplate=
        "<b>%{label}</b><br>" +
        "Titles: %{value}<br>" +
        "Percentage: %{percent}<extra></extra>"
    )

    fig.update_layout(
        title="Movies vs TV Shows",
        height=500,

        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,

        font_color="white",

        showlegend=True,

        legend=dict(
            font=dict(color="white", size=14),
            x=1.02,
            y=1
        ),

        margin=dict(
            l=80,
            r=80,
            t=60,
            b=60
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# Content Added

with right:

    if "year_added" in filtered.columns:

        trend = (
            filtered.groupby("year_added")
            .size()
            .reset_index(name="Titles")
        )

        fig = px.line(
    trend,
    x="year_added",
    y="Titles",
    markers=True,
    text="Titles"
)

        fig.update_traces(
    line_color="#A855F7",
    textposition="top center"
)
        fig.update_layout(
            title="Content Added by Year",
            height=500,
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font_color="white"
        )

        st.plotly_chart(fig,use_container_width=True)



# ---------------- ROW 2 ----------------

left, right = st.columns(2)
# Top Countries

with left:

    top_country = (
        filtered["country"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_country.columns = ["Country","Titles"]

    fig = px.bar(
    top_country,
    x="Titles",
    y="Country",
    orientation="h",
    text="Titles"
)

    fig.update_traces(
    marker_color="#FF1493",
    textposition="outside",
    cliponaxis=False
)

    fig.update_layout(
    title="Top Countries",
    height=500,
    xaxis=dict(range=[0, top_country["Titles"].max()*1.25]),
    yaxis=dict(autorange="reversed"),
    paper_bgcolor=CARD_BG,
    plot_bgcolor=CARD_BG,
    font_color="white"
)

    st.plotly_chart(fig,use_container_width=True)
# Top Genres

with right:

    genre = (
    filtered["listed_in"]
    .value_counts()
    .head(10)
    .reset_index()
)

    genre.columns = ["Genre", "Titles"]

# Sort descending
    genre = genre.sort_values(
    by="Titles",
    ascending=False
)

    fig = px.bar(
    genre,
    x="Titles",
    y="Genre",
    orientation="h",
    text="Titles"
)

    fig.update_traces(
    marker_color="#00BFFF",
    textposition="outside",
    cliponaxis=False
)

    fig.update_layout(
    title="Top Genres",
    height=500,
    xaxis=dict(range=[0, genre["Titles"].max()*1.25]),
    yaxis=dict(
        categoryorder="total ascending"
    ),
    paper_bgcolor=CARD_BG,
    plot_bgcolor=CARD_BG,
    font_color="white"
)

    st.plotly_chart(fig, use_container_width=True)


# ---------------- ROW 3 ----------------

left, right = st.columns(2)
# Ratings Treemap

with left:

    rating = (
        filtered["rating"]
        .value_counts()
        .reset_index()
    )

    rating.columns = ["Rating", "Count"]

    fig = px.treemap(
        rating,
        path=["Rating"],
        values="Count",
        color="Count",
        color_continuous_scale="Plasma"
    )

    fig.update_layout(
        title="Ratings Distribution",
        height=500,
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font_color="white",
        margin=dict(t=50,l=10,r=10,b=10)
    )

    st.plotly_chart(fig, use_container_width=True)
# Release Trend

with right:

    release = (
        filtered.groupby("release_year")
        .size()
        .reset_index(name="Titles")
    )

    fig = px.area(
        release,
        x="release_year",
        y="Titles"
    )

    fig.update_traces(
        line_color="#A855F7"
    )

    fig.update_layout(
        title="Release Year Trend",
        height=500,
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font_color="white"
    )

    st.plotly_chart(fig,use_container_width=True)
# ---------------- ROW 4 ----------------
left, right = st.columns(2)
with left:

    country_map = (
        filtered["country"]
        .value_counts()
        .reset_index()
    )

    country_map.columns = ["country","titles"]

    fig = px.choropleth(
    country_map,
    locations="country",
    locationmode="country names",
    color="titles",
    color_continuous_scale="Plasma"
)

    fig.update_geos(
    showcoastlines=False,
    showframe=False,
    bgcolor="rgba(0,0,0,0)"
)

    fig.update_layout(
    title="Country Distribution",
    paper_bgcolor=CARD_BG,
    geo_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    height=500
)
    st.plotly_chart(fig,use_container_width=True)

with right:

   st.markdown("""
### 📊 Key Insights

✅ Movies account for over 70% of total content

✅ United States is the largest content producer

✅ TV Shows continue to grow every year

✅ Drama and Animation dominate the platform

✅ Major content additions happened after 2018

✅ Platform content spans 90+ countries
""")
