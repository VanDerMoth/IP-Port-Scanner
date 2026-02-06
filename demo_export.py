#!/usr/bin/env python3
"""
Manual test demonstration for export functionality
This script simulates scanning and exporting results to show the feature works
"""

import os
import sys
import json
import csv
import socket
import time

# Add script directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import test module which has PortScanner class
from test_export import PortScanner

def demonstrate_export_feature():
    """Demonstrate the export feature with a real scan"""
    print("=" * 70)
    print("IP Port Scanner - Export Feature Demonstration")
    print("=" * 70)
    
    # Start test servers
    test_ports = [9876, 9877, 9878]
    servers = []
    
    print("\n[*] Setting up test servers for demonstration...")
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
    
    # Perform a scan
    print(f"\n[*] Scanning localhost (127.0.0.1) ports {test_ports[0]}-{test_ports[-1]+10}...")
    print("[*] Please wait...\n")
    
    scanner = PortScanner('127.0.0.1', test_ports[0], test_ports[-1]+10, timeout=0.3)
    start_time = time.time()
    results = scanner.scan()
    scan_duration = time.time() - start_time
    
    print(f"[*] Scan completed in {scan_duration:.2f} seconds")
    print(f"[*] Found {len(results)} open port(s)\n")
    
    if results:
        print("Open ports discovered:")
        for port, service in results:
            print(f"  Port {port:5d}: OPEN - {service}")
    
    # Prepare scan metadata
    scan_metadata = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'scan_duration_seconds': round(scan_duration, 2)
    }
    
    # Export to all formats
    print("\n" + "-" * 70)
    print("EXPORTING RESULTS TO DIFFERENT FORMATS")
    print("-" * 70)
    
    export_dir = '/tmp/scan_exports'
    os.makedirs(export_dir, exist_ok=True)
    
    formats = {
        'json': 'scan_results.json',
        'csv': 'scan_results.csv',
        'txt': 'scan_results.txt'
    }
    
    for file_format, filename in formats.items():
        filepath = os.path.join(export_dir, filename)
        
        print(f"\n[*] Exporting to {file_format.upper()} format...")
        print(f"    Destination: {filepath}")
        
        try:
            scanner.export_results(filepath, file_format, scan_metadata)
            file_size = os.path.getsize(filepath)
            print(f"    ✓ Export successful ({file_size} bytes)")
            
            # Show file contents
            print(f"\n    Content preview:")
            print("    " + "=" * 60)
            with open(filepath, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                for i, line in enumerate(lines[:15]):  # Show first 15 lines
                    print(f"    {line}")
                if len(lines) > 15:
                    print(f"    ... ({len(lines) - 15} more lines)")
            print("    " + "=" * 60)
            
        except Exception as e:
            print(f"    ✗ Export failed: {e}")
    
    # Show export directory contents
    print(f"\n[*] All exported files in {export_dir}:")
    for filename in os.listdir(export_dir):
        filepath = os.path.join(export_dir, filename)
        file_size = os.path.getsize(filepath)
        print(f"    - {filename} ({file_size} bytes)")
    
    # Cleanup servers
    print("\n[*] Cleaning up test servers...")
    for sock in servers:
        sock.close()
    print("    ✓ Test servers closed")
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE!")
    print("=" * 70)
    print(f"\nExported files are available at: {export_dir}")
    print("\nThese files can be:")
    print("  • Used with other security tools")
    print("  • Imported into spreadsheets for analysis")
    print("  • Processed with scripts for automation")
    print("  • Archived for historical comparison")
    print("  • Shared in documentation and reports")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        demonstrate_export_feature()
    except KeyboardInterrupt:
        print("\n\n[!] Demonstration interrupted by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
