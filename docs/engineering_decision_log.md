# Engineering Decision Log

## Bangkok Airbnb Market Intelligence Project

---

### Decision 1: City Selection — Bangkok, Thailand

**Options Considered:**
- New York (most documented, many references available)
- London (rich dataset, familiar market)
- Bangkok (large dataset, unique Southeast Asian market)

**Decision:** Bangkok

**Rationale:** Bangkok offered 28,806 listings and 10.5 million 
calendar records — a large enough dataset to demonstrate 
scalability while providing a less commonly analyzed market. 
This allowed for more original insights rather than reproducing 
well-known findings from New York or London datasets.

**Trade-offs Accepted:** Less reference material available online. 
Currency is THB requiring careful price interpretation.

---

### Decision 2: Python + DuckDB over PySpark or Cloud Tools

**Options Considered:**
- PySpark (scalable but complex setup)
- BigQuery (cloud-native but requires GCP account)
- PostgreSQL (full-featured but heavyweight)
- DuckDB (lightweight, fast, SQL-native)

**Decision:** Python (pandas) + DuckDB

**Rationale:** DuckDB provides SQL analytical capabilities without 
requiring a server setup. For a 603MB dataset on a single machine, 
DuckDB outperforms PostgreSQL in setup simplicity while maintaining 
full SQL compatibility. pandas handles transformation logic naturally 
in Python.

**Trade-offs Accepted:** Not cloud-native. Would require migration 
to BigQuery or Redshift for production at scale.

---

### Decision 3: Star Schema Design

**Options Considered:**
- Single flat table (simple but poor for analytics)
- Snowflake schema (normalized but complex joins)
- Star schema (balance of simplicity and analytical power)

**Decision:** Star Schema with 4 dimension tables and 2 fact tables

**Rationale:** Star schema optimizes for analytical query performance.
Dimension tables (dim_host, dim_property, dim_location, dim_date) 
allow clean slicing and dicing. Two fact tables separate listing-level 
metrics from daily calendar data, avoiding row explosion.

**Trade-offs Accepted:** Some denormalization exists. Slowly changing 
dimensions (SCDs) not implemented — host attributes are treated as 
current snapshots only.

---

### Decision 4: Price Outlier Removal Strategy

**Options Considered:**
- IQR method (statistical but aggressive)
- Z-score method (assumes normality)
- Domain-based thresholds (business-driven)
- Keep all data (no filtering)

**Decision:** Domain-based thresholds (100 THB min, 50,000 THB max)

**Rationale:** Airbnb Bangkok pricing context: 100 THB (~$3 USD) is 
below any realistic nightly rate; 50,000 THB (~$1,400 USD) covers 
luxury villas. IQR would have removed legitimate luxury listings. 
5,573 records (19.3%) removed as extreme outliers.

**Trade-offs Accepted:** Luxury segment (>50,000 THB) excluded from 
analysis. These represent <1% of listings but could skew averages.

---

### Decision 5: Non-Parametric Statistical Tests

**Options Considered:**
- T-tests (assumes normality)
- ANOVA (assumes normality and equal variance)
- Mann-Whitney U / Kruskal-Wallis (non-parametric)

**Decision:** Mann-Whitney U and Kruskal-Wallis tests

**Rationale:** Price and occupancy distributions are heavily right-skewed 
(confirmed by distribution analysis). Normality assumption violations 
make parametric tests inappropriate. Non-parametric tests are more 
robust for this dataset.

**Trade-offs Accepted:** Non-parametric tests are less powerful than 
parametric equivalents when normality holds. Effect sizes reported 
using Cohen's d alongside p-values to compensate.

---

### Decision 6: Visualization Tool — Power BI + Streamlit

**Options Considered:**
- matplotlib/seaborn only (simple but static)
- Tableau (powerful but expensive)
- Power BI (professional, interactive)
- Streamlit (Python-native, deployable)

**Decision:** Power BI for EDA section + Streamlit for Open Innovation

**Rationale:** Power BI provides professional interactive dashboards 
suitable for business stakeholder presentation (Section 04). 
Streamlit demonstrates engineering capability — building a deployable 
web application directly from Python data pipeline outputs (Section 08).
Using both tools showcases breadth of visualization expertise.

**Trade-offs Accepted:** Power BI dashboards require desktop application 
to view. Streamlit requires Python environment to run locally.

---

### Decision 7: Missing Value Strategy

**Options Considered:**
- Drop all rows with nulls (loses too much data)
- Mean imputation (distorts distribution)
- Median imputation (robust to outliers)
- Sentinel values (-1 or "Unknown")

**Decision:** Median imputation for review scores and bedrooms/beds; 
explicit nulls retained for categorical fields

**Rationale:** Review scores missing for ~35% of listings (new/inactive).
Median imputation preserves distribution shape better than mean for 
skewed data. Categorical fields (neighbourhood, host_location) kept as 
null to avoid introducing false categories.

**Trade-offs Accepted:** Imputed values may underrepresent true variance 
in review scores for new listings. Analysis notes this limitation.

---

### Decision 8: Content-Based Recommendation over Collaborative Filtering

**Options Considered:**
- Collaborative filtering (requires user interaction history)
- Matrix factorization (requires rating matrix)
- Content-based TF-IDF (uses listing attributes)

**Decision:** Content-based filtering using TF-IDF + cosine similarity

**Rationale:** Inside Airbnb data contains no user interaction history 
or explicit ratings per user — only aggregate review counts. 
Collaborative filtering is therefore not applicable. Content-based 
filtering using listing descriptions, amenities, and numerical features 
provides meaningful recommendations without user history.

**Trade-offs Accepted:** Cold-start problem for new listings with no 
description text. Cannot personalize beyond listing attributes.