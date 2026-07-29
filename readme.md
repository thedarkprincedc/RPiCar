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

Create virtual environment: (osx/linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Create virtual environment: (windows)
```bash
python3 -m venv .venv
source .venv/Scripts/activate
```

Install Dependencies
```bash
pip install -r requirements.txt
```

Run Application
```bash
python src/main.py
```

PORT = "/dev/serial0"

```
python -m venv venv
source .venv/Scripts/activate
pip install -r requirements-dev.txt
```

python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

### Secure Shell Access
---
#### Generate SSH Key
```bash 
ssh-keygen -t ed25519 -C "your_email@example.com"
ssh-keygen -t ed25519 -f ~/.ssh/rpi_key -C "Raspberry Pi"

ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_rpicar -C "RPiCar SSH key"
```

#### Copy Public SSH Key to Server for Login
```bash
ssh-copy-id admin@<pi-ip-address>
ssh-copy-id -i ~/.ssh/id_ed25519_rpicar.pub admin@<pi-ip-address>
```

#### Use SSH Key to Server for Login
```bash
ssh admin@<pi-ip-address>
ssh -i ~/.ssh/my_key admin@<pi-ip-address>
```

### Setup Service
---
#### Start Service

```bash
sudo cp rpicar.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rpicar
sudo systemctl start rpicar
```

#### Stop Service

```bash
sudo systemctl stop rpicar
```

#### Restart Service

```bash
sudo systemctl restart rpicar
```

#### Disable Service

```bash
sudo systemctl disable rpicar
```