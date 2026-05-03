import streamlit as st
import cv2
import time
import config
import os
from detector import HumanDetector
from tracker import HumanTracker
from utils import draw_bounding_boxes_and_paths
from line_crossing import LineCrossingCounter

st.set_page_config(page_title="Fire Safety Monitor", page_icon="🔥", layout="wide")

st.title("🔥 Fire Safety & Evacuation Monitor")
st.markdown("### Real-time Building Occupancy Tracker")

# Sidebar
st.sidebar.header("Navigation")
st.sidebar.info("Currently on: Fire Safety Monitor")
confidence = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.5)
start_btn = st.sidebar.button("▶️ Start Monitoring", use_container_width=True, type="primary")
stop_btn = st.sidebar.button("⏹️ Stop Monitoring", use_container_width=True)

if 'fire_running' not in st.session_state:
    st.session_state.fire_running = False

if start_btn: st.session_state.fire_running = True
if stop_btn: st.session_state.fire_running = False

# Metrics
col1, col2, col3, col4 = st.columns(4)
m_occupancy = col1.empty()
m_in = col2.empty()
m_out = col3.empty()
m_fps = col4.empty()

video_placeholder = st.empty()

if st.session_state.fire_running:
    config.CONFIDENCE_THRESHOLD = confidence
    # UPDATED VIDEO PATH FOR FIRE SAFETY (Door/Entrance view)
    video_src = os.path.join(config.BASE_DIR, 'videos', 'door_crossing.mp4')
    cap = cv2.VideoCapture(video_src)
    
    detector = HumanDetector()
    tracker = HumanTracker()
    line_counter = LineCrossingCounter(int(cap.get(3)), int(cap.get(4)), line_position=0.5)
    
    while st.session_state.fire_running:
        loop_start = time.time()
        ret, frame = cap.read()
        if not ret: break
        
        tracks = tracker.update_tracks(detector.detect_people(frame))
        frame = draw_bounding_boxes_and_paths(frame, tracks)
        line_counter.update(tracks)
        frame = line_counter.draw_ui(frame)
        
        occ = line_counter.in_count - line_counter.out_count
        m_occupancy.metric("People Inside Building", occ, delta=occ)
        m_in.metric("Total IN", line_counter.in_count)
        m_out.metric("Total OUT", line_counter.out_count)
        m_fps.metric("FPS", int(1.0 / (time.time() - loop_start + 1e-6)))
        
        video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
    cap.release()
else:
    st.info("System Standby. Press Start to monitor building occupancy.")
