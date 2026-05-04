"""Network cleaning and projection helpers."""
import geopandas as gpd
import osmnx as ox
from pathlib import Path

# Purely pedestrian — exclude from road/bike ratio denominator
_ROAD_EXCLUDE = frozenset({"steps", "corridor"})

# Values in cycleway:* tags that indicate real infrastructure
# "separate" means a physically separate way already mapped as highway=cycleway — skip to avoid double-count
_CYCLEWAY_INFRA_VALUES = frozenset({"lane", "track", "shared_lane", "share_busway"})


def _hw_matches(value, tag_set: frozenset) -> bool:
    """Return True if a highway value (str or list) overlaps with tag_set."""
    if isinstance(value, str):
        return value in tag_set
    return bool(tag_set.intersection(value))


def _tag_has_infra(value) -> bool:
    """Return True if a cycleway:* tag value indicates real cycling infrastructure."""
    if isinstance(value, float):  # NaN
        return False
    if isinstance(value, str):
        return value in _CYCLEWAY_INFRA_VALUES
    # osmnx sometimes returns a list when multiple values exist
    return any(v in _CYCLEWAY_INFRA_VALUES for v in value)


def load_and_project(graphml_path: Path, crs: str) -> gpd.GeoDataFrame:
    """Load GraphML network, return edge GeoDataFrame projected to crs."""
    G = ox.load_graphml(graphml_path)
    _, edges = ox.graph_to_gdfs(G)
    return edges.to_crs(crs)


def filter_road_network(edges: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Drop pedestrian-only edge types (steps, corridors) from a road network GDF."""
    keep_cols = [c for c in ["highway", "length", "geometry"] if c in edges.columns]
    mask = ~edges["highway"].apply(_hw_matches, tag_set=_ROAD_EXCLUDE)
    return edges.loc[mask, keep_cols].copy()


def extract_cycling_infrastructure(edges: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Identify all edges that carry cycling infrastructure and tag them by type.

    Types assigned (mutually exclusive, in priority order):
      - "dedicated"  : highway=cycleway or bicycle=designated on a non-road way
      - "lane"       : painted/marked bike lane on a regular road
                       (cycleway, cycleway:left, cycleway:right, or cycleway:both
                        with values lane/track/shared_lane/share_busway)

    Returns a GeoDataFrame with columns [highway, length, infra_type, geometry].
    """
    df = edges.copy()

    # --- dedicated paths ---
    is_cycleway_hw = df["highway"].apply(_hw_matches, tag_set=frozenset({"cycleway"}))

    is_designated = (
        df.get("bicycle", "").apply(
            lambda v: v == "designated" if isinstance(v, str) else "designated" in v if isinstance(v, list) else False
        )
        & ~is_cycleway_hw  # already counted above
    )

    # --- on-road cycling infrastructure ---
    cy_side_cols = [c for c in ["cycleway:left", "cycleway:right", "cycleway:both"] if c in df.columns]
    has_side_lane = (
        sum(df[c].apply(_tag_has_infra) for c in cy_side_cols) > 0
        if cy_side_cols else False
    )

    has_cy_tag = (
        df["cycleway"].apply(_tag_has_infra) if "cycleway" in df.columns else False
    )

    is_lane = (has_side_lane | has_cy_tag) & ~is_cycleway_hw & ~is_designated

    mask = is_cycleway_hw | is_designated | is_lane

    result = df.loc[mask, ["highway", "length", "geometry"]].copy()
    result["infra_type"] = "lane"
    result.loc[is_cycleway_hw[mask], "infra_type"] = "dedicated"
    result.loc[is_designated[mask], "infra_type"] = "dedicated"

    return result
