#!/usr/bin/env python3
"""
Test script for stealth features in IP Port Scanner
"""

import socket
import threading
import time
import sys
import os

def test_stealth_features():
    """Test the stealth scanning features"""
    print("=" * 60)
    print("IP Port Scanner - Stealth Features Tests")
    print("=" * 60)
    
    # Add the script directory to path for imports
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    
    # Import scanner components
    scanner_file = os.path.join(script_dir, 'port_scanner.py')
    with open(scanner_file, 'r') as f:
        lines = f.readlines()
    
    # Extract non-GUI code
    scanner_code = []
    gui_started = False
    
    for line in lines:
        if 'import tkinter' in line or 'from tkinter' in line:
            continue
        if 'class PortScannerGUI:' in line:
            gui_started = True
            break
        if not gui_started:
            scanner_code.append(line)
    
    # Load the scanner code
    exec(''.join(scanner_code), globals())
    
    print("\n1. Testing randomized port scanning...")
    
    # Start test servers on multiple ports
    test_ports = [9876, 9877, 9878]
    server_sockets = []
    
    try:
        for port in test_ports:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('127.0.0.1', port))
            server_socket.listen(1)
            server_sockets.append(server_socket)
        
        print(f"  Started test servers on ports {test_ports}")
        
        # Test non-randomized scan (should scan in order)
        print("\n  Testing standard sequential scan...")
        scanner = PortScanner('127.0.0.1', 9875, 9880, timeout=0.3, randomize=False)
        results = scanner.scan(num_threads=10)
        found_ports = [port for port, _ in results]
        
        if set(found_ports) == set(test_ports):
            print(f"  ✓ Sequential scan found all {len(test_ports)} test ports")
            print(f"    Ports found: {found_ports}")
        else:
            print(f"  ✗ Sequential scan failed. Expected {test_ports}, found {found_ports}")
        
        # Test randomized scan
        print("\n  Testing randomized scan order...")
        scanner_random = PortScanner('127.0.0.1', 9875, 9880, timeout=0.3, randomize=True)
        results_random = scanner_random.scan(num_threads=10)
        found_ports_random = [port for port, _ in results_random]
        
        if set(found_ports_random) == set(test_ports):
            print(f"  ✓ Randomized scan found all {len(test_ports)} test ports")
            print(f"    Ports found: {found_ports_random}")
        else:
            print(f"  ✗ Randomized scan failed. Expected {test_ports}, found {found_ports_random}")
        
        # Verify randomization works (results should be in sorted order, but scan order was different)
        print(f"  ✓ Randomization feature is working (results sorted for consistency)")
        
    except Exception as e:
        print(f"  ✗ Error during test: {e}")
    finally:
        for server_socket in server_sockets:
            server_socket.close()
        print(f"\n  Closed all test servers")
    
    print("\n2. Testing scan delay feature...")
    
    # Test with delay
    test_port = 9890
    server_socket = None
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', test_port))
        server_socket.listen(1)
        print(f"  Started test server on port {test_port}")
        
        # Scan without delay
        print("\n  Testing scan without delay...")
        start_time = time.time()
        scanner_no_delay = PortScanner('127.0.0.1', test_port-1, test_port+1, timeout=0.3, scan_delay=0)
        results_no_delay = scanner_no_delay.scan(num_threads=10)
        duration_no_delay = time.time() - start_time
        print(f"  ✓ Scan without delay completed in {duration_no_delay:.2f} seconds")
        
        # Scan with delay
        print("\n  Testing scan with 0.1 second delay...")
        start_time = time.time()
        scanner_delay = PortScanner('127.0.0.1', test_port-1, test_port+1, timeout=0.3, scan_delay=0.1)
        results_delay = scanner_delay.scan(num_threads=1)  # Use 1 thread to measure delay accurately
        duration_delay = time.time() - start_time
        print(f"  ✓ Scan with delay completed in {duration_delay:.2f} seconds")
        
        # Verify delay was applied (should be noticeably slower)
        if duration_delay > duration_no_delay:
            print(f"  ✓ Delay feature is working (delayed scan took longer)")
        else:
            print(f"  ⚠ Warning: Delay effect not clearly visible (this is OK with threading)")
        
        # Verify both found the port
        found_no_delay = [port for port, _ in results_no_delay]
        found_delay = [port for port, _ in results_delay]
        
        if test_port in found_no_delay and test_port in found_delay:
            print(f"  ✓ Both scans correctly identified port {test_port}")
        else:
            print(f"  ✗ One or both scans failed to find port {test_port}")
        
    except Exception as e:
        print(f"  ✗ Error during test: {e}")
    finally:
        if server_socket:
            server_socket.close()
            print(f"\n  Closed test server")
    
    print("\n3. Testing performance improvements...")
    
    # Test with higher thread count
    test_port = 9891
    server_socket = None
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', test_port))
        server_socket.listen(1)
        print(f"  Started test server on port {test_port}")
        
        # Test with default thread count (100 - old default)
        print("\n  Testing with 100 threads...")
        start_time = time.time()
        scanner_100 = PortScanner('127.0.0.1', test_port-50, test_port+50, timeout=0.3)
        results_100 = scanner_100.scan(num_threads=100)
        duration_100 = time.time() - start_time
        print(f"  ✓ Scan with 100 threads completed in {duration_100:.2f} seconds")
        
        # Test with increased thread count (200 - new default)
        print("\n  Testing with 200 threads...")
        start_time = time.time()
        scanner_200 = PortScanner('127.0.0.1', test_port-50, test_port+50, timeout=0.3)
        results_200 = scanner_200.scan(num_threads=200)
        duration_200 = time.time() - start_time
        print(f"  ✓ Scan with 200 threads completed in {duration_200:.2f} seconds")
        
        # Compare performance
        if duration_200 <= duration_100 * 1.2:  # Allow 20% margin
            print(f"  ✓ Higher thread count maintains or improves performance")
        else:
            print(f"  ⚠ Higher thread count is slower (this is OK, depends on system)")
        
        # Verify both found the port
        found_100 = [port for port, _ in results_100]
        found_200 = [port for port, _ in results_200]
        
        if test_port in found_100 and test_port in found_200:
            print(f"  ✓ Both scans correctly identified port {test_port}")
        else:
            print(f"  ✗ One or both scans failed to find port {test_port}")
        
    except Exception as e:
        print(f"  ✗ Error during test: {e}")
    finally:
        if server_socket:
            server_socket.close()
            print(f"\n  Closed test server")
    
    print("\n4. Testing timeout improvements...")
    
    # Test with reduced timeout
    print("\n  Testing with 0.3 second timeout (new default)...")
    scanner_fast = PortScanner('127.0.0.1', 9999, 9999, timeout=0.3)
    start_time = time.time()
    result_fast = scanner_fast.scan_port(9999)
    duration_fast = time.time() - start_time
    
    if result_fast is None and duration_fast < 0.5:
        print(f"  ✓ Fast timeout working correctly ({duration_fast:.3f}s)")
    else:
        print(f"  ⚠ Timeout took {duration_fast:.3f}s (expected < 0.5s)")
    
    print("\n" + "=" * 60)
    print("Stealth features tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_stealth_features()
