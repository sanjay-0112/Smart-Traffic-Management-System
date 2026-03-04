import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


class ARIMATrafficPredictor:
    """
    Uses ARIMA model to predict short-term traffic flow.
    """

    def __init__(self):
        self.model = None
        self.model_fit = None

    def train(self, df):
        """
        Train ARIMA model using vehicle count time series
        """

        if "vehicle_count" not in df.columns:
            raise ValueError("vehicle_count column missing")

        series = df["vehicle_count"]

        # ARIMA(p,d,q)
        self.model = ARIMA(series, order=(2, 1, 2))
        self.model_fit = self.model.fit()

    def predict(self, steps=5):
        """
        Predict next traffic values
        """

        if self.model_fit is None:
            return []

        forecast = self.model_fit.forecast(steps=steps)

        return forecast.tolist()