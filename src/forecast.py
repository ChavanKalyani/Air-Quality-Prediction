import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import pickle
import os
from src.config import LIVE_DATA_PATH, MODEL_PATH, TIME_STEPS

PRED_SAVE_PATH = "data/predictions/latest_forecast.csv"
PLOT_SAVE_PATH = "plots/forecast_plot.png"

def load_live_data():
    df = pd.read_csv(LIVE_DATA_PATH)
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df = df.sort_values("Datetime")

    pm25 = df["PM2.5"].values[-TIME_STEPS:]

    if len(pm25) < TIME_STEPS:
        raise ValueError(f"Need at least {TIME_STEPS} live data points for forecasting.")

    return pm25.reshape(-1, 1)


def forecast_future(hours=24):

    # Load scaler
    with open("models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    # Load trained LSTM model
    model = load_model(MODEL_PATH, compile=False)
    model.compile(optimizer="adam", loss="mse")

    # Load last 30 live values
    last_data = load_live_data()
    scaled_input = scaler.transform(last_data)
    input_seq = scaled_input.reshape(1, TIME_STEPS, 1)

    predictions = []

    for _ in range(hours):
        pred_scaled = model.predict(input_seq, verbose=0)
        predictions.append(pred_scaled[0, 0])

        # Sliding window update
        next_step = pred_scaled.reshape(1, 1, 1)
        input_seq = np.concatenate((input_seq[:, 1:, :], next_step), axis=1)

    # Convert back to original units
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    future_times = pd.date_range(start=pd.Timestamp.now(), periods=hours, freq="H")

    df_pred = pd.DataFrame({
        "datetime": future_times,
        "predicted_pm25": predictions.flatten()
    })

    # ------------------------------
    #  SAVE CSV
    # ------------------------------
    os.makedirs("data/predictions", exist_ok=True)
    df_pred.to_csv(PRED_SAVE_PATH, index=False)
    print(f"Predictions saved to: {PRED_SAVE_PATH}")

    # ------------------------------
    #  SAVE PLOT
    # ------------------------------
    os.makedirs("plots", exist_ok=True)

    plt.figure(figsize=(12, 5))
    plt.plot(df_pred["datetime"], df_pred["predicted_pm25"], marker="o")
    plt.title("Next 24-Hour PM2.5 Forecast")
    plt.xlabel("Time")
    plt.ylabel("Predicted PM2.5")
    plt.grid(True)
    plt.savefig(PLOT_SAVE_PATH)
    plt.close()

    print(f"Forecast plot saved to: {PLOT_SAVE_PATH}")

    return df_pred


if __name__ == "__main__":
    df = forecast_future()
    print(df.head())
