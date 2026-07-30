## SystemCtl

Start Service
```bash
sudo cp rpicar.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rpicar
sudo systemctl start rpicar
```

Stop Service
```bash
sudo systemctl stop rpicar
```

Restart Service
```bash
sudo systemctl restart rpicar
```

Disable Service
```bash
sudo systemctl disable rpicar
```