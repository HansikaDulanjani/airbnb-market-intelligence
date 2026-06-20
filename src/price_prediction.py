import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import sys

sys.stdout = open('docs/price_prediction_report.txt', 'w', encoding='utf-8')

print("BANGKOK AIRBNB - PRICE PREDICTION MODEL")
print("=" * 60)

# Load data
master = pd.read_csv('data/processed/master_listings.csv', low_memory=False)
print(f"Dataset loaded: {master.shape[0]:,} listings")

#
# FEATURE ENGINEERING

print("\nPreparing features...")

features = [
    'room_type', 'neighbourhood_cleansed', 'accommodates',
    'bedrooms', 'beds', 'review_scores_rating',
    'review_scores_cleanliness', 'review_scores_location',
    'host_is_superhost', 'host_tenure_years',
    'instant_bookable', 'minimum_nights', 'availability_365'
]

target = 'price_clean'

# Select and clean
df = master[features + [target]].dropna()
print(f"Clean dataset: {df.shape[0]:,} rows")

# Encode categorical columns
le_room = LabelEncoder()
le_neighbourhood = LabelEncoder()

df['room_type_encoded'] = le_room.fit_transform(df['room_type'])
df['neighbourhood_encoded'] = le_neighbourhood.fit_transform(
    df['neighbourhood_cleansed']
)
df['superhost_encoded'] = df['host_is_superhost'].astype(int)
df['instant_encoded'] = df['instant_bookable'].astype(int)

# Final features
X_features = [
    'room_type_encoded', 'neighbourhood_encoded', 'accommodates',
    'bedrooms', 'beds', 'review_scores_rating',
    'review_scores_cleanliness', 'review_scores_location',
    'superhost_encoded', 'host_tenure_years',
    'instant_encoded', 'minimum_nights', 'availability_365'
]

X = df[X_features]
y = df[target]

#
# TRAIN/TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTraining set: {X_train.shape[0]:,} rows")
print(f"Testing set:  {X_test.shape[0]:,} rows")

#
# MODELS


models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(
        n_estimators=100, random_state=42, n_jobs=-1
    ),
    'Gradient Boosting': GradientBoostingRegressor(
        n_estimators=100, random_state=42
    )
}

results = {}

print("\nTraining models...")
for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    results[name] = {
        'MAE': mae,
        'RMSE': rmse,
        'R2': r2,
        'model': model
    }

    print(f"  MAE:  {mae:.2f} THB")
    print(f"  RMSE: {rmse:.2f} THB")
    print(f"  R2:   {r2:.4f}")

# 
# BEST MODEL - FEATURE IMPORTANCE


print("\n\nMODEL COMPARISON:")
print("-" * 50)
for name, result in results.items():
    print(f"{name:25} MAE: {result['MAE']:.2f} | "
          f"RMSE: {result['RMSE']:.2f} | "
          f"R2: {result['R2']:.4f}")

# Feature importance from Random Forest
print("\n\nFEATURE IMPORTANCE (Random Forest):")
print("-" * 50)
rf_model = results['Random Forest']['model']
importance_df = pd.DataFrame({
    'feature': X_features,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

for _, row in importance_df.iterrows():
    bar = '█' * int(row['importance'] * 100)
    print(f"{row['feature']:35} {row['importance']:.4f} {bar}")


# 
# SAMPLE PREDICTIONS


print("\n\nSAMPLE PRICE PREDICTIONS (Random Forest):")
print("-" * 50)

sample_listings = X_test.head(5)
actual_prices = y_test.head(5).values
predicted_prices = rf_model.predict(sample_listings)

for i, (actual, predicted) in enumerate(zip(actual_prices, predicted_prices)):
    diff = abs(actual - predicted)
    print(f"Listing {i+1}: Actual={actual:.0f} THB | "
          f"Predicted={predicted:.0f} THB | "
          f"Difference={diff:.0f} THB")

print("\n\nMODEL SUMMARY:")
print("-" * 50)
best_model = min(results, key=lambda x: results[x]['MAE'])
print(f"Best Model: {best_model}")
print(f"MAE:  {results[best_model]['MAE']:.2f} THB")
print(f"RMSE: {results[best_model]['RMSE']:.2f} THB")
print(f"R2:   {results[best_model]['R2']:.4f}")
print(f"\nInterpretation: The model predicts nightly price")
print(f"within +/- {results[best_model]['MAE']:.0f} THB on average")

sys.stdout.close()
sys.stdout = sys.__stdout__
print("Price prediction report saved to docs/price_prediction_report.txt")