import pandas as pd
import numpy as np
from scipy import stats
import sys

sys.stdout = open('docs/hypothesis_tests_report.txt', 'w', encoding='utf-8')

print("BANGKOK AIRBNB - HYPOTHESIS TESTS")
print("=" * 60)

# Load master data
master = pd.read_csv('data/processed/master_listings.csv')
print(f"Dataset loaded: {master.shape[0]:,} rows\n")


# TEST 1: Superhost vs Non-Superhost Pricing

print("\nTEST 1: Do Superhosts charge higher prices?")
print("-" * 50)
print("H0: No difference in price between superhosts and non-superhosts")
print("H1: Superhosts charge significantly different prices")

superhost_price = master[master['host_is_superhost'] == True]['price_clean'].dropna()
non_superhost_price = master[master['host_is_superhost'] == False]['price_clean'].dropna()

t_stat, p_value = stats.mannwhitneyu(superhost_price, non_superhost_price, alternative='two-sided')

print(f"\nSuperhost avg price:     {superhost_price.mean():.2f} THB")
print(f"Non-superhost avg price: {non_superhost_price.mean():.2f} THB")
print(f"Test statistic:          {t_stat:.4f}")
print(f"P-value:                 {p_value:.6f}")
print(f"Result: {'REJECT H0' if p_value < 0.05 else 'FAIL TO REJECT H0'} (alpha=0.05)")
if p_value < 0.05:
    print("Conclusion: Significant price difference exists between superhosts and non-superhosts")
else:
    print("Conclusion: No significant price difference between superhosts and non-superhosts")


# TEST 2: Entire Home vs Private Room Occupancy

print("\n\nTEST 2: Do Entire homes have higher occupancy than Private rooms?")
print("-" * 50)
print("H0: No difference in occupancy between entire homes and private rooms")
print("H1: Entire homes have higher occupancy rates")

entire_home = master[master['room_type'] == 'Entire home/apt']['occupancy_rate'].dropna()
private_room = master[master['room_type'] == 'Private room']['occupancy_rate'].dropna()

t_stat2, p_value2 = stats.mannwhitneyu(entire_home, private_room, alternative='greater')

print(f"\nEntire home avg occupancy: {entire_home.mean():.2f}%")
print(f"Private room avg occupancy:{private_room.mean():.2f}%")
print(f"Test statistic:            {t_stat2:.4f}")
print(f"P-value:                   {p_value2:.6f}")
print(f"Result: {'REJECT H0' if p_value2 < 0.05 else 'FAIL TO REJECT H0'} (alpha=0.05)")
if p_value2 < 0.05:
    print("Conclusion: Entire homes have significantly higher occupancy than private rooms")
else:
    print("Conclusion: No significant occupancy difference between entire homes and private rooms")


# TEST 3: Price vs Review Score Correlation

print("\n\nTEST 3: Is there a correlation between price and review scores?")
print("-" * 50)
print("H0: No correlation between price and review scores")
print("H1: Significant correlation exists")

clean = master[['price_clean', 'review_scores_rating']].dropna()
corr, p_value3 = stats.spearmanr(clean['price_clean'], clean['review_scores_rating'])

print(f"\nSpearman correlation:    {corr:.4f}")
print(f"P-value:                 {p_value3:.6f}")
print(f"Result: {'REJECT H0' if p_value3 < 0.05 else 'FAIL TO REJECT H0'} (alpha=0.05)")
if p_value3 < 0.05:
    print(f"Conclusion: Significant {'positive' if corr > 0 else 'negative'} correlation between price and review scores")
else:
    print("Conclusion: No significant correlation between price and review scores")


# TEST 4: Instant Bookable vs Occupancy

print("\n\nTEST 4: Do instant bookable listings have higher occupancy?")
print("-" * 50)
print("H0: No difference in occupancy for instant bookable listings")
print("H1: Instant bookable listings have higher occupancy")

instant = master[master['instant_bookable'] == True]['occupancy_rate'].dropna()
non_instant = master[master['instant_bookable'] == False]['occupancy_rate'].dropna()

t_stat4, p_value4 = stats.mannwhitneyu(instant, non_instant, alternative='greater')

print(f"\nInstant bookable avg occupancy:     {instant.mean():.2f}%")
print(f"Non-instant bookable avg occupancy: {non_instant.mean():.2f}%")
print(f"Test statistic:                     {t_stat4:.4f}")
print(f"P-value:                            {p_value4:.6f}")
print(f"Result: {'REJECT H0' if p_value4 < 0.05 else 'FAIL TO REJECT H0'} (alpha=0.05)")
if p_value4 < 0.05:
    print("Conclusion: Instant bookable listings have significantly higher occupancy")
else:
    print("Conclusion: No significant occupancy advantage for instant bookable listings")


# TEST 5: Price Differences Across Neighbourhoods

print("\n\nTEST 5: Do neighbourhoods differ significantly in pricing?")
print("-" * 50)
print("H0: No price difference across neighbourhoods")
print("H1: At least one neighbourhood has significantly different prices")

# Get top 10 neighbourhoods by listing count
top_neighbourhoods = master['neighbourhood_cleansed'].value_counts().head(10).index
groups = [
    master[master['neighbourhood_cleansed'] == n]['price_clean'].dropna()
    for n in top_neighbourhoods
]

f_stat, p_value5 = stats.kruskal(*groups)

print(f"\nTop 10 neighbourhoods tested:")
for n in top_neighbourhoods:
    avg = master[master['neighbourhood_cleansed'] == n]['price_clean'].mean()
    print(f"  {n:30} avg price: {avg:.2f} THB")

print(f"\nKruskal-Wallis H statistic: {f_stat:.4f}")
print(f"P-value:                    {p_value5:.6f}")
print(f"Result: {'REJECT H0' if p_value5 < 0.05 else 'FAIL TO REJECT H0'} (alpha=0.05)")
if p_value5 < 0.05:
    print("Conclusion: Significant price differences exist across Bangkok neighbourhoods")
else:
    print("Conclusion: No significant price differences across neighbourhoods")

print("\n\nSUMMARY OF ALL HYPOTHESIS TESTS:")
print("-" * 50)
results = [
    ("Test 1: Superhost pricing", p_value),
    ("Test 2: Room type occupancy", p_value2),
    ("Test 3: Price-review correlation", p_value3),
    ("Test 4: Instant bookable occupancy", p_value4),
    ("Test 5: Neighbourhood pricing", p_value5),
]
for name, pval in results:
    result = "REJECT H0 (Significant)" if pval < 0.05 else "FAIL TO REJECT H0"
    print(f"{name:35} p={pval:.6f} -> {result}")

sys.stdout.close()
sys.stdout = sys.__stdout__
print("Hypothesis tests saved to docs/hypothesis_tests_report.txt")