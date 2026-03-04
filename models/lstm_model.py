import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler


class LSTMTrafficPredictor:
    """
    Simple LSTM model for traffic flow prediction.
    """

    def __init__(self, sequence_length=5):

        self.sequence_length = sequence_length
        self.model = None
        self.scaler = MinMaxScaler()

    def prepare_data(self, series):

        data = series.values.reshape(-1, 1)

        scaled = self.scaler.fit_transform(data)

        X = []
        y = []

        for i in range(len(scaled) - self.sequence_length):
            X.append(scaled[i:i + self.sequence_length])
            y.append(scaled[i + self.sequence_length])

        return np.array(X), np.array(y)

    def train(self, df):

        if "vehicle_count" not in df.columns:
            raise ValueError("vehicle_count column missing")

        series = df["vehicle_count"]

        X, y = self.prepare_data(series)

        self.model = Sequential()

        self.model.add(
            LSTM(32, input_shape=(self.sequence_length, 1))
        )

        self.model.add(Dense(1))

        self.model.compile(
            optimizer="adam",
            loss="mse"
        )

        self.model.fit(
            X,
            y,
            epochs=5,
            batch_size=8,
            verbose=0
        )

    def predict(self, series):

        last_values = series.values[-self.sequence_length:]
        last_values = last_values.reshape(-1, 1)

        scaled = self.scaler.transform(last_values)

        X = scaled.reshape(1, self.sequence_length, 1)

        prediction = self.model.predict(X, verbose=0)

        value = self.scaler.inverse_transform(prediction)

        return float(value[0][0])