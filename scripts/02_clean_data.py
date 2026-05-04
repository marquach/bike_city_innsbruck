"""Project networks to metric CRS and filter relevant OSM tags."""
import logging

from bike_city_innsbruck.config import CRS_METRIC, DATA_INTERIM, DATA_RAW
from bike_city_innsbruck.preprocess import (
    extract_cycling_infrastructure,
    filter_road_network,
    load_and_project,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    DATA_INTERIM.mkdir(parents=True, exist_ok=True)

    logger.info("Loading and projecting road network...")
    roads = load_and_project(DATA_RAW / "roads.graphml", CRS_METRIC)
    roads = filter_road_network(roads)
    roads.to_file(DATA_INTERIM / "roads_clean.gpkg", driver="GPKG")
    logger.info("Road network: %d edges → %s", len(roads), DATA_INTERIM / "roads_clean.gpkg")

    logger.info("Extracting cycling infrastructure...")
    cycling = extract_cycling_infrastructure(roads)
    cycling.to_file(DATA_INTERIM / "cycling_clean.gpkg", driver="GPKG")
    logger.info("Cycling infrastructure: %d edges → %s", len(cycling), DATA_INTERIM / "cycling_clean.gpkg")

    print(f"Clean data saved to {DATA_INTERIM}")
