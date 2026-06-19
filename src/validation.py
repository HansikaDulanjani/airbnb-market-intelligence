import pandas as pd
import sys
from ingestion import load_datasets

sys.stdout = open('docs/validation_report.txt', 'w')

listings, calendar, reviews = load_datasets()

# 1. PRICE OUTLIERS

print("PRICE OUTLIER ANALYSIS:\n")
listings['price_clean'] = listings['price'].replace(
    '[\$,]', '', regex=True).astype(float)

price = listings['price_clean'].dropna()
Q1 = price.quantile(0.25)
Q3 = price.quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

print(f"Price Q1:              {Q1:,.2f} THB")
print(f"Price Q3:              {Q3:,.2f} THB")
print(f"IQR:                   {IQR:,.2f} THB")
print(f"Lower bound:           {lower:,.2f} THB")
print(f"Upper bound:           {upper:,.2f} THB")
print(f"Outliers below lower:  {(price < lower).sum():,}")
print(f"Outliers above upper:  {(price > upper).sum():,}")
print(f"Max price:             {price.max():,.2f} THB")
print(f"Min price:             {price.min():,.2f} THB")

# 2. NEGATIVE PRICE VALIDATION

print("\n\nDATA VALIDATION:\n")
neg_price = (price < 0).sum()
print(f"Negative prices:       {neg_price}")

# 3. LAT/LONG VALIDATION

invalid_lat = listings[
    (listings['latitude'] < 13.0) | 
    (listings['latitude'] > 14.0)
].shape[0]
invalid_lon = listings[
    (listings['longitude'] < 100.0) | 
    (listings['longitude'] > 101.0)
].shape[0]

print(f"Invalid latitudes:     {invalid_lat}")
print(f"Invalid longitudes:    {invalid_lon}")

# 4. AVAILABILITY OUTLIERS

print("\n\nAVAILABILITY OUTLIER ANALYSIS:\n")
print(f"Min availability_365:  {listings['availability_365'].min()}")
print(f"Max availability_365:  {listings['availability_365'].max()}")
print(f"Mean availability_365: {listings['availability_365'].mean():.2f}")
listings_over_365 = (listings['availability_365'] > 365).sum()
print(f"Listings over 365:     {listings_over_365}")

# 5. REVIEW COUNT OUTLIERS

print("\n\nREVIEW COUNT OUTLIER ANALYSIS:\n")
reviews_col = listings['number_of_reviews']
print(f"Min reviews:           {reviews_col.min()}")
print(f"Max reviews:           {reviews_col.max()}")
print(f"Mean reviews:          {reviews_col.mean():.2f}")
print(f"Listings with 0 reviews: {(reviews_col == 0).sum():,}")

sys.stdout.close()
sys.stdout = sys.__stdout__
print("Validation report saved to docs/validation_report.txt")