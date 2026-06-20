import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys

sys.stdout = open('docs/sentiment_report.txt', 'w', encoding='utf-8')

print("BANGKOK AIRBNB - SENTIMENT ANALYSIS ON REVIEWS")
print("=" * 60)

# Load reviews
print("\nLoading reviews...")
reviews = pd.read_csv('data/processed/reviews_clean.csv')
print(f"Total reviews: {reviews.shape[0]:,}")

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Analyze sentiment on sample (10,000 reviews for speed)
print("\nAnalyzing sentiment on 10,000 reviews...")
sample = reviews.dropna(subset=['comments']).head(10000)

def get_sentiment(text):
    try:
        score = analyzer.polarity_scores(str(text))
        compound = score['compound']
        if compound >= 0.05:
            return compound, 'Positive'
        elif compound <= -0.05:
            return compound, 'Negative'
        else:
            return compound, 'Neutral'
    except:
        return 0, 'Neutral'

sample[['compound_score', 'sentiment']] = sample['comments'].apply(
    lambda x: pd.Series(get_sentiment(x))
)

# Results
print("\nSENTIMENT DISTRIBUTION:")
print(sample['sentiment'].value_counts())
print(f"\nPercentage breakdown:")
print((sample['sentiment'].value_counts(normalize=True) * 100).round(2))

print(f"\nAverage compound score: {sample['compound_score'].mean():.4f}")
print(f"Max score: {sample['compound_score'].max():.4f}")
print(f"Min score: {sample['compound_score'].min():.4f}")

# Most positive reviews
print("\n\nTOP 3 MOST POSITIVE REVIEWS:")
top_positive = sample.nlargest(3, 'compound_score')[['comments', 'compound_score']]
for i, row in top_positive.iterrows():
    print(f"\nScore: {row['compound_score']:.4f}")
    print(f"Review: {str(row['comments'])[:200]}...")

# Most negative reviews
print("\n\nTOP 3 MOST NEGATIVE REVIEWS:")
top_negative = sample.nsmallest(3, 'compound_score')[['comments', 'compound_score']]
for i, row in top_negative.iterrows():
    print(f"\nScore: {row['compound_score']:.4f}")
    print(f"Review: {str(row['comments'])[:200]}...")

# Sentiment by year
print("\n\nSENTIMENT BY YEAR:")
sentiment_year = sample.groupby('review_year')['compound_score'].mean().round(4)
print(sentiment_year)

# Save enriched reviews
sample.to_csv('data/processed/reviews_with_sentiment.csv', index=False)
print("\nSaved reviews with sentiment to data/processed/reviews_with_sentiment.csv")

sys.stdout.close()
sys.stdout = sys.__stdout__
print("Sentiment analysis saved to docs/sentiment_report.txt")