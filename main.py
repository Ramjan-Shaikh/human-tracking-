import cv2
import config
from detector import HumanDetector
from tracker import HumanTracker
from utils import draw_bounding_boxes_and_paths
from line_crossing import LineCrossingCounter
import os

def main():
    print("Initializing Human Tracking System...")
    
    # Initialize detector and tracker
    detector = HumanDetector()
    tracker = HumanTracker()
    
    # Open video source
    print(f"Opening video source: {config.VIDEO_SOURCE}")
    cap = cv2.VideoCapture(config.VIDEO_SOURCE)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return
        
    # Get video properties for output
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Initialize Line Crossing Counter
    line_counter = LineCrossingCounter(width, height, line_position=0.5, orientation='horizontal')
    
    if fps == 0:
        fps = 30
    
    # Setup video writer
    output_path = os.path.join(config.OUTPUT_DIR, 'output.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"Processing video. Output will be saved to: {output_path}")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # 1. Detect humans
        detections = detector.detect_people(frame)
        
        # 2. Track humans
        tracks = tracker.update_tracks(detections)
        
        # 3. Draw bounding boxes, IDs, and movement paths
        frame = draw_bounding_boxes_and_paths(frame, tracks)
        
        # 4. Update Line Crossing Counter and Draw UI
        line_counter.update(tracks)
        frame = line_counter.draw_ui(frame)
        
        # 5. Show and Write frame
        cv2.imshow('Human Tracking System [Press Q to Exit]', frame)
        out.write(frame)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    print(f"Finished processing. Total frames processed: {frame_count}")
    
    # Cleanup
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
