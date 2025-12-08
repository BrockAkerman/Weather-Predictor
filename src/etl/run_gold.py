import pandas as pd
from pathlib import Path
from datetime import datetime

from silver_to_gold import transform_silver_to_gold
from add_labels import add_ml_labels

# ---------------------------------------------------------
# Set project root path based on THIS file's location
# ---------------------------------------------------------
base_dir = Path(__file__).resolve().parents[2]

silver_path = base_dir / "data" / "silver"
gold_path = base_dir / "data" / "gold"

gold_path.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load latest Silver parquet
# ---------------------------------------------------------
silver_files = sorted(silver_path.glob("silver_*.parquet"))
if not silver_files:
    raise FileNotFoundError(f"No silver files found in {silver_path}")

latest = silver_files[-1]
print(f"Using Silver file: {latest}")

df_silver = pd.read_parquet(latest)
print(f"Loaded {len(df_silver)} rows and {len(df_silver.columns)} columns from silver.")

# Show columns
print("\nSilver Columns:")
for col in df_silver.columns:
    print("  -", col)

# ---------------------------------------------------------
# Transform to Gold
# ---------------------------------------------------------
df_hourly, df_daily = transform_silver_to_gold(df_silver)

# Add ML labels
df_hourly = add_ml_labels(df_hourly)

print("\nGold transformation complete!")
print("\nHourly sample:")
print(df_hourly.head())

print("\nDaily sample:")
print(df_daily.head())

# ---------------------------------------------------------
# Save Gold datasets
# ---------------------------------------------------------
date_tag = datetime.now().strftime("%Y%m%d")

hourly_file = gold_path / f"hourly_features_{date_tag}.parquet"
daily_file = gold_path / f"daily_aggregates_{date_tag}.parquet"

df_hourly.to_parquet(hourly_file, index=False)
df_daily.to_parquet(daily_file, index=False)

print(f"\nSaved hourly -> {hourly_file}")
print(f"Saved daily  -> {daily_file}")

# ---------------------------------------------------------
# (NEW) Save ML-ready dataset (Option B)
# ---------------------------------------------------------

ml_ready_path = gold_path / "ml_ready_hourly.parquet"
df_ml = df_hourly.copy()

# Remove metadata columns that are NOT features
cols_to_drop = ["silver_loaded_at"]
df_ml = df_ml.drop(columns=[c for c in cols_to_drop if c in df_ml.columns])

df_ml.to_parquet(ml_ready_path, index=False)
print(f"\nSaved ML-ready dataset -> {ml_ready_path}")
