import pandas as pd
import sys
from ingestion import load_datasets

sys.stdout = open('docs/profiling_report.txt', 'w')

listings, calendar, reviews = load_datasets()

# LISTINGS PROFILE
print("\nLISTINGS PROFILE:\n")
print(f"Total rows:         {listings.shape[0]:,}")
print(f"Total columns:      {listings.shape[1]}")
print(f"Duplicate rows:     {listings.duplicated().sum():,}")
print(f"Null values total:  {listings.isnull().sum().sum():,}")

print("\nNull % per column (only columns with nulls):")
null_pct = (listings.isnull().sum() / len(listings) * 100)
print(null_pct[null_pct > 0].sort_values(ascending=False).round(2))

# CALENDAR PROFILE
print("\n\nCALENDAR PROFILE:\n")
print(f"Total rows:         {calendar.shape[0]:,}")
print(f"Total columns:      {calendar.shape[1]}")
print(f"Duplicate rows:     Skipped (too large for memory)")
print(f"Null values total:  {calendar.isnull().sum().sum():,}")
print(f"\nAvailability breakdown:")
print(calendar['available'].value_counts())

# REVIEWS PROFILE
print("\n\nREVIEWS PROFILE:\n")
print(f"Total rows:         {reviews.shape[0]:,}")
print(f"Total columns:      {reviews.shape[1]}")
print(f"Duplicate rows:     {reviews.duplicated().sum():,}")
print(f"Null values total:  {reviews.isnull().sum().sum():,}")
print(f"\nReviews per year:")
reviews['year'] = pd.to_datetime(reviews['date']).dt.year
print(reviews['year'].value_counts().sort_index())

sys.stdout.close()
sys.stdout = sys.__stdout__
print("Profiling report saved to docs/profiling_report.txt")