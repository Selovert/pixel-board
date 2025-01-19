#!/bin/bash

# -- install python bindings --
sudo apt-get update && sudo apt-get install python3-dev cython3 -y
(cd /home/dietpi/Projects/pixel-board/app/rpi-rgb-led-matrix/ && sudo make build-python)
(cd /home/dietpi/Projects/pixel-board/app/rpi-rgb-led-matrix/ && sudo make install-python)
