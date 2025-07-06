import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Track last gesture to prevent continuous keypress
last_gesture = None
gesture_cooldown = 1  # seconds
last_time = time.time()

# Define gesture detection logic
def get_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x

    tips = [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]
    average_tip = np.mean(tips)

    # Determine gesture based on distance
    finger_states = [tip > average_tip + 0.02 for tip in tips]

    if finger_states == [False, False, False, False, False]:
        return "FIST"
    elif finger_states == [True, True, True, True, True]:
        return "PALM"
    elif finger_states[1] and not any(finger_states[i] for i in [0, 2, 3, 4]):
        return "POINT"
    elif finger_states[0] and not any(finger_states[1:]):
        return "THUMBS_UP"
    else:
        return "UNKNOWN"

# Map gestures to keyboard actions
def trigger_action(gesture):
    global last_gesture, last_time
    if gesture != last_gesture and (time.time() - last_time > gesture_cooldown):
        if gesture == "FIST":
            pyautogui.press('ctrl')  # Attack
        elif gesture == "PALM":
            pyautogui.press('space')  # Jump
        elif gesture == "POINT":
            pyautogui.press('w')  # Move forward
        elif gesture == "THUMBS_UP":
            pyautogui.press('e')  # Special action
        last_gesture = gesture
        last_time = time.time()

# Main loop
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.6, max_num_hands=1) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image = cv2.flip(image, 1)  # Flip image for mirror view
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        gesture = "No Hand"
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = get_gesture(hand_landmarks)
                trigger_action(gesture)

        # Display gesture
        cv2.putText(image, f'Gesture: {gesture}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow('Gesture Game Controller', image)

        if cv2.waitKey(10) & 0xFF == 27:  # ESC to exit
            break

cap.release()
cv2.destroyAllWindows()
