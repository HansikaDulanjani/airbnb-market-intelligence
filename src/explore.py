import pandas as pd

import sys
sys.stdout = open('docs/exploration_report.txt', 'w')

# Load datasets
print("Loading datasets...")
listings = pd.read_csv("data/raw/listings.csv")
calendar = pd.read_csv("data/raw/calendar.csv")
reviews = pd.read_csv("data/raw/reviews.csv")

print("\nDatasets loaded successfully!")

# Shape of each dataset
print("\nDATASET SHAPES:")
print(f"Listings  -> {listings.shape[0]:,} rows x {listings.shape[1]} columns")
print(f"Calendar  -> {calendar.shape[0]:,} rows x {calendar.shape[1]} columns")
print(f"Reviews   -> {reviews.shape[0]:,} rows x {reviews.shape[1]} columns")

# Column names
print("\nLISTINGS COLUMNS:")
print(listings.columns.tolist())

print("\nCALENDAR COLUMNS:")
print(calendar.columns.tolist())

print("\nREVIEWS COLUMNS:")
print(reviews.columns.tolist())

# Data types and null analysis
print("\nLISTINGS - NULL COUNTS (top 20):")
print(listings.isnull().sum().sort_values(ascending=False).head(20))

print("\nCALENDAR - NULL COUNTS:")
print(calendar.isnull().sum())

print("\nREVIEWS - NULL COUNTS:")
print(reviews.isnull().sum())

# Sample values
print("\nLISTINGS - SAMPLE (first 2 rows):")
print(listings[['id','name','room_type','price','neighbourhood_cleansed','review_scores_rating']].head(2))

print("\nCALENDAR - SAMPLE (first 2 rows):")
print(calendar.head(2))

print("\nREVIEWS - SAMPLE (first 2 rows):")
print(reviews.head(2))

sys.stdout.close()