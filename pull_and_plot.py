from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import requests

BASE = "https://services.ga.gov.au/gis/rest/services/Electricity_Infrastructure/MapServer"
LAYERS = {"substations": 0, "power_lines": 2}
BOX = "140.9,-39.3,150.1,-33.9"
STATES_URL = "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_1_states_provinces.zip"
OUT = Path("data")


def pull(layer_id):
    r = requests.get(
        f"{BASE}/{layer_id}/query",
        params={
            "where": "1=1",
            "geometry": BOX,
            "geometryType": "esriGeometryEnvelope",
            "inSR": 4326,
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": "*",
            "outSR": 4326,
            "f": "geojson",
        },
    )
    gdf = gpd.GeoDataFrame.from_features(r.json()["features"], crs="EPSG:4326")
    return gdf[[c for c in gdf.columns if "(" not in c]]


au = gpd.read_file(STATES_URL).query("admin == 'Australia'")
vic = au[au["name"] == "Victoria"].geometry.union_all()

OUT.mkdir(exist_ok=True)    # I assume this just leaves the directory if it exists?
data = {}

# pulls layers from GA and decides whether each line/substation is at least partly in VIC
for name, layer_id in LAYERS.items():
    gdf = pull(layer_id)
    keep = gdf[(gdf["state"] == "VIC") | gdf.intersects(vic)]
    keep.to_file(OUT / f"{name}_vic.geojson", driver="GeoJSON")
    data[name] = keep
    print(f"{name}: {len(gdf)} in box, {len(keep)} kept, {(keep['state'] != 'VIC').sum()} tagged other states")

fig, ax = plt.subplots(figsize=(11, 8))
au.boundary.plot(ax=ax, color="grey", linewidth=0.5)
data["power_lines"].plot(
    ax=ax,
    column="capacity_kv",
    cmap="viridis",
    legend=True,
    linewidth=1,
    legend_kwds={"label": "Line capacity (kV)"},
)
data["substations"].plot(ax=ax, color="red", markersize=8)

minx, miny, maxx, maxy = data["power_lines"].total_bounds
ax.set_xlim(minx - 0.3, maxx + 0.3)
ax.set_ylim(miny - 0.3, maxy + 0.3)
ax.set_title("Victorian substations and power lines")
ax.set_xlabel(
    "Data: (c) Commonwealth of Australia (Geoscience Australia) 2026, CC BY 4.0. "
    "Filtered to Victoria and nearby cross-border lines. Borders: Natural Earth.",
    fontsize=7,
)
fig.savefig(OUT / "vic_network.png", dpi=150, bbox_inches="tight")

print(data["power_lines"].query("state != 'VIC'")[["feature_name", "state", "capacity_kv"]])
print(data["substations"].query("state != 'VIC'")[["feature_name", "state", "voltage_kv"]])
