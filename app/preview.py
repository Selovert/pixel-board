#!/usr/bin/env python3
"""Dev preview: python app/board.py | python app/preview.py"""
import sys
import queue
import threading
import tkinter as tk
from PIL import Image, ImageTk

W, H, SCALE = 64, 32, 12
FRAME = W * H * 3

root = tk.Tk()
root.title("pixel-board preview")
root.resizable(False, False)
label = tk.Label(root)
label.pack()

# stdin reads block, so they run on a background thread and frames are handed
# to the main thread via a queue. maxsize=2 drops frames if the UI falls behind.
frame_queue: queue.Queue = queue.Queue(maxsize=2)

def reader():
    while True:
        data = sys.stdin.buffer.read(FRAME)
        if len(data) < FRAME:
            root.quit()
            return
        try:
            frame_queue.put_nowait(data)
        except queue.Full:
            pass

threading.Thread(target=reader, daemon=True).start()

def next_frame():
    try:
        data = frame_queue.get_nowait()
        img = Image.frombytes('RGB', (W, H), data).resize(
            (W * SCALE, H * SCALE), Image.NEAREST)
        photo = ImageTk.PhotoImage(img)
        label.configure(image=photo)
        label.image = photo  # prevent GC
    except queue.Empty:
        pass
    root.after(16, next_frame)

root.after(0, next_frame)
root.mainloop()
