"""
Enhanced Image Object Detection with BLIP Scene Captioning
Combines YOLOv11 object detection + BLIP AI caption generation.
"""

import cv2
import os
from pathlib import Path
from ultralytics import YOLO
from blip_caption import BLIPCaptioner
import time


class ImageDetectorWithBLIP:
    """
    Enhanced image detector with YOLO + BLIP caption generation.
    """
    
    def __init__(self, model_path="models/yolo11n.pt", confidence=0.5):
        """
        Initialize the detector with YOLO and BLIP models.
        
        Args:
            model_path (str): Path to YOLO model
            confidence (float): Detection confidence threshold
        """
        print(f"\n{'='*60}")
        print("Image Detection + BLIP Caption System")
        print(f"{'='*60}")
        
        # Load YOLO model
        print(f"\n📦 Loading YOLO model: {model_path}")
        self.model = YOLO(model_path)
        self.confidence = confidence
        print(f"✅ YOLO model loaded successfully!")
        
        # Load BLIP captioner
        self.captioner = BLIPCaptioner()
        
        print(f"\n{'='*60}\n")
    
    def detect_and_caption(self, image_path, save_output=True):
        """
        Detect objects and generate AI caption for a single image.
        
        Args:
            image_path (str): Path to input image
            save_output (bool): Whether to save annotated image
            
        Returns:
            dict: Detection results with caption
        """
        print(f"\n📷 Processing: {os.path.basename(image_path)}")
        
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Error: Could not read image {image_path}")
            return None
        
        h, w = image.shape[:2]
        print(f"   Resolution: {w}x{h}")
        
        # Run YOLO detection
        start_time = time.time()
        results = self.model(image, conf=self.confidence, verbose=False)
        detection_time = time.time() - start_time
        
        # Extract detected objects
        detected_objects = []
        detection_details = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class name and confidence
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = self.model.names[cls_id]
                
                detected_objects.append(class_name)
                detection_details.append({
                    'class': class_name,
                    'confidence': conf,
                    'bbox': box.xyxy[0].tolist()
                })
                
                # Draw bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label
                label = f"{class_name} {conf:.2f}"
                cv2.putText(image, label, (x1, y1-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        print(f"   Detected: {len(detected_objects)} objects in {detection_time:.2f}s")
        
        # Generate BLIP caption
        print(f"   🤖 Generating AI caption...")
        caption_start = time.time()
        ai_caption = self.captioner.generate_caption(image, detected_objects)
        caption_time = time.time() - caption_start
        
        print(f"   ✅ Caption: '{ai_caption}' ({caption_time:.2f}s)")
        
        # Add caption overlay to image
        self._add_caption_overlay(image, ai_caption, detected_objects)
        
        # Save output image
        if save_output:
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            output_filename = f"blip_{os.path.basename(image_path)}"
            output_path = output_dir / output_filename
            cv2.imwrite(str(output_path), image)
            print(f"   💾 Saved: {output_path}")
        
        return {
            'image_path': image_path,
            'detected_objects': detected_objects,
            'detection_details': detection_details,
            'ai_caption': ai_caption,
            'detection_time': detection_time,
            'caption_time': caption_time,
            'annotated_image': image
        }
    
    def _add_caption_overlay(self, image, caption, detected_objects):
        """Add caption and detection info overlay to image."""
        h, w = image.shape[:2]
        
        # Create semi-transparent overlay at bottom
        overlay = image.copy()
        overlay_height = 120
        cv2.rectangle(overlay, (0, h-overlay_height), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)
        
        # Add detected objects count
        unique_objects = list(set(detected_objects))
        obj_text = f"Detected: {', '.join(unique_objects[:5])}"
        if len(unique_objects) > 5:
            obj_text += f" +{len(unique_objects)-5} more"
        
        cv2.putText(image, obj_text, (10, h-90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Add AI caption
        cv2.putText(image, "AI Caption:", (10, h-60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Wrap caption text if too long
        max_width = w - 20
        words = caption.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            text_size = cv2.getTextSize(test_line, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0][0]
            
            if text_size < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        # Draw caption lines
        y_pos = h - 30
        for line in lines[:2]:  # Max 2 lines
            cv2.putText(image, line, (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            y_pos += 25
    
    def detect_batch(self, input_folder="input/images"):
        """
        Process all images in a folder with BLIP captioning.
        
        Args:
            input_folder (str): Path to input folder
            
        Returns:
            list: List of detection results
        """
        input_path = Path(input_folder)
        
        if not input_path.exists():
            print(f"❌ Error: Input folder '{input_folder}' not found!")
            return []
        
        # Find all images
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
        image_files = []
        for ext in image_extensions:
            image_files.extend(input_path.glob(f"*{ext}"))
            image_files.extend(input_path.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"\n❌ No images found in '{input_folder}'")
            print("   Supported formats: JPG, JPEG, PNG, BMP, WEBP")
            return []
        
        print(f"\n📂 Found {len(image_files)} images to process")
        print(f"{'='*60}")
        
        # Process each image
        results = []
        total_start = time.time()
        
        for idx, image_path in enumerate(image_files, 1):
            print(f"\n[{idx}/{len(image_files)}]", end=" ")
            result = self.detect_and_caption(str(image_path))
            if result:
                results.append(result)
        
        total_time = time.time() - total_start
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"✅ Batch Processing Complete!")
        print(f"{'='*60}")
        print(f"Total images: {len(results)}")
        print(f"Total time: {total_time:.2f}s")
        print(f"Average time per image: {total_time/len(results):.2f}s")
        print(f"Output folder: output/")
        print(f"{'='*60}\n")
        
        return results


def main():
    """Main function for interactive image detection with BLIP."""
    
    print("\n" + "="*60)
    print("🚀 YOLO + BLIP Image Detection System")
    print("="*60)
    
    # Initialize detector
    detector = ImageDetectorWithBLIP(confidence=0.5)
    
    # Process images
    results = detector.detect_batch("input/images")
    
    if results:
        print("\n📊 Sample Results:")
        print("="*60)
        for i, result in enumerate(results[:3], 1):  # Show first 3
            print(f"\n[{i}] {os.path.basename(result['image_path'])}")
            print(f"    Objects: {len(result['detected_objects'])}")
            print(f"    Caption: '{result['ai_caption']}'")
        
        if len(results) > 3:
            print(f"\n... and {len(results)-3} more images processed")


if __name__ == "__main__":
    main()
