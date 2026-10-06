#!/usr/bin/env python3
"""
End-to-End Yelp Scalable Big Data Analytics Pipeline (arXiv:2104.08396).
Executes high-throughput columnar analytics via DuckDB on Apache Parquet tables,
evaluates business performance, geo-spatial patterns, reviewer dynamics, and check-ins.
"""
import sys
import time
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import ARTIFACTS_DIR, PROCESSED_DATA_DIR
from src.data_loader import generate_yelp_dataset
from src.analytics import YelpBigDataAnalytics
from src.visualizations import (
    plot_category_performance,
    plot_geospatial_distribution,
    plot_temporal_checkin_heatmap,
    plot_reviewer_influence,
    plot_business_ratings,
)


def main():
    print("=" * 70)
    print(" YELP BIG DATA SCALABLE ANALYTICS PIPELINE (arXiv:2104.08396)")
    print("=" * 70)

    # 1. Ingest / Prepare Parquet Tables
    print("\n[Step 1/5] Verifying and loading Apache Parquet columnar tables...")
    t0 = time.time()
    generate_yelp_dataset()
    print(f"Data tables validated in {time.time() - t0:.2f}s.")

    # 2. Connect DuckDB Columnar Engine
    print("\n[Step 2/5] Initializing DuckDB high-throughput SQL engine...")
    engine = YelpBigDataAnalytics()

    # 3. Execute Core Analytics Dimensions
    print("\n[Step 3/5] Executing 4 Core Analytical Dimensions via DuckDB SQL...")
    
    # Dimension 1: Category Performance
    t_start = time.time()
    df_cats = engine.analyze_category_performance()
    print(f" -> Dimension 1 (Category Performance) executed in {time.time() - t_start:.3f}s:")
    print(df_cats.to_string(index=False))

    # Dimension 2: Geo-spatial Distribution
    t_start = time.time()
    df_geo = engine.analyze_geospatial_distribution()
    print(f"\n -> Dimension 2 (Geo-Spatial Distribution) executed in {time.time() - t_start:.3f}s:")
    print(df_geo.to_string(index=False))

    # Dimension 3: Reviewer Profiling
    t_start = time.time()
    df_users = engine.analyze_reviewer_characteristics()
    print(f"\n -> Dimension 3 (Reviewer Profiling) executed in {time.time() - t_start:.3f}s:")
    print(df_users.to_string(index=False))

    # Dimension 4: Temporal Check-In Foot Traffic
    t_start = time.time()
    df_checkins = engine.analyze_temporal_checkins()
    print(f"\n -> Dimension 4 (Temporal Check-Ins) aggregated {len(df_checkins):,} time intervals in {time.time() - t_start:.3f}s.")

    # Business Ratings
    df_ratings = engine.analyze_rating_distributions()

    # 4. Save Processed Aggregations
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df_cats.to_csv(PROCESSED_DATA_DIR / "category_performance.csv", index=False)
    df_geo.to_csv(PROCESSED_DATA_DIR / "geospatial_summary.csv", index=False)
    df_users.to_csv(PROCESSED_DATA_DIR / "user_demographics.csv", index=False)
    print(f"\n[Step 4/5] Saved aggregated analytical tables to: {PROCESSED_DATA_DIR}")

    # 5. Generate Visualizations
    print("\n[Step 5/5] Generating publication-grade big data visualizations...")
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    cat_plot = plot_category_performance(df_cats, ARTIFACTS_DIR / "category_performance_benchmark.png")
    geo_plot = plot_geospatial_distribution(df_geo, ARTIFACTS_DIR / "geospatial_business_density.png")
    heat_plot = plot_temporal_checkin_heatmap(df_checkins, ARTIFACTS_DIR / "temporal_checkin_heatmap.png")
    user_plot = plot_reviewer_influence(df_users, ARTIFACTS_DIR / "reviewer_influence_distribution.png")
    rat_plot = plot_business_ratings(df_ratings, ARTIFACTS_DIR / "business_rating_distribution.png")

    print(f"Saved category performance plot to: {cat_plot}")
    print(f"Saved geospatial density plot to:   {geo_plot}")
    print(f"Saved check-in heatmap to:          {heat_plot}")
    print(f"Saved reviewer influence plot to:   {user_plot}")
    print(f"Saved rating distribution plot to:  {rat_plot}")

    print("\n" + "=" * 70)
    print(" YELP BIG DATA PIPELINE COMPLETED SUCCESSFULLY!")
    print(f" Artifacts directory: {ARTIFACTS_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()
