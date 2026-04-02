# Air Glitter ✨

An interactive, anti-gravity neon particle drawing application powered by Python and Google's MediaPipe machine learning library. Wave your hand in the air like a wand to sketch beautiful, fading, physics-based neon trails.

## 🚀 Features

- **Real-Time Hand Tracking:** Utilizes the lightweight `mediapipe.tasks.vision` API natively on your CPU for sub-millisecond, highly-stable finger indexing.
- **Physics Engine:** Custom Numpy Anti-gravity particle system so your sparks naturally float upwards (or downwards!) with dynamic momentum and decay.
- **Open Palm Eraser:** Simply extend all your fingers into an open palm pose to instantly transform your glowing brush into a massive canvas eraser—pure magic!
- **Glowing Graphics:** Core additive-blending architecture utilizing deep OpenCV float matrices and Gaussian blurring to create realistic, vibrant, additive neon effects.
- **Customization Options:** Seamless, hot-swappable color palettes, brush sizes, and gravity toggles built elegantly into the interface.

## 🛠 Installation

Ensure you have Python 3 installed on your machine. We recommend setting up a virtual environment.

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/air-glitter.git
cd air-glitter

# 2. Setup your virtual environment
python -m venv venv
source venv/bin/activate  # Or `venv\Scripts\activate` on Windows

# 3. Install Python requirements
pip install -r requirements.txt
```

## 🎮 Running the Application

Boot the desktop app directly from your terminal:
```bash
python main.py
```
*(Note: On initialization, the script will rapidly download a simple ~3MB MediaPipe tracking model to your directory.)*

## ⌨️ Controls

- **Draw:** Point with your index finger.
- **Erase:** Hold up an open Hand (Palm).
- **`e` Key:** Toggle the finger eraser brush manually.
- **`c` Key:** Instantly clear the canvas.
- **`ESC` Key:** Shut down the application and disable the camera.
- *Use your mouse pointer at the bottom of the screen to change your neon palette, brush size, or reverse particle gravity!*
