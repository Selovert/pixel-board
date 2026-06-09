// Reads raw RGB frames from stdin and drives the LED matrix.
// Designed to run as the read end of a named FIFO (see run.sh); board.py is
// the writer.

#include <cstdio>
#include <cstdlib>
#include <vector>
#include "led-matrix.h"

using namespace rgb_matrix;

// Reads exactly n bytes into buf, retrying across short reads.
// Returns false only on EOF or error (i.e. the writer closed the pipe).
static bool read_frame(uint8_t* buf, size_t n) {
    size_t total = 0;
    while (total < n) {
        size_t got = fread(buf + total, 1, n - total, stdin);
        if (got == 0) return false;
        total += got;
    }
    return true;
}

int main() {
    RGBMatrix::Options options;
    options.rows = 32;
    options.cols = 64;
    options.brightness = 60;
    options.chain_length = 1;
    options.parallel = 1;
    options.hardware_mapping = "adafruit-hat-pwm";
    options.led_rgb_sequence = "RBG";  // physical wiring on this hat is R-B-G
    options.limit_refresh_rate_hz = 160;

    RuntimeOptions runtime;
    runtime.gpio_slowdown = 3;  // Pi Zero 2W needs slowdown to avoid glitches

    RGBMatrix* matrix = CreateMatrixFromOptions(options, runtime);
    if (!matrix) {
        fprintf(stderr, "Failed to create matrix\n");
        return 1;
    }

    // Double-buffered canvas: we write into the back buffer and swap on vsync
    // to avoid tearing.
    FrameCanvas* canvas = matrix->CreateFrameCanvas();
    const int w = matrix->width();
    const int h = matrix->height();

    std::vector<uint8_t> buf(w * h * 3);  // one frame: 64*32*3 = 6144 bytes

    while (read_frame(buf.data(), buf.size())) {
        for (int y = 0; y < h; ++y) {
            const uint8_t* row = buf.data() + y * w * 3;
            for (int x = 0; x < w; ++x) {
                canvas->SetPixel(x, y, row[x*3], row[x*3+1], row[x*3+2]);
            }
        }
        // Blocks until the matrix's internal refresh thread is ready to swap,
        // then returns the now-free back buffer for the next frame.
        canvas = matrix->SwapOnVSync(canvas);
    }

    matrix->Clear();
    delete matrix;
    return 0;
}
