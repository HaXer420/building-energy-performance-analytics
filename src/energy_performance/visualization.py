from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


def save_portfolio_trend(portfolio_daily, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 5))
    sns.lineplot(data=portfolio_daily, x="date", y="energy_kwh", ax=ax)
    ax.set_title("Daily Portfolio Electricity Consumption")
    ax.set_xlabel("Date")
    ax.set_ylabel("Electricity (kWh)")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_dir / "daily_portfolio_energy.png", dpi=160)
    plt.close(fig)


def save_out_of_hours_chart(summary, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=summary, y="building_id", x="avg_out_of_hours_share", ax=ax)
    ax.set_title("Highest Average Out-of-Hours Energy Share")
    ax.set_xlabel("Average out-of-hours share")
    ax.set_ylabel("Building")
    fig.tight_layout()
    fig.savefig(output_dir / "out_of_hours_buildings.png", dpi=160)
    plt.close(fig)


def save_anomaly_chart(anomalies, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    counts = (
        anomalies[anomalies["is_anomaly"]]
        .groupby(["building_id", "anomaly_direction"])
        .size()
        .reset_index(name="days")
    )
    if counts.empty:
        return
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=counts, y="building_id", x="days", hue="anomaly_direction", ax=ax)
    ax.set_title("Anomaly Days by Building")
    ax.set_xlabel("Anomaly days")
    ax.set_ylabel("Building")
    fig.tight_layout()
    fig.savefig(output_dir / "anomaly_days.png", dpi=160)
    plt.close(fig)

