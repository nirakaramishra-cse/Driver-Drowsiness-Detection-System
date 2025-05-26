# Driver-Drowsiness-Detection-System

This project implements a **A Real-Time Driver Monitoring System** using computer vision and machine learning techniques. It monitors the driver's facial features in real-time to detect signs of drowsiness such as eye closure, yawning, and head pose. When drowsiness is detected, the system triggers audio alerts and desktop notifications to warn the driver.

## Features

- Real-time detection of eye closure (using Eye Aspect Ratio - EAR)
- Yawning detection (using Mouth Aspect Ratio - MAR)
- Head pose estimation to monitor driver’s attention
- Audible alerts using speech synthesis (gTTS)
- Desktop notifications for immediate alerts
- Night mode for better visibility during nighttime driving
- Event logging of detected drowsiness and yawning incidents
- Graphical User Interface (GUI) built with Tkinter for easy monitoring
- Rainbow-colored facial landmark visualization for clarity

---

## Requirements

Install the dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt 

```
