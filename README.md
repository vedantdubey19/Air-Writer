✨ Air Writer – Write in Air using Computer Vision

Air Writer is a computer vision-based application that allows users to write text in the air using hand gestures, which gets captured and displayed on the screen in real-time.

This project leverages OpenCV and hand tracking techniques to create a touchless writing experience — ideal for gesture-based interfaces, virtual drawing, and interactive systems.

⸻

🚀 Features
	•	✋ Real-time hand tracking
	•	✍️ Write in the air using finger movements
	•	🎯 Smooth drawing with gesture detection
	•	🧠 Intelligent tracking using computer vision
	•	🖥️ Live display of written strokes
	•	❌ Clear screen gesture / reset option

🛠️ Tech Stack
	•	Python
	•	OpenCV
	•	NumPy
	•	MediaPipe (for hand tracking)

⸻

📂 Project Structure
Air-Writer/
│── main.py              # Main application file
│── requirements.txt     # Dependencies
│── utils/               # Helper functions (if any)
│── README.md            # Project documentation



⸻

⚙️ Installation

1. Clone the repository
   git clone https://github.com/vedantdubey19/Air-Writer.git
cd Air-Writer


2. Create virtual environment (recommended)
   conda create -n airwriter python=3.9
conda activate airwriter

3. Install dependencies
   pip install -r requirements.txt

▶️ Usage

Run the application:
   python main.py

How it works:
	•	Show your hand in front of the camera
	•	Use your index finger to draw
	•	Move finger in the air → drawing appears on screen
	•	Use gestures to clear or control drawing

⸻

🧠 How It Works
	1.	Camera captures real-time video feed
	2.	Hand landmarks are detected using MediaPipe
	3.	Index finger position is tracked
	4.	Movement is converted into drawing strokes
	5.	Strokes are rendered on a virtual canvas

⸻

📸 Demo (Optional)

Add screenshots or GIFs here

⸻

🔮 Future Improvements
	•	✍️ Add text recognition (convert drawing → text)
	•	🎨 Multiple colors and brush sizes
	•	🧾 Save drawings as images
	•	🤖 Integrate AI handwriting recognition
	•	🕹️ Gesture-based UI controls

⸻

🤝 Contributing

Contributions are welcome!
	1.	Fork the repo
	2.	Create a new branch
	3.	Make your changes
	4.	Submit a pull request

⸻

📄 License

This project is licensed under the MIT License.

⸻

🙌 Author

Vedant Dubey
	•	💻 Aspiring Full Stack & AI/ML Developer
	•	🚀 Passionate about building real-world projects




