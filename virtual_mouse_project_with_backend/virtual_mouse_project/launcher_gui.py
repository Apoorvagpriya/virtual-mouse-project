import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import subprocess
import threading
import requests
import os

# === Backend Config ===
BASE_URL = "http://127.0.0.1/virtual_mouse_project_with_backend/backend/api"
LOG_URL = f"{BASE_URL}/log_action.php"

def log_action(module, action="select", meta=None, timeout=2):
    """Send a POST to PHP backend. Non-blocking fire-and-forget."""
    payload = {"module": module, "action": action}
    if meta is not None:
        payload["meta"] = meta
    try:
        threading.Thread(
            target=lambda: requests.post(LOG_URL, json=payload, timeout=timeout),
            daemon=True
        ).start()
    except Exception as e:
        print("Log failed:", e)

def run_local_module(script_name, module_name):
    """Run local Python script and log start/stop events."""
    if not os.path.exists(script_name):
        print(f"Script not found: {script_name}")
        return None

    try:
        proc = subprocess.Popen(["python", script_name])
        # log start
        log_action(module_name, "start", meta={"pid": proc.pid})

        # log stop when process exits
        def watch(p):
            p.wait()
            log_action(module_name, "stop", meta={"pid": p.pid})
        threading.Thread(target=lambda: watch(proc), daemon=True).start()
        return proc
    except Exception as e:
        print("Failed to run", script_name, ":", e)
        return None

# === Launch Functions with logging ===
def launch_eye_control():
    log_action("eye", "select", meta={"ui": "launcher"})
    run_local_module("eye_control.py", "eye")

def launch_hand_control():
    log_action("hand", "select", meta={"ui": "launcher"})
    run_local_module("hand_control.py", "hand")

def launch_voice_assistant():
    log_action("voice", "select", meta={"ui": "launcher"})
    run_local_module("voice_assistant.py", "voice")

# === Carousel Function ===
def update_carousel():
    global carousel_index
    carousel_index = (carousel_index + 1) % len(carousel_images)
    img_label.config(image=carousel_images[carousel_index])
    root.after(4000, update_carousel)

# === Root Window ===
root = ThemedTk(theme="arc")
root.title("Virtual Control Hub")
root.geometry("1000x780")
root.resizable(False, False)

# === Gradient Background ===
gradient = tk.Canvas(root, width=1000, height=780)
gradient.pack(fill="both", expand=True)

for i in range(0, 780):
    r = int(240 - i * 0.1)
    g = int(245 - i * 0.15)
    b = int(255 - i * 0.3)
    color = f"#{r:02x}{g:02x}{b:02x}"
    gradient.create_line(0, i, 1000, i, fill=color)

# === Navbar ===
navbar = tk.Frame(root, bg="#343a40", height=50)
navbar.place(relwidth=1, y=0)

tk.Label(navbar, text="  Virtual Control Hub", fg="white", bg="#343a40",
         font=("Segoe UI", 16, "bold"), anchor="w").pack(side="left", padx=20)

for name in ["Home", "About", "Contact"]:
    tk.Button(navbar, text=name, bg="#343a40", fg="white", bd=0, activebackground="#495057",
              font=("Segoe UI", 10)).pack(side="right", padx=10)

# === Carousel Section ===
carousel_frame = tk.Frame(root, bg="", pady=10)
carousel_frame.place(x=20, y=60)

img_paths = [
    r"C:\Users\yuvas\Desktop\virtual_mouse_project\eye.png",
    r"C:\Users\yuvas\Desktop\virtual_mouse_project\hand.png",
    r"C:\Users\yuvas\Desktop\virtual_mouse_project\voice.png"
]

carousel_images = []
for path in img_paths:
    try:
        img = Image.open(path).resize((960, 270))
    except:
        img = Image.new("RGB", (960, 270), color=(200, 200, 200))
    carousel_images.append(ImageTk.PhotoImage(img))

carousel_index = 0
img_label = tk.Label(carousel_frame, image=carousel_images[carousel_index], bd=0)
img_label.pack()
root.after(4000, update_carousel)

# === Section Title ===
section_title = tk.Label(root, text="Choose Your Control Mode",
                         font=("Segoe UI", 17, "bold"), bg="#e3f2fd", fg="#212529", pady=10)
section_title.place(relx=0.5, y=350, anchor="center")

# === Cards Section ===
card_frame = tk.Frame(root, bg="")
card_frame.place(relx=0.5, y=460, anchor="center")

def create_card(parent, title, desc, features, command, bg_color, fg_color):
    frame = tk.Frame(parent, bg=bg_color, width=280, height=240, bd=0, highlightbackground=fg_color,
                     highlightthickness=2)
    frame.pack_propagate(False)

    tk.Label(frame, text=title, bg=bg_color, fg=fg_color, font=("Segoe UI", 14, "bold")).pack(pady=(10, 4))
    tk.Label(frame, text=desc, bg=bg_color, fg=fg_color, font=("Segoe UI", 10), wraplength=240).pack(pady=(0, 5))

    for feat in features:
        tk.Label(frame, text="• " + feat, bg=bg_color, fg=fg_color, font=("Segoe UI", 9)).pack(anchor="w", padx=20)

    tk.Button(frame, text="Launch", command=command, bg=fg_color, fg="white", relief="flat",
              font=("Segoe UI", 10, "bold"), padx=12, pady=6).pack(pady=10)
    return frame

# === Cards Data ===
cards = [
    ("EyePilot", "Control your computer using eye blinks and iris tracking.",
     ["Move cursor with eyes", "Left/Right click by blinking", "Double blink for double click"],
     launch_eye_control, "#e3f2fd", "#1976d2"),

    ("HandNav", "Use hand gestures to navigate and interact with your system.",
     ["Cursor with finger", "Left/Right click gestures", "Scroll and drag supported"],
     launch_hand_control, "#e8f5e9", "#2e7d32"),

    ("VoiceMate", "Talk to your assistant to open apps and get info.",
     ["Say 'use open app command to open'", "Ask time", "Say 'exit' to quit"],
     launch_voice_assistant, "#e0f7fa", "#00838f")
]

for i, (title, desc, feats, cmd, bg, fg) in enumerate(cards):
    create_card(card_frame, title, desc, feats, cmd, bg, fg).grid(row=0, column=i, padx=20, pady=30)

# === Footer ===
footer = tk.Label(root, text="© 2025 Virtual Control Hub • Final Year Project",
                  font=("Segoe UI", 10), bg="#dee2e6", fg="#495057", pady=8)
footer.place(relwidth=1, y=750)

root.mainloop()
