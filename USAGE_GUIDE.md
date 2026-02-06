# IP Port Scanner - GUI Layout and Usage Guide

## Application Window Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  IP Port Scanner                                          [_][□][X]│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Target IP Address:    [127.0.0.1________________________]      │
│                                                                  │
│  Start Port:          [1_________________________________]      │
│                                                                  │
│  End Port:            [1024______________________________]      │
│                                                                  │
│         [Start Scan]    [Stop Scan]    [Clear Results]          │
│                                                                  │
│  [████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░]            │
│                                                                  │
│  Scan Results:                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Port 22: OPEN - SSH                                      │   │
│  │ Port 80: OPEN - HTTP                                     │   │
│  │ Port 443: OPEN - HTTPS                                   │   │
│  │ Port 3306: OPEN - MySQL                                  │   │
│  │ Port 8080: OPEN - HTTP Proxy                             │   │
│  │                                                           │   │
│  │                                                           ▲   │
│  │                                                           █   │
│  │                                                           █   │
│  │                                                           ▼   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Ready to scan                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Step-by-Step Usage Guide

### 1. Launch the Application

#### On Linux with Python:
```bash
python3 port_scanner.py
```

#### On Linux with built executable:
```bash
./dist/ip-port-scanner
```

### 2. Enter Target Information

- **Target IP Address**: Enter the IP you want to scan
  - Examples: `127.0.0.1` (localhost), `192.168.1.1`, etc.
  - Must be a valid IPv4 address
  
- **Start Port**: First port in the range (1-65535)
  - Common ranges:
    - Well-known ports: 1-1024
    - Registered ports: 1025-49151
    - Dynamic ports: 49152-65535
  
- **End Port**: Last port in the range (1-65535)
  - Must be >= Start Port

### 3. Start the Scan

Click **"Start Scan"** button to begin scanning:
- Progress bar will animate during the scan
- Open ports will appear in real-time
- Each result shows: `Port [number]: OPEN - [Service Name]`

### 4. Control the Scan

- **Stop Scan**: Halts the current scan operation
- **Clear Results**: Clears the results display area
- **Start Scan**: Disabled during active scan

### 5. View Results

Results show:
- Port number
- Status (OPEN)
- Associated service (if known)

Example output:
```
Port 22: OPEN - SSH
Port 80: OPEN - HTTP
Port 443: OPEN - HTTPS
Port 3306: OPEN - MySQL
```

## Build Instructions

### Building the Linux Executable

1. Install dependencies:
```bash
make install
```

2. Build the executable:
```bash
make build
```

This creates a standalone Linux executable at: `dist/ip-port-scanner`

3. The executable can be:
   - Copied to `/usr/local/bin/` for system-wide access
   - Distributed to other Linux systems
   - Run without Python installed

### Makefile Commands

```bash
make help      # Show available commands
make install   # Install Python dependencies
make run       # Run the application with Python
make build     # Build standalone Linux executable
make clean     # Remove build artifacts
```

## Technical Features

### Port Scanning
- **Method**: TCP socket connections
- **Timeout**: Configurable (default: 0.5s per port)
- **Threading**: Multi-threaded (default: 100 threads)
- **Speed**: Fast scanning with concurrent connections

### Service Detection
Identifies common services on standard ports:
- Web servers (HTTP, HTTPS)
- Databases (MySQL, PostgreSQL, MongoDB, Redis)
- Remote access (SSH, RDP, VNC, Telnet)
- File transfer (FTP, SMB)
- Email (SMTP, POP3, IMAP)
- And more...

### Input Validation
- IP address format validation
- Port range validation (1-65535)
- Range logic validation (start <= end)
- Error messages for invalid input

### GUI Features
- Native Linux desktop appearance
- Responsive layout
- Real-time result updates
- Scrollable results area
- Visual progress indicator
- Status bar for feedback

## Security Notice

⚠️ **Important Legal Notice**

Only scan IP addresses and networks that:
- You own
- You have explicit written permission to scan
- Are in authorized penetration testing scenarios

Unauthorized port scanning may:
- Violate computer fraud laws
- Break terms of service
- Be considered hostile reconnaissance
- Result in legal consequences

Always scan responsibly and ethically.

## Requirements

### System Requirements
- Linux operating system
- Python 3.6 or higher
- Tkinter (python3-tk package)
- Network connectivity

### Python Dependencies
- PyInstaller (for building executables)
- Standard library modules:
  - tkinter (GUI)
  - socket (networking)
  - threading (concurrency)
  - queue (thread-safe queues)
  - re (input validation)

### Installation on Various Linux Distributions

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-tk python3-pip
pip3 install -r requirements.txt
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-tkinter python3-pip
pip3 install -r requirements.txt
```

**Arch Linux:**
```bash
sudo pacman -S python python-tk python-pip
pip3 install -r requirements.txt
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'tkinter'"
Install Tkinter:
```bash
sudo apt install python3-tk    # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

### "Permission denied" when scanning low ports
Some systems require elevated privileges for ports < 1024:
```bash
sudo python3 port_scanner.py
```

### Scan is slow
- Reduce port range
- Increase timeout value (less accurate)
- Check network connectivity
- Firewall may be blocking

### No ports found
- Check if target is reachable: `ping [target_ip]`
- Verify services are running on target
- Check firewall rules
- Try scanning localhost first: `127.0.0.1`

## Examples

### Example 1: Scan Localhost Common Ports
```
Target IP: 127.0.0.1
Start Port: 1
End Port: 1024
Result: Finds SSH (22), HTTP (80), etc.
```

### Example 2: Scan Web Server Ports
```
Target IP: 192.168.1.100
Start Port: 80
End Port: 8080
Result: Finds HTTP (80), HTTPS (443), proxies
```

### Example 3: Scan Database Ports
```
Target IP: 10.0.0.50
Start Port: 3306
End Port: 27017
Result: Finds MySQL (3306), PostgreSQL (5432), MongoDB (27017)
```

## License and Credits

This IP Port Scanner is an open-source tool developed with GitHub Copilot.
Feel free to use, modify, and distribute according to the project license.
