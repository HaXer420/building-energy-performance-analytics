import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from energy_performance.config import AnalysisConfig
from energy_performance.features import add_time_features, daily_building_usage


def test_out_of_hours_flags_nights_and_weekends():
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2024-01-01 10:00", "2024-01-01 22:00", "2024-01-06 12:00"]
            ),
            "building_id": ["b1", "b1", "b1"],
            "energy_kwh": [10.0, 20.0, 30.0],
            "sqm": [100.0, 100.0, 100.0],
        }
    )

    result = add_time_features(frame, AnalysisConfig())

    assert result["is_out_of_hours"].tolist() == [False, True, True]
    assert result["energy_kwh_per_sqm"].tolist() == [0.1, 0.2, 0.3]


def test_daily_usage_sums_out_of_hours_energy():
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2024-01-01 10:00", "2024-01-01 22:00"]),
            "building_id": ["b1", "b1"],
            "primaryspaceusage": ["Office", "Office"],
            "energy_kwh": [10.0, 20.0],
            "estimated_co2_kg": [2.0, 4.0],
            "sqm": [100.0, 100.0],
            "airTemperature": [8.0, 7.0],
        }
    )
    features = add_time_features(frame, AnalysisConfig())

    daily = daily_building_usage(features)

    assert daily.loc[0, "energy_kwh"] == 30.0
    assert daily.loc[0, "out_of_hours_kwh"] == 20.0

