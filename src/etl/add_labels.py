import pandas as pd

def add_ml_labels(df):
    df = df.copy()

    # Rain in next hour? (you can adjust threshold)
    df["rain_next_hour"] = (df["precipitation"].shift(-1) > 0.2).astype(int)

    # Optional: 3h lookahead window
    df["rain_next_3h"] = (
        df["precipitation"].rolling(window=3, min_periods=1).max().shift(-3) > 0.2
    ).astype(int)

    return df
