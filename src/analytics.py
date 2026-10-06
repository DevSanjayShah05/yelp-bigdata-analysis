"""
Scalable Big Data Analytics Engine using DuckDB.
Implements vectorized SQL descriptive analytics matching arXiv:2104.08396.
"""
from typing import Dict, Any
import duckdb
import pandas as pd

from src.data_loader import get_dataset_paths


class YelpBigDataAnalytics:
    """Scalable columnar analytical engine for Yelp dataset."""

    def __init__(self):
        paths = get_dataset_paths()
        self.con = duckdb.connect(database=":memory:")
        
        # Register Parquet files as zero-copy views in DuckDB
        self.con.execute(f"CREATE VIEW businesses AS SELECT * FROM read_parquet('{paths['businesses']}');")
        self.con.execute(f"CREATE VIEW reviews AS SELECT * FROM read_parquet('{paths['reviews']}');")
        self.con.execute(f"CREATE VIEW users AS SELECT * FROM read_parquet('{paths['users']}');")
        self.con.execute(f"CREATE VIEW checkins AS SELECT * FROM read_parquet('{paths['checkins']}');")
        print("DuckDB engine connected and initialized views over Parquet tables.")

    def analyze_category_performance(self) -> pd.DataFrame:
        """
        Dimension 1: Analyze business performance across categories.
        Measures mean rating, total review volume, and open business ratio.
        """
        query = """
        WITH unnested_cats AS (
            SELECT 
                business_id,
                trim(unnest(string_split(categories, ','))) AS category,
                stars,
                review_count,
                is_open
            FROM businesses
        )
        SELECT 
            category,
            count(*) AS total_businesses,
            round(avg(stars), 2) AS avg_stars,
            sum(review_count) AS total_reviews,
            round(avg(is_open) * 100, 1) AS open_percentage
        FROM unnested_cats
        WHERE category IN ('Restaurants', 'Nightlife', 'Shopping', 'Food', 'Bars', 'Coffee & Tea', 'Beauty & Spas', 'Home Services')
        GROUP BY category
        ORDER BY total_businesses DESC;
        """
        return self.con.execute(query).df()

    def analyze_geospatial_distribution(self) -> pd.DataFrame:
        """
        Dimension 2: Geo-spatial concentration and rating variances across cities.
        """
        query = """
        SELECT 
            city,
            state,
            count(*) AS business_count,
            round(avg(latitude), 4) AS centroid_lat,
            round(avg(longitude), 4) AS centroid_lon,
            round(avg(stars), 2) AS avg_city_rating,
            sum(review_count) AS total_reviews
        FROM businesses
        GROUP BY city, state
        ORDER BY business_count DESC;
        """
        return self.con.execute(query).df()

    def analyze_reviewer_characteristics(self) -> pd.DataFrame:
        """
        Dimension 3: User characteristics comparing Elite vs. Non-Elite reviewers.
        """
        query = """
        SELECT 
            is_elite,
            count(*) AS user_count,
            round(avg(review_count), 1) AS avg_reviews_written,
            round(avg(average_stars), 2) AS mean_rating_given,
            round(avg(useful), 1) AS avg_useful_votes,
            round(avg(funny), 1) AS avg_funny_votes,
            round(avg(cool), 1) AS avg_cool_votes
        FROM users
        GROUP BY is_elite;
        """
        return self.con.execute(query).df()

    def analyze_temporal_checkins(self) -> pd.DataFrame:
        """
        Dimension 4: Temporal distribution of check-ins across Hour and Day of Week.
        """
        query = """
        SELECT 
            day_of_week,
            hour_of_day,
            count(*) AS checkin_count
        FROM checkins
        GROUP BY day_of_week, hour_of_day
        ORDER BY hour_of_day, day_of_week;
        """
        return self.con.execute(query).df()

    def analyze_rating_distributions(self) -> pd.DataFrame:
        """Distribution of star ratings across businesses."""
        query = """
        SELECT 
            stars,
            count(*) AS count,
            round(count(*) * 100.0 / sum(count(*)) OVER (), 2) AS percentage
        FROM businesses
        GROUP BY stars
        ORDER BY stars;
        """
        return self.con.execute(query).df()
