import cv2
import mediapipe as mp
import serial
import time

# -------- SERIAL SETUP --------
# Change COM port according to your system
arduino = serial.Serial('COM5', 9600)
time.sleep(2)

# -------- MEDIAPIPE SETUP --------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

# Eye Aspect Ratio threshold
EAR_THRESHOLD = 0.20


def eye_aspect_ratio(landmarks, eye_indices):
    """Calculate Eye Aspect Ratio using Mediapipe landmarks."""
    p1 = landmarks[eye_indices[0]]
    p2 = landmarks[eye_indices[1]]
    p3 = landmarks[eye_indices[2]]
    p4 = landmarks[eye_indices[3]]
    p5 = landmarks[eye_indices[4]]
    p6 = landmarks[eye_indices[5]]

    # Vertical distances
    A = ((p2.x - p6.x) ** 2 + (p2.y - p6.y) ** 2) ** 0.5
    B = ((p3.x - p5.x) ** 2 + (p3.y - p5.y) ** 2) ** 0.5

    # Horizontal distance
    C = ((p1.x - p4.x) ** 2 + (p1.y - p4.y) ** 2) ** 0.5

    ear = (A + B) / (2.0 * C)
    return ear


# Mediapipe Eye Index Values
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not detected!")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # Calculate EAR values
            left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
            right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)

            # Eye state detection
            left_closed = left_ear < EAR_THRESHOLD
            right_closed = right_ear < EAR_THRESHOLD

            if left_closed and right_closed:
                command = "FORWARD"
            elif left_closed and not right_closed:
                command = "LEFT"
            elif right_closed and not left_closed:
                command = "RIGHT"
            else:
                command = "STOP"

            print("Command:", command)

            try:
                arduino.write(command.encode())
            except:
                print("Error sending command to Arduino.")

            time.sleep(0.1)

    cv2.imshow("Eye Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
arduino.close()