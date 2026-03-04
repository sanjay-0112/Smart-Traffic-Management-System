import streamlit as st

class DashboardComponents:
    """
    UI components used in the Streamlit dashboard.
    """

    def __init__(self):
        pass

    def show_metrics(self, metrics):
        """
        Display traffic statistics
        """

        col1, col2, col3 = st.columns(3)

        col1.metric(
            label="Total Vehicles",
            value=metrics.get("total_vehicles", 0)
        )

        col2.metric(
            label="Average Speed (km/h)",
            value=metrics.get("average_speed", 0)
        )

        col3.metric(
            label="Traffic Density",
            value=metrics.get("traffic_density", 0)
        )


    def show_congestion(self, congestion_level):
        """
        Display congestion status
        """

        if congestion_level == "High":
            st.error("🚨 High Traffic Congestion")

        elif congestion_level == "Medium":
            st.warning("⚠️ Moderate Traffic")

        else:
            st.success("✅ Traffic Flow Normal")


    def show_signal_decision(self, decision):
        """
        Display signal timing decision
        """

        st.subheader("🚦 Signal Control Decision")

        st.write(
            f"Green Signal Time: **{decision['green_signal_time']} seconds**"
        )

        if decision.get("predicted_traffic") is not None:
            st.write(
                f"Predicted Traffic: **{decision['predicted_traffic']:.2f} vehicles**"
            )


    def show_network_status(self):
        """
        Display simulated network status
        """

        st.sidebar.subheader("Network Status")

        st.sidebar.write("Sensor Nodes: Active")
        st.sidebar.write("Edge Server: Running")
        st.sidebar.write("Data Transmission: OK")