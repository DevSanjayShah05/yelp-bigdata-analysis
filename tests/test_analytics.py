"""
Tests for DuckDB analytical SQL engine in Project 3.
"""
from src.analytics import YelpBigDataAnalytics


def test_category_performance_query():
    engine = YelpBigDataAnalytics()
    df = engine.analyze_category_performance()
    assert not df.empty
    assert "category" in df.columns
    assert "avg_stars" in df.columns
    assert "total_businesses" in df.columns


def test_geospatial_distribution_query():
    engine = YelpBigDataAnalytics()
    df = engine.analyze_geospatial_distribution()
    assert not df.empty
    assert "city" in df.columns
    assert "centroid_lat" in df.columns
    assert "business_count" in df.columns


def test_reviewer_characteristics_query():
    engine = YelpBigDataAnalytics()
    df = engine.analyze_reviewer_characteristics()
    assert len(df) == 2  # Elite vs Non-Elite
    assert "is_elite" in df.columns
    assert "avg_reviews_written" in df.columns


def test_temporal_checkins_query():
    engine = YelpBigDataAnalytics()
    df = engine.analyze_temporal_checkins()
    assert not df.empty
    assert "hour_of_day" in df.columns
    assert "checkin_count" in df.columns
