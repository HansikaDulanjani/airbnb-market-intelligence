import duckdb
import sys

sys.stdout = open('docs/sql_queries_report.txt', 'w', encoding='utf-8')

con = duckdb.connect('data/output/airbnb_bangkok.duckdb')

print("BANGKOK AIRBNB - KEY ANALYTICAL SQL QUERIES")
print("=" * 60)

# QUERY 1: Top 10 neighbourhoods by average price
print("\nQUERY 1: Top 10 Neighbourhoods by Average Nightly Price\n")
print(con.execute("""
    SELECT 
        neighbourhood_cleansed,
        COUNT(*) as total_listings,
        ROUND(AVG(nightly_price), 2) as avg_price_thb,
        ROUND(MEDIAN(nightly_price), 2) as median_price_thb
    FROM fact_listings
    GROUP BY neighbourhood_cleansed
    ORDER BY avg_price_thb DESC
    LIMIT 10
""").df().to_string())

# QUERY 2: Room type analysis
print("\n\nQUERY 2: Room Type Distribution & Pricing\n")
print(con.execute("""
    SELECT 
        p.room_type,
        COUNT(*) as total_listings,
        ROUND(AVG(f.nightly_price), 2) as avg_price_thb,
        ROUND(AVG(f.occupancy_rate), 2) as avg_occupancy_rate,
        ROUND(AVG(f.review_scores_rating), 2) as avg_rating
    FROM fact_listings f
    JOIN dim_property p ON f.listing_id = p.listing_id
    GROUP BY p.room_type
    ORDER BY total_listings DESC
""").df().to_string())

# QUERY 3: Superhost vs non-superhost
print("\n\nQUERY 3: Superhost vs Non-Superhost Performance\n")
print(con.execute("""
    SELECT 
        h.host_is_superhost,
        COUNT(*) as total_listings,
        ROUND(AVG(f.nightly_price), 2) as avg_price,
        ROUND(AVG(f.review_scores_rating), 2) as avg_rating,
        ROUND(AVG(f.occupancy_rate), 2) as avg_occupancy
    FROM fact_listings f
    JOIN dim_host h ON f.host_id = h.host_id
    GROUP BY h.host_is_superhost
""").df().to_string())

# QUERY 4: Top 10 hosts by listings
print("\n\nQUERY 4: Top 10 Hosts by Number of Listings\n")
print(con.execute("""
    SELECT 
        h.host_name,
        h.host_is_superhost,
        COUNT(*) as total_listings,
        ROUND(AVG(f.nightly_price), 2) as avg_price,
        ROUND(AVG(f.review_scores_rating), 2) as avg_rating
    FROM fact_listings f
    JOIN dim_host h ON f.host_id = h.host_id
    GROUP BY h.host_name, h.host_is_superhost
    ORDER BY total_listings DESC
    LIMIT 10
""").df().to_string())

# QUERY 5: Monthly availability trend
print("\n\nQUERY 5: Monthly Availability Trend\n")
print(con.execute("""
    SELECT 
        d.year,
        d.month,
        COUNT(*) as total_days,
        SUM(CASE WHEN f.is_available THEN 1 ELSE 0 END) as available_days,
        ROUND(SUM(CASE WHEN f.is_available THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as availability_pct
    FROM fact_calendar f
    JOIN dim_date d ON f.date = d.date
    GROUP BY d.year, d.month
    ORDER BY d.year, d.month
""").df().to_string())

# QUERY 6: Revenue estimate by neighbourhood
print("\n\nQUERY 6: Estimated Revenue by Neighbourhood\n")
print(con.execute("""
    SELECT 
        neighbourhood_cleansed,
        COUNT(*) as listings,
        ROUND(SUM(estimated_revenue), 2) as total_revenue_thb,
        ROUND(AVG(estimated_revenue), 2) as avg_revenue_per_listing
    FROM fact_listings
    WHERE estimated_revenue IS NOT NULL
    GROUP BY neighbourhood_cleansed
    ORDER BY total_revenue_thb DESC
    LIMIT 10
""").df().to_string())

con.close()
sys.stdout.close()
sys.stdout = sys.__stdout__
print("SQL queries report saved to docs/sql_queries_report.txt")