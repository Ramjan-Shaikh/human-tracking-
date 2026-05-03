import cv2
from ultralytics import YOLO
import config

class HumanDetector:
    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        """Loads the YOLO model pre-trained weights."""
        print(f"Loading YOLOv8 model from {config.MODEL_PATH}...")
        model = YOLO('yolov8n.pt' if not __import__('os').path.exists(config.MODEL_PATH) else config.MODEL_PATH)
        return model

    def detect_people(self, frame):
        """
        Detects people in the given frame.
        Returns a list of detections: [x1, y1, x2, y2, conf]
        """
        results = self.model(frame, classes=[config.PERSON_CLASS_ID], conf=config.CONFIDENCE_THRESHOLD, verbose=False)
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                detections.append([x1, y1, x2, y2, conf])
        return detections
