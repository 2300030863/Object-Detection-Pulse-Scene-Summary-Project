# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Run Setup Script
```bash
python setup.py
```

This will:
- Check Python version
- Create virtual environment
- Install all dependencies
- Set up project structure

### Step 2: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 3: Test Camera Detection (No input files needed!)
```bash
python src/detect_camera_blip.py
```

This is the quickest way to test the system - it uses your webcam!

**Controls:**
- Press `q` to quit
- Press `c` to generate a new AI caption
- Press `s` to save frame

---

## 📁 Testing with Your Own Files

### For Images:
1. Place images in: `input/images/`
2. Run: `python src/detect_image_blip.py`
3. Check results in: `output/`

### For Videos:
1. Place videos in: `input/videos/`
2. Run: `python src/detect_video_blip.py`
3. Press `q` to quit, `p` to pause

## 🔧 Troubleshooting

### Camera not working?
```bash
# Try different camera ID
# Edit src/detect_camera_blip.py and change camera_id
detector = CameraDetectorWithBLIP(camera_id=1)  # Try 1, 2, etc.
```

### Slow performance?
- Already using the smallest model (yolo11n.pt)
- Close other applications
- Consider using a GPU (CUDA)

### Module not found error?
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📊 What Objects Can Be Detected?

YOLO is trained on COCO dataset with **80 object classes**:

**People & Animals:**
person, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, etc.

**Vehicles:**
car, truck, bus, train, motorcycle, bicycle, airplane, boat

**Indoor Objects:**
chair, couch, bed, table, tv, laptop, mouse, keyboard, phone, book, clock

**Kitchen:**
bottle, cup, fork, knife, spoon, bowl, banana, apple, sandwich, pizza

**And many more!**

Full list: https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/datasets/coco.yaml

---

## 💡 Tips for Best Results

1. **Good Lighting**: Ensure adequate lighting for better detection
2. **Distance**: Objects should be clearly visible (not too far/close)
3. **Confidence**: Adjust threshold in code (default: 0.5)
4. **Camera Quality**: Better camera = better detection

---

## 📈 Performance Benchmarks

**Expected FPS (Frames Per Second):**
- Modern Laptop (CPU): 15-25 FPS
- Gaming PC (GPU): 60+ FPS
- Older Hardware: 5-15 FPS

**Model Comparison:**
- yolo11n.pt (nano): Fastest, good accuracy ⚡
- yolo11s.pt (small): Balanced
- yolo11m.pt (medium): Better accuracy, slower
- yolo11l.pt (large): Best accuracy, requires GPU

---

## 🎓 Learning Resources

- [YOLO Documentation](https://docs.ultralytics.com/)
- [OpenCV Tutorials](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)

---

## 🆘 Need Help?

Check these in order:
1. This QUICKSTART.md
2. README.md (detailed documentation)
3. Code comments in src/ files
4. Ultralytics YOLO documentation

---

**Happy Detecting! 🎯**
