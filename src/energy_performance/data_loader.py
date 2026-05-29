from pathlib import Path

import pandas as pd

from .config import AnalysisConfig, REQUIRED_RAW_FILES


def validate_raw_files(raw_data_dir: Path) -> None:
    missing = [name for name in REQUIRED_RAW_FILES if not (raw_data_dir / name).exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing raw data files: {missing}. See data/README.md for setup."
        )


def load_metadata(raw_data_dir: Path) -> pd.DataFrame:
    metadata = pd.read_csv(raw_data_dir / "metadata.csv")
    required = {"building_id", "site_id", "primaryspaceusage", "sqm"}
    missing = required.difference(metadata.columns)
    if missing:
        raise ValueError(f"metadata.csv missing columns: {sorted(missing)}")
    return metadata


def select_buildings(metadata: pd.DataFrame, config: AnalysisConfig) -> list[str]:
    candidates = metadata[
        (metadata["primaryspaceusage"] == config.target_usage)
        & (metadata["electricity"].fillna("") == "Yes")
        & metadata["sqm"].notna()
    ].copy()
    if candidates.empty:
        raise ValueError(f"No buildings found for usage: {config.target_usage}")
    candidates = candidates.sort_values(["site_id", "building_id"])
    return candidates["building_id"].head(config.sample_buildings).tolist()


def load_electricity_sample(raw_data_dir: Path, building_ids: list[str]) -> pd.DataFrame:
    columns = ["timestamp", *building_ids]
    electricity = pd.read_csv(
        raw_data_dir / "electricity.csv",
        usecols=lambda column: column in columns,
        parse_dates=["timestamp"],
    )
    long = electricity.melt(
        id_vars="timestamp", var_name="building_id", value_name="energy_kwh"
    )
    return long.dropna(subset=["energy_kwh"]).reset_index(drop=True)


def load_weather(raw_data_dir: Path, site_ids: list[str]) -> pd.DataFrame:
    weather = pd.read_csv(raw_data_dir / "weather.csv", parse_dates=["timestamp"])
    weather = weather[weather["site_id"].isin(site_ids)].copy()
    keep = ["timestamp", "site_id", "airTemperature", "dewTemperature", "windSpeed"]
    return weather[keep]


def load_analysis_data(config: AnalysisConfig) -> pd.DataFrame:
    validate_raw_files(config.raw_data_dir)
    metadata = load_metadata(config.raw_data_dir)
    building_ids = select_buildings(metadata, config)
    building_metadata = metadata[metadata["building_id"].isin(building_ids)].copy()
    site_ids = building_metadata["site_id"].dropna().unique().tolist()

    electricity = load_electricity_sample(config.raw_data_dir, building_ids)
    weather = load_weather(config.raw_data_dir, site_ids)
    frame = electricity.merge(building_metadata, on="building_id", how="left")
    frame = frame.merge(weather, on=["timestamp", "site_id"], how="left")
    return frame.sort_values(["building_id", "timestamp"]).reset_index(drop=True)

