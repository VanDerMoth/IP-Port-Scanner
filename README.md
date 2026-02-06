# IP Port Scanner

A Linux desktop application for scanning ports on a specified IP address to discover running services.

## Features

- 🖥️ **User-friendly GUI** - Built with Tkinter for a native Linux desktop experience
- 🔍 **Port Scanning** - Scan any IP address for open ports
- ⚡ **Multi-threaded** - Fast scanning with configurable number of threads
- 📊 **Service Detection** - Identifies common services running on open ports
- 🎯 **Flexible Range** - Specify custom port ranges (1-65535)
- 📝 **Real-time Results** - See open ports as they are discovered

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
3. **Start Scan**: Click "Start Scan" to begin scanning
4. **View Results**: Open ports and their associated services will appear in real-time
5. **Stop/Clear**: Use "Stop Scan" to halt scanning or "Clear Results" to reset

## Common Ports Detected

The scanner identifies common services including:
- Port 22: SSH
- Port 80: HTTP
- Port 443: HTTPS
- Port 3306: MySQL
- Port 5432: PostgreSQL
- Port 8080: HTTP Proxy
- And many more...

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
