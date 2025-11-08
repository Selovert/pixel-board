#!/bin/bash

echo "------ Installing dependencies ------"
sudo apt-get update && sudo apt-get install -y build-essential python3-dev cython3 python3 python3.11-venv python3-pip
# -- install uv --
echo "------ Installing uv ------"
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH=~/.local/bin:$PATH
echo "------ installing venv ------"
cd /usr/local/pixel-board
uv lock --no-dev
echo "------ Installing python packages ------"
uv export --no-dev --no-hashes > requirements.txt
sudo pip install -r requirements.txt --break-system-packages
echo "------ Build rpi matrix python bindings ------"
(cd app/rpi-rgb-led-matrix/ && sudo make build-python)
(cd app/rpi-rgb-led-matrix/ && sudo make install-python)
echo "------ Add nightly restart to crontab ------"
# (sudo crontab -l 2>/dev/null; echo "30 2   *   *   *    reboot") | sudo crontab -

mkdir /var/lib/dietpi/dietpi-autostart/
touch /var/lib/dietpi/dietpi-autostart/custom.sh
cat > /var/lib/dietpi/dietpi-autostart/custom.sh << EOF
#!/bin/bash
# DietPi-AutoStart custom script
# Location: /var/lib/dietpi/dietpi-autostart/custom.sh
/usr/local/pixel-board/run.sh
EOF