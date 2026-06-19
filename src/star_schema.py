import duckdb
import pandas as pd
import os

def build_star_schema():
    print("Building star schema in DuckDB...")

    # Load master table
    master = pd.read_csv('data/processed/master_listings.csv')
    calendar = pd.read_csv('data/processed/calendar_clean.csv')
    reviews = pd.read_csv('data/processed/reviews_clean.csv')

    # Connect to DuckDB
    os.makedirs('data/output', exist_ok=True)
    con = duckdb.connect('data/output/airbnb_bangkok.duckdb')

    # DIMENSION TABLE 1: dim_host
    
    print("Creating dim_host...")
    con.execute("""
        CREATE OR REPLACE TABLE dim_host AS
        SELECT DISTINCT
            host_id,
            host_name,
            host_since,
            host_is_superhost,
            host_response_time,
            host_response_rate,
            host_acceptance_rate,
            host_identity_verified,
            host_has_profile_pic,
            host_tenure_years,
            calculated_host_listings_count
        FROM master
    """)

    # DIMENSION TABLE 2: dim_property
    
    print("Creating dim_property...")
    con.execute("""
        CREATE OR REPLACE TABLE dim_property AS
        SELECT DISTINCT
            id AS listing_id,
            name,
            property_type,
            room_type,
            accommodates,
            bedrooms,
            beds,
            bathrooms_text,
            amenities
        FROM master
    """)

    # DIMENSION TABLE 3: dim_location
   
    print("Creating dim_location...")
    con.execute("""
        CREATE OR REPLACE TABLE dim_location AS
        SELECT DISTINCT
            neighbourhood_cleansed,
            latitude,
            longitude,
            median_price,
            listing_density,
            avg_rating
        FROM master
    """)

    # DIMENSION TABLE 4: dim_date
    
    print("Creating dim_date...")
    con.execute("""
        CREATE OR REPLACE TABLE dim_date AS
        SELECT DISTINCT
            date,
            YEAR(date::DATE) AS year,
            MONTH(date::DATE) AS month,
            DAY(date::DATE) AS day,
            DAYOFWEEK(date::DATE) AS day_of_week,
            QUARTER(date::DATE) AS quarter
        FROM calendar
    """)

    # FACT TABLE: fact_listings
    
    print("Creating fact_listings...")
    con.execute("""
        CREATE OR REPLACE TABLE fact_listings AS
        SELECT
            id AS listing_id,
            host_id,
            neighbourhood_cleansed,
            price_clean AS nightly_price,
            price_per_bedroom,
            availability_365,
            occupancy_rate,
            estimated_revenue,
            number_of_reviews,
            review_scores_rating,
            review_scores_cleanliness,
            review_scores_location,
            review_scores_value,
            instant_bookable,
            minimum_nights,
            maximum_nights,
            booked_days,
            available_days
        FROM master
    """)

    # FACT TABLE 2: fact_calendar
    
    print("Creating fact_calendar...")
    con.execute("""
        CREATE OR REPLACE TABLE fact_calendar AS
        SELECT
            listing_id,
            date,
            is_available,
            minimum_nights,
            maximum_nights
        FROM calendar
    """)

    # Show all tables
    print("\nTables created in DuckDB:")
    tables = con.execute("SHOW TABLES").fetchdf()
    print(tables)

    # Row counts
    print("\nRow counts:")
    for table in ['dim_host', 'dim_property', 'dim_location', 
                  'dim_date', 'fact_listings', 'fact_calendar']:
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table:20} -> {count:,} rows")

    con.close()
    print("\nStar schema saved to data/output/airbnb_bangkok.duckdb")

if __name__ == "__main__":
    build_star_schema()