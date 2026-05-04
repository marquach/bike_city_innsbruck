"""Network cleaning and projection helpers."""
import geopandas as gpd
import osmnx as ox
from pathlib import Path

# Purely pedestrian — exclude from road/bike ratio denominator
_ROAD_EXCLUDE = frozenset({"steps", "corridor"})

# Dedicated cycling infrastructure highway types
_CYCLING_INFRA = frozenset({"cycleway"})


def _hw_matches(value, tag_set: frozenset) -> bool:
    """Return True if a highway value (str or list) overlaps with tag_set."""
    if isinstance(value, str):
        return value in tag_set
    return bool(tag_set.intersection(value))


def load_and_project(graphml_path: Path, crs: str) -> gpd.GeoDataFrame:
    """Load GraphML network, return edge GeoDataFrame projected to crs."""
    G = ox.load_graphml(graphml_path)
    _, edges = ox.graph_to_gdfs(G)
    return edges.to_crs(crs)


def filter_road_network(edges: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Drop pedestrian-only edge types (steps, corridors) from a road network GDF."""
    mask = ~edges["highway"].apply(_hw_matches, tag_set=_ROAD_EXCLUDE)
    return edges.loc[mask, ["highway", "length", "geometry"]].copy()


def extract_cycling_infrastructure(edges: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Keep only dedicated cycling edges (highway=cycleway) from a road network GDF."""
    mask = edges["highway"].apply(_hw_matches, tag_set=_CYCLING_INFRA)
    return edges.loc[mask, ["highway", "length", "geometry"]].copy()
