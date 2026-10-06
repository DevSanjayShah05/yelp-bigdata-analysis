"""
Data synthesizer and loader for Yelp Big Data Analysis.
Generates columnar Parquet tables matching Yelp Open Dataset specifications.
"""
from pathlib import Path
import pandas as pd
import numpy as np

from src.config import (
    RAW_DATA_DIR,
    BUSINESS_PARQUET,
    REVIEW_PARQUET,
    USER_PARQUET,
    CHECKIN_PARQUET,
    PRIMARY_CATEGORIES,
    METROPOLITAN_CITIES,
    RANDOM_STATE,
)


def generate_yelp_dataset(force: bool = False):
    """Generate authentic, scaled Yelp datasets in Apache Parquet format."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if (
        not force
        and BUSINESS_PARQUET.exists()
        and REVIEW_PARQUET.exists()
        and USER_PARQUET.exists()
        and CHECKIN_PARQUET.exists()
    ):
        print("Yelp Parquet tables already exist. Skipping generation.")
        return

    print("Generating scaled Yelp Big Data tables in Apache Parquet format...")
    np.random.seed(RANDOM_STATE)

    # 1. Businesses Table (10,000 records)
    n_businesses = 10000
    b_ids = [f"b_{i:06d}" for i in range(n_businesses)]
    
    city_coords = {
        "Philadelphia": (39.9526, -75.1652, "PA"),
        "Tucson": (32.2226, -110.9747, "AZ"),
        "Tampa": (27.9506, -82.4572, "FL"),
        "Indianapolis": (39.7684, -86.1581, "IN"),
        "Nashville": (36.1627, -86.7816, "TN"),
        "New Orleans": (29.9511, -90.0715, "LA"),
        "Edmonton": (53.5461, -113.4938, "AB"),
        "Reno": (39.5296, -119.8138, "NV"),
    }
    
    cities = np.random.choice(list(city_coords.keys()), size=n_businesses)
    lats = [city_coords[c][0] + np.random.normal(0, 0.05) for c in cities]
    lons = [city_coords[c][1] + np.random.normal(0, 0.05) for c in cities]
    states = [city_coords[c][2] for c in cities]
    
    stars = np.random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0], size=n_businesses, p=[0.02, 0.03, 0.08, 0.12, 0.18, 0.22, 0.20, 0.12, 0.03])
    review_counts = np.random.exponential(scale=45, size=n_businesses).astype(int) + 3
    is_open = np.random.choice([1, 0], size=n_businesses, p=[0.82, 0.18])
    
    categories_col = []
    for _ in range(n_businesses):
        cats = np.random.choice(PRIMARY_CATEGORIES, size=np.random.randint(1, 4), replace=False)
        categories_col.append(", ".join(cats))

    df_businesses = pd.DataFrame({
        "business_id": b_ids,
        "name": [f"Business {i}" for i in range(n_businesses)],
        "city": cities,
        "state": states,
        "latitude": lats,
        "longitude": lons,
        "stars": stars,
        "review_count": review_counts,
        "is_open": is_open,
        "categories": categories_col
    })
    df_businesses.to_parquet(BUSINESS_PARQUET, compression="snappy", index=False)
    print(f" -> Businesses saved: {BUSINESS_PARQUET} ({len(df_businesses):,} rows)")

    # 2. Users Table (20,000 records)
    n_users = 20000
    u_ids = [f"u_{i:06d}" for i in range(n_users)]
    elite_status = np.random.choice([True, False], size=n_users, p=[0.08, 0.92])
    user_review_counts = np.random.exponential(scale=25, size=n_users).astype(int) + 1
    user_avg_stars = np.clip(np.random.normal(3.7, 0.6, size=n_users), 1.0, 5.0).round(2)
    
    df_users = pd.DataFrame({
        "user_id": u_ids,
        "name": [f"User {i}" for i in range(n_users)],
        "review_count": user_review_counts,
        "yelping_since": pd.date_range("2015-01-01", periods=n_users, freq="2h").strftime("%Y-%m-%d"),
        "useful": np.random.poisson(12, size=n_users),
        "funny": np.random.poisson(5, size=n_users),
        "cool": np.random.poisson(8, size=n_users),
        "is_elite": elite_status,
        "average_stars": user_avg_stars
    })
    df_users.to_parquet(USER_PARQUET, compression="snappy", index=False)
    print(f" -> Users saved: {USER_PARQUET} ({len(df_users):,} rows)")

    # 3. Reviews Table (50,000 records)
    n_reviews = 50000
    df_reviews = pd.DataFrame({
        "review_id": [f"r_{i:07d}" for i in range(n_reviews)],
        "user_id": np.random.choice(u_ids, size=n_reviews),
        "business_id": np.random.choice(b_ids, size=n_reviews),
        "stars": np.random.choice([1, 2, 3, 4, 5], size=n_reviews, p=[0.10, 0.12, 0.18, 0.30, 0.30]),
        "useful": np.random.poisson(1.5, size=n_reviews),
        "funny": np.random.poisson(0.5, size=n_reviews),
        "cool": np.random.poisson(0.8, size=n_reviews),
        "date": pd.date_range("2019-01-01", periods=n_reviews, freq="40min").strftime("%Y-%m-%d %H:%M:%S")
    })
    df_reviews.to_parquet(REVIEW_PARQUET, compression="snappy", index=False)
    print(f" -> Reviews saved: {REVIEW_PARQUET} ({len(df_reviews):,} rows)")

    # 4. Checkins Table (100,000 records)
    n_checkins = 100000
    hour_probs = np.array([
        0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02, 0.03,  # 00-07
        0.04, 0.05, 0.06, 0.08, 0.09, 0.08, 0.06, 0.06,  # 08-15
        0.07, 0.08, 0.09, 0.07, 0.04, 0.02, 0.01, 0.01   # 16-23 (peaks at lunch & dinner)
    ])
    hour_probs = hour_probs / hour_probs.sum()
    hours = np.random.choice(range(24), size=n_checkins, p=hour_probs)

    dow_probs = np.array([0.11, 0.12, 0.13, 0.14, 0.18, 0.20, 0.12])
    dow_probs = dow_probs / dow_probs.sum()
    dows = np.random.choice(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], size=n_checkins, p=dow_probs)
    
    df_checkins = pd.DataFrame({
        "checkin_id": [f"chk_{i:07d}" for i in range(n_checkins)],
        "business_id": np.random.choice(b_ids, size=n_checkins),
        "day_of_week": dows,
        "hour_of_day": hours,
        "timestamp": pd.date_range("2021-01-01", periods=n_checkins, freq="25min").strftime("%Y-%m-%d %H:%M:%S")
    })
    df_checkins.to_parquet(CHECKIN_PARQUET, compression="snappy", index=False)
    print(f" -> Check-ins saved: {CHECKIN_PARQUET} ({len(df_checkins):,} rows)")


def get_dataset_paths():
    """Return dictionary of parquet paths, generating them if not found."""
    generate_yelp_dataset()
    return {
        "businesses": BUSINESS_PARQUET,
        "reviews": REVIEW_PARQUET,
        "users": USER_PARQUET,
        "checkins": CHECKIN_PARQUET,
    }
