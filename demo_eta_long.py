#!/usr/bin/env python3
"""
Extended demo for ETC (Estimated Time to Completion) feature with longer scan times
"""

import socket
import threading
import time
import os
import sys

def demo_long_scan():
    """Demo with a longer port range to show ETC in action"""
    print("=" * 70)
    print("IP Port Scanner - Extended ETC Demo (Longer Scan)")
    print("=" * 70)
    print("\nThis demo scans a larger port range to show ETC calculations.")
    print()
    
    # Load scanner code
    scanner_file = os.path.join(os.path.dirname(__file__), 'port_scanner.py')
    with open(scanner_file, 'r') as f:
        lines = f.readlines()
    
    scanner_code = []
    for line in lines:
        if 'import tkinter' in line or 'from tkinter' in line:
            continue
        if 'class PortScannerGUI:' in line:
            break
        scanner_code.append(line)
    
    exec(''.join(scanner_code), globals())
    
    # Set up progress tracking
    start_time = None
    last_print_time = 0
    
    def progress_callback(scanned, total):
        nonlocal start_time, last_print_time
        
        if start_time is None:
            start_time = time.time()
        
        current_time = time.time()
        
        # Print updates every 1 second
        if current_time - last_print_time >= 1.0 or scanned == total:
            elapsed = current_time - start_time
            progress_percent = (scanned / total) * 100
            
            # Calculate ETA
            if scanned > 0:
                avg_time_per_port = elapsed / scanned
                remaining_ports = total - scanned
                eta_seconds = avg_time_per_port * remaining_ports
                
                # Format ETC
                if eta_seconds < 60:
                    eta_str = f"{int(eta_seconds)}s"
                elif eta_seconds < 3600:
                    minutes = int(eta_seconds / 60)
                    seconds = int(eta_seconds % 60)
                    eta_str = f"{minutes}m {seconds}s"
                else:
                    hours = int(eta_seconds / 3600)
                    minutes = int((eta_seconds % 3600) / 60)
                    eta_str = f"{hours}h {minutes}m"
                
                print(f"  Progress: {scanned:4d}/{total} ({progress_percent:5.1f}%) | "
                      f"Elapsed: {elapsed:5.1f}s | ETC: {eta_str:>8s}")
            
            last_print_time = current_time
    
    # Scan a larger port range
    start_port = 1
    end_port = 500  # Scan 500 ports to show ETA
    print(f"Scanning ports {start_port}-{end_port} on localhost...")
    print(f"Total ports to scan: {end_port - start_port + 1}")
    print()
    
    overall_start = time.time()
    scanner = PortScanner('127.0.0.1', start_port, end_port, timeout=0.2)
    results = scanner.scan(
        num_threads=50,  # Reduce threads to make scan take longer
        progress_callback=progress_callback
    )
    overall_elapsed = time.time() - overall_start
    
    print()
    print("=" * 70)
    print("Scan Complete!")
    print("=" * 70)
    print(f"Total time: {overall_elapsed:.2f} seconds")
    print(f"Total ports: {scanner.total_ports}")
    print(f"Ports scanned: {scanner.ports_scanned}")
    print(f"Open ports found: {len(results)}")
    print(f"Average time per port: {(overall_elapsed / scanner.total_ports):.4f}s")
    
    if results:
        print("\nOpen ports discovered:")
        for port, service in results[:10]:  # Show first 10
            print(f"  - Port {port:5d}: {service}")
        if len(results) > 10:
            print(f"  ... and {len(results) - 10} more")
    
    print("\n" + "=" * 70)
    print("Key Features Demonstrated:")
    print("  ✓ Real-time progress updates (ports scanned / total)")
    print("  ✓ Progress percentage calculation")
    print("  ✓ Elapsed time tracking")
    print("  ✓ ETC (Estimated Time to Completion) calculation")
    print("  ✓ Dynamic time formatting (seconds, minutes, hours)")
    print("=" * 70)

if __name__ == "__main__":
    demo_long_scan()
