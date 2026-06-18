import pandas as pd
import sys

sys.stdout = open('docs/schema_analysis.txt', 'w')

print("Loading datasets...")
listings = pd.read_csv("data/raw/listings.csv")
calendar = pd.read_csv("data/raw/calendar.csv")
reviews = pd.read_csv("data/raw/reviews.csv")
print("Datasets loaded!\n")

# 1. DATA TYPES
print("LISTINGS - DATA TYPES:\n")
print(listings.dtypes)

print("\n\nCALENDAR - DATA TYPES:\n")
print(calendar.dtypes)

print("\n\nREVIEWS - DATA TYPES:\n")
print(reviews.dtypes)

# 2. PRIMARY & FOREIGN KEYS
print("\n\nKEY RELATIONSHIPS:\n")
print("Listings.id         -> PRIMARY KEY")
print("Calendar.listing_id -> FOREIGN KEY -> Listings.id")
print("Reviews.listing_id  -> FOREIGN KEY -> Listings.id")

cal_match = calendar['listing_id'].isin(listings['id']).sum()
rev_match = reviews['listing_id'].isin(listings['id']).sum()

print(f"\nCalendar rows matching listings: {cal_match:,} / {len(calendar):,}")
print(f"Reviews rows matching listings:  {rev_match:,} / {len(reviews):,}")

# 3. UNIQUE VALUE COUNTS
print("\n\nUNIQUE VALUES:\n")
print(f"Unique listings (id):              {listings['id'].nunique():,}")
print(f"Unique hosts:                      {listings['host_id'].nunique():,}")
print(f"Unique neighbourhoods:             {listings['neighbourhood_cleansed'].nunique():,}")
print(f"Unique room types:                 {listings['room_type'].nunique():,}")
print(f"Room types:                        {listings['room_type'].unique().tolist()}")
print(f"\nUnique listings in calendar:       {calendar['listing_id'].nunique():,}")
print(f"Date range in calendar:            {calendar['date'].min()} to {calendar['date'].max()}")
print(f"\nUnique listings in reviews:        {reviews['listing_id'].nunique():,}")
print(f"Date range in reviews:             {reviews['date'].min()} to {reviews['date'].max()}")

# 4. PRICE ANALYSIS
print("\n\nPRICE ANALYSIS (Listings):\n")
listings['price_clean'] = listings['price'].replace('[\$,]', '', regex=True).astype(float)
print(listings['price_clean'].describe())

# 5. NEIGHBOURHOOD DISTRIBUTION
print("\n\nTOP 10 NEIGHBOURHOODS BY LISTING COUNT:\n")
print(listings['neighbourhood_cleansed'].value_counts().head(10))

sys.stdout.close()
sys.stdout = sys.__stdout__
print("Schema analysis saved to docs/schema_analysis.txt")