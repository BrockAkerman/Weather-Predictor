from pathlib import Path
import json
import pandas as pd
from datetime import datetime

from silver_transform import normalize_weather_json

# --------------------------------------------------
# 1. Paths (fixed: only go up ONE directory)
# --------------------------------------------------
# run_silver.py is in src/etl → need to go up twice to reach project root
base_dir = Path(__file__).resolve().parents[2]


bronze_path = base_dir / "data" / "bronze"
silver_path = base_dir / "data" / "silver"

silver_path.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Find latest bronze file
# --------------------------------------------------
json_files = sorted(bronze_path.glob("raw_*.json"))
if not json_files:
    raise FileNotFoundError(f"No JSON files found in {bronze_path}")

latest_file = json_files[-1]
print(f"Using latest bronze file: {latest_file.name}")

# --------------------------------------------------
# 3. Load JSON
# --------------------------------------------------
with open(latest_file, "r") as f:
    data = json.load(f)

# --------------------------------------------------
# 4. Transform → Silver
# --------------------------------------------------
df_silver = normalize_weather_json(data)

print("Silver transformation complete!")
print(df_silver.head())

# --------------------------------------------------
# 5. Save parquet
# --------------------------------------------------
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = silver_path / f"silver_{timestamp}.parquet"
df_silver.to_parquet(output_file, index=False)

print(f"Silver file saved: {output_file}")
