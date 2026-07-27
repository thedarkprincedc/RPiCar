HOST_IP_OR_NAME=10.1.20.235

scp -r * admin@$HOST_IP_OR_NAME:/home/admin/RPiCar
ssh admin@$HOST_IP_OR_NAME "cd ~/RPiCar && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 src/main.py"