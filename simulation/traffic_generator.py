import pandas as pd
import random


class TrafficGenerator:

    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)

        if "DateTime" in self.df.columns:
            self.df["DateTime"] = pd.to_datetime(self.df["DateTime"])

        self.index = 0

    def get_next_data(self):

        if self.index >= len(self.df):
            self.index = 0

        row = self.df.iloc[self.index]
        self.index += 1

        traffic_data = {
            "timestamp": row.get("DateTime", None),
            "junction": row.get("Junction", 1),
            "vehicle_count": row.get("Vehicles", random.randint(10, 50))
        }

        return traffic_data