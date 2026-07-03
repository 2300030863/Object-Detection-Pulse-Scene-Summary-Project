"""
Setup Script for Object Detection Project
Run this script to set up the project environment.
"""

import os
import sys
import subprocess


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python_version():
    """Check if Python version is compatible."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("\n❌ Error: Python 3.8 or higher is required")
        print("Please upgrade Python and try again.")
        return False
    
    print("✅ Python version is compatible")
    return True


def create_virtual_environment():
    """Create a virtual environment."""
    print_header("Creating Virtual Environment")
    
    if os.path.exists("venv"):
        print("Virtual environment already exists")
        response = input("Do you want to recreate it? (y/n): ").lower()
        if response == 'y':
            print("Removing existing virtual environment...")
            if sys.platform == "win32":
                os.system("rmdir /s /q venv")
            else:
                os.system("rm -rf venv")
        else:
            print("Skipping virtual environment creation")
            return True
    
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False


def get_pip_executable():
    """Get the pip executable path based on OS."""
    if sys.platform == "win32":
        return os.path.join("venv", "Scripts", "pip.exe")
    else:
        return os.path.join("venv", "bin", "pip")


def install_dependencies():
    """Install project dependencies."""
    print_header("Installing Dependencies")
    
    pip_path = get_pip_executable()
    
    if not os.path.exists(pip_path):
        print("❌ Error: Virtual environment not found")
        print("Please create virtual environment first")
        return False
    
    print("Upgrading pip...")
    try:
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        print("✅ Pip upgraded successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Warning: Could not upgrade pip: {e}")
    
    print("\nInstalling project dependencies...")
    print("This may take several minutes...")
    
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def verify_installation():
    """Verify that key packages are installed."""
    print_header("Verifying Installation")
    
    pip_path = get_pip_executable()
    
    required_packages = ['ultralytics', 'opencv-python', 'torch', 'numpy']
    
    print("Checking installed packages...")
    try:
        result = subprocess.run(
            [pip_path, "list"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        installed = result.stdout.lower()
        all_found = True
        
        for package in required_packages:
            if package.lower() in installed:
                print(f"  ✅ {package}")
            else:
                print(f"  ❌ {package} - NOT FOUND")
                all_found = False
        
        return all_found
    except subprocess.CalledProcessError as e:
        print(f"❌ Error verifying installation: {e}")
        return False


def create_placeholder_files():
    """Create placeholder files to maintain directory structure."""
    print_header("Creating Directory Structure")
    
    dirs_to_create = [
        "models",
        "input/images",
        "input/videos",
        "output"
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
        
        # Create .gitkeep file
        gitkeep_path = os.path.join(dir_path, ".gitkeep")
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write("")
    
    print("✅ Directory structure created")


def print_next_steps():
    """Print instructions for next steps."""
    print_header("Setup Complete!")
    
    print("\n🎉 Your Object Detection project is ready to use!")
    print("\nNext steps:")
    print("\n1. Activate virtual environment:")
    
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Run object detection:")
    print("   - For images:  python src/detect_image_blip.py")
    print("   - For videos:  python src/detect_video_blip.py")
    print("   - For camera:  python src/detect_camera_blip.py")
    
    print("\n3. Add your input files:")
    print("   - Images: input/images/")
    print("   - Videos: input/videos/")
    
    print("\n4. Check README.md for detailed documentation")
    
    print("\n" + "="*60)


def main():
    """Main setup function."""
    print_header("Object Detection Project Setup")
    print("This script will set up your development environment")
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\n❌ Setup failed at virtual environment creation")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\n⚠️ Warning: Some packages may not be installed correctly")
    
    # Create directory structure
    create_placeholder_files()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
