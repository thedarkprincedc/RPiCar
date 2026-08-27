## RPiCar
Remote control car software for Raspberry Pi using an waveshare rover chasis.  

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
4. [Waveshare Rover](https://www.waveshare.com/wiki/WAVE_ROVER#Driver_Board_General_Driver_for_Robots_Module_Usage_Tutorial)

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

### Install Dependencies (Requirements)
Install Dependencies
```bash
pip install -r requirements.txt
```
Install Dependencies (Environment - Development)
```bash
pip install -r requirements-dev.txt
```

### Install Dependencies (PyProject)
Install Dependencies
```bash
pip install .
```

Install Dependencies (Environment - Development) 
```bash
pip install -e ".[dev]"
```

Run Application (On Car - Linux)
```bash
python src/main.py
```

PORT = "/dev/serial0"
SupplementaryGroups=dialout,input,bluetooth


### Synchronize Files from (Windows)
```bash
scripts/dev.sh
```
### Start Daemon
```bash
scripts/setup.sh
```
### Uninstall Daemon
```bash
scripts/uninstall.sh
```

### Run Application
```bash
scripts/run.sh
```

py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .


python -m pip install .