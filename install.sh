#!/bin/bash

sudo apt-get update && sudo apt-get install -y build-essential python3-dev cython3 python python3.11-venv pip
# -- install PDM --
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
export PATH=/dietpi/.local/bin:$PATH
# -- clone the repo and cd in --
git clone --recurse-submodules https://github.com/Selovert/pixel-board
cd pixel-board
# -- install python dependencies --
sudo pdm install
pdm export -o requirements.txt --without-hashes
sudo pip install -r requirements.txt --break-system-packages
# -- install python bindings --
(cd app/rpi-rgb-led-matrix/ && sudo make build-python)
(cd app/rpi-rgb-led-matrix/ && sudo make install-python)