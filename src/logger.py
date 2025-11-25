import requests
import pandas as pd
import time
from datetime import datetime
from src.config import LIVE_DATA_PATH, WAQI_CITY, WAQI_TOKEN

RETRY_INTERVAL = 300      # retry every 5 minutes when internet fails
SUCCESS_INTERVAL = 1800   # fetch every half an  hour


def fetch_pm25():
    """
    Fetch PM2.5 from WAQI API.
    Returns integer PM2.5 value or None if API fails.
    """
    url = f"https://api.waqi.info/feed/{WAQI_CITY}/?token={WAQI_TOKEN}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data["status"] != "ok":
            print(f"[{datetime.now()}] API Error: {data}")
            return None

        pm25 = data["data"]["iaqi"]["pm25"]["v"]
        return pm25

    except Exception as e:
        print(f"[{datetime.now()}] Connection error: {e}")
        return None


def log_pm25():
    """
    Runs forever: fetch PM2.5 every half an hour with retry protection.
    Writes new rows to live_pm25_log.csv safely.
    """
    print("\n🟢 Real-time logger started (safe mode)")
    print("   - Hourly fetch")
    print("   - Auto-retry on failure")
    print("   - Writing to:", LIVE_DATA_PATH, "\n")

    while True:
        pm25 = fetch_pm25()

        if pm25 is None:
            print(f"[{datetime.now()}] ❌ Failed. Retrying in 5 minutes...\n")
            time.sleep(RETRY_INTERVAL)
            continue

        # Success
        now = datetime.now()

        # Append to CSV
        df_new = pd.DataFrame({"Datetime": [now], "PM2.5": [pm25]})

        try:
            df_old = pd.read_csv(LIVE_DATA_PATH)
            df = pd.concat([df_old, df_new], ignore_index=True)
        except:
            df = df_new  # file doesn't exist yet → create it

        df.to_csv(LIVE_DATA_PATH, index=False)

        print(f"[{now}] Logged PM2.5 =", pm25)
        print(f"   Next update in 0.5 hour...\n")

        # Sleep for 1 hour
        time.sleep(SUCCESS_INTERVAL)

if __name__=="__main__":
            log_pm25()
