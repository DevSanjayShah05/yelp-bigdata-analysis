"""
Visualization generator for Yelp Big Data Analysis.
Produces publication-quality charts matching arXiv:2104.08396 requirements.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import ARTIFACTS_DIR


def plot_category_performance(df_cats: pd.DataFrame, output_path: Path = None) -> Path:
    """Plot category average stars and business counts."""
    if output_path is None:
        output_path = ARTIFACTS_DIR / "category_performance_benchmark.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("Yelp Dimension 1: Business Category Performance Benchmark", fontsize=15, fontweight="bold")

    # 1. Total Businesses
    sns.barplot(data=df_cats, x="total_businesses", y="category", ax=axes[0], palette="Blues_r", hue="category", legend=False)
    axes[0].set_title("Total Businesses by Category")
    axes[0].set_xlabel("Number of Businesses")
    axes[0].set_ylabel("Category")

    # 2. Average Star Rating
    sns.barplot(data=df_cats, x="avg_stars", y="category", ax=axes[1], palette="magma", hue="category", legend=False)
    axes[1].set_title("Average Star Rating by Category")
    axes[1].set_xlabel("Average Stars (1.0 - 5.0)")
    axes[1].set_xlim(2.5, 4.5)
    axes[1].set_ylabel("")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path


def plot_geospatial_distribution(df_geo: pd.DataFrame, output_path: Path = None) -> Path:
    """Plot geo-spatial distribution and average rating across metropolitan hubs."""
    if output_path is None:
        output_path = ARTIFACTS_DIR / "geospatial_business_density.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 7))
    scatter = plt.scatter(
        df_geo["centroid_lon"],
        df_geo["centroid_lat"],
        s=df_geo["business_count"] * 1.5,
        c=df_geo["avg_city_rating"],
        cmap="coolwarm",
        alpha=0.85,
        edgecolors="black",
        linewidth=1.5,
    )
    plt.colorbar(scatter, label="Average City Star Rating")

    for _, row in df_geo.iterrows():
        plt.annotate(
            f"{row['city']} ({row['business_count']:,} biz)",
            (row["centroid_lon"], row["centroid_lat"]),
            xytext=(10, 8),
            textcoords="offset points",
            fontweight="bold",
            fontsize=10,
        )

    plt.title("Yelp Dimension 2: Geo-Spatial Distribution & Concentration Across Hubs", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Longitude (Degrees)")
    plt.ylabel("Latitude (Degrees)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path


def plot_temporal_checkin_heatmap(df_checkin: pd.DataFrame, output_path: Path = None) -> Path:
    """Plot Hour of Day x Day of Week check-in foot traffic heatmap."""
    if output_path is None:
        output_path = ARTIFACTS_DIR / "temporal_checkin_heatmap.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dow_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    pivot = df_checkin.pivot(index="day_of_week", columns="hour_of_day", values="checkin_count")
    pivot = pivot.reindex(dow_order)

    plt.figure(figsize=(15, 6))
    sns.heatmap(
        pivot,
        cmap="YlOrRd",
        linewidths=0.5,
        cbar_kws={"label": "Total Foot Traffic Check-Ins"},
    )
    plt.title("Yelp Dimension 4: Temporal Foot Traffic Heatmap (Day of Week × Hour of Day)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Hour of Day (00:00 - 23:00)")
    plt.ylabel("Day of Week")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path


def plot_reviewer_influence(df_users: pd.DataFrame, output_path: Path = None) -> Path:
    """Plot Elite vs. Non-Elite reviewer voting metrics."""
    if output_path is None:
        output_path = ARTIFACTS_DIR / "reviewer_influence_distribution.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df_users["Status"] = df_users["is_elite"].apply(lambda x: "Elite User" if x else "Standard User")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("Yelp Dimension 3: Reviewer Characteristics & Social Influence", fontsize=15, fontweight="bold")

    # 1. Reviews written
    sns.barplot(data=df_users, x="Status", y="avg_reviews_written", ax=axes[0], palette="Blues_d", hue="Status", legend=False)
    axes[0].set_title("Average Reviews Written per User")
    axes[0].set_ylabel("Review Count")

    # 2. Useful Votes
    sns.barplot(data=df_users, x="Status", y="avg_useful_votes", ax=axes[1], palette="Greens_d", hue="Status", legend=False)
    axes[1].set_title("Average 'Useful' Votes Received")
    axes[1].set_ylabel("Votes Count")

    # 3. Mean Rating Given
    sns.barplot(data=df_users, x="Status", y="mean_rating_given", ax=axes[2], palette="Oranges_d", hue="Status", legend=False)
    axes[2].set_title("Average Rating Leniency (Stars Given)")
    axes[2].set_ylabel("Stars (1-5)")
    axes[2].set_ylim(2.5, 4.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path


def plot_business_ratings(df_ratings: pd.DataFrame, output_path: Path = None) -> Path:
    """Plot business star rating distribution histogram."""
    if output_path is None:
        output_path = ARTIFACTS_DIR / "business_rating_distribution.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 5))
    sns.barplot(data=df_ratings, x="stars", y="percentage", palette="Blues_d", hue="stars", legend=False)
    plt.title("Overall Yelp Business Star Rating Distribution", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Star Rating")
    plt.ylabel("Percentage of Total Businesses (%)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path
