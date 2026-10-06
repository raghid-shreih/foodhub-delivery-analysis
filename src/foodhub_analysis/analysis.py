"""Transparent descriptive metrics for a food delivery order table."""

from pathlib import Path

import pandas as pd

REQUIRED = {
    "order_id", "customer_id", "restaurant_name", "cuisine_type",
    "cost_of_the_order", "day_of_the_week", "rating",
    "food_preparation_time", "delivery_time",
}


def load_orders(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    if frame.empty:
        raise ValueError("The CSV has no orders")
    if frame[list(REQUIRED)].isna().any().any():
        raise ValueError("Required columns contain missing values")
    if frame["order_id"].duplicated().any():
        raise ValueError("Duplicate order_id values")
    if not frame["day_of_the_week"].isin(["Weekday", "Weekend"]).all():
        raise ValueError("day_of_the_week must be Weekday or Weekend")
    for column in ("cost_of_the_order", "food_preparation_time", "delivery_time"):
        frame[column] = pd.to_numeric(frame[column], errors="raise")
        if (frame[column] < 0).any():
            raise ValueError(f"{column} cannot be negative")
    rating = frame["rating"].astype(str)
    if not rating.isin(["1", "2", "3", "4", "5", "Not given"]).all():
        raise ValueError("rating must be 1–5 or 'Not given'")
    return frame


def analyze_orders(frame: pd.DataFrame) -> dict:
    total = len(frame)
    day = frame.groupby("day_of_the_week")["delivery_time"].agg(["size", "mean"])
    delivery = {
        kind: {"orders": int(day.loc[kind, "size"]), "mean_minutes": round(float(day.loc[kind, "mean"]), 2)}
        for kind in ("Weekday", "Weekend") if kind in day.index
    }
    weekend = frame.loc[frame["day_of_the_week"] == "Weekend", "cuisine_type"].value_counts()
    cuisine = frame["cuisine_type"].value_counts()
    cost = frame["cost_of_the_order"]
    commission = (cost.where(cost > 20, 0) * .25 + cost.where((cost > 5) & (cost <= 20), 0) * .15).sum()
    unrated = int((frame["rating"].astype(str) == "Not given").sum())
    slow = int(((frame["food_preparation_time"] + frame["delivery_time"]) > 60).sum())
    rated = frame.loc[frame["rating"].astype(str) != "Not given"].copy()
    rated["rating"] = rated["rating"].astype(int)
    restaurant = rated.groupby("restaurant_name")["rating"].agg(["count", "mean"])
    eligible = restaurant[(restaurant["count"] > 50) & (restaurant["mean"] > 4)].sort_index()
    return {
        "orders": total,
        "restaurants": int(frame["restaurant_name"].nunique()),
        "unique_customers": int(frame["customer_id"].nunique()),
        "top_cuisines": {str(k): int(v) for k, v in cuisine.head(5).items()},
        "weekend_top_cuisine": {"name": str(weekend.index[0]), "orders": int(weekend.iloc[0])} if len(weekend) else None,
        "delivery_by_day": delivery,
        "orders_over_60_minutes": {"count": slow, "share": round(slow / total, 4)},
        "unrated_orders": {"count": unrated, "share": round(unrated / total, 4)},
        "orders_over_20_dollars": {"count": int((cost > 20).sum()), "share": round(float((cost > 20).mean()), 4)},
        "estimated_commission_dollars": round(float(commission), 2),
        "promotion_candidates": [
            {"restaurant": str(name), "rated_orders": int(row["count"]), "mean_rating": round(float(row["mean"]), 2)}
            for name, row in eligible.iterrows()
        ],
    }
