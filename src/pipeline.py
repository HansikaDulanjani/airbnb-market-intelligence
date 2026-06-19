import logging
import os
import json
from datetime import datetime
from ingestion import load_datasets
from cleaning import clean_listings, clean_calendar, clean_reviews
from enrichment import enrich_listings
from star_schema import build_star_schema

# ============================================
# LOGGING SETUP
# ============================================
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# METADATA TRACKING
# ============================================
def save_metadata(metadata):
    os.makedirs('docs', exist_ok=True)
    with open('docs/pipeline_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)
    logger.info("Metadata saved to docs/pipeline_metadata.json")

# ============================================
# MAIN PIPELINE
# ============================================
def run_pipeline(city="bangkok", data_path="data/raw"):
    metadata = {
        "city": city,
        "pipeline_start": datetime.now().isoformat(),
        "steps": {}
    }

    logger.info(f"Starting pipeline for city: {city.upper()}")
    logger.info("=" * 60)

    try:
        # STEP 1: INGESTION
        logger.info("STEP 1: Data Ingestion")
        start = datetime.now()
        listings, calendar, reviews = load_datasets(data_path)
        metadata['steps']['ingestion'] = {
            "status": "success",
            "duration_seconds": (datetime.now() - start).seconds,
            "listings_rows": len(listings),
            "calendar_rows": len(calendar),
            "reviews_rows": len(reviews)
        }
        logger.info("STEP 1 COMPLETE")

        # STEP 2: CLEANING
        logger.info("STEP 2: Data Cleaning")
        start = datetime.now()
        listings_clean = clean_listings(listings)
        calendar_clean = clean_calendar(calendar)
        reviews_clean = clean_reviews(reviews)

        os.makedirs('data/processed', exist_ok=True)
        listings_clean.to_csv('data/processed/listings_clean.csv', index=False)
        calendar_clean.to_csv('data/processed/calendar_clean.csv', index=False)
        reviews_clean.to_csv('data/processed/reviews_clean.csv', index=False)

        metadata['steps']['cleaning'] = {
            "status": "success",
            "duration_seconds": (datetime.now() - start).seconds,
            "listings_after_cleaning": len(listings_clean),
            "reviews_after_cleaning": len(reviews_clean)
        }
        logger.info("STEP 2 COMPLETE")

        # STEP 3: ENRICHMENT
        logger.info("STEP 3: Data Enrichment")
        start = datetime.now()
        master, neighbourhood_agg = enrich_listings(
            listings_clean, calendar_clean, reviews_clean
        )
        master.to_csv('data/processed/master_listings.csv', index=False)
        neighbourhood_agg.to_csv('data/processed/neighbourhood_agg.csv', index=False)

        metadata['steps']['enrichment'] = {
            "status": "success",
            "duration_seconds": (datetime.now() - start).seconds,
            "master_rows": len(master),
            "master_columns": len(master.columns),
            "neighbourhoods": len(neighbourhood_agg)
        }
        logger.info("STEP 3 COMPLETE")

        # STEP 4: STAR SCHEMA
        logger.info("STEP 4: Building Star Schema")
        start = datetime.now()
        build_star_schema()
        metadata['steps']['star_schema'] = {
            "status": "success",
            "duration_seconds": (datetime.now() - start).seconds,
            "database": "data/output/airbnb_bangkok.duckdb"
        }
        logger.info("STEP 4 COMPLETE")

        # PIPELINE COMPLETE
        metadata['pipeline_end'] = datetime.now().isoformat()
        metadata['status'] = "success"
        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY!")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        metadata['status'] = "failed"
        metadata['error'] = str(e)
        raise

    finally:
        save_metadata(metadata)

if __name__ == "__main__":
    run_pipeline(city="bangkok", data_path="data/raw")