#include <cstdio>
#include <cstdlib>
#include <vector>
#include "led-matrix.h"

using namespace rgb_matrix;

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
    RGBMatrixOptions options;
    options.rows = 32;
    options.cols = 64;
    options.brightness = 60;
    options.chain_length = 1;
    options.parallel = 1;
    options.hardware_mapping = "adafruit-hat-pwm";
    options.led_rgb_sequence = "RBG";
    options.limit_refresh_rate_hz = 160;

    RuntimeOptions runtime;
    runtime.gpio_slowdown = 3;

    RGBMatrix* matrix = CreateMatrixFromOptions(options, runtime);
    if (!matrix) {
        fprintf(stderr, "Failed to create matrix\n");
        return 1;
    }

    FrameCanvas* canvas = matrix->CreateFrameCanvas();
    const int w = matrix->width();
    const int h = matrix->height();

    std::vector<uint8_t> buf(w * h * 3);

    while (read_frame(buf.data(), buf.size())) {
        for (int y = 0; y < h; ++y) {
            const uint8_t* row = buf.data() + y * w * 3;
            for (int x = 0; x < w; ++x) {
                canvas->SetPixel(x, y, row[x*3], row[x*3+1], row[x*3+2]);
            }
        }
        canvas = matrix->SwapOnVSync(canvas);
    }

    matrix->Clear();
    delete matrix;
    return 0;
}
