#!/usr/bin/env python3
"""
IP Port Scanner - A Linux desktop application for scanning ports on a specified IP address
"""

import socket
import threading
from queue import Queue
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import re
import json
import csv
from datetime import datetime

# Common ports and their associated services
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


class PortScannerGUI:
    """GUI Application for Port Scanner"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("IP Port Scanner")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.scanning = False
        self.scanner = None
        self.scan_start_time = None
        self.scan_duration = None
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # IP Address input
        ttk.Label(main_frame, text="Target IP Address:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ip_entry = ttk.Entry(main_frame, width=30)
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.ip_entry.insert(0, "127.0.0.1")
        
        # Start Port input
        ttk.Label(main_frame, text="Start Port:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.start_port_entry = ttk.Entry(main_frame, width=30)
        self.start_port_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.start_port_entry.insert(0, "1")
        
        # End Port input
        ttk.Label(main_frame, text="End Port:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.end_port_entry = ttk.Entry(main_frame, width=30)
        self.end_port_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.end_port_entry.insert(0, "1024")
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.scan_button = ttk.Button(button_frame, text="Start Scan", command=self.start_scan)
        self.scan_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop Scan", command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear Results", command=self.clear_results)
        self.clear_button.grid(row=0, column=2, padx=5)
        
        self.export_button = ttk.Button(button_frame, text="Export Results", command=self.export_results)
        self.export_button.grid(row=0, column=3, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Results area
        ttk.Label(main_frame, text="Scan Results:").grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.results_text = scrolledtext.ScrolledText(main_frame, width=80, height=20, wrap=tk.WORD)
        self.results_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready to scan", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
    def validate_ip(self, ip):
        """Validate IP address format"""
        pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
        if pattern.match(ip):
            parts = ip.split('.')
            return all(0 <= int(part) <= 255 for part in parts)
        return False
    
    def validate_port(self, port):
        """Validate port number"""
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except ValueError:
            return False
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
    
    def append_result(self, port, service):
        """Append scan result to results text"""
        self.results_text.insert(tk.END, f"Port {port}: OPEN - {service}\n")
        self.results_text.see(tk.END)
    
    def clear_results(self):
        """Clear results text area"""
        self.results_text.delete(1.0, tk.END)
        self.update_status("Results cleared")
    
    def start_scan(self):
        """Start the port scanning process"""
        # Validate inputs
        target_ip = self.ip_entry.get().strip()
        if not self.validate_ip(target_ip):
            messagebox.showerror("Invalid IP", "Please enter a valid IP address")
            return
        
        start_port = self.start_port_entry.get().strip()
        if not self.validate_port(start_port):
            messagebox.showerror("Invalid Port", "Start port must be between 1 and 65535")
            return
        
        end_port = self.end_port_entry.get().strip()
        if not self.validate_port(end_port):
            messagebox.showerror("Invalid Port", "End port must be between 1 and 65535")
            return
        
        start_port = int(start_port)
        end_port = int(end_port)
        
        if start_port > end_port:
            messagebox.showerror("Invalid Range", "Start port must be less than or equal to end port")
            return
        
        # Disable scan button and enable stop button
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.scanning = True
        
        # Clear previous results
        self.clear_results()
        
        # Update status and start progress bar
        self.update_status(f"Scanning {target_ip} ports {start_port}-{end_port}...")
        self.progress.start()
        
        # Run scan in separate thread
        scan_thread = threading.Thread(target=self.run_scan, args=(target_ip, start_port, end_port))
        scan_thread.daemon = True
        scan_thread.start()
    
    def run_scan(self, target_ip, start_port, end_port):
        """Run the actual scan"""
        try:
            self.scan_start_time = datetime.now()
            self.scanner = PortScanner(target_ip, start_port, end_port, timeout=0.5)
            results = self.scanner.scan(num_threads=100, callback=self.append_result)
            
            if self.scanning:
                self.scan_duration = (datetime.now() - self.scan_start_time).total_seconds()
                self.root.after(0, self.scan_complete, len(results))
        except Exception as e:
            self.root.after(0, self.scan_error, str(e))
    
    def scan_complete(self, num_open_ports):
        """Handle scan completion"""
        self.progress.stop()
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.scanning = False
        
        if num_open_ports > 0:
            self.update_status(f"Scan complete - Found {num_open_ports} open port(s)")
        else:
            self.update_status("Scan complete - No open ports found")
            self.results_text.insert(tk.END, "No open ports found in the specified range.\n")
    
    def scan_error(self, error_msg):
        """Handle scan errors"""
        self.progress.stop()
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.scanning = False
        self.update_status("Scan failed")
        messagebox.showerror("Scan Error", f"An error occurred: {error_msg}")
    
    def stop_scan(self):
        """Stop the scanning process"""
        self.scanning = False
        self.progress.stop()
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("Scan stopped by user")
    
    def export_results(self):
        """Export scan results to a file"""
        if not self.scanner or not self.scanner.open_ports:
            messagebox.showwarning("No Results", "No scan results to export. Please run a scan first.")
            return
        
        # Ask user for file format
        format_window = tk.Toplevel(self.root)
        format_window.title("Select Export Format")
        format_window.geometry("300x150")
        format_window.resizable(False, False)
        
        ttk.Label(format_window, text="Choose export format:", font=('', 10, 'bold')).pack(pady=10)
        
        format_var = tk.StringVar(value='json')
        
        ttk.Radiobutton(format_window, text="JSON (.json)", variable=format_var, value='json').pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(format_window, text="CSV (.csv)", variable=format_var, value='csv').pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(format_window, text="Text (.txt)", variable=format_var, value='txt').pack(anchor=tk.W, padx=20)
        
        def do_export():
            file_format = format_var.get()
            format_window.destroy()
            
            # File extensions based on format
            extensions = {
                'json': [('JSON files', '*.json'), ('All files', '*.*')],
                'csv': [('CSV files', '*.csv'), ('All files', '*.*')],
                'txt': [('Text files', '*.txt'), ('All files', '*.*')]
            }
            
            # Ask user for file location
            filename = filedialog.asksaveasfilename(
                title="Export Scan Results",
                defaultextension=f".{file_format}",
                filetypes=extensions.get(file_format, [('All files', '*.*')])
            )
            
            if filename:
                try:
                    # Prepare scan metadata
                    scan_metadata = {
                        'timestamp': self.scan_start_time.strftime('%Y-%m-%d %H:%M:%S') if self.scan_start_time else 'Unknown',
                        'scan_duration_seconds': round(self.scan_duration, 2) if self.scan_duration else 'Unknown'
                    }
                    
                    # Export the results
                    self.scanner.export_results(filename, file_format, scan_metadata)
                    
                    messagebox.showinfo("Export Successful", f"Results exported successfully to:\n{filename}")
                    self.update_status(f"Results exported to {filename}")
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export results:\n{str(e)}")
        
        ttk.Button(format_window, text="Export", command=do_export).pack(pady=10)
        
        # Center the window
        format_window.transient(self.root)
        format_window.grab_set()
        format_window.update_idletasks()
        x = (format_window.winfo_screenwidth() // 2) - (format_window.winfo_width() // 2)
        y = (format_window.winfo_screenheight() // 2) - (format_window.winfo_height() // 2)
        format_window.geometry(f"+{x}+{y}")


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
