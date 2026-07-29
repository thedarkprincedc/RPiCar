#sudo nano /etc/systemd/system/rpicar.service
sudo cp rpicar.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rpicar
sudo systemctl start rpicar