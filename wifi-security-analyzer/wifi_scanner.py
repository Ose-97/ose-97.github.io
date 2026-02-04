#!/usr/bin/env python3
"""
Wi-Fi Security Analyzer - Backend Server
Scans for nearby Wi-Fi networks and provides security information.

Educational purposes only. Only scan networks you own or have permission to analyze.
"""

import json
import subprocess
import platform
import re
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for the frontend

def scan_wifi_windows():
    """Scan Wi-Fi networks on Windows using netsh command."""
    networks = []
    
    try:
        # Run netsh command to get Wi-Fi profiles and available networks
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return networks
        
        output = result.stdout
        current_network = {}
        
        for line in output.split('\n'):
            line = line.strip()
            
            # SSID
            if line.startswith('SSID'):
                if current_network:
                    networks.append(current_network)
                current_network = {}
                ssid_match = re.search(r'SSID \d+ : (.+)', line)
                if ssid_match:
                    current_network['ssid'] = ssid_match.group(1)
            
            # Network type
            elif 'Network type' in line:
                current_network['type'] = line.split(':')[1].strip() if ':' in line else 'Infrastructure'
            
            # Authentication
            elif 'Authentication' in line:
                auth = line.split(':')[1].strip() if ':' in line else 'Unknown'
                current_network['authentication'] = auth
            
            # Encryption
            elif 'Encryption' in line:
                encryption = line.split(':')[1].strip() if ':' in line else 'None'
                current_network['encryption'] = encryption
            
            # BSSID
            elif 'BSSID' in line and ':' in line:
                bssid = line.split(':')[1].strip()
                if bssid and bssid != 'N/A':
                    current_network['bssid'] = bssid
            
            # Signal
            elif 'Signal' in line and '%' in line:
                signal_match = re.search(r'(\d+)%', line)
                if signal_match:
                    current_network['signal'] = signal_match.group(1)
            
            # Radio type
            elif 'Radio type' in line:
                radio = line.split(':')[1].strip() if ':' in line else '802.11'
                if '802.11' in radio:
                    if 'n' in radio.lower():
                        current_network['frequency'] = '2.4/5 GHz'
                    elif 'ac' in radio.lower() or 'ax' in radio.lower():
                        current_network['frequency'] = '5 GHz'
                    else:
                        current_network['frequency'] = '2.4 GHz'
            
            # Channel
            elif 'Channel' in line:
                channel_match = re.search(r'(\d+)', line)
                if channel_match:
                    current_network['channel'] = channel_match.group(1)
        
        if current_network:
            networks.append(current_network)
        
        # Remove duplicates based on SSID and BSSID
        seen = set()
        unique_networks = []
        for net in networks:
            key = (net.get('ssid', ''), net.get('bssid', ''))
            if key not in seen and key[0]:  # Only add if SSID exists
                seen.add(key)
                unique_networks.append(net)
        
        return unique_networks
        
    except subprocess.TimeoutExpired:
        return []
    except Exception as e:
        print(f"Error scanning Wi-Fi: {e}")
        return []

def scan_wifi_linux():
    """Scan Wi-Fi networks on Linux using nmcli or iwlist."""
    networks = []
    
    try:
        # Try nmcli first (NetworkManager)
        result = subprocess.run(
            ['nmcli', '-t', '-f', 'SSID,SIGNAL,SECURITY,FREQ,BSSID', 'device', 'wifi', 'list'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split(':')
                if len(parts) >= 5:
                    network = {
                        'ssid': parts[0] if parts[0] else 'Hidden Network',
                        'signal': parts[1] if len(parts) > 1 else '0',
                        'encryption': parts[2] if len(parts) > 2 else 'Unknown',
                        'frequency': parts[3] if len(parts) > 3 else 'N/A',
                        'bssid': parts[4] if len(parts) > 4 else 'N/A'
                    }
                    networks.append(network)
            return networks
        
        # Fallback to iwlist (older systems)
        result = subprocess.run(
            ['iwlist', 'scan'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Parse iwlist output (simplified)
            current_network = {}
            for line in result.stdout.split('\n'):
                if 'ESSID:' in line:
                    if current_network:
                        networks.append(current_network)
                    current_network = {}
                    essid = line.split('ESSID:')[1].strip().strip('"')
                    current_network['ssid'] = essid if essid else 'Hidden Network'
                elif 'Encryption key:' in line:
                    if 'on' in line.lower():
                        current_network['encryption'] = 'WPA/WPA2'
                    else:
                        current_network['encryption'] = 'Open'
                elif 'Signal level=' in line:
                    signal_match = re.search(r'Signal level=(-?\d+)', line)
                    if signal_match:
                        # Convert dBm to percentage (rough approximation)
                        dbm = int(signal_match.group(1))
                        signal_pct = max(0, min(100, int((dbm + 100) * 2)))
                        current_network['signal'] = str(signal_pct)
            
            if current_network:
                networks.append(current_network)
        
        return networks
        
    except subprocess.TimeoutExpired:
        return []
    except Exception as e:
        print(f"Error scanning Wi-Fi: {e}")
        return []

def scan_wifi_macos():
    """Scan Wi-Fi networks on macOS using airport command."""
    networks = []
    
    try:
        # Try to find airport command
        airport_paths = [
            '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport',
            '/usr/local/bin/airport'
        ]
        
        airport_cmd = None
        for path in airport_paths:
            if os.path.exists(path):
                airport_cmd = path
                break
        
        if not airport_cmd:
            return networks
        
        result = subprocess.run(
            [airport_cmd, '-s'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return networks
        
        # Parse airport output
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        for line in lines:
            if not line.strip():
                continue
            
            parts = line.split()
            if len(parts) >= 6:
                network = {
                    'ssid': parts[0],
                    'bssid': parts[1],
                    'signal': parts[2].replace('dBm', '').strip(),
                    'channel': parts[3],
                    'encryption': ' '.join(parts[5:]) if len(parts) > 5 else 'Unknown'
                }
                networks.append(network)
        
        return networks
        
    except subprocess.TimeoutExpired:
        return []
    except Exception as e:
        print(f"Error scanning Wi-Fi: {e}")
        return []

def scan_wifi():
    """Scan Wi-Fi networks based on the operating system."""
    system = platform.system()
    
    if system == 'Windows':
        return scan_wifi_windows()
    elif system == 'Linux':
        return scan_wifi_linux()
    elif system == 'Darwin':  # macOS
        return scan_wifi_macos()
    else:
        return []

@app.route('/')
def index():
    """Serve the main HTML page."""
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'wifi-analyzer.html')

@app.route('/scan', methods=['GET'])
def scan():
    """Endpoint to scan for Wi-Fi networks."""
    try:
        networks = scan_wifi()
        
        # Sort by signal strength (descending)
        networks.sort(key=lambda x: int(x.get('signal', 0)), reverse=True)
        
        return jsonify({
            'success': True,
            'networks': networks,
            'count': len(networks)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'networks': []
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'platform': platform.system()})

if __name__ == '__main__':
    print("=" * 60)
    print("Wi-Fi Security Analyzer - Backend Server")
    print("=" * 60)
    print("\n⚠️  EDUCATIONAL USE ONLY")
    print("Only scan networks you own or have explicit permission to analyze.\n")
    print("Server starting on http://localhost:5000")
    print("Open wifi-analyzer.html in your browser to use the interface.\n")
    print("=" * 60)
    
    app.run(host='127.0.0.1', port=5000, debug=True)

