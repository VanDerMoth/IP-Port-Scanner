#!/usr/bin/env python3
"""
Demo script showing IP Port Scanner functionality without GUI
This demonstrates the scanner works in CLI mode for systems without display
"""

import sys
import os
import socket
import time

# Add the script directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import scanner components by reading only what's needed
import re
from queue import Queue
import threading

# Load scanner code dynamically to avoid GUI dependencies
scanner_file = os.path.join(script_dir, 'port_scanner.py')
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

# Execute to get COMMON_SERVICES and PortScanner
exec(''.join(scanner_code))


def print_banner():
    """Print application banner"""
    print("\n" + "="*70)
    print(" " * 18 + "IP PORT SCANNER - DEMO")
    print("="*70)
    print("\nThis demo shows the scanner detecting open ports on localhost")
    print("In the GUI version, this is done with a user-friendly interface\n")


def demo_scan():
    """Run a demonstration scan"""
    print_banner()
    
    # Setup test servers on some ports
    test_ports = [8001, 8002, 8003]
    servers = []
    
    print("[*] Setting up test servers...")
    for port in test_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('127.0.0.1', port))
            sock.listen(1)
            servers.append(sock)
            print(f"    ✓ Test server started on port {port}")
        except Exception as e:
            print(f"    ✗ Could not start server on port {port}: {e}")
    
    print(f"\n[*] Scanning localhost (127.0.0.1) ports 8000-8010...")
    print("[*] Please wait...\n")
    
    # Callback to show results in real-time
    def show_result(port, service):
        print(f"    ✓ FOUND: Port {port:5d} - {service}")
    
    # Perform the scan
    scanner = PortScanner('127.0.0.1', 8000, 8010, timeout=0.3)
    start_time = time.time()
    results = scanner.scan(num_threads=20, callback=show_result)
    scan_time = time.time() - start_time
    
    # Display summary
    print("\n" + "-"*70)
    print(f"[*] Scan completed in {scan_time:.2f} seconds")
    print(f"[*] Found {len(results)} open port(s)\n")
    
    if results:
        print("Summary of Open Ports:")
        print("-" * 70)
        for port, service in results:
            print(f"  Port {port:5d}: OPEN - {service}")
    else:
        print("No open ports found in the specified range.")
    
    # Cleanup
    print("\n[*] Cleaning up test servers...")
    for sock in servers:
        sock.close()
    
    print("\n" + "="*70)
    print("GUI APPLICATION FEATURES:")
    print("="*70)
    print("• User-friendly graphical interface with Tkinter")
    print("• Input fields for IP address and port range")
    print("• Real-time results display as ports are discovered")
    print("• Progress indicator during scanning")
    print("• Start/Stop/Clear buttons for easy control")
    print("• Validation of IP addresses and port ranges")
    print("• Service identification for common ports")
    print("• Multi-threaded for fast scanning")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        demo_scan()
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
