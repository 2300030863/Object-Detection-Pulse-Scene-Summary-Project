"""
BLIP Scene Caption Module
Uses Salesforce BLIP model for AI-powered image captioning.
"""

import torch
from PIL import Image
import cv2
import numpy as np


class BLIPCaptioner:
    """
    A class to generate AI-powered scene captions using BLIP model.
    """
    
    def __init__(self, model_name="Salesforce/blip-image-captioning-base"):
        """
        Initialize the BLIP Captioner.
        
        Args:
            model_name (str): Hugging Face model identifier
        """
        print(f"\n{'='*60}")
        print(f"Loading BLIP Caption Model: {model_name}")
        print(f"{'='*60}")
        print("⏳ Downloading model... (first time only, ~1GB)")
        
        try:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            
            self.processor = BlipProcessor.from_pretrained(model_name)
            self.model = BlipForConditionalGeneration.from_pretrained(model_name)
            
            # Move to GPU if available
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = self.model.to(self.device)
            
            print(f"✅ Model loaded successfully on {self.device.upper()}!")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"❌ Error loading BLIP model: {e}")
            print("💡 Install required libraries: pip install transformers")
            raise
    
    def generate_caption(self, image, detected_objects=None):
        """
        Generate AI caption for an image.
        
        Args:
            image: Input image (OpenCV BGR, PIL Image, or numpy array)
            detected_objects (list): Optional list of detected objects to guide caption
            
        Returns:
            str: AI-generated scene caption
        """
        try:
            # Convert different image formats to PIL Image
            if isinstance(image, np.ndarray):
                # OpenCV BGR to RGB
                if len(image.shape) == 3 and image.shape[2] == 3:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(image)
            elif isinstance(image, Image.Image):
                pil_image = image
            else:
                raise ValueError(f"Unsupported image type: {type(image)}")
            
            # Generate caption with conditional text (if objects provided)
            if detected_objects and len(detected_objects) > 0:
                # Create context prompt from detected objects
                obj_list = ", ".join(set(detected_objects[:5]))  # Top 5 unique objects
                text_prompt = f"a photo of {obj_list}"
                inputs = self.processor(pil_image, text=text_prompt, return_tensors="pt").to(self.device)
            else:
                # Unconditional caption generation
                inputs = self.processor(pil_image, return_tensors="pt").to(self.device)
            
            # Generate caption
            with torch.no_grad():
                output_ids = self.model.generate(**inputs, max_length=50, num_beams=3)
            
            # Decode caption
            caption = self.processor.decode(output_ids[0], skip_special_tokens=True)
            
            return caption
            
        except Exception as e:
            print(f"❌ Error generating caption: {e}")
            return "Error generating scene caption."
    
    def generate_batch_captions(self, images, detected_objects_list=None):
        """
        Generate captions for multiple images.
        
        Args:
            images (list): List of images
            detected_objects_list (list): Optional list of detected object lists
            
        Returns:
            list: List of generated captions
        """
        captions = []
        
        for i, image in enumerate(images):
            objects = detected_objects_list[i] if detected_objects_list else None
            caption = self.generate_caption(image, objects)
            captions.append(caption)
        
        return captions


def test_blip_caption():
    """
    Test function to verify BLIP caption generation.
    """
    print("\n" + "="*60)
    print("Testing BLIP Scene Caption Model")
    print("="*60)
    
    try:
        # Initialize captioner
        captioner = BLIPCaptioner()
        
        # Test with sample image (create a simple test image)
        print("\n📷 Creating test image...")
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(test_image, "Object Detection + BLIP", (50, 240),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Generate caption
        print("🤖 Generating AI caption...")
        caption = captioner.generate_caption(test_image)
        
        print(f"\n✅ Generated Caption:")
        print(f"   '{caption}'")
        
        # Test with object context
        print("\n🎯 Testing with detected objects context...")
        test_objects = ["person", "laptop", "chair"]
        caption_with_context = captioner.generate_caption(test_image, test_objects)
        
        print(f"✅ Contextual Caption:")
        print(f"   Detected: {', '.join(test_objects)}")
        print(f"   Caption: '{caption_with_context}'")
        
        print("\n" + "="*60)
        print("✅ BLIP Caption Model Test Complete!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    test_blip_caption()
