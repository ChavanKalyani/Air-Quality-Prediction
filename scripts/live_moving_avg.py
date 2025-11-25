import pandas as pd
import matplotlib.pyplot as plt
from src.config import LIVE_DATA_PATH

def plot_moving_avg():
    df = pd.read_csv(LIVE_DATA_PATH)

    if len(df) < 5:
        print("❌ Need at least 5 data points for moving average.")
        return

    df["Datetime"] = pd.to_datetime(df["Datetime"])

    df["MA5"] = df["PM2.5"].rolling(window=5).mean()
    df["MA10"] = df["PM2.5"].rolling(window=10).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(df["Datetime"], df["PM2.5"], label="Raw PM2.5", alpha=0.5)
    plt.plot(df["Datetime"], df["MA5"], label="5-point MA", linewidth=2)
    plt.plot(df["Datetime"], df["MA10"], label="10-point MA", linewidth=2)

    plt.title("Live PM2.5 Moving Average Trend", fontsize=16)
    plt.xlabel("Time")
    plt.ylabel("PM2.5 µg/m³")
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_moving_avg()
