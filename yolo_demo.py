"""
YOLO (You Only Look Once) - Quick Demo
Demonstrates the key advantages of YOLO for object detection.

Advantages:
✓ Fast inference - Real-time detection at 30+ FPS
✓ Single-stage detection - Processes entire image in one pass
✓ Pre-trained on COCO dataset - 80 object classes ready to use
✓ High accuracy - State-of-the-art results
✓ Easy to use - Simple API with few lines of code
"""

import cv2
from ultralytics import YOLO
import time


def demo_yolo_advantages():
    """
    Demonstrate YOLO's key advantages with live examples.
    """
    
    print("="*60)
    print("YOLO Advantages Demo")
    print("="*60)
    
    # ✓ ADVANTAGE 1: Easy Import and Setup
    print("\n✓ ADVANTAGE 1: Easy Import & Setup")
    print("   from ultralytics import YOLO")
    print("   model = YOLO('yolo11n.pt')  # Just one line!")
    
    # Load pre-trained model
    print("\nLoading YOLOv11 model (pre-trained on COCO dataset)...")
    model = YOLO('yolo11n.pt')
    print("✅ Model loaded successfully!")
    
    
    # ✓ ADVANTAGE 2: Pre-trained on Large Datasets (COCO)
    print("\n✓ ADVANTAGE 2: Pre-trained on COCO Dataset")
    print(f"   Total classes available: {len(model.names)}")
    print("   Sample classes:", list(model.names.values())[:10], "...")
    
    
    # ✓ ADVANTAGE 3: Fast Inference
    print("\n✓ ADVANTAGE 3: Fast Real-time Inference")
    print("Opening camera for speed test...")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("⚠️ Camera not available, skipping speed test")
        return
    
    print("Running 30-frame speed test...")
    
    frame_count = 0
    start_time = time.time()
    test_frames = 30
    
    while frame_count < test_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run YOLO detection (this is where the magic happens!)
        results = model(frame, verbose=False)
        
        frame_count += 1
        
        # Display progress
        if frame_count % 10 == 0:
            print(f"   Processed {frame_count}/{test_frames} frames...")
    
    elapsed_time = time.time() - start_time
    avg_fps = frame_count / elapsed_time
    avg_time_per_frame = (elapsed_time / frame_count) * 1000  # milliseconds
    
    print(f"\n   Results:")
    print(f"   • Average FPS: {avg_fps:.2f}")
    print(f"   • Time per frame: {avg_time_per_frame:.2f}ms")
    print(f"   • Total time: {elapsed_time:.2f}s")
    
    if avg_fps >= 20:
        print("   ✅ Real-time performance achieved! (>20 FPS)")
    elif avg_fps >= 10:
        print("   ✅ Good performance for most applications (>10 FPS)")
    else:
        print("   ⚠️ Consider using GPU for better performance")
    
    cap.release()
    
    
    # ✓ ADVANTAGE 4: Single Detection Call
    print("\n✓ ADVANTAGE 4: Simple Detection API")
    print("   # Just one line to detect objects:")
    print("   results = model(image)")
    print("   # That's it! No complex preprocessing needed.")
    
    
    # Show detection example
    print("\n✓ ADVANTAGE 5: Rich Detection Information")
    print("Capturing one frame for detailed analysis...")
    
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    if ret:
        results = model(frame, verbose=False)
        
        detection_count = 0
        print("\nDetected objects in current frame:")
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                
                detection_count += 1
                print(f"   {detection_count}. {class_name} (confidence: {confidence:.2%})")
        
        if detection_count == 0:
            print("   No objects detected in current frame")
        else:
            print(f"\n   ✅ Total: {detection_count} objects detected!")
    
    cap.release()
    
    
    # Summary
    print("\n" + "="*60)
    print("YOLO Advantages Summary")
    print("="*60)
    print("✓ Fast: ~7-30 FPS on CPU, 60+ FPS on GPU")
    print("✓ Easy: Simple API with minimal code")
    print("✓ Accurate: State-of-the-art performance")
    print("✓ Pre-trained: 80 classes ready to use (COCO)")
    print("✓ Versatile: Works with images, videos, and live camera")
    print("✓ Lightweight: YOLO11n model is compact and fast")
    print("="*60)


def quick_detection_example():
    """
    Minimal example showing how easy YOLO is to use.
    """
    print("\n" + "="*60)
    print("Quick Detection Example (Minimal Code)")
    print("="*60)
    
    print("\nCode:")
    print("""
    from ultralytics import YOLO
    import cv2
    
    # 1. Load model (pre-trained on COCO)
    model = YOLO('yolo11n.pt')
    
    # 2. Capture image
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    # 3. Run detection (one line!)
    results = model(frame)
    
    # That's it! Objects are detected!
    """)
    
    print("="*60)


if __name__ == "__main__":
    try:
        print("\n🎯 Starting YOLO Advantages Demo...")
        print("This will demonstrate why YOLO is excellent for real-time detection\n")
        
        demo_yolo_advantages()
        quick_detection_example()
        
        print("\n✅ Demo complete!")
        print("\nTo run full detection:")
        print("  python src/detect_camera_blip.py  # Real-time camera")
        print("  python src/detect_image_blip.py   # Batch images")
        print("  python src/detect_video_blip.py   # Video files")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
