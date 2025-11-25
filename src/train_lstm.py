import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from src.config import HIST_DATA_PATH, MODEL_PATH, TIME_STEPS
from src.preprocess import load_and_scale, create_sequences

print(">>> TRAIN LSTM STARTED")
print("HIST_DATA_PATH =", HIST_DATA_PATH)


def train_model():
  print(">>> Loading CSV...")
df = pd.read_csv(HIST_DATA_PATH)
print(">>> CSV Loaded. Shape =", df.shape)
print(">>> Columns =", df.columns.tolist())

df["Datetime"] = pd.to_datetime(df["Datetime"])
df = df[df["City"] == "Delhi"].sort_values("Datetime")
print(">>> After filtering Delhi, shape =", df.shape)


df["PM2.5"] = df["PM2.5"].interpolate()
df = df[["PM2.5"]]

print(">>> Starting model training...")

scaled, scaler = load_and_scale(df)
X, y = create_sequences(scaled)

model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(TIME_STEPS, 1)),
        Dropout(0.2),
        LSTM(64),
        Dense(32, activation="relu"),
        Dense(1)
    ])

model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=20, batch_size=32)

model.save(MODEL_PATH)
print("Training complete. Model saved to:", MODEL_PATH)
