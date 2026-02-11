import tkinter as tk
import subprocess
import screeninfo
import os
import sys


# ================= WINDOW SIZE (80%) =================
screen = screeninfo.get_monitors()[0]
WIDTH = int(screen.width * 0.8)
HEIGHT = int(screen.height * 0.8)

root = tk.Tk()
root.title("Smart Attendance System")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="#121212")

x = (screen.width - WIDTH) // 2
y = (screen.height - HEIGHT) // 2
root.geometry(f"+{x}+{y}")

# ================= TITLE =================
title = tk.Label(
    root,
    text="Smart Face Recognition Attendance System",
    font=("Segoe UI", 24, "bold"),
    fg="white",
    bg="#121212"
)
title.pack(pady=30)

status = tk.Label(
    root,
    text="Select an option to continue",
    font=("Segoe UI", 14),
    fg="lightgreen",
    bg="#121212"
)
status.pack(pady=10)

# ================= PYTHONW PATH =================
pythonw = sys.executable.replace("python.exe", "pythonw.exe")

# ================= BUTTON ACTIONS =================
def run_capture():
    status.config(text="Capturing face images...")
    subprocess.Popen(
        [pythonw, "capture_faces.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

def run_train():
    status.config(text="Training model...")
    subprocess.Popen(
        [pythonw, "train_model.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

def run_attendance():
    status.config(text="Starting attendance system...")
    subprocess.Popen(
        [pythonw, "attendance_gui.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

# ================= BUTTON STYLE =================
btn_style = {
    "font": ("Segoe UI", 16, "bold"),
    "width": 25,
    "height": 2,
    "bd": 0
}

# ================= BUTTONS =================
tk.Button(
    root, text="📷 Capture Images",
    bg="#1f6feb", fg="white",
    command=run_capture, **btn_style
).pack(pady=20)

tk.Button(
    root, text="🧠 Train Model",
    bg="#238636", fg="white",
    command=run_train, **btn_style
).pack(pady=20)

tk.Button(
    root, text="✅ Take Attendance",
    bg="#d73a49", fg="white",
    command=run_attendance, **btn_style
).pack(pady=20)

# ================= FOOTER =================
tk.Label(
    root,
    text="Developed by Ritik Kushwaha",
    font=("Segoe UI", 10),
    fg="gray",
    bg="#121212"
).pack(side="bottom", pady=10)

root.mainloop()
