"""
Scene Summary Module
Generates human-readable descriptions of detected objects in a scene.
"""

from collections import Counter


class SceneSummarizer:
    """
    A class to generate scene summaries from detected objects.
    """
    
    def __init__(self):
        """Initialize the SceneSummarizer."""
        self.detected_objects = []
    
    def add_detection(self, object_name):
        """
        Add a detected object to the list.
        
        Args:
            object_name (str): Name of the detected object
        """
        if object_name:
            self.detected_objects.append(object_name)
    
    def clear_detections(self):
        """Clear all detected objects."""
        self.detected_objects = []
    
    def get_unique_objects(self):
        """
        Get list of unique detected objects with their counts.
        
        Returns:
            dict: Dictionary of objects and their counts
        """
        return dict(Counter(self.detected_objects))
    
    def generate_summary(self):
        """
        Generate a natural language summary of the scene.
        
        Returns:
            str: Human-readable scene description
        """
        if not self.detected_objects:
            return "No objects detected in the scene."
        
        # Get unique objects
        unique_objects = list(set(self.detected_objects))
        num_objects = len(unique_objects)
        
        if num_objects == 0:
            return "No objects detected in the scene."
        elif num_objects == 1:
            return f"A {unique_objects[0]} is present in the scene."
        elif num_objects == 2:
            return f"A {unique_objects[0]} and {unique_objects[1]} are present in the scene."
        else:
            # Create a natural sentence with multiple objects
            objects_str = ", ".join(unique_objects[:-1])
            last_object = unique_objects[-1]
            
            # Detect if person is in the scene for better description
            if 'person' in unique_objects:
                other_objects = [obj for obj in unique_objects if obj != 'person']
                if other_objects:
                    if len(other_objects) == 1:
                        return f"A person is near a {other_objects[0]}."
                    else:
                        objects_list = ", ".join(other_objects[:-1])
                        return f"A person is near a {objects_list} and {other_objects[-1]}."
                else:
                    return "A person is present in the scene."
            
            return f"The scene contains {objects_str} and {last_object}."
    
    def get_detection_list(self):
        """
        Get formatted list of detected objects with counts.
        
        Returns:
            str: Formatted string of detected objects
        """
        if not self.detected_objects:
            return "No objects detected."
        
        unique_objects = self.get_unique_objects()
        output = "Detected Objects:\n"
        
        for obj, count in unique_objects.items():
            if count > 1:
                output += f"  - {obj.capitalize()} (x{count})\n"
            else:
                output += f"  - {obj.capitalize()}\n"
        
        return output
    
    def get_full_summary(self):
        """
        Get complete summary including object list and scene description.
        
        Returns:
            str: Complete formatted summary
        """
        object_list = self.get_detection_list()
        scene_summary = self.generate_summary()
        
        return f"{object_list}\nScene Summary:\n  \"{scene_summary}\""


def create_simple_summary(object_names):
    """
    Create a simple summary from a list of object names.
    
    Args:
        object_names (list): List of detected object names
        
    Returns:
        str: Scene summary
    """
    summarizer = SceneSummarizer()
    for obj in object_names:
        summarizer.add_detection(obj)
    return summarizer.get_full_summary()


# Example usage
if __name__ == "__main__":
    # Test the summarizer
    print("=== Scene Summary Module Test ===\n")
    
    # Test Case 1: Single object
    print("Test 1: Single object")
    summarizer1 = SceneSummarizer()
    summarizer1.add_detection("laptop")
    print(summarizer1.get_full_summary())
    print()
    
    # Test Case 2: Multiple objects
    print("Test 2: Multiple objects")
    summarizer2 = SceneSummarizer()
    objects = ["person", "laptop", "chair", "bottle"]
    for obj in objects:
        summarizer2.add_detection(obj)
    print(summarizer2.get_full_summary())
    print()
    
    # Test Case 3: Duplicate objects
    print("Test 3: Duplicate objects")
    summarizer3 = SceneSummarizer()
    objects = ["person", "person", "laptop", "bottle", "bottle"]
    for obj in objects:
        summarizer3.add_detection(obj)
    print(summarizer3.get_full_summary())
    print()
    
    # Test Case 4: Using helper function
    print("Test 4: Helper function")
    objects = ["person", "laptop", "mouse", "keyboard"]
    print(create_simple_summary(objects))
