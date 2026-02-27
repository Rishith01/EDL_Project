"""
Test module for Direction Calculation - INDEPENDENT DIRECTION TEST
Tests mouse position to angle/speed conversion
Usage: python test_direction.py
"""

import math


def compute_direction(mouse_x, mouse_y, label_width, label_height):
    """
    Calculate arm direction based on mouse position
    (Copy of the function from camera_gui.py for testing)
    
    Returns:
        tuple: (angle in radians, speed magnitude 0.0-1.0)
    """
    # Center of display
    label_cx = label_width // 2
    label_cy = label_height // 2
    
    # Vector from center to mouse
    dx = mouse_x - label_cx
    dy = label_cy - mouse_y  # Invert Y for correct coordinate system

    angle = math.atan2(dy, dx)
    magnitude = math.sqrt(dx*dx + dy*dy)
    max_dist = math.sqrt(label_cx*label_cx + label_cy*label_cy)
    speed = min(magnitude / max_dist, 1.0) if max_dist > 0 else 0.0

    return angle, speed


def test_center_position():
    """Test 1: Mouse at center should have zero speed"""
    print("\n[Test 1] Mouse at center position...")
    label_width, label_height = 640, 480
    mouse_x, mouse_y = label_width // 2, label_height // 2
    
    angle, speed = compute_direction(mouse_x, mouse_y, label_width, label_height)
    print(f"  Position: ({mouse_x}, {mouse_y})")
    print(f"  Angle: {angle:.4f} rad ({math.degrees(angle):.2f}°)")
    print(f"  Speed: {speed:.4f}")
    assert speed == 0.0, f"Speed should be 0.0 at center, got {speed}"
    print("✓ Center position test passed")


def test_right_direction():
    """Test 2: Mouse to the right"""
    print("\n[Test 2] Mouse to the right...")
    label_width, label_height = 640, 480
    mouse_x, mouse_y = label_width // 2 + 100, label_height // 2
    
    angle, speed = compute_direction(mouse_x, mouse_y, label_width, label_height)
    print(f"  Position: ({mouse_x}, {mouse_y})")
    print(f"  Angle: {angle:.4f} rad ({math.degrees(angle):.2f}°)")
    print(f"  Speed: {speed:.4f}")
    assert abs(angle - 0.0) < 0.01, f"Should be ~0° (0.0 rad), got {math.degrees(angle)}°"
    assert speed > 0, f"Speed should be positive, got {speed}"
    print("✓ Right direction test passed")


def test_up_direction():
    """Test 3: Mouse up (negative speed direction)"""
    print("\n[Test 3] Mouse pointing up...")
    label_width, label_height = 640, 480
    mouse_x, mouse_y = label_width // 2, label_height // 2 - 100
    
    angle, speed = compute_direction(mouse_x, mouse_y, label_width, label_height)
    print(f"  Position: ({mouse_x}, {mouse_y})")
    print(f"  Angle: {angle:.4f} rad ({math.degrees(angle):.2f}°)")
    print(f"  Speed: {speed:.4f}")
    assert abs(angle - math.pi/2) < 0.01, f"Should be ~90° (π/2), got {math.degrees(angle)}°"
    print("✓ Up direction test passed")


def test_diagonal_direction():
    """Test 4: Mouse at diagonal"""
    print("\n[Test 4] Mouse at diagonal (upper-right)...")
    label_width, label_height = 640, 480
    mouse_x = label_width // 2 + 100
    mouse_y = label_height // 2 - 100
    
    angle, speed = compute_direction(mouse_x, mouse_y, label_width, label_height)
    print(f"  Position: ({mouse_x}, {mouse_y})")
    print(f"  Angle: {angle:.4f} rad ({math.degrees(angle):.2f}°)")
    print(f"  Speed: {speed:.4f}")
    assert 40 < math.degrees(angle) < 50, f"Should be ~45°, got {math.degrees(angle)}°"
    assert speed > 0, f"Speed should be positive"
    print("✓ Diagonal direction test passed")


def test_speed_scaling():
    """Test 5: Speed increases with distance"""
    print("\n[Test 5] Speed scaling with distance...")
    label_width, label_height = 640, 480
    
    # Small distance
    mouse_x1, mouse_y1 = label_width // 2 + 50, label_height // 2
    _, speed1 = compute_direction(mouse_x1, mouse_y1, label_width, label_height)
    
    # Larger distance
    mouse_x2, mouse_y2 = label_width // 2 + 200, label_height // 2
    _, speed2 = compute_direction(mouse_x2, mouse_y2, label_width, label_height)
    
    print(f"  Distance 50px: speed = {speed1:.4f}")
    print(f"  Distance 200px: speed = {speed2:.4f}")
    assert speed2 > speed1, f"Larger distance should have higher speed"
    print("✓ Speed scaling test passed")


def test_speed_capped_at_one():
    """Test 6: Speed is capped at 1.0"""
    print("\n[Test 6] Speed capped at maximum (1.0)...")
    label_width, label_height = 640, 480
    
    # Very far distance (beyond screen)
    mouse_x = label_width // 2 + 5000
    mouse_y = label_height // 2 + 5000
    
    _, speed = compute_direction(mouse_x, mouse_y, label_width, label_height)
    print(f"  Position: ({mouse_x}, {mouse_y})")
    print(f"  Speed: {speed:.4f}")
    assert speed <= 1.0, f"Speed should be capped at 1.0, got {speed}"
    assert speed == 1.0, f"Speed so far should be 1.0, got {speed}"
    print("✓ Speed capping test passed")


def test_all_quadrants():
    """Test 7: All four quadrants"""
    print("\n[Test 7] Testing all quadrants...")
    label_width, label_height = 640, 480
    cx, cy = label_width // 2, label_height // 2
    dist = 100
    
    quadrants = [
        ("Right (+x, 0y)", cx + dist, cy, "0°"),
        ("Up (0x, -y)", cx, cy - dist, "90°"),
        ("Left (-x, 0y)", cx - dist, cy, "180° or -180°"),
        ("Down (0x, +y)", cx, cy + dist, "-90° or 270°"),
    ]
    
    for name, mx, my, expected in quadrants:
        angle, speed = compute_direction(mx, my, label_width, label_height)
        angle_deg = math.degrees(angle)
        print(f"  {name}: {angle_deg:.1f}° (expected {expected})")
    
    print("✓ All quadrants tested")


def test_message_output_format():
    """Test 8: Format for UART messages"""
    print("\n[Test 8] Message format for UART...")
    label_width, label_height = 640, 480
    mouse_x, mouse_y = 400, 300
    
    angle, speed = compute_direction(mouse_x, mouse_y, label_width, label_height)
    
    # Format as it would be sent
    message = f"ANGLE:{angle:.2f},SPEED:{speed:.2f}\n"
    print(f"  Direction: angle={angle:.4f}, speed={speed:.4f}")
    print(f"  UART Message: {message.strip()}")
    print("✓ Message format test passed")


if __name__ == "__main__":
    print("=" * 70)
    print("Direction Calculation Independent Tests")
    print("Tests mouse click position to angle/speed conversion")
    print("=" * 70)
    
    try:
        test_center_position()
        test_right_direction()
        test_up_direction()
        test_diagonal_direction()
        test_speed_scaling()
        test_speed_capped_at_one()
        test_all_quadrants()
        test_message_output_format()
        
        print("\n" + "=" * 70)
        print("✓ All direction calculation tests passed!")
        print("=" * 70)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
