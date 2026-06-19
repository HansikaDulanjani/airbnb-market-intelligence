import pandas as pd
import os

def load_cleaned():
    print("Loading cleaned datasets...")
    listings = pd.read_csv('data/processed/listings_clean.csv')
    calendar = pd.read_csv('data/processed/calendar_clean.csv')
    reviews = pd.read_csv('data/processed/reviews_clean.csv')
    print(f"Listings: {listings.shape[0]:,} rows")
    print(f"Calendar: {calendar.shape[0]:,} rows")
    print(f"Reviews:  {reviews.shape[0]:,} rows")
    return listings, calendar, reviews

def enrich_listings(listings, calendar, reviews):
    print("\nEnriching listings...")

    # 1. REVIEW SUMMARY PER LISTING
    review_summary = reviews.groupby('listing_id').agg(
        total_reviews     = ('id', 'count'),
        latest_review     = ('date', 'max'),
        earliest_review   = ('date', 'min'),
        review_frequency  = ('review_year', 'nunique')
    ).reset_index()

    # 2. CALENDAR OCCUPANCY PER LISTING
    occupancy = calendar.groupby('listing_id').agg(
        total_days        = ('is_available', 'count'),
        available_days    = ('is_available', 'sum'),
    ).reset_index()
    occupancy['booked_days'] = occupancy['total_days'] - occupancy['available_days']
    occupancy['occupancy_rate'] = (
        occupancy['booked_days'] / occupancy['total_days'] * 100
    ).round(2)

    # 3. NEIGHBOURHOOD AGGREGATES
    neighbourhood_agg = listings.groupby('neighbourhood_cleansed').agg(
        median_price      = ('price_clean', 'median'),
        listing_density   = ('id', 'count'),
        avg_rating        = ('review_scores_rating', 'mean')
    ).reset_index()

    # 4. JOIN EVERYTHING TO LISTINGS
    master = listings.merge(
        review_summary, left_on='id', right_on='listing_id', how='left'
    )
    master = master.merge(
        occupancy, left_on='id', right_on='listing_id', how='left'
    )
    master = master.merge(
        neighbourhood_agg, on='neighbourhood_cleansed', how='left'
    )

    # 5. ESTIMATED REVENUE
    master['estimated_revenue'] = (
        master['booked_days'] * master['price_clean']
    )

    print(f"Master table created -> {master.shape[0]:,} rows x {master.shape[1]} columns")
    return master, neighbourhood_agg

if __name__ == "__main__":
    listings, calendar, reviews = load_cleaned()
    master, neighbourhood_agg = enrich_listings(listings, calendar, reviews)

    os.makedirs('data/processed', exist_ok=True)
    master.to_csv('data/processed/master_listings.csv', index=False)
    neighbourhood_agg.to_csv('data/processed/neighbourhood_agg.csv', index=False)

    print("\nSaved:")
    print(f"master_listings.csv    -> {master.shape[0]:,} rows x {master.shape[1]} columns")
    print(f"neighbourhood_agg.csv  -> {neighbourhood_agg.shape[0]:,} rows")

    print("\nSample occupancy rates:")
    print(master[['id', 'neighbourhood_cleansed', 
                  'price_clean', 'occupancy_rate', 
                  'estimated_revenue']].head(10))