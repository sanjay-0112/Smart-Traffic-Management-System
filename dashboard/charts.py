import matplotlib.pyplot as plt
import pandas as pd


class TrafficCharts:
    """
    Generates charts for the Streamlit dashboard.
    """

    def __init__(self):
        pass

    def vehicle_count_chart(self, df):
        """
        Plot vehicle count per sensor
        """

        fig, ax = plt.subplots()

        ax.bar(
            df["sensor_name"],
            df["vehicle_count"]
        )

        ax.set_xlabel("Sensors")
        ax.set_ylabel("Vehicle Count")
        ax.set_title("Vehicle Count per Lane")

        return fig


    def speed_chart(self, df):
        """
        Plot average speed per sensor
        """

        fig, ax = plt.subplots()

        ax.bar(
            df["sensor_name"],
            df["avg_speed"]
        )

        ax.set_xlabel("Sensors")
        ax.set_ylabel("Average Speed (km/h)")
        ax.set_title("Average Speed per Lane")

        return fig


    def prediction_chart(self, history, prediction):
        """
        Plot historical traffic and predicted value
        """

        fig, ax = plt.subplots()

        ax.plot(history, label="Historical Traffic")

        ax.scatter(
            len(history),
            prediction,
            label="Predicted Traffic"
        )

        ax.set_xlabel("Time Step")
        ax.set_ylabel("Vehicle Count")
        ax.set_title("Traffic Prediction")

        ax.legend()

        return fig