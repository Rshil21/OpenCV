# Gesture-Based Game Controller using OpenCV + MediaPipe

Control your favorite PC games with just your hand gestures!  
This project uses **OpenCV**, **MediaPipe**, and **PyAutoGUI** to detect real-time hand gestures via webcam and simulate keyboard actions.

---

##  Features

✅ Detects real-time hand gestures from webcam  
✅ Recognizes:
- **Fist** → `Ctrl` (attack)
- **Open Palm** → `Space` (jump)
- **Pointing Finger** → `W` (move forward)
- **Thumbs Up** → `E` (special action)

✅ Sends keyboard inputs to active window  
✅ Compatible with most PC games using keyboard controls  
✅ Lightweight, no hardware required beyond a webcam

---

## Tech Stack

- **Python**
- **OpenCV** – Image processing & webcam feed
- **MediaPipe** – Hand landmark detection
- **PyAutoGUI** – Simulates keyboard presses
- **NumPy** – For gesture logic & landmark analysis

---

## Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/gesture-game-controller-opencv.git
   cd gesture-game-controller-opencv
2. Install dependencies:
   pip install -r requirements.txt
3. Run the controller:
   python main.py
4. Make gestures in front of your webcam and watch them trigger game actions!
   
