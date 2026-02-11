import cv2
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import winsound
import os
import time
import pandas as pd
from tkinter import filedialog, messagebox


# ================== GLOBALS ==================
running = True
last_beep_time = 0
attendance_records = []

today = datetime.now().strftime("%Y-%m-%d")

# ================== LOAD MODEL ==================
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# ================== LOAD LABELS ==================
label_map = {}
with open("labels.txt", "r") as f:
    for line in f:
        k, v = line.strip().split(",")
        label_map[int(k)] = v

# ================== FACE DETECTOR ==================
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ================== SOUND ==================
sound_path = os.path.join(os.getcwd(), "beep.wav")

# ================== GUI ==================
root = tk.Tk()
root.title("Smart Attendance System")

# ---- window size 80% ----
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
w = int(screen_w * 0.8)
h = int(screen_h * 0.8)
x = (screen_w - w) // 2
y = (screen_h - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")
root.configure(bg="#121212")

# ================== UI ELEMENTS ==================
title = tk.Label(
    root,
    text="Face Recognition Attendance",
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg="#121212"
)
title.pack(pady=10)

video_label = tk.Label(root)
video_label.pack()

status_label = tk.Label(
    root,
    text="Camera Running...",
    font=("Segoe UI", 14),
    fg="lightgreen",
    bg="#121212"
)
status_label.pack(pady=10)

# ================== CAMERA ==================
cam = cv2.VideoCapture(0)
marked_names = set()

# ================== FUNCTIONS ==================
def update_frame():
    global last_beep_time

    if not running:
        return

    ret, frame = cam.read()
    if not ret:
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face)

        if confidence < 70:
            name = label_map[label]

            if name not in marked_names:
                time_now = datetime.now().strftime("%H:%M:%S")
                attendance_records.append([name, today, time_now])
                marked_names.add(name)
                status_label.config(text=f"Attendance marked for {name}")

                if time.time() - last_beep_time > 2:
                    winsound.PlaySound(
                        sound_path,
                        winsound.SND_FILENAME | winsound.SND_ASYNC
                    )
                    last_beep_time = time.time()

            text = name
            color = (0, 255, 0)
        else:
            text = "Unknown"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(
            frame, text, (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2
        )

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(frame))
    video_label.imgtk = img
    video_label.configure(image=img)

    root.after(10, update_frame)

# ================== STOP ATTENDANCE ==================
def stop_attendance():
    global running
    running = False
    cam.release()
    status_label.config(text="Attendance Completed ✅")
    export_btn.pack(pady=15)

# ================== EXPORT EXCEL ==================
def export_excel():
    if not attendance_records:
        messagebox.showwarning("No Data", "No attendance data to export.")
        return

    file_path = filedialog.asksaveasfilename(
        title="Save Attendance File",
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")]
    )

    if not file_path:
        return

    df = pd.DataFrame(
        attendance_records,
        columns=["Name", "Date", "Time"]
    )

    df.to_excel(file_path, index=False)
    messagebox.showinfo("Success", "Attendance exported successfully!")

# ================== BUTTONS ==================
stop_btn = tk.Button(
    root,
    text="Attendance Completed",
    font=("Segoe UI", 14, "bold"),
    bg="#d73a49",
    fg="white",
    command=stop_attendance
)
stop_btn.pack(pady=10)

export_btn = tk.Button(
    root,
    text="Export Attendance to Excel",
    font=("Segoe UI", 14, "bold"),
    bg="#1f6feb",
    fg="white",
    command=export_excel
)
# ❌ not packed initially

# ================== START ==================
update_frame()
root.mainloop()
