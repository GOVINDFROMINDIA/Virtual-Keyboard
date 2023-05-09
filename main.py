import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# define the keys on the keyboard
"""keys = {'`': (30,50), '1': (100, 50), '2': (200, 50), '3': (300, 50), '4': (400, 50),
        '5': (500, 50), '6': (600, 50), '7': (700, 50), '8': (800, 50), '9': (900, 50),
        '0': (1000, 50), '-': (1100, 50), '=': (1200, 50),
        'Q': (175, 100), 'W': (275, 100), 'E': (375, 100), 'R': (475, 100), 'T': (575, 100),
        'Y': (675, 100), 'U': (775, 100), 'I': (875, 100), 'O': (975, 100), 'P': (1075, 100),
        '[': (1175, 200), ']': (1275, 200), '\\': (1375, 200),
        'A': (225, 300), 'S': (325, 300), 'D': (425, 300), 'F': (525, 300), 'G': (625, 300),
        'H': (725, 300), 'J': (825, 300), 'K': (925, 300), 'L': (1025, 300),
        ';': (1125, 300), "'": (1225, 300),
        'Z': (275, 400), 'X': (375, 400), 'C': (475, 400), 'V': (575, 400), 'B': (675, 400),
        'N': (775, 400), 'M': (875, 400), ',': (975, 400), '.': (1075, 400), '/': (1175, 400),
        ' ': (525, 500)}"""
keys_set_1 = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8", 8: "9", 9: "0", 10: "CL", 11: "ENT"}
keys_set_2 = {0: "q", 1: "w", 2: "e", 3: "r", 4: "t", 5: "y", 6: "u", 7: "i", 8: "o", 9: "p", 10: "DEL"}
keys_set_3 = {0: "a", 1: "s", 2: "d", 3: "f", 4: "g", 5: "h", 6: "j", 7: "k", 8: "l", 9: ".", 10: "CAPS"}
keys_set_4 = {0: "SHIFT", 1: "z", 2: "x", 3: "c", 4: "v", 5: "b", 6: "n", 7: "m", 8: ",", 9: ".", 10: "?"}

keys = [keys_set_1, keys_set_2, keys_set_3, keys_set_4]


# define the keys that are numbers and symbols
"""num_keys = {'`': True, '1': True, '2': True, '3': True, '4': True,
            '5': True, '6': True, '7': True, '8': True, '9': True,
            '0': True, '-': True, '=': True,
            '[': True, ']': True, '\\': True,
            ';': True, "'": True,
            ',': True, '.': True, '/': True}"""

# define the keys that are alphabets
"""alpha_keys = {k: False for k in keys}
for k in num_keys:
    alpha_keys.pop(k, None)"""
# capture video from the default camera
cap = cv2.VideoCapture(1)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = cv2.flip(frame, 1)
        # convert to RGB for Mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # detect hand landmarks using Mediapipe
        results = hands.process(image)

        # get the coordinates of the fingertips
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 8:
                        # determine which key the fingertip is closest to
                        closest_key = None
                        closest_distance = float('inf')
                        for k, pos in keys.items():
                            distance = ((cx - pos[0]) * 2 + (cy - pos[1]) * 2) ** 0.5
                            if distance < complex(closest_distance):
                                closest_distance = distance
                                closest_key = k
                        # highlight the selected key
                        cv2.circle(frame, pos, 30, (0, 255, 0), -1)

        # display the keyboard
        """for k, pos in keys.items():
            cv2.putText(frame, k, pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)"""
        key_width = 50
        key_height = 50
        x_start = 10
        y_start = 100
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        for i in range(len(keys)):
            for j in range(len(keys[i])):
                x = x_start + j*key_width
                y = y_start + i*key_height
                #cv2.rectangle(frame, (x, y), (x+key_width, y+key_height), (255, 255, 255), 2)
                cv2.putText(frame, keys[i][j], (x+10, y+40), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

        # show the frame
        cv2.imshow('Virtual Keyboard', frame)

        # exit on ESC
        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()