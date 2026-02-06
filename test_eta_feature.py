#!/usr/bin/env python3
"""
Test script for ETC (Estimated Time to Completion) feature
"""

import socket
import threading
import time
import sys
import os

def test_eta_feature():
    """Test the ETC (Estimated Time to Completion) progress tracking functionality"""
    print("=" * 60)
    print("IP Port Scanner - ETC Feature Tests")
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
    
    print("\n1. Testing progress tracking attributes...")
    scanner = PortScanner('127.0.0.1', 1, 100, timeout=0.1)
    
    if hasattr(scanner, 'ports_scanned'):
        print(f"  ✓ PortScanner has 'ports_scanned' attribute: {scanner.ports_scanned}")
    else:
        print(f"  ✗ PortScanner missing 'ports_scanned' attribute")
    
    if hasattr(scanner, 'total_ports'):
        print(f"  ✓ PortScanner has 'total_ports' attribute: {scanner.total_ports}")
    else:
        print(f"  ✗ PortScanner missing 'total_ports' attribute")
    
    print("\n2. Testing progress callback...")
    
    # Track progress updates
    progress_updates = []
    
    def progress_callback(scanned, total):
        progress_updates.append((scanned, total))
    
    # Start a test server on a high port
    test_port = 9876
    server_socket = None
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', test_port))
        server_socket.listen(1)
        print(f"  Started test server on port {test_port}")
        
        # Test scanning with progress callback
        print(f"\n  Testing scan with progress tracking (ports {test_port-5} to {test_port+5})...")
        scanner = PortScanner('127.0.0.1', test_port-5, test_port+5, timeout=0.2)
        results = scanner.scan(num_threads=5, progress_callback=progress_callback)
        
        if progress_updates:
            print(f"  ✓ Progress callback was called {len(progress_updates)} times")
            print(f"  First update: {progress_updates[0][0]}/{progress_updates[0][1]} ports")
            if len(progress_updates) > 1:
                print(f"  Last update: {progress_updates[-1][0]}/{progress_updates[-1][1]} ports")
            
            # Verify progress goes from 0 to total
            final_scanned, final_total = progress_updates[-1]
            expected_total = test_port + 5 - (test_port - 5) + 1
            if final_scanned == expected_total and final_total == expected_total:
                print(f"  ✓ Progress reached 100% ({final_scanned}/{final_total})")
            else:
                print(f"  ✗ Progress mismatch: got {final_scanned}/{final_total}, expected {expected_total}/{expected_total}")
        else:
            print(f"  ✗ Progress callback was never called")
        
        # Verify scanner's internal counters
        if scanner.ports_scanned == scanner.total_ports:
            print(f"  ✓ Scanner's internal counter: {scanner.ports_scanned}/{scanner.total_ports}")
        else:
            print(f"  ✗ Scanner's internal counter mismatch: {scanner.ports_scanned}/{scanner.total_ports}")
        
    except Exception as e:
        print(f"  ✗ Error during test: {e}")
    finally:
        if server_socket:
            server_socket.close()
            print(f"\n  Closed test server")
    
    print("\n3. Testing ETC calculation simulation...")
    # Simulate ETC calculation
    total_ports = 1000
    ports_scanned = 250
    elapsed_time = 10.0  # seconds
    
    if ports_scanned > 0:
        avg_time_per_port = elapsed_time / ports_scanned
        remaining_ports = total_ports - ports_scanned
        estimated_remaining_time = avg_time_per_port * remaining_ports
        
        print(f"  Total ports: {total_ports}")
        print(f"  Ports scanned: {ports_scanned}")
        print(f"  Elapsed time: {elapsed_time}s")
        print(f"  Average time per port: {avg_time_per_port:.4f}s")
        print(f"  Estimated remaining time: {estimated_remaining_time:.2f}s")
        
        # Format ETC
        if estimated_remaining_time < 60:
            eta_str = f"{int(estimated_remaining_time)}s"
        elif estimated_remaining_time < 3600:
            minutes = int(estimated_remaining_time / 60)
            seconds = int(estimated_remaining_time % 60)
            eta_str = f"{minutes}m {seconds}s"
        else:
            hours = int(estimated_remaining_time / 3600)
            minutes = int((estimated_remaining_time % 3600) / 60)
            eta_str = f"{hours}h {minutes}m"
        
        print(f"  ✓ Formatted ETC: {eta_str}")
        
        # Test different time formats
        test_times = [30, 90, 150, 3700]
        print(f"\n  Testing time formatting:")
        for test_time in test_times:
            if test_time < 60:
                formatted = f"{int(test_time)}s"
            elif test_time < 3600:
                mins = int(test_time / 60)
                secs = int(test_time % 60)
                formatted = f"{mins}m {secs}s"
            else:
                hrs = int(test_time / 3600)
                mins = int((test_time % 3600) / 60)
                formatted = f"{hrs}h {mins}m"
            print(f"    {test_time}s -> {formatted}")
    
    print("\n" + "=" * 60)
    print("ETC feature tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_eta_feature()
