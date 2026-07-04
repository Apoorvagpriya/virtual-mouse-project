print("Hand Control Mouse Started...")

import cv2
import mediapipe as mp
import pyautogui
import math
import time
# from playsound import playsound  # Optional: Uncomment if using sound

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

# Screen size
screen_w, screen_h = pyautogui.size()
dragging = False

def find_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def fingers_up(landmarks):
    tips = [8, 12, 16, 20]
    up = []
    for i in tips:
        up.append(landmarks[i].y < landmarks[i - 2].y)
    return up  # [Index, Middle, Ring, Pinky]

def get_label(handedness):
    try:
        return handedness.classification[0].label
    except:
        return None

cap = cv2.VideoCapture(0)
prev_pos = None
exiting = False

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            lm = hand_landmarks.landmark
            lm_list = [(int(l.x * w), int(l.y * h)) for l in lm]
            label = get_label(results.multi_handedness[idx])

            index_finger = lm_list[8]
            middle_finger = lm_list[12]
            thumb_tip = lm_list[4]

            fingers = fingers_up(lm)
            all_up = all(fingers)
            index_up, middle_up = fingers[0], fingers[1]
            ring_up, pinky_up = fingers[2], fingers[3]
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if all_up:
                continue  
            if index_up and middle_up:
                x, y = lm_list[8]
                screen_x = int(screen_w * lm[8].x)
                screen_y = int(screen_h * lm[8].y)
                pyautogui.moveTo(screen_x, screen_y)
                prev_pos = (screen_x, screen_y)
            elif not index_up and middle_up:
                pyautogui.click()
                pyautogui.sleep(0.3)
            elif index_up and not middle_up:
                pyautogui.click(button='right')
                pyautogui.sleep(0.3)
            elif not index_up and not middle_up:
                dist = find_distance(index_finger, middle_finger)
                if dist < 40:
                    pyautogui.doubleClick()
                    pyautogui.sleep(0.3)
            elif not index_up and not middle_up and not ring_up and not pinky_up:
                if not dragging:
                    dragging = True
                    pyautogui.mouseDown()
                if prev_pos:
                    pyautogui.moveTo(prev_pos[0], prev_pos[1])
            else:
                if dragging:
                    dragging = False
                    pyautogui.mouseUp()

            # Pinch Scroll (Left Hand)
            if label == "Left" and all(fingers[i] for i in [1, 2, 3]):
                pinch_dist = find_distance(index_finger, thumb_tip)
                if pinch_dist < 50:
                    diff = index_finger[1] - thumb_tip[1]
                    if diff > 10:
                        pyautogui.scroll(50)
                    elif diff < -10:
                        pyautogui.scroll(-50)
    cv2.putText(frame, "Hand Control - Press 'q' or Esc to Quit", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q') or key == 27:
        exiting = True
    if exiting:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, h//2 - 50), (w, h//2 + 50), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        cv2.putText(frame, "Exiting...", (w//2 - 100, h//2 + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
        cv2.imshow("AI Virtual Mouse", frame)
        print("Exit key (q or Esc) pressed. Exiting gracefully...")
        cv2.waitKey(1500)
        break
    cv2.imshow("AI Virtual Mouse", frame)
cap.release()
cv2.destroyAllWindows()
