# Object Detection and Scene Capture Summary System

## 📋 Project Overview

An intelligent system that automatically detects objects in images, videos, or live camera feeds and generates captions plus short scene summaries using YOLOv11.

### Problem Statement
People need automated systems to understand and describe visual content in images, videos, and live feeds.

### Solution
A Python-based object detection system that:
- Detects objects using YOLOv11 pretrained model (COCO dataset - 80 classes)
- Draws bounding boxes with confidence scores
- Works with images, videos, and real-time camera
- Generates BLIP scene captions
- Generates short scene summaries from captions

### Example Output
```
Detected Objects:
- Person (0.94)
- Laptop (0.87)
- Chair (0.81)

Scene Caption:
"A person is sitting at a desk with a laptop and chair nearby."

Scene Summary:
"A person is working at a desk with a laptop."
```

---

## 🎯 Objectives

1. ✅ Detect objects using YOLOv11 pretrained model
2. ✅ Display bounding boxes with labels
3. ✅ Process images
4. ✅ Process videos
5. ✅ Real-time camera detection
6. ✅ Generate BLIP scene captions
7. ✅ Generate automatic short scene summaries

---

## 🛠️ Technologies Used

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.10+ |
| **Computer Vision** | OpenCV |
| **Object Detection** | Ultralytics YOLOv11 |
| **Caption Model** | Salesforce BLIP |
| **Text Summarization** | Transformers summarization pipeline |
| **Deep Learning** | PyTorch |
| **Numerical Computing** | NumPy |
| **Dataset** | COCO (80 object classes) |

---

## 📁 Project Structure

```
object_detection_project/
│
├── detect.py                 # ★ Main entry point – image / video / camera
├── yolo11n.pt                # YOLOv11 model weights (auto-downloaded)
├── models/                   # Additional YOLO model files
├── input/
│   ├── images/               # Input images
│   └── videos/               # Input videos
├── output/                   # Annotated detection results
├── src/
│   ├── scene_summary.py      # Natural-language scene summarizer
│   ├── text_summary.py       # Caption-to-summary module
│   ├── detect_image_blip.py  # Image detection + BLIP captioning
│   ├── detect_video_blip.py  # Video detection + BLIP captioning
│   └── detect_camera_blip.py # Camera detection + BLIP captioning
├── ARCHITECTURE_DIAGRAM.md   # System architecture diagram
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 📦 Deliverables

- Source Code: this workspace
- Trained Models: YOLO model file (`yolo11n.pt`) auto-downloaded by Ultralytics
- Project Report: `PROJECT_SUMMARY.md`
- Architecture Diagram: `ARCHITECTURE_DIAGRAM.md`
- Demo Guide: `DEMO.md`

---

## 🚀 Installation & Setup

### Step 1: Prerequisites
- Python 3.10 or higher
- Webcam (for real-time detection)

Verify Python installation:
```bash
python --version
```

### Step 2: Clone/Download Project
Navigate to project directory:
```bash
cd "c:\project\Object detaction"
```

### Step 3: Create Virtual Environment
```bash
python -m venv venv
```

Activate virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Linux/Mac**: `source venv/bin/activate`

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Model Download
YOLO model (yolo11n.pt) automatically downloads on first run.

**Note on Large Model Files:**
The project contains large model files (`.pt` files) that are not tracked in Git to keep repository size manageable. These files are listed as **untracked** and must be added manually.

#### Option A: Automatic Download (Recommended)
Models automatically download on first run of any detection script:
```bash
python detect.py --image input/images/photo.jpg
```
The YOLO models will auto-download to:
- `~/.cache/yolo/` (Linux/Mac)
- `%APPDATA%\yolo\` (Windows)
- `models/` directory (project folder)

#### Option B: Manual Download
If you need to pre-download models or use specific versions:

1. **YOLOv11 Nano (recommended - 5.9MB):**
   ```bash
   yolo export model=yolo11n.pt format=pt
   # Or download directly from Ultralytics
   ```

2. **YOLOv11 Small (more accurate - 24MB):**
   ```bash
   yolo export model=yolo11s.pt format=pt
   ```

3. **YOLOv8 Nano (legacy):**
   ```bash
   yolo export model=yolov8n.pt format=pt
   ```

Place downloaded `.pt` files in:
```
models/
├── yolo11n.pt    # YOLOv11 Nano (primary)
├── yolo11s.pt    # YOLOv11 Small (optional)
└── yolov8n.pt    # YOLOv8 Nano (optional/legacy)
```

#### How to Add Large Files to Git (Optional)
If you want to track these models in Git, use **Git LFS** (Large File Storage):

1. **Install Git LFS:**
   ```bash
   # Windows
   choco install git-lfs
   # Or download from: https://git-lfs.github.com
   
   # Linux
   sudo apt-get install git-lfs
   
   # Mac
   brew install git-lfs
   ```

2. **Initialize Git LFS in the project:**
   ```bash
   git lfs install
   ```

3. **Track .pt files with Git LFS:**
   ```bash
   git lfs track "*.pt"
   git add .gitattributes
   ```

4. **Add model files:**
   ```bash
   git add models/*.pt yolo*.pt
   git commit -m "Add YOLO model files with Git LFS"
   git push
   ```

**Why models are excluded by default:**
- Model files are very large (5-100+ MB each)
- They don't change frequently
- They can be auto-downloaded by the framework
- This keeps the repository lightweight (~13 MB vs ~250+ MB)

### Step 6: Run Detection
```bash
# Detect in an image (auto-discovers images in input/images/)
python detect.py

# Explicit paths:
python detect.py --image input/images/photo.jpg
python detect.py --video input/videos/clip.mp4
python detect.py --camera
```

---

## 💻 Usage

### 1. Detect Objects in an Image
```bash
python detect.py --image input/images/photo.jpg --save
```
- Draws bounding boxes and labels on the image
- Prints detected objects and a scene caption
- `--save` writes the annotated image to `output/`

### 2. Detect Objects in a Video
```bash
python detect.py --video input/videos/clip.mp4
```
- Processes frame-by-frame with live display
- Press **p** to pause/resume, **q** to quit
- Add `--save` to write the annotated video to `output/`

### 3. Real-time Camera Detection
```bash
python detect.py --camera
```
- Opens the default webcam (index 0)
- Press **q** to quit; session summary printed on exit
- Use `--cam-id N` for a different camera index

### 4. Options
| Flag | Default | Description |
|------|---------|-------------|
| `--image PATH` | `image.jpg` | Input image path |
| `--video PATH` | — | Input video path |
| `--camera` | — | Live webcam feed |
| `--conf FLOAT` | `0.5` | Confidence threshold |
| `--save` | off | Save annotated output to `output/` |
| `--cam-id INT` | `0` | Camera device index |

---

## 🎨 Features

### Object Detection
- **80 Object Classes** from COCO dataset
- **Real-time Detection** (30+ FPS on modern hardware)
- **High Accuracy** using YOLOv11 pretrained model
- **Confidence Scores** for each detection

### Visual Output
- Bounding boxes around detected objects
- Object labels with confidence scores
- Color-coded boxes for easy identification

### Scene Understanding
- Automatic object collection
- Duplicate removal
- Natural language scene descriptions

---

## 📊 System Architecture

```
Input Source (Image/Video/Camera)
        ↓
Preprocessing (Resize, Convert)
        ↓
Object Detection (YOLOv11)
        ↓
Caption Generation (BLIP)
        ↓
Detection Output (Name, Score, Box)
        ↓
Scene Understanding (Collect Objects)
        ↓
Scene Summary (Generate Sentence)
```

---

## 🧪 Testing

| Test Case | Input | Expected Output |
|-----------|-------|-----------------|
| TC1 | Single image | Objects detected with boxes |
| TC2 | Video file | Frame-by-frame detection |
| TC3 | Live camera | Real-time detection |
| TC4 | Multiple objects | Accurate scene summary |

---

## 📈 Functional Requirements

| ID | Requirement |
|----|-------------|
| FR1 | Accept image input |
| FR2 | Accept video input |
| FR3 | Accept real-time webcam input |
| FR4 | Detect objects using YOLO |
| FR5 | Draw bounding boxes with labels |
| FR6 | Generate scene summary text |
| FR7 | Display results on screen |

---

## ⚡ Non-Functional Requirements

- **Performance**: Real-time detection capability
- **Accuracy**: Using pretrained YOLOv11 model
- **Usability**: Simple command-based execution
- **Scalability**: Support for model upgrades

---

## 🔮 Future Enhancements

- [ ] Voice description for visually impaired users
- [ ] Object tracking across frames
- [ ] Dangerous object detection alerts
- [ ] Mobile application
- [ ] Smart surveillance system
- [ ] Custom object training
- [ ] Multi-language support
- [ ] Cloud deployment

---

## 📝 Example Workflow

1. User runs: `python src/detect_camera_blip.py`
2. System opens webcam
3. System detects objects in real-time
4. System draws bounding boxes
5. System displays object labels
6. System generates scene summary
7. Output displayed on screen

**Sample Output:**
```
Detected Objects:
- Person (0.94)
- Laptop (0.87)
- Bottle (0.82)

Scene Summary:
"A person is sitting near a laptop and bottle."
```

---

## 🐛 Troubleshooting

### Issue: Camera not detected
**Solution**: Check camera permissions and drivers

### Issue: Slow detection
**Solution**: Use GPU acceleration or smaller YOLO model (yolo11n.pt)

### Issue: Module not found
**Solution**: Ensure virtual environment is activated and dependencies installed

---

## 📄 License

This project is for educational purposes.

---

## 👥 Contributors

Developed as part of object detection learning project.

---

## 📞 Support

For issues or questions, please refer to:
- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)
- [OpenCV Documentation](https://docs.opencv.org/)

---

**Happy Detecting! 🎯**
"# Object-Detection-Pulse-Scene-Summary-Project" 
