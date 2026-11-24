import json
from pathlib import Path

import pytest

DATA = Path(__file__).resolve().parent.parent / "data"

# Each file and the lowercase properties every feature must have.
FILES = {
    "substations_vic.geojson": ["feature_name", "voltage_kv", "state"],
    "power_lines_vic.geojson": ["feature_name", "capacity_kv", "state"],
}


@pytest.mark.parametrize("filename, required", FILES.items())
def test_geojson_loads_with_lowercase_properties(filename, required):
    data = json.loads((DATA / filename).read_text())

    assert data["type"] == "FeatureCollection"
    assert data["features"], f"{filename} has no features"
    for feature in data["features"]:
        missing = [key for key in required if key not in feature["properties"]]
        assert not missing, f"{filename} feature missing {missing}"
