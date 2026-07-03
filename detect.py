"""
Object Detection – Main Script
Detects objects in an image, video file, or live camera feed using YOLOv11.

Usage:
    python detect.py                        # detect in default image
    python detect.py --image path/to/img   # detect in image
    python detect.py --video path/to/vid   # detect in video
    python detect.py --camera              # live camera feed
"""

import os
import sys
import argparse
import cv2
from ultralytics import YOLO

# ---------------------------------------------------------------------------
# Model – loaded once at module level so re-imports are cheap
# ---------------------------------------------------------------------------
MODEL_PATH = "yolo11n.pt"
model = YOLO(MODEL_PATH)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _caption_from_labels(labels: list[str]) -> str:
    """
    Build a simple natural-language caption from a list of detected labels.

    Example:
        ['person', 'bicycle', 'dog'] → "A person is near a bicycle and dog."
    """
    if not labels:
        return "No objects detected in the scene."

    unique = list(dict.fromkeys(labels))   # deduplicate, preserve first-seen order

    if len(unique) == 1:
        return f"A {unique[0]} is present in the scene."
    if len(unique) == 2:
        return f"A {unique[0]} and {unique[1]} are present in the scene."

    if "person" in unique:
        others = [o for o in unique if o != "person"]
        if len(others) == 1:
            return f"A person is near a {others[0]}."
        rest = ", ".join(others[:-1])
        return f"A person is near a {rest} and {others[-1]}."

    head = ", ".join(unique[:-1])
    return f"The scene contains {head} and {unique[-1]}."


def _draw_summary_banner(frame, summary_text: str) -> None:
    """Draw a readable scene-summary banner on the top-left of a frame."""
    if not summary_text:
        summary_text = "No objects detected in the scene."

    # Keep overlay compact for small frames.
    max_chars = 90
    if len(summary_text) > max_chars:
        summary_text = summary_text[: max_chars - 3] + "..."

    text = f"Scene: {summary_text}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.6
    thickness = 2
    x, y = 12, 28

    (tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
    cv2.rectangle(frame, (x - 8, y - th - 10), (x + tw + 8, y + 8), (0, 0, 0), -1)
    cv2.putText(frame, text, (x, y), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)


# ---------------------------------------------------------------------------
# detect_objects – core function (image path → list of labels)
# ---------------------------------------------------------------------------

def detect_objects(image_path: str, confidence: float = 0.5) -> list[str]:
    """
    Run YOLO on a single image and return detected object labels.

    Args:
        image_path: Path to the input image file.
        confidence: Minimum confidence threshold (0–1).

    Returns:
        List of unique detected object label strings.

    Example:
        >>> labels = detect_objects("image.jpg")
        >>> print(labels)
        ['person', 'dog', 'bicycle']
    """
    results = model(image_path, conf=confidence, verbose=False)
    labels = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            labels.append(r.names[cls])
    return list(dict.fromkeys(labels))   # unique, order-preserving


# ---------------------------------------------------------------------------
# detect_image – detect + draw boxes + print results
# ---------------------------------------------------------------------------

def detect_image(image_path: str, confidence: float = 0.5, save: bool = True) -> None:
    """
    Detect objects in a static image, draw bounding boxes, and print labels.

    Args:
        image_path: Path to the input image.
        confidence: Detection confidence threshold.
        save: If True, saves annotated image to output/.
    """
    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return

    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] Could not read image: {image_path}")
        return

    print(f"\nProcessing image : {os.path.basename(image_path)}")
    print(f"Resolution       : {image.shape[1]}x{image.shape[0]}")
    print("-" * 50)

    results = model(image, conf=confidence, verbose=False)

    labels_all: list[str] = []
    for result in results:
        for box in result.boxes:
            conf_val   = float(box.conf[0])
            cls        = int(box.cls[0])
            label      = result.names[cls]
            labels_all.append(label)

            # Draw bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label + confidence
            text = f"{label} {conf_val:.2f}"
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(image, (x1, y1 - th - 8), (x1 + tw + 4, y1), (0, 255, 0), -1)
            cv2.putText(image, text, (x1 + 2, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Print results
    unique_labels = list(dict.fromkeys(labels_all))
    print(f"\nDetected Objects ({len(labels_all)} total, {len(unique_labels)} unique):")
    if unique_labels:
        for lbl in unique_labels:
            count = labels_all.count(lbl)
            print(f"  • {lbl}" + (f"  ×{count}" if count > 1 else ""))
    else:
        print("  (none above confidence threshold)")

    summary = _caption_from_labels(unique_labels)
    print(f"\n{'─' * 50}")
    print("  SCENE SUMMARY")
    print(f"{'─' * 50}")
    print(f"  {summary}")
    print(f"{'─' * 50}")

    if save and labels_all:
        os.makedirs("output", exist_ok=True)
        out_path = os.path.join("output", f"detected_{os.path.basename(image_path)}")
        cv2.imwrite(out_path, image)
        print(f"\nAnnotated image saved → {out_path}")

    print("=" * 50)


# ---------------------------------------------------------------------------
# detect_video – frame-by-frame detection with live display
# ---------------------------------------------------------------------------

def detect_video(video_path: str, confidence: float = 0.5, save: bool = False) -> None:
    """
    Detect objects in a video file and display annotated frames in real time.

    Args:
        video_path: Path to the video file.
        confidence: Detection confidence threshold.
        save: If True, saves annotated video to output/.
    """
    if not os.path.exists(video_path):
        print(f"[ERROR] Video not found: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] Could not open video: {video_path}")
        return

    fps    = int(cap.get(cv2.CAP_PROP_FPS)) or 25
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"\nProcessing video : {os.path.basename(video_path)}")
    print(f"Resolution       : {width}x{height}  |  FPS: {fps}  |  Frames: {total}")
    print("Press 'q' to quit, 'p' to pause/resume")
    print("-" * 50)

    out = None
    if save:
        os.makedirs("output", exist_ok=True)
        out_path = os.path.join("output", f"detected_{os.path.basename(video_path)}")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
        print(f"Saving output to: {out_path}")

    all_labels: list[str] = []
    frame_num  = 0
    paused     = False

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break

            frame_num += 1
            results = model(frame, conf=confidence, verbose=False)
            frame_labels: list[str] = []

            for result in results:
                for box in result.boxes:
                    cls   = int(box.cls[0])
                    label = result.names[cls]
                    all_labels.append(label)
                    frame_labels.append(label)

            annotated = results[0].plot()
            frame_unique = list(dict.fromkeys(frame_labels))
            live_summary = _caption_from_labels(frame_unique)
            _draw_summary_banner(annotated, live_summary)

            if frame_num % 30 == 0:
                if frame_unique:
                    print(f"  [Frame {frame_num:>5}] Objects: {', '.join(frame_unique)}")
                else:
                    print(f"  [Frame {frame_num:>5}] Objects: none")

            if out:
                out.write(annotated)

            cv2.imshow("YOLOv11 Object Detection", annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("p"):
            paused = not paused

    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()

    # Final summary
    unique_labels = list(dict.fromkeys(all_labels))
    print(f"\nVideo Summary – {frame_num} frames processed")
    print(f"Detected Objects ({len(unique_labels)} unique):")
    for lbl in unique_labels:
        print(f"  • {lbl}  ×{all_labels.count(lbl)}")

    print(f"\n{'─' * 50}")
    print("  SCENE SUMMARY")
    print(f"{'─' * 50}")
    print(f"  {_caption_from_labels(unique_labels)}")
    print(f"{'─' * 50}")
    print("=" * 50)


# ---------------------------------------------------------------------------
# detect_camera – live webcam detection
# ---------------------------------------------------------------------------

def detect_camera(camera_index: int = 0, confidence: float = 0.5) -> None:
    """
    Detect objects from a live webcam or camera feed.

    Args:
        camera_index: OpenCV camera index (0 = default webcam).
        confidence: Detection confidence threshold.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[ERROR] Could not open camera index {camera_index}")
        return

    print(f"\nLive camera detection started (index={camera_index})")
    print("Press 'q' to quit")
    print("-" * 50)

    all_labels: list[str] = []
    frame_num = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read camera frame.")
            break

        frame_num += 1
        results = model(frame, conf=confidence, verbose=False)
        frame_labels: list[str] = []

        for result in results:
            for box in result.boxes:
                cls   = int(box.cls[0])
                label = result.names[cls]
                all_labels.append(label)
                frame_labels.append(label)

        annotated = results[0].plot()
        frame_unique = list(dict.fromkeys(frame_labels))
        live_summary = _caption_from_labels(frame_unique)
        _draw_summary_banner(annotated, live_summary)

        if frame_num % 30 == 0:
            if frame_unique:
                print(f"  [Frame {frame_num:>5}] Objects: {', '.join(frame_unique)}")
            else:
                print(f"  [Frame {frame_num:>5}] Objects: none")

        cv2.imshow("YOLOv11 Live Detection", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    unique_labels = list(dict.fromkeys(all_labels))
    print(f"\nSession Summary – Detected Objects ({len(unique_labels)} unique):")
    for lbl in unique_labels:
        print(f"  • {lbl}  ×{all_labels.count(lbl)}")
    print(f"\n{'─' * 50}")
    print("  SCENE SUMMARY")
    print(f"{'─' * 50}")
    print(f"  {_caption_from_labels(unique_labels)}")
    print(f"{'─' * 50}")
    print("=" * 50)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="YOLOv11 Object Detection – image / video / camera",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--image",  metavar="PATH", help="Path to input image")
    mode.add_argument("--video",  metavar="PATH", help="Path to input video")
    mode.add_argument("--camera", action="store_true", help="Use live camera feed")
    p.add_argument("--conf",    type=float, default=0.3, metavar="FLOAT",
                   help="Confidence threshold (default: 0.3)")
    p.add_argument("--save",    action="store_true",
                   help="Save annotated output to output/ folder")
    p.add_argument("--cam-id",  type=int,   default=0, metavar="INT",
                   help="Camera device index (default: 0)")
    return p


if __name__ == "__main__":
    args = _build_parser().parse_args()

    if args.camera:
        detect_camera(camera_index=args.cam_id, confidence=args.conf)
    elif args.video:
        detect_video(args.video, confidence=args.conf, save=args.save)
    else:
        # Default: image mode
        image_path = args.image or "image.jpg"

        # Auto-discover an image if the default doesn't exist
        if not os.path.exists(image_path):
            for folder in ("input/images", "input", "."):
                for ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
                    for fname in os.listdir(folder) if os.path.isdir(folder) else []:
                        if fname.lower().endswith(ext):
                            image_path = os.path.join(folder, fname)
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break

        detect_image(image_path, confidence=args.conf, save=args.save)
