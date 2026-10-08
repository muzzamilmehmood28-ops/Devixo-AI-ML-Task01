import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(
    page_title="Netflix Dataset Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv('Dataset.csv')
    if 'release_year' in df.columns:
        df = df.rename(columns={'release_year': 'specific_release_year'})
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'Dataset.csv' file not found. Please ensure it is in the same directory as this script.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Dashboard Filters")

# Content Type Filter
content_types = df['type'].dropna().unique().tolist()
selected_type = st.sidebar.selectbox("Select Content Type", options=["All"] + content_types)

# Specific Release Year Range Filter
min_year = int(df['specific_release_year'].min())
max_year = int(df['specific_release_year'].max())
year_range = st.sidebar.slider(
    "Select Specific Release Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Country Filter
countries = sorted(df['country'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", options=["All"] + countries)

# Apply Filters
filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df['type'] == selected_type]
if selected_country != "All":
    filtered_df = filtered_df[filtered_df['country'] == selected_country]
filtered_df = filtered_df[
    (filtered_df['specific_release_year'] >= year_range[0]) & 
    (filtered_df['specific_release_year'] <= year_range[1])
]

# --- MAIN DASHBOARD HEADER ---
st.title("📊 Netflix Content Analysis Dashboard")
st.markdown("An interactive dashboard exploring catalog trends, distribution patterns, and metadata statistics.")

# --- TOP KPIS ---
st.markdown("### 📌 Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{len(filtered_df):,}")
col2.metric("Total Columns", f"{len(filtered_df.columns)}")
col3.metric("Avg Specific Release Year", f"{filtered_df['specific_release_year'].mean():.1f}" if len(filtered_df) > 0 else "N/A")
top_country = filtered_df['country'].mode()[0] if not filtered_df['country'].dropna().empty else "N/A"
col4.metric("Top Country", top_country)

st.markdown("---")

# --- ROW 1: CHARTS ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📈 Distribution of Specific Release Years")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(filtered_df['specific_release_year'], bins=30, kde=True, color='teal', ax=ax)
    ax.set_title("Histogram of Specific Release Years", fontweight='bold')
    ax.set_xlabel("Specific Release Year")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

with col_b:
    st.subheader("🌍 Top 10 Production Countries")
    fig, ax = plt.subplots(figsize=(8, 4))
    top_countries = filtered_df['country'].value_counts().head(10)
    if not top_countries.empty:
        sns.barplot(x=top_countries.values, y=top_countries.index, hue=top_countries.index, palette='crest', legend=False, ax=ax)
        ax.set_title("Top 10 Production Countries", fontweight='bold')
        ax.set_xlabel("Count")
        ax.set_ylabel("Country")
    else:
        ax.text(0.5, 0.5, "No data available", horizontalalignment='center', verticalalignment='center')
    st.pyplot(fig)

# --- ROW 2: CHARTS ---
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("🥧 Proportion of Content Types")
    fig, ax = plt.subplots(figsize=(6, 6))
    type_counts = filtered_df['type'].value_counts()
    if not type_counts.empty:
        ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', 
               colors=['#2b5c8f', '#2a9d8f'], startangle=90, explode=(0.05, 0))
        ax.set_title("Proportion of Content Types", fontweight='bold')
    else:
        ax.text(0.5, 0.5, "No data available", horizontalalignment='center', verticalalignment='center')
    st.pyplot(fig)

with col_d:
    st.subheader("⭐ Top Maturity Ratings")
    fig, ax = plt.subplots(figsize=(8, 4))
    top_ratings = filtered_df['rating'].value_counts().head(10)
    if not top_ratings.empty:
        sns.barplot(x=top_ratings.index, y=top_ratings.values, hue=top_ratings.index, palette='viridis', legend=False, ax=ax)
        ax.set_title("Count of Top Maturity Ratings", fontweight='bold')
        ax.set_xlabel("Maturity Rating")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
    else:
        ax.text(0.5, 0.5, "No data available", horizontalalignment='center', verticalalignment='center')
    st.pyplot(fig)

st.markdown("---")

# --- SUMMARY STATISTICS & DATA PREVIEW ---
st.markdown("### 📋 Summary Statistics & Filtered Data Preview")
tab1, tab2 = st.tabs(["Summary Statistics", "Raw Dataset View"])

with tab1:
    st.write(filtered_df.describe())

with tab2:
    st.dataframe(filtered_df.head(100), width='stretch')

# --- KEY INSIGHTS SECTION ---
st.markdown("---")
st.markdown("### 💡 Key Insights")
st.markdown("""
* **Contemporary Focus:** The vast majority of titles are concentrated in recent years, with a sharp surge starting in the 2010s.
* **Content Split:** Movies make up the substantial majority of the catalog (~70%), while TV shows account for the remaining (~30%).
* **Geographic Dominance:** The United States leads content production by a wide margin, followed by India and the UK.
* **Audience Targeting:** Maturity ratings skew heavily toward adult and mature audiences (`TV-MA` and `TV-14`).
""")
