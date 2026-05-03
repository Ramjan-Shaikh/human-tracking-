import cv2
import numpy as np
from collections import defaultdict

# Dictionary to store trajectory of each person
# Key: track_id, Value: list of (x, y) centroid coordinates
movement_paths = defaultdict(list)

def draw_bounding_boxes_and_paths(frame, tracks, max_path_length=50):
    """
    Draws bounding boxes, IDs, and movement paths on the frame.
    """
    for track in tracks:
        x1, y1, x2, y2, track_id = map(int, track)
        
        # Calculate centroid
        centroid_x = int((x1 + x2) / 2)
        centroid_y = int((y1 + y2) / 2)
        
        # Store centroid path
        movement_paths[track_id].append((centroid_x, centroid_y))
        
        # Limit path length to avoid clutter
        if len(movement_paths[track_id]) > max_path_length:
            movement_paths[track_id].pop(0)
            
        # Draw bounding box (Cyan color)
        color = (255, 200, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Draw ID with background for better readability
        label = f"[ID:{track_id}] Person"
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(frame, (x1, max(0, y1 - 20)), (x1 + w, max(0, y1)), color, -1)
        cv2.putText(frame, label, (x1, max(15, y1 - 5)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # Draw movement path (trajectory)
        path = movement_paths[track_id]
        for i in range(1, len(path)):
            pt1 = path[i - 1]
            pt2 = path[i]
            # Thin out the tail for a cleaner look
            thickness = int(max(1, 3 - (len(path) - i) / 10.0))
            cv2.line(frame, pt1, pt2, (255, 100, 0), thickness)
            
    return frame
