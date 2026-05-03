import streamlit as st
import cv2
import time
import config
import os
from detector import HumanDetector
from tracker import HumanTracker
from utils import draw_bounding_boxes_and_paths
from line_crossing import LineCrossingCounter

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Human Tracking", page_icon="🛡️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stMetric {
        background-color: #1e1e2e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #45475a;
    }
    div[data-testid="stMetricValue"] {
        color: #00e5ff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AI Human Tracking System")
st.markdown("### Core Analytics Dashboard")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ System Controls")
confidence = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.5)
source_toggle = st.sidebar.radio("Video Source", ["Webcam", "Video File"])

if 'running' not in st.session_state:
    st.session_state.running = False

col_start, col_stop = st.sidebar.columns(2)
if col_start.button("▶️ Start", use_container_width=True, type="primary"):
    st.session_state.running = True
if col_stop.button("⏹️ Stop", use_container_width=True):
    st.session_state.running = False

# --- MAIN DASHBOARD ---
# Top Metrics Row (Removed Occupancy/Inside Building)
col1, col2, col3, col4, col5 = st.columns(5)
metric_total = col1.empty()
metric_active = col2.empty()
metric_in = col3.empty()
metric_out = col4.empty()
metric_fps = col5.empty()

# Initialization
metric_total.metric("Total Unique People", 0)
metric_active.metric("Active IDs", 0)
metric_in.metric("IN Count", 0)
metric_out.metric("OUT Count", 0)
metric_fps.metric("FPS", 0)

st.markdown("### 🎥 Live Tracking Feed")
video_placeholder = st.empty()

# --- PROCESSING LOOP ---
if st.session_state.running:
    config.CONFIDENCE_THRESHOLD = confidence
    video_src = 0 if source_toggle == "Webcam" else os.path.join(config.BASE_DIR, 'videos', 'pedestrians.mp4')
    cap = cv2.VideoCapture(video_src)
    
    detector = HumanDetector()
    tracker = HumanTracker()
    line_counter = LineCrossingCounter(int(cap.get(3)), int(cap.get(4)), line_position=0.5)
    unique_ids_seen = set()
    
    while st.session_state.running:
        loop_start = time.time()
        ret, frame = cap.read()
        if not ret: break
        
        tracks = tracker.update_tracks(detector.detect_people(frame))
        frame = draw_bounding_boxes_and_paths(frame, tracks)
        line_counter.update(tracks)
        frame = line_counter.draw_ui(frame)
        
        for track in tracks: unique_ids_seen.add(int(track[4]))
        
        metric_total.metric("Total Unique People", len(unique_ids_seen))
        metric_active.metric("Active IDs", len(tracks))
        metric_in.metric("IN Count", line_counter.in_count)
        metric_out.metric("OUT Count", line_counter.out_count)
        metric_fps.metric("FPS", int(1.0 / (time.time() - loop_start + 1e-6)))
        
        video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
    cap.release()
else:
    video_placeholder.info("System Standby. Use the sidebar to start tracking.")
