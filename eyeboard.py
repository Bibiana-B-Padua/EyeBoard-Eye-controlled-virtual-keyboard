import cv2
import numpy as np
import dlib
from math import hypot
import pyglet

# Load sounds (ensure these files exist in your folder)
try:
    sound = pyglet.media.load("sound.wav", streaming=False)
    left_sound = pyglet.media.load("left.wav", streaming=False)
    right_sound = pyglet.media.load("right.wav", streaming=False)
except:
    print("Sound files not found. Continuing without audio.")

cap = cv2.VideoCapture(0) # Changed to 0 for default webcam
board = np.zeros((600, 1000), np.uint8) # Increased height for paragraphs
board[:] = 255

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:/Users/binoc/OneDrive/Desktop/Project/shape_predictor_68_face_landmarks.dat")

# Keyboard settings
keyboard = np.zeros((600, 1000, 3), np.uint8)
keys_set_1 = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T",
              5: "A", 6: "S", 7: "D", 8: "F", 9: "G",
              10: "Z", 11: "X", 12: "C", 13: "V", 14: "<"} # < is Backspace

keys_set_2 = {0: "Y", 1: "U", 2: "I", 3: "O", 4: "P",
              5: "H", 6: "J", 7: "K", 8: "L", 9: "_", # _ is Space
              10: "ENT", 11: "B", 12: "N", 13: "M", 14: "<"} # ENT is New Line

def draw_letters(letter_index, text, letter_light):
    x = (letter_index % 5) * 200
    y = (letter_index // 5) * 200
    width, height, th = 200, 200, 3

    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale, font_th = 4, 4 # Adjusted scale for "ENT" to fit
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    text_x = int((width - text_size[0]) / 2) + x
    text_y = int((height + text_size[1]) / 2) + y

    if letter_light:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
        cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
    else:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
        cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)

def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    return hor_line_lenght / ver_line_lenght

def get_gaze_ratio(eye_points, facial_landmarks, frame, gray):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[i]).x, facial_landmarks.part(eye_points[i]).y) for i in range(6)], np.int32)
    mask = np.zeros(gray.shape, np.uint8)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)
    min_x, max_x = np.min(left_eye_region[:, 0]), np.max(left_eye_region[:, 0])
    min_y, max_y = np.min(left_eye_region[:, 1]), np.max(left_eye_region[:, 1])
    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    h, w = threshold_eye.shape
    left_side = cv2.countNonZero(threshold_eye[0: h, 0: int(w / 2)])
    right_side = cv2.countNonZero(threshold_eye[0: h, int(w / 2): w])
    return left_side / right_side if right_side != 0 else 5

# Counters & Settings
frames, letter_index, blinking_frames = 0, 0, 0
frames_to_blink, frames_active_letter = 10, 18
text = ""
keyboard_selected = "left"
select_keyboard_menu = True
keyboard_selection_frames = 0
font = cv2.FONT_HERSHEY_PLAIN

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    keyboard[:] = (26, 26, 26)
    rows, cols, _ = frame.shape
    frames += 1

    if select_keyboard_menu:
        # Drawing simple Menu
        cv2.putText(keyboard, "LEFT", (50, 300), font, 5, (255, 255, 255), 5)
        cv2.putText(keyboard, "RIGHT", (550, 300), font, 5, (255, 255, 255), 5)

    keys_set = keys_set_1 if keyboard_selected == "left" else keys_set_2
    active_letter = keys_set[letter_index]

    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        blinking_ratio = (get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks) + 
                          get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)) / 2
        if blinking_ratio > 6:
           cv2.putText(frame, "BLINKING", (50, 150), font, 4, (255, 0, 0),thickness=3)
           blinking_frames += 1
           frames -= 1

        
        if select_keyboard_menu:
            gaze_ratio = (get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks, frame, gray) + 
                          get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks, frame, gray)) / 2
            
            if gaze_ratio <= 0.9:
                keyboard_selected = "right"
                keyboard_selection_frames += 1
            else:
                keyboard_selected = "left"
                keyboard_selection_frames += 1

            if keyboard_selection_frames == 30:
                select_keyboard_menu = False
                try: (right_sound if keyboard_selected == "right" else left_sound).play()
                except: pass
                frames = 0
                keyboard_selection_frames = 0
        else:
            if blinking_ratio > 5:
                blinking_frames += 1
                frames -= 1
                if blinking_frames == frames_to_blink:
                    if active_letter == "_": text += " "
                    elif active_letter == "<": text = text[:-1]
                    elif active_letter == "ENT": text += "\n"
                    else: text += active_letter
                    
                    try: sound.play()
                    except: pass
                    select_keyboard_menu = True
                    blinking_frames = 0
            else:
                blinking_frames = 0

    if not select_keyboard_menu:
        if frames == frames_active_letter:
            letter_index = (letter_index + 1) % 15
            frames = 0
        for i in range(15):
            draw_letters(i, keys_set[i], i == letter_index)

    # Paragraph Display Logic
    board[:] = 255
    lines = text.split("\n")
    for i, line in enumerate(lines):
        y_pos = 100 + (i * 80)
        cv2.putText(board, line, (50, y_pos), font, 4, 0, 3)

    # Visual loading bar
    loading_x = int(cols * (blinking_frames / frames_to_blink))
    cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (0, 255, 0), -1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Virtual keyboard", keyboard)
    cv2.imshow("Board", board)

    if cv2.waitKey(1) == 27: break

cap.release()
cv2.destroyAllWindows()
