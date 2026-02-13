"""
Test module for Camera Detection
Tests camera initialization and frame capture independently
"""

import cv2
import sys


def test_camera_detection():
    """Test available cameras on the system"""
    print("=" * 60)
    print("Camera Detection Test")
    print("=" * 60)
    
    # Test 1: Detect cameras
    print("\n[Test 1] Detecting available cameras...")
    available_cameras = []
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            # Get camera properties
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            print(f"  ✓ Camera {i} found - {int(width)}x{int(height)} @ {fps:.1f} FPS")
            cap.release()
        else:
            print(f"  ✗ Camera {i} not available")
    
    if not available_cameras:
        print("  ⚠ No cameras detected!")
        return
    
    # Test 2: Open first camera and capture frame
    print(f"\n[Test 2] Opening Camera {available_cameras[0]} and capturing frame...")
    cap = cv2.VideoCapture(available_cameras[0])
    
    if not cap.isOpened():
        print("  ✗ Failed to open camera")
        return
    
    ret, frame = cap.read()
    if ret:
        h, w, c = frame.shape
        print(f"  ✓ Frame captured successfully")
        print(f"    - Resolution: {w}x{h}")
        print(f"    - Channels: {c}")
    else:
        print("  ✗ Failed to capture frame")
    
    cap.release()
    
    # Test 3: Test frame rate
    print(f"\n[Test 3] Testing frame capture rate (10 frames)...")
    cap = cv2.VideoCapture(available_cameras[0])
    
    import time
    start = time.time()
    for i in range(10):
        ret, frame = cap.read()
        if not ret:
            print(f"  ✗ Failed to capture frame {i}")
            break
    elapsed = time.time() - start
    fps = 10 / elapsed
    print(f"  ✓ Captured 10 frames in {elapsed:.2f}s ({fps:.1f} FPS)")
    
    cap.release()
    
    print("\n" + "=" * 60)
    print("Camera Detection Test Completed")
    print("=" * 60)


if __name__ == "__main__":
    test_camera_detection()
