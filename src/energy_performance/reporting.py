from pathlib import Path


def write_summary_report(
    output_path: Path,
    quality: dict,
    forecast_metrics: dict,
    portfolio_daily,
    anomalies,
    out_of_hours,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    total_energy = portfolio_daily["energy_kwh"].sum()
    total_co2 = portfolio_daily["estimated_co2_kg"].sum()
    anomaly_days = int(anomalies["is_anomaly"].sum())
    top_waste = out_of_hours.iloc[0] if not out_of_hours.empty else None
    top_waste_text = (
        f"{top_waste['building_id']} ({top_waste['avg_out_of_hours_share']:.1%} average out-of-hours share)"
        if top_waste is not None
        else "No building identified"
    )

    report = f"""# Building Energy Performance Summary

This report uses public Building Data Genome Project 2 electricity, metadata and weather data. It is inspired by building performance analytics use cases such as energy monitoring, anomaly detection, out-of-hours waste checks and ESG-style reporting.

## Portfolio Snapshot

- Rows analysed: {quality['rows']:,}
- Buildings analysed: {quality['buildings']}
- Period: {quality['start']} to {quality['end']}
- Total electricity: {total_energy:,.0f} kWh
- Estimated CO2: {total_co2:,.0f} kg CO2e
- Daily anomaly flags: {anomaly_days}
- Weekly naive forecast MAE: {forecast_metrics['mae_kwh']:.2f} kWh
- Top out-of-hours candidate: {top_waste_text}

## Interpretation

The analysis creates a practical monitoring view from meter data: overall demand trend, high/low daily anomalies, out-of-hours consumption and a simple short-term baseline forecast.

The output is not intended to replace a production building analytics platform. It demonstrates the analytical workflow: data checks, time-series features, transparent rules and a short report that a customer success or operations team could review.

## Recommended Next Checks

- Confirm whether high out-of-hours readings match real occupancy or operational schedules.
- Investigate high anomaly days against weather and site events.
- Replace the illustrative CO2 factor with the correct reporting factor for the target region and year.
- Add building operating hours where available instead of using a generic night/weekend rule.
"""
    output_path.write_text(report, encoding="utf-8")

