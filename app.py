import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import folium
from streamlit_folium import st_folium

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="NYC Airbnb Data Analysis", layout="wide")

st.title("🏠 NYC Airbnb Data Analysis Dashboard")
st.markdown("Exploring pricing, availability, and trends in the NYC Airbnb dataset.")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("AB_NYC_2019.csv")
    # Basic cleaning
    df = df[df['price'] < 1000]
    df = df[df['minimum_nights'] < 365]
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
    return df

df = load_data()

st.sidebar.header("🔎 Filters")
borough = st.sidebar.selectbox("Select Borough", ["All"] + df['neighbourhood_group'].unique().tolist())
if borough != "All":
    df = df[df['neighbourhood_group'] == borough]

# -----------------------------
# 1. Price Distribution
# -----------------------------
st.subheader("💰 Price Distribution")
fig, ax = plt.subplots(figsize=(8,4))
sns.histplot(df['price'], bins=50, kde=True, ax=ax)
ax.set_xlim(0, 500)
st.pyplot(fig)

# -----------------------------
# 2. Price by Borough (Boxplot)
# -----------------------------
st.subheader("📍 Price by Borough")
fig, ax = plt.subplots(figsize=(8,4))
sns.boxplot(x="neighbourhood_group", y="price", data=df, ax=ax)
ax.set_ylim(0, 500)
st.pyplot(fig)

# -----------------------------
# 3. Room Type vs Price
# -----------------------------
st.subheader("🛏️ Room Type vs Price")
fig, ax = plt.subplots(figsize=(8,4))
sns.boxplot(x="room_type", y="price", data=df, ax=ax)
ax.set_ylim(0, 500)
st.pyplot(fig)

# -----------------------------
# 4. Availability Histogram
# -----------------------------
st.subheader("📅 Availability Distribution")
fig, ax = plt.subplots(figsize=(8,4))
sns.histplot(df['availability_365'], bins=30, ax=ax)
st.pyplot(fig)

# -----------------------------
# 5. Correlation Heatmap
# -----------------------------
st.subheader("📊 Correlation Heatmap")
numeric_df = df[['price', 'minimum_nights', 'number_of_reviews',
                 'reviews_per_month', 'availability_365']]
fig, ax = plt.subplots(figsize=(6,4))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

# -----------------------------
# 6. WordCloud of Listings
# -----------------------------
st.subheader("🔠 WordCloud of Listing Names")
text = " ".join(str(name) for name in df['name'] if isinstance(name, str))
wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white",
                      max_words=100, colormap="viridis").generate(text)
fig, ax = plt.subplots(figsize=(10,6))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# -----------------------------
# 7. Interactive Map (Plotly)
# -----------------------------
st.subheader("🗺️ Interactive Map of Listings")
fig = px.scatter_mapbox(df.sample(min(1000, len(df))), 
                        lat="latitude", lon="longitude",
                        color="price", size="availability_365",
                        hover_name="neighbourhood",
                        mapbox_style="carto-positron",
                        zoom=10, title="Airbnb Listings in NYC")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("✅ Analysis complete. Use the sidebar to filter by borough.")
