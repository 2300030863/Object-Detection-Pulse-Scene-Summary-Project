"""
Enhanced Video Object Detection with BLIP Scene Captioning
Combines YOLOv11 object detection + BLIP AI caption generation for videos.
"""

import cv2
import os
import time
from pathlib import Path
from ultralytics import YOLO
from blip_caption import BLIPCaptioner


class VideoDetectorWithBLIP:
    """Enhanced video detector with YOLO + BLIP caption generation."""

    def __init__(
        self,
        model_path="models/yolo11s.pt",
        confidence=0.35,
        process_every_n_frames=1,
        caption_update_interval=8.0,
        inference_imgsz=1280,
    ):
        """Initialize detector models and performance settings."""
        print(f"\n{'='*60}")
        print("Video Detection + BLIP Caption System")
        print(f"{'='*60}")

        print(f"\nLoading YOLO model: {model_path}")
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.process_every_n_frames = max(1, int(process_every_n_frames))
        self.caption_update_interval = max(1.0, float(caption_update_interval))
        self.inference_imgsz = max(320, int(inference_imgsz))
        self.base_infer_confidence = 0.2
        print("Model loaded successfully!")

        self.captioner = BLIPCaptioner()

        print(f"\nConfidence threshold: {self.confidence}")
        print(f"Process every N frames: {self.process_every_n_frames}")
        print(f"Caption update interval: {self.caption_update_interval:.1f}s")
        print(f"YOLO inference size: {self.inference_imgsz}")
        print(f"{'='*60}\n")

    def detect_video(self, video_path):
        """Process a video with YOLO detections and periodic BLIP captions."""
        print(f"\nProcessing video: {os.path.basename(video_path)}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            return

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        print(f"Resolution: {width}x{height}")
        print(f"FPS: {fps}")
        print(f"Total frames: {total_frames}")
        print(f"Duration: {duration:.2f} seconds")
        print("\nPress 'q' to quit, 'p' to pause/resume, 'c' to refresh caption")
        print(f"{'='*60}\n")

        frame_count = 0
        start_time = time.time()
        paused = False
        last_frame = None
        last_detected_objects = []
        last_detection_boxes = []

        last_caption_update = 0.0
        current_caption = "Analyzing video..."
        detected_objects_buffer = []
        progress_step = max(120, fps * 10) if fps > 0 else 300

        try:
            while cap.isOpened():
                if not paused:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_count += 1
                    last_frame = frame
                    now = time.time()

                    run_inference = (frame_count % self.process_every_n_frames == 0)
                    frame_objects = []
                    frame_detection_boxes = []

                    if run_inference:
                        # Run YOLO on every Nth frame for better throughput on long videos.
                        results = self.model(
                            frame,
                            conf=self.base_infer_confidence,
                            imgsz=self.inference_imgsz,
                            verbose=False,
                        )

                        for result in results:
                            for box in result.boxes:
                                cls_id = int(box.cls[0])
                                conf = float(box.conf[0])
                                class_name = self.model.names[cls_id]

                                # Keep a slightly lower threshold for bike classes,
                                # since these objects are often smaller/farther in traffic scenes.
                                if class_name in {"motorcycle", "bicycle"}:
                                    min_conf = max(0.2, self.confidence - 0.15)
                                else:
                                    min_conf = self.confidence

                                if conf < min_conf:
                                    continue

                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                display_name = self._display_class_name(
                                    class_name,
                                    x1,
                                    y1,
                                    x2,
                                    y2,
                                    width,
                                    height,
                                )

                                frame_objects.append(display_name)
                                detected_objects_buffer.append(display_name)

                                label = f"{display_name} {conf:.2f}"
                                frame_detection_boxes.append(
                                    {
                                        "bbox": (x1, y1, x2, y2),
                                        "label": label,
                                    }
                                )

                        last_detected_objects = frame_objects
                        last_detection_boxes = frame_detection_boxes

                    # Keep boxes visible on skipped frames to avoid blinking.
                    self._draw_detections(frame, frame_detection_boxes or last_detection_boxes)

                    if (
                        run_inference
                        and now - last_caption_update >= self.caption_update_interval
                        and detected_objects_buffer
                    ):
                        print(f"\n[Frame {frame_count}] Generating AI caption...")
                        caption_start = time.time()
                        current_caption = self.captioner.generate_caption(
                            frame,
                            detected_objects_buffer[-10:],
                        )
                        caption_time = time.time() - caption_start

                        unique_objs = list(set(detected_objects_buffer[-30:]))
                        print(f"   Objects: {', '.join(unique_objs[:5])}")
                        print(f"   Caption: '{current_caption}' ({caption_time:.2f}s)")

                        last_caption_update = now
                        detected_objects_buffer = detected_objects_buffer[-50:]

                    if total_frames > 0 and frame_count % progress_step == 0:
                        elapsed = now - start_time
                        progress = (frame_count / total_frames) * 100
                        eta = (elapsed / frame_count) * (total_frames - frame_count)
                        print(
                            f"[Progress] {progress:.1f}% ({frame_count}/{total_frames}) | ETA: {eta/60:.1f} min"
                        )

                    self._add_overlays(
                        frame,
                        frame_count,
                        start_time,
                        frame_objects or last_detected_objects,
                        current_caption,
                    )
                    cv2.imshow("YOLO + BLIP Video Detection", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print("\nStopping video processing...")
                    break
                if key == ord("p"):
                    paused = not paused
                    print("\nPAUSED" if paused else "\nRESUMED")
                if key == ord("c"):
                    if last_frame is not None and detected_objects_buffer:
                        print(f"\n[Frame {frame_count}] Refreshing caption...")
                        current_caption = self.captioner.generate_caption(
                            last_frame,
                            detected_objects_buffer[-10:],
                        )
                        print(f"   Caption: '{current_caption}'")
                        last_caption_update = time.time()
        finally:
            cap.release()
            cv2.destroyAllWindows()

        elapsed_time = time.time() - start_time
        avg_fps = frame_count / elapsed_time if elapsed_time > 0 else 0

        print(f"\n{'='*60}")
        print("Processing complete!")
        print(f"Total frames processed: {frame_count}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        print(f"Average FPS: {avg_fps:.2f}")
        print(f"\nFinal Caption: '{current_caption}'")
        print(f"{'='*60}\n")

    def _add_overlays(self, frame, frame_count, start_time, current_objects, caption):
        """Add information overlays to frame."""
        h, w = frame.shape[:2]

        elapsed = time.time() - start_time
        current_fps = frame_count / elapsed if elapsed > 0 else 0
        info_text = f"Frame: {frame_count} | FPS: {current_fps:.1f}"
        cv2.putText(frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if current_objects:
            unique_objs = list(set(current_objects))
            obj_text = f"{len(unique_objs)} types detected"
            text_size = cv2.getTextSize(obj_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.putText(
                frame,
                obj_text,
                (w - text_size[0] - 10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )

        overlay = frame.copy()
        overlay_height = 100
        cv2.rectangle(overlay, (0, h - overlay_height), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        cv2.putText(frame, "AI Scene Caption:", (10, h - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

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

        y_pos = h - 35
        for line in lines[:2]:
            cv2.putText(frame, line, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            y_pos += 25

    def _draw_detections(self, frame, detections):
        """Draw cached detections on the current frame."""
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            label = det["label"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    def _display_class_name(self, class_name, x1, y1, x2, y2, frame_w, frame_h):
        """Map model class names to traffic-friendly display labels."""
        if class_name in {"motorcycle", "bicycle"}:
            return "bike"

        return class_name

    def process_folder(self, input_folder="input/videos"):
        """Process all videos in a folder."""
        input_path = Path(input_folder)

        if not input_path.exists():
            print(f"Error: Input folder '{input_folder}' not found!")
            return

        video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"]
        video_files = []
        for ext in video_extensions:
            video_files.extend(input_path.glob(f"*{ext}"))
            video_files.extend(input_path.glob(f"*{ext.upper()}"))
        video_files = sorted(set(video_files))

        if not video_files:
            print(f"\nNo videos found in '{input_folder}'")
            print("Supported formats: MP4, AVI, MOV, MKV, FLV, WMV")
            return

        print(f"Found {len(video_files)} videos to process")
        print(f"{'='*60}\n")

        for idx, video_path in enumerate(video_files, 1):
            print(f"\n[Video {idx}/{len(video_files)}]")
            self.detect_video(str(video_path))


def main():
    """Main function for video detection with BLIP."""
    detector = VideoDetectorWithBLIP(confidence=0.5)
    detector.process_folder("input/videos")


if __name__ == "__main__":
    main()
