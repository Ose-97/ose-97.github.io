# Quick Start Guide

## ✅ Setup Complete!

All dependencies have been installed. You're ready to use the Wi-Fi Security Analyzer.

## 🚀 Starting the Server

### Option 1: Using the Start Script (Easiest)
- **Windows**: Double-click `start.bat`
- **Linux/macOS**: Run `./start.sh` (make it executable first: `chmod +x start.sh`)

### Option 2: Manual Start
1. Open a terminal/command prompt
2. Navigate to this directory:
   ```bash
   cd wifi-security-analyzer
   ```
3. Run the server:
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

## 🌐 Using the Interface

1. **Open the web interface:**
   - Navigate to `http://localhost:5000` in your browser
   - OR open `wifi-analyzer.html` directly in your browser

2. **Click "Scan Networks"** to discover nearby Wi-Fi networks

3. **Review the results:**
   - See network names, security types, signal strength
   - Check encryption types (WPA3, WPA2, WPA, WEP, Open)
   - View channel and frequency information

## ⚠️ Important Notes

- **Administrator privileges** may be required on Windows for best results
- Make sure your **Wi-Fi is enabled** before scanning
- Only scan networks you **own or have permission** to analyze
- The server runs on **http://localhost:5000** (local only, not accessible from other devices)

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## 📝 Troubleshooting

**Server won't start?**
- Make sure port 5000 is not in use by another application
- Check that Python is installed: `python --version`

**No networks found?**
- Ensure Wi-Fi is enabled
- Try running with Administrator privileges (Windows)
- Check that you have proper network permissions

**Connection refused?**
- Make sure the server is running
- Check the server output for any error messages
- Verify you're accessing `http://localhost:5000`

---

Happy scanning! Remember: Educational use only! 🔒


