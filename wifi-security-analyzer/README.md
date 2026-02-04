# Wi-Fi Security Analyzer

A cybersecurity tool for analyzing nearby Wi-Fi networks, displaying security information, encryption types, and signal strength. Built for educational purposes to help understand Wi-Fi security.

## ⚠️ Ethical Use Notice

**This tool is for educational purposes only.** Only scan networks that you own or have explicit written permission to analyze. Unauthorized network scanning may violate local laws and regulations. Use responsibly and ethically.

## Features

- 🔍 Scan for nearby Wi-Fi networks
- 🔒 Display encryption types (WPA3, WPA2, WPA, WEP, Open)
- 📶 Show signal strength with visual indicators
- 📊 Display network details (BSSID, Channel, Frequency)
- 🎨 Modern, responsive web interface
- 🖥️ Cross-platform support (Windows, Linux, macOS)

## Prerequisites

- Python 3.7 or higher
- Wi-Fi adapter enabled
- Administrator/root privileges (may be required on some systems)

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Backend Server

1. **Open a terminal/command prompt**

2. **Navigate to the project directory**

3. **Run the Python server:**
   ```bash
   python wifi_scanner.py
   ```

   You should see:
   ```
   ============================================================
   Wi-Fi Security Analyzer - Backend Server
   ============================================================
   
   ⚠️  EDUCATIONAL USE ONLY
   Only scan networks you own or have explicit permission to analyze.
   
   Server starting on http://localhost:5000
   Open wifi-analyzer.html in your browser to use the interface.
   
   ============================================================
   ```

### Using the Web Interface

1. **Open `wifi-analyzer.html` in your web browser**
   - You can double-click the file or open it directly
   - Or navigate to `http://localhost:5000` in your browser

2. **Click "Scan Networks"** to discover nearby Wi-Fi networks

3. **Review the results:**
   - Network names (SSID)
   - Security badges (WPA3, WPA2, WPA, WEP, Open)
   - Signal strength indicators
   - Channel and frequency information
   - BSSID (MAC address of access point)

## Platform-Specific Notes

### Windows
- Uses `netsh wlan show networks mode=Bssid`
- May require running as Administrator for best results
- Works with Windows 10/11

### Linux
- Uses `nmcli` (NetworkManager) or `iwlist` as fallback
- May require root privileges for scanning
- Tested on Ubuntu, Debian, and similar distributions

### macOS
- Uses the `airport` command
- May require enabling location services
- Tested on macOS 10.14+

## Security Ratings

- **🟢 WPA3** - Excellent: Latest security standard with enhanced protection
- **🔵 WPA2** - Good: Strong security, widely used and recommended
- **🟡 WPA** - Weak: Older standard, less secure than WPA2/WPA3
- **🔴 WEP / Open** - Poor: Very weak or no encryption - avoid using

## Troubleshooting

### No networks found
- Ensure Wi-Fi is enabled on your device
- Check that you have proper permissions (may need admin/root)
- Try running the server with elevated privileges

### Connection refused error
- Make sure the Python server is running on port 5000
- Check if another application is using port 5000
- Verify firewall settings aren't blocking the connection

### Permission errors (Linux/macOS)
- Try running with `sudo` (Linux) or check System Preferences (macOS)
- On Linux, you may need to add your user to the `netdev` group

## Project Structure

```
.
├── wifi-analyzer.html    # Frontend web interface
├── wifi_scanner.py       # Backend Python server
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Learning Resources

This project demonstrates:
- Network scanning techniques
- Wi-Fi security protocols
- Web API development (Flask)
- Frontend-backend communication
- Cross-platform system commands

## Future Enhancements

- Export scan results to CSV/JSON
- Historical tracking of network changes
- More detailed security analysis
- Network vulnerability assessment
- Signal strength mapping

## License

This project is provided for educational purposes. Use responsibly and in accordance with local laws and regulations.

## Contributing

Feel free to submit issues or pull requests to improve this educational tool.

---

**Remember: Always use cybersecurity tools ethically and legally. Only scan networks you own or have permission to analyze.**
