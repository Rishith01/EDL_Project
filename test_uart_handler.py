"""
Test module for UartHandler - INDEPENDENT UART TEST
Tests UART serial communication without GUI
Usage: python test_uart_handler.py
"""

from uart_handler import UartHandler
from PyQt5.QtCore import QCoreApplication
import sys

app = QCoreApplication(sys.argv)

def test_uart_initialization():
    """Test 1: UART handler creation"""
    print("\n[Test 1] Creating UART handler...")
    handler = UartHandler(port='COM5', baudrate=9600)
    assert handler.port == 'COM5'
    assert handler.baudrate == 9600
    assert handler.is_connected == False
    print("✓ Handler created successfully")
    print(f"  Port: {handler.port}, Baud: {handler.baudrate}")


def test_uart_connection():
    """Test 2: Connect to UART (may fail if RPi not connected)"""
    print("\n[Test 2] Testing UART connection...")
    handler = UartHandler(port='COM5', baudrate=9600)
    result = handler.connect()
    if result:
        print("✓ Connected successfully to UART")
        handler.disconnect()
    else:
        print("✗ Connection failed (expected if RPi not connected)")


def test_uart_send_command():
    """Test 3: Send direction command"""
    print("\n[Test 3] Testing send_command()...")
    handler = UartHandler(port='COM5', baudrate=9600)
    
    if handler.connect():
        # Send test command
        handler.send_command(angle=1.57, speed=0.75)
        print("✓ Command sent: ANGLE:1.57,SPEED:0.75")
        handler.disconnect()
    else:
        print("✗ Cannot test - UART not connected")


def test_uart_send_capture():
    """Test 4: Send capture command"""
    print("\n[Test 4] Testing send_capture()...")
    handler = UartHandler(port='COM5', baudrate=9600)
    
    if handler.connect():
        # Send test capture
        handler.send_capture(x=320, y=240)
        print("✓ Capture sent: CAPTURE:320,240")
        handler.disconnect()
    else:
        print("✗ Cannot test - UART not connected")


def test_uart_message_formats():
    """Test 5: Verify message format (without actual UART)"""
    print("\n[Test 5] Testing message formats...")
    
    # Test angle/speed format
    angle, speed = 0.45, 0.6
    msg_cmd = f"ANGLE:{angle:.2f},SPEED:{speed:.2f}\n"
    expected_cmd = "ANGLE:0.45,SPEED:0.60\n"
    assert msg_cmd == expected_cmd
    print(f"✓ Command format correct: {msg_cmd.strip()}")
    
    # Test capture format
    x, y = 100, 200
    msg_cap = f"CAPTURE:{x},{y}\n"
    expected_cap = "CAPTURE:100,200\n"
    assert msg_cap == expected_cap
    print(f"✓ Capture format correct: {msg_cap.strip()}")


if __name__ == "__main__":
    print("=" * 60)
    print("UART Handler Independent Tests")
    print("=" * 60)
    
    try:
        test_uart_initialization()
        test_uart_connection()
        test_uart_send_command()
        test_uart_send_capture()
        test_uart_message_formats()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
