FROM ptrsr/pi-ci:latest

# Your additional tooling
RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        git \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/RPiCar

COPY pyproject.toml .
COPY src ./src

# Install dependencies
RUN pip install --no-cache-dir .

#COPY . .

#RUN python3 -m pip install --break-system-packages -e .

CMD ["start"]