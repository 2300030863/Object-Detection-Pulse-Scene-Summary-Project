"""
YOLO + BLIP Detection System Launcher
Interactive menu to choose between detection modes with AI captioning.
"""

import os
import sys
from pathlib import Path


def print_header():
    """Print welcome header."""
    print("\n" + "="*70)
    print("🚀 YOLO + BLIP Object Detection & Scene Caption System")
    print("="*70)
    print("\nAI-Powered Detection with Natural Language Scene Understanding")
    print("\nFeatures:")
    print("  ✅ YOLOv11 Object Detection (80 COCO classes)")
    print("  ✅ BLIP AI Scene Captioning (Salesforce/blip-image-captioning-base)")
    print("  ✅ Real-time processing for images, videos, and camera")
    print("="*70)


def check_resources():
    """Check if required files and folders exist."""
    issues = []
    
    # Check model
    if not Path("models/yolo11n.pt").exists() and not Path("models/yolov8n.pt").exists():
        issues.append("❌ YOLO model not found (will auto-download)")
    
    # Check input folders
    if not Path("input/images").exists():
        Path("input/images").mkdir(parents=True, exist_ok=True)
        issues.append("📁 Created: input/images/")
    
    if not Path("input/videos").exists():
        Path("input/videos").mkdir(parents=True, exist_ok=True)
        issues.append("📁 Created: input/videos/")
    
    # Check output folder
    if not Path("output").exists():
        Path("output").mkdir(exist_ok=True)
        issues.append("📁 Created: output/")
    
    if issues:
        print("\n⚠ Setup Notes:")
        for issue in issues:
            print(f"   {issue}")
        print()


def show_menu():
    """Display interactive menu."""
    print("\n" + "="*70)
    print("📋 Select Detection Mode:")
    print("="*70)
    
    print("\n🖼  Image Detection:")
    print("   [1] Process images with BLIP AI captions")
    
    print("\n🎬 Video Detection:")
    print("   [3] Process videos with BLIP AI captions")
    
    print("\n📹 Camera Detection:")
    print("   [5] Real-time camera with BLIP AI captions")
    
    print("\n🧪 Testing:")
    print("   [7] Test BLIP caption model")
    print("   [8] Run system tests")
    
    print("\n📊 Information:")
    print("   [9] View project structure")
    print("   [0] Exit")
    
    print("\n" + "="*70)


def run_detection(choice):
    """Run selected detection mode."""
    
    if choice == "1":
        print("\n🚀 Starting Image Detection with BLIP...")
        print("="*70)
        os.system(f"{sys.executable} src/detect_image_blip.py")
    
    elif choice == "2":
        print("\nℹ Basic image mode was removed; using BLIP image mode instead...")
        print("="*70)
        os.system(f"{sys.executable} src/detect_image_blip.py")
    
    elif choice == "3":
        print("\n🚀 Starting Video Detection with BLIP...")
        print("="*70)
        os.system(f"{sys.executable} src/detect_video_blip.py")
    
    elif choice == "4":
        print("\nℹ Basic video mode was removed; using BLIP video mode instead...")
        print("="*70)
        os.system(f"{sys.executable} src/detect_video_blip.py")
    
    elif choice == "5":
        print("\n🚀 Starting Camera Detection with BLIP...")
        print("="*70)
        print("Controls: q=quit | c=refresh caption | s=save frame")
        print("="*70)
        os.system(f"{sys.executable} src/detect_camera_blip.py")

    elif choice == "6":
        print("\nℹ Basic camera mode was removed; using BLIP camera mode instead...")
        print("="*70)
        print("Controls: q=quit | c=refresh caption | s=save frame")
        print("="*70)
        os.system(f"{sys.executable} src/detect_camera_blip.py")
    
    elif choice == "7":
        print("\n🧪 Testing BLIP Caption Model...")
        print("="*70)
        os.system(f"{sys.executable} src/blip_caption.py")
    
    elif choice == "8":
        print("\n🧪 Running System Tests...")
        print("="*70)
        os.system(f"{sys.executable} test_system.py")
    
    elif choice == "9":
        show_project_info()
    
    elif choice == "0":
        print("\n👋 Goodbye!")
        print("="*70)
        return False
    
    else:
        print("\n❌ Invalid choice! Please select 0-9.")
    
    return True


def show_project_info():
    """Display project structure and information."""
    print("\n" + "="*70)
    print("📁 Project Structure:")
    print("="*70)
    
    structure = """
    object_detection_project/
    │
    ├── models/
    │   └── yolo11n.pt              # YOLO model (auto-downloaded)
    │
    ├── input/
    │   ├── images/                 # Place images here (.jpg, .png, etc.)
    │   └── videos/                 # Place videos here (.mp4, .avi, etc.)
    │
    ├── output/                     # Detection results saved here
    │
    ├── src/
    │   ├── blip_caption.py         # 🆕 BLIP AI caption generator
    │   ├── detect_image_blip.py    # 🆕 Image detection + BLIP
    │   ├── detect_video_blip.py    # 🆕 Video detection + BLIP
    │   ├── detect_camera_blip.py   # 🆕 Camera detection + BLIP
    │   └── scene_summary.py        # Simple scene summarizer
    │
    └── run_blip.py                 # 👈 This launcher script
    
    """
    print(structure)
    
    print("="*70)
    print("💡 Quick Start:")
    print("="*70)
    print("  1. Add images to 'input/images/' folder")
    print("  2. Add videos to 'input/videos/' folder")
    print("  3. Run this script and select a detection mode")
    print("  4. Results saved in 'output/' folder")
    print("="*70)
    
    print("\n📊 Model Information:")
    print("="*70)
    print("  YOLO Model: YOLOv11n (Nano)")
    print("    - 80 COCO object classes")
    print("    - Real-time detection (30+ FPS on GPU)")
    print("    - Confidence threshold: 0.5")
    print("\n  BLIP Model: Salesforce/blip-image-captioning-base")
    print("    - AI-powered scene captioning")
    print("    - Natural language descriptions")
    print("    - Contextual understanding")
    print("="*70)
    
    input("\nPress Enter to continue...")


def main():
    """Main launcher function."""
    
    # Print header
    print_header()
    
    # Check resources
    check_resources()
    
    # Main loop
    while True:
        show_menu()
        
        try:
            choice = input("\n👉 Enter your choice (0-9): ").strip()
            
            if not run_detection(choice):
                break
        
        except KeyboardInterrupt:
            print("\n\n⚠ Interrupted by user")
            print("👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
