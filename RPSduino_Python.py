import cv2
import mediapipe as mp
import random
import serial
import time
import winsound  # Import winsound for sound effects

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Set up serial communication with Arduino
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Allow Arduino to initialize

# Function to classify gestures
def classify_gesture(hand_landmarks, hand_type):
    thumb_is_open = hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x if hand_type == "Right" else hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x
    index_is_open = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_is_open = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    ring_is_open = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
    pinky_is_open = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y

    if not (thumb_is_open or index_is_open or middle_is_open or ring_is_open or pinky_is_open):
        return "Rock"
    elif all([thumb_is_open, index_is_open, middle_is_open, ring_is_open, pinky_is_open]):
        return "Paper"
    elif index_is_open and middle_is_open and not (ring_is_open or pinky_is_open or thumb_is_open):
        return "Scissors"
    return "Unknown"

# Initialize game variables
computer_score = 0
user_score = 0

# Open video capture
cap = cv2.VideoCapture(1)  # Change index if needed for DroidCam
if not cap.isOpened():
    print("Error: Unable to access camera.")
    exit()

print("Press 's' to start the game or 'q' to quit.")

while True:
    key = input("Enter 's' to start or 'q' to quit: ").strip().lower()
    if key == 'q':
        print("Exiting game. Goodbye!")
        break
    elif key == 's':
        print("Game started!")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read frame.")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            user_move = "Unknown"
            computer_move = "Waiting..."
            user_detected = False

            # Detect user's gesture
            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Get hand type (Right/Left)
                    hand_type = results.multi_handedness[idx].classification[0].label
                    user_move = classify_gesture(hand_landmarks, hand_type)
                    user_detected = True

            # Generate computer's move only when user's move is detected
            if user_detected:
                computer_move = random.choice(["Rock", "Paper", "Scissors"])

                # Scoring logic
                if user_move == "Rock" and computer_move == "Scissors":
                    user_score += 1
                elif user_move == "Paper" and computer_move == "Rock":
                    user_score += 1
                elif user_move == "Scissors" and computer_move == "Paper":
                    user_score += 1
                elif user_move != "Unknown" and user_move != computer_move:
                    computer_score += 1

            # Display moves and scores
            cv2.putText(frame, f"Your Move: {user_move}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Computer: {computer_move}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Scores - You: {user_score} Comp: {computer_score}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Send scores to Arduino
            arduino.write(f"{user_score},{computer_score}\n".encode())

            # Show video feed
            cv2.imshow("Rock-Paper-Scissors", frame)

            # Sound effects based on the result
            if user_move != "Unknown":
                if user_move == "Rock" and computer_move == "Scissors":
                    winsound.PlaySound("win.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                elif user_move == "Paper" and computer_move == "Rock":
                    winsound.PlaySound("win.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                elif user_move == "Scissors" and computer_move == "Paper":
                    winsound.PlaySound("win.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                elif user_move == computer_move:
                    winsound.PlaySound("draw.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                else:
                    winsound.PlaySound("lose.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

            # Exit conditions
            if user_move == "Paper" or cv2.waitKey(1) & 0xFF == ord('q'):
                winner = "You Won!" if user_score > computer_score else "Computer Won!" if computer_score > user_score else "It's a Tie!"
                print(f"Game Over! Final Score - User: {user_score}, Computer: {computer_score}. {winner}")
                arduino.write(f"Game Over,{winner}\n".encode())
                winsound.PlaySound("game_over.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                break

            time.sleep(1)  # Add time gap between rounds

        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
