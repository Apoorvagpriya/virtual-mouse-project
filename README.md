# AI Virtual Mouse

A multi-modal, contactless virtual mouse that lets you control your computer using **hand gestures**, **eye/blink tracking**, and **voice commands** — no physical mouse required. Built with OpenCV and MediaPipe for computer vision, PyAutoGUI for system control, and a PHP + MySQL backend for usage logging and a dashboard view.

Designed with accessibility in mind — a flexible alternative to a traditional mouse for users with mobility impairments, and a fun demo of real-time computer vision otherwise.

## Features

**🖐️ Hand Control (`hand_control.py`)**
- Move the cursor by pointing with your index finger
- Left click, right click, and double click via finger gestures
- Click-and-drag support
- Two-finger pinch scrolling (left hand)

**👁️ Eye Control (`eye_control.py`)**
- Cursor follows iris position via MediaPipe Face Mesh
- Left/right click via single-eye blinks
- Double blink for a double click

**🎙️ Voice Assistant (`voice_assistant.py`)**
- Wake word ("hello") to activate listening
- Opens common apps (Chrome, Word, Excel, Paint, Spotify, File Explorer) by voice
- Tells the current time, exits on command

**🖥️ Launcher GUI (`launcher_gui.py`)**
- Desktop control panel (Tkinter) to start/stop each module
- Image carousel and card-based mode selection
- Logs every mode selection/start/stop to the backend for usage tracking

**📊 Backend Dashboard (PHP + MySQL)**
- REST-style API to log and fetch usage events (`log_action.php`, `get_actions.php`)
- Health check endpoint (`health.php`)
- Simple dashboard (`index.php`) showing latest activity and recent action history

## Tech Stack

| Layer | Technology |
|---|---|
| Computer Vision | OpenCV, MediaPipe |
| System Control | PyAutoGUI |
| Desktop GUI | Tkinter, ttkthemes, Pillow |
| Voice | SpeechRecognition, pyttsx3, PyAudio |
| Backend API | PHP, MySQL (mysqli) |
| Dashboard UI | Bootstrap 5 |

## Project Structure

```
virtual_mouse_project_with_backend/
├── virtual_mouse_project/
│   ├── launcher_gui.py       # Main GUI entry point
│   ├── hand_control.py       # Hand gesture module
│   ├── eye_control.py        # Eye/blink tracking module
│   ├── voice_assistant.py    # Voice command module
│   ├── eye.png / hand.png / voice.png   # Carousel images
└── backend/
    ├── schema.sql             # MySQL schema (creates `actions` table)
    ├── api/
    │   ├── config.php         # DB connection + CORS headers
    │   ├── log_action.php     # POST — logs a module event
    │   ├── get_actions.php    # GET  — fetches recent events
    │   └── health.php         # GET  — health check
    └── dashboard/
        └── index.php          # Usage dashboard UI
```

## Setup

### 1. Python environment

```bash
cd virtual_mouse_project_with_backend/virtual_mouse_project
python -m venv venv
venv\Scripts\activate        # Windows
pip install opencv-python mediapipe pyautogui numpy pillow ttkthemes requests SpeechRecognition pyttsx3 pyaudio
```

> `pyaudio` can be tricky to install on Windows via pip. If it fails, install the matching wheel from [pypi.org/project/PyAudio](https://pypi.org/project/PyAudio/) or use `pipwin install pyaudio`.

### 2. Backend (PHP + MySQL)

1. Install [XAMPP](https://www.apachefriends.org/) or [WAMP](https://www.wampserver.com/) and place the `backend/` folder inside `htdocs/virtual_mouse_project_with_backend/`.
2. Start Apache and MySQL.
3. Import `backend/schema.sql` into MySQL to create the `virtual_mouse` database and `actions` table.
4. Verify the API is up: visit `http://localhost/virtual_mouse_project_with_backend/backend/api/health.php`
5. View the dashboard: `http://localhost/virtual_mouse_project_with_backend/backend/dashboard/index.php`

### 3. Run it

```bash
python launcher_gui.py
```

Pick a mode from the launcher — each one runs independently and logs its start/stop events to the dashboard.

## ⚠️ Known Limitations

- **Hardcoded file paths**: `launcher_gui.py` currently points to local image paths (`C:\Users\...\Desktop\virtual_mouse_project\...`) and `voice_assistant.py` hardcodes app install paths (Chrome, Excel, Word, Spotify). Update these to match your own machine, or better, switch to relative paths before sharing/running on another PC.
- **Windows-only voice assistant**: app-opening commands use Windows-specific paths (`os.startfile`).
- **Single-user, local-only backend**: the API assumes `localhost` and has no authentication — fine for a demo/project, not production-ready as-is.
- **Lighting/webcam dependent**: hand and eye tracking accuracy depends on lighting conditions and webcam quality.

## Team

Developed as a project by:
- Yuvasree M-E5223019
- Apoorva-E5223012

## License


