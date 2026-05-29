from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AnalysisConfig:
    raw_data_dir: Path = Path("data/raw")
    output_dir: Path = Path("outputs")
    sample_buildings: int = 10
    target_usage: str = "Lodging/residential"
    out_of_hours_start: int = 19
    out_of_hours_end: int = 7
    anomaly_iqr_multiplier: float = 1.5
    co2_kg_per_kwh: float = 0.207


REQUIRED_RAW_FILES = ("electricity.csv", "metadata.csv", "weather.csv")

