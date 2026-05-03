import streamlit as st
import cv2
import time
import config
import os
from detector import HumanDetector
from tracker import HumanTracker
from utils import draw_bounding_boxes_and_paths
from line_crossing import LineCrossingCounter

st.set_page_config(page_title="Stampede Preventer", page_icon="🚉", layout="wide")

st.title("🚉 Railway Stampede Preventer")
st.markdown("### Platform Crowd Density Monitor")

# Sidebar
st.sidebar.header("Navigation")
st.sidebar.info("Currently on: Stampede Preventer")
confidence = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.5)
start_btn = st.sidebar.button("▶️ Start Monitoring", use_container_width=True, type="primary")
stop_btn = st.sidebar.button("⏹️ Stop Monitoring", use_container_width=True)

if 'stampede_running' not in st.session_state:
    st.session_state.stampede_running = False

if start_btn: st.session_state.stampede_running = True
if stop_btn: st.session_state.stampede_running = False

# Metrics
col1, col2, col3 = st.columns(3)
m_density = col1.empty()
m_total = col2.empty()
m_fps = col3.empty()

alert_placeholder = st.empty()
video_placeholder = st.empty()

if st.session_state.stampede_running:
    config.CONFIDENCE_THRESHOLD = confidence
    # UPDATED VIDEO PATH FOR RAILWAY STATION (Platform/Aisle view)
    video_src = os.path.join(config.BASE_DIR, 'videos', 'pedestrians.mp4')
    cap = cv2.VideoCapture(video_src)
    
    detector = HumanDetector()
    tracker = HumanTracker()
    line_counter = LineCrossingCounter(int(cap.get(3)), int(cap.get(4)), line_position=0.5)
    
    while st.session_state.stampede_running:
        loop_start = time.time()
        ret, frame = cap.read()
        if not ret: break
        
        tracks = tracker.update_tracks(detector.detect_people(frame))
        frame = draw_bounding_boxes_and_paths(frame, tracks)
        line_counter.update(tracks)
        frame = line_counter.draw_ui(frame)
        
        density = len(tracks)
        m_density.metric("Platform Density (Current)", density)
        m_total.metric("Total People Served", line_counter.in_count + line_counter.out_count)
        m_fps.metric("FPS", int(1.0 / (time.time() - loop_start + 1e-6)))
        
        if density > 8:
            alert_placeholder.error("🚨 CRITICAL OVERCROWDING: Stop further platform entries!")
        elif density > 5:
            alert_placeholder.warning("⚠️ HIGH DENSITY: Monitor closely.")
        else:
            alert_placeholder.success("✅ Density Normal")
            
        video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
    cap.release()
else:
    st.info("System Standby. Press Start to monitor crowd density.")
