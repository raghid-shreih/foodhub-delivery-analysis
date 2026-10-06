"""Generate local analysis charts and an aggregate portfolio gallery."""

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


def save_gallery(frame: pd.DataFrame, directory: str | Path) -> list[Path]:
    """Render portfolio figures from an authorized CSV as shareable SVGs.

    These figures use aggregate counts or distributions, never order/customer IDs.
    """
    destination = Path(directory)
    destination.mkdir(parents=True, exist_ok=True)
    ink, burgundy, rose, pale = "#24303B", "#672744", "#BD7898", "#EDF0F2"
    paths = []
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.labelcolor": ink, "text.color": ink,
                         "svg.fonttype": "none", "svg.hashsalt": "foodhub-gallery"}):
        cuisine = frame["cuisine_type"].value_counts().head(8).sort_values()
        fig, ax = plt.subplots(figsize=(9, 5.2))
        bars = ax.barh(cuisine.index, cuisine.values, color=[rose] * (len(cuisine) - 1) + [burgundy])
        ax.bar_label(bars, padding=6, color=ink, fontsize=10)
        ax.set_xlim(0, max(cuisine) * 1.13)
        ax.set_xlabel("Number of orders")
        ax.set_title("Most ordered cuisines", loc="left", weight="bold", pad=18)
        ax.grid(axis="x", color=pale)
        ax.set_axisbelow(True)
        fig.tight_layout()
        paths.append(destination / "cuisine-demand.svg")
        fig.savefig(paths[-1], format="svg", metadata={"Date": None})
        plt.close(fig)

        groups = [frame.loc[frame["day_of_the_week"] == d, "delivery_time"] for d in ("Weekday", "Weekend")]
        if any(group.empty for group in groups):
            raise ValueError("Gallery requires orders from both weekday and weekend groups")
        fig, ax = plt.subplots(figsize=(8, 5.2))
        box = ax.boxplot(groups, patch_artist=True, widths=.48, showfliers=False,
                         medianprops={"color": ink, "linewidth": 2})
        ax.set_xticks([1, 2], labels=[f"Weekday\n(n={len(groups[0]):,})", f"Weekend\n(n={len(groups[1]):,})"])
        for patch, color in zip(box["boxes"], [burgundy, rose]):
            patch.set_facecolor(color)
            patch.set_alpha(.9)
        for item in box["whiskers"] + box["caps"]:
            item.set_color(ink)
        means = [float(g.mean()) for g in groups]
        ax.scatter([1, 2], means, marker="D", s=50, color="#E8B85A", edgecolor=ink, zorder=3, label="Mean")
        for x, mean in enumerate(means, 1):
            ax.annotate(f"{mean:.2f} min", (x, mean), xytext=(14, 9), textcoords="offset points",
                        weight="bold", bbox={"facecolor": "white", "edgecolor": "none", "alpha": .9, "pad": 2})
        ax.set_ylabel("Delivery time (minutes)")
        ax.set_title("Delivery time distributions by day type", loc="left", weight="bold", pad=18)
        ax.grid(axis="y", color=pale)
        ax.set_axisbelow(True)
        ax.legend(frameon=False, loc="upper right")
        fig.tight_layout()
        paths.append(destination / "delivery-time.svg")
        fig.savefig(paths[-1], format="svg", metadata={"Date": None})
        plt.close(fig)

        total = frame["food_preparation_time"] + frame["delivery_time"]
        minutes = range(int(total.min()), int(total.max()) + 1)
        counts = total.value_counts().reindex(minutes, fill_value=0)
        fig, ax = plt.subplots(figsize=(9, 5.2))
        ax.bar(list(minutes), counts.values, width=.9, color=[rose if minute <= 60 else burgundy for minute in minutes])
        ax.axvline(60.5, color=ink, linestyle="--", linewidth=1.7)
        above = int((total > 60).sum())
        ax.text(.98, .96, f"{above:,} orders > 60 min\n{above / len(total):.1%} of all orders",
                transform=ax.transAxes, va="top", ha="right", color=burgundy, weight="bold")
        ax.set_xlabel("Preparation + delivery time (minutes)")
        ax.set_ylabel("Orders")
        ax.set_title("Preparation and delivery time by minute", loc="left", weight="bold", pad=18)
        ax.grid(axis="y", color=pale)
        ax.set_axisbelow(True)
        fig.tight_layout()
        paths.append(destination / "total-time.svg")
        fig.savefig(paths[-1], format="svg", metadata={"Date": None})
        plt.close(fig)

        labels = ["Not given", "5", "4", "3", "2", "1"]
        ratings = frame["rating"].astype(str).value_counts().reindex(labels, fill_value=0)
        fig, ax = plt.subplots(figsize=(8, 5.2))
        bars = ax.bar(labels, ratings.values, color=[burgundy] + [rose] * 5)
        ax.bar_label(bars, padding=5, fontsize=10)
        ax.set_ylim(0, max(ratings) * 1.18)
        ax.set_ylabel("Number of orders")
        ax.set_xlabel("Recorded rating")
        ax.set_title("Many orders have no recorded rating", loc="left", weight="bold", pad=18)
        ax.grid(axis="y", color=pale)
        ax.set_axisbelow(True)
        fig.tight_layout()
        paths.append(destination / "rating-coverage.svg")
        fig.savefig(paths[-1], format="svg", metadata={"Date": None})
        plt.close(fig)
    return paths
