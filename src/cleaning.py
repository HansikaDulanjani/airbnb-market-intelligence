import pandas as pd
import os
import sys
from ingestion import load_datasets

def clean_listings(listings):
    print("Cleaning listings...")
    df = listings.copy()

    # 1. CLEAN PRICE - remove $ and commas, cast to float
    df['price_clean'] = df['price'].replace(
        '[\$,]', '', regex=True).astype(float)

    # 2. REMOVE EXTREME PRICE OUTLIERS
    before = len(df)
    df = df[df['price_clean'] <= 50000]  # max 50,000 THB/night
    df = df[df['price_clean'] >= 100]    # min 100 THB/night
    after = len(df)
    print(f"Removed {before - after:,} extreme price outliers")

    # 3. PARSE DATE FIELDS
    df['last_scraped'] = pd.to_datetime(df['last_scraped'])
    df['host_since'] = pd.to_datetime(df['host_since'])
    df['first_review'] = pd.to_datetime(df['first_review'])
    df['last_review'] = pd.to_datetime(df['last_review'])

    # 4. HOST TENURE (years on platform)
    df['host_tenure_years'] = (
        pd.Timestamp('2025-09-27') - df['host_since']
    ).dt.days / 365.25

    # 5. CLEAN RESPONSE RATE
    df['host_response_rate'] = df['host_response_rate'].replace(
        '%', '', regex=True).astype(float)
    df['host_acceptance_rate'] = df['host_acceptance_rate'].replace(
        '%', '', regex=True).astype(float)

    # 6. BOOLEAN FIELDS
    df['host_is_superhost'] = df['host_is_superhost'].map(
        {'t': True, 'f': False})
    df['instant_bookable'] = df['instant_bookable'].map(
        {'t': True, 'f': False})
    df['host_has_profile_pic'] = df['host_has_profile_pic'].map(
        {'t': True, 'f': False})
    df['host_identity_verified'] = df['host_identity_verified'].map(
        {'t': True, 'f': False})

    # 7. FILL MISSING REVIEW SCORES WITH MEDIAN
    review_cols = [
        'review_scores_rating', 'review_scores_accuracy',
        'review_scores_cleanliness', 'review_scores_checkin',
        'review_scores_communication', 'review_scores_location',
        'review_scores_value'
    ]
    for col in review_cols:
        median = df[col].median()
        df[col] = df[col].fillna(median)

    # 8. FILL MISSING BEDROOMS/BEDS WITH MEDIAN
    df['bedrooms'] = df['bedrooms'].fillna(df['bedrooms'].median())
    df['beds'] = df['beds'].fillna(df['beds'].median())

    # 9. PRICE PER BEDROOM
    df['price_per_bedroom'] = df['price_clean'] / df['bedrooms'].replace(0, 1)

    # 10. STANDARDIZE NEIGHBOURHOOD
    df['neighbourhood_cleansed'] = df['neighbourhood_cleansed'].str.strip().str.title()

    print(f"Listings cleaned -> {df.shape[0]:,} rows remaining")
    return df


def clean_calendar(calendar):
    print("Cleaning calendar...")
    df = calendar.copy()

    # 1. PARSE DATE
    df['date'] = pd.to_datetime(df['date'])

    # 2. CONVERT AVAILABLE TO BOOLEAN
    df['is_available'] = df['available'].map({'t': True, 'f': False})

    # 3. DROP NULL PRICE COLUMNS (100% null)
    df = df.drop(columns=['price', 'adjusted_price'])

    print(f"Calendar cleaned -> {df.shape[0]:,} rows")
    return df


def clean_reviews(reviews):
    print("Cleaning reviews...")
    df = reviews.copy()

    # 1. PARSE DATE
    df['date'] = pd.to_datetime(df['date'])

    # 2. DROP NULL COMMENTS
    df = df.dropna(subset=['comments'])

    # 3. EXTRACT YEAR AND MONTH
    df['review_year'] = df['date'].dt.year
    df['review_month'] = df['date'].dt.month

    print(f"Reviews cleaned -> {df.shape[0]:,} rows remaining")
    return df


if __name__ == "__main__":
    listings, calendar, reviews = load_datasets()

    listings_clean = clean_listings(listings)
    calendar_clean = clean_calendar(calendar)
    reviews_clean = clean_reviews(reviews)

    # SAVE CLEANED DATA
    os.makedirs('data/processed', exist_ok=True)
    listings_clean.to_csv('data/processed/listings_clean.csv', index=False)
    calendar_clean.to_csv('data/processed/calendar_clean.csv', index=False)
    reviews_clean.to_csv('data/processed/reviews_clean.csv', index=False)

    print("\nAll cleaned datasets saved to data/processed/")
    print(f"Listings clean:  {listings_clean.shape[0]:,} rows x {listings_clean.shape[1]} columns")
    print(f"Calendar clean:  {calendar_clean.shape[0]:,} rows x {calendar_clean.shape[1]} columns")
    print(f"Reviews clean:   {reviews_clean.shape[0]:,} rows x {reviews_clean.shape[1]} columns")