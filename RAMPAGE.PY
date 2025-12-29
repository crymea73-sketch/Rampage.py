import ctypes
import random
import time
import math

# Load Win32 APIs
user32 = ctypes.WinDLL("user32")
gdi32  = ctypes.WinDLL("gdi32")

GetDC            = user32.GetDC
GetSystemMetrics = user32.GetSystemMetrics
BitBlt           = gdi32.BitBlt
StretchBlt       = gdi32.StretchBlt
PatBlt           = gdi32.PatBlt

# Raster ops
SRCCOPY   = 0x00CC0020
SRCINVERT = 0x00660046
BLACKNESS = 0x00000042
WHITENESS = 0x00FF0062
PATINVERT = 0x005A0049

# Screen metrics
SM_CXSCREEN = 0
SM_CYSCREEN = 1

# Desktop DC
hdc = GetDC(ctypes.c_void_p(0))
sw  = GetSystemMetrics(SM_CXSCREEN)
sh  = GetSystemMetrics(SM_CYSCREEN)

# ---------------- PHASES ---------------- #

def smear_horizontal():
    y = random.randint(0, sh - 1)
    h = random.randint(5, 80)
    offset = random.randint(-200, 200)
    BitBlt(hdc, offset, y, sw, h, hdc, 0, y, SRCCOPY)

def smear_vertical():
    x = random.randint(0, sw - 1)
    w = random.randint(5, 80)
    offset = random.randint(-200, 200)
    BitBlt(hdc, x, offset, w, sh, hdc, x, 0, SRCCOPY)

def zoom_pulse():
    w = random.randint(200, sw)
    h = random.randint(200, sh)
    x = random.randint(0, sw - w)
    y = random.randint(0, sh - h)

    scale = random.choice([0.5, 0.75, 1.25, 1.5, 2.0])
    dw = int(w * scale)
    dh = int(h * scale)
    dx = x + (w - dw) // 2
    dy = y + (h - dh) // 2

    StretchBlt(hdc, dx, dy, dw, dh, hdc, x, y, w, h, SRCCOPY)

def invert_rects():
    for _ in range(random.randint(5, 25)):
        w = random.randint(40, 300)
        h = random.randint(40, 300)
        x = random.randint(0, sw - w)
        y = random.randint(0, sh - h)
        BitBlt(hdc, x, y, w, h, hdc, x, y, SRCINVERT)

def scanlines():
    step = random.randint(3, 10)
    for y in range(0, sh, step * 2):
        BitBlt(hdc, 0, y + step, sw, step, hdc, 0, y, SRCCOPY)

def slice_wave():
    slice_h = random.randint(10, 80)
    t = time.time()
    for y in range(0, sh, slice_h):
        offset = int(80 * math.sin(t * 3 + y * 0.05))
        BitBlt(hdc, offset, y, sw, slice_h, hdc, 0, y, SRCCOPY)

def flash_blocks():
    mode = random.choice([BLACKNESS, WHITENESS, PATINVERT])
    for _ in range(random.randint(10, 40)):
        w = random.randint(50, 250)
        h = random.randint(50, 250)
        x = random.randint(0, sw - w)
        y = random.randint(0, sh - h)
        PatBlt(hdc, x, y, w, h, mode)

# Phase list
phases = [
    smear_horizontal,
    smear_vertical,
    zoom_pulse,
    invert_rects,
    scanlines,
    slice_wave,
    flash_blocks
]

# ---------------- MAIN LOOP ---------------- #

def main():
    print("RAMPAGE Chaos Engine running. Ctrl+C to stop.")
    try:
        while True:
            phase = random.choice(phases)
            for _ in range(random.randint(5, 25)):
                phase()
                time.sleep(0.01)
    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == "__main__":
    main()
