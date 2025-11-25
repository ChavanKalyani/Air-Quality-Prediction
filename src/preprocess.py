import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler
from src.config import TIME_STEPS, SCALER_PATH

def load_and_scale(df):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[["PM2.5"]])

    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    return scaled, scaler

def create_sequences(data):
    X, y = [], []
    for i in range(TIME_STEPS, len(data)):
        X.append(data[i-TIME_STEPS:i, 0])
        y.append(data[i, 0])
    return (
        np.array(X).reshape(-1, TIME_STEPS, 1),
        np.array(y)
    )
