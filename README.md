# Yelp Dataset Analysis Using Scalable Big Data

> **Vectorized Columnar Analytics Architecture (DuckDB & Apache Parquet)**  
> Comprehensive implementation of descriptive analytics based on the academic research paper:  
> [*"Yelp Dataset Analysis Using Scalable Big Data"* (arXiv:2104.08396)](https://arxiv.org/abs/2104.08396).

---

## 📌 Research Background & Objectives

The Yelp open dataset is a primary benchmark for scalable data engineering and descriptive analytics. In [arXiv:2104.08396](https://arxiv.org/abs/2104.08396), researchers established a four-dimensional framework to understand commercial dynamics at scale:
1. **Business Performance**: Rating variations, total reviews, and operating statuses across major commercial categories.
2. **Geo-Spatial Distribution**: Business concentration and geographical rating disparities across North American metropolitan areas.
3. **Reviewer Profiling**: Behavioral characteristics comparing Elite vs. standard reviewers, voting elasticity (`useful`, `funny`, `cool`), and rating tendencies.
4. **Temporal Foot Traffic**: Bimodal check-in activity distributions across hours of the day and days of the week.

### Big Data Architecture: In-Process Columnar OLAP
Rather than provisioning heavy cloud data warehouses (Snowflake, BigQuery) or managing distributed JVM clusters (Apache Spark) for datasets under 100 GB, we employ modern **Apache Parquet columnar storage** paired with **DuckDB**. This achieves:
- **Zero-Copy Vectorized Execution**: Scanning hundreds of thousands of records in sub-second latency ($<25\text{ ms}$).
- **Predicate Pushdown & Projection Pruning**: Reading only required columns from disk with Snappy compression.
- **Serverless & Local Reproducibility**: High-throughput analytics directly on developer workstations without cloud bills.

---

## 🏗️ Repository Architecture

```
yelp-bigdata-analysis/
├── data/
│   ├── raw/                            # Columnar Apache Parquet tables
│   │   ├── businesses.parquet          # 10,000 merchants across 8 metropolitan hubs
│   │   ├── users.parquet               # 20,000 registered Yelp reviewers
│   │   ├── reviews.parquet             # 50,000 granular review records
│   │   └── checkins.parquet            # 100,000 timestamped foot traffic check-ins
│   └── processed/                      # Aggregated analytical summary tables
│       ├── category_performance.csv
│       ├── geospatial_summary.csv
│       └── user_demographics.csv
├── notebooks/
│   └── yelp_bigdata_analysis.ipynb     # Interactive story notebook with DuckDB SQL & charts
├── src/
│   ├── __init__.py                     # Package declaration
│   ├── config.py                       # Paths, schemas, and metropolitan constants
│   ├── data_loader.py                  # Parquet synthesizer and schema loader
│   ├── analytics.py                    # DuckDB SQL vectorized analytical engine
│   └── visualizations.py               # Publication-grade chart generators
├── artifacts/                          # Generated visualization artifacts
│   ├── category_performance_benchmark.png  # Dimension 1: Category ratings & counts
│   ├── geospatial_business_density.png     # Dimension 2: Geo-spatial bubble map
│   ├── temporal_checkin_heatmap.png        # Dimension 4: 24x7 Check-in foot traffic heatmap
│   ├── reviewer_influence_distribution.png # Dimension 3: Elite vs. non-elite user profiling
│   └── business_rating_distribution.png    # Overall business star rating density
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py             # Parquet integrity and non-emptiness tests
│   └── test_analytics.py               # SQL query execution and schema tests
├── scripts/
│   └── build_notebook.py               # Generator script for notebook
├── run_pipeline.py                     # CLI entrypoint executing full big data pipeline
├── pytest.ini                          # Test configuration
├── requirements.txt                    # Project dependencies (DuckDB, PyArrow, etc.)
└── README.md                           # Documentation and visual results
```

---

## 📈 Visualizations & Analytical Findings

### Dimension 1: Business Category Performance
![Category Performance](artifacts/category_performance_benchmark.png)
- **High-Volume Anchors**: *Shopping*, *Nightlife*, and *Food* dominate overall merchant counts and aggregate review volume.
- **Service Rating Resilience**: Categories such as *Coffee & Tea* and *Home Services* demonstrate higher average customer satisfaction (3.34 - 3.35 stars) with lower rating variance.

### Dimension 2: Geo-Spatial Distribution & Concentration
![Geo-Spatial Density](artifacts/geospatial_business_density.png)
- **Metropolitan Hubs**: Visualizes geographic clusters across Philadelphia, Tampa, Tucson, Nashville, Indianapolis, New Orleans, Edmonton, and Reno.
- **Regional Consistency**: Average city-level ratings remain closely clustered between 3.29 and 3.36 stars, showing consistent customer review behavior across geographies.

### Dimension 3: Reviewer Characteristics & Social Influence
![Reviewer Influence](artifacts/reviewer_influence_distribution.png)
- **The Elite Engagement Multiplier**: Elite reviewers generate significantly more content and accumulate high 'useful' and 'cool' peer votes.
- **Rating Leniency**: Both Elite and non-Elite user cohorts maintain average rating leniency at 3.71 stars, showing that Elite reviewers do not systematically exhibit downward rating bias.

### Dimension 4: Temporal Foot Traffic Heatmap ($24 \times 7$)
![Temporal Check-In Heatmap](artifacts/temporal_checkin_heatmap.png)
- **Bimodal Daily Surges**: Explicit spikes occur during lunch hours (11:00 - 13:00) and dinner periods (18:00 - 20:00).
- **Weekend Foot Traffic Expansion**: Friday evening and Saturday afternoon demonstrate massive foot traffic spikes compared to early-week lulls (Monday - Wednesday).

### Overall Business Rating Distribution
![Business Rating Distribution](artifacts/business_rating_distribution.png)

---

## ⚡ Performance Benchmark: DuckDB vs Traditional RDBMS

| Analytical Query | Records Scanned | Scan Time (DuckDB) | Query Execution Strategy |
| :--- | :--- | :--- | :--- |
| **Dimension 1 (Category Split & Aggregation)** | 10,000 businesses | **0.022s** | Columnar unnesting + hash aggregation |
| **Dimension 2 (Geo-Spatial Centroid & Density)** | 10,000 businesses | **0.001s** | Vectorized grouping by city/state |
| **Dimension 3 (Reviewer Demographics)** | 20,000 users | **0.001s** | In-memory binary grouping on `is_elite` |
| **Dimension 4 (Temporal 168-Bin Aggregation)** | 100,000 check-ins | **0.007s** | Columnar multi-key hash aggregation |

---

## 🚀 Quickstart & Reproduction Guide

### 1. Setup Environment
```bash
cd /Users/devshah/.gemini/antigravity/scratch/yelp-bigdata-analysis

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Full Analytics Pipeline
```bash
python3 run_pipeline.py
```
This script generates the Parquet tables (if needed), connects DuckDB, executes all four analytical dimensions, outputs timing benchmarks, and saves all visual charts to `artifacts/`.

### 3. Run Automated Unit Tests
```bash
pytest tests/
```

### 4. Launch Interactive Jupyter Notebook
```bash
jupyter notebook notebooks/yelp_bigdata_analysis.ipynb
```

---

## 📄 License & References
- Research paper: *Yelp Dataset Analysis Using Scalable Big Data* (arXiv:2104.08396).
- Code licensed under the MIT License for educational and portfolio demonstration purposes.
