from sort import Sort
import numpy as np
import config

class HumanTracker:
    def __init__(self):
        self.tracker = self.initialize_tracker()

    def initialize_tracker(self):
        """Initializes the SORT tracker."""
        print("Initializing SORT tracker...")
        return Sort(max_age=config.MAX_AGE, min_hits=config.MIN_HITS, iou_threshold=config.IOU_THRESHOLD)

    def update_tracks(self, detections):
        """
        Updates tracking with new detections.
        Input: list of [x1, y1, x2, y2, score]
        Output: list of tracked objects [x1, y1, x2, y2, track_id]
        """
        if len(detections) == 0:
            return self.tracker.update(np.empty((0, 5)))
        else:
            return self.tracker.update(np.array(detections))
