import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'yolov8n.pt')

# Add your new videos inside the 'videos' folder and change the name here:
#VIDEO_SOURCE = os.path.join(BASE_DIR, 'videos', 'sample.mp4')
# OR use your Webcam by uncommenting the line below and commenting out the above line:
VIDEO_SOURCE = 0
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Detection config
CONFIDENCE_THRESHOLD = 0.5
PERSON_CLASS_ID = 0  # COCO dataset class ID for person

# Tracking config
MAX_AGE = 30
MIN_HITS = 3
IOU_THRESHOLD = 0.3
