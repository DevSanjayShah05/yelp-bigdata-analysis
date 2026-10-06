"""
Tests for Yelp Big Data data loader module.
"""
from src.data_loader import get_dataset_paths


def test_parquet_tables_exist():
    paths = get_dataset_paths()
    for name, path in paths.items():
        assert path.exists(), f"Parquet table {name} was not generated"
        assert path.stat().st_size > 1000, f"Parquet table {name} is empty"
