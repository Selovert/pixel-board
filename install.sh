#!/bin/bash

# -- install python bindings --
# sudo apt-get update && sudo apt-get install python3-dev cython3 -y
# (cd app/rpi-rgb-led-matrix/ && sudo make build-python)
# (cd app/rpi-rgb-led-matrix/ && sudo make install-python)

sudo pdm install
pdm export -o requirements.txt --without-hashes
sudo pip install -r requirements.txt