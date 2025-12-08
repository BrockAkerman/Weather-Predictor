import pandas as pd
from datetime import datetime

def normalize_weather_json(raw):
    """
    Convert Open-Meteo hourly JSON into a proper Silver dataframe.
    """

    # -------------------------
    # 1. Validate structure
    # -------------------------
    if "hourly" not in raw:
        raise ValueError("Expected key 'hourly' in JSON payload")

    hourly = raw["hourly"]

    # -------------------------
    # 2. Ensure all hourly fields align
    # -------------------------
    main_len = len(hourly["time"])
    for k, v in hourly.items():
        if len(v) != main_len:
            raise ValueError(f"Hourly field '{k}' has mismatched length.")

    # -------------------------
    # 3. Build proper hourly dataframe
    # -------------------------
    df = pd.DataFrame(hourly)

    # -------------------------
    # 4. Timestamp parsing
    # -------------------------
    # Open-Meteo timestamps are ISO8601 strings
    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")

    # -------------------------
    # 5. Standardize column names
    # -------------------------
    df = df.rename(columns=lambda c: c.lower())

    # -------------------------
    # 6. Add Silver metadata
    # -------------------------
    df["silver_loaded_at"] = datetime.utcnow()

    return df
