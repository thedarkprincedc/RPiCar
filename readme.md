## RPiCar
Remote control car software for Raspberry Pi using an Waveshare Rover chasis.  

### Features
- Supports PS5 DualSense controllers (USB + Bluetooth).
- Keyboard fallback control (optional)
- Real-time motor control
- Threaded input system (non-blocking)
- Cross-platform input decoding layer
- Serial Communication 

### Hardware
- Raspberry Pi (3/4/5)
- Waveshare Rover Chasis

### Requirements
- Python 3.9+
- Linux (recommended: Raspberry Pi OS)

### Documents

1. [SystemCtrl](docs/systemctl.md)
2. [Secure Shell (ssh)](docs/ssh.md)
3. [Virtual Environments](docs/venv.md)

---

### Commands

Create/Run Virtual Environment (Development - Windows)
```bash
python -m venv venv
source venv/Scripts/activate
```

Create/Run Virtual Environment (Linux)
```bash
python -m venv venv
source venv/bin/activate
```

Install Dependencies (Development)
```bash
pip install -r requirements-dev.txt
```

Install Dependencies
```bash
pip install -r requirements.txt
```

Run Application (On Car - Linux)
```bash
python src/main.py
```

PORT = "/dev/serial0"