"""
Quick Detection Launcher
Automatically detects and processes your uploaded images and videos.
"""

import os
import sys


def check_files(folder, extensions):
    """Check if files exist in folder."""
    if not os.path.exists(folder):
        return []
    
    files = [f for f in os.listdir(folder) 
             if any(f.lower().endswith(ext) for ext in extensions)]
    return files


def main():
    print("="*60)
    print("Object Detection - File Processor")
    print("="*60)
    
    # Check for images
    image_folder = "input/images"
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
    images = check_files(image_folder, image_extensions)
    
    # Check for videos
    video_folder = "input/videos"
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
    videos = check_files(video_folder, video_extensions)
    
    print(f"\n📁 Found in input folders:")
    print(f"   • Images: {len(images)} file(s)")
    print(f"   • Videos: {len(videos)} file(s)")
    
    if len(images) == 0 and len(videos) == 0:
        print("\n⚠️ No files found!")
        print("\nTo add files:")
        print("1. Open: input/images/  (for images)")
        print("2. Open: input/videos/  (for videos)")
        print("3. Drag and drop your files")
        print("4. Run this script again")
        
        # Open folders
        response = input("\nOpen folders now? (y/n): ").lower()
        if response == 'y':
            os.system('explorer.exe "input\\images"')
            os.system('explorer.exe "input\\videos"')
            print("✅ Folders opened!")
        return
    
    # Display found files
    if images:
        print(f"\n📷 Images found:")
        for img in images[:5]:  # Show first 5
            print(f"   • {img}")
        if len(images) > 5:
            print(f"   ... and {len(images)-5} more")
    
    if videos:
        print(f"\n🎬 Videos found:")
        for vid in videos[:5]:  # Show first 5
            print(f"   • {vid}")
        if len(videos) > 5:
            print(f"   ... and {len(videos)-5} more")
    
    # Ask what to process
    print("\n" + "="*60)
    print("What would you like to detect?")
    print("="*60)
    
    options = []
    if images:
        options.append("1. Detect objects in IMAGES")
    if videos:
        options.append("2. Detect objects in VIDEOS")
    options.append("3. Open input folders")
    options.append("4. Exit")
    
    for opt in options:
        print(opt)
    
    choice = input("\nEnter choice: ").strip()
    
    if choice == '1' and images:
        print("\n🚀 Starting image detection...")
        print("Press any key to continue between images")
        os.system('venv\\Scripts\\python.exe src\\detect_image_blip.py')
        
    elif choice == '2' and videos:
        print("\n🚀 Starting video detection...")
        print("Controls: q=quit, p=pause/resume, c=refresh caption")
        os.system('venv\\Scripts\\python.exe src\\detect_video_blip.py')
        
    elif choice == '3':
        os.system('explorer.exe "input\\images"')
        os.system('explorer.exe "input\\videos"')
        print("✅ Folders opened!")
        
    elif choice == '4':
        print("Goodbye! 👋")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
