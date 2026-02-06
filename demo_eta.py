#!/usr/bin/env python3
"""
Demo script to test the ETA feature in the GUI
This script simulates scanning with a visual display of progress
"""

import socket
import threading
import time
import sys

# Create test servers on multiple ports for demonstration
def start_test_servers():
    """Start test servers on multiple ports"""
    servers = []
    test_ports = [9876, 9877, 9878]
    
    for port in test_ports:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('127.0.0.1', port))
            server.listen(1)
            servers.append(server)
            print(f"Test server started on port {port}")
        except Exception as e:
            print(f"Failed to start server on port {port}: {e}")
    
    return servers

def stop_test_servers(servers):
    """Stop all test servers"""
    for server in servers:
        try:
            server.close()
        except:
            pass

def demo_eta_feature():
    """Demonstrate the ETA feature"""
    print("=" * 60)
    print("IP Port Scanner - ETA Feature Demo")
    print("=" * 60)
    print("\nThis demo shows how the ETA feature works.")
    print("It will scan a range of ports and display progress updates.")
    print()
    
    # Import scanner by loading only the non-GUI parts
    import os
    scanner_file = os.path.join(os.path.dirname(__file__), 'port_scanner.py')
    with open(scanner_file, 'r') as f:
        lines = f.readlines()
    
    # Extract non-GUI code
    scanner_code = []
    for line in lines:
        if 'import tkinter' in line or 'from tkinter' in line:
            continue
        if 'class PortScannerGUI:' in line:
            break
        scanner_code.append(line)
    
    exec(''.join(scanner_code), globals())
    
    # Start test servers
    print("Starting test servers...")
    servers = start_test_servers()
    time.sleep(0.5)
    
    try:
        # Track progress
        last_update_time = None
        
        def result_callback(port, service):
            print(f"  Found OPEN port: {port} ({service})")
        
        def progress_callback(scanned, total):
            nonlocal last_update_time
            current_time = time.time()
            
            # Only print updates every 0.5 seconds to avoid spam
            if last_update_time is None or (current_time - last_update_time) >= 0.5:
                progress_percent = (scanned / total) * 100
                print(f"  Progress: {scanned}/{total} ({progress_percent:.1f}%)")
                last_update_time = current_time
        
        # Scan a port range
        start_port = 9870
        end_port = 9885
        print(f"\nScanning ports {start_port}-{end_port}...")
        print()
        
        start_time = time.time()
        scanner = PortScanner('127.0.0.1', start_port, end_port, timeout=0.3)
        results = scanner.scan(
            num_threads=10,
            callback=result_callback,
            progress_callback=progress_callback
        )
        elapsed = time.time() - start_time
        
        print(f"\n✓ Scan completed in {elapsed:.2f} seconds")
        print(f"  Total ports scanned: {scanner.total_ports}")
        print(f"  Ports scanned counter: {scanner.ports_scanned}")
        print(f"  Open ports found: {len(results)}")
        
        if results:
            print("\nOpen ports:")
            for port, service in results:
                print(f"  - Port {port}: {service}")
        
    finally:
        print("\nStopping test servers...")
        stop_test_servers(servers)
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("\nTo see the ETA feature in the GUI:")
    print("1. Run: python3 port_scanner.py")
    print("2. Set target IP: 127.0.0.1")
    print("3. Set port range (e.g., 1-10000 for longer scan)")
    print("4. Click 'Start Scan'")
    print("5. Watch the progress bar and ETA update in real-time!")
    print("=" * 60)

if __name__ == "__main__":
    demo_eta_feature()
