# AI Human Tracking & Line Crossing System

A real-time AI-powered human tracking system using YOLOv8 and SORT, featuring a professional Streamlit dashboard with specialized social impact applications.

## 🚀 Features
* **Real-time Tracking:** Uses YOLOv8 for detection and SORT for persistent ID tracking.
* **Line Crossing Detection:** Accurate IN/OUT counting using virtual perimeters.
* **Multi-Page Dashboard:** A premium Streamlit UI with 3 specialized modules:
    * **Fire Safety Monitor:** Real-time building occupancy tracking.
    * **Stampede Preventer:** Platform crowd density monitoring with alerts.
    * **Danger Zone Alarm:** Perimeter security for restricted areas.
* **Modern UI:** Dark theme, real-time metrics, and sleek visualizations.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-link>
   cd human-tracking-system
   ```

2. **Set up a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Usage

Run the main Streamlit dashboard:
```bash
streamlit run app.py
```

## 📁 Project Structure
* `app.py`: Main entry point for the dashboard.
* `pages/`: Specialized application pages.
* `line_crossing.py`: Logic for virtual perimeter crossing.
* `tracker.py` & `sort.py`: Tracking algorithms.
* `detector.py`: YOLOv8 detection wrapper.
* `utils.py`: Visualization utilities.

## 🌍 Social Impact
This project is designed with humanitarian benefits in mind, focusing on emergency evacuation safety, crowd disaster prevention, and workplace security.
