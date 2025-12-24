import pandas as pd

# -------------------------------------------------
# Hourly Feature Engineering
# -------------------------------------------------
def make_hourly_features(df):
    df = df.copy()

    # Ensure sorted by time
    df = df.sort_values("time")

    # Lag features
    for lag in [1, 2, 3]:
        df[f"temp_lag_{lag}h"] = df["temperature_2m"].shift(lag)
        df[f"humidity_lag_{lag}h"] = df["relative_humidity_2m"].shift(lag)
        df[f"wind_lag_{lag}h"] = df["wind_speed_10m"].shift(lag)

    # Change features
    df["temp_change_1h"] = df["temperature_2m"] - df["temperature_2m"].shift(1)
    df["humidity_change_1h"] = df["relative_humidity_2m"] - df["relative_humidity_2m"].shift(1)
    df["wind_change_1h"] = df["wind_speed_10m"] - df["wind_speed_10m"].shift(1)

    return df


# -------------------------------------------------
# Daily Aggregates
# -------------------------------------------------
def make_daily_aggregates(df):
    df = df.copy()

    df["date"] = df["time"].dt.date

    daily = df.groupby("date").agg({
        "temperature_2m": ["min", "max", "mean"],
        "relative_humidity_2m": ["min", "max", "mean"],
        "wind_speed_10m": ["max", "mean"],
        "precipitation": "sum",
        "cloud_cover": "mean",
        "surface_pressure": "mean"
    })

    daily.columns = ["_".join(col).rstrip("_") for col in daily.columns]

    return daily.reset_index()


# -------------------------------------------------
# Entrypoint (fixed)
# -------------------------------------------------
def transform_silver_to_gold(df_silver):

    print("\nRAW time samples BEFORE conversion:")
    print(df_silver["time"].head(10))

    # Work on a copy
    df_silver = df_silver.copy()

    # Convert timestamp to UTC timezone-aware
    df_silver["time"] = pd.to_datetime(
        df_silver["time"],
        utc=True,
        errors="coerce"
    )

    print("\nParsed time samples AFTER conversion:")
    print(df_silver["time"].head(10))

    # Convert to timezone-naive microsecond precision for Spark compatibility
    df_silver["time"] = df_silver["time"].dt.tz_localize(None)
    df_silver["time"] = df_silver["time"].astype("datetime64[us]")

    # ---- YOUR INDENTATION PROBLEM WAS *HERE* ----
    hourly = make_hourly_features(df_silver)
    daily = make_daily_aggregates(df_silver)

    return hourly, daily
