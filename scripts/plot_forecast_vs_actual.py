import pandas as pd
import matplotlib.pyplot as plt
from src.forecast import forecast_future
from src.config import LIVE_DATA_PATH, TIME_STEPS

def plot_forecast_vs_actual():
    # Load real live data
    df_live = pd.read_csv(LIVE_DATA_PATH)
    df_live["Datetime"] = pd.to_datetime(df_live["Datetime"])
    df_live = df_live.sort_values("Datetime")

    # Take last TIME_STEPS real values
    df_live_recent = df_live.tail(TIME_STEPS)

    # Run forecasting
    df_forecast = forecast_future(hours=24)

    # Plot
    plt.figure(figsize=(12, 6))

    # REAL DATA
    plt.plot(df_live_recent["Datetime"], df_live_recent["PM2.5"],
             label="Real PM2.5 (last 30 readings)", color="blue", marker="o")

    # FORECASTED DATA
    plt.plot(df_forecast["datetime"], df_forecast["predicted_pm25"],
             label="Forecasted PM2.5 (next 24 hours)", color="red", marker="o")

    # Labels and title
    plt.xlabel("Time")
    plt.ylabel("PM2.5  (µg/m³)")
    plt.title("Real vs Forecasted PM2.5")
    plt.grid(True)
    plt.legend()

    # Show plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_forecast_vs_actual()
