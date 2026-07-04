print("Eye Control Mouse Started...")
import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

screen_w, screen_h = pyautogui.size()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
mp_drawing = mp.solutions.drawing_utils

BLINK_RATIO_THRESHOLD = 5.0
DOUBLE_BLINK_TIME = 0.4

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
LEFT_IRIS = [468]
RIGHT_IRIS = [473]

last_blink_time = 0
blink_count = 0
double_blink_active = False

# Utils for blink detection
def get_blink_ratio(eye_points, landmarks, image_w, image_h):
    top = np.linalg.norm(
        np.array([
            landmarks[eye_points[1]].x * image_w,
            landmarks[eye_points[1]].y * image_h
        ]) -
        np.array([
            landmarks[eye_points[5]].x * image_w,
            landmarks[eye_points[5]].y * image_h
        ])
    )
    left_right = np.linalg.norm(
        np.array([
            landmarks[eye_points[0]].x * image_w,
            landmarks[eye_points[0]].y * image_h
        ]) -
        np.array([
            landmarks[eye_points[3]].x * image_w,
            landmarks[eye_points[3]].y * image_h
        ])
    )
    ratio = left_right / top if top != 0 else 0
    return ratio

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        mesh = results.multi_face_landmarks[0].landmark
        left_ratio = get_blink_ratio(LEFT_EYE, mesh, w, h)
        right_ratio = get_blink_ratio(RIGHT_EYE, mesh, w, h)
        left_blink = left_ratio > BLINK_RATIO_THRESHOLD
        right_blink = right_ratio > BLINK_RATIO_THRESHOLD
        iris = mesh[LEFT_IRIS[0]]
        x = int(iris.x * screen_w)
        y = int(iris.y * screen_h)
        pyautogui.moveTo(x, y, duration=0.05)
        current_time = time.time()
        if left_blink and right_blink:
            if current_time - last_blink_time < DOUBLE_BLINK_TIME:
                blink_count += 1
            else:
                blink_count = 1
            last_blink_time = current_time

            if blink_count == 2:
                pyautogui.doubleClick()
                blink_count = 0
                print("Double Clicked")
        elif left_blink and not right_blink:
            pyautogui.click(button='left')
            print("Left Click")
            time.sleep(0.3)
        elif right_blink and not left_blink:
            pyautogui.click(button='right')
            print("Right Click")
            time.sleep(0.3)
    cv2.putText(frame, "Eye Controlled Mouse - Press 'Esc' or 'q' to Quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Eye Mouse", frame)
    key = cv2.waitKey(5) & 0xFF
    if key in [27, ord('q')]:
        print("Exit key pressed; quitting.")
        break
cap.release()
cv2.destroyAllWindows()
