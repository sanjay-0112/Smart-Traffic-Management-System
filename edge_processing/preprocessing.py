import pandas as pd


class EdgePreprocessor:
    """
    Simulates preprocessing done at the edge server.
    Cleans incoming sensor data before analysis.
    """

    def __init__(self):
        pass

    def clean_sensor_data(self, sensor_messages):
        """
        Convert raw sensor messages into structured dataframe
        """

        df = pd.DataFrame(sensor_messages)

        # Handle missing values
        df = df.fillna({
            "vehicle_count": 0,
            "avg_speed": 0
        })

        # Ensure numeric types
        df["vehicle_count"] = pd.to_numeric(df["vehicle_count"], errors="coerce")
        df["avg_speed"] = pd.to_numeric(df["avg_speed"], errors="coerce")

        return df

    def smooth_traffic(self, df):
        """
        Simple smoothing of vehicle counts to remove noise
        """

        if "vehicle_count" in df.columns:
            df["vehicle_count_smooth"] = df["vehicle_count"].rolling(
                window=2, min_periods=1
            ).mean()

        return df