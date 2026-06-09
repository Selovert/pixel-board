#!/bin/bash

RUNNER=/usr/local/pixel-board/app/rpi-rgb-led-matrix/rgbmatrix
PYTHON=/usr/local/pixel-board/.venv/bin/python
BOARD=/usr/local/pixel-board/app/board.py
DISPLAY=/usr/local/pixel-board/app/build/display

while true; do
  $PYTHON $BOARD | $RUNNER $DISPLAY
done
