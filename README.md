# Bangkok Airbnb Market Intelligence
**Data Engineer Intern Technical Assessment | Expernetic (Pvt) Ltd**

---

## About This Project

This project analyzes the Bangkok short-term rental market using publicly 
available Inside Airbnb data. I built an end-to-end data engineering pipeline 
covering ingestion, cleaning, enrichment, star schema modeling, statistical 
analysis, machine learning, NLP sentiment analysis, and an interactive dashboard.

**Dataset:** Bangkok, Thailand  
**Listings:** 28,806 | **Calendar Records:** 10.5 million | **Reviews:** 583,333  
**Data Source:** https://insideairbnb.com/get-the-data/

---

## How to Set Up

**1. Clone the repo**
```bash
git clone https://github.com/HansikaDulanjani/airbnb-market-intelligence.git
cd airbnb-market-intelligence
```

**2. Create virtual environment**
```bash
python -m venv venv
source venv/Scripts/activate   # Windows
pip install -r requirements.txt
```

**3. Download Bangkok dataset from Inside Airbnb**

Download these 3 files and extract into data/raw/:
- listings.csv.gz
- calendar.csv.gz
- reviews.csv.gz

**4. Run the full pipeline**
```bash
python src/pipeline.py
```

---

## Project Structure

The src/ folder contains all Python scripts:

- ingestion.py — loads raw CSV files
- profiling.py — generates data quality report
- validation.py — detects outliers and validates data
- cleaning.py — cleans and standardizes all datasets
- enrichment.py — joins datasets and creates master table
- star_schema.py — builds DuckDB star schema
- sql_queries.py — runs analytical SQL queries
- pipeline.py — runs everything end to end
- hypothesis_tests.py — statistical tests with effect sizes
- sentiment_analysis.py — VADER sentiment on reviews
- recommendation.py — content-based listing recommender
- price_prediction.py — price prediction with RF, GB, LR + SHAP
- llm_insights.py — LLM insight generation pipeline
- dashboard.py — Streamlit interactive dashboard
- auto_report.py — automated PDF report generator

The docs/ folder contains all analysis outputs and documentation.

The reports/ folder contains the final PDF report and Power BI dashboard.

---

## Run Individual Scripts

```bash
python src/hypothesis_tests.py    # statistical tests
python src/price_prediction.py    # ML price model
python src/sentiment_analysis.py  # sentiment analysis
python src/recommendation.py      # recommendations
python src/auto_report.py         # generate PDF report
streamlit run src/dashboard.py    # launch dashboard
```

---

## Technical Stack

For this project I used Python 3.11 as the primary language. 
Data processing was done with pandas and DuckDB. Statistical 
analysis used scipy and numpy. Machine learning models were built 
with scikit-learn and SHAP for explainability. NLP sentiment 
analysis used VADER. Visualizations were built in Power BI, 
Streamlit, and Plotly. The star schema database runs on DuckDB. 
All code is version controlled with Git and GitHub.

---

## Recommended Review Order


1. Start with the final PDF report in the reports/ folder — this 
   covers everything with business context and interpretations

2. Open the Power BI dashboard file (Bangkok_Airbnb_Analysis.pbix) 
   in reports/ to explore the interactive EDA visuals

3. Run the Streamlit dashboard locally using 
   streamlit run src/dashboard.py for the interactive web app

4. Read docs/engineering_decision_log.md to understand the key 
   technical decisions made throughout the project

5. Browse the src/ scripts starting from pipeline.py which 
   orchestrates the full end-to-end workflow

6. Check docs/hypothesis_tests_report.txt for detailed 
   statistical findings with effect sizes and confidence intervals

7. Check docs/price_prediction_report.txt for ML model results 
   including cross-validation and SHAP values
   
---

## Key Results

- Average nightly price in Bangkok: 2,141 THB (median 1,378 THB)
- Superhosts achieve 50% higher occupancy than regular hosts
- 81.96% of guest reviews are positive
- Price prediction MAE: 866 THB (Random Forest, 5-fold CV)
- Bedrooms is the strongest price driver (864 THB SHAP impact)
- Vadhana commands 87% price premium over budget neighbourhoods

---

## Sections Completed

Section 02 — Dataset Familiarization  
Section 03 — Data Engineering Pipeline  
Section 04 — Exploratory Data Analysis (Power BI)  
Section 05 — Statistical Hypothesis Testing  
Section 06 — Price Prediction Model  
Section 07 — Sentiment Analysis + Recommendations + LLM Pipeline  
Section 08 — Streamlit Dashboard + Automated PDF Report 

---

## Summary of Completed Work

**Section 02 — Dataset Familiarization**
Downloaded and explored Bangkok dataset (28,806 listings, 10.5M 
calendar records, 583,333 reviews). Documented schema, data types, 
primary/foreign key relationships, business context, assumptions, 
and dataset limitations.

**Section 03 — Data Engineering Pipeline**
Built a full modular pipeline covering ingestion, profiling, 
validation, cleaning, enrichment, and DuckDB star schema with 
4 dimension tables and 2 fact tables. Automated end-to-end 
pipeline with structured logging and metadata tracking.

**Section 04 — Exploratory Data Analysis**
Built a 5-page interactive Power BI dashboard covering price 
analysis, occupancy analysis, host analysis, review analysis, 
and geographic mapping with 13 visualizations total.

**Section 05 — Statistical Analysis**
Conducted 5 hypothesis tests using Mann-Whitney U and 
Kruskal-Wallis methods. Reported Cohen's d effect sizes and 
95% confidence intervals for all tests with business interpretations.

**Section 06 — Price Prediction**
Trained and compared 3 models (Linear Regression, Random Forest, 
Gradient Boosting) with 5-fold cross-validation and SHAP 
explainability. Best model achieved MAE of 866 THB.

**Section 07 — AI and ML Experiments**
Implemented VADER sentiment analysis on 10,000 reviews, 
content-based listing recommendation system using TF-IDF 
and cosine similarity, and LLM insight generation pipeline 
using Anthropic Claude API.

**Section 08 — Open Innovation**
Built an interactive Streamlit web dashboard with real-time 
filters and maps, and an automated PDF market intelligence 
report generator using ReportLab.

**Optional Deliverables Completed**
- Interactive Dashboard (Streamlit + Power BI)
- Architecture Diagram with tool annotations
- Automated Reporting system

---

## Summary of Incomplete Work

**Section 03.6 — Advanced Cloud-Native Topics**
Not implemented due to time constraints. Cloud architecture, 
Docker containerization, and CDC strategies are discussed as 
design proposals in the final report. These were deprioritized 
to maintain depth in core mandatory sections.

**Section 05.2/5.3 — Full Correlation Matrix and VIF Analysis**
Spearman correlation was computed for price vs review scores 
but a full correlation matrix and VIF multicollinearity checks 
were not implemented. These would be prioritized with more time.

**Section 06 — Hyperparameter Tuning**
Default hyperparameters were used for all models. GridSearchCV 
optimization was not performed due to time constraints and is 
documented as a future improvement.

**Section 07.2 — LLM Pipeline Execution**
The pipeline was fully implemented in src/llm_insights.py but 
could not be executed due to Anthropic API credit limitations. 
The code is production-ready and documented transparently 
in the final report.

**Section 07.1 — Topic Modeling and NER**
LDA topic modeling and named entity recognition were not 
implemented. Sentiment analysis was prioritized as it provided 
the most direct business value within the available time.

---

*Hansika Dulanjani | Expernetic Data Engineer Intern Assessment | June 2026*