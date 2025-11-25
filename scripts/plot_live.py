import pandas as pd
import matplotlib.pyplot as plt
from src.config import LIVE_DATA_PATH

def plot_live_trend():
    df = pd.read_csv(LIVE_DATA_PATH)

    if len(df) < 1:
        print("❌ No live data available yet.")
        return

    df["Datetime"] = pd.to_datetime(df["Datetime"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["Datetime"], df["PM2.5"], marker="o", linewidth=2)
    plt.title("Live PM2.5 Trend (Real-time Data)", fontsize=16)
    plt.xlabel("Time")
    plt.ylabel("PM2.5 µg/m³")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.close()
if __name__ == "__main__":
    plot_live_trend()

