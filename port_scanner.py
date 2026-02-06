#!/usr/bin/env python3
"""
IP Port Scanner - A Linux desktop application for scanning ports on a specified IP address
"""

import socket
import threading
from queue import Queue
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re

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


class PortScannerGUI:
    """GUI Application for Port Scanner"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("IP Port Scanner")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.scanning = False
        self.scanner = None
        
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
            self.scanner = PortScanner(target_ip, start_port, end_port, timeout=0.5)
            results = self.scanner.scan(num_threads=100, callback=self.append_result)
            
            if self.scanning:
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


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
