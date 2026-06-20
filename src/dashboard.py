import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 
# PAGE CONFIG

st.set_page_config(
    page_title="Bangkok Airbnb Market Intelligence",
    page_icon="🏠",
    layout="wide"
)

# 
# LOAD DATA

@st.cache_data
def load_data():
    master = pd.read_csv('data/processed/master_listings.csv', low_memory=False)
    neighbourhood_agg = pd.read_csv('data/processed/neighbourhood_agg.csv')
    return master, neighbourhood_agg

master, neighbourhood_agg = load_data()

# 
# HEADER

st.title("🏠 Bangkok Airbnb Market Intelligence Dashboard")
st.markdown("---")

# 
# KPI METRICS

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Listings", f"{master.shape[0]:,}")
with col2:
    st.metric("Avg Nightly Price", f"{master['price_clean'].mean():.0f} THB")
with col3:
    st.metric("Avg Occupancy Rate", f"{master['occupancy_rate'].mean():.1f}%")
with col4:
    st.metric("Total Hosts", f"{master['host_id'].nunique():,}")
with col5:
    st.metric("Neighbourhoods", f"{master['neighbourhood_cleansed'].nunique()}")

st.markdown("---")

# 
# SIDEBAR FILTERS

st.sidebar.title("Filters")

# Room type filter
room_types = ['All'] + master['room_type'].unique().tolist()
selected_room = st.sidebar.selectbox("Room Type", room_types)

# Neighbourhood filter
neighbourhoods = ['All'] + sorted(master['neighbourhood_cleansed'].unique().tolist())
selected_neighbourhood = st.sidebar.selectbox("Neighbourhood", neighbourhoods)

# Price range filter
min_price = int(master['price_clean'].min())
max_price = int(master['price_clean'].quantile(0.95))
price_range = st.sidebar.slider(
    "Price Range (THB)",
    min_price, max_price,
    (min_price, max_price)
)

# Superhost filter
superhost_filter = st.sidebar.checkbox("Superhosts Only")

# Apply filters
filtered = master.copy()
if selected_room != 'All':
    filtered = filtered[filtered['room_type'] == selected_room]
if selected_neighbourhood != 'All':
    filtered = filtered[filtered['neighbourhood_cleansed'] == selected_neighbourhood]
filtered = filtered[
    (filtered['price_clean'] >= price_range[0]) &
    (filtered['price_clean'] <= price_range[1])
]
if superhost_filter:
    filtered = filtered[filtered['host_is_superhost'] == True]

st.sidebar.markdown(f"**Showing: {filtered.shape[0]:,} listings**")

# 
# ROW 1: PRICE ANALYSIS

st.subheader("Price Analysis")
col1, col2 = st.columns(2)

with col1:
    # Top 10 neighbourhoods by avg price
    top_price = filtered.groupby('neighbourhood_cleansed')['price_clean'].mean()\
        .nlargest(10).reset_index()
    fig1 = px.bar(
        top_price,
        x='price_clean',
        y='neighbourhood_cleansed',
        orientation='h',
        title='Top 10 Neighbourhoods by Average Price',
        labels={'price_clean': 'Avg Price (THB)', 'neighbourhood_cleansed': 'Neighbourhood'},
        color='price_clean',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Price by room type
    room_price = filtered.groupby('room_type')['price_clean'].mean().reset_index()
    fig2 = px.bar(
        room_price,
        x='room_type',
        y='price_clean',
        title='Average Price by Room Type',
        labels={'price_clean': 'Avg Price (THB)', 'room_type': 'Room Type'},
        color='price_clean',
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig2, use_container_width=True)

# 
# ROW 2: OCCUPANCY & MAP

st.subheader("Geographic & Occupancy Analysis")
col1, col2 = st.columns(2)

with col1:
    # Map
    fig3 = px.scatter_mapbox(
        filtered.dropna(subset=['latitude', 'longitude']).head(2000),
        lat='latitude',
        lon='longitude',
        color='price_clean',
        size='occupancy_rate',
        hover_name='name',
        hover_data=['price_clean', 'room_type', 'neighbourhood_cleansed'],
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        zoom=10,
        title='Listing Map - Size=Occupancy, Color=Price'
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Occupancy by neighbourhood
    top_occ = filtered.groupby('neighbourhood_cleansed')['occupancy_rate'].mean()\
        .nlargest(10).reset_index()
    fig4 = px.bar(
        top_occ,
        x='occupancy_rate',
        y='neighbourhood_cleansed',
        orientation='h',
        title='Top 10 Neighbourhoods by Occupancy Rate',
        labels={'occupancy_rate': 'Avg Occupancy (%)', 'neighbourhood_cleansed': 'Neighbourhood'},
        color='occupancy_rate',
        color_continuous_scale='Oranges'
    )
    st.plotly_chart(fig4, use_container_width=True)

# 
# ROW 3: HOST & REVIEW ANALYSIS

st.subheader("Host & Review Analysis")
col1, col2 = st.columns(2)

with col1:
    # Superhost comparison
    superhost_data = filtered.groupby('host_is_superhost').agg(
        avg_price=('price_clean', 'mean'),
        avg_occupancy=('occupancy_rate', 'mean'),
        avg_rating=('review_scores_rating', 'mean')
    ).reset_index()
    superhost_data['host_type'] = superhost_data['host_is_superhost'].map(
        {True: 'Superhost', False: 'Regular Host'}
    )
    fig5 = px.bar(
        superhost_data.dropna(),
        x='host_type',
        y='avg_occupancy',
        title='Superhost vs Regular Host - Avg Occupancy',
        labels={'avg_occupancy': 'Avg Occupancy (%)', 'host_type': 'Host Type'},
        color='host_type',
        color_discrete_map={'Superhost': '#FF5A5F', 'Regular Host': '#00A699'}
    )
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    # Review scores distribution
    fig6 = px.histogram(
        filtered.dropna(subset=['review_scores_rating']),
        x='review_scores_rating',
        title='Review Scores Distribution',
        labels={'review_scores_rating': 'Review Score', 'count': 'Count'},
        color_discrete_sequence=['#FF5A5F'],
        nbins=20
    )
    st.plotly_chart(fig6, use_container_width=True)

# 
# ROW 4: DATA TABLE

st.subheader("Listings Data Explorer")
st.dataframe(
    filtered[[
        'name', 'neighbourhood_cleansed', 'room_type',
        'price_clean', 'occupancy_rate', 'review_scores_rating',
        'host_is_superhost', 'instant_bookable'
    ]].head(100),
    use_container_width=True
)

st.markdown("---")
st.markdown("**Built by:** Hansika Dulanjani | **Data:** Inside Airbnb Bangkok | **Tool:** Streamlit + Plotly")