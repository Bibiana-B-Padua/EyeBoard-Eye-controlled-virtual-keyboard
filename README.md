# EyeBoard – Empowering Communication Through Eye Control

EyeBoard is an assistive technology system that enables **hands‑free typing using eye movements and blinking**. Designed for individuals with severe motor disabilities, it provides an affordable, accessible, and user‑friendly communication solution using standard webcams and open‑source tools.

---

## ✨ Features
- **Hands‑Free Communication**: Text input via eye gaze and blink detection.  
- **Low‑Cost Setup**: Works with standard webcams, no specialized hardware required.  
- **Computer Vision Powered**: Uses OpenCV, dlib, and MediaPipe for facial landmark detection and gaze tracking.  
- **Virtual Keyboard UI**: Built with Tkinter/PyGame, supports space, backspace, and enter keys.  
- **Audio Feedback**: Pyglet integration for sound cues during key selection.  
- **Optional TTS Output**: Converts typed text into speech for enhanced accessibility.  

---

## 🏗️ System Architecture
1. **Video Capture** – Real‑time frame acquisition (OpenCV).  
2. **Face & Landmark Detection** – dlib/MediaPipe for 68‑point facial landmarks.  
3. **Eye ROI Extraction** – Isolates eye region for blink/gaze analysis.  
4. **Blink Detection** – Eye Aspect Ratio (EAR) thresholding for key selection.  
5. **Gaze Estimation** – Pupil position & pixel ratio for navigation.  
6. **Virtual Keyboard UI** – Interactive layouts with automatic highlighting.  
7. **Text Output Buffer** – Displays typed text and supports optional TTS.  

---

## 📂 Modules
- **Computer Vision**: Face detection, landmark extraction, blink & gaze tracking.  
- **Interaction**: Blink‑based character selection, gaze‑based keyboard switching.  
- **User Interface**: Virtual keyboard, text display, audio feedback.  

---

## 🚀 Implementation Highlights
- **Blink Detection**: EAR‑based threshold logic for intentional blinks.  
- **Gaze Detection**: Eye region analysis for left/right navigation.  
- **Keyboard Setup**: Dual layouts with highlighted keys for easy selection.  

---

## 📊 Results
- Successfully demonstrated **real‑time blink and gaze detection**.  
- Achieved smooth text entry with minimal delay.  
- Verified outputs through debug console and keyboard selection tests.  

---

## 🔮 Future Work
- Adaptive thresholding for varied lighting conditions.  
- Word prediction & auto‑completion.  
- Multi‑language support.  
- Mobile/embedded system integration.  
- Voice output for visually impaired users.  

---

## 📜 Conference Publication
- **Conference**: ICSTS 2025  
- **Paper Title**: *EyeBoard – A Low‑Cost Eye‑Controlled Virtual Keyboard for Hands‑Free Communication Using Standard Webcams*  

---

## ⚙️ Tech Stack
- **Languages**: Python  
- **Libraries**: OpenCV, dlib, MediaPipe, Tkinter, PyGame, Pyglet, PyAutoGUI  

---

## 📚 References
1. Verdzekov et al., *Multi‑stage gaze‑controlled virtual keyboard using eye tracking*, PLOS ONE, 2024.  
2. Panwar et al., *EyeBoard: A fast and accurate eye gaze‑based text entry system*, IJHCI, 2022.  
3. Islam & Rahman, *Computer vision‑based eye gaze controlled virtual keyboard for people with quadriplegia*, IEEE ICCCNT, 2020.  
4. Falch & Lohan, *Webcam‑based gaze estimation using CNN techniques*, ACM ETRA, 2018.  

---

## 📥 Getting Started
```bash
# Clone the repository
git clone https://github.com/yourusername/eyeboard.git

# Navigate to project directory
cd eyeboard

# Install dependencies
pip install -r requirements.txt

Download the dlib facial landmark model:
shape_predictor_68_face_landmarks.dat (dlib.net in Bing)  
Extract and place it in the models/ folder.

# Run the application
python eyeboard.py
```
