# 🚘 Driver-Drowsiness-Detection-System


## 📝 Overview

This project implements a **Real-Time Driver Monitoring System** using computer vision and machine learning techniques. It monitors the driver's facial features in real time to detect signs of drowsiness such as eye closure, yawning, and head pose estimation. When drowsiness is detected, the system triggers **audible alerts** and **desktop notifications** to warn the driver (🚗 💤 🔔).


## ✨ Key Features 

- **Real-time Eye Closure Detection:**  
  Utilizes Eye Aspect Ratio (EAR) to monitor eye closure and detect potential drowsiness.

- **Yawning Detection:**  
  Implements Mouth Aspect Ratio (MAR) to identify yawning, a sign of driver fatigue.

- **Head Pose Estimation:**  
  Tracks head tilts and nods to monitor driver attention and detect distraction.

- **Audible Alerts:**  
  Generates speech-based alerts using the gTTS library to immediately warn the driver.

- **Desktop Notifications:**  
  Provides instant visual alerts on the desktop to notify the driver of drowsiness or yawning events.

- **Night Mode:**  
  Offers an improved visibility mode for nighttime driving to reduce eye strain.

- **Event Logging:**  
  Records detailed logs of detected drowsiness and yawning incidents for analysis.

- **Graphical User Interface (GUI):**  
  Built with Tkinter for intuitive real-time monitoring and control.

- **Rainbow-colored Facial Landmark Visualization:**  
  Displays facial landmarks with distinct colors for clear and precise detection.


![Alt Text](https://github.com/nirakaramishra-cse/Driver-Drowsiness-Detection-System/blob/3fae871cc184f57e0d3cf1f26066d78c7103b192/Key%20Features.png).

---


## 💻 Technologies Used

### Programming Languages & Libraries:
- Python 🐍 (develop the system)
- OpenCV 📷 (real-time image processing)
- Dlib 🖼️ (for face detection)
- Numpy 🔢 (For numerical operations)
- gTTS 🔊 (for speech alerts)
- Tkinter 🖥️ (for GUI)


![Alt Text](https://github.com/nirakaramishra-cse/Driver-Drowsiness-Detection-System/blob/3fae871cc184f57e0d3cf1f26066d78c7103b192/Technologies.png)

---


## 🔍 How It Works

**Eye Aspect Ratio (EAR):**
Calculates the ratio of distances between vertical and horizontal eye landmarks. Low EAR indicates closed eyes.

**Mouth Aspect Ratio (MAR):**
Measures mouth openness to detect yawning.

**Head Pose Estimation:**
Uses a 3D model of facial landmarks and OpenCV’s solvePnP function to estimate the head’s rotation angles (pitch, yaw, roll).

**Alerts:**
When EAR or MAR thresholds are crossed consecutively over several frames, audio alerts and desktop notifications are triggered.

**Event Logging:**
Each alert event (sleepiness or yawning) is timestamped and saved to a CSV log file.


## ⚙️ Configuration

- You can adjust the following parameters in the script:
  
| Parameter            | Description                                                 | Default Value |
| -------------------- | ----------------------------------------------------------- | ------------- |
| `EAR_THRESHOLD`      | Threshold below which eyes are considered closed            | 0.25          |
| `EAR_CONSEC_FRAMES`  | Number of consecutive frames with low EAR to trigger alert  | 20            |
| `MAR_THRESHOLD`      | Threshold above which mouth is considered yawning           | 0.75          |
| `YAWN_CONSEC_FRAMES` | Number of consecutive frames with high MAR to trigger alert | 15            |
| `alert_cooldown`     | Cooldown time (seconds) between alerts to avoid spamming    | 5             |


## 🖥️ GUI Dashboard

#### Real-Time Video Feed:
- See live video feed with EAR, yawning status, and head pose.

#### Visual Feedback:
- Display current EAR value, MAR value, Drowsiness status, and Head position.
- Alerts listbox with detected events, date and timestamps.


![Alt Text](https://github.com/nirakaramishra-cse/Driver-Drowsiness-Detection-System/blob/3fae871cc184f57e0d3cf1f26066d78c7103b192/GUI%20Dashboard.png)

---


## 🧪 Test Results

- **✅ Face Detection:** 95% accurate; occasional false negatives and rare false positives.

- **✅ Facial Landmarks:** 98% accuracy; 0.5s/frame latency.

- **✅ EAR & MAR:** 92% accuracy for eye closure, 90% for yawning detection.

- **✅ Alerts:** 100% correct speech alerts, real-time visual alerts.

- **✅ Head Pose:** 93% tilt detection (>30°), 95% yawning detection.

- **✅ Performance:** 25–30 FPS, 40% CPU, 2GB RAM usage.


![Alt Text](https://github.com/nirakaramishra-cse/Driver-Drowsiness-Detection-System/blob/3fae871cc184f57e0d3cf1f26066d78c7103b192/Results.png)

---


## 🛠️ Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/nirakaramishra-cse/Driver-Drowsiness-Detection-System.git
    cd Driver-Drowsiness-Detection-System
    ```

2. Install the dependencies from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt 
    ```


## 🚀 Usage

* Run the following command to start the system:
    ```bash
    python drowsiness_detection.py
    ```
