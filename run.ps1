# Object Detection System - Quick Launcher
# PowerShell script to easily run different detection modes

param(
    [Parameter(Position=0)]
    [ValidateSet('camera', 'image', 'video', 'test', 'setup', 'help')]
    [string]$Mode = 'help'
)

function Show-Header {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "  Object Detection System - YOLOv11" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Help {
    Show-Header
    Write-Host "Usage: .\run.ps1 <mode>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Available modes:" -ForegroundColor Green
    Write-Host "  camera  - Start real-time camera detection" -ForegroundColor White
    Write-Host "  image   - Detect objects in images" -ForegroundColor White
    Write-Host "  video   - Detect objects in videos" -ForegroundColor White
    Write-Host "  test    - Run system tests" -ForegroundColor White
    Write-Host "  setup   - Run setup script" -ForegroundColor White
    Write-Host "  help    - Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 camera" -ForegroundColor Gray
    Write-Host "  .\run.ps1 image" -ForegroundColor Gray
    Write-Host "  .\run.ps1 video" -ForegroundColor Gray
    Write-Host ""
}

function Test-VirtualEnvironment {
    if (-not (Test-Path "venv\Scripts\activate.ps1")) {
        Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please run setup first:" -ForegroundColor Yellow
        Write-Host "  .\run.ps1 setup" -ForegroundColor White
        Write-Host ""
        return $false
    }
    return $true
}

function Activate-VirtualEnvironment {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

function Run-CameraDetection {
    Show-Header
    Write-Host "Starting Real-time Camera Detection (YOLO + BLIP)..." -ForegroundColor Green
    Write-Host ""
    Write-Host "Controls:" -ForegroundColor Yellow
    Write-Host "  Press 'q' to quit" -ForegroundColor White
    Write-Host "  Press 'c' to generate new AI caption" -ForegroundColor White
    Write-Host "  Press 's' to save current frame" -ForegroundColor White
    Write-Host ""
    
    if (Test-VirtualEnvironment) {
        Activate-VirtualEnvironment
        python src\detect_camera_blip.py
    }
}

function Run-ImageDetection {
    Show-Header
    Write-Host "Starting Image Detection (YOLO + BLIP)..." -ForegroundColor Green
    Write-Host ""
    
    # Check if images exist
    $imageFolder = "input\images"
    if (-not (Test-Path $imageFolder)) {
        New-Item -ItemType Directory -Path $imageFolder -Force | Out-Null
    }
    
    $images = Get-ChildItem -Path (Join-Path $imageFolder '*') -Include *.jpg,*.jpeg,*.png,*.bmp -File
    
    if ($images.Count -eq 0) {
        Write-Host "⚠️ No images found in $imageFolder" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Please add images to the folder and try again." -ForegroundColor White
        Write-Host ""
        return
    }
    
    Write-Host "Found $($images.Count) image(s) to process" -ForegroundColor Green
    Write-Host ""
    
    if (Test-VirtualEnvironment) {
        Activate-VirtualEnvironment
        python src\detect_image_blip.py
    }
}

function Run-VideoDetection {
    Show-Header
    Write-Host "Starting Video Detection (YOLO + BLIP)..." -ForegroundColor Green
    Write-Host ""
    Write-Host "Controls:" -ForegroundColor Yellow
    Write-Host "  Press 'q' to quit" -ForegroundColor White
    Write-Host "  Press 'p' to pause/resume" -ForegroundColor White
    Write-Host "  Press 'c' to refresh caption" -ForegroundColor White
    Write-Host ""
    
    # Check if videos exist
    $videoFolder = "input\videos"
    if (-not (Test-Path $videoFolder)) {
        New-Item -ItemType Directory -Path $videoFolder -Force | Out-Null
    }
    
    $videos = Get-ChildItem -Path (Join-Path $videoFolder '*') -Include *.mp4,*.avi,*.mov,*.mkv -File
    
    if ($videos.Count -eq 0) {
        Write-Host "⚠️ No videos found in $videoFolder" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Please add videos to the folder and try again." -ForegroundColor White
        Write-Host ""
        return
    }
    
    Write-Host "Found $($videos.Count) video(s) to process" -ForegroundColor Green
    Write-Host ""
    
    if (Test-VirtualEnvironment) {
        Activate-VirtualEnvironment
        python src\detect_video_blip.py
    }
}

function Run-Tests {
    Show-Header
    Write-Host "Running System Tests..." -ForegroundColor Green
    Write-Host ""
    
    if (Test-VirtualEnvironment) {
        Activate-VirtualEnvironment
        python test_system.py
    }
}

function Run-Setup {
    Show-Header
    Write-Host "Running Setup..." -ForegroundColor Green
    Write-Host ""
    python setup.py
}

# Main script logic
switch ($Mode) {
    'camera' { Run-CameraDetection }
    'image'  { Run-ImageDetection }
    'video'  { Run-VideoDetection }
    'test'   { Run-Tests }
    'setup'  { Run-Setup }
    'help'   { Show-Help }
    default  { Show-Help }
}
