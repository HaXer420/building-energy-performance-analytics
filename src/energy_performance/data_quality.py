import pandas as pd


def quality_summary(frame: pd.DataFrame) -> dict:
    return {
        "rows": int(len(frame)),
        "buildings": int(frame["building_id"].nunique()),
        "start": str(frame["timestamp"].min()),
        "end": str(frame["timestamp"].max()),
        "missing_energy_rows": int(frame["energy_kwh"].isna().sum()),
        "duplicate_building_timestamps": int(
            frame.duplicated(["building_id", "timestamp"]).sum()
        ),
        "missing_weather_rows": int(frame["airTemperature"].isna().sum())
        if "airTemperature" in frame
        else None,
    }


def timestamp_gap_summary(frame: pd.DataFrame, expected_frequency: str = "1h") -> pd.DataFrame:
    expected = pd.Timedelta(expected_frequency)
    rows = []
    for building_id, group in frame.groupby("building_id"):
        timestamps = group["timestamp"].sort_values()
        gaps = timestamps.diff().dropna()
        rows.append(
            {
                "building_id": building_id,
                "observations": len(group),
                "large_gaps": int((gaps > expected).sum()),
                "max_gap_hours": float(gaps.max() / pd.Timedelta(hours=1))
                if not gaps.empty
                else 0.0,
            }
        )
    return pd.DataFrame(rows)

