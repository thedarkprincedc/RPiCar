# initialize raspberrypi
sudo apt update
sudo apt install -y \
    git

# download project
git clone https://github.com/thedarkprincedc/RPiCar.git
cd ./RPiCar
git checkout development/rpicar

# install dependencies
python3 -m venv --system-site-packages venv
# python -m venv venv
source venv/bin/activate
pip install -e .

#
python src/main.py --debug
python src/server.py --debug


udo apt install -y libcap-dev
sudo apt install -y build-essential
sudo apt install python3.13-dev

sudo apt install -y \
    python3-libcamera \
    python3-kms++ \
    python3-picamera2 \
    libcamera-apps

