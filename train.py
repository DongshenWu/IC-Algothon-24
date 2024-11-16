import numpy as np
import cryptpandas as crp
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

def train_save(data_series, path, n_epochs=5, seq_length=64):
    scaler = MinMaxScaler()
    data_series_scaled = scaler.fit_transform(data_series)

    # Create sequences
    def create_sequences(data, seq_length):
        sequences = []
        labels = []
        for i in range(len(data) - seq_length):
            sequences.append(data[i:i + seq_length])
            labels.append(data[i + seq_length])
        return np.array(sequences), np.array(labels)
    
    X, y = create_sequences(data_series_scaled, seq_length)

    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(shape=(seq_length, 1)),
        tf.keras.layers.LSTM(100, return_sequences=True),
        tf.keras.layers.LSTM(100, return_sequences=True),
        tf.keras.layers.LSTM(100),
        tf.keras.layers.Dense(50, activation='relu'),
        tf.keras.layers.Dropout(0.05),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')
    
    model.fit(X, y, epochs=n_epochs)

    model.save(path)

# df = crp.read_encrypted(path="./data/release_4827.crypt", password='KZpaNLmv4lDHBN6O')

# for strat_num in range(len(df)):
#     filepath = f"./models/lstm_{strat_num}.keras"
#     series = df[df.columns[strat_num]].replace([np.inf, -np.inf], np.nan).dropna().cumsum().values.reshape(-1, 1)
#     train_save(series, filepath)
