"""
Test module for Camera - INDEPENDENT CAMERA TEST
Tests camera detection, frame capture, and properties independently
Usage: python test_camera.py
"""

import cv2
import time


def test_camera_detection():
    """Test 1: Detect all available cameras"""
    print("\n[Test 1] Detecting available cameras...")
    available_cameras = []
    
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
            print(f"  ✓ Camera {i} available")
        else:
            print(f"  ✗ Camera {i} not found")
    
    if not available_cameras:
        print("  ⚠ No cameras detected!")
        return []

    print(f"  Found {len(available_cameras)} camera(s): {available_cameras}")
    return available_cameras


def test_camera_properties(camera_index):
    """Test 2: Get camera hardware properties"""
    print("\n[Test 2] Getting camera properties...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"  ✗ Cannot open camera {camera_index}")
        return False
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    contrast = cap.get(cv2.CAP_PROP_CONTRAST)
    saturation = cap.get(cv2.CAP_PROP_SATURATION)
    
    print(f"  ✓ Camera {camera_index} Properties:")
    print(f"    - Resolution: {width}x{height} pixels")
    print(f"    - FPS setting: {fps}")
    print(f"    - Brightness: {brightness}")
    print(f"    - Contrast: {contrast}")
    print(f"    - Saturation: {saturation}")
    
    cap.release()
    return True


def test_frame_capture(camera_index):
    """Test 3: Capture and analyze frame"""
    print("\n[Test 3] Capturing frame...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"  ✗ Cannot open camera {camera_index}")
        return False
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("  ✗ Failed to capture frame")
        return False
    
    h, w, c = frame.shape
    print(f"  ✓ Frame captured:")
    print(f"    - Shape: {w}x{h}x{c}")
    print(f"    - Data type: {frame.dtype}")
    print(f"    - Size in memory: {frame.nbytes / 1024:.1f} KB")
    
    # Check frame validity
    min_val = frame.min()
    max_val = frame.max()
    mean_val = frame.mean()
    print(f"    - Pixel value range: {min_val}-{max_val} (mean: {mean_val:.1f})")
    
    return True


def test_frame_rate(camera_index, num_frames=30):
    """Test 4: Measure actual frame capture rate"""
    print(f"\n[Test 4] Measuring frame rate ({num_frames} frames)...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"  ✗ Cannot open camera {camera_index}")
        return False
    
    start_time = time.time()
    successful_frames = 0
    failed_frames = 0
    
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            successful_frames += 1
        else:
            failed_frames += 1
    
    elapsed = time.time() - start_time
    fps = successful_frames / elapsed if elapsed > 0 else 0
    
    print(f"  ✓ Capture complete:")
    print(f"    - Frames captured: {successful_frames}/{num_frames}")
    print(f"    - Failed frames: {failed_frames}")
    print(f"    - Time elapsed: {elapsed:.2f} seconds")
    print(f"    - Actual FPS: {fps:.2f}")
    
    cap.release()
    return True


def test_frame_color_conversion(camera_index):
    """Test 5: Test BGR to RGB conversion"""
    print("\n[Test 5] Testing color conversion...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"  ✗ Cannot open camera {camera_index}")
        return False
    
    ret, frame_bgr = cap.read()
    cap.release()
    
    if not ret:
        print("  ✗ Failed to capture frame")
        return False
    
    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    
    print(f"  ✓ Conversion successful:")
    print(f"    - Original: BGR (OpenCV format)")
    print(f"    - Converted: RGB (PyQt5 format)")
    print(f"    - Shape preserved: {frame_bgr.shape == frame_rgb.shape}")
    
    return True


def test_rectangle_drawing(camera_index):
    """Test 6: Test ROI extraction (rectangle drawing)"""
    print("\n[Test 6] Testing ROI extraction...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"  ✗ Cannot open camera {camera_index}")
        return False
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("  ✗ Failed to capture frame")
        return False
    
    h, w = frame.shape[:2]
    
    # Define ROI (Region of Interest)
    center_x, center_y = w // 2, h // 2
    roi_size = 60
    x1 = max(0, center_x - roi_size)
    y1 = max(0, center_y - roi_size)
    x2 = min(w, center_x + roi_size)
    y2 = min(h, center_y + roi_size)
    
    roi = frame[y1:y2, x1:x2].copy()
    
    print(f"  ✓ ROI extraction successful:")
    print(f"    - Frame size: {w}x{h}")
    print(f"    - ROI center: ({center_x}, {center_y})")
    print(f"    - ROI coordinates: ({x1},{y1}) to ({x2},{y2})")
    print(f"    - ROI size: {roi.shape[1]}x{roi.shape[0]}")
    
    return True


def test_multiple_cameras(available_cameras):
    """Test 7: Switch between multiple cameras"""
    if len(available_cameras) < 2:
        print("\n[Test 7] Skipping - only one camera available")
        return True
    
    print(f"\n[Test 7] Testing camera switching ({len(available_cameras)} cameras)...")
    
    for cam_idx in available_cameras:
        cap = cv2.VideoCapture(cam_idx)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"  ✓ Camera {cam_idx}: ✓")
            else:
                print(f"  - Camera {cam_idx}: No frame")
            cap.release()
        else:
            print(f"  ✗ Camera {cam_idx}: Failed to open")
    
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Camera Independent Tests")
    print("Tests camera detection, properties, frame capture")
    print("=" * 70)
    
    try:
        # Detect available cameras
        available_cameras = test_camera_detection()
        if not available_cameras:
            print("\n✗ No cameras available - tests aborted")
            exit(1)

        # Run tests for each detected camera
        for camera_idx in available_cameras:
            print("\n" + "-" * 60)
            print(f"Running tests for camera {camera_idx}")
            print("-" * 60)
            test_camera_properties(camera_idx)
            test_frame_capture(camera_idx)
            test_frame_rate(camera_idx, num_frames=30)
            test_frame_color_conversion(camera_idx)
            test_rectangle_drawing(camera_idx)

        # Multi-camera switching test using detected list
        test_multiple_cameras(available_cameras)
        
        print("\n" + "=" * 70)
        print("✓ All camera tests completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
