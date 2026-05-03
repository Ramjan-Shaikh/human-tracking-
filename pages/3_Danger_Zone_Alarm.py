import streamlit as st
import cv2
import time
import config
import os
from detector import HumanDetector
from tracker import HumanTracker
from utils import draw_bounding_boxes_and_paths
from line_crossing import LineCrossingCounter

st.set_page_config(page_title="Danger Zone Alarm", page_icon="⚠️", layout="wide")

st.title("⚠️ Danger Zone Perimeter Alarm")
st.markdown("### Restricted Area Safety Monitor")

# Sidebar
st.sidebar.header("Navigation")
st.sidebar.info("Currently on: Danger Zone Alarm")
confidence = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.5)
start_btn = st.sidebar.button("▶️ Start Monitoring", use_container_width=True, type="primary")
stop_btn = st.sidebar.button("⏹️ Stop Monitoring", use_container_width=True)

if 'danger_running' not in st.session_state:
    st.session_state.danger_running = False

if start_btn: st.session_state.danger_running = True
if stop_btn: st.session_state.danger_running = False

# Metrics
col1, col2, col3 = st.columns(3)
m_breach = col1.empty()
m_active = col2.empty()
m_fps = col3.empty()

alert_placeholder = st.empty()
video_placeholder = st.empty()

if st.session_state.danger_running:
    config.CONFIDENCE_THRESHOLD = confidence
    # UPDATED VIDEO PATH FOR DANGER ZONE (Restricted area view)
    video_src = os.path.join(config.BASE_DIR, 'videos', 'pedestrians.mp4')
    cap = cv2.VideoCapture(video_src)
    
    detector = HumanDetector()
    tracker = HumanTracker()
    line_counter = LineCrossingCounter(int(cap.get(3)), int(cap.get(4)), line_position=0.5)
    
    while st.session_state.danger_running:
        loop_start = time.time()
        ret, frame = cap.read()
        if not ret: break
        
        tracks = tracker.update_tracks(detector.detect_people(frame))
        frame = draw_bounding_boxes_and_paths(frame, tracks)
        line_counter.update(tracks)
        frame = line_counter.draw_ui(frame)
        
        breaches = line_counter.in_count
        m_breach.metric("Unauthorized Entries", breaches, delta=breaches, delta_color="inverse")
        m_active.metric("Humans in Danger Zone", len(tracks))
        m_fps.metric("FPS", int(1.0 / (time.time() - loop_start + 1e-6)))
        
        if breaches > 0:
            alert_placeholder.error(f"🚨 SECURITY BREACH: {breaches} unauthorized entries detected!")
        else:
            alert_placeholder.success("✅ Perimeter Secure")
            
        video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
    cap.release()
else:
    st.info("System Standby. Press Start to monitor restricted area.")
