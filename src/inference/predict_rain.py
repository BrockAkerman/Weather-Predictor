from joblib import load
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Load trained model
# --------------------------------------------------
#MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "rain_next_hour_gbt.joblib"
MODEL_PATH = r"A:\Personal Files\Education\Data Science\Weather_Predictor\models\rain_next_hour_model.joblib"

artifact = load(MODEL_PATH)
model = artifact["model"]
features = artifact["features"]

# --------------------------------------------------
# Prediction function
# --------------------------------------------------
def predict_rain(input_dict: dict) -> float:
    """
    input_dict: dictionary of feature_name -> value
    returns: probability of rain next hour
    """
    df = pd.DataFrame([input_dict])

    # Enforce feature order
    df = df[features]

    prob = model.predict_proba(df)[0, 1]
    return float(prob)


# --------------------------------------------------
# Example run (local test)
# --------------------------------------------------
if __name__ == "__main__":
    sample = {
        "temperature_2m": 4.5,
        "relative_humidity_2m": 91,
        "dew_point_2m": 3.2,
        "precipitation_probability": 0,
        "precipitation": 0.0,
        "cloud_cover": 48,
        "surface_pressure": 988.5,
        "wind_speed_10m": 1.84,
        "wind_gusts_10m": 3.9,
        "wind_direction_10m": 299,
        "temp_lag_1h": 5.3,
        "humidity_lag_1h": 93,
        "wind_lag_1h": 1.6,
        "temp_lag_2h": 5.4,
        "humidity_lag_2h": 89,
        "wind_lag_2h": 2.4,
        "temp_lag_3h": 6.5,
        "humidity_lag_3h": 93,
        "wind_lag_3h": 2.0,
        "temp_change_1h": -0.8,
        "humidity_change_1h": -2.0,
        "wind_change_1h": 0.24
    }

    p = predict_rain(sample)
    print(f"Rain probability next hour: {p:.2%}")
