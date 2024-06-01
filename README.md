# Football Analysis Project

This project is designed to analyze football matches using computer vision techniques. The project is divided into three Python files: `funcs.py`, `libs.py`, and `main.py`.

## File Descriptions

1. **funcs.py**: This file contains all the functions used in the project. These functions include:
    - `getFrames()`: Extracts frames from a video file and saves them in a specified location.
    - `maskPlayers()`: Masks players in a frame based on their jersey color.
    - `applyMask()`: Applies a mask to a frame.
    - `joinImages()`: Joins two images side by side.
    - `getNewBallPosition()`: Determines the new position of the ball.
    - `detectBall()`: Detects the ball in the frames.
    - `dist()`: Calculates the distance between two points.
    - `getFirstFrameCenter()`: Determines the center of the first frame.
    - `getRegion()`: Determines the region of the frame.

2. **libs.py**: This file imports the required libraries for the project, which include `cv2`, `numpy`, and `os`.

3. **main.py**: This is the main file that uses the functions defined in `funcs.py` to perform the football analysis. It includes the extraction of frames, masking of players, detection of the ball, and region labeling.

## Usage

To use this project, run the `main.py` file. The program will display the frames with the masked players and the detected ball. Press the "q" key to move to the next frame. The program will automatically close the display window once all frames have been processed.

## Requirements

This project requires Python 3 and the following Python libraries installed:

- OpenCV
- NumPy

## Note

Please ensure that the video file path and the target location for saving frames are correctly specified in the `getFrames()` function in `main.py`. The initial position of the ball and the ball size should also be accurately provided in the `detectBall()` function.

This project is intended for educational purposes only and is not suitable for real-time football match analysis. The accuracy of the player masking and ball detection may vary depending on the quality of the video and the color of the players' jerseys and the ball. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
