"""OSM network download helpers."""
import logging
from pathlib import Path

import osmnx as ox

logger = logging.getLogger(__name__)

# Extra OSM way tags to fetch on top of osmnx defaults — needed to detect
# painted bike lanes and tracks that sit on regular road edges.
_EXTRA_TAGS = [
    "cycleway",
    "cycleway:left",
    "cycleway:right",
    "cycleway:both",
    "bicycle",
]


def _configure_tags() -> None:
    """Extend osmnx useful_tags_way with cycling-specific tags."""
    current = list(ox.settings.useful_tags_way)
    additions = [t for t in _EXTRA_TAGS if t not in current]
    if additions:
        ox.settings.useful_tags_way = current + additions


def _bbox_to_ox(bbox: tuple) -> tuple:
    """Convert (south, west, north, east) tuple to osmnx 2.x (west, south, east, north)."""
    south, west, north, east = bbox
    return (west, south, east, north)


def download_road_network(bbox: tuple, save_path: Path, overwrite: bool = False):
    """Download full road network for bbox, save as GraphML. Returns graph."""
    save_path = Path(save_path)
    if save_path.exists() and not overwrite:
        logger.info("Road network already at %s — skipping download", save_path)
        return ox.load_graphml(save_path)
    _configure_tags()
    logger.info("Downloading road network (network_type='all')...")
    G = ox.graph_from_bbox(_bbox_to_ox(bbox), network_type="all")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    ox.save_graphml(G, save_path)
    logger.info("Saved road network → %s", save_path)
    return G


def download_cycling_network(bbox: tuple, save_path: Path, overwrite: bool = False):
    """Download cycling network for bbox, save as GraphML. Returns graph."""
    save_path = Path(save_path)
    if save_path.exists() and not overwrite:
        logger.info("Cycling network already at %s — skipping download", save_path)
        return ox.load_graphml(save_path)
    _configure_tags()
    logger.info("Downloading cycling network (network_type='bike')...")
    G = ox.graph_from_bbox(_bbox_to_ox(bbox), network_type="bike")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    ox.save_graphml(G, save_path)
    logger.info("Saved cycling network → %s", save_path)
    return G
