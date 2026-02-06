# IP Port Scanner

A Linux desktop application for scanning ports on a specified IP address to discover running services.

## Features

- 🖥️ **User-friendly GUI** - Built with Tkinter for a native Linux desktop experience
- 🔍 **Port Scanning** - Scan any IP address for open ports
- ⚡ **Multi-threaded** - Fast scanning with configurable number of threads (default: 200 threads)
- 🥷 **Stealth Mode** - Randomize port scan order and add delays to avoid detection
- 📊 **Service Detection** - Identifies common services running on open ports
- 🎯 **Flexible Range** - Specify custom port ranges (1-65535)
- 📝 **Real-time Results** - See open ports as they are discovered
- 💾 **Export Results** - Save scan results to JSON, CSV, or TXT files for future analysis
- 🚀 **Optimized Performance** - Reduced timeout (0.3s) for faster scans

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python)
- PyInstaller (for building standalone executables)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/VanDerMoth/IP-Port-Scanner.git
cd IP-Port-Scanner
```

2. Install dependencies:
```bash
make install
```

Or manually:
```bash
pip3 install -r requirements.txt
```

## Usage

### Running the Application

Run the application directly with Python:
```bash
make run
```

Or:
```bash
python3 port_scanner.py
```

### Building for Linux

Build a standalone executable for Linux:
```bash
make build
```

The executable will be created in the `dist/` directory and can be run on any Linux system:
```bash
./dist/ip-port-scanner
```

### Using the Scanner

1. **Enter Target IP**: Input the IP address you want to scan (e.g., 127.0.0.1 for localhost)
2. **Set Port Range**: Define the start and end ports (default: 1-1024)
3. **Configure Stealth Options** (optional):
   - Enable "Randomize port scan order" to scan ports in random order
   - Set "Scan delay" (in seconds) to add delays between port scans for stealth
   - A delay of 0.01-0.1 seconds provides good stealth without significantly impacting speed
4. **Start Scan**: Click "Start Scan" to begin scanning
5. **View Results**: Open ports and their associated services will appear in real-time
6. **Stop/Clear**: Use "Stop Scan" to halt scanning or "Clear Results" to reset
7. **Export Results**: Click "Export Results" to save scan results to a file (JSON, CSV, or TXT format)

## Common Ports Detected

The scanner identifies common services including:
- Port 22: SSH
- Port 80: HTTP
- Port 443: HTTPS
- Port 3306: MySQL
- Port 5432: PostgreSQL
- Port 8080: HTTP Proxy
- And many more...

## Stealth Scanning Features

The scanner includes stealth features to help avoid detection during scanning:

### Randomized Port Order
Enable "Randomize port scan order" to scan ports in a random sequence rather than sequentially. This makes the scan pattern less predictable and harder to detect by intrusion detection systems (IDS).

### Scan Delay
Set a delay (in seconds) between each port scan to slow down the scan rate:
- **0 seconds**: Maximum speed (no delay)
- **0.01-0.05 seconds**: Light stealth with minimal impact on speed
- **0.1-0.5 seconds**: Moderate stealth, significantly slower but harder to detect
- **1+ seconds**: High stealth, very slow but mimics normal network traffic

**Note**: Combining randomized order with scan delays provides the best stealth characteristics.

## Performance Improvements

Recent optimizations have significantly improved scanning speed:

- **Increased Thread Count**: Default thread count increased from 100 to 200 for faster parallel scanning
- **Reduced Timeout**: Socket timeout reduced from 1.0s to 0.3s for quicker closed port detection
- **Optimized Algorithm**: Improved port queuing and scanning logic for better performance

**Performance comparison** (scanning 1000 ports on localhost):
- Old version: ~3-5 seconds
- New version: ~1-2 seconds (2-3x faster)

## Exporting Scan Results

The scanner allows you to export scan results in multiple formats for further analysis or integration with other tools:

### Export Formats

1. **JSON** - Structured data format ideal for programmatic processing
   - Contains scan metadata (timestamp, duration, target IP, port range)
   - Results array with port numbers and service names
   - Easy to parse with any programming language

2. **CSV** - Spreadsheet-compatible format
   - Includes metadata as comment rows
   - Port and service columns for easy import into Excel/Sheets
   - Suitable for data analysis and reporting

3. **TXT** - Human-readable plain text format
   - Clean, formatted output for documentation
   - Includes all scan information and results
   - Easy to read and share

### How to Export

1. Complete a port scan
2. Click the "Export Results" button
3. Select your desired format (JSON, CSV, or TXT)
4. Choose a location and filename
5. Results are saved with scan metadata including timestamp and duration

### Example Export Formats

**JSON Format:**
```json
{
  "scan_info": {
    "target_ip": "127.0.0.1",
    "start_port": 1,
    "end_port": 1024,
    "timeout": 0.5,
    "total_open_ports": 3,
    "timestamp": "2024-01-15 10:30:45",
    "scan_duration_seconds": 2.34
  },
  "results": [
    {"port": 22, "service": "SSH"},
    {"port": 80, "service": "HTTP"},
    {"port": 443, "service": "HTTPS"}
  ]
}
```

**CSV Format:**
```csv
# timestamp,2024-01-15 10:30:45
# scan_duration_seconds,2.34
# Target IP,127.0.0.1
# Port Range,1-1024
# Total Open Ports,3

Port,Service
22,SSH
80,HTTP
443,HTTPS
```

**TXT Format:**
```
IP Port Scanner - Scan Results
============================================================

Scan Metadata:
  timestamp: 2024-01-15 10:30:45
  scan_duration_seconds: 2.34

Target IP: 127.0.0.1
Port Range: 1-1024
Total Open Ports: 3

Open Ports:
------------------------------------------------------------
Port    22: OPEN - SSH
Port    80: OPEN - HTTP
Port   443: OPEN - HTTPS
```

## Makefile Commands

- `make help` - Display available commands
- `make install` - Install dependencies
- `make run` - Run the application
- `make build` - Build Linux executable
- `make clean` - Clean build artifacts

## Security Notice

⚠️ **Important**: Only scan IP addresses and networks you own or have explicit permission to scan. Unauthorized port scanning may be illegal in your jurisdiction.

## Technical Details

- **Language**: Python 3
- **GUI Framework**: Tkinter
- **Scanning Method**: TCP socket connections
- **Threading**: Multi-threaded for performance
- **Build Tool**: PyInstaller

## License

This project is open source and available for use and modification.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
