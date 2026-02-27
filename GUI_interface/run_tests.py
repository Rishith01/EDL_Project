"""
Master Test Runner - Run All Independent Tests
Tests all components: UART, Camera, Direction Calculation, and GUI
Usage: python run_tests.py
"""

import sys
import subprocess


def run_test(test_name, test_file):
    """Run a single test file and report results"""
    print("\n" + "=" * 70)
    print(f"Running: {test_name}")
    print("=" * 70)
    
    try:
        result = subprocess.run([sys.executable, test_file], capture_output=False)
        if result.returncode == 0:
            print(f"✓ {test_name} PASSED")
            return True
        else:
            print(f"✗ {test_name} FAILED")
            return False
    except Exception as e:
        print(f"✗ {test_name} ERROR: {e}")
        return False


def main():
    """Run all independent tests"""
    print("\n" + "=" * 70)
    print("ROBOTIC ARM CONTROL - INDEPENDENT TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("UART Handler Test", "test_uart_handler.py"),
        ("Camera Test", "test_camera.py"),
        ("Direction Calculation Test", "test_direction.py"),
        ("GUI Test", "test_gui.py"),
    ]
    
    results = {}
    
    for test_name, test_file in tests:
        results[test_name] = run_test(test_name, test_file)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✓ PASSED" if passed_flag else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
