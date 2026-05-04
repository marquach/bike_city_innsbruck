"""Download Innsbruck road and cycling networks from OpenStreetMap."""
import logging

from bike_city_innsbruck.config import BBOX_CENTRE, DATA_RAW
from bike_city_innsbruck.data import download_cycling_network, download_road_network

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

if __name__ == "__main__":
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    download_road_network(BBOX_CENTRE, DATA_RAW / "roads.graphml")
    download_cycling_network(BBOX_CENTRE, DATA_RAW / "cycling.graphml")

    print(f"Extraction complete. Files saved to {DATA_RAW}")
