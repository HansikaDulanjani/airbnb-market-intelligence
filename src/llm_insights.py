import anthropic
import pandas as pd
import json
import sys

# Load our analysis results
master = pd.read_csv('data/processed/master_listings.csv')
neighbourhood_agg = pd.read_csv('data/processed/neighbourhood_agg.csv')

# Build context from our data
def build_context():
    context = f"""
You are a Bangkok Airbnb Market Intelligence Assistant.
Here is the current market data:

MARKET OVERVIEW:
- Total listings: {master.shape[0]:,}
- Average nightly price: {master['price_clean'].mean():.0f} THB
- Median nightly price: {master['price_clean'].median():.0f} THB
- Average occupancy rate: {master['occupancy_rate'].mean():.1f}%
- Total unique hosts: {master['host_id'].nunique():,}
- Superhost count: {master[master['host_is_superhost']==True].shape[0]:,}

ROOM TYPE BREAKDOWN:
{master['room_type'].value_counts().to_string()}

TOP 5 NEIGHBOURHOODS BY PRICE:
{neighbourhood_agg.nlargest(5, 'median_price')[['neighbourhood_cleansed','median_price','listing_density','avg_rating']].to_string()}

TOP 5 NEIGHBOURHOODS BY LISTINGS:
{neighbourhood_agg.nlargest(5, 'listing_density')[['neighbourhood_cleansed','listing_density','median_price']].to_string()}

HYPOTHESIS TEST RESULTS:
- Superhosts charge significantly different prices (p=0.000044)
- Entire homes have significantly higher occupancy than private rooms (p<0.001)
- Weak positive correlation between price and review scores (r=0.057, p<0.001)
- Instant bookable listings do NOT have higher occupancy (p=0.000031)
- Significant price differences exist across neighbourhoods (p<0.001)

SENTIMENT ANALYSIS:
- 81.96% of reviews are Positive
- 3.87% of reviews are Negative
- Average sentiment score: 0.6688 (strongly positive)
- Sentiment declining over years (guests becoming more critical)
"""
    return context

def ask_claude(question, context):
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"{context}\n\nQuestion: {question}"
            }
        ]
    )
    return message.content[0].text

# Generate insights
context = build_context()

questions = [
    "What are the top 3 investment opportunities in Bangkok Airbnb market?",
    "Which neighbourhood would you recommend for a new host wanting maximum occupancy?",
    "What does the sentiment trend tell us about the Bangkok Airbnb market health?",
    "How should a host price their entire home listing in Vadhana neighbourhood?",
    "What are the key risks and limitations of this dataset for business decisions?"
]

sys.stdout = open('docs/llm_insights_report.txt', 'w', encoding='utf-8')

print("BANGKOK AIRBNB - LLM POWERED INSIGHTS")
print("=" * 60)
print("Model: Claude Sonnet (claude-sonnet-4-6)")
print("Data: Inside Airbnb Bangkok Dataset")
print("=" * 60)

for i, question in enumerate(questions, 1):
    print(f"\nQ{i}: {question}")
    print("-" * 50)
    answer = ask_claude(question, context)
    print(f"A{i}: {answer}")
    print()

sys.stdout.close()
sys.stdout = sys.__stdout__
print("LLM insights saved to docs/llm_insights_report.txt")