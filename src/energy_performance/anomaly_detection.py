import pandas as pd


def flag_iqr_anomalies(
    daily: pd.DataFrame,
    value_column: str = "energy_kwh_per_sqm",
    multiplier: float = 1.5,
) -> pd.DataFrame:
    data = daily.copy()
    bounds = []
    for building_id, group in data.groupby("building_id"):
        q1 = group[value_column].quantile(0.25)
        q3 = group[value_column].quantile(0.75)
        iqr = q3 - q1
        bounds.append(
            {
                "building_id": building_id,
                "lower": q1 - multiplier * iqr,
                "upper": q3 + multiplier * iqr,
            }
        )
    bounds_frame = pd.DataFrame(bounds)
    data = data.merge(bounds_frame, on="building_id", how="left")
    data["is_anomaly"] = (data[value_column] < data["lower"]) | (
        data[value_column] > data["upper"]
    )
    data["anomaly_direction"] = "normal"
    data.loc[data[value_column] > data["upper"], "anomaly_direction"] = "high"
    data.loc[data[value_column] < data["lower"], "anomaly_direction"] = "low"
    return data


def high_out_of_hours_buildings(daily: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    summary = (
        daily.groupby("building_id", as_index=False)
        .agg(
            total_energy_kwh=("energy_kwh", "sum"),
            out_of_hours_kwh=("out_of_hours_kwh", "sum"),
            avg_out_of_hours_share=("out_of_hours_share", "mean"),
        )
        .sort_values("avg_out_of_hours_share", ascending=False)
        .head(top_n)
    )
    return summary

