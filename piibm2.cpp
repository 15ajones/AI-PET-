#include <unistd.h>
#include <iostream>
#include <signal.h>
#include <thread>
#include <led-matrix.h>
#include <graphics.h>

volatile sig_atomic_t running = 1;

void sigHandler(int signo) {
    running = 0;
}

int main() {
    signal(SIGTERM, sigHandler);
    signal(SIGINT, sigHandler);

    // Set up the RGB matrix options
    RGBMatrix::Options matrixOptions;
    matrixOptions.hardware_mapping = "regular";  // or "adafruit-hat" for HAT boards
    matrixOptions.rows = 32;
    matrixOptions.cols = 32;
    matrixOptions.chain_length = 1;
    matrixOptions.parallel = 1;

    // Create the RGB matrix object
    RGBMatrix matrix(matrixOptions);

    // Create a canvas to draw on
    FrameCanvas* canvas = matrix.CreateFrameCanvas();

    // Load and display an image on the canvas
    const std::string imagePath = "path_to_your_image.jpg";  // Update with the path to your image
    if (canvas->LoadImage(imagePath)) {
        // Resize the image to fit the LED matrix size
        canvas->Resize(matrix.width(), matrix.height());

        // Display the canvas on the matrix
        matrix.SwapOnVSync(canvas);
    } else {
        std::cout << "Failed to load image: " << imagePath << std::endl;
    }

    // Wait for a few seconds
    sleep(5);

    // Clean up
    delete canvas;

    return 0;
}
