# 🎯 Object Detection System - Visual Workflow Guide

## 🔄 System Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     INPUT SOURCES                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📷 Camera          🖼️ Images          🎬 Videos            │
│  (detect_camera)    (detect_image)     (detect_video)       │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                  PREPROCESSING                               │
├─────────────────────────────────────────────────────────────┤
│  • Read frame/image                                          │
│  • Resize if needed                                          │
│  • Format conversion                                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│               YOLO OBJECT DETECTION                          │
├─────────────────────────────────────────────────────────────┤
│  Model: yolo11n.pt (nano - fastest)                         │
│  Dataset: COCO (80 object classes)                          │
│  Confidence: 0.5 (adjustable)                               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                 DETECTION OUTPUT                             │
├─────────────────────────────────────────────────────────────┤
│  For each detected object:                                   │
│  • Class name (e.g., "person", "laptop")                    │
│  • Confidence score (0.0 - 1.0)                             │
│  • Bounding box coordinates (x1, y1, x2, y2)                │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│               VISUALIZATION                                  │
├─────────────────────────────────────────────────────────────┤
│  • Draw bounding boxes (green/red)                          │
│  • Add labels with confidence                               │
│  • Display FPS counter                                       │
│  • Show object count                                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            SCENE SUMMARY MODULE                              │
│              (scene_summary.py)                              │
├─────────────────────────────────────────────────────────────┤
│  1. Collect all detected objects                            │
│  2. Remove duplicates (track counts)                        │
│  3. Generate natural language description                   │
│  4. Format output text                                       │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                  FINAL OUTPUT                                │
├─────────────────────────────────────────────────────────────┤
│  Display:                                                    │
│  • Annotated visual (boxes + labels)                        │
│  • Detected objects list                                    │
│  • Scene summary text                                        │
│  • Performance metrics (FPS)                                 │
│                                                              │
│  Save (optional):                                            │
│  • Annotated images to output/                              │
│  • Screenshots from camera                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎮 User Interaction Flow

### 1️⃣ Camera Detection Flow
```
User runs: python src/detect_camera_blip.py
    ↓
Camera opens, starts capturing
    ↓
[Live loop begins]
    ↓
YOLO detects objects in frame
    ↓
Draw bounding boxes
    ↓
Update scene summary (every 2 seconds)
    ↓
Display annotated frame
    ↓
User actions:
    • Press 'q' → Exit
    • Press 's' → Save screenshot
    • Press 'r' → Reset summary
    ↓
[Loop continues until quit]
    ↓
Show final statistics
```

### 2️⃣ Image Detection Flow
```
User adds images to input/images/
    ↓
User runs: python src/detect_image_blip.py
    ↓
System finds all images in folder
    ↓
For each image:
    ↓
    YOLO detects objects
    ↓
    Draw bounding boxes
    ↓
    Generate scene summary
    ↓
    Save to output/
    ↓
    Display on screen
    ↓
    Wait for key press
    ↓
Next image
    ↓
All images processed → Done
```

### 3️⃣ Video Detection Flow
```
User adds video to input/videos/
    ↓
User runs: python src/detect_video_blip.py
    ↓
Open video file
    ↓
[Frame loop begins]
    ↓
Read next frame
    ↓
YOLO detects objects
    ↓
Draw bounding boxes
    ↓
Collect objects for summary
    ↓
Display frame
    ↓
User actions:
    • Press 'q' → Exit
    • Press 'p' → Pause/Resume
    ↓
[Loop until video ends or quit]
    ↓
Show overall video summary
```

---

## 🎨 Example Screen Layout (Camera Mode)

```
┌─────────────────────────────────────────────────────────┐
│ FPS: 25.3                                               │
│ Objects: 3                                              │
│                                                         │
│         ┌─────────────────────┐                        │
│         │ Person: 0.94        │                        │
│         │  ┌──────────────┐   │                        │
│         │  │              │   │                        │
│         │  │   [Person]   │   │                        │
│         │  │              │   │                        │
│         │  └──────────────┘   │                        │
│         └─────────────────────┘                        │
│                                                         │
│    ┌────────────┐        ┌────────────┐              │
│    │Laptop: 0.87│        │Chair: 0.81 │              │
│    │[Laptop]    │        │[Chair]     │              │
│    └────────────┘        └────────────┘              │
│                                                         │
│                                                         │
│─────────────────────────────────────────────────────── │
│ Scene Summary:                                          │
│ "A person is near a laptop and chair."                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Detection Performance Factors

```
High FPS (Fast)          ←→          Low FPS (Slow)
─────────────────────────────────────────────────────
✅ Good lighting                    ❌ Poor lighting
✅ Simple scene                     ❌ Complex scene
✅ GPU acceleration                 ❌ CPU only
✅ Low resolution                   ❌ 4K resolution
✅ yolo11n.pt (nano)               ❌ yolo11x.pt (xlarge)
✅ Few objects                      ❌ Many objects
✅ Modern hardware                  ❌ Old hardware
```

---

## 🎯 YOLO Detection Process (Internal)

```
Input Image (640x480)
    ↓
┌────────────────────────────────┐
│ YOLOv11 Neural Network         │
├────────────────────────────────┤
│ • Backbone: Extract features   │
│ • Neck: Feature fusion         │
│ • Head: Predictions            │
└────────────────────────────────┘
    ↓
Raw Predictions
    ↓
┌────────────────────────────────┐
│ Post-Processing                │
├────────────────────────────────┤
│ • Confidence filtering (>0.5)  │
│ • Non-Max Suppression (NMS)    │
│ • Class assignment             │
└────────────────────────────────┘
    ↓
Final Detections
[
  {class: "person", conf: 0.94, box: [x1,y1,x2,y2]},
  {class: "laptop", conf: 0.87, box: [x1,y1,x2,y2]},
  {class: "chair", conf: 0.81, box: [x1,y1,x2,y2]}
]
```

---

## 🔧 Scene Summary Generation Logic

```python
Input: ["person", "laptop", "person", "chair", "bottle"]
    ↓
Step 1: Collect objects
    detected_objects = ["person", "laptop", "person", "chair", "bottle"]
    ↓
Step 2: Count duplicates
    unique_counts = {
        "person": 2,
        "laptop": 1,
        "chair": 1,
        "bottle": 1
    }
    ↓
Step 3: Generate natural language
    unique_objects = ["person", "laptop", "chair", "bottle"]
    ↓
    Check if "person" in scene → Yes
    ↓
    Build sentence: "A person is near a..."
    ↓
    Add other objects: "laptop, chair and bottle"
    ↓
Output: "A person is near a laptop, chair and bottle."
```

---

## 🎓 Code Architecture

```
scene_summary.py
├── SceneSummarizer (Main Class)
│   ├── __init__()
│   ├── add_detection(name)
│   ├── clear_detections()
│   ├── get_unique_objects()
│   ├── generate_summary()
│   ├── get_detection_list()
│   └── get_full_summary()
└── create_simple_summary() (Helper)

detect_camera_blip.py
├── CameraObjectDetector (Main Class)
│   ├── __init__(model, camera_id)
│   └── start_detection(confidence)
└── main()

detect_image_blip.py
├── ImageDetectorWithBLIP (Main Class)
│   ├── __init__(model)
│   ├── detect_objects(path)
│   └── detect_batch(folder)
└── main()

detect_video_blip.py
├── VideoDetectorWithBLIP (Main Class)
│   ├── __init__(model)
│   ├── detect_video(path)
│   └── detect_batch(folder)
└── main()
```

---

## 🚦 Quick Start Decision Tree

```
Start Here
    │
    ▼
Do you have Python 3.10+?
    │
    ├─ Yes ──→ Run: python setup.py
    │              │
    │              ▼
    │          Setup successful?
    │              │
    │              ├─ Yes ──→ Choose detection mode:
    │              │            │
    │              │            ├─ Camera ──→ .\run.ps1 camera
    │              │            ├─ Image  ──→ .\run.ps1 image
    │              │            └─ Video  ──→ .\run.ps1 video
    │              │
    │              └─ No ──→ Check error message
    │                         Read QUICKSTART.md
    │
    └─ No ──→ Install Python 3.10+
              Then start over
```

---

## 📱 Control Reference

### Camera Mode
| Key | Action |
|-----|--------|
| `q` | Quit detection |
| `s` | Save screenshot |
| `r` | Reset scene summary |

### Video Mode
| Key | Action |
|-----|--------|
| `q` | Quit detection |
| `p` | Pause/Resume |

### Image Mode
| Key | Action |
|-----|--------|
| Any key | Next image |
| `q` | Quit detection |

---

## 🎯 Success Indicators

Your system is working correctly when you see:

✅ Camera opens without errors  
✅ Objects are detected and labeled  
✅ Bounding boxes appear around objects  
✅ FPS counter shows 10+ FPS  
✅ Scene summary updates dynamically  
✅ Confidence scores are reasonable (>0.5)  
✅ Test suite passes all 7 tests  

---

**End of Visual Workflow Guide** 🎨
