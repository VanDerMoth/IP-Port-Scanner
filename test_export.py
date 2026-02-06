#!/usr/bin/env python3
"""
Test script for export functionality
"""

import os
import sys
import json
import csv
import tempfile
import socket
import time
import threading
from queue import Queue
from datetime import datetime
import re

# Add script directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import only what we need from port_scanner without GUI
COMMON_SERVICES = {
    20: "FTP Data",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP Proxy",
    8443: "HTTPS Alt",
    27017: "MongoDB",
}


class PortScanner:
    """Core port scanning functionality"""
    
    def __init__(self, target_ip, start_port, end_port, timeout=1):
        self.target_ip = target_ip
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.open_ports = []
        self.queue = Queue()
        self.lock = threading.Lock()
        
    def scan_port(self, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target_ip, port))
            sock.close()
            
            if result == 0:
                service = COMMON_SERVICES.get(port, "Unknown Service")
                with self.lock:
                    self.open_ports.append((port, service))
                return port, service
        except socket.gaierror:
            return None
        except socket.error:
            return None
        return None
    
    def worker(self, callback=None):
        """Worker thread for scanning ports"""
        while not self.queue.empty():
            port = self.queue.get()
            result = self.scan_port(port)
            if result and callback:
                callback(result[0], result[1])
            self.queue.task_done()
    
    def scan(self, num_threads=100, callback=None):
        """Main scanning function with multi-threading"""
        self.open_ports = []
        
        # Fill the queue with ports to scan
        for port in range(self.start_port, self.end_port + 1):
            self.queue.put(port)
        
        # Start worker threads
        threads = []
        for _ in range(min(num_threads, self.queue.qsize())):
            thread = threading.Thread(target=self.worker, args=(callback,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        return sorted(self.open_ports, key=lambda x: x[0])
    
    def export_results(self, filename, file_format='json', scan_metadata=None):
        """
        Export scan results to a file
        
        Args:
            filename: Output file path
            file_format: Format to export ('json', 'csv', or 'txt')
            scan_metadata: Optional dictionary with scan metadata (timestamp, duration, etc.)
        """
        if file_format == 'json':
            self._export_json(filename, scan_metadata)
        elif file_format == 'csv':
            self._export_csv(filename, scan_metadata)
        elif file_format == 'txt':
            self._export_txt(filename, scan_metadata)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
    
    def _export_json(self, filename, scan_metadata):
        """Export results as JSON"""
        data = {
            'scan_info': {
                'target_ip': self.target_ip,
                'start_port': self.start_port,
                'end_port': self.end_port,
                'timeout': self.timeout,
                'total_open_ports': len(self.open_ports)
            },
            'results': [
                {'port': port, 'service': service}
                for port, service in self.open_ports
            ]
        }
        
        if scan_metadata:
            data['scan_info'].update(scan_metadata)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _export_csv(self, filename, scan_metadata):
        """Export results as CSV"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write metadata as comments
            if scan_metadata:
                writer.writerow(['# Scan Metadata'])
                for key, value in scan_metadata.items():
                    writer.writerow([f'# {key}', value])
            
            writer.writerow(['# Target IP', self.target_ip])
            writer.writerow(['# Port Range', f'{self.start_port}-{self.end_port}'])
            writer.writerow(['# Total Open Ports', len(self.open_ports)])
            writer.writerow([])  # Empty row
            
            # Write header and results
            writer.writerow(['Port', 'Service'])
            for port, service in self.open_ports:
                writer.writerow([port, service])
    
    def _export_txt(self, filename, scan_metadata):
        """Export results as plain text"""
        with open(filename, 'w') as f:
            f.write("IP Port Scanner - Scan Results\n")
            f.write("=" * 60 + "\n\n")
            
            if scan_metadata:
                f.write("Scan Metadata:\n")
                for key, value in scan_metadata.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
            
            f.write(f"Target IP: {self.target_ip}\n")
            f.write(f"Port Range: {self.start_port}-{self.end_port}\n")
            f.write(f"Total Open Ports: {len(self.open_ports)}\n\n")
            
            if self.open_ports:
                f.write("Open Ports:\n")
                f.write("-" * 60 + "\n")
                for port, service in self.open_ports:
                    f.write(f"Port {port:5d}: OPEN - {service}\n")
            else:
                f.write("No open ports found.\n")


def test_export_functionality():
    """Test the export functionality"""
    print("=" * 70)
    print("IP Port Scanner - Export Functionality Tests")
    print("=" * 70)
    
    # Start a test server
    test_ports = [9876, 9877]
    servers = []
    
    print("\n[*] Setting up test servers...")
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
    print(f"\n[*] Scanning localhost ports {test_ports[0]}-{test_ports[-1]+5}...")
    scanner = PortScanner('127.0.0.1', test_ports[0], test_ports[-1]+5, timeout=0.3)
    start_time = time.time()
    results = scanner.scan()
    scan_duration = time.time() - start_time
    
    print(f"    ✓ Scan completed in {scan_duration:.2f} seconds")
    print(f"    ✓ Found {len(results)} open port(s)")
    
    # Test export formats
    test_formats = ['json', 'csv', 'txt']
    
    for file_format in test_formats:
        print(f"\n[*] Testing {file_format.upper()} export...")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{file_format}', delete=False) as tmp:
            tmp_filename = tmp.name
        
        try:
            # Prepare scan metadata
            scan_metadata = {
                'timestamp': '2024-01-01 12:00:00',
                'scan_duration_seconds': round(scan_duration, 2)
            }
            
            # Export results
            scanner.export_results(tmp_filename, file_format, scan_metadata)
            print(f"    ✓ Export to {file_format} successful")
            
            # Verify file was created and has content
            if not os.path.exists(tmp_filename):
                print(f"    ✗ File was not created")
                continue
            
            file_size = os.path.getsize(tmp_filename)
            if file_size == 0:
                print(f"    ✗ File is empty")
                continue
            
            print(f"    ✓ File created with size {file_size} bytes")
            
            # Verify content based on format
            if file_format == 'json':
                with open(tmp_filename, 'r') as f:
                    data = json.load(f)
                    
                if 'scan_info' not in data or 'results' not in data:
                    print(f"    ✗ JSON structure is invalid")
                    continue
                
                if data['scan_info']['target_ip'] != '127.0.0.1':
                    print(f"    ✗ Target IP is incorrect")
                    continue
                
                if len(data['results']) != len(results):
                    print(f"    ✗ Number of results doesn't match")
                    continue
                
                print(f"    ✓ JSON structure is valid")
                print(f"    ✓ Contains {len(data['results'])} results")
                
            elif file_format == 'csv':
                with open(tmp_filename, 'r') as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                
                # Count data rows (excluding metadata and header)
                data_rows = [row for row in rows if row and not row[0].startswith('#') and row[0] != 'Port']
                
                if len(data_rows) != len(results):
                    print(f"    ✗ Number of results doesn't match: {len(data_rows)} vs {len(results)}")
                    continue
                
                print(f"    ✓ CSV format is valid")
                print(f"    ✓ Contains {len(data_rows)} results")
                
            elif file_format == 'txt':
                with open(tmp_filename, 'r') as f:
                    content = f.read()
                
                if '127.0.0.1' not in content:
                    print(f"    ✗ Target IP not found in content")
                    continue
                
                # Check that all ports are mentioned
                all_ports_found = all(str(port) in content for port, _ in results)
                if not all_ports_found:
                    print(f"    ✗ Not all ports found in content")
                    continue
                
                print(f"    ✓ Text format is valid")
                print(f"    ✓ Contains all {len(results)} results")
            
            # Show a preview of the file
            print(f"    Preview of {file_format} file:")
            with open(tmp_filename, 'r') as f:
                preview = f.read(200)
                print("    " + "-" * 60)
                for line in preview.split('\n')[:5]:
                    print(f"    {line}")
                if len(preview) >= 200:
                    print("    ...")
                print("    " + "-" * 60)
            
        except Exception as e:
            print(f"    ✗ Export failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup
            if os.path.exists(tmp_filename):
                os.remove(tmp_filename)
    
    # Test invalid format
    print(f"\n[*] Testing invalid format handling...")
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.invalid', delete=False) as tmp:
            tmp_filename = tmp.name
        
        scanner.export_results(tmp_filename, 'invalid', {})
        print(f"    ✗ Should have raised ValueError for invalid format")
    except ValueError as e:
        print(f"    ✓ Correctly raised ValueError: {e}")
    finally:
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)
    
    # Cleanup servers
    print("\n[*] Cleaning up test servers...")
    for sock in servers:
        sock.close()
    print("    ✓ Test servers closed")
    
    print("\n" + "=" * 70)
    print("Export functionality tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_export_functionality()
    except Exception as e:
        print(f"\n[!] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
