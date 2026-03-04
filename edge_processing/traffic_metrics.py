import pandas as pd


class TrafficMetrics:
    """
    Calculates traffic statistics from processed sensor data.
    These metrics help determine congestion levels and signal decisions.
    """

    def __init__(self):
        pass

    def compute_metrics(self, df):

        metrics = {}

        # Total vehicles detected
        total_vehicles = df["vehicle_count"].sum()

        # Average vehicle speed
        avg_speed = df["avg_speed"].mean()

        # Traffic density approximation
        density = total_vehicles / max(len(df), 1)

        metrics["total_vehicles"] = total_vehicles
        metrics["average_speed"] = round(avg_speed, 2)
        metrics["traffic_density"] = round(density, 2)

        # Determine congestion level
        if density > 20:
            congestion = "High"
        elif density > 10:
            congestion = "Medium"
        else:
            congestion = "Low"

        metrics["congestion_level"] = congestion

        return metrics