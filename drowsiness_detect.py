
import cv2
import dlib
import numpy as np
import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from scipy.spatial import distance as dist
from gtts import gTTS
from datetime import datetime
import time

# -------------------- Functions --------------------

def eye_aspect_ratio(eye):
    """Calculate Eye Aspect Ratio (EAR) to detect blinking/drowsiness."""
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[3], mouth[7])  # 63 - 67
    B = dist.euclidean(mouth[2], mouth[6])  # 62 - 66
    C = dist.euclidean(mouth[1], mouth[5])  # 61 - 65
    D = dist.euclidean(mouth[0], mouth[4])  # 60 - 64
    mar = (A + B + C) / (3.0 * D)
    return mar

def sound_alert(text):
    """Generate a speech alert using gTTS and play it."""
    tts = gTTS(text=text, lang='en')
    tts.save("alert.mp3")
    os.system("mpg123 alert.mp3")

def desktop_notification(title, message):
    """Send a desktop notification (Linux-based using notify-send)."""
    subprocess.Popen(['notify-send', title, message])

def hsv_to_rgb(h, s, v):
    """Convert HSV color values to RGB."""
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f * s))
    i = i % 6

    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)

def get_rainbow_color(t):
    """Generate a changing rainbow color based on time."""
    hue = (t % 1)
    saturation = 1.0
    value = 1.0
    return hsv_to_rgb(hue, saturation, value)

def update_gui(frame, ear_value, mar_value, status_text, head_pose_text):
    """Update the Tkinter GUI elements with new frame and stats."""
    if night_mode:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    else:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    ear_label.config(text=f"EAR: {ear_value:.3f}")
    mar_label.config(text=f"MAR: {mar_value:.3f}")
    status_label.config(text=f"Status: {status_text}")
    pose_label.config(text=f"Head Pose: {head_pose_text}")

    root.update()

def log_event(status, head_pose):
    """Log detection events into listbox and CSV file."""
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    alerts_listbox.insert(0, f"[{current_time}] {status} | {head_pose}")
    with open("drowsiness_log.csv", "a") as f:
        f.write(f"{current_time}, {status}, {head_pose}\n") 

def toggle_night_mode():
    """Toggle night mode ON/OFF."""
    global night_mode
    night_mode = not night_mode

# -------------------- Drowsiness Detection --------------------

def detect_drowsiness():
    """Main loop for detecting drowsiness and head pose."""
    global COUNTER, YAWAN_COUNTER, last_alert_time
    current_time = time.time()

    ret, frame = cap.read()
    if not ret:
        root.after(10, detect_drowsiness)
        return

    size = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    status_text = "Normal"
    head_pose_text = "Normal"

    t = (current_time % 1)
    rainbow_color = get_rainbow_color(t)
    
    for rect in rects:
        shape = predictor(gray, rect)

        # Get inner mouth coordinates (landmark 60–67)
        mouth = np.array([(shape.part(i).x, shape.part(i).y) for i in range(60, 68)], np.int32)
        MAR = mouth_aspect_ratio(mouth)
        
        # Get eye coordinates
        leftEye = np.array([(shape.part(i).x, shape.part(i).y) for i in range(36, 42)], np.int32)
        rightEye = np.array([(shape.part(i).x, shape.part(i).y) for i in range(42, 48)], np.int32)

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        EAR = (leftEAR + rightEAR) / 2.0

        # Detect drowsiness
        if EAR < EAR_THRESHOLD:
            COUNTER += 1
            if COUNTER >= EAR_CONSEC_FRAMES:
                status_text = "Drowsy"
        else:
            COUNTER = 0

        if MAR > MAR_THRESHOLD:
            YAWAN_COUNTER += 1
            if YAWAN_COUNTER >= YAWN_CONSEC_FRAMES:
                status_text = "Yawning"
        else:
            YAWAN_COUNTER = 0    

        # Head pose estimation
        model_points = np.array([
            (0.0, 0.0, 0.0),
            (0.0, -330.0, -65.0),
            (-225.0, 170.0, -135.0),
            (225.0, 170.0, -135.0),
            (-150.0, -150.0, -125.0),
            (150.0, -150.0, -125.0)
        ], dtype="double")

        image_points = np.array([
            (shape.part(30).x, shape.part(30).y),
            (shape.part(8).x, shape.part(8).y),
            (shape.part(36).x, shape.part(36).y),
            (shape.part(45).x, shape.part(45).y),
            (shape.part(48).x, shape.part(48).y),
            (shape.part(54).x, shape.part(54).y)
        ], dtype="double")

        focal_length = size[1]
        center = (size[1] / 2, size[0] / 2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )
        dist_coeffs = np.zeros((4, 1))

        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
        )

        rvec_matrix, _ = cv2.Rodrigues(rotation_vector)
        pose_mat = cv2.hconcat((rvec_matrix, translation_vector))
        _, _, _, _, _, _, eulerAngles = cv2.decomposeProjectionMatrix(pose_mat)

        pitch, yaw, roll = eulerAngles.flatten()

        # if pitch > :
        #     head_pose_text = "Nodding Up"
        if pitch < -15:
            head_pose_text = "Nodding Down"    
        elif yaw > 20:
            head_pose_text = "Looking Right"
        elif yaw < -20:
            head_pose_text = "Looking Left"
        elif roll > 15:
            head_pose_text = "Tilting Left"
        elif roll < -15:
            head_pose_text = "Tilting Right"
        else:
            head_pose_text = "Facing Forward"

        # Draw facial landmarks with rainbow color
        for i in range(68):
            x, y = shape.part(i).x, shape.part(i).y
            color = tuple(int(c * 255) for c in rainbow_color)
            cv2.circle(frame, (x, y), 2, color, -1)

    # Update GUI
    update_gui(frame, EAR if rects else 0.0, MAR if rects else 0.0, status_text, head_pose_text)

    # Send alerts if status is abnormal and enough time has passed
    if (status_text != "Normal") and (time.time() - last_alert_time > alert_cooldown):
        threading.Thread(target=sound_alert, args=("Stay alert! Drowsiness Detected!, Please take a break!",)).start()
        desktop_notification("Driver Alert", f"{status_text} | {head_pose_text}")
        log_event(status_text, head_pose_text)
        last_alert_time = time.time()

    if (head_pose_text == "Normal") and (time.time() - last_alert_time > alert_cooldown):
        threading.Thread(target=sound_alert, args=("Stay alert! You are Sleeping, Please wake up!",)).start()
        desktop_notification("Driver Alert", "You are slepping")
        last_alert_time = time.time()    

    elif (head_pose_text != "Facing Forward") and (time.time() - last_alert_time > alert_cooldown):
        threading.Thread(target=sound_alert, args=("Stay alert! Your Facing not Forward!, Please Look forward!",)).start()
        desktop_notification("Driver Alert", f"{status_text} | {head_pose_text}")
        log_event(status_text, head_pose_text)
        last_alert_time = time.time()    

    root.after(10, detect_drowsiness)

# -------------------- Main Program --------------------

# Initialize GUI
root = tk.Tk()
root.title("Driver Drowsiness Detection Dashboard")

video_label = tk.Label(root)
video_label.pack()

info_frame = tk.Frame(root)
info_frame.pack(pady=10)

ear_label = tk.Label(info_frame, text="EAR: --", font=("Arial", 14))
ear_label.grid(row=0, column=0, padx=10)

mar_label = tk.Label(info_frame, text="MAR: --", font=("Arial", 14))
mar_label.grid(row=0, column=1, padx=10)

status_label = tk.Label(info_frame, text="Status: --", font=("Arial", 14))
status_label.grid(row=0, column=2, padx=10)

pose_label = tk.Label(info_frame, text="Head Pose: --", font=("Arial", 14))
pose_label.grid(row=0, column=3, padx=10)

alerts_listbox = tk.Listbox(root, width=80, height=8)
alerts_listbox.pack(pady=10)

# Night mode toggle button
toggle_button = ttk.Button(root, text="Toggle Night Mode", command=toggle_night_mode)
toggle_button.pack(pady=5)

# Load models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Thresholds and counters eyr
EAR_THRESHOLD = 0.25
EAR_CONSEC_FRAMES = 15
COUNTER = 0

# Thresholds and counters mouth
MAR_THRESHOLD = 0.5
YAWN_CONSEC_FRAMES = 15
YAWAN_COUNTER = 0

# Night mode flag
night_mode = False

# Cooldown between alerts (seconds)
alert_cooldown = 10
last_alert_time = 0

# Start Video Capture
cap = cv2.VideoCapture(0)

# Start detection loop
root.after(10, detect_drowsiness)
root.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), root.destroy()))
root.mainloop()

