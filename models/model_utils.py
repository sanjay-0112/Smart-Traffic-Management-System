from models.arima_model import ARIMATrafficPredictor
from models.lstm_model import LSTMTrafficPredictor


class ModelComparison:
    """
    Utility class to compare ARIMA and LSTM traffic predictions.
    """

    def __init__(self):

        self.arima = ARIMATrafficPredictor()
        self.lstm = LSTMTrafficPredictor()

    def run_models(self, df):
        """
        Train both models and generate predictions
        """

        if "vehicle_count" not in df.columns:
            raise ValueError("vehicle_count column missing")

        results = {}

        # ---- ARIMA ----
        self.arima.train(df)
        arima_pred = self.arima.predict(steps=1)

        results["ARIMA"] = arima_pred[0] if len(arima_pred) > 0 else None

        # ---- LSTM ----
        try:
            self.lstm.train(df)
            lstm_pred = self.lstm.predict(df["vehicle_count"])

            results["LSTM"] = lstm_pred

        except Exception:
            # If LSTM fails due to small dataset
            results["LSTM"] = None

        return results

    def compare_models(self, results):
        """
        Determine which model predicts higher traffic
        """

        arima_val = results.get("ARIMA")
        lstm_val = results.get("LSTM")

        comparison = {}

        comparison["ARIMA_prediction"] = arima_val
        comparison["LSTM_prediction"] = lstm_val

        if arima_val is None and lstm_val is None:
            comparison["best_model"] = "None"

        elif lstm_val is None:
            comparison["best_model"] = "ARIMA"

        elif arima_val is None:
            comparison["best_model"] = "LSTM"

        else:
            if lstm_val > arima_val:
                comparison["best_model"] = "LSTM"
            else:
                comparison["best_model"] = "ARIMA"

        return comparison