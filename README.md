# 🛡️ Advanced Network Intelligence Scanner

A modular Python-based **Network Security Assessment Platform** capable of automated LAN discovery, multi-threaded port scanning, device classification, CVE intelligence lookup, risk scoring, topology visualization, persistent scan storage, and web-based monitoring.

---

# 🚀 Features

- Automatic Local Network Detection (`--auto`)
- ARP-Based Host Discovery
- Multi-Threaded TCP Port Scanning
- Custom Port Selection
- Service Banner Grabbing
- Device Type Identification
- Risk Scoring Engine (LOW / MEDIUM / HIGH)
- CVE Lookup via NVD API
- Network Topology Visualization
- SQLite Scan History
- Flask-Based Web Dashboard

---

# 📁 Project Structure

```
advanced_network_scanner/
│
├── main.py
├── scanner.py
├── host_discovery.py
├── utils.py
├── risk_analyzer.py
├── device_identifier.py
├── cve_lookup.py
├── topology_visualizer.py
├── report_generator.py
├── database.py
├── dashboard.py
├── requirements.txt
└── templates/
    └── dashboard.html
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/advanced-network-scanner.git
cd advanced-network-scanner
```

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🖥️ Usage

## 🔹 Scan Single Target

```bash
python main.py -t 192.168.1.10
```

---

## 🔹 Scan with Custom Ports

```bash
python main.py -t 192.168.1.10 -p 22,80,443
```

---

## 🔹 Scan Entire Local Network (Auto Mode)

```bash
sudo python main.py --auto
```

> **Note:** ARP scanning requires administrator/root privileges.

---

# 🌐 Launch Web Dashboard

```bash
python dashboard.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

# 📊 Generated Output Files

After scanning, the tool generates:

- `report_<ip>.json`
- `report_<ip>.html`
- `network_topology.png`
- `scan_history.db`

---

# 🧠 Risk Scoring Logic

| Port | Service | Risk Score |
|------|----------|------------|
| 21   | FTP      | +3 |
| 23   | Telnet   | +5 |
| 3389 | RDP      | +4 |
| 445  | SMB      | +4 |

Risk Levels:
- 0–4 → LOW  
- 5–9 → MEDIUM  
- 10+ → HIGH  

---

# 🛠️ Technologies Used

- Python
- Scapy
- Socket Programming
- ThreadPoolExecutor
- SQLite3
- Flask
- NetworkX
- Matplotlib
- Requests (NVD API)

---

# 🔐 Ethical Disclaimer

This tool is intended strictly for:

- Educational purposes  
- Personal lab environments  
- Authorized network security testing  

Unauthorized network scanning without permission is illegal.

---

# 📌 Resume Description

Developed a modular Network Security Assessment Platform in Python featuring automated LAN discovery, multi-threaded port scanning, device classification, CVE intelligence integration, dynamic risk scoring engine, topology visualization, persistent scan history database, and a web-based monitoring dashboard.

---

# 👨‍💻 Author

 Cybersecurity and Ethical hacking club - KL Sac
