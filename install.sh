#!/bin/bash

echo "------ Installing dependencies ------"
sudo apt-get update && sudo apt-get install -y build-essential python3-dev cython3 python3 python3.11-venv python3-pip
# -- install PDM --
echo "------ Installing PDM ------"
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
export PATH=~/.local/bin:$PATH
echo "------ Building PDM lock ------"
cd /usr/local/pixel-board
pdm install
echo "------ Installing python packages ------"
pdm export -o requirements.txt --without-hashes
sudo pip install -r requirements.txt --break-system-packages
echo "------ Build rpi matrix python bindings ------"
(cd app/rpi-rgb-led-matrix/ && sudo make build-python)
(cd app/rpi-rgb-led-matrix/ && sudo make install-python)
echo "------ Add nightly restart to crontab ------"
(sudo crontab -l 2>/dev/null; echo "30 2   *   *   *    /sbin/shutdown -r +5") | sudo crontab -

mkdir /var/lib/dietpi/dietpi-autostart/
touch /var/lib/dietpi/dietpi-autostart/custom.sh
cat > /var/lib/dietpi/dietpi-autostart/custom.sh << EOF
#!/bin/bash
# DietPi-AutoStart custom script
# Location: /var/lib/dietpi/dietpi-autostart/custom.sh
/usr/local/pixel-board/app/board.py
EOF