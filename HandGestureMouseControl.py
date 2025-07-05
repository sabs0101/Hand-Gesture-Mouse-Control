import cv2
import mediapipe as mp
from pynput.mouse import Controller, Button
import threading
import time
import math

# Mouse controller
mouse = Controller()

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)
mp_draw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # Low resolution for faster processing
cap.set(4, 240)

# Screen resolution
screen_w, screen_h = 1920, 1080  # Change to your screen if different

# Smoothing and thresholds
prev_x, prev_y = 0, 0
smoothening = 5
move_threshold = 5

# Shared values for mouse thread
mouse_x = 0
mouse_y = 0
click_flag = False
lock = threading.Lock()

# Click control variables
clicking = False
last_click_time = 0
click_cooldown = 0.6  # seconds

# Mouse movement and click thread
def mouse_worker():
    global mouse_x, mouse_y, click_flag
    while True:
        with lock:
            x, y = mouse_x, mouse_y
            do_click = click_flag
            click_flag = False
        mouse.position = (x, y)
        if do_click:
            mouse.click(Button.left, 1)
        time.sleep(0.01)

# Start background thread
threading.Thread(target=mouse_worker, daemon=True).start()

# Main camera + hand tracking loop
while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm_list = []
        h, w, _ = img.shape
        for id, lm in enumerate(hand.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append((id, cx, cy))

        mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

        # Index tip and thumb tip
        index_x, index_y = lm_list[8][1], lm_list[8][2]
        thumb_x, thumb_y = lm_list[4][1], lm_list[4][2]

        # Draw circles
        cv2.circle(img, (index_x, index_y), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (thumb_x, thumb_y), 8, (255, 0, 255), cv2.FILLED)

        # Screen mapping
        target_x = int(index_x * screen_w / 320)
        target_y = int(index_y * screen_h / 240)

        # Smooth movement
        curr_x = prev_x + (target_x - prev_x) // smoothening
        curr_y = prev_y + (target_y - prev_y) // smoothening

        if abs(curr_x - prev_x) > move_threshold or abs(curr_y - prev_y) > move_threshold:
            with lock:
                mouse_x = curr_x
                mouse_y = curr_y
            prev_x, prev_y = curr_x, curr_y

        # Pinch detection for click
        distance = math.hypot(index_x - thumb_x, index_y - thumb_y)
        now = time.time()

        if distance < 30:
            if not clicking and (now - last_click_time) > click_cooldown:
                with lock:
                    click_flag = True
                clicking = True
                last_click_time = now
                cv2.circle(img, (index_x, index_y), 15, (0, 255, 0), cv2.FILLED)
        else:
            clicking = False

    # Show webcam feed
    cv2.imshow("Gesture Mouse (Final Version)", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break



