# Bike City Innsbruck — Geospatial Infrastructure Audit

> **Research question:** Is Innsbruck's "Bike City" label backed by actual cycling infrastructure data?

We use OpenStreetMap data to map bike lanes against the full road network in Innsbruck,
compute a bike-to-road ratio, identify spatial gaps, and cluster "bike-lane deserts."

---

## Study Area

**Pilot:** Innsbruck city centre (bounding box: `[47.255, 11.375, 47.285, 11.425]`)  
**Full city:** to follow in a later milestone

## Data Source

[OpenStreetMap](https://www.openstreetmap.org/) via [`osmnx`](https://osmnx.readthedocs.io/).
No manual downloads needed — scripts pull data at runtime.

## Method

1. **Extract** — download road and cycling networks with `osmnx`
2. **Clean** — project to metric CRS (EPSG:31287), filter relevant OSM tags
3. **Measure** — compute total road length and bike-infrastructure length; derive city-wide ratio
4. **Analyse** — split study area into 200 m grid cells; compute local bike-lane density per cell
5. **Model** — DBSCAN clustering on grid-cell density features to locate bike-lane deserts
6. **Communicate** — static figures + interactive Folium map

## Results

> **TBD — analysis in progress**

## Repo Structure

```
bike-city-audit-innsbruck/
├── bike_city_innsbruck/   # shared package (config, helpers)
├── scripts/               # numbered pipeline stages
├── notebooks/             # results communication only
├── data/
│   ├── raw/               # OSM downloads (git-ignored)
│   ├── interim/           # intermediate GeoPackages (git-ignored)
│   └── processed/         # final outputs
├── reports/
│   ├── figures/
│   └── maps/
└── references/            # methodology & tagging notes
```

## Reproduce

```bash
# 1. Clone
git clone https://github.com/marquach/bike_city_innsbruck.git
cd bike_city_innsbruck

# 2. Create environment
python -m venv .venv && source .venv/bin/activate
pip install -e .

# 3. Run pipeline
python scripts/01_extract_data.py
python scripts/02_clean_data.py
python scripts/03_compute_metrics.py
python scripts/04_spatial_analysis.py
python scripts/05_cluster_gaps.py
python scripts/06_make_figures.py

# 4. View results
jupyter notebook notebooks/01_results_overview.ipynb
```
