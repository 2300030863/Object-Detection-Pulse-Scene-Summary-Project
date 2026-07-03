# Technologies Used

## Language & Runtime
- **Python**: 3.10 or higher
  - Core language for the entire application
  - Compatible with Python 3.13+

## Computer Vision & Object Detection
- **Ultralytics YOLOv11** (>= 8.0.0)
  - Main object detection model
  - Pretrained on COCO dataset (80 object classes)
  - Automatically downloads model weights on first use
  - Includes YOLOv11 nano (n) and small (s) variants
  - Legacy YOLOv8nano support maintained

- **OpenCV** (opencv-python >= 4.8.0)
  - Computer vision library for image/video processing
  - Real-time camera stream handling
  - Bounding box drawing and annotation
  - Frame manipulation and encoding

## Deep Learning & AI Models
- **PyTorch** (>= 2.1.0)
  - Deep learning framework
  - Powers YOLOv11 model inference
  - GPU acceleration support

- **TorchVision** (>= 0.16.0)
  - Computer vision models and utilities
  - Image transformations

- **Transformer Models** (Hugging Face, >= 4.35.0)
  - **BLIP** (Bootstrapping Language-Image Pre-training)
    - Scene caption generation from images
    - Natural language image understanding
    - Summarization pipeline for text

- **Accelerate** (>= 0.25.0)
  - Optimized model loading and inference
  - Hardware acceleration support

## Numerical & Data Processing
- **NumPy** (>= 1.26.0)
  - Numerical computing and array operations
  - Python 3.13 compatible
  - Used for image data manipulation

- **Pillow** (>= 10.0.0)
  - Image processing library
  - Image format conversions
  - Image I/O operations

## Build & Packaging
- **setuptools** (>= 65.0.0)
  - Package building and distribution

- **wheel** (>= 0.38.0)
  - Python binary package format

## System & Runtime
- **PowerShell** (5.1+)
  - Cross-platform launcher script (run.ps1)
  - Virtual environment management
  - Mode-based execution (camera, image, video, test, setup)

## Deployment & Datasets
- **COCO Dataset**
  - 80 object classes for YOLOv11 pretraining
  - Enables out-of-box object recognition

## Optional/Previous Technologies
- ~~Flask~~ (removed - web layer removed from project)
- ~~imageio-ffmpeg~~ (removed - web layer removed from project)

## Development Environment
- **Virtual Environment**: Python venv
  - Isolated dependency management
  - Managed via run.ps1 script

## Typical Execution Flow
```
User Input (Image/Video/Camera)
    ↓
YOLOv11 (Object Detection)
    ↓
OpenCV + NumPy (Frame Processing)
    ↓
BLIP + Transformers (Scene Captioning)
    ↓
Transformers Summarization (Text Summary)
    ↓
Output Display/Saving
```

## Performance Considerations
- **GPU Support**: PyTorch with CUDA acceleration (if available)
- **Memory Efficient**: Nano (n) and small (s) model variants
- **Real-time Processing**: Optimized for camera streams via OpenCV
- **Accelerated Inference**: Accelerate library for faster model loading

## Architecture Highlights
- **Model-agnostic**: Can swap YOLOv11 variants
- **Multi-modal I/O**: Images, videos, live camera feeds
- **Modular Design**: Separate detection and captioning modules
- **Reproducible**: Docker-compatible setup (optional)
