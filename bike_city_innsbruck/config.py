from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
REPORTS_FIGURES = ROOT / "reports" / "figures"
REPORTS_MAPS = ROOT / "reports" / "maps"

# Study area — Innsbruck city centre (south, west, north, east)
BBOX_CENTRE = (47.255, 11.375, 47.285, 11.425)

# Metric CRS for Austria
CRS_METRIC = "EPSG:31287"

# Grid cell size in metres
GRID_CELL_M = 200
