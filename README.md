# 🖐️ Gesture-Based Mouse Control

A Python project that lets you control your mouse cursor using hand gestures — no extra hardware, just your webcam.  
Built using **MediaPipe**, **OpenCV**, and **pynput**.

---

## 🎯 Features

- Cursor movement using index finger  
- Left-click by pinching thumb + index finger  
- Right-click by pinching thumb + middle finger  
- Real-time hand landmark tracking  
- Smooth mouse movement with threading and cooldowns

---

## 📚 What I Learned

- How to detect hands and landmarks using MediaPipe  
- Real-time video processing with OpenCV  
- Simulating mouse actions using `pynput`  
- Gesture recognition using fingertip distances  
- Using multithreading to keep UI responsive  

---

## 🧠 How It Works

- Captures video from webcam  
- Detects hand and finger positions using MediaPipe  
- Tracks specific landmarks like index, thumb, and middle finger  
- Calculates distance between landmarks to detect gestures  
- Maps finger position to screen coordinates  
- Moves cursor or clicks based on the gesture  

---

## 🛠️ Tech Stack

- Python 3  
- OpenCV  
- MediaPipe  
- pynput  
- threading

---

## 🎥 Demo

[🔗 Add demo video link here — YouTube or Google Drive]

---

## 🚀 How to Run

1. Clone this repository  
2. Install the required libraries: pip install opencv-python mediapipe pynput
3. Run `HandTrackingCode.py`  
4. Allow webcam access  
5. Use gestures to control the mouse



