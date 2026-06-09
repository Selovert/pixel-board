#!/bin/bash

echo "------ Installing system dependencies ------"
sudo apt-get update && sudo apt-get install -y build-essential python-dev-is-python3 python3-dev cmake python3 python3-pil cython3

echo "------ Installing uv ------"
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH=~/.local/bin:$PATH

echo "------ Installing Python packages ------"
cd /usr/local/pixel-board
uv sync

echo "------ Building and installing rgbmatrix Python bindings ------"
uv pip install ./app/rpi-rgb-led-matrix/

echo "------ Configuring autostart ------"
mkdir -p /var/lib/dietpi/dietpi-autostart/
cat > /var/lib/dietpi/dietpi-autostart/custom.sh << EOF
#!/bin/bash
# DietPi-AutoStart custom script
# Location: /var/lib/dietpi/dietpi-autostart/custom.sh
/usr/local/pixel-board/run.sh
EOF
