import numpy as np
import cryptpandas as crp
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import os

from train import train_save

def retrain_predict(data_series, path, n_epochs=5, seq_length=32):
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

    model = tf.keras.models.load_model(path)
    model.fit(X, y, epochs=n_epochs)
    model.save(path)

    # Predictions
    def predict_future(model, data, scaler, seq_length, num_predictions):
        predictions = []
        current_sequence = data[-seq_length:]
        
        for _ in range(num_predictions):
            prediction = model.predict(current_sequence[np.newaxis, :, :])
            predictions.append(prediction[0, 0])
            current_sequence = np.append(current_sequence[1:], prediction, axis=0)
        
        return scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    future_points = predict_future(model, data_series_scaled, scaler, seq_length, 64)
    return future_points


def find_ratios(cryptname, cryptcode):
    length = len([name for name in os.listdir('./models')]) - 1
    df = crp.read_encrypted(path=f"./data/{cryptname}", password=cryptcode)[-512:]
    if len(df.columns) > length:
        for strat_num in range(length, len(df.columns)):
            filepath = f"./models/lstm_{strat_num}.keras"
            series = df[df.columns[strat_num]].replace([np.inf, -np.inf], np.nan).dropna().cumsum().values.reshape(-1, 1)
            print(strat_num)
            train_save(series, filepath)

    ret = [0] * length
    vol = [0] * length
    for strat_num in range(length):
        filepath = f"./models/lstm_{strat_num}.keras"
        series = df[df.columns[strat_num]].replace([np.inf, -np.inf], np.nan).dropna().cumsum().values.reshape(-1, 1)
        print(strat_num)
        future_points = retrain_predict(series, filepath, n_epochs=3).flatten()
        ret[strat_num] = future_points[-1] - future_points[1]
        vol[strat_num] = np.log(series.std())

    ratios = np.divide(ret, vol)
    ratios[9] = 0
    np.save("ratios.npy", np.array(ratios))
    return ratios

def greedy_allocate(arr):
    ranked = list(sorted(arr, key=abs,reverse=True))[:10]
    weights = [0] * len(arr)
    for i, n in enumerate(arr):
        if n in ranked:
            weights[i] = 0.1 if n > 0 else -0.1
    return weights

def convert_to_submission(weights):
    res = dict()
    for i in range(len(weights)):
        res[f"strat_{i}"] = weights[i]
    res['team_name'] = 'Yoghurt'
    res['passcode'] = 'yoghurt'
    return res


def get_submit(name, code):
    ratios = find_ratios(name, code)
    return convert_to_submission(greedy_allocate(ratios))

# print(get_submit("release_5787.crypt", "udaxEolZcR3jRgDO"))
# ratios = np.load("ratios.npy")
# ratios[9] = 0
# print(ratios)
# print(convert_to_submission(greedy_allocate(ratios)))
