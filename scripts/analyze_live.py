import pandas as pd
from src.config import LIVE_DATA_PATH

def analyze_live_data():
    df = pd.read_csv(LIVE_DATA_PATH)

    if len(df) < 1:
        print("❌ No live data available yet.")
        return

    df["Datetime"] = pd.to_datetime(df["Datetime"])

    print("\n==============================")
    print(" SUMMARY OF LIVE PM2.5 DATA")
    print("==============================")
    print(df["PM2.5"].describe())

    print("\n==============================")
    print(" HOURLY AVERAGE PM2.5")
    print("==============================")
    df["hour"] = df["Datetime"].dt.hour
    print(df.groupby("hour")["PM2.5"].mean())

    print("\n==============================")
    print(" DAILY AVERAGE PM2.5")
    print("==============================")
    df["date"] = df["Datetime"].dt.date
    print(df.groupby("date")["PM2.5"].mean())

if __name__ == "__main__":
    analyze_live_data()

