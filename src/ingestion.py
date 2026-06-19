import pandas as pd
import os
import sys

def load_datasets(data_path="data/raw"):
    """Load all raw datasets and return as dataframes"""
    
    print("Starting data ingestion pipeline...")
    print(f"Loading from: {data_path}")
    
    # Check files exist
    files = {
        'listings': os.path.join(data_path, 'listings.csv'),
        'calendar': os.path.join(data_path, 'calendar.csv'),
        'reviews': os.path.join(data_path, 'reviews.csv')
    }
    
    for name, path in files.items():
        if os.path.exists(path):
            size = os.path.getsize(path) / (1024*1024)
            print(f"Found {name}.csv -> {size:.1f} MB")
        else:
            print(f"ERROR: {name}.csv not found at {path}")
            sys.exit(1)
    
    # Load datasets
    print("\nLoading listings...")
    listings = pd.read_csv(files['listings'])
    print(f"Listings loaded -> {listings.shape[0]:,} rows x {listings.shape[1]} columns")
    
    print("Loading calendar...")
    calendar = pd.read_csv(files['calendar'])
    print(f"Calendar loaded -> {calendar.shape[0]:,} rows x {calendar.shape[1]} columns")
    
    print("Loading reviews...")
    reviews = pd.read_csv(files['reviews'])
    print(f"Reviews loaded  -> {reviews.shape[0]:,} rows x {reviews.shape[1]} columns")
    
    print("\nIngestion pipeline complete!")
    
    return listings, calendar, reviews

if __name__ == "__main__":
    listings, calendar, reviews = load_datasets()