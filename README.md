# Power Model

Interactive map tool for displaying the Victorian power network GIS model.

## Interactive map

Serve the repository root and open the map in a browser:

```bash
python -m http.server
```

Then go to <http://localhost:8000/map/>. The page must be served over HTTP (not opened as a file) because it loads `data/*.geojson` with `fetch`.

The map shows Victorian substations and high-voltage power lines from Geoscience Australia's Electricity Infrastructure dataset. `pull_and_plot.py` queries the Geoscience Australia map service for a bounding box around Victoria, keeps features tagged `VIC` or intersecting the Victorian border, and writes them to `data/substations_vic.geojson` and `data/power_lines_vic.geojson` in WGS84. Lines are coloured by `capacity_kv`, and features tagged `NSW` are cross-border features, drawn dashed in purple. The script also saves a static overview plot, `data/vic_network.png`.

## Licence and attribution

Power line and substation data: (c) Commonwealth of Australia (Geoscience Australia) 2026, Electricity Infrastructure, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Filtered to Victoria and reprojected from GDA2020 (EPSG:7844) for web display. Not endorsed by Geoscience Australia. Indicative only; not a substitute for Dial Before You Dig.
