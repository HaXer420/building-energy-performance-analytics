import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from energy_performance.anomaly_detection import flag_iqr_anomalies, high_out_of_hours_buildings


def test_iqr_anomaly_flags_high_daily_energy():
    daily = pd.DataFrame(
        {
            "building_id": ["b1"] * 6,
            "energy_kwh_per_sqm": [1.0, 1.1, 1.0, 1.2, 1.1, 10.0],
        }
    )

    result = flag_iqr_anomalies(daily, multiplier=1.5)

    assert bool(result.iloc[-1]["is_anomaly"]) is True
    assert result.iloc[-1]["anomaly_direction"] == "high"


def test_high_out_of_hours_buildings_returns_largest_share():
    daily = pd.DataFrame(
        {
            "building_id": ["a", "b"],
            "energy_kwh": [100.0, 100.0],
            "out_of_hours_kwh": [20.0, 80.0],
            "out_of_hours_share": [0.2, 0.8],
        }
    )

    result = high_out_of_hours_buildings(daily, top_n=1)

    assert result.iloc[0]["building_id"] == "b"

