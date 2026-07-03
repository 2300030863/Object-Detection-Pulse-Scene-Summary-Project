"""
Test Script for Object Detection System
Tests the scene summary module functionality.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scene_summary import SceneSummarizer, create_simple_summary


def print_test_header(test_name):
    """Print formatted test header."""
    print("\n" + "="*60)
    print(f"TEST: {test_name}")
    print("="*60)


def test_single_object():
    """Test detection with single object."""
    print_test_header("Single Object Detection")
    
    summarizer = SceneSummarizer()
    summarizer.add_detection("laptop")
    
    print(summarizer.get_full_summary())
    
    expected = "laptop"
    assert expected in summarizer.generate_summary().lower(), "Test failed!"
    print("\n✅ Test passed!")


def test_multiple_objects():
    """Test detection with multiple objects."""
    print_test_header("Multiple Objects Detection")
    
    summarizer = SceneSummarizer()
    objects = ["person", "laptop", "chair", "bottle"]
    
    for obj in objects:
        summarizer.add_detection(obj)
    
    print(summarizer.get_full_summary())
    
    summary = summarizer.generate_summary().lower()
    assert "person" in summary, "Test failed!"
    print("\n✅ Test passed!")


def test_duplicate_objects():
    """Test detection with duplicate objects."""
    print_test_header("Duplicate Objects Detection")
    
    summarizer = SceneSummarizer()
    objects = ["person", "person", "laptop", "bottle", "bottle", "bottle"]
    
    for obj in objects:
        summarizer.add_detection(obj)
    
    print(summarizer.get_full_summary())
    
    unique = summarizer.get_unique_objects()
    assert unique["person"] == 2, "Test failed!"
    assert unique["bottle"] == 3, "Test failed!"
    print("\n✅ Test passed!")


def test_empty_detection():
    """Test with no objects detected."""
    print_test_header("Empty Detection")
    
    summarizer = SceneSummarizer()
    print(summarizer.get_full_summary())
    
    summary = summarizer.generate_summary().lower()
    assert "no objects" in summary, "Test failed!"
    print("\n✅ Test passed!")


def test_helper_function():
    """Test helper function."""
    print_test_header("Helper Function Test")
    
    objects = ["person", "laptop", "mouse", "keyboard", "monitor"]
    summary = create_simple_summary(objects)
    
    print(summary)
    
    assert "person" in summary.lower(), "Test failed!"
    assert "laptop" in summary.lower(), "Test failed!"
    print("\n✅ Test passed!")


def test_scene_scenarios():
    """Test realistic scene scenarios."""
    print_test_header("Realistic Scene Scenarios")
    
    scenarios = [
        {
            "name": "Office Scene",
            "objects": ["person", "laptop", "keyboard", "mouse", "monitor", "chair"]
        },
        {
            "name": "Living Room",
            "objects": ["person", "couch", "tv", "remote"]
        },
        {
            "name": "Kitchen",
            "objects": ["person", "bottle", "cup", "bowl", "spoon"]
        },
        {
            "name": "Outdoor",
            "objects": ["person", "car", "bicycle", "dog"]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")
        summarizer = SceneSummarizer()
        
        for obj in scenario['objects']:
            summarizer.add_detection(obj)
        
        print(summarizer.get_full_summary())
    
    print("\n✅ All scenarios tested!")


def test_clear_functionality():
    """Test clear functionality."""
    print_test_header("Clear Functionality Test")
    
    summarizer = SceneSummarizer()
    summarizer.add_detection("laptop")
    summarizer.add_detection("mouse")
    
    print("Before clear:")
    print(summarizer.get_detection_list())
    
    summarizer.clear_detections()
    
    print("\nAfter clear:")
    print(summarizer.get_detection_list())
    
    assert len(summarizer.detected_objects) == 0, "Test failed!"
    print("\n✅ Test passed!")


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("OBJECT DETECTION SYSTEM - TEST SUITE")
    print("="*60)
    
    tests = [
        test_single_object,
        test_multiple_objects,
        test_duplicate_objects,
        test_empty_detection,
        test_helper_function,
        test_scene_scenarios,
        test_clear_functionality
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total tests: {passed + failed}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 All tests passed successfully!")
        return True
    else:
        print(f"\n⚠️ {failed} test(s) failed")
        return False


def main():
    """Main test function."""
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
