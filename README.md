# RPSDUINO

# Rock-Paper-Scissors Game with Hand Gesture Recognition and Arduino LCD Display

This repository contains the code for a Rock-Paper-Scissors game that uses hand gesture recognition with Python and real-time score display on an Arduino-driven LCD. The game is designed to be interactive, leveraging MediaPipe for gesture detection and an LCD1602 module (I2C interface) for displaying the game results.

## Features
- Real-time hand gesture detection using MediaPipe and OpenCV.
- Arduino Uno and an LCD1602 module to display scores and game results.
- Sound effects for win, lose, draw, and game over events.
- Compatibility with Windows and DroidCam as the input camera.

## Specifications

### Hardware
- **Microcontroller**: Arduino Uno
- **Display**: LCD1602 module with pin header, I2C interface
- **Camera**: DroidCam (used instead of the laptop's built-in webcam)

### Software
- **Python**: Version 3.12.8
- **Arduino IDE**: Version 2.3.4
- **Operating System**: Windows

## Repository Contents

### Python Code: `rpsduino-python.py`
This script handles gesture recognition and game logic.
- Detects hand gestures (Rock, Paper, Scissors) using a webcam.
- Randomly generates a move for the computer.
- Determines the winner and updates scores.
- Sends scores to the Arduino via serial communication.
- Plays sound effects for game events.

#### Dependencies
- OpenCV (`opencv-python`)
- MediaPipe
- PySerial
- Winsound (Windows only, for sound effects)

#### Running the Script
1. Install dependencies using pip:
   ```bash
   pip install opencv-python mediapipe pyserial
   ```
2. Connect the Arduino to your computer.
3. Ensure DroidCam is set up and running.
4. Run the script:
   ```bash
   python rpsduino-python.py
   ```

### Arduino Code: `rpsduino-arduino.ino`
This sketch manages the display of scores and game results on the LCD1602 module.
- Receives scores and messages from the Python script via serial communication.
- Displays the current scores and updates the screen in real-time.

#### Uploading the Sketch
1. Open `rpsduino-arduino.ino` in the Arduino IDE.
2. Ensure the correct COM port and board are selected in the IDE settings.
3. Upload the sketch to the Arduino Uno.
4. Connect the LCD1602 module to the Arduino as per the wiring defined in the code.

## How to Play
1. **Set Up Hardware**:
   - Connect the LCD1602 module to the Arduino Uno using the I2C interface.
   - Ensure all connections match the pin configuration in the Arduino sketch.
2. **Start the Python Script**:
   - Launch the Python script and follow on-screen instructions.
   - Use DroidCam to capture hand gestures.
3. **Play the Game**:
   - Make gestures for Rock (fist), Paper (open hand), or Scissors (peace sign) in front of the camera.
   - Watch the scores update on the LCD in real time.
   - End the game by showing a "Paper" gesture or pressing `q` in the Python terminal.

## Notes
- Ensure the serial port in the Python script (`COM3`) matches the port assigned to your Arduino.
- Sound effects require `.wav` files (`win.wav`, `draw.wav`, `lose.wav`, `game_over.wav`) to be in the same directory as the Python script.
- Adjust the camera index in the Python script if DroidCam is not detected as `1`.

## License
This project is licensed under the MIT License. Feel free to modify and use it in your projects.

