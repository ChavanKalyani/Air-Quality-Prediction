import os

# === API SETTINGS ===
WAQI_TOKEN = "cfc8072c24493f9282708ddc6ce10ac043db8ec5"  
CITY = "delhi"

WAQI_CITY = CITY 

# === PATH SETTINGS ===
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LIVE_DATA_PATH = os.path.join(BASE_DIR, "data", "live", "live_pm25_log.csv")
HIST_DATA_PATH = os.path.join(BASE_DIR, "data", "historical", "city_hour.csv")

SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "models", "lstm_model.h5")

# === MODEL PARAMETERS ===
TIME_STEPS = 30
FUTURE_HOURS = 24
