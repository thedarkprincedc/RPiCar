## Auto Pi Car
Remote control car software for Raspberry Pi using an L298N H-Bridge motor driver.  
Supports PS5 DualSense controllers (USB + Bluetooth).

### Features
- DualSense controller support
- Keyboard fallback control (optional)
- Real-time motor control
- Threaded input system (non-blocking)
- Cross-platform input decoding layer

---

### Hardware
- Raspberry Pi (3/4/5)
- L298N H-Bridge motor driver
- DC motors + chassis
- Power supply (separate motor power recommended)

---

### Requirements
- Python 3.9+
- Linux (recommended: Raspberry Pi OS)

---

### Setup

Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install Dependencies
```bash
pip install -r requirements.txt
```

Run Application
```bash
python src/main.py
```