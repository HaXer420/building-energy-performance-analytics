import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from energy_performance.anomaly_detection import flag_iqr_anomalies, high_out_of_hours_buildings
from energy_performance.config import AnalysisConfig
from energy_performance.data_loader import load_analysis_data
from energy_performance.data_quality import quality_summary, timestamp_gap_summary
from energy_performance.features import add_time_features, daily_building_usage, portfolio_daily_usage
from energy_performance.forecasting import add_weekly_naive_forecast, forecast_metrics
from energy_performance.reporting import write_summary_report
from energy_performance.visualization import (
    save_anomaly_chart,
    save_out_of_hours_chart,
    save_portfolio_trend,
)


def main() -> None:
    config = AnalysisConfig()
    frame = load_analysis_data(config)
    features = add_time_features(frame, config)
    daily = daily_building_usage(features)
    portfolio_daily = portfolio_daily_usage(daily)
    anomalies = flag_iqr_anomalies(daily, multiplier=config.anomaly_iqr_multiplier)
    out_of_hours = high_out_of_hours_buildings(daily)
    forecasted = add_weekly_naive_forecast(features)
    forecast_summary = forecast_metrics(forecasted)
    quality = quality_summary(features)
    gaps = timestamp_gap_summary(features)

    outputs = config.output_dir
    (outputs / "reports").mkdir(parents=True, exist_ok=True)
    (outputs / "figures").mkdir(parents=True, exist_ok=True)
    (outputs / "reports" / "quality_summary.json").write_text(
        json.dumps(quality, indent=2), encoding="utf-8"
    )
    gaps.to_csv(outputs / "reports" / "timestamp_gaps.csv", index=False)
    daily.to_csv(outputs / "reports" / "daily_building_usage.csv", index=False)
    out_of_hours.to_csv(outputs / "reports" / "out_of_hours_candidates.csv", index=False)
    save_portfolio_trend(portfolio_daily, outputs / "figures")
    save_out_of_hours_chart(out_of_hours, outputs / "figures")
    save_anomaly_chart(anomalies, outputs / "figures")
    write_summary_report(
        outputs / "reports" / "summary_report.md",
        quality,
        forecast_summary,
        portfolio_daily,
        anomalies,
        out_of_hours,
    )
    print(json.dumps({"quality": quality, "forecast": forecast_summary}, indent=2))


if __name__ == "__main__":
    main()

