import pandas as pd

from .config import AnalysisConfig


def add_time_features(frame: pd.DataFrame, config: AnalysisConfig) -> pd.DataFrame:
    data = frame.copy()
    data["hour"] = data["timestamp"].dt.hour
    data["date"] = data["timestamp"].dt.date
    data["day_of_week"] = data["timestamp"].dt.dayofweek
    data["is_weekend"] = data["day_of_week"].isin([5, 6])
    data["is_out_of_hours"] = (
        (data["hour"] >= config.out_of_hours_start)
        | (data["hour"] < config.out_of_hours_end)
        | data["is_weekend"]
    )
    data["energy_kwh_per_sqm"] = data["energy_kwh"] / data["sqm"]
    data["estimated_co2_kg"] = data["energy_kwh"] * config.co2_kg_per_kwh
    return data


def daily_building_usage(frame: pd.DataFrame) -> pd.DataFrame:
    daily = (
        frame.groupby(["building_id", "date", "primaryspaceusage"], as_index=False)
        .agg(
            energy_kwh=("energy_kwh", "sum"),
            estimated_co2_kg=("estimated_co2_kg", "sum"),
            sqm=("sqm", "first"),
            avg_temperature=("airTemperature", "mean"),
            out_of_hours_kwh=("energy_kwh", lambda series: series[frame.loc[series.index, "is_out_of_hours"]].sum()),
        )
    )
    daily["energy_kwh_per_sqm"] = daily["energy_kwh"] / daily["sqm"]
    daily["out_of_hours_share"] = daily["out_of_hours_kwh"] / daily["energy_kwh"]
    return daily


def portfolio_daily_usage(daily: pd.DataFrame) -> pd.DataFrame:
    portfolio = (
        daily.groupby("date", as_index=False)
        .agg(
            energy_kwh=("energy_kwh", "sum"),
            estimated_co2_kg=("estimated_co2_kg", "sum"),
            out_of_hours_kwh=("out_of_hours_kwh", "sum"),
            avg_temperature=("avg_temperature", "mean"),
        )
    )
    portfolio["out_of_hours_share"] = (
        portfolio["out_of_hours_kwh"] / portfolio["energy_kwh"]
    )
    return portfolio

