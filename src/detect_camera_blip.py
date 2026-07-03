"""
Enhanced Camera Object Detection with BLIP Scene Captioning
Real-time detection combining YOLOv11 + BLIP AI caption generation.
"""

import cv2
import time
from ultralytics import YOLO
from blip_caption import BLIPCaptioner


class CameraDetectorWithBLIP:
    """
    Real-time camera detector with YOLO + BLIP caption generation.
    """
    
    def __init__(self, model_path="models/yolo11n.pt", confidence=0.5, camera_id=0):
        """
        Initialize the camera detector.
        
        Args:
            model_path (str): Path to YOLO model
            confidence (float): Detection confidence threshold
            camera_id (int): Camera device ID
        """
        print(f"\n{'='*60}")
        print("Real-Time Camera Detection + BLIP Caption")
        print(f"{'='*60}")
        
        # Load YOLO model
        print(f"\nLoading YOLO model: {model_path}")
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.camera_id = camera_id
        print("Model loaded successfully!")
        
        # Load BLIP captioner
        self.captioner = BLIPCaptioner()
        
        print(f"\nConfidence threshold: {self.confidence}")
        print(f"Camera ID: {self.camera_id}")
        print(f"{'='*60}\n")
    
    def start_detection(self):
        """Start real-time camera detection with BLIP captioning."""
        
        print("🎥 Starting camera...")
        
        # Open camera
        cap = cv2.VideoCapture(self.camera_id)
        
        if not cap.isOpened():
            print(f"❌ Error: Could not open camera {self.camera_id}")
            print("   Try different camera ID (0, 1, 2...)")
            return
        
        # Set camera resolution (optional)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"✅ Camera opened successfully!")
        print(f"Resolution: {width}x{height}")
        print(f"\nControls:")
        print("  'q' - Quit")
        print("  'c' - Generate new AI caption")
        print("  's' - Save current frame")
        print(f"{'='*60}\n")
        
        # Initialize tracking
        frame_count = 0
        start_time = time.time()
        saved_frames = 0
        
        # Caption settings
        caption_update_interval = 5.0  # Update every 5 seconds
        last_caption_update = 0
        current_caption = "Starting detection..."
        detected_objects_buffer = []
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Error: Failed to read frame from camera")
                    break
                
                frame_count += 1
                
                # Run YOLO detection
                results = self.model(frame, conf=self.confidence, verbose=False)
                
                # Process detections
                frame_objects = []
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        # Get class info
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])
                        class_name = self.model.names[cls_id]
                        
                        frame_objects.append(class_name)
                        detected_objects_buffer.append(class_name)
                        
                        # Draw bounding box
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        # Draw label
                        label = f"{class_name} {conf:.2f}"
                        cv2.putText(frame, label, (x1, y1-10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Update BLIP caption periodically
                current_time = time.time()
                if (current_time - last_caption_update >= caption_update_interval and 
                    len(detected_objects_buffer) > 0):
                    
                    print(f"\n[Frame {frame_count}] 🤖 Generating AI caption...")
                    caption_start = time.time()
                    current_caption = self.captioner.generate_caption(
                        frame, detected_objects_buffer[-15:]  # Recent detections
                    )
                    caption_time = time.time() - caption_start
                    
                    unique_objs = list(set(detected_objects_buffer[-30:]))
                    print(f"   Objects: {', '.join(unique_objs[:5])}")
                    print(f"   Caption: '{current_caption}' ({caption_time:.2f}s)")
                    
                    last_caption_update = current_time
                    detected_objects_buffer = detected_objects_buffer[-50:]  # Keep buffer small
                
                # Add overlays
                self._add_overlays(frame, frame_count, start_time, 
                                  frame_objects, current_caption)
                
                # Display frame
                cv2.imshow('YOLO + BLIP Camera Detection', frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\n⏹ Stopping camera...")
                    break
                elif key == ord('c'):
                    # Force caption update
                    if len(detected_objects_buffer) > 0:
                        print(f"\n[Frame {frame_count}] 🔄 Generating caption...")
                        current_caption = self.captioner.generate_caption(
                            frame, detected_objects_buffer[-15:]
                        )
                        print(f"   Caption: '{current_caption}'")
                        last_caption_update = current_time
                elif key == ord('s'):
                    # Save frame
                    from pathlib import Path
                    output_dir = Path("output")
                    output_dir.mkdir(exist_ok=True)
                    
                    filename = f"camera_capture_{saved_frames+1}.jpg"
                    filepath = output_dir / filename
                    cv2.imwrite(str(filepath), frame)
                    saved_frames += 1
                    print(f"\n📸 Saved: {filepath}")
        
        except KeyboardInterrupt:
            print("\n\n⚠ Interrupted by user")
        
        finally:
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
            
            # Final statistics
            elapsed_time = time.time() - start_time
            avg_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            print(f"\n{'='*60}")
            print("Camera Detection Complete!")
            print(f"{'='*60}")
            print(f"Total frames: {frame_count}")
            print(f"Time elapsed: {elapsed_time:.2f} seconds")
            print(f"Average FPS: {avg_fps:.2f}")
            print(f"Frames saved: {saved_frames}")
            if current_caption:
                print(f"\nLast Caption: '{current_caption}'")
            print(f"{'='*60}\n")
    
    def _add_overlays(self, frame, frame_count, start_time, 
                     current_objects, caption):
        """Add information overlays to frame."""
        h, w = frame.shape[:2]
        
        # Calculate FPS
        elapsed = time.time() - start_time
        current_fps = frame_count / elapsed if elapsed > 0 else 0
        
        # Add FPS counter (top-left)
        fps_text = f"FPS: {current_fps:.1f} | Frame: {frame_count}"
        cv2.putText(frame, fps_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add object count (top-right)
        if current_objects:
            unique_objs = list(set(current_objects))
            obj_text = f"{len(unique_objs)} types"
            text_size = cv2.getTextSize(obj_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.putText(frame, obj_text, (w-text_size[0]-10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Add AI caption overlay (bottom)
        overlay = frame.copy()
        overlay_height = 100
        cv2.rectangle(overlay, (0, h-overlay_height), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Caption label
        cv2.putText(frame, "AI Scene Caption:", (10, h-70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Wrap caption text
        max_width = w - 20
        words = caption.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            text_size = cv2.getTextSize(test_line, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0][0]
            
            if text_size < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        # Draw caption lines
        y_pos = h - 35
        for line in lines[:2]:  # Max 2 lines
            cv2.putText(frame, line, (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            y_pos += 25


def main():
    """Main function for camera detection with BLIP."""
    detector = CameraDetectorWithBLIP(confidence=0.5, camera_id=0)
    detector.start_detection()


if __name__ == "__main__":
    main()
