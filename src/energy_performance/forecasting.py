import numpy as np
import pandas as pd


def add_weekly_naive_forecast(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.sort_values(["building_id", "timestamp"]).copy()
    data["forecast_kwh"] = data.groupby("building_id")["energy_kwh"].shift(168)
    data["absolute_error"] = (data["energy_kwh"] - data["forecast_kwh"]).abs()
    return data


def forecast_metrics(forecasted: pd.DataFrame) -> dict:
    valid = forecasted.dropna(subset=["forecast_kwh", "energy_kwh"])
    if valid.empty:
        return {"mae_kwh": np.nan, "mape": np.nan, "evaluated_rows": 0}
    denominator = valid["energy_kwh"].replace(0, np.nan).abs()
    return {
        "mae_kwh": float(valid["absolute_error"].mean()),
        "mape": float((valid["absolute_error"] / denominator).dropna().mean()),
        "evaluated_rows": int(len(valid)),
    }

