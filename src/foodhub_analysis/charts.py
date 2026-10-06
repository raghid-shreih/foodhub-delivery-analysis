"""Save three compact charts locally; never embed source data in the repo."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def save_charts(frame: pd.DataFrame, directory: str | Path) -> list[Path]:
    destination = Path(directory)
    destination.mkdir(parents=True, exist_ok=True)
    paths = []

    cuisines = frame["cuisine_type"].value_counts().head(8).sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    cuisines.plot.barh(ax=ax, color="#6B2747")
    ax.set(xlabel="Orders", ylabel="Cuisine", title="Most ordered cuisines")
    fig.tight_layout()
    paths.append(destination / "cuisine-volume.png")
    fig.savefig(paths[-1], dpi=160)
    plt.close(fig)

    days = frame.groupby("day_of_the_week")["delivery_time"].mean().reindex(["Weekday", "Weekend"]).dropna()
    fig, ax = plt.subplots(figsize=(6, 4))
    days.plot.bar(ax=ax, color=["#6B2747", "#C891A8"][:len(days)], rot=0)
    ax.set(ylabel="Mean delivery time (minutes)", xlabel="", title="Delivery time by day type")
    ax.set_ylim(0, max(days) * 1.2)
    fig.tight_layout()
    paths.append(destination / "delivery-by-day.png")
    fig.savefig(paths[-1], dpi=160)
    plt.close(fig)

    counts = frame["rating"].astype(str).value_counts().reindex(["Not given", "1", "2", "3", "4", "5"], fill_value=0)
    fig, ax = plt.subplots(figsize=(7, 4))
    counts.plot.bar(ax=ax, color="#6B2747", rot=0)
    ax.set(ylabel="Orders", xlabel="Rating", title="Rating response and distribution")
    fig.tight_layout()
    paths.append(destination / "ratings.png")
    fig.savefig(paths[-1], dpi=160)
    plt.close(fig)
    return paths
