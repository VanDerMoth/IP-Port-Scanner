# Installation and Quick Start Guide

## System Requirements

- **Operating System**: Linux (Ubuntu, Debian, Fedora, Arch, or any other distribution)
- **Python**: Version 3.6 or higher
- **Display**: X11 or Wayland (for GUI)
- **Network**: For scanning remote hosts

## Installation Steps

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-tk python3-pip git
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-tkinter python3-pip git
```

**Arch Linux:**
```bash
sudo pacman -S python python-tk python-pip git
```

### 2. Clone the Repository

```bash
git clone https://github.com/VanDerMoth/IP-Port-Scanner.git
cd IP-Port-Scanner
```

### 3. Install Python Dependencies

```bash
make install
```

Or manually:
```bash
pip3 install -r requirements.txt
```

## Running the Application

### Option 1: Run with Python (Recommended for Development)

```bash
make run
```

Or directly:
```bash
python3 port_scanner.py
```

### Option 2: Build and Run Standalone Executable

Build the executable:
```bash
make build
```

Run the executable:
```bash
./dist/ip-port-scanner
```

The standalone executable can be:
- Copied to `/usr/local/bin/` for system-wide access
- Distributed to other Linux systems (with same architecture)
- Run without Python installed on the target system

## Quick Usage Example

1. **Launch the application**
2. **Enter target IP**: `127.0.0.1` (for testing localhost)
3. **Set port range**: Start: `1`, End: `1024`
4. **Click "Start Scan"**
5. **View results** as they appear in real-time

## Testing Without GUI

If you want to test the scanner without the GUI (e.g., on a headless server):

```bash
python3 demo_scanner.py
```

This will run a demonstration scan showing the core functionality.

## Running Tests

To verify the installation and core functionality:

```bash
python3 test_scanner.py
```

Expected output: All tests should pass with ✓ marks.

## Troubleshooting

### "ModuleNotFoundError: No module named 'tkinter'"

Install Tkinter:
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### "Permission denied" when scanning

For ports < 1024, you may need elevated privileges:
```bash
sudo python3 port_scanner.py
```

### Scan finds no ports

- Verify target is reachable: `ping [target_ip]`
- Check firewall settings
- Try scanning localhost first: `127.0.0.1`
- Ensure services are actually running on the target

## Making the Executable System-Wide

After building the executable:

```bash
sudo cp dist/ip-port-scanner /usr/local/bin/
sudo chmod +x /usr/local/bin/ip-port-scanner
```

Then you can run it from anywhere:
```bash
ip-port-scanner
```

## Uninstallation

To remove the application:

```bash
# Remove the repository
cd ..
rm -rf IP-Port-Scanner

# Remove the system-wide executable (if installed)
sudo rm /usr/local/bin/ip-port-scanner
```

## Security Best Practices

⚠️ **Important**: Only scan networks and systems you own or have explicit permission to scan.

- Never scan production systems without approval
- Be aware of your organization's security policies
- Some ISPs may flag port scanning activity
- Consider using rate limiting for large scans
- Always document your scanning activities

## Getting Help

For detailed usage instructions, see:
- `README.md` - Overview and features
- `USAGE_GUIDE.md` - Comprehensive usage guide

For issues or questions:
- Check the troubleshooting section above
- Review the project's GitHub issues
- Consult the documentation files

## Next Steps

After installation:
1. Test with localhost (`127.0.0.1`) to familiarize yourself with the interface
2. Scan your own network devices (with permission)
3. Explore different port ranges to find various services
4. Review the scan results and service identifications

Enjoy using the IP Port Scanner! 🎉
