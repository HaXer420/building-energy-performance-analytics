# Building Energy Performance Analytics

This project analyses public building electricity, metadata and weather
time-series data to identify unusual consumption patterns, out-of-hours energy
waste and short-term consumption behaviour.

It is inspired by building performance intelligence use cases such as energy
monitoring, anomaly detection, operational reporting and ESG analytics.

![Daily portfolio electricity trend](assets/daily_portfolio_energy.png)

## Business Question

Can building meter, metadata and weather time-series data be used to identify
energy anomalies, out-of-hours waste and short-term consumption patterns?

## Dataset

The project uses the public **Building Data Genome Project 2** dataset.

Dataset repository: <https://github.com/buds-lab/building-data-genome-project-2>

Files used locally:

- `electricity.csv`
- `metadata.csv`
- `weather.csv`

The full electricity file is large, so this repository does not commit raw
data. The analysis samples a small group of lodging/residential buildings from
the public dataset.

See [`data/README.md`](data/README.md) for dataset setup details.

## What the Analysis Does

- Loads building electricity, metadata and weather time-series data.
- Selects a manageable lodging/residential building subset.
- Checks missing values, duplicate building timestamps and timestamp gaps.
- Adds calendar, out-of-hours, energy intensity and estimated CO2 features.
- Aggregates hourly data into daily building and portfolio-level summaries.
- Detects unusual daily energy intensity using an IQR rule.
- Identifies buildings with high out-of-hours energy share.
- Builds a simple weekly naive forecast for short-term baseline comparison.
- Generates plots and a short markdown report for non-technical review.

## Sample Result

The current run analysed 166,552 hourly readings across 10 lodging/residential
buildings from 2016-01-01 to 2017-12-31.

Key outputs:

- 8,839,782 kWh total electricity across the sampled buildings.
- 226 daily anomaly flags using transparent IQR-based detection.
- 7.00 kWh weekly naive forecast MAE.
- Highest out-of-hours candidate: `Bear_lodging_Dannie`, with 68.2% average out-of-hours share.

See [`RESULTS.md`](RESULTS.md) for the sample portfolio summary.

## Project Structure

```text
building-energy-performance-analytics/
|-- README.md
|-- RESULTS.md
|-- requirements.txt
|-- assets/
|-- data/
|   `-- README.md
|-- src/energy_performance/
|   |-- data_loader.py
|   |-- data_quality.py
|   |-- features.py
|   |-- anomaly_detection.py
|   |-- forecasting.py
|   |-- visualization.py
|   `-- reporting.py
|-- tests/
|-- outputs/
|   |-- figures/
|   `-- reports/
`-- run_analysis.py
```

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the analysis:

```bash
python run_analysis.py
```

Run tests:

```bash
pytest
```

## Outputs

The pipeline writes:

- `outputs/reports/summary_report.md`
- `outputs/reports/quality_summary.json`
- `outputs/reports/daily_building_usage.csv`
- `outputs/reports/out_of_hours_candidates.csv`
- `outputs/figures/daily_portfolio_energy.png`
- `outputs/figures/out_of_hours_buildings.png`
- `outputs/figures/anomaly_days.png`

Generated files are ignored by Git so they can be recreated from the public
data.

## Why This Project Exists

The project is designed as a practical data analyst / data scientist portfolio
piece for building-performance analytics. It focuses on the type of workflow a
data team might use before building a customer-facing dashboard:

1. check data quality;
2. create useful time-series features;
3. detect operational issues;
4. summarise findings clearly;
5. keep the methods simple enough to explain and test.

## Limitations

- The out-of-hours rule uses a generic night/weekend assumption because real
  operating schedules are not available.
- The CO2 calculation uses a configurable illustrative factor and should be
  replaced with the correct reporting factor for a real ESG submission.
- IQR anomaly detection is transparent but simple; a production platform would
  validate alerts against operational events, occupancy and meter context.
