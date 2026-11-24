## Project
Power system modelling tool: maps Victorian electricity transmission infrastructure from Geoscience Australia open data. A Python pipeline produces GeoJSON, and a static Leaflet page in `map/` displays it. Scope is Victoria only for now.

## Layout
- `pull_and_plot.py`: pulls substations and power lines, writes `data/substations_vic.geojson`, `data/power_lines_vic.geojson` and `data/vic_network.png`
- `map/index.html`: static interactive map, loads `../data/*.geojson`
- `tests/`: pytest; `.github/workflows/ci.yml` runs it on every push

## Data
- Source: https://services.ga.gov.au/gis/rest/services/Electricity_Infrastructure/MapServer (layer 0 Substations, 1 Major Power Stations, 2 Power Lines). Do not use the older National_Electricity_Infrastructure service; its field names differ.
- Requests use `outSR=4326`, so output is already WGS84. Source CRS is GDA2020 (EPSG:7844).
- GeoJSON property names are lowercase: `feature_name`, `capacity_kv`, `voltage_kv`, `state`. The uppercase names in the service field list do not appear in the output.
- Columns containing brackets (e.g. `st_length(shape)`) are dropped.
- Selection: bounding box (140.9,-39.3,150.1,-33.9), keeping features tagged VIC or intersecting the Natural Earth Victoria polygon. The state tag alone misses cross-border features, which is why the intersection test exists. Features tagged NSW are cross-border features.
- Limit: no electrical properties beyond voltage (no impedance), so the data is for mapping and measuring, not power flow.

## Licence and attribution
Data is CC BY 4.0, (c) Commonwealth of Australia (Geoscience Australia) 2026. Any published map or page must carry the attribution footer already in `map/index.html` (credit, licence link, note that data was filtered and reprojected, not endorsed, indicative only). Natural Earth (public domain) must be credited if its borders are shown. Any new data source needs its own attribution check before publishing.

## Conventions
- Code should be easy to read.
- Work on a branch and open a pull request; CI must pass.
- Do not change `data/` or the pipeline script unless asked.

## Planned, not yet built
- Weather layer from BARRA2 reanalysis (wind and solar resource)
- PostGIS backend for the network data
- ABS state boundary replacing Natural Earth (the Hume substation on the Murray is the doubtful case)
- Static hosting on S3 + CloudFront (GitHub Pages as fallback)
