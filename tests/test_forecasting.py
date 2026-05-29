import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from energy_performance.forecasting import add_weekly_naive_forecast, forecast_metrics


def test_weekly_naive_forecast_uses_same_hour_previous_week():
    timestamps = pd.date_range("2024-01-01", periods=170, freq="h")
    frame = pd.DataFrame(
        {
            "timestamp": timestamps,
            "building_id": ["b1"] * len(timestamps),
            "energy_kwh": list(range(len(timestamps))),
        }
    )

    result = add_weekly_naive_forecast(frame)

    assert pd.isna(result.loc[167, "forecast_kwh"])
    assert result.loc[168, "forecast_kwh"] == 0
    assert result.loc[169, "forecast_kwh"] == 1


def test_forecast_metrics_reports_mae():
    frame = pd.DataFrame(
        {
            "energy_kwh": [10.0, 20.0],
            "forecast_kwh": [8.0, 25.0],
            "absolute_error": [2.0, 5.0],
        }
    )

    result = forecast_metrics(frame)

    assert result["mae_kwh"] == 3.5
    assert result["evaluated_rows"] == 2

