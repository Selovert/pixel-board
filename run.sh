#!/bin/bash

FIFO=/tmp/pixel-frames
RUNNER=/usr/local/pixel-board/app/rpi-rgb-led-matrix/rgbmatrix
PYTHON=/usr/local/pixel-board/.venv/bin/python
BOARD=/usr/local/pixel-board/app/board.py
DISPLAY_BIN=/usr/local/pixel-board/app/build/display
RESTART_INTERVAL=3600

mkfifo "$FIFO" 2>/dev/null || true

# Start display first — its child process blocks on opening the FIFO for
# reading until we open the write end below. The parent shell continues.
$RUNNER $DISPLAY_BIN < "$FIFO" &
DISPLAY_PID=$!
trap "kill $DISPLAY_PID 2>/dev/null; rm -f $FIFO" EXIT

# Opening the write end unblocks the display child and also keeps fd 3 open
# for the lifetime of this script, so display never sees EOF between Python restarts.
exec 3>"$FIFO"

while true; do
    timeout $RESTART_INTERVAL $PYTHON $BOARD > "$FIFO" || true
    sleep 0.1  # ~100ms pause while Python restarts; display holds last frame
done
