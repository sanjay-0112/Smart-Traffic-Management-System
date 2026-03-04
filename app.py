import streamlit as st
import pandas as pd
import random

from streamlit_autorefresh import st_autorefresh

from simulation.sensor_simulator import SensorSimulator
from edge_processing.preprocessing import EdgePreprocessor
from edge_processing.traffic_metrics import TrafficMetrics
from control.signal_controller import SignalController
from dashboard.charts import TrafficCharts
from dashboard.dashboard_components import DashboardComponents
from models.model_utils import ModelComparison

# -----------------------------
# Page configuration & Custom CSS
# -----------------------------
st.set_page_config(page_title="Smart Traffic Management System", layout="wide")

# Custom CSS for the "Beautiful" UI
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #00d4ff; }
    .status-card {
        background-color: #1a1c24;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #31333f;
        text-align: center;
        margin-bottom: 10px;
    }
    .css-10trblm { color: #808495; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# Header Section
# -----------------------------
t_col1, t_col2 = st.columns([3, 1])
with t_col1:
    st.title("🚦 Smart Traffic Management System")
    st.caption("IoT + Edge Networking Real-Time Traffic Simulation")

# -----------------------------
# Sidebar & Network Status
# -----------------------------
with st.sidebar:
    st.header("🛰️ Network Control")
    ui = DashboardComponents()
    ui.show_network_status()
    st.divider()
    st.info("System Status: Active")
    st.progress(0.85, text="Edge Node Sync")

# -----------------------------
# Auto refresh (5 seconds)
# -----------------------------
st_autorefresh(interval=5000, key="traffic_refresh")

# -----------------------------
# Initialize components
# -----------------------------
DATASET_PATH = "data/traffic_simulation.csv"
sensor_sim = SensorSimulator(DATASET_PATH)
preprocessor = EdgePreprocessor()
metrics_engine = TrafficMetrics()
charts = TrafficCharts()
model_compare = ModelComparison()

# -----------------------------
# Data Processing Logic (UNCHANGED)
# -----------------------------
sensor_data = sensor_sim.read_all_sensors()
df = preprocessor.clean_sensor_data(sensor_data)
df = preprocessor.smooth_traffic(df)
df["vehicle_count"] = df["vehicle_count"].round().astype(int)

if "traffic_df" not in st.session_state:
    st.session_state.traffic_df = df
else:
    df = st.session_state.traffic_df

if "previous_yellow" not in st.session_state:
    st.session_state.previous_yellow = None

# Simulation logic (UNCHANGED)
arrival_lane = random.choice(df["sensor_name"].tolist())
arrival_count = random.randint(2, 3)
yellow_lane = None

for i in range(len(df)):
    lane = df.loc[i, "sensor_name"]
    vehicles = df.loc[i, "vehicle_count"]
    if lane == arrival_lane:
        vehicles += arrival_count
    if lane == st.session_state.previous_yellow:
        departure = random.randint(3, 5)
    elif lane == yellow_lane:
        departure = random.randint(1, 2)
    else:
        departure = random.randint(0, 1)
    vehicles -= departure
    vehicles = max(0, min(vehicles, 30))
    df.loc[i, "vehicle_count"] = vehicles

for i in range(len(df)):
    vehicles = df.loc[i, "vehicle_count"]
    speed = max(15, 60 - vehicles * 2 + random.randint(-3, 3))
    df.loc[i, "avg_speed"] = speed

st.session_state.traffic_df = df
metrics = metrics_engine.compute_metrics(df)

# -----------------------------
# TOP METRICS ROW
# -----------------------------
st.subheader("📍 Live Network Metrics")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Vehicles", metrics["total_vehicles"], delta=f"{arrival_count} new")
m2.metric("Avg Speed", f"{int(df['avg_speed'].mean())} km/h")
m3.metric("Congestion", metrics["congestion_level"])
m4.metric("Flow Rate", f"{random.randint(85, 98)}%")

st.divider()

# -----------------------------
# SIGNAL & PREDICTION SECTION
# -----------------------------
# Historical & Prediction Logic (UNCHANGED)
if "traffic_history" not in st.session_state:
    st.session_state.traffic_history = []
st.session_state.traffic_history.append(metrics["total_vehicles"])
history_df = pd.DataFrame({"vehicle_count": st.session_state.traffic_history})

results = model_compare.run_models(history_df)
comparison = model_compare.compare_models(results)
arima_prediction = comparison["ARIMA_prediction"]
lstm_prediction = comparison["LSTM_prediction"]
prediction = arima_prediction if arima_prediction else metrics["total_vehicles"]

# Signal Timing Logic (UNCHANGED)
if prediction > 40:
    green_time = 60
elif prediction > 20:
    green_time = 45
else:
    green_time = 30

if "signal_timer" not in st.session_state:
    st.session_state.signal_timer = 0

sorted_lanes = df.sort_values("vehicle_count", ascending=False)

if st.session_state.signal_timer == 0:
    yellow_lane = sorted_lanes.iloc[0]["sensor_name"]
    green_lane = st.session_state.previous_yellow
    for lane in sorted_lanes["sensor_name"]:
        if lane != green_lane:
            yellow_lane = lane
            break
    st.session_state.previous_yellow = yellow_lane
    st.session_state.signal_timer = int(green_time / 3)
else:
    st.session_state.signal_timer -= 1
    green_lane = st.session_state.previous_yellow
    yellow_lane = None
    for lane in sorted_lanes["sensor_name"]:
        if lane != green_lane:
            yellow_lane = lane
            break

# -----------------------------
# VISUAL SIGNAL STATUS CARDS
# -----------------------------
st.subheader("🚦 Intersection Status")
lanes = df["sensor_name"].tolist()
signal_cols = st.columns(len(lanes))

for idx, lane in enumerate(lanes):
    with signal_cols[idx]:
        if lane == green_lane:
            color, label, icon = "#28a745", "CLEAR", "🟢"
        elif lane == yellow_lane:
            color, label, icon = "#ffc107", "SLOW", "🟡"
        else:
            color, label, icon = "#dc3545", "STOP", "🔴"

        st.markdown(f"""
            <div class="status-card" style="border-top: 5px solid {color};">
                <small style="color: #808495;">{lane.upper()}</small>
                <h2 style="margin: 10px 0;">{icon}</h2>
                <strong style="color: {color};">{label}</strong>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# -----------------------------
# CHARTS & ANALYTICS TABS
# -----------------------------
tab1, tab2 = st.tabs(["📊 Traffic Analysis", "🧠 AI Predictions"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.pyplot(charts.vehicle_count_chart(df), use_container_width=True)
    with col_b:
        st.pyplot(charts.speed_chart(df), use_container_width=True)

with tab2:
    p_col1, p_col2 = st.columns([1, 2])
    with p_col1:
        st.markdown("### Model Insights")
        st.metric("ARIMA", int(arima_prediction) if arima_prediction else "N/A")
        st.metric("LSTM", int(lstm_prediction) if lstm_prediction else "N/A")
        st.success(f"Best: {comparison['best_model']}")
        st.info(f"Adaptive Green: {green_time}s")
    with p_col2:
        st.pyplot(charts.prediction_chart(st.session_state.traffic_history, prediction))

# Final Footer Step
st.caption("System running in real-time. Data refreshes every 5s.")