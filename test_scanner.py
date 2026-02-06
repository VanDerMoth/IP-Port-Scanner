#!/usr/bin/env python3
"""
Test script for IP Port Scanner core functionality
"""

import socket
import threading
import time
import sys
import os

# Test the PortScanner class without GUI
def test_port_scanner():
    """Test the core port scanning functionality"""
    print("=" * 60)
    print("IP Port Scanner - Core Functionality Tests")
    print("=" * 60)
    
    # Add the script directory to path for imports
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    
    # Import scanner components by reading only what's needed
    scanner_file = os.path.join(script_dir, 'port_scanner.py')
    with open(scanner_file, 'r') as f:
        lines = f.readlines()
    
    # Extract non-GUI code (imports, constants, PortScanner class)
    scanner_code = []
    gui_started = False
    
    for line in lines:
        # Skip GUI-related imports
        if 'import tkinter' in line or 'from tkinter' in line:
            continue
        # Stop before GUI class definition
        if 'class PortScannerGUI:' in line:
            gui_started = True
            break
        if not gui_started:
            scanner_code.append(line)
    
    # Load the scanner code into globals
    exec(''.join(scanner_code), globals())
    
    print("\n1. Testing IP validation...")
    test_ips = [
        ("127.0.0.1", True),
        ("192.168.1.1", True),
        ("256.1.1.1", False),
        ("invalid", False),
        ("", False)
    ]
    
    import re
    pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
    for ip, expected in test_ips:
        valid = False
        if pattern.match(ip):
            parts = ip.split('.')
            valid = all(0 <= int(part) <= 255 for part in parts)
        result = "✓" if valid == expected else "✗"
        print(f"  {result} IP: {ip:20s} Valid: {valid} (Expected: {expected})")
    
    print("\n2. Testing port validation...")
    test_ports = [
        ("80", True),
        ("65535", True),
        ("0", False),
        ("65536", False),
        ("abc", False)
    ]
    
    for port, expected in test_ports:
        try:
            port_num = int(port)
            valid = 1 <= port_num <= 65535
        except ValueError:
            valid = False
        result = "✓" if valid == expected else "✗"
        print(f"  {result} Port: {port:10s} Valid: {valid} (Expected: {expected})")
    
    print("\n3. Testing port scanning with test server...")
    
    # Start a test server on a high port
    test_port = 9876
    server_socket = None
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', test_port))
        server_socket.listen(1)
        print(f"  Started test server on port {test_port}")
        
        # Test scanning a closed port
        print(f"\n  Testing scan on closed port 9999...")
        scanner = PortScanner('127.0.0.1', 9999, 9999, timeout=0.2)
        result = scanner.scan_port(9999)
        if result is None:
            print(f"  ✓ Correctly identified port 9999 as closed")
        else:
            print(f"  ✗ Port 9999 should be closed but was detected as open")
        
        # Test scanning the open port
        print(f"\n  Testing scan on open port {test_port}...")
        scanner = PortScanner('127.0.0.1', test_port, test_port, timeout=0.5)
        result = scanner.scan_port(test_port)
        if result and result[0] == test_port:
            print(f"  ✓ Correctly identified port {test_port} as OPEN")
        else:
            print(f"  ✗ Port {test_port} should be open but was not detected")
        
        # Test range scanning
        print(f"\n  Testing range scan (ports {test_port-5} to {test_port+5})...")
        scanner = PortScanner('127.0.0.1', test_port-5, test_port+5, timeout=0.3)
        open_ports = scanner.scan()
        
        if any(port == test_port for port, _ in open_ports):
            print(f"  ✓ Range scan found the open port {test_port}")
            print(f"  Found {len(open_ports)} open port(s): {[p for p, _ in open_ports]}")
        else:
            print(f"  ✗ Range scan failed to find port {test_port}")
        
    except Exception as e:
        print(f"  ✗ Error during test: {e}")
    finally:
        if server_socket:
            server_socket.close()
            print(f"\n  Closed test server")
    
    print("\n4. Testing common services dictionary...")
    print(f"  Total known services: {len(COMMON_SERVICES)}")
    print(f"  Sample services:")
    for port in [22, 80, 443, 3306, 8080]:
        service = COMMON_SERVICES.get(port, "Unknown")
        print(f"    Port {port:5d}: {service}")
    
    print("\n" + "=" * 60)
    print("Core functionality tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_port_scanner()
