"""
Test module for SocketHandler
Tests TCP socket communication independently
"""

import time
from socket_handler import SocketHandler


def test_socket_handler():
    """Test socket handler initialization and methods"""
    print("=" * 60)
    print("Socket Handler Test")
    print("=" * 60)
    
    # Test 1: Create handler
    print("\n[Test 1] Creating SocketHandler...")
    handler = SocketHandler(host='127.0.0.1', port=5000)
    print(f"✓ Handler created: {handler}")
    print(f"  - Host: {handler.host}")
    print(f"  - Port: {handler.port}")
    print(f"  - Connected: {handler.is_connected}")
    
    # Test 2: Test connection attempt (will fail without server)
    print("\n[Test 2] Attempting connection (will fail without running RPi server)...")
    result = handler.connect()
    print(f"  - Connection result: {result}")
    
    # Test 3: Test sending command (should fail gracefully if not connected)
    print("\n[Test 3] Testing send_command() without connection...")
    handler.send_command(1.57, 0.5)
    print("  - No error raised (expected if disconnected)")
    
    # Test 4: Test sending capture (should fail gracefully if not connected)
    print("\n[Test 4] Testing send_capture() without connection...")
    handler.send_capture(320, 240)
    print("  - No error raised (expected if disconnected)")
    
    # Test 5: Disconnect
    print("\n[Test 5] Testing disconnect()...")
    handler.disconnect()
    print(f"  - Handler disconnected")
    print(f"  - Is connected: {handler.is_connected}")
    
    print("\n" + "=" * 60)
    print("Socket Handler Test Completed")
    print("=" * 60)


if __name__ == "__main__":
    test_socket_handler()
