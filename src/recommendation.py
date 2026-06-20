import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import sys

sys.stdout = open('docs/recommendation_report.txt', 'w', encoding='utf-8')

print("BANGKOK AIRBNB - LISTING RECOMMENDATION SYSTEM")
print("=" * 60)

# Load data
master = pd.read_csv('data/processed/master_listings.csv', low_memory=False)
print(f"Dataset loaded: {master.shape[0]:,} listings")


# CONTENT-BASED FILTERING


print("\nBuilding content-based recommendation system...")

# Use subset for speed
df = master[['id', 'name', 'neighbourhood_cleansed', 'room_type',
             'price_clean', 'review_scores_rating', 'occupancy_rate',
             'accommodates', 'bedrooms', 'amenities']].dropna(subset=['name'])

# 1. TEXT FEATURES - combine name and amenities
df['text_features'] = (
    df['name'].fillna('') + ' ' +
    df['neighbourhood_cleansed'].fillna('') + ' ' +
    df['room_type'].fillna('') + ' ' +
    df['amenities'].fillna('')
)

# 2. TF-IDF on text features
print("Computing TF-IDF vectors...")
tfidf = TfidfVectorizer(max_features=500, stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['text_features'])

# 3. NUMERICAL FEATURES
scaler = MinMaxScaler()
numerical_features = df[['price_clean', 'review_scores_rating',
                          'occupancy_rate', 'accommodates']].fillna(0)
numerical_scaled = scaler.fit_transform(numerical_features)

# 4. COMBINE TEXT + NUMERICAL (70% text, 30% numerical)
from scipy.sparse import hstack, csr_matrix
combined_features = hstack([
    tfidf_matrix * 0.7,
    csr_matrix(numerical_scaled) * 0.3
])

print("Computing similarity matrix...")
# Use sample of 2000 for speed
sample_size = 2000
similarity_matrix = cosine_similarity(
    combined_features[:sample_size],
    combined_features[:sample_size]
)

df_sample = df.iloc[:sample_size].reset_index(drop=True)



# RECOMMENDATION FUNCTION


def recommend_listings(listing_id, n=5):
    """Get top N similar listings for a given listing ID"""
    try:
        idx = df_sample[df_sample['id'] == listing_id].index[0]
        sim_scores = list(enumerate(similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]  # exclude itself

        recommendations = []
        for i, score in sim_scores:
            rec = df_sample.iloc[i]
            recommendations.append({
                'listing_id': rec['id'],
                'name': rec['name'][:50],
                'neighbourhood': rec['neighbourhood_cleansed'],
                'room_type': rec['room_type'],
                'price_thb': rec['price_clean'],
                'rating': rec['review_scores_rating'],
                'similarity_score': round(score, 4)
            })
        return recommendations
    except:
        return []



# TEST RECOMMENDATIONS
 


print("\nTESTING RECOMMENDATION SYSTEM:")
print("-" * 50)

# Test with first 3 listings
test_listings = df_sample.head(3)

for _, listing in test_listings.iterrows():
    print(f"\nSource Listing:")
    print(f"  ID:            {listing['id']}")
    print(f"  Name:          {listing['name'][:50]}")
    print(f"  Neighbourhood: {listing['neighbourhood_cleansed']}")
    print(f"  Room Type:     {listing['room_type']}")
    print(f"  Price:         {listing['price_clean']:.0f} THB")
    print(f"  Rating:        {listing['review_scores_rating']:.2f}")

    recommendations = recommend_listings(listing['id'])
    print(f"\n  Top 5 Similar Listings:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec['name']}")
        print(f"     Neighbourhood: {rec['neighbourhood']} | "
              f"Price: {rec['price_thb']:.0f} THB | "
              f"Rating: {rec['rating']:.2f} | "
              f"Similarity: {rec['similarity_score']}")



# SYSTEM SUMMARY


print("\n\nRECOMMENDATION SYSTEM SUMMARY:")
print("-" * 50)
print(f"Total listings indexed:     {len(df_sample):,}")
print(f"Feature dimensions:         {combined_features.shape[1]}")
print(f"Text weight:                70%")
print(f"Numerical weight:           30%")
print(f"Algorithm:                  Content-Based TF-IDF + Cosine Similarity")
print(f"Features used:              name, amenities, neighbourhood,")
print(f"                            room_type, price, rating, occupancy")

sys.stdout.close()
sys.stdout = sys.__stdout__
print("Recommendation report saved to docs/recommendation_report.txt")