import cv2
import csv
from datetime import datetime
import winsound
import pandas as pd
import os
import time
import numpy as np

# ================= STARTUP SCREEN =================
start_frame = np.zeros((300, 600, 3), dtype=np.uint8)
cv2.putText(start_frame, "Starting Attendance System...",
            (40, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
cv2.imshow("Attendance System", start_frame)
cv2.waitKey(1500)
cv2.destroyAllWindows()

# ================= LOAD MODEL =================
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# ================= LOAD LABELS =================
label_map = {}
with open("labels.txt", "r") as f:
    for line in f:
        key, value = line.strip().split(",")
        label_map[int(key)] = value

# ================= FACE DETECTOR =================
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ================= CAMERA =================
cam = cv2.VideoCapture(0)

# ================= ATTENDANCE FILE =================
attendance_file = "attendance.csv"
marked_names = set()
today = datetime.now().strftime("%Y-%m-%d")

# Load already marked names
if os.path.exists(attendance_file):
    with open(attendance_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[1] == today:
                marked_names.add(row[0])

# ================= SOUND SETUP =================
sound_path = os.path.join(os.getcwd(), "beep.wav")
last_beep_time = 0

# ================= MAIN LOOP =================
with open(attendance_file, "a", newline="") as f:
    writer = csv.writer(f)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face)

            if confidence < 70:
                name = label_map[label]

                if name not in marked_names:
                    time_now = datetime.now().strftime("%H:%M:%S")
                    writer.writerow([name, today, time_now])
                    marked_names.add(name)
                    print(f"Attendance marked for {name}")

                    # 🔊 PLAY BEEP (SAFE + NON-BLOCKING)
                    if time.time() - last_beep_time > 2:
                        try:
                            winsound.PlaySound(
                                sound_path,
                                winsound.SND_FILENAME | winsound.SND_ASYNC
                            )
                        except:
                            winsound.MessageBeep()
                        last_beep_time = time.time()

                text = name
                color = (0, 255, 0)
            else:
                text = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) == 27:  # ESC
            break

# ================= CLEANUP =================
cam.release()
cv2.destroyAllWindows()

# ================= CSV → EXCEL REPORT =================
if os.path.exists(attendance_file):
    df = pd.read_csv(attendance_file, header=None)
    df.columns = ["Name", "Date", "Time"]

    today_df = df[df["Date"] == today]

    summary = today_df["Name"].value_counts().reset_index()
    summary.columns = ["Name", "Entries"]

    with pd.ExcelWriter("attendance_report.xlsx", engine="openpyxl") as writer:
        today_df.to_excel(writer, sheet_name="Attendance", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)

    print("Excel report generated successfully")
