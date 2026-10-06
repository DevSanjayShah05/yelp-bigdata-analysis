"""
Configuration module for Yelp Big Data Analysis project.
Defines file paths, schemas, and analytical constants.
"""
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ARTIFACTS_DIR = PROJECT_DIR / "artifacts"
NOTEBOOKS_DIR = PROJECT_DIR / "notebooks"

# Parquet file paths
BUSINESS_PARQUET = RAW_DATA_DIR / "businesses.parquet"
REVIEW_PARQUET = RAW_DATA_DIR / "reviews.parquet"
USER_PARQUET = RAW_DATA_DIR / "users.parquet"
CHECKIN_PARQUET = RAW_DATA_DIR / "checkins.parquet"

# Analytical targets
PRIMARY_CATEGORIES = [
    "Restaurants", "Nightlife", "Shopping", "Food", 
    "Bars", "Coffee & Tea", "Beauty & Spas", "Home Services"
]

METROPOLITAN_CITIES = [
    "Philadelphia", "Tucson", "Tampa", "Indianapolis", 
    "Nashville", "New Orleans", "Edmonton", "Reno"
]

RANDOM_STATE = 42
SCALE_FACTOR = 10000  # Number of business entities for analysis
