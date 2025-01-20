#!/bin/bash

echo "------ Installing dependencies ------"
sudo apt-get update && sudo apt-get install -y build-essential python3-dev cython3 python3 python3.11-venv python3-pip
# -- install PDM --
echo "------ Installing PDM ------"
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
export PATH=/dietpi/.local/bin:$PATH
echo "------ Building PDM lock ------"
cd /usr/local/pixel-board
sudo pdm install
echo "------ Installing python packages ------"
pdm export -o requirements.txt --without-hashes
sudo pip install -r requirements.txt --break-system-packages
echo "------ Build rpi matrix python bindings ------"
(cd app/rpi-rgb-led-matrix/ && sudo make build-python)
(cd app/rpi-rgb-led-matrix/ && sudo make install-python)