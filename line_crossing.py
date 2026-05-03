import cv2
import numpy as np

class LineCrossingCounter:
    def __init__(self, width, height, line_position=0.5, orientation='horizontal'):
        """
        Initializes the line crossing counter.
        :param width: Frame width
        :param height: Frame height
        :param line_position: Relative position of the line (0.0 to 1.0)
        :param orientation: 'horizontal' or 'vertical'
        """
        self.width = width
        self.height = height
        self.orientation = orientation
        
        if self.orientation == 'horizontal':
            y = int(height * line_position)
            self.line_p1 = (0, y)
            self.line_p2 = (width, y)
        else:
            x = int(width * line_position)
            self.line_p1 = (x, 0)
            self.line_p2 = (x, height)
            
        self.in_count = 0
        self.out_count = 0
        # State dictionary: track_id -> 'IN_REGION' or 'OUT_REGION'
        self.id_states = {}
        
    def _get_region(self, point):
        """
        Determines which region a point is in relative to the line.
        """
        if self.orientation == 'horizontal':
            # Top is OUT, Bottom is IN
            return 'OUT_REGION' if point[1] < self.line_p1[1] else 'IN_REGION'
        else:
            # Left is OUT, Right is IN
            return 'OUT_REGION' if point[0] < self.line_p1[0] else 'IN_REGION'

    def update(self, tracks):
        """
        Updates counts based on current track positions.
        """
        for track in tracks:
            x1, y1, x2, y2, track_id = map(int, track)
            centroid = (int((x1 + x2) / 2), int((y1 + y2) / 2))
            
            current_region = self._get_region(centroid)
            
            if track_id not in self.id_states:
                # First time seeing this ID, initialize its state
                self.id_states[track_id] = current_region
            else:
                previous_region = self.id_states[track_id]
                
                # Check for crossing (state change)
                if previous_region == 'OUT_REGION' and current_region == 'IN_REGION':
                    self.in_count += 1
                    self.id_states[track_id] = current_region
                elif previous_region == 'IN_REGION' and current_region == 'OUT_REGION':
                    self.out_count += 1
                    self.id_states[track_id] = current_region

    def draw_ui(self, frame):
        """
        Draws the line, UI panel, and directional arrows on the frame.
        """
        # Dark theme UI panel
        ui_panel = frame.copy()
        cv2.rectangle(ui_panel, (15, 15), (260, 115), (20, 20, 20), -1)
        # Add subtle border to UI panel
        cv2.rectangle(ui_panel, (15, 15), (260, 115), (100, 100, 100), 1)
        cv2.addWeighted(ui_panel, 0.8, frame, 0.2, 0, frame)
        
        # Bright line indicator (Yellowish-Red/Orange or bright Red, let's go with bright Cyan/Yellow)
        # Requirement says: "Bright line indicator (red/yellow)"
        cv2.line(frame, self.line_p1, self.line_p2, (0, 255, 255), 3) # Bright yellow
        
        # Labels showing IN/OUT counters
        cv2.putText(frame, f"IN:  {self.in_count}", (30, 55), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f"OUT: {self.out_count}", (30, 95), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # Draw arrows on the line to indicate direction
        if self.orientation == 'horizontal':
            center_x = self.width // 2
            line_y = self.line_p1[1]
            # IN direction arrow (downward)
            cv2.arrowedLine(frame, (center_x - 60, line_y - 30), (center_x - 60, line_y + 30), (0, 255, 0), 3, tipLength=0.2)
            cv2.putText(frame, "IN", (center_x - 60 - 15, line_y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # OUT direction arrow (upward)
            cv2.arrowedLine(frame, (center_x + 60, line_y + 30), (center_x + 60, line_y - 30), (0, 0, 255), 3, tipLength=0.2)
            cv2.putText(frame, "OUT", (center_x + 60 - 20, line_y + 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        else:
            center_y = self.height // 2
            line_x = self.line_p1[0]
            # IN direction arrow (rightward)
            cv2.arrowedLine(frame, (line_x - 30, center_y - 60), (line_x + 30, center_y - 60), (0, 255, 0), 3, tipLength=0.2)
            cv2.putText(frame, "IN", (line_x + 40, center_y - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # OUT direction arrow (leftward)
            cv2.arrowedLine(frame, (line_x + 30, center_y + 60), (line_x - 30, center_y + 60), (0, 0, 255), 3, tipLength=0.2)
            cv2.putText(frame, "OUT", (line_x - 80, center_y + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        return frame
