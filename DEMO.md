# Demo Guide

## 1. Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Run CLI Mode

```powershell
python run_blip.py
```

Choose a mode from the menu.

## 3. Demo Scenarios

1. Image demo
- Add image files to `input/images`.
- Select image mode from `run_blip.py` menu.
- Verify: detected objects, caption, and summary in terminal output.

2. Video demo
- Add a short MP4 file to `input/videos`.
- Select video mode from `run_blip.py` menu.
- Verify: detection overlay, caption refresh, and final summary.

3. Camera demo
- Select camera mode from `run_blip.py` menu.
- Verify: live detections, updated captions, and summary text.

## 4. CLI Demo (Optional)

```powershell
python run_blip.py
```

Use either `run_blip.py` or `run.ps1` to run image, video, and camera modes.
